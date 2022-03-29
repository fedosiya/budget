from typing import Optional
import uvicorn as uvicorn
from fastapi import FastAPI
from config.config import database
from models import *
import db.base
import db.tables

app = FastAPI()


@app.get("/")
async def read_root():
    return "Сервер запущен!"


@app.post("/sign_up")
async def sign_up(user_model: db.base.UserModel):
    message_from_db = db.base.sign_up(user_model)
    print(message_from_db)
    return message_from_db


@app.post("/sign_in")
async def sign_in(user_model: db.base.UserModel):
    message_from_db = db.base.sign_in(user_model)
    print(message_from_db)
    return message_from_db


@app.post("/change_login")
async def change_login(change_user_data_model: ChangeUserModel):
    message_from_db = db.base.change_login(change_user_data_model)
    print(message_from_db)
    return message_from_db


@app.post("/change_password")
async def change_password(change_user_data_model: ChangeUserModel):
    message_from_db = db.base.change_password(change_user_data_model)
    return message_from_db


@app.post("/block_users")
async def block_user(user_model: UserModel):
    message_from_db = db.base.block_user(user_model)
    return message_from_db


@app.post("/unblock_users")
async def unblock_user(model: UserModel):
    db_message = db.base.unblock_user(model)
    return db_message


@app.get("/blocked_users")
async def get_blocked_users():
    db_message = db.base.get_blocked_users()
    return db_message


@app.post("/delete_users")
async def delete_user(user_model: UserModel):
    message_from_db = db.base.delete_user(user_model)
    return message_from_db


@app.get("/users")
async def get_logins_of_users():
    message_from_db = db.base.get_logins()
    return message_from_db


@app.get("/get_values_for_admin")
async def get_admin_values():
    db_message = db.base.get_values_for_admin()
    return db_message


@app.post("/get_values_for_user")
async def get_user_values(model: UserModel):
    db_message = db.base.get_values_for_user(model)
    return db_message


@app.post("/get_aims")
async def get_aims(model: FinanceAimModel):
    db_message = db.base.get_aims(model)
    return db_message


@app.post("/get_aims_to_put_aside")
async def get_aims(model: FinanceAimModel):
    db_message = db.base.get_aims_to_put_aside(model)
    return db_message


@app.post("/add_aim")
async def add_aim(model: FinanceAimModel):
    db_message = db.base.add_aim(model)
    return db_message


@app.post("/edit_aim_name")
async def edit_aim_name(model: FinanceAimModel):
    db_message = db.base.edit_aim_name(model)
    return db_message


@app.post("/edit_aim_sum")
async def edit_aim_name(model: FinanceAimModel):
    db_message = db.base.edit_aim_sum(model)
    return db_message


@app.post("/edit_aim_deadline")
async def edit_deadline(model: FinanceAimModel):
    db_message = db.base.edit_deadline(model)
    return db_message


@app.post("/make_aim_completed")
async def make_completed(model: FinanceAimModel):
    db_message = db.base.make_aim_completed(model)
    return db_message


@app.post("/delete_aims")
async def delete_aim(model: FinanceAimModel):
    db_message = db.base.delete_aim(model)
    return db_message


@app.post("/to_put_aside")
async def delete_aim(model: FinanceAimModel):
    db_message = db.base.put_aside(model)
    return db_message


@app.post("/add_incomes")
async def add_income(model: IncomesModel):
    message_from_db = db.base.add_income(model)
    return message_from_db


@app.post("/delete_incomes")
async def delete_income(model: IncomesModel):
    message_from_db = db.base.delete_income(model)
    return message_from_db


@app.post("/incomes")
async def get_incomes(model: IncomesModel):
    message_from_db = db.base.get_incomes(model)
    return message_from_db


@app.post("/edit_incomes_name")
async def edit_incomes_name(model: IncomesModel):
    db_message = db.base.edit_income_name(model)
    return db_message


@app.post("/edit_incomes_sum")
async def edit_incomes_sum(model: IncomesModel):
    db_message = db.base.edit_income_sum(model)
    return db_message


@app.post("/edit_incomes_date")
async def edit_incomes_date(model: IncomesModel):
    db_message = db.base.edit_income_date(model)
    return db_message


@app.post("/edit_incomes_type")
async def edit_incomes_sum(model: IncomesModel):
    db_message = db.base.edit_income_type(model)
    return db_message


@app.post("/get_expenses")
async def get_exp(model: ExpensesModel):
    db_message = db.base.get_expenses(model)
    return db_message


@app.post("/add_exp")
async def add_exp(model: ExpensesModel):
    db_message = db.base.add_exp(model)
    return db_message


@app.post("/get_aims_to_put_aside")
async def get_aims_to_put_aside(model: FinanceAimModel):
    db_message = db.base.get_aims_to_put_aside(model)
    return db_message


@app.post("/delete_exp")
async def delete_exp(model: ExpensesModel):
    db_message = db.base.delete_exp(model)
    return db_message


@app.post("/edit_exp_name")
async def edit_exp_name(model: ExpensesModel):
    db_message = db.base.edit_exp_name(model)
    return db_message


@app.post("/edit_exp_sum")
async def edit_exp_sum(model: ExpensesModel):
    db_message = db.base.edit_exp_sum(model)
    return db_message


@app.post("/edit_exp_date")
async def edit_exp_date(model: ExpensesModel):
    db_message = db.base.edit_exp_date(model)
    return db_message


@app.post("/send_feedback")
async def send_feedback(model: FeedbackModel):
    db_message = db.base.send_feedback(model)
    return db_message


@app.get("/get_feedback")
async def get_feedback():
    db_message = db.base.get_feedback()
    return db_message


@app.post("/aims_report")
async def aims_report(model: UserModel):
    db_message = db.base.get_aims_for_report(model)
    return db_message


@app.post("/incomes_report")
async def incomes_report(model: UserModel):
    db_message = db.base.get_incomes_for_report(model)
    return db_message


@app.post("/expenses_report")
async def expenses_report(model: UserModel):
    db_message = db.base.get_expenses_for_report(model)
    return db_message


@app.get("/get_num_marks")
async def get_num_marks():
    db_message = db.base.get_num_marks()
    return db_message


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=5000, reload=True, access_log=False)
