"""
this class is abstract class of db

if you want to inherit from AbsDb
you need to implement all this options

options:
    global:
        connect
        search

    user options:
        create user
        get user info
        delete user
        update user

    company options:
        create company
        get company info
        delete company
        update company

    model options:
        create model
        get model
        delete model
"""


class AbsDb:
    def __init__(self):
        pass

    def connect(self, name=None, password=None):
        pass

    def search(self, table, db_query, values=None):
        pass

    def close_connection(self):
        pass

    def create_user(self, user_info):
        pass

    def get_user(self, user_name, password):
        pass

    def delete_user(self, user_id):
        pass

    def update_user(self, action, user_id, user_info):
        pass

    def get_admin(self, user_name, password):
        pass

    def create_model(self, model_info):
        pass

    def delete_model(self, model_id):
        pass

    def get_model(self, model_id):
        pass

    def get_model_list(self):
        pass

    def create_company(self, company_info):
        pass

    def delete_company(self, company_id):
        pass

    def update_company(self, action, company_name, company_info):
        pass
