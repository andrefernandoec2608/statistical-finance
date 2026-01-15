class FinanceManagerException(Exception):
    pass

class DuplicateIDException(FinanceManagerException):
    def __init__(self, item_id):
        super().__init__(f"ID '{item_id}' already exists in the system.")
        self.item_id = item_id

class NotFoundIDException(FinanceManagerException):
    def __init__(self, item_id):
        super().__init__(f"ID '{item_id}' doesn't exist in the system.")
        self.item_id = item_id