import os

import streamlit as st

import json

import pandas as pd

from groq import Groq

from dotenv import load_dotenv


############################################

# LOAD ENV

############################################

load_dotenv()


groq_key=(

    os.getenv(

        "GROQ_API_KEY"

    )

    or

    st.secrets.get(

        "GROQ_API_KEY",

        None

    )

)


if groq_key is None:

    raise Exception(

        "GROQ_API_KEY not found"

    )


############################################

# GROQ CLIENT

############################################

client=Groq(

    api_key=groq_key

)


############################################

# LOAD DATA

############################################

with open(

    "outputs/processed/doctor_profiles.json",

    "r",

    encoding="utf-8"

) as f:

    profiles=json.load(f)


scores=pd.read_csv(

    "outputs/processed/influence_scores.csv"

)


similarity=pd.read_csv(

    "outputs/processed/similarity_matrix.csv",

    index_col=0

)


try:

    clusters=pd.read_csv(

        "outputs/processed/clusters.csv"

    )

except:

    clusters=None


doctor_names=[

    p["doctor_name"]

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

    if p["doctor_name"]==doctor:

        profile=p

        break


############################################

# PROFILE

############################################

st.header(

    "Doctor Profile"

)

st.write(

f"**Name:** {profile.get('doctor_name')}"

)

st.write(

f"**Specialty:** {profile.get('specialty')}"

)

st.write(

f"**Therapy Areas:** {profile.get('therapy_area')}"

)

st.write(

f"**Geography:** {profile.get('geography')}"

)

st.write(

f"**Citations:** {profile.get('citations')}"

)

st.write(

f"**H Index:** {profile.get('h_index')}"

)

st.write(

f"**Publication Count:** {profile.get('publication_count')}"

)


############################################

# CLUSTERS

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

st.header(

    "Most Similar KOLs"

)

top_similar=(

    similarity.loc[doctor]

    .sort_values(

        ascending=False

    )

    [1:4]

)

st.dataframe(

    top_similar

)


############################################

# RANKINGS

############################################

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

payments=profile.get(

    "payments",

    {}

)

st.write(

    payments

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


def get_profile(name):

    for p in profiles:

        if p["doctor_name"]==name:

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

Compare these KOLs:

Doctor 1:

{json.dumps(p1)}

Doctor 2:

{json.dumps(p2)}

Give:

1 Expertise overlap

2 Major differences

3 Research similarity

4 Influence comparison

5 Summary

"""

    response=client.chat.completions.create(

        model="llama-3.3-70b-versatile",

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


with st.expander(

    "Full JSON"

):

    st.json(

        profile

    )


with st.expander(

    "Similarity Matrix"

):

    st.dataframe(

        similarity

    )