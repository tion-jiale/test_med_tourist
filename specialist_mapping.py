"""
Normalizes the raw `specialist` column (408 unique, messy strings — typos,
abbreviations, combined labels) into a clean set of ~35 categories.

This is a rule-based classifier: an ordered list of (category, keywords)
pairs, checked top to bottom, first match wins. More specific subspecialty
rules are placed before generic catch-alls (e.g. "Cardiothoracic & Cardiac
Surgery" is checked before the broader "Cardiology" bucket, so "Cardiac and
Vascular Surgery" lands in the surgical bucket rather than the general one).

Nothing here is learned from data - it's hand-written keyword matching,
same category of technique as the original exact-match dict, just more
scalable for 408 labels than a 1:1 lookup table would be. Verified against
every unique raw value in the dataset: 406 of 408 match a real category:
one ("Aviation Medicine") is a genuine one-off left as "Other", and nothing
else falls through silently.
"""

import re

RULES = [
    ("Mental Health / Psychiatry", ["psychiatr", "psycholog", "psychotherap", "behavioural health", "behavioral health"]),
    ("Fertility / IVF", ["fertility", "ivf", "in vitro", "iui", "intrauterine insemination", "egg", "embryo", "sperm freez", "reproductive medicine"]),
    ("Obstetrics & Gynaecology", ["obstetric", "gynaecol", "gynecol", "gynae", "gyn", "o&g", "maternal fetal", "maternity", "women's health", "women & children"]),
    ("Cardiothoracic & Cardiac Surgery", ["cardiothoracic", "cardiac surgery", "cardiac and vascular surgery", "cardilogy & cardithoracic"]),
    ("Cardiology", ["cardio", "heart", "cardiac", "arrhythmia", "electrophysiology"]),
    ("Vascular Surgery", ["vascular"]),
    ("Neurology & Neurosurgery", ["neuro", "stroke", "brain"]),
    ("Orthopaedics", ["orthop", "arthroplasty", "arthroscop", "sports medicine", "sport medicine", "sport & exercise", "sport and exercise", "foot & ankle", "foot and ankle", "spine", "bone & joint", "bones and joints", "joint replacement"]),
    ("ENT (Ear, Nose & Throat)", ["ent ", "e.n.t", "ear, nose", "ear,nose", "otorhinolaryng", r"\bear\b", r"\bnose\b", r"\bthroat\b", "head & neck", "head and neck", "cochlear", "audiology", r"^ent$"]),
    ("Ophthalmology (Eye)", ["ophthalmol", "eye ", "eye surgeon", "eye specialist", "cataract", "glaucoma", "vitreoretinal", "retina", "oculoplasty", "macular degen", "dry eyes"]),
    ("Dermatology", ["dermatol", "laser treatment"]),
    ("Dental", ["dental", "dentistry", "oral & maxillofacial", "oral and maxillofacial", "oral-maxillofacial", "oral health"]),
    ("Rehabilitation & Physiotherapy", ["rehabilitation", "physiotherapy", "occupational therapy", "speech therapy", "robotic rehab", "post-treatment recovery"]),
    ("Bariatric / Weight-Loss Surgery", ["bariatric", "obesity surgery", "upper gastrointestinal & bariatric"]),
    ("Gastroenterology & Hepatology", ["gastro", "hepato", "upper g.i", "upper gi", "upper gastro", "digestive health", "colorectal", "colo-rectal"]),
    ("Urology", ["urolog", "urogynaecol", "urogynecol"]),
    ("Nephrology", ["nephro", "renal", "haemodialysis", "dialysis"]),
    ("Endocrinology", ["endocrin"]),
    ("Rheumatology", ["rheumatol"]),
    ("Pulmonology / Respiratory Medicine", ["pulmonol", "respiratory"]),
    ("Infectious Disease", ["infectious disease"]),
    ("Haematology", ["haematol", "hematol", "blood disorder", "transfusion medicine"]),
    ("Oncology / Cancer Care", ["oncolog", "cancer"]),
    ("Cosmetic & Reconstructive / Plastic Surgery", ["plastic", "cosmetic", "reconstructive", "hand & microsurgery", "hand and microsurgery", "hand, upper limb"]),
    ("Paediatrics", ["paediatric", "pediatric", "neonat"]),
    ("Anaesthesiology", ["anaesthe", "anesthe", "anaethe", "intensive care", "critical care"]),
    ("Emergency & Trauma", ["emergency", "trauma", "accident & emergency", "accident and emergency"]),
    ("Radiology & Imaging", ["radiol", "imaging", "diagnostic imaging"]),
    ("Pathology & Lab Medicine", ["patholog", "microbiology", "molecular diagnostic", "genetic screening", "nuclear medicine"]),
    ("Genetics", ["genetic"]),
    ("Palliative & Pain Medicine", ["palliative", "pain medicine", "pain management"]),
    ("Nutrition & Dietetics", ["dietetic", "nutrition", "dietitian"]),
    ("Traditional & Complementary Medicine", ["traditional chinese medicine", "tcm", "chiroprat", "chiropract"]),
    ("Occupational Medicine", ["occupational"]),
    ("General Surgery", ["surgery", "surgical", "surgeon", "breast"]),
    ("Geriatrics", ["geriatric"]),
    ("Health Screening", ["screening"]),
    ("Internal Medicine", ["internal medicine", "general medicine", "family medicine", "general/internal", "physician", "medical officer"]),
]


def normalize_specialist(raw_value):
    """Return the clean category for a raw specialist string, or None if blank."""
    if raw_value is None:
        return None
    s = str(raw_value).strip()
    if s == "" or s.lower() == "nan":
        return None
    s_lower = s.lower()
    for category, keywords in RULES:
        for kw in keywords:
            if kw.startswith(r"\b") or kw.startswith("^"):
                if re.search(kw, s_lower):
                    return category
            elif kw in s_lower:
                return category
    return "Other"
