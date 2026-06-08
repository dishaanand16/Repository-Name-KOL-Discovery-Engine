import numpy as np

import json

import pandas as pd

from sklearn.cluster import KMeans


EMBEDDINGS=(

"outputs/processed/doctor_embeddings.npy"

)

PROFILES=(

"outputs/processed/doctor_profiles.json"

)


emb=np.load(

    EMBEDDINGS

)

with open(

    PROFILES,

    "r",

    encoding="utf-8"

) as f:

    profiles=json.load(

        f

    )

names=[

    x["doctor_name"]

    for x in profiles

]

kmeans=KMeans(

    n_clusters=3,

    random_state=42

)

clusters=kmeans.fit_predict(

    emb

)

df=pd.DataFrame(

    {

        "doctor":names,

        "cluster":clusters

    }

)

print(

    df.sort_values(

        "cluster"

    )

)