import requests


def fetch_trials(

        doctor_name

):

    url=(

"https://clinicaltrials.gov/api/query/study_fields"

    )

    search_name = doctor_name.replace(

        " ",

        "+"

    )

    params={

        "expr":search_name,

        "fields":"NCTId,LeadSponsorName,BriefTitle",

        "min_rnk":1,

        "max_rnk":50,

        "fmt":"json"

    }

    try:

        response=requests.get(

            url,

            params=params,

            timeout=30

        )

        data=response.json()

        studies=data[

            "StudyFieldsResponse"

        ][

            "StudyFields"

        ]

        trial_ids=[]

        for study in studies:

            if len(

                study["NCTId"]

            )>0:

                trial_ids.append(

                    study["NCTId"][0]

                )

        return {

            "trial_count":

                len(

                    trial_ids

                ),

            "trial_ids":

                trial_ids

        }

    except Exception:

        return {

            "trial_count":0,

            "trial_ids":[]

        }


if __name__=="__main__":

    print(

        fetch_trials(

            "Eric Topol"

        )

    )