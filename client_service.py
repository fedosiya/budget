import httpx
import orjson
from pydantic import BaseModel
from models import *


class ClientService:
    def __init__(self):
        self._server_base_url = "http://localhost:5000"
        self._client = httpx.Client()

    def close(self):
        self._client.close()

    def sign_up(self, user_model: dict):
        url = "http://localhost:5000/sign_up"
        response = self._client.post(url, content=orjson.dumps(user_model))
        return response

    def sign_in(self, user_model: dict):
        url = "http://localhost:5000/sign_in"
        response = self._client.post(url, content=orjson.dumps(user_model))
        return response

    def change_user_login(self, change_user_data_model: dict):
        url = "http://localhost:5000/change_login"
        response = self._client.post(url, content=orjson.dumps(change_user_data_model))
        return response

    def change_user_password(self, change_user_data_model: dict):
        url = "http://localhost:5000/change_password"
        response = self._client.post(url, content=orjson.dumps(change_user_data_model))
        return response

    def get_logins_of_users(self):
        url = "http://localhost:5000/users"
        response = self._client.get(url)
        return response.json()

    def block_user(self, user_model: dict):
        url = "http://localhost:5000/block_users"
        response = self._client.post(url, content=orjson.dumps(user_model))
        return response

    def unblock_user(self, model: dict):
        url = "http://localhost:5000/unblock_users"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_blocked_users(self):
        url = "http://localhost:5000/blocked_users"
        response = self._client.get(url)
        return response.json()

    def delete_user(self, user_model: dict):
        url = "http://localhost:5000/delete_users"
        response = self._client.post(url, content=orjson.dumps(user_model))
        return response

    def get_values_for_admin_stat(self):
        url = "http://localhost:5000/get_values_for_admin"
        response = self._client.get(url)
        return response

    def get_values_for_user_stat(self, model: dict):
        url = "http://localhost:5000/get_values_for_user"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    # work with aims

    def delete_aim(self, model: dict):
        url = "http://localhost:5000/delete_aims"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def add_aim(self, model: dict):
        url = "http://localhost:5000/add_aim"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_aims(self, model: dict):
        url = "http://localhost:5000/get_aims"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_aim_name(self, model: dict):
        url = "http://localhost:5000/edit_aim_name"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_aim_sum(self, model: dict):
        url = "http://localhost:5000/edit_aim_sum"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_deadline(self, model: dict):
        url = "http://localhost:5000/edit_aim_deadline"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def make_aim_completed(self, model: dict):
        url = "http://localhost:5000/make_aim_completed"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def put_aside(self, model: dict):
        url = "http://localhost:5000/to_put_aside"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    # work with expenses
    def get_expenses(self, model: dict):
        url = "http://localhost:5000/get_expenses"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def add_exp(self, model: dict):
        url = "http://localhost:5000/add_exp"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def get_aims_to_put_aside(self, model: dict):
        url = "http://localhost:5000/get_aims_to_put_aside"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def delete_exp(self, model:dict):
        url = "http://localhost:5000/delete_exp"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def edit_exp_name(self, model:dict):
        url = "http://localhost:5000/edit_exp_name"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def edit_exp_sum(self, model:dict):
        url = "http://localhost:5000/edit_exp_sum"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def edit_exp_date(self, model: dict):
        url = "http://localhost:5000/edit_exp_date"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    # work with incomes
    def get_incomes_of_user(self, model: dict):
        url = "http://localhost:5000/incomes"
        response = self._client.post(url, content=orjson.dumps(model))
        return response.json()

    def add_income(self, model:dict):
        url = "http://localhost:5000/add_incomes"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def delete_income(self, model: dict):
        url = "http://localhost:5000/delete_incomes"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_income_name(self, model: dict):
        url = "http://localhost:5000/edit_incomes_name"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_income_sum(self, model: dict):
        url = "http://localhost:5000/edit_incomes_sum"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_income_date(self, model: dict):
        url = "http://localhost:5000/edit_incomes_date"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def edit_incomes_type(self, model: dict):
        url = "http://localhost:5000/edit_incomes_type"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    # send feedback to admin
    def send_feedback(self, model: dict):
        url = "http://localhost:5000/send_feedback"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_all_feedback(self):
        url = "http://localhost:5000/get_feedback"
        response = self._client.get(url)
        return response

    # reports of aims, incomes, expenses

    def get_aims_for_report(self, model: dict):
        url = "http://localhost:5000/aims_report"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_incomes_for_report(self, model:dict):
        url = "http://localhost:5000/incomes_report"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_expenses_for_report(self, model:dict):
        url = "http://localhost:5000/expenses_report"
        response = self._client.post(url, content=orjson.dumps(model))
        return response

    def get_num_of_marks(self):
        url = "http://localhost:5000/get_num_marks"
        response = self._client.get(url)
        return response
