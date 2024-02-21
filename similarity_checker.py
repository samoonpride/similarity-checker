import os

from dotenv import load_dotenv
from flask import Flask, request

from models.issue_dto import IssueDtoList
from services.similarity import cal_similarity_issue, find_10_most_similar_issues
from services.issue_dto_service import set_issue_dto_list

# Load environment variables from the .env file
load_dotenv()

# Initialize the IssueSimilarityCheckDtoList
issue_similarity_check_dto_list = IssueDtoList()

app = Flask(__name__)


@app.route('/similarity', methods=['POST'])
def similarity():
    issue_target = request.get_json()
    set_issue_dto_list(issue_similarity_check_dto_list)
    ranked_similarity_scores = cal_similarity_issue(issue_target, issue_similarity_check_dto_list.get())
    return {"similarIssues": find_10_most_similar_issues(ranked_similarity_scores)}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("APP_PORT"))
