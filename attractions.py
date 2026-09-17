"""
Loads the two real, OSM-sourced attraction datasets:

- attractions_near_hospitals.csv: attractions within ~23km of 36 of the 91
  hospitals (query_type = "hospital_radius", reference_point = hospital name)
- attractions_rural_regions.csv: attractions within ~67km of 7 candidate
  rural regions from the feasibility project (query_type = "rural_region",
  reference_point = region name, e.g. "Sabah_interior")

Nothing here is invented - every attraction name, category, and coordinate
comes straight from these two files. The only derived values are the
haversine distances used to rank rural regions by proximity to a hospital.
"""

import math
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
HOSPITAL_ATTR_PATH = APP_DIR / "attractions_near_hospitals.csv"
RURAL_ATTR_PATH = APP_DIR / "attractions_rural_regions.csv"

# Low-exertion / short-visit categories, reasonable to recommend to someone
# recovering from major surgery and staying close to the hospital. This is
# a judgment call, not something in the source data.
URBAN_DEFAULT_CATEGORIES = [
    "Park / Green Space", "Museum", "Art Gallery", "General Attraction",
    "Aquarium", "Public Art",
]

# Categories that read as "scenic rural sight" for someone with more freedom
# to travel. Also a judgment call, not in the source data.
RURAL_DEFAULT_CATEGORIES = [
    "Viewpoint / Scenic Spot", "Mountain / Peak", "Nature Reserve",
    "Park / Green Space", "Beach", "Zoo / Wildlife Park",
]

# Human-readable label for each rural region code used in the CSV.
RURAL_REGION_LABELS = {
    "Sabah_interior": "Sabah interior",
    "Sarawak_interior": "Sarawak interior",
    "Kelantan": "Kelantan",
    "Terengganu": "Terengganu",
    "Perak_interior": "Perak interior",
    "Kedah": "Kedah",
    "Melaka_hinterland": "Melaka hinterland",
}


@st.cache_data
def load_hospital_attractions():
    return pd.read_csv(HOSPITAL_ATTR_PATH)


@st.cache_data
def load_rural_attractions():
    return pd.read_csv(RURAL_ATTR_PATH)


def attractions_for_hospital(hospital_name):
    df = load_hospital_attractions()
    return df[df["reference_point"] == hospital_name].copy()


def hospitals_with_attraction_data():
    df = load_hospital_attractions()
    return sorted(df["reference_point"].unique())


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


@st.cache_data
def rural_region_centroids():
    """One row per rural region: its centroid (mean lat/lon of its
    attractions) and how many attractions were found for it."""
    df = load_rural_attractions()
    grouped = df.groupby(["reference_point", "reference_state"]).agg(
        centroid_lat=("lat", "mean"),
        centroid_lon=("lon", "mean"),
        n_attractions=("osm_id", "count"),
    ).reset_index()
    grouped["label"] = grouped["reference_point"].map(RURAL_REGION_LABELS)
    return grouped


def rural_regions_ranked_by_distance(hospital_lat, hospital_lon):
    """Rural regions sorted by straight-line distance from a hospital's
    coordinates to that region's centroid. Straight-line, not road distance -
    useful for relative ranking, not for trip-planning ETAs."""
    centroids = rural_region_centroids().copy()
    centroids["distance_km"] = centroids.apply(
        lambda r: haversine_km(hospital_lat, hospital_lon, r["centroid_lat"], r["centroid_lon"]),
        axis=1,
    )
    return centroids.sort_values("distance_km")


def attractions_for_region(reference_point):
    df = load_rural_attractions()
    return df[df["reference_point"] == reference_point].copy()
