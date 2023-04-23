import concurrent.futures
import os
import json

import requests

from app import app


# Define a function to fetch a single URL
def fetch_url(url, headers=None):
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    response = session.get(url)
    if response.status_code != 200:
        print("Error fetching url: ", url)
        return None
    return response.json()


def get_seers_disease_data(
    base_url, endpoints, version="latest", count=100, offset=0, num_workers=4
):
    seers_api_key = os.environ.get("SEERS_API_KEY")

    # Create a list of URLs to fetch
    urls = [
        base_url
        + endpoints["disease"].format(
            version=version, count=count, offset=offset + i * count
        )
        for i in range(num_workers)
    ]

    headers = {"X-SEERAPI-KEY": seers_api_key}

    # Use a ThreadPoolExecutor to fetch all URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = []
        while True:
            # Submit all URL fetches to the executor
            future_list = [executor.submit(fetch_url, url, headers) for url in urls]

            # Wait for all URL fetches to complete
            for future in concurrent.futures.as_completed(future_list):
                response = future.result()
                if "results" in response:
                    results.extend(response["results"])
                    offset += count
                    urls = [
                        base_url
                        + endpoints["disease"].format(
                            version=version, count=count, offset=offset + i * count
                        )
                        for i in range(num_workers)
                    ]
                else:
                    break
            else:
                continue
            break

    # write cache
    with open("app/.cache/disease_data1.json", "w") as f:
        json.dump(results, f, indent=2)

    # return all results with key "name"
    # return [result["name"] for result in results]
    # return unique results
    return list(set([result["name"] for result in results]))


def get_seers_glossary_data(
    base_url, endpoints, version="latest", count=100, offset=0, num_workers=4
):
    seers_api_key = os.environ.get("SEERS_API_KEY")

    # Create a list of URLs to fetch
    urls = [
        base_url
        + endpoints["glossary"].format(
            version=version, count=count, offset=offset + i * count
        )
        for i in range(num_workers)
    ]

    headers = {"X-SEERAPI-KEY": seers_api_key}

    # Use a ThreadPoolExecutor to fetch all URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = []
        while True:
            # Submit all URL fetches to the executor
            future_list = [executor.submit(fetch_url, url, headers) for url in urls]

            # Wait for all URL fetches to complete
            for future in concurrent.futures.as_completed(future_list):
                response = future.result()
                if "results" in response:
                    results.extend(response["results"])
                    offset += count
                    urls = [
                        base_url
                        + endpoints["glossary"].format(
                            version=version, count=count, offset=offset + i * count
                        )
                        for i in range(num_workers)
                    ]
                else:
                    break
            else:
                continue
            break

    # write cache
    with open("app/.cache/glossary_data1.json", "w") as f:
        json.dump(results, f, indent=2)

    # return [result["name"] for result in results]
    return list(set([result["name"] for result in results]))


def get_seers_rx_data(
    base_url, endpoints, version="latest", count=100, offset=0, num_workers=4
):
    seers_api_key = os.environ.get("SEERS_API_KEY")

    # Create a list of URLs to fetch
    urls = [
        base_url
        + endpoints["rx"].format(
            version=version, count=count, offset=offset + i * count
        )
        for i in range(num_workers)
    ]

    headers = {"X-SEERAPI-KEY": seers_api_key}

    # Use a ThreadPoolExecutor to fetch all URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = []
        while True:
            # Submit all URL fetches to the executor
            future_list = [executor.submit(fetch_url, url, headers) for url in urls]

            # Wait for all URL fetches to complete
            for future in concurrent.futures.as_completed(future_list):
                response = future.result()
                if "results" in response:
                    results.extend(response["results"])
                    offset += count
                    urls = [
                        base_url
                        + endpoints["rx"].format(
                            version=version, count=count, offset=offset + i * count
                        )
                        for i in range(num_workers)
                    ]
                else:
                    break
            else:
                continue
            break

    # write cache
    with open("app/.cache/rx_data1.json", "w") as f:
        json.dump(results, f, indent=2)

    # return [result["name"] for result in results]
    return list(set([result["name"] for result in results]))


def get_seers_ndc_data(base_url, endpoints, count=100, offset=1, num_workers=4):
    seers_api_key = os.environ.get("SEERS_API_KEY")
    # Create a list of URLs to fetch
    urls = [
        base_url + endpoints["ndc"].format(count=count, offset=offset + i * count)
        for i in range(num_workers)
    ]

    headers = {"X-SEERAPI-KEY": seers_api_key}

    # Use a ThreadPoolExecutor to fetch all URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = []
        while True:
            # Submit all URL fetches to the executor
            future_list = [executor.submit(fetch_url, url, headers) for url in urls]

            # Wait for all URL fetches to complete
            for future in concurrent.futures.as_completed(future_list):
                response = future.result()
                if response:
                    results.extend(response)
                    offset += count
                    urls = [
                        base_url
                        + endpoints["ndc"].format(
                            count=count, offset=offset + i * count
                        )
                        for i in range(num_workers)
                    ]
                else:
                    break
            else:
                continue
            break

    # write cache
    with open("app/.cache/ndc_data1.json", "w") as f:
        json.dump(results, f, indent=2)

    # return [result["proprietary_name"] for result in results]
    # return list(set([result["proprietary_name"] for result in results]))
    # prettify and return
    # results = results[5:]
    prop_name = set([result["proprietary_name"] for result in results])
    non_prop_name = set(
        [
            x.strip()
            for result in results
            for x in result["non_proprietary_name"][0].split(",")
        ]
    )
    # merge prop_name and non_prop_name
    return list(prop_name.union(non_prop_name))


def get_seers_surgery_data(base_url, endpoints, year="latest"):
    seers_api_key = os.environ.get("SEERS_API_KEY")

    # get surgery data
    surgery_url = base_url + endpoints["surgery"]

    headers = {"X-SEERAPI-KEY": seers_api_key}

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(surgery_url.format(year=year))

    # write cache
    with open("app/.cache/surgery_data.json", "w") as f:
        json.dump(response.json(), f, indent=2)

    # return response.json()
    return list(set(response.json()))


def get_clinicaltrials_gov(args, max_results=1000, num_workers=4):

    expr = args.get("expr", default="", type=str)
    min_rnk = args.get("min_rnk", default=1, type=int)
    max_rnk = args.get("max_rnk", default=100, type=int)
    max_rnk = min(max_rnk, max_results)
    fmt = args.get("fmt", default="json", type=str)

    base_url = "https://clinicaltrials.gov/api/query/full_studies"

    query = "?expr={expr}&min_rnk={min_rnk}&max_rnk={max_rnk}&fmt={fmt}"

    urls = [
        base_url  + query.format(expr=expr, min_rnk=min_rnk + i * max_rnk, max_rnk=max_rnk + i * max_rnk, fmt=fmt) for i in range(max_results // max_rnk)
    ]   

    # Use a ThreadPoolExecutor to fetch all URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = []
        # Submit all URL fetches to the executor
        future_list = [executor.submit(fetch_url, url) for url in urls]

        # Wait for all URL fetches to complete
        for future in concurrent.futures.as_completed(future_list):
            response = future.result()
            if response:
                # results.extend(response.get(["FullStudiesResponse"]["FullStudies"])
                results.extend(response.get("FullStudiesResponse", {}).get("FullStudies", []))
            else:
                break

    # # write cache
    with open("clinical_trials_data.json", "w") as f:
        json.dump(results, f, indent=2)

    return results




# def get_seers_disease_data(base_url, endpoints, version="latest", count=100, offset=0):
#     # get disease data
#     disease_url = base_url + endpoints["disease"]

#     headers = {"X-SEERAPI-KEY": seers_api_key}

#     session = requests.Session()
#     session.headers.update(headers)

#     # loop through till there is no more results key
#     results = []
#     while True:
#         response = session.get(
#             disease_url.format(version=version, count=count, offset=offset)
#         )
#         print("Getting disease data... for offset: ", offset)
#         if "results" in response.json():
#             offset += count
#         else:
#             break
#         results.extend(response.json()["results"])

#     # write cache
#     with open("app/.cache/disease_data.json", "w") as f:
#         json.dump(results, f, indent=2)

#     # return all results with key "name"
#     # return [result["name"] for result in results]
#     # return unique results
#     return list(set([result["name"] for result in results]))


# def get_seers_glossary_data(base_url, endpoints, version="latest", count=100, offset=0):
#     # get glossary data
#     glossary_url = base_url + endpoints["glossary"]

#     headers = {"X-SEERAPI-KEY": seers_api_key}

#     session = requests.Session()
#     session.headers.update(headers)

#     # loop through till there is no more results key
#     results = []
#     while True:
#         response = session.get(
#             glossary_url.format(version=version, count=count, offset=offset)
#         )
#         print("Getting glossary data... for offset: ", offset)
#         if "results" in response.json():
#             offset += count
#         else:
#             break
#         results.extend(response.json()["results"])

#     # write cache
#     with open("app/.cache/glossary_data.json", "w") as f:
#         json.dump(results, f, indent=2)

#     # return [result["name"] for result in results]
#     return list(set([result["name"] for result in results]))

# def get_seers_ndc_data(base_url, endpoints, count=100, offset=0):
#     # get ndc data
#     ndc_url = base_url + endpoints["ndc"]

#     headers = {"X-SEERAPI-KEY": seers_api_key}

#     session = requests.Session()
#     session.headers.update(headers)

#     # loop through till there is no more results key
#     results = []
#     while True:
#         response = session.get(ndc_url.format(count=count, offset=offset))
#         print("Getting ndc data... for offset: ", offset)

#         # if response is not empty
#         if response.json():
#             offset += count
#         else:
#             break

#         results.extend(response.json())

#     # write cache
#     with open("app/.cache/ndc_data.json", "w") as f:
#         json.dump(results, f, indent=2)

#     # return [result["proprietary_name"] for result in results]
#     # return list(set([result["proprietary_name"] for result in results]))
#     # prettify and return
#     results = results[5:]
#     prop_name = set([result["proprietary_name"] for result in results])
#     non_prop_name = set(
#         [
#             x.strip()
#             for result in results
#             for x in result["non_proprietary_name"][0].split(",")
#         ]
#     )
#     # merge prop_name and non_prop_name
#     return list(prop_name.union(non_prop_name))

# def get_seers_rx_data(base_url, endpoints, version="latest", count=100, offset=0):
#     # get rx data
#     rx_url = base_url + endpoints["rx"]

#     headers = {"X-SEERAPI-KEY": seers_api_key}

#     session = requests.Session()
#     session.headers.update(headers)

#     # loop through till there is no more results key
#     results = []
#     while True:
#         response = session.get(
#             rx_url.format(version=version, count=count, offset=offset)
#         )
#         print("Getting rx data... for offset: ", offset)
#         if "results" in response.json():
#             offset += count
#         else:
#             break
#         results.extend(response.json()["results"])

#     # write cache
#     with open("app/.cache/rx_data.json", "w") as f:
#         json.dump(results, f, indent=2)

#     # return [result["name"] for result in results]
#     return list(set([result["name"] for result in results]))
#     # return jsonify(results)

# def get_seers_rx_data(base_url, endpoints, version="latest", count=100, offset=0):
#     # get rx data
#     rx_url = base_url + endpoints["rx"]

#     headers = {"X-SEERAPI-KEY": seers_api_key}

#     session = requests.Session()
#     session.headers.update(headers)

#     # loop through till there is no more results key
#     results = []
#     while True:
#         response = session.get(
#             rx_url.format(version=version, count=count, offset=offset)
#         )
#         print("Getting rx data... for offset: ", offset)
#         if "results" in response.json():
#             offset += count
#         else:
#             break
#         results.extend(response.json()["results"])

#     # write cache
#     with open("app/.cache/rx_data.json", "w") as f:
#         json.dump(results, f, indent=2)

#     # return [result["name"] for result in results]
#     return list(set([result["name"] for result in results]))
#     # return jsonify(results)


# %%

# base_url = "https://api.seer.cancer.gov/"

# # list of all endpoints
# endpoints = {
#     "disease": "rest/disease/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
#     "glossary": "rest/glossary/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
#     "ndc": "rest/ndc?include_removed=false&page={offset}&per_page={count}",
#     "surgery": "rest/surgery/{year}/tables",
#     "rx": "rest/rx/{version}?mode=OR&count={count}&offset={offset}&output_type=MIN&glossary=false",
# }


# if not os.path.exists("disease_data.json"):
#     disease_data = get_seers_disease_data(base_url, endpoints)
# else:
#     with open("disease_data.json", "r") as f:
#         disease_data = json.load(f)

# if not os.path.exists("glossary_data.json"):
#     glossary_data = get_seers_glossary_data(base_url, endpoints)
# else:
#     with open("glossary_data.json", "r") as f:
#         glossary_data = json.load(f)

# if not os.path.exists("rx_data.json"):
#     rx_data = get_seers_rx_data(base_url, endpoints)
# else:
#     with open("rx_data.json", "r") as f:
#         rx_data = json.load(f)

# if not os.path.exists("ndc_data.json"):
#     ndc_data = get_seers_ndc_data(base_url, endpoints)
# else:
#     with open("ndc_data.json", "r") as f:
#         ndc_data = json.load(f)

# if not os.path.exists("surgery_data.json"):
#     surgery_data = get_seers_surgery_data(base_url, endpoints)
# else:
#     with open("surgery_data.json", "r") as f:
#         surgery_data = json.load(f)

# # %%


# print(len(disease_data))
# print(len(glossary_data))
# print(len(rx_data))
# print(len(ndc_data))
# print(len(surgery_data))


# # %%
