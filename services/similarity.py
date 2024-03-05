import math
import os

from dotenv import load_dotenv
from geopy.distance import geodesic

import logging as log

from utils.sentence_similarity_model import get_similarity_scores

load_dotenv()
log.basicConfig(level=log.INFO, filemode='w', filename='similarity.log')

DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD"))
DECAY_SCALE = float(os.getenv("DECAY_SCALE"))
LOCATION_WEIGHT = float(os.getenv("LOCATION_WEIGHT"))
TITLE_WEIGHT = float(os.getenv("TITLE_WEIGHT"))


def cal_location_similarity(location_target, all_locations):
    def calculate_similarity(location):
        distance = geodesic(
            location_target, location
        ).meters
        similarity_score = math.exp(-distance / DISTANCE_THRESHOLD * DECAY_SCALE)
        return similarity_score

    return list(map(calculate_similarity, all_locations))


def cal_sentence_similarity(source_sentence, sentences):
    return get_similarity_scores(source_sentence, sentences)


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
    title_similarity = cal_sentence_similarity(title_target, all_titles)

    # Combine weighted similarities
    weighted_similarity = [
        (LOCATION_WEIGHT * loc_sim) + (TITLE_WEIGHT * title_sim)
        for loc_sim, title_sim in zip(location_similarity, title_similarity)
    ]
    return weighted_similarity


def map_similarity_to_issue_similarity_bubble(all_issues, similarity_scores):
    return [
        {
            "issueId": issue.issue_id,
            "duplicateIssueId": issue.duplicate_issue_id,
            "similarityScore": similarity_score,
            "issueBubbleDto": {
                "title": issue.title,
                "thumbnailPath": issue.thumbnail_path,
                "status": issue.status
            }
        }
        # Map similarity score to issue similarity bubble
        # And check the similarity score is greater than the threshold
        for issue, similarity_score in zip(all_issues, similarity_scores)
        if similarity_score >= float(os.getenv("SIMILARITY_THRESHOLD"))
    ]


def get_issue_similarity_bubble(issue_target, all_issues, count):
    # Log all issues
    similarity_scores = cal_similarity_issue(issue_target, all_issues)
    issue_similarity_bubble = map_similarity_to_issue_similarity_bubble(all_issues, similarity_scores)
    if len(issue_similarity_bubble) == 0:
        return []
    # Sort by similarity score
    issue_similarity_bubble.sort(key=lambda x: x["similarityScore"], reverse=True)
    return issue_similarity_bubble[:count]
