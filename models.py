from typing import Optional
import json
from pydantic import BaseModel as Base
import datetime


class UserModel(Base):
    user_id: Optional[int]
    user_login: Optional[str]
    user_password: Optional[str]
    is_admin: Optional[bool]
    is_blocked: Optional[bool]


class ExpensesModel(Base):
    exp_id: Optional[int]
    user_id: Optional[int]
    user_login: Optional[str]
    is_put_aside: Optional[bool]
    exp_name: Optional[str]
    new_name: Optional[str]
    summa: Optional[float]
    exp_date: Optional[datetime.date]
    type_of_sorting: Optional[str]
    type_of_filter: Optional[str]


class IncomesModel(Base):
    inc_id: Optional[int]
    user_id: Optional[int]
    user_login: Optional[str]
    is_const: Optional[bool]
    new_const: Optional[bool]
    inc_name: Optional[str]
    new_name: Optional[str]
    summa: Optional[float]
    inc_date: Optional[datetime.date]
    new_date: Optional[datetime.date]
    type_of_sorting: Optional[str]
    type_of_filter: Optional[str]


class FinanceAimModel(Base):
    aim_id: Optional[int]
    user_id: Optional[int]
    user_login: Optional[str]
    aim_name: Optional[str]
    new_name: Optional[str]
    summa: Optional[float]
    put_aside: Optional[float]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    is_completed: Optional[bool]
    type_of_sorting: Optional[str]
    type_of_filter: Optional[str]


class ReportsModel(Base):
    report_id: Optional[int]
    user_id: Optional[int]
    incomes_report: str
    expenses_report: str
    #incomes_diagran_data: json
    #expenses_diagram_data: json


class FeedbackModel(Base):
    feedb_id: Optional[int]
    user_id: Optional[int]
    feedback: Optional[str]
    mark: Optional[int]
    user_login: Optional[str]


class ChangeUserModel(Base):
    old_login: Optional[str]
    old_password: Optional[str]
    new_login: Optional[str]
    new_password: Optional[str]
