# Malaysia Medical Tourism — Hospital & Recovery Recommender

Streamlit multipage app, split into two parts:

```
med_tourism_app/
├── app.py                              # landing page, links to both parts
├── pages/
│   ├── 1_Hospital_Recommendation.py    # specialty → filtered, ranked hospitals
│   └── 2_Recovery_Plan.py              # hospital → treatment type → urban/rural recovery
├── shared.py                           # hospital data loading, shared by both pages
├── attractions.py                      # loads/queries the two attraction datasets
├── specialist_mapping.py               # rule-based (keyword) classifier: 408 raw
│                                        #   specialist labels → 39 clean categories
├── specialty_severity.py               # heuristic specialty → major/minor/mental_health default
└── hospitals_raw.csv, attractions_near_hospitals.csv, attractions_rural_regions.csv
    (also duplicated under data/ — code currently reads the flat root copies,
    since that's how the deployed repo is laid out)
```

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What's real vs. curated

- **Hospital data**: 91 hospitals, directly from the uploaded
  `malaysia_hospitals_specialist_cleaned.csv`. Every hospital now has at
  least one specialty listed (unlike the earlier dataset, where 59 of 91 had
  none).
- **Specialty categories**: normalized from 408 raw, messy specialist
  strings via a rule-based keyword classifier (`specialist_mapping.py`) —
  406 of 408 map cleanly; only "Aviation Medicine" is a genuine one-off left
  as "Other". This is deterministic rule-based logic, not a trained model.
- **Mental Health / Psychiatry** is now a real category (23 hospitals) —
  previously flagged as absent from the data entirely.
- **Attraction data**: from two OpenStreetMap-sourced CSVs. Only 36 of 91
  hospitals have nearby-attraction data — the app says so explicitly.
- **Judgment calls that ARE curated (not from data)**:
  - specialty → major/minor/mental_health severity default (`specialty_severity.py`)
  - which attraction categories count as "urban low-exertion" vs "rural scenic"
  - accreditation/membership-tier sort order on the Hospital Recommendation page

## Recovery Plan logic

- **Major surgery** → urban only: real attractions near that hospital, low-exertion by default.
- **Minor procedure / mental health** → user chooses urban (same as above) or
  rural: the project's 7 candidate rural regions (Sabah, Sarawak, Kelantan,
  Terengganu, Perak interior, Kedah, Melaka hinterland), ranked by
  straight-line distance from the hospital, with real attractions in
  whichever region is picked.

For a Mental Health / Psychiatry specialty pick, the recovery-plan intensity
defaults straight to "mental health / wellness care" rather than requiring
the user to re-select it.
