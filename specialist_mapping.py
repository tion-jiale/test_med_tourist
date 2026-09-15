"""
Maps the raw, inconsistently-labelled `specialist` strings found in
hospitals_raw.csv to a clean set of category labels for filtering.

Built by inspecting every unique raw value in the dataset (99 of them) -
nothing here is invented; it's spelling/format consolidation only
(e.g. "ENT (Ear Nose Throat)" and "Ear, Nose & Throat (ENT)" -> "ENT").
Rows whose raw specialist has no match fall back to "Other".
"""

SPECIALIST_MAP = {
    # Cardiology
    "Cardiology": "Cardiology",
    "Cardiology & Interventional Cardiology": "Cardiology",
    "Cardiology / Cardiovascular (Heart & Vascular)": "Cardiology",
    "Cardiology and Internal Medicine": "Cardiology",
    "Interventional Cardiology": "Cardiology",
    "Arrhythmia": "Cardiology",
    "Electrophysiology": "Cardiology",
    "Heart & Lung Centre": "Cardiology",
    "Heart & Vascular: Adventist Heart Clinic": "Cardiology",
    "Cardio-Oncology (Specialised Care for Cancer Patients)": "Cardiology",
    "Cardilogy & Cardithoracic Surgery": "Cardiology",

    # Cardiothoracic / cardiac surgery
    "Cardiothoracic Surgery": "Cardiothoracic & Cardiac Surgery",
    "Cardiac Surgery": "Cardiothoracic & Cardiac Surgery",
    "Thoracic Surgery": "Cardiothoracic & Cardiac Surgery",

    # Oncology
    "Oncology": "Oncology / Cancer Care",
    "Oncology (Clinical)": "Oncology / Cancer Care",
    "Cancer Centre": "Oncology / Cancer Care",
    "Cancer Care: Adventist Oncology": "Oncology / Cancer Care",

    # Orthopaedics
    "Orthopaedics": "Orthopaedics",
    "Orthopaedics & Joint Replacement Surgery": "Orthopaedics",
    "Orthopaedics & Spine Surgery": "Orthopaedics",
    "Orthopaedics: Adventist Orthopaedic Clinic": "Orthopaedics",
    "Bones and Joints (Orthopaedics)": "Orthopaedics",
    "Joint Orthopaedic Surgery": "Orthopaedics",
    "Arthroplasty Surgery": "Orthopaedics",
    "Paediatric Ortho": "Orthopaedics",
    "Sports Medicine": "Orthopaedics",

    # Fertility / IVF
    "Fertility": "Fertility / IVF",
    "Fertility Centre": "Fertility / IVF",
    "Fertility Preservation": "Fertility / IVF",
    "In Vitro Fertilization (IVF)": "Fertility / IVF",
    "Advanced Reproductive Medicine including IVF": "Fertility / IVF",
    "Intrauterine Insemination (IUI)": "Fertility / IVF",
    "Egg": "Fertility / IVF",
    "Egg Freezing": "Fertility / IVF",
    "Embryo Freezing": "Fertility / IVF",
    "Frozen Embryo Transfer (FET)": "Fertility / IVF",
    "Sperm Freezing": "Fertility / IVF",
    "Sperm & Embryo Freezing": "Fertility / IVF",

    # Obstetrics & Gynaecology / Women's health
    "Obstetrics & Gynaecology": "Obstetrics & Gynaecology",
    "Obstetrics and Gynaecology": "Obstetrics & Gynaecology",
    "Obstetrics and Gynaecology (O&G)": "Obstetrics & Gynaecology",
    "OB&GYN": "Obstetrics & Gynaecology",
    "Women's Health": "Obstetrics & Gynaecology",
    "Women & Children's Centre": "Obstetrics & Gynaecology",

    # ENT
    "ENT (Ear Nose Throat)": "ENT (Ear, Nose & Throat)",
    "Ear, Nose & Throat (ENT)": "ENT (Ear, Nose & Throat)",
    "Ear, Nose, Throat, Head & Neck Surgery and Cochlear Implant Surgery": "ENT (Ear, Nose & Throat)",
    "Paediatric ENT": "ENT (Ear, Nose & Throat)",

    # Ophthalmology / eye
    "Eye Surgery & Glaucomatology": "Ophthalmology (Eye)",
    "Cataract Surgery": "Ophthalmology (Eye)",
    "Glaucoma Treatment": "Ophthalmology (Eye)",
    "Dry Eyes": "Ophthalmology (Eye)",
    "Age Related Macular Degenaration": "Ophthalmology (Eye)",

    # Dermatology
    "Dermatology": "Dermatology",
    "Laser Treatment": "Dermatology",

    # Dental
    "Dental": "Dental",
    "Dentistry": "Dental",

    # Gastroenterology
    "Gastroenterology": "Gastroenterology",
    "Gastroenterology and Hepatology": "Gastroenterology",
    "Digestive Health Centre": "Gastroenterology",
    "Upper G.I.": "Gastroenterology",

    # General / other surgery
    "General Surgery": "General Surgery",
    "Surgical": "General Surgery",
    "Colorectal Surgery": "General Surgery",
    "Breast Surgery": "General Surgery",
    "Breast & Endocrine Surgery": "General Surgery",
    "Breast and Endocrine Surgery": "General Surgery",
    "Breast Endocrine": "General Surgery",
    "Vascular Surgery": "General Surgery",
    "Cosmetic & Reconstructive Surgery: Adventist Cosmetic & Reconstructive Clinic": "Cosmetic & Reconstructive Surgery",

    # Neurology / Neurosurgery
    "Neurology": "Neurology & Neurosurgery",
    "Neurology & Neurosurgery": "Neurology & Neurosurgery",
    "Neurosciences": "Neurology & Neurosurgery",
    "Stroke Centre": "Neurology & Neurosurgery",

    # Nephrology
    "Nephrology": "Nephrology",
    "Renal Care: Adventist Renal Care Centre": "Nephrology",

    # Endocrinology
    "Endocrinology": "Endocrinology",
    "Endocrine & Diabetes Centre": "Endocrinology",

    # Internal medicine
    "Internal Medicine": "Internal Medicine",

    # Paediatrics
    "Paediatric": "Paediatrics",
    "Paediatrics": "Paediatrics",

    # Bariatric
    "Bariatric": "Bariatric / Weight-Loss Surgery",
    "Bariatric (Weight Loss Surgery)": "Bariatric / Weight-Loss Surgery",
    "Bariatric Surgery": "Bariatric / Weight-Loss Surgery",

    # Anaesthesiology
    "Anaesthesiology": "Anaesthesiology",
    "Anaestheosiology": "Anaesthesiology",
    "Anesthesiology": "Anaesthesiology",
    "Anaesthesiology & Critical Care": "Anaesthesiology",

    # Emergency & trauma
    "Accident & Emergency": "Emergency & Trauma",
    "Emergency Services": "Emergency & Trauma",
    "Emergency & Occupational Health": "Emergency & Trauma",
    "Trauma": "Emergency & Trauma",

    # Radiology / imaging
    "Clinical Radiology": "Radiology & Imaging",
    "Imaging": "Radiology & Imaging",

    # Geriatrics
    "Geriatrics": "Geriatrics",

    # Screening
    "Screening": "Health Screening",

    # Blood
    "Blood Disorders": "Haematology",

    # Niche / other
    "Aviation Medicine": "Other",
}


def normalize_specialist(raw_value):
    """Return the clean category for a raw specialist string, or None if blank."""
    if raw_value is None:
        return None
    raw_value = str(raw_value).strip()
    if raw_value == "" or raw_value.lower() == "nan":
        return None
    return SPECIALIST_MAP.get(raw_value, "Other")
