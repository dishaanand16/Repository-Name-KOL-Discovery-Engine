import json

import numpy as np

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


EMBED_FILE=(

"outputs/processed/doctor_embeddings.npy"

)

PROFILE_FILE=(

"outputs/processed/doctor_profiles.json"

)

OUTPUT_FILE=(

"outputs/processed/similarity_matrix.csv"

)


def build_similarity():

    embeddings=np.load(

        EMBED_FILE

    )

    similarities=cosine_similarity(

        embeddings

    )

    with open(

        PROFILE_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        profiles=json.load(

            f

        )

    doctor_names=[

        x["doctor_name"]

        for x in profiles

    ]

    df=pd.DataFrame(

        similarities,

        columns=doctor_names,

        index=doctor_names

    )

    df.to_csv(

        OUTPUT_FILE

    )

    print(

        df.round(

            2

        )

    )


if __name__=="__main__":

    build_similarity()