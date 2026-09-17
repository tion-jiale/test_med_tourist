"""
Suggests a default recovery-intensity tier for each specialty category, used
only to pre-select an option in the Recovery Planner - the user can and
should override it based on what their doctor actually recommends.

This is a general heuristic (which categories *typically* involve major
surgery vs. outpatient/minor procedures), not a clinical rule and not sourced
from the hospital dataset. Treat it as a starting point, not medical advice.
"""

# "major"  -> typically needs to stay close to the treating hospital for follow-up
# "minor"  -> typically outpatient / short recovery, more freedom to travel
SEVERITY_DEFAULT = {
    "Cardiothoracic & Cardiac Surgery": "major",
    "Neurology & Neurosurgery": "major",
    "Oncology / Cancer Care": "major",
    "Orthopaedics": "major",
    "Bariatric / Weight-Loss Surgery": "major",
    "General Surgery": "major",
    "Nephrology": "major",
    "Cardiology": "major",           # often interventional (angioplasty, etc.)
    "Cosmetic & Reconstructive Surgery": "major",

    "Obstetrics & Gynaecology": "minor",
    "Gastroenterology": "minor",
    "ENT (Ear, Nose & Throat)": "minor",
    "Ophthalmology (Eye)": "minor",
    "Fertility / IVF": "minor",
    "Dermatology": "minor",
    "Dental": "minor",
    "Endocrinology": "minor",
    "Internal Medicine": "minor",
    "Paediatrics": "minor",
    "Health Screening": "minor",
    "Geriatrics": "minor",
    "Haematology": "minor",
    "Anaesthesiology": "minor",
    "Emergency & Trauma": "major",
    "Radiology & Imaging": "minor",
    "Other": "minor",
}


def default_intensity(category):
    return SEVERITY_DEFAULT.get(category, "minor")
