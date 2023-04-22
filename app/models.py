from dataclasses import dataclass
from typing import List
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSONB, JSON
import json

from app import db


@dataclass
class SearchTerm(db.Model):
    __tablename__ = "search_terms"
    resource: str = db.Column(db.String(100), primary_key=True)
    term: str = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return f"{self.resource} - {self.term}"

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_term(cls, term):
        return cls.query.filter(cls.term.like(f"%{term}%")).all()

    # funtion to save list of search terms
    @classmethod
    def save_all(cls, terms):
        db.session.add_all(terms)
        db.session.commit()
        return terms


@dataclass
class GDCCases(db.Model):
    __tablename__ = "gdc_cases"
    case_id: str = db.Column(db.String(100), primary_key=True)
    primary_site: str = db.Column(db.String(100))
    disease_type: str = db.Column(db.String(100))
    primary_diagnosis: str = db.Column(db.String(100))
    submitter_id: str = db.Column(db.String(100))
    tissue_source_site: str = db.Column(db.String(100))
    site_of_resection_or_biopsy: str = db.Column(db.String(100))
    year_of_diagnosis: str = db.Column(db.String(100))
    age_at_diagnosis: str = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.case_id} - {self.submitter_id}: {self.primary_diagnosis}"

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def serialize(self):
        return {
            "case_id": self.case_id,
            "primary_site": self.primary_site,
            "disease_type": self.disease_type,
            "primary_diagnosis": self.primary_diagnosis,
            "submitter_id": self.submitter_id,
            "tissue_source_site": self.tissue_source_site,
            "site_of_resection_or_biopsy": self.site_of_resection_or_biopsy,
            "year_of_diagnosis": self.year_of_diagnosis,
            "age_at_diagnosis": self.age_at_diagnosis
        }


@dataclass
class ClinicalTrials(db.Model):
    __tablename__ = "clinical_trials"
    term: str = db.Column(db.String(100), primary_key=True)
    title: str = db.Column(db.String(1000), primary_key=True)
    official_title: str = db.Column(db.String(1000))
    phase: str = db.Column(db.String(100))
    status: str = db.Column(db.String(100))
    age: list = db.Column(db.String(100))
    gender: str = db.Column(db.String(100))
    description: str = db.Column(db.String(10000))
    summary: str = db.Column(db.String(10000))
    study_type: str = db.Column(db.String(100))
    study_design: dict = db.Column(JSON)
    condition: str = db.Column(db.String(100))
    intervention: dict = db.Column(JSON)
    study_completion_date: str = db.Column(db.String(100))
    primary_completion_date: str = db.Column(db.String(100))
    eligibility_criteria: str = db.Column(db.String(1000))
    investigator: dict = db.Column(JSON)
    collaborators: dict = db.Column(JSON)
    nct_id: str = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.term} - {self.title}: {self.phase}"

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def save_all(cls, trials):
        db.session.add_all(trials)
        db.session.commit()
        return trials

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_term(cls, term):
        # search all columns for the term in or statement
        return cls.query.filter(cls.term.like(f"%{term}%")).all()

    @classmethod
    def get_by_term_and_filters(cls, term, filters):
        # go through each filter and add to the query with and statement
        query = cls.query.filter(cls.term.like(f"%{term}%"))
        print(filters)
        for key, values in filters.items():
            print(f'key: {key}, values: {values}')
            for value in values:
                if value:
                    print(f'{getattr(cls, key).like(f"%{value}%")}')
                    query = query.filter(getattr(cls, key).like(f"%{value}%"))
        return query.all()
    
    # write class to compare two clinical trials
    def __eq__(self, other):
        if not isinstance(other, ClinicalTrials):
            return False
        return self.term == other.term and self.title == other.title

    @classmethod
    def to_json(cls, trials):
        def default(obj):
            if isinstance(obj, ClinicalTrials):
                return obj.__dict__
            return obj

        return json.dumps(trials, default=default)

@dataclass
class ClinicalTrialsFilters:
    age: List[str] = ("Child", "Adult", "Older Adult")
    gender: List[str] = ("All", "Female", "Male")
    phase: List[str] = (
        "Early Phase 1",
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "Phase 4",
        "Not Applicable",
    )
    status: List[str] = (
        "Not yet recruiting",
        "Recruiting",
        "Enrolling by invitation",
        "Active, not recruiting",
        "Completed",
        "Terminated",
        "Suspended",
        "Withdrawn",
        "Unknown status",
    )

