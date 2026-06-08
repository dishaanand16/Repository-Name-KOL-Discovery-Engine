import json

import pandas as pd


INPUT_FILE=(

"outputs/processed/doctor_profiles.json"

)

OUTPUT_FILE=(

"outputs/processed/influence_scores.csv"

)


def normalize(

        values

):

    minimum=min(

        values

    )

    maximum=max(

        values

    )

    if maximum==minimum:

        return [

            1

            for _ in values

        ]

    return [

        (

            x-minimum

        )/

        (

            maximum-minimum

        )

        for x in values

    ]


def generate_scores():

    with open(

        INPUT_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        profiles=json.load(

            f

        )

    citations=[

        p.get(

            "citations",

            0

        ) or 0

        for p in profiles

    ]

    publications=[

        p.get(

            "publication_count",

            0

        ) or 0

        for p in profiles

    ]

    hindex=[

        p.get(

            "h_index",

            0

        ) or 0

        for p in profiles

    ]

    payments=[

        p.get(

            "payments",

            {}

        ).get(

            "total_payment",

            0

        ) or 0

        for p in profiles

    ]

    c_norm=normalize(

        citations

    )

    p_norm=normalize(

        publications

    )

    h_norm=normalize(

        hindex

    )

    pay_norm=normalize(

        payments

    )

    rows=[]

    for i,p in enumerate(

        profiles

    ):

        score=(

            0.35*c_norm[i]

            +

            0.30*p_norm[i]

            +

            0.20*h_norm[i]

            +

            0.15*pay_norm[i]

        )

        rows.append(

            {

                "doctor":

                    p["doctor_name"],

                "influence_score":

                    round(

                        score,

                        4

                    )

            }

        )

    df=pd.DataFrame(

        rows

    )

    df=df.sort_values(

        "influence_score",

        ascending=False

    )

    df.to_csv(

        OUTPUT_FILE,

        index=False

    )

    print(

        df

    )


if __name__=="__main__":

    generate_scores()