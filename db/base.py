from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session, query, sessionmaker
from config.config import DATABASE_URL
from datetime import datetime, timedelta
import datetime

from models import *
from db.tables import *

from password import Password

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def sign_up(user_model: UserModel):
    res = session.query(User).filter(User.user_login == user_model.user_login).all()
    if not res:
        hashed_passw = Password()
        hashed_passw.set_password(user_model.user_password)
        user_model.user_password = hashed_passw.get_hashed_password().decode()

        new_user = User(
            user_login=user_model.user_login,
            user_password=user_model.user_password,
            is_admin=False,
            is_blocked=False
        )

        session.add(new_user)
        session.commit()
        return "Пользователь успешно создан"

    else:
        return "Пользователь с таким логином существует"


def sign_in(user_model: UserModel):
    is_blocked = session.query(User.is_blocked).filter(and_(User.user_login == user_model.user_login,
                                                            User.is_blocked != False)).first()
    if is_blocked:
        return "Пользователь был заблокирован адинистратором"
    else:
        hashed_passw = Password()
        hashed_passw.set_password(user_model.user_password)
        res = session.query(User).filter(User.user_login == user_model.user_login).all()
        if not res or not \
                hashed_passw.check_password(user_model.user_password.encode(), hashed_passw.get_hashed_password()):
            return "Неверный логин/пароль"
        else:
            return "Успешный вход"


def change_login(change_user_data: ChangeUserModel):
    try:
        session.query(User).filter(User.user_login == change_user_data.old_login).update(
            {"user_login": change_user_data.new_login}, synchronize_session='fetch')
        session.commit()
        return "Логин изменен"
    except:
        return "Пользователь с таким логином уже существует!"


def change_password(change_user_data: ChangeUserModel):
    hashed_passw = Password()
    hashed_passw.set_password(change_user_data.new_password)
    change_user_data.new_password = hashed_passw.get_hashed_password().decode()
    session.query(User).filter(User.user_login == change_user_data.old_login).update(
            {"user_password": change_user_data.new_password}, synchronize_session='fetch')
    session.commit()
    return "Пароль изменен"


def get_logins():
    is_admin = False
    res = session.query(User.user_login).filter(User.is_admin == is_admin).all()
    if not res:
        print("В системе нет пользователей")
    else:
        logins_list = []
        for row in res:
            logins_list.append(row.user_login)
        return logins_list


def get_values_for_admin():
    users = session.query(User).all()
    incomes = session.query(Income).all()
    exp = session.query(Expense).all()
    aims = session.query(Financeaim).all()
    fb = session.query(Feedback).all()
    list_of_values = {"num_incomes": len(incomes),
                      "num_expenses": len(exp),
                      "num_aims": len(aims),
                      "num_users": len(users),
                      "num_feedbacks": len(fb)}
    return list_of_values


def get_values_for_user(model: UserModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]

    incomes = session.query(Income).filter(Income.user_id == model.user_id).all()
    exp = session.query(Expense).filter(Expense.user_id == model.user_id).all()
    aims = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).all()
    c_aims = session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                                   Financeaim.is_completed == True)).all()
    fb = session.query(Feedback).filter(Feedback.user_id == model.user_id).all()
    list_of_values = {"num_incomes": len(incomes),
                      "num_expenses": len(exp),
                      "num_aims": len(aims),
                      "num_completed_aims": len(c_aims),
                      "num_feedbacks": len(fb)}
    return list_of_values


def block_user(user: UserModel):
    try:
        session.query(User).filter(User.user_login == user.user_login).update(
            {"is_blocked": user.is_blocked}, synchronize_session='fetch')
        session.commit()
        return "Пользователь заблокирован!"
    except:
        return "Ошибка.Позователь уже заблокирован!"


def unblock_user(model: UserModel):
    session.query(User).filter(and_(User.user_login == model.user_login,
                                    User.is_blocked != model.is_blocked)).update({"is_blocked": model.is_blocked},
                                                                                 synchronize_session='fetch')
    session.commit()
    return "Разблокирован"


def get_blocked_users():
    model = UserModel(is_blocked=True)
    users = session.query(User.user_login).filter(User.is_blocked == model.is_blocked).all()
    return users


def delete_user(user: UserModel):
    session.query(User).filter(User.user_login == user.user_login).delete(synchronize_session='fetch')
    session.commit()
    return "Пользователь удален"


def add_aim(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).first()
    model.user_id = user_id[0]
    new_aim = Financeaim(user_id=model.user_id,
                         aim_name=model.aim_name,
                         start_date=model.start_date,
                         end_date=model.end_date,
                         summa=model.summa,
                         is_completed=model.is_completed,
                         put_aside=model.put_aside)
    session.add(new_aim)
    session.commit()
    return "Добавлено"


def get_aims(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    if model.type_of_sorting:
        if model.type_of_sorting == "По алфавиту":
            res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).order_by(Financeaim.aim_name).all()
        elif model.type_of_sorting == "По дате":
            res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).order_by(Financeaim.start_date).all()
        else:
            res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).order_by(Financeaim.summa).all()
    else:
        if model.type_of_filter == "Все цели":
            res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).order_by(Financeaim.aim_name).all()
        elif model.type_of_filter == "Выполненные":
            res = session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                                        Financeaim.is_completed == model.is_completed)).order_by(Financeaim.aim_name).all()
        else:
            res = session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                                        Financeaim.is_completed == model.is_completed)).order_by(Financeaim.aim_name).all()
    if not res:
        return "Нет значений"
    else:
        return res


def edit_aim_name(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).update({"aim_name": model.new_name},
                                                                                         synchronize_session='fetch')
    session.commit()
    return "Изменено"


def edit_aim_sum(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).update({"summa": model.summa},
                                                                                         synchronize_session='fetch')
    session.commit()
    return "Изменено"


def edit_deadline(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).update({"end_date": model.end_date},
                                                                                         synchronize_session='fetch')
    session.commit()
    return "Изменено"


def make_aim_completed(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).update({"is_completed": model.is_completed},
                                                                                         synchronize_session='fetch')
    session.commit()
    return "Изменено"


def delete_aim(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).delete(synchronize_session='fetch')
    session.commit()
    return "Удалено"


def put_aside(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]

    money = session.query(Financeaim.put_aside).filter(and_(Financeaim.user_id == model.user_id, Financeaim.aim_name ==
                                                            model.aim_name)).first()
    model.put_aside = model.put_aside + float(money[0])
    session.query(Financeaim).filter(and_(Financeaim.user_id == model.user_id,
                                          Financeaim.aim_name == model.aim_name)).update({"put_aside": model.put_aside},
                                                                                         synchronize_session='fetch')
    session.commit()
    return "Отложено"


def get_incomes(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    if model.type_of_sorting:
        if model.type_of_sorting == "По алфавиту":
            res = session.query(Income).filter(Income.user_id == model.user_id).order_by(Income.inc_name).all()
        elif model.type_of_sorting == "По дате":
            res = session.query(Income).filter(Income.user_id == model.user_id).order_by(Income.inc_date).all()
        else:
            res = session.query(Income).filter(Income.user_id == model.user_id).order_by(Income.summa).all()
    else:
        if model.type_of_filter == "Постоянные":
            res = session.query(Income).filter(and_(Income.user_id == model.user_id,
                                                    Income.is_const == model.is_const)).order_by(Income.inc_name).all()
        elif model.type_of_filter == "Непостоянные":
            res = session.query(Income).filter(and_(Income.user_id == model.user_id,
                                                    Income.is_const != model.is_const)).order_by(Income.inc_name).all()
        elif model.type_of_filter == "За первое полугодие":
            res = session.query(Income).filter(and_(Income.user_id == model.user_id, Income.inc_date >= "2021-01-01",
                                                    Income.inc_date < "2021-07-01")).order_by(Income.inc_date).all()
        elif model.type_of_filter == "За второе полугодие":
            res = session.query(Income).filter(and_(Income.user_id == model.user_id, Income.inc_date >= "2021-07-01",
                                                    Income.inc_date < "2022-01-01")).order_by(Income.inc_date).all()
        else:
            res = session.query(Income).filter(Income.user_id == model.user_id).order_by(Income.inc_name).all()
    if not res:
        return "Нет значений"
    else:
        return res


def add_income(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    new_income = Income(user_id=model.user_id,
                        inc_name=model.inc_name,
                        summa=model.summa,
                        inc_date=model.inc_date,
                        is_const=model.is_const)
    session.add(new_income)
    session.commit()
    return "Добавлено"


def delete_income(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Income).filter(and_(Income.user_id == model.user_id,
                                      Income.inc_name == model.inc_name)).delete(synchronize_session='fetch')
    session.commit()
    return "Удалено"


def edit_income_name(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).first()
    model.user_id = user_id[0]
    session.query(Income).filter(and_(Income.user_id == model.user_id,
                                      Income.inc_name == model.inc_name)).update({"inc_name": model.new_name},
                                                                                 synchronize_session='fetch')
    session.commit()
    return "Изменено"


def edit_income_sum(model: IncomesModel):
    id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = id[0][0]
    session.query(Income).filter(and_(Income.user_id == model.user_id,
                                      Income.inc_name == model.inc_name)).update({"summa": model.summa},
                                                                                 synchronize_session='fetch')

    session.commit()
    return "Изменено"


def edit_income_date(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Income).filter(and_(Income.user_id == model.user_id,
                                      Income.inc_name == model.inc_name)).update({"inc_date": model.new_date},
                                                                                 synchronize_session='fetch')

    session.commit()
    return "Изменено"


def edit_income_type(model: IncomesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Income).filter(and_(Income.user_id == model.user_id,
                                      Income.inc_name == model.inc_name)).update({"is_const": model.new_const},
                                                                                 synchronize_session='fetch')

    session.commit()
    return "Изменено"


def get_expenses(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    if model.type_of_sorting:
        if model.type_of_sorting == "По алфавиту":
            res = session.query(Expense).filter(Expense.user_id == model.user_id).order_by(Expense.exp_name).all()
        elif model.type_of_sorting == "По дате":
            res = session.query(Expense).filter(Expense.user_id == model.user_id).order_by(Expense.exp_date).all()
        else:
            res = session.query(Expense).filter(Expense.user_id == model.user_id).order_by(Expense.summa).all()
    else:
        if model.type_of_filter == "Отложенные":
            res = session.query(Expense).filter(and_(Expense.user_id == model.user_id,
                                                     Expense.is_put_aside == model.is_put_aside)).order_by(Expense.exp_name).all()
        elif model.type_of_filter == "За первое полугодие":
            res = session.query(Expense).filter(and_(Expense.user_id == model.user_id, Expense.exp_date >= "2021-01-01",
                                                     Expense.exp_date < "2021-07-01")).order_by(Expense.exp_date).all()
        elif model.type_of_filter == "За второе полугодие":
            res = session.query(Expense).filter(and_(Expense.user_id == model.user_id, Expense.exp_date < "2022-01-01",
                                                     Expense.exp_date >= "2021-07-01")).order_by(Expense.exp_date).all()
        else:
            res = session.query(Expense).filter(Expense.user_id == model.user_id).order_by(Expense.exp_name).all()

    if not res:
        return "Нет значений"
    else:
        return res


def add_exp(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    new_exp = Expense(user_id=model.user_id,
                      exp_name=model.exp_name,
                      summa=model.summa,
                      exp_date=model.exp_date,
                      is_put_aside=model.is_put_aside)
    session.add(new_exp)
    session.commit()
    return "Добавлено"


def save_money(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    new_exp = Expense(user_id=model.user_id,
                      exp_name=model.exp_name,
                      summa=model.summa,
                      exp_date=model.exp_date,
                      is_put_aside=model.is_put_aside)
    session.add(new_exp)
    session.commit()
    return "Добавлено"


def get_aims_to_put_aside(model: FinanceAimModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).all()
    if not res:
        print("У пользователя нет финансовых целей")
    else:
        aims_list = []
        for row in res:
            aims_list.append(row.aim_name)
        return aims_list


def delete_exp(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Expense).filter(and_(Expense.user_id == model.user_id,
                                       Expense.exp_name == model.exp_name)).delete(synchronize_session='fetch')
    session.commit()
    return "Удалено"


def edit_exp_name(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Expense).filter(and_(Expense.user_id == model.user_id,
                                       Expense.exp_name == model.exp_name)).update({"exp_name": model.new_name},
                                                                                   synchronize_session='fetch')
    session.commit()
    return "Изменено"


def edit_exp_sum(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Expense).filter(and_(Expense.user_id == model.user_id,
                                       Expense.exp_name == model.exp_name)).update({"summa": model.summa},
                                                                                   synchronize_session='fetch')
    session.commit()
    return "Изменено"


def edit_exp_date(model: ExpensesModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    session.query(Expense).filter(and_(Expense.user_id == model.user_id,
                                       Expense.exp_name == model.exp_name)).update({"exp_date": model.exp_date},
                                                                                   synchronize_session='fetch')
    session.commit()
    return "Изменено"


def send_feedback(model: FeedbackModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    feedback = Feedback(user_id=model.user_id,
                        user_login=model.user_login,
                        feedback=model.feedback,
                        appresial=model.mark)
    session.add(feedback)
    session.commit()
    return "Отправлено"


def get_feedback():
    res = session.query(Feedback).all()
    if not res:
        return "Нет значений"
    else:
        return res


def get_aims_for_report(model: UserModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    res = session.query(Financeaim).filter(Financeaim.user_id == model.user_id).all()
    return res


def get_incomes_for_report(model: UserModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    res = session.query(Income).filter(Income.user_id == model.user_id).all()
    return res


def get_expenses_for_report(model: UserModel):
    user_id = session.query(User.user_id).filter(User.user_login == model.user_login).all()
    model.user_id = user_id[0][0]
    res = session.query(Expense).filter(Expense.user_id == model.user_id).all()
    return res


def get_num_marks():
    marks_list = []
    one = session.query(Feedback.appresial).filter(Feedback.appresial == 1).all()
    two = session.query(Feedback.appresial).filter(Feedback.appresial == 2).all()
    three = session.query(Feedback.appresial).filter(Feedback.appresial == 3).all()
    four = session.query(Feedback.appresial).filter(Feedback.appresial == 4).all()
    five = session.query(Feedback.appresial).filter(Feedback.appresial == 5).all()
    marks_list.append(len(one))
    marks_list.append(len(two))
    marks_list.append(len(three))
    marks_list.append(len(four))
    marks_list.append(len(five))
    return marks_list
