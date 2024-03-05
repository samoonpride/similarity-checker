import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from models.issue_dto import IssueDtoList
from services.similarity import get_issue_similarity_bubble, cal_sentence_similarity
from services.issue_dto_service import set_issue_dto_list

# Load environment variables from the .env file
load_dotenv()

# Initialize the IssueSimilarityCheckDtoList
issue_similarity_check_dto_list = IssueDtoList()

app = Flask(__name__)


@app.route('/similarity/issue', methods=['POST'])
def similarity_issues():
    issue_target = request.get_json()
    set_issue_dto_list(issue_similarity_check_dto_list)
    ranked_similarity_scores = get_issue_similarity_bubble(
        issue_target,
        issue_similarity_check_dto_list.get(),
        10
    )
    if len(ranked_similarity_scores) == 0:
        return jsonify({"error": "No similar issues found."}), 204
    return jsonify(ranked_similarity_scores)


@app.route('/similarity/sentence', methods=['POST'])
def similarity_text():
    text = request.get_json()
    similarity_score = cal_sentence_similarity(text["sourceSentence"], text["sentences"])
    return jsonify(similarity_score)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("APP_PORT"))
