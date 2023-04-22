# %%
import asyncio
import concurrent.futures
import json
import os
import ast

import requests
from flask import Flask, jsonify, request

from app import app, db
from app.data_extraction import (
    get_seers_disease_data,
    get_seers_glossary_data,
    get_seers_ndc_data,
    get_seers_rx_data,
    get_seers_surgery_data,
    get_clinicaltrials_gov,
)
from app.models import SearchTerm, ClinicalTrials, ClinicalTrialsFilters, GDCCases
from app.utils import SearchTreeNode, find_tag

# %%


# route for / and /seers_data
@app.route("/", methods=["GET"])
def seers_data(args={"version": "latest", "year": "latest"}):
    base_url = "https://api.seer.cancer.gov/"

    # list of all endpoints
    endpoints = {
        "disease": "rest/disease/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
        "glossary": "rest/glossary/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
        "ndc": "rest/ndc?include_removed=false&page={offset}&per_page={count}",
        "surgery": "rest/surgery/{year}/tables",
        "rx": "rest/rx/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
    }

    # create .cache folder if it doesn't exist
    if not os.path.exists("app/.cache"):
        os.makedirs("app/.cache")

    # check if resource column has any data with disease value
    if not db.session.query(
        SearchTerm.query.filter_by(resource="disease").exists()
    ).scalar():
        disease_data = get_seers_disease_data(base_url, endpoints)
        # store disease data in database
        disease_objects = []
        for disease in disease_data:
            disease_objects.append(SearchTerm(resource="disease", term=disease.strip()))
        SearchTerm.save_all(disease_objects)
        print("disease data saved")

    # check if resource column has any data with glossary value
    if not db.session.query(
        SearchTerm.query.filter_by(resource="glossary").exists()
    ).scalar():
        glossary_data = get_seers_glossary_data(base_url, endpoints)
        # store glossary data in database
        glossary_objects = []
        for glossary in glossary_data:
            glossary_objects.append(
                SearchTerm(resource="glossary", term=glossary.strip())
            )
        SearchTerm.save_all(glossary_objects)
        print("glossary data saved")

    # check if resource column has any data with ndc value
    if not db.session.query(
        SearchTerm.query.filter_by(resource="ndc").exists()
    ).scalar():
        ndc_data = get_seers_ndc_data(base_url, endpoints)
        # store ndc data in database
        ndc_objects = []
        for ndc in ndc_data:
            ndc_objects.append(SearchTerm(resource="ndc", term=ndc.strip()))
        SearchTerm.save_all(ndc_objects)
        print("ndc data saved")

    # check if resource column has any data with surgery value
    if not db.session.query(
        SearchTerm.query.filter_by(resource="surgery").exists()
    ).scalar():
        surgery_data = get_seers_surgery_data(base_url, endpoints)
        # store surgery data in database
        surgery_objects = []
        for surgery in surgery_data:
            surgery_objects.append(SearchTerm(resource="surgery", term=surgery.strip()))
        SearchTerm.save_all(surgery_objects)
        print("surgery data saved")

    # check if resource column has any data with rx value
    if not db.session.query(
        SearchTerm.query.filter_by(resource="rx").exists()
    ).scalar():
        rx_data = get_seers_rx_data(base_url, endpoints)
        # store rx data in database
        rx_objects = []
        for rx in rx_data:
            rx_objects.append(SearchTerm(resource="rx", term=rx.strip()))
        SearchTerm.save_all(rx_objects)
        print("rx data saved")

    return "data saved"


@app.route("/search_terms", methods=["GET"])
def search_terms():
    args = request.args
    if args:
        term = args["term"]

        data = SearchTerm.get_by_term(term)
    else:
        data = SearchTerm.get_all()

    return jsonify(data)


@app.route("/clinical_trials", methods=["GET"])
def get_clinical_trials():
    args = request.args

    expr = args.get("expr", "")
    num_results = args.get("num_results", 10)
    if expr != "":
        # get everything before AND
        expr = expr.split("&")[0]

    age_filter = args.get("age_filter", [])
    gender_filter = args.get("gender_filter", [])
    phase_filter = args.get("phase_filter", [])
    status_filter = args.get("status_filter", [])

    filters = {
        "age": ast.literal_eval(age_filter) if age_filter else age_filter,
        "gender": ast.literal_eval(gender_filter) if gender_filter else gender_filter,
        "phase": ast.literal_eval(phase_filter) if phase_filter else phase_filter,
        "status": ast.literal_eval(status_filter) if status_filter else status_filter,
    }

    print("filters", filters)

    # clinical_trials_objects_db = ClinicalTrials.get_by_term_and_filters(expr, filters)
    clinical_trials_objects_db_wo_filters = ClinicalTrials.get_by_term(expr)
    # check if we have num_results other wise call clinical trials api

    # check if term is in database
    if not clinical_trials_objects_db_wo_filters or len(
        clinical_trials_objects_db_wo_filters
    ) < int(num_results):
        print("clinical trials not in database")
        clinical_trials = get_clinicaltrials_gov(args, max_results=100)

        # store clinical trials data in database
        clinical_trials_objects = []
        for clinical_trial in clinical_trials:
            ct = ClinicalTrials(
                term=expr,
                # title=clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("IdentificationModule", {}).get("BriefTitle", None),
                title=find_tag(clinical_trial, "BriefTitle"),
                # phase=clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("DesignModule", {}).get("PhaseList", {}).get("Phase", None),
                # phase='' if ','.join(clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("DesignModule", {}).get("PhaseList", {}).get("Phase", [])) == '' else ','.join(clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("DesignModule", {}).get("PhaseList", {}).get("Phase", [])),
                phase="Not Applicable"
                if find_tag(clinical_trial, "Phase") is None
                else ",".join(find_tag(clinical_trial, "Phase")),
                # make sure phase has value from ClinicalTrialsFilter dataclasses
                # status='Unknown status' if clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("StatusModule", {}).get("OverallStatus", None) is None else clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("StatusModule", {}).get("OverallStatus", None),
                status="Unknown status"
                if find_tag(clinical_trial, "OverallStatus") is None
                else find_tag(clinical_trial, "OverallStatus"),
                # age=','.join(clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("EligibilityModule", {}).get("StdAgeList", {}).get("StdAge", [])),
                age=",".join(find_tag(clinical_trial, "StdAge")),
                # gender='' if clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("StatusModule", {}).get("Gender", None) is None else  clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("StatusModule", {}).get("Gender", None),
                gender=find_tag(clinical_trial, "Gender"),
                # description=clinical_trial.get("Study", {}).get("ProtocolSection", {}).get("DescriptionModule", {}).get("DetailedDescription", None),
                description=find_tag(clinical_trial, "DetailedDescription"),
                official_title=find_tag(clinical_trial, "OfficialTitle"),
                summary=find_tag(clinical_trial, "BriefSummary"),
                study_type=find_tag(clinical_trial, "StudyType"),
                study_design=find_tag(clinical_trial, "DesignInfo"),
                condition=find_tag(clinical_trial, "Condition")[0],
                intervention=find_tag(clinical_trial, "Intervention"),
                study_completion_date=find_tag(clinical_trial, "CompletionDate"),
                primary_completion_date=find_tag(clinical_trial, "PrimaryCompletionDate"),
                eligibility_criteria=find_tag(clinical_trial, "EligibilityCriteria"),
                investigator=find_tag(clinical_trial, "OverallOfficial"),
                collaborators=find_tag(clinical_trial, "Collaborator"),
                nct_id=find_tag(clinical_trial, "NCTId"),

            )
            # make sure we don't have duplicates
            if ct not in clinical_trials_objects:
                # db should also not have duplicates
                if ct not in clinical_trials_objects_db_wo_filters:
                    # print(f"adding {ct.title} to database {ct.phase}")
                    clinical_trials_objects.append(ct)

        # save clinical trials objects to database
        ClinicalTrials.save_all(clinical_trials_objects)

    # create Tree
    root = SearchTreeNode("term", f"{args.get('term', default='').split(' AND ')[0]}")

    # get clinical trials from database
    clinical_trials_objects_db = ClinicalTrials.get_by_term_and_filters(expr, filters)
    for clinical_trial in clinical_trials_objects_db:
        root.records.append(clinical_trial)

    # print(f'root records {len(root.records)}')
    # create tree
    root.create_search_tree()

    # store tree to json file
    tree_dict = root.to_dict()
    with open("clinical_trials_tree.json", "w") as f:
        json.dump(tree_dict, f, indent=4)

    # return jsonify(root.serialize())
    # make dataclasses as dict and return
    # return jsonify(root.serialize())
    return jsonify(root.get_filtered_records(filters, num_records=num_results))


@app.route("/gdc_cases", methods=["GET"])
def gdc_cases():
    primary_diagnosis = request.args.get("primary_diagnosis", default="", type=str)
    from_idx = request.args.get("from", default=0, type=int)
    size_idx = request.args.get("size", default=100, type=int)

    print(primary_diagnosis, from_idx, size_idx)
    filter = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "diagnoses.primary_diagnosis",
                    "value": ["*" + primary_diagnosis + "*"],
                },
            },
        ],
    }

    params = {
        "filters": json.dumps(filter),
        "expand": ["diagnoses"],
        "format": "JSON",
        "from": from_idx,
        "size": size_idx,
    }

    cases_endpoint = "https://api.gdc.cancer.gov/cases"

    response = requests.get(cases_endpoint, params=params)

    # create GDC objects

    # get all cases
    cases = response.json()["data"]["hits"]

    gdc_list = []
    for case in cases:
        gdc = GDCCases(
            case_id=case["id"],
            primary_site=case["primary_site"],
            disease_type=case["disease_type"],
            primary_diagnosis=case["diagnoses"][0]["primary_diagnosis"],
            submitter_id=case["submitter_id"],
            tissue_source_site=case["diagnoses"][0]["tissue_or_organ_of_origin"],
            year_of_diagnosis=case["diagnoses"][0].get("year_of_diagnosis", None),
            age_at_diagnosis=case["diagnoses"][0]["age_at_diagnosis"] // 365 if case["diagnoses"][0]["age_at_diagnosis"] else None,
        )
    
        gdc_list.append(gdc)


    return jsonify([gdc.serialize() for gdc in gdc_list]) 
    # return response.json()

#####################################################################################
