import json

import numpy as np

from sentence_transformers import SentenceTransformer


INPUT_FILE="outputs/processed/doctor_profiles.json"

OUTPUT_FILE="outputs/processed/doctor_embeddings.npy"


model = SentenceTransformer(

    "all-MiniLM-L6-v2"

)


def build_text(

        profile

):

    return f"""

    {profile.get('doctor_name','')}

    {profile.get('specialty','')}

    {' '.join(

        profile.get(

            'therapy_area',

            []

        )

    )}

    {profile.get(

        'affiliation',

        ''

    )}

    Citations:

    {profile.get(

        'citations',

        0

    )}

    H index:

    {profile.get(

        'h_index',

        0

    )}

    """



def generate():

    with open(

        INPUT_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        profiles=json.load(

            f

        )

    texts=[

        build_text(

            profile

        )

        for profile in profiles

    ]

    embeddings=model.encode(

        texts

    )

    np.save(

        OUTPUT_FILE,

        embeddings

    )

    print(

        "Embeddings shape:",

        embeddings.shape

    )


if __name__=="__main__":

    generate()