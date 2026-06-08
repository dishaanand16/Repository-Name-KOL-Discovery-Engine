import pandas as pd

import json

from tqdm import tqdm

from src.api.serp_api import (

    search_doctor,

    fetch_full_profile

)

from src.api.cms_api import (

    fetch_payments

)


INPUT_FILE=(

    "data/raw/doctor_list.csv"

)

OUTPUT_FILE=(

    "outputs/processed/doctor_profiles.json"

)


def build_profiles():

    df=pd.read_csv(

        INPUT_FILE

    )

    profiles=[]

    for doctor_name in tqdm(

        df["doctor_name"]

    ):

        try:

            doctor=search_doctor(

                doctor_name

            )

            if doctor is None:

                print(

                    f"Skipping {doctor_name}"

                )

                continue

            profile=fetch_full_profile(

                doctor["author_id"],

                doctor_name

            )

            payments=fetch_payments(

                doctor_name

            )

            profile[

                "payments"

            ]=payments


            #####################################

            # CONFIDENCE SCORES

            #####################################

            profile[

                "confidence_scores"

            ]={

                "specialty":

                    0.95

                    if profile.get(

                        "specialty"

                    )

                    else 0.40,

                "therapy_area":

                    0.90

                    if profile.get(

                        "therapy_area"

                    )

                    else 0.40,

                "geography":

                    0.90

                    if profile.get(

                        "geography"

                    )

                    else 0.40,

                "citations":

                    0.95

                    if profile.get(

                        "citations"

                    )

                    else 0.30,

                "payments":

                    0.90

                    if payments.get(

                        "payment_count",

                        0

                    )>0

                    else 0.30,

                "trials":

                    0.85

                    if profile.get(

                        "trials",

                        {}

                    ).get(

                        "trial_count",

                        0

                    )>0

                    else 0.30

            }

            profiles.append(

                profile

            )

        except Exception as e:

            print(

                doctor_name,

                e

            )

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            profiles,

            f,

            indent=4,

            ensure_ascii=False

        )

    print(

        f"\nSaved {len(profiles)} profiles"

    )


if __name__=="__main__":

    build_profiles()