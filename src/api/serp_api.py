import os

import streamlit as st

import requests

from serpapi import GoogleSearch

from dotenv import load_dotenv


load_dotenv()


SERP_KEY=(

    os.getenv(

        "SERP_API_KEY"

    )

    or

    st.secrets.get(

        "SERP_API_KEY",

        None

    )

)


if SERP_KEY is None:

    raise Exception(

        "SERP_API_KEY not found"

    )


#####################################################

# SEARCH DOCTOR

#####################################################

def search_doctor(

        doctor_name

):

    params = {

        "engine":"google_scholar",

        "q":doctor_name,

        "api_key":SERP_KEY

    }

    results = GoogleSearch(

        params

    ).get_dict()

    profiles = results.get(

        "profiles",

        {}

    )

    authors = profiles.get(

        "authors",

        []

    )

    if len(authors)==0:

        return None

    return authors[0]


#####################################################

# EXTRACT GEOGRAPHY

#####################################################

def extract_geography(

        affiliation

):

    affiliation = affiliation.lower()

    geography_map = {

        "stanford":"USA",

        "harvard":"USA",

        "scripps":"USA",

        "mayo":"USA",

        "johns hopkins":"USA",

        "cleveland clinic":"USA",

        "toronto":"Canada",

        "cambridge":"UK",

        "oxford":"UK"

    }

    for key,value in geography_map.items():

        if key in affiliation:

            return value

    return "Unknown"


#####################################################

# FETCH TRIALS

#####################################################

def fetch_trials(

        doctor_name

):

    url=(

"https://clinicaltrials.gov/api/query/study_fields"

    )

    params={

        "expr":doctor_name,

        "fields":"NCTId",

        "min_rnk":1,

        "max_rnk":100,

        "fmt":"json"

    }

    try:

        response=requests.get(

            url,

            params=params,

            timeout=20

        )

        data=response.json()

        studies=data[

            "StudyFieldsResponse"

        ][

            "StudyFields"

        ]

        return {

            "trial_count":

                len(

                    studies

                ),

            "trial_ids":[

                x["NCTId"][0]

                for x in studies

                if len(

                    x["NCTId"]

                )>0

            ]

        }

    except:

        return {

            "trial_count":0,

            "trial_ids":[]

        }


#####################################################

# FULL PROFILE

#####################################################

def fetch_full_profile(

        author_id,

        doctor_name

):

    params = {

        "engine":"google_scholar_author",

        "author_id":author_id,

        "api_key":SERP_KEY

    }

    results = GoogleSearch(

        params

    ).get_dict()

    author = results.get(

        "author",

        {}

    )

    cited = results.get(

        "cited_by",

        {}

    )

    interests=[

        x.get(

            "title"

        )

        for x in author.get(

            "interests",

            []

        )

    ]

    affiliation = author.get(

        "affiliations",

        ""

    )

    trials = fetch_trials(

        doctor_name

    )

    profile={

        "doctor_name":

            author.get(

                "name"

            ),

        "affiliation":

            affiliation,

        "email":

            author.get(

                "email"

            ),

        "specialty":

            interests[0]

            if len(

                interests

            )>0

            else None,

        "therapy_area":

            interests,

        "geography":

            extract_geography(

                affiliation

            ),

        "citations":

            cited.get(

                "table",

                [{}]

            )[0].get(

                "citations",

                {}

            ).get(

                "all"

            ),

        "h_index":

            cited.get(

                "table",

                [{},{}]

            )[1].get(

                "h_index",

                {}

            ).get(

                "all"

            ),

        "i10_index":

            cited.get(

                "table",

                [{},{},{}]

            )[2].get(

                "i10_index",

                {}

            ).get(

                "all"

            ),

        "publication_count":

            len(

                results.get(

                    "articles",

                    []

                )

            ),

        "trials":

            trials

    }

    return profile


#####################################################

# TEST

#####################################################

if __name__=="__main__":

    doctor = search_doctor(

        "Eric Topol"

    )

    profile = fetch_full_profile(

        doctor["author_id"],

        "Eric Topol"

    )

    print(

        "\nFINAL PROFILE:\n"

    )

    print(

        profile

    )