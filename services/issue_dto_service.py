import os
import requests

from dotenv import load_dotenv
from models.issue_dto import IssueDto

load_dotenv()


def get_all_issue_dto():
    """Fetches the latest issue DTO from the backend API."""
    return requests.get(os.getenv("BACKEND_API_URL") + "/issue/get/all").json()


def set_issue_dto_list(issue_dto_list=None):
    """Creates a list of issue DTOs from the fetched issue DTOs."""
    for issue in get_all_issue_dto():
        issue_dto = IssueDto(
            issue["id"],
            issue["duplicateIssueId"],
            issue["title"],
            issue["latitude"],
            issue["longitude"],
            issue["thumbnailPath"],
            issue["status"]
        )
        issue_dto_list.add(issue_dto)
