"""
Suggests a default recovery-intensity tier for each specialty category, used
only to pre-select an option in the Recovery Planner - the user can and
should override it based on what their doctor actually recommends.

This is a general heuristic (which categories *typically* involve major
surgery vs. outpatient/minor procedures vs. mental-health/wellness care),
not a clinical rule and not sourced from the hospital dataset.
"""

# "major"         -> typically needs to stay close to the treating hospital
# "minor"         -> typically outpatient / short recovery, more freedom to travel
# "mental_health" -> mental-health/wellness-focused care
SEVERITY_DEFAULT = {
    # major - surgical / needs close follow-up
    "Cardiothoracic & Cardiac Surgery": "major",
    "Neurology & Neurosurgery": "major",
    "Oncology / Cancer Care": "major",
    "Orthopaedics": "major",
    "Bariatric / Weight-Loss Surgery": "major",
    "General Surgery": "major",
    "Nephrology": "major",
    "Cardiology": "major",  # often interventional (angioplasty, etc.)
    "Cosmetic & Reconstructive / Plastic Surgery": "major",
    "Vascular Surgery": "major",
    "Urology": "major",
    "Emergency & Trauma": "major",

    # mental health / wellness
    "Mental Health / Psychiatry": "mental_health",

    # minor - outpatient / lighter follow-up
    "Obstetrics & Gynaecology": "minor",
    "Gastroenterology & Hepatology": "minor",
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
    "Radiology & Imaging": "minor",
    "Pathology & Lab Medicine": "minor",
    "Rheumatology": "minor",
    "Pulmonology / Respiratory Medicine": "minor",
    "Infectious Disease": "minor",
    "Genetics": "minor",
    "Palliative & Pain Medicine": "minor",
    "Nutrition & Dietetics": "minor",
    "Traditional & Complementary Medicine": "minor",
    "Occupational Medicine": "minor",
    "Rehabilitation & Physiotherapy": "minor",
    "Other": "minor",
}


def default_intensity(category):
    return SEVERITY_DEFAULT.get(category, "minor")
