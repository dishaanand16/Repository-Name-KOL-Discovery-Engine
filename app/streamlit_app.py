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

ROOT_DIR = Path(__file__).resolve().parent

# For local development only
if os.path.exists(ROOT_DIR / ".env"):
    load_dotenv(ROOT_DIR / ".env")

OUTPUT_DIR = ROOT_DIR / "outputs" / "processed"


############################################
# LOAD ENV / SECRETS
############################################

def get_secret(key):
    """
    Get secret from environment or Streamlit secrets.
    Priority: Streamlit secrets > Environment variables
    """
    # Try Streamlit secrets first (for deployed apps)
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        pass
    
    # Fall back to environment variables (for local development)
    value = os.getenv(key)
    if value:
        return value
    
    return None


groq_key = get_secret("GROQ_API_KEY")

if not groq_key:
    st.error(
        "❌ GROQ_API_KEY not found!\n\n"
        "**For Local Development:**\n"
        "1. Create a `.env` file in your project root\n"
        "2. Add: `GROQ_API_KEY=your_key_here`\n\n"
        "**For Streamlit Cloud Deployment:**\n"
        "1. Go to your app settings (⚙️ gear icon)\n"
        "2. Click 'Secrets (optional)'\n"
        "3. Add: `GROQ_API_KEY = your_key_here`\n"
        "4. Deploy"
    )
    st.stop()


############################################
# GROQ CLIENT
############################################

client = Groq(api_key=groq_key)


############################################
# LOAD DATA
############################################

try:
    with open(
        OUTPUT_DIR / "doctor_profiles.json",
        "r",
        encoding="utf-8"
    ) as f:
        profiles = json.load(f)
except FileNotFoundError:
    st.error(
        f"❌ doctor_profiles.json not found at {OUTPUT_DIR}\n\n"
        "Make sure your data files are in the correct location."
    )
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"❌ Error reading doctor_profiles.json: {e}")
    st.stop()


try:
    scores = pd.read_csv(OUTPUT_DIR / "influence_scores.csv")
except FileNotFoundError:
    st.warning("⚠️ influence_scores.csv not found")
    scores = pd.DataFrame()

try:
    similarity = pd.read_csv(
        OUTPUT_DIR / "similarity_matrix.csv",
        index_col=0
    )
except FileNotFoundError:
    st.warning("⚠️ similarity_matrix.csv not found")
    similarity = None

try:
    clusters = pd.read_csv(OUTPUT_DIR / "clusters.csv")
except FileNotFoundError:
    st.warning("⚠️ clusters.csv not found")
    clusters = None


doctor_names = [
    p.get("doctor_name", "Unknown") for p in profiles
]


############################################
# TITLE
############################################

st.title("KOL Discovery Engine")

doctor = st.selectbox("Choose Doctor", doctor_names)

profile = next(
    (p for p in profiles if p.get("doctor_name") == doctor),
    None
)

if profile is None:
    st.error("Profile missing")
    st.stop()


############################################
# PROFILE
############################################

st.header("Doctor Profile")
st.json(profile)


############################################
# CLUSTERS
############################################

if clusters is not None:
    st.subheader("Cluster Assignment")
    st.dataframe(
        clusters[clusters["doctor"] == doctor]
    )


############################################
# SIMILARITY
############################################

if similarity is not None:
    st.header("Most Similar KOLs")
    top_similar = (
        similarity
        .loc[doctor]
        .sort_values(ascending=False)[1:4]
    )
    st.dataframe(top_similar)


############################################
# INFLUENCE
############################################

if not scores.empty:
    st.header("Influence Ranking")
    scores = scores.sort_values("influence_score", ascending=False)
    scores.insert(0, "Rank", range(1, len(scores) + 1))
    st.dataframe(scores)


############################################
# COMPARISON
############################################

st.header("Compare Two KOLs")

doc1 = st.selectbox("Doctor 1", doctor_names, key="d1")
doc2 = st.selectbox("Doctor 2", doctor_names, key="d2")


def get_profile(name):
    for p in profiles:
        if p.get("doctor_name") == name:
            return p


if st.button("Compare"):
    p1 = get_profile(doc1)
    p2 = get_profile(doc2)

    prompt = f"""
Compare these KOLs.

Doctor1:
{json.dumps(p1, indent=2)}

Doctor2:
{json.dumps(p2, indent=2)}

Provide:
1. Expertise overlap
2. Major differences
3. Research similarity
4. Influence comparison
5. Final summary
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        st.subheader("LLM Comparison")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ LLM failed: {e}")


############################################
# EXPANDERS
############################################

with st.expander("Full JSON"):
    st.json(profile)

if similarity is not None:
    with st.expander("Similarity Matrix"):
        st.dataframe(similarity)