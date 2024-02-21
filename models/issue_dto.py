class IssueDto:
    def __init__(self,
                 issue_id: int,
                 duplicate_issue_id: int,
                 title: str,
                 latitude: float,
                 longitude: float,
                 thumbnail_path: str,
                 status: str
                 ):
        self.issue_id = issue_id
        self.duplicate_issue_id = duplicate_issue_id
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.thumbnail_path = thumbnail_path
        self.status = status


class IssueDtoList:
    def __init__(self):
        self.issue_dto_list = []

    def add(self, issue_dto: IssueDto):
        if issue_dto not in self.issue_dto_list:
            self.issue_dto_list.append(issue_dto)

    def find_by_id(self, issue_id: int):
        for issue in self.issue_dto_list:
            if issue.issue_id == issue_id:
                return issue
        return None

    def get(self):
        return self.issue_dto_list
