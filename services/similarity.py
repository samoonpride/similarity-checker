import math
import os

from dotenv import load_dotenv
from geopy.distance import geodesic

from utils.similarity_model import send_request_to_get_score

load_dotenv()

DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD"))
DECAY_SCALE = float(os.getenv("DECAY_SCALE"))
LOCATION_WEIGHT = float(os.getenv("LOCATION_WEIGHT"))
TITLE_WEIGHT = float(os.getenv("TITLE_WEIGHT"))


def cal_location_similarity(location_target, all_locations):
    def calculate_similarity(location):
        distance = geodesic(
            location_target,location
        ).meters
        similarity_score = math.exp(-distance / DISTANCE_THRESHOLD * DECAY_SCALE)
        return similarity_score

    return list(map(calculate_similarity, all_locations))


def cal_title_similarity(title_target, all_titles):
    return send_request_to_get_score(title_target, all_titles)


def cal_similarity_issue(issue_target, all_issues):
    # Set target issue's location and title
    location_target = (
        issue_target["latitude"],
        issue_target["longitude"]
    )
    title_target = issue_target["title"]
    # Set all issues' location and title
    all_locations = [
        (
            issue.latitude,
            issue.longitude
        ) for issue in all_issues
    ]
    all_titles = [issue.title for issue in all_issues]
    # Calculate similarities
    location_similarity = cal_location_similarity(location_target, all_locations)
    title_similarity = cal_title_similarity(title_target, all_titles)

    # Combine weighted similarities
    weighted_similarity = [
        (LOCATION_WEIGHT * loc_sim) + (TITLE_WEIGHT * title_sim)
        for loc_sim, title_sim in zip(location_similarity, title_similarity)
    ]

    return list(map_similarity_to_issue(all_issues, weighted_similarity))


def map_similarity_to_issue(all_issues, similarity_scores):
    return [
        {
            "id": issue.issue_id,
            "title": issue.title,
            "duplicateIssueId": issue.duplicate_issue_id,
            "thumbnailPath": issue.thumbnail_path,
            "similarityScore": similarity_score
        }
        for issue, similarity_score in zip(all_issues, similarity_scores)
    ]


def find_10_most_similar_issues(issue_similarity_list):
    issue_similarity_list.sort(key=lambda x: x["similarityScore"], reverse=True)
    return issue_similarity_list[:10]
