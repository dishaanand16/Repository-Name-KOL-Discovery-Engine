# KOL Discovery Engine

## Overview

KOL Discovery Engine is an AI-powered system designed to extract, structure, compare, and rank Key Opinion Leaders (KOLs) from publicly available data sources.

The system performs profile extraction, embedding-based similarity analysis, influence scoring, confidence estimation, LLM-powered comparison, and visualization through an interactive dashboard.

---

## Features

### Profile Extraction

* Extract doctor/KOL information
* Structured JSON generation
* Therapy area detection
* Specialty identification
* Geography extraction

### Data Sources

* SERP API (Google Scholar Profiles)
* CMS Open Payments API
* Clinical Trials API

### AI Components

* Sentence Embeddings
* Cosine Similarity Matrix
* Influence Score Generation
* Confidence Scores
* LLM Comparison using Groq

### Dashboard

* Doctor Profile Explorer
* Influence Rankings
* Similarity Search
* LLM Comparison
* Payment Signal Visualization

---

## Architecture

Doctor Names

↓

Profile Extraction

↓

Structured JSON Profiles

↓

Embeddings Generation

↓

Similarity Matrix

↓

Influence Score Calculation

↓

LLM Comparison

↓

Streamlit Dashboard

---

## Project Structure

```text

KOL_project_refined/

├── app/

│   ├── compare_kols.py

│   └── streamlit_app.py

├── extraction/

│   └── fetch_doctor_profile.py

├── embeddings/

│   ├── generate_embeddings.py

│   └── similarity.py

├── scoring/

│   └── influence_score.py

├── src/

│   └── api/

│       ├── serp_api.py

│       ├── cms_api.py

│       └── trials_api.py

├── outputs/

│   └── processed/

├── data/

├── README.md

└── requirements.txt

```

---

## Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Pipeline

### Profile Extraction

```bash
python -m extraction.fetch_doctor_profile
```

### Generate Embeddings

```bash
python embeddings/generate_embeddings.py
```

### Similarity Matrix

```bash
python embeddings/similarity.py
```

### Influence Scores

```bash
python scoring/influence_score.py
```

### Streamlit Dashboard

```bash
python -m streamlit run app/streamlit_app.py
```

---

## Outputs

Generated outputs:

* doctor_profiles.json
* doctor_embeddings.npy
* similarity_matrix.csv
* influence_scores.csv

---

## Technologies Used

* Python
* Streamlit
* Sentence Transformers
* Scikit Learn
* Groq LLM
* Pandas
* NumPy

---

## Future Improvements

* Better KOL matching
* Improved payment attribution
* Advanced clustering
* Additional biomedical sources
