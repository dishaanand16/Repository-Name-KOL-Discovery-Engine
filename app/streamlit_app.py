import os
import json

from pathlib import Path

import streamlit as st
import pandas as pd

from groq import Groq
from dotenv import load_dotenv


############################################
# PATHS
############################################

ROOT_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = (

    ROOT_DIR

    / "outputs"

    / "processed"

)


############################################
# LOAD ENV
############################################

env_path = ROOT_DIR / ".env"

if env_path.exists():

    load_dotenv(

        env_path

    )


############################################
# SECRET LOADING
############################################

def get_secret(

        key

):

    try:

        return st.secrets[

            key

        ]

    except:

        pass

    value=os.getenv(

        key

    )

    if value:

        return value

    return None


groq_key=get_secret(

    "GROQ_API_KEY"

)


if groq_key is None:

    st.error(

        "GROQ_API_KEY missing"

    )

    st.stop()


############################################
# GROQ CLIENT
############################################

client=Groq(

    api_key=groq_key

)


############################################
# LOAD DATA
############################################

try:

    with open(

        OUTPUT_DIR /

        "doctor_profiles.json",

        "r",

        encoding="utf-8"

    ) as f:

        profiles=json.load(

            f

        )

except Exception as e:

    st.error(

        f"doctor_profiles.json missing: {e}"

    )

    st.stop()


try:

    scores=pd.read_csv(

        OUTPUT_DIR /

        "influence_scores.csv"

    )

except:

    scores=pd.DataFrame()


try:

    similarity=pd.read_csv(

        OUTPUT_DIR /

        "similarity_matrix.csv",

        index_col=0

    )

except:

    similarity=None


try:

    clusters=pd.read_csv(

        OUTPUT_DIR /

        "clusters.csv"

    )

except:

    clusters=None


doctor_names=[

    p.get(

        "doctor_name",

        "Unknown"

    )

    for p in profiles

]


############################################
# TITLE
############################################

st.title(

    "KOL Discovery Engine"

)


doctor=st.selectbox(

    "Choose Doctor",

    doctor_names

)


profile=None

for p in profiles:

    if p.get(

        "doctor_name"

    )==doctor:

        profile=p

        break


if profile is None:

    st.error(

        "Profile not found"

    )

    st.stop()


############################################
# PROFILE
############################################

st.header(

    "Doctor Profile"

)

st.json(

    profile

)


############################################
# CLUSTER
############################################

if clusters is not None:

    st.subheader(

        "Cluster Assignment"

    )

    st.dataframe(

        clusters[

            clusters["doctor"]

            ==doctor

        ]

    )


############################################
# SIMILARITY
############################################

if similarity is not None:

    st.header(

        "Most Similar KOLs"

    )

    try:

        top_similar=(

            similarity

            .loc[doctor]

            .sort_values(

                ascending=False

            )[1:4]

        )

        st.dataframe(

            top_similar

        )

    except:

        st.warning(

            "Similarity unavailable"

        )


############################################
# INFLUENCE
############################################

if not scores.empty:

    st.header(

        "Influence Ranking"

    )

    scores=scores.sort_values(

        "influence_score",

        ascending=False

    )

    scores.insert(

        0,

        "Rank",

        range(

            1,

            len(scores)+1

        )

    )

    st.dataframe(

        scores

    )


############################################
# PAYMENTS
############################################

st.header(

    "CMS Payment Signals"

)

st.write(

    profile.get(

        "payments",

        {}

    )

)


############################################
# COMPARISON
############################################

st.header(

    "Compare Two KOLs"

)


doc1=st.selectbox(

    "Doctor 1",

    doctor_names,

    key="d1"

)

doc2=st.selectbox(

    "Doctor 2",

    doctor_names,

    key="d2"

)


def get_profile(

        name

):

    for p in profiles:

        if p.get(

            "doctor_name"

        )==name:

            return p


if st.button(

    "Compare"

):

    p1=get_profile(

        doc1

    )

    p2=get_profile(

        doc2

    )

    prompt=f"""

Compare these KOLs.

Doctor1:

{json.dumps(p1)}

Doctor2:

{json.dumps(p2)}

Provide:

1 Expertise overlap

2 Major differences

3 Research similarity

4 Influence comparison

5 Final summary

"""

    try:

        response=client.chat.completions.create(

            model=

            "llama-3.3-70b-versatile",

            messages=[

                {

                    "role":"user",

                    "content":prompt

                }

            ]

        )

        st.subheader(

            "LLM Comparison"

        )

        st.write(

            response

            .choices[0]

            .message.content

        )

    except Exception as e:

        st.error(

            f"LLM failed: {e}"

        )


############################################
# EXPANDERS
############################################

with st.expander(

    "Full JSON"

):

    st.json(

        profile

    )


if similarity is not None:

    with st.expander(

        "Similarity Matrix"

    ):

        st.dataframe(

            similarity

        )