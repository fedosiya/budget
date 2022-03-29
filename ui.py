from datetime import date
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QMainWindow, QListWidget, QListWidgetItem, \
    QAbstractItemView, QMessageBox
from UI import *
from client_service import ClientService
import matplotlib.pyplot as plt

client = ClientService()

# for listBox
users_list_item: str
aims_list_item: str

# for DB
simple_user_login: str
list_of_incomes: str
income_name: str
exp_name: str
aim_name: str
start_date: date


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('UI/mainWindow.ui', self)
        self.signUpButton.clicked.connect(self.sign_in)
        self.signInButton.clicked.connect(self.sign_up)

    def update_line_edit(self):
        self.inputLogin.clear()
        self.inputPassword.clear()

    def sign_in(self):
        login = self.inputLogin.text()
        passw = self.inputPassword.text()

        if not login or not passw:
            print("Не все поля заполнены!")
        else:
            user = {"user_login": login, "user_password": passw}
            response = client.sign_in(user)
            if response.json() == "Успешный вход" and login == "admin":
                admin_menu = AdminMenu()
                widget.addWidget(admin_menu)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif response.json() == "Успешный вход":
                global simple_user_login
                simple_user_login = login
                user_menu = UserMenu()
                widget.addWidget(user_menu)
                widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up(self):
        sign_up_menu = SignUpMenu()
        widget.addWidget(sign_up_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUpMenu(QDialog):
    def __init__(self):
        super(SignUpMenu, self).__init__()
        loadUi('UI/signUpWindow.ui', self)
        self.signInButton.clicked.connect(self.sign_up)
        self.backButton.clicked.connect(self.gotomain)

    def sign_up(self):
        login = self.inputLogin.text()
        passw = self.inputPassword.text()

        if not login or not passw:
            message = QMessageBox()
            message.setWindowTitle("Регистрация")
            message.setText("Не все поля заполнены!")
            message.setIcon(QMessageBox.Warning)
            message.setStandardButtons(QMessageBox.Ok)
            message.exec_()
        else:
            user = {"user_login": login, "user_password": passw}
            response = client.sign_up(user)
            message = QMessageBox()
            message.setWindowTitle("Регистрация")
            message.setText(response.json())
            message.setIcon(QMessageBox.Information)
            message.setStandardButtons(QMessageBox.Ok)
            message.exec_()

            main = MainWindow()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotomain(self):
        main = MainWindow()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminMenu(QDialog):
    def __init__(self):
        super(AdminMenu, self).__init__()
        loadUi('UI/adminMenu_d.ui', self)
        self.quitBtn.clicked.connect(self.return_to_main)
        self.workWithUsersBtn.clicked.connect(self.work_with_users_data)
        self.unblockedBtn.clicked.connect(self.unblock_users)
        self.usersStatsBtn.clicked.connect(self.check_statistics)
        self.feedbackBtn.clicked.connect(self.check_feedback)

    def return_to_main(self):
        main = MainWindow()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def work_with_users_data(self):
        users_data_menu = UserChangerMenu()
        widget.addWidget(users_data_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def unblock_users(self):
        unblock_menu = UnblockUsersMenu()
        widget.addWidget(unblock_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def check_statistics(self):
        st = AdminStatistics()
        widget.addWidget(st)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def check_feedback(self):
        fb = AdminFeedback()
        widget.addWidget(fb)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AdminStatistics(QDialog):
    def __init__(self):
        super(AdminStatistics, self).__init__()
        loadUi("UI/adminStatistics.ui", self)
        self.quitBtn.clicked.connect(self.close_window)
        self.marksReportBtn.clicked.connect(self.show_diagram)
        self.set_values()

    def close_window(self):
        admin = AdminMenu()
        widget.addWidget(admin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def show_diagram(self):
        labels = ["Оценка 1", "Оценка 2", "Оценка 3", "Оценка 4", "Оценка 5"]
        res = client.get_num_of_marks()
        vals = res.json()
        plt.pie(vals, labels=labels)
        plt.show()

    def set_values(self):
        res = client.get_values_for_admin_stat()
        values_list = res.json()
        self.numIncomes.setText(str(values_list["num_incomes"]))
        self.numExpenses.setText(str(values_list["num_expenses"]))
        self.numAims.setText(str(values_list["num_aims"]))
        self.numUsers.setText(str(values_list["num_users"]))
        self.numFeedbacks.setText(str(values_list["num_feedbacks"]))


class AdminFeedback(QDialog):
    def __init__(self):
        super(AdminFeedback, self).__init__()
        loadUi("UI/adminFeedback.ui", self)
        self.quitBtn.clicked.connect(self.close_window)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.get_all_feedback()

    def close_window(self):
        menu = AdminMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def get_all_feedback(self):
        f = client.get_all_feedback()
        feedback = f.json()
        if feedback == "Нет значений":
            row = 0
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("--"))

        else:
            row = 0
            self.tableWidget.setRowCount(len(feedback))
            for item in feedback:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["user_login"]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(item["feedback"])))
                row = row + 1


class UserChangerMenu(QDialog, QListWidget):
    def __init__(self):
        super(UserChangerMenu, self).__init__()
        loadUi('UI/userChanger.ui', self)
        self.changeLoginBtn.clicked.connect(self.change_user_login)
        self.changePasswBtn.clicked.connect(self.change_user_password)
        self.blockBtn.clicked.connect(self.block_user)
        self.deleteUserBtn.clicked.connect(self.delete_user)
        self.quitBtn.clicked.connect(self.return_to_menu)
        self.listOfUsers.itemClicked.connect(self.get_item_of_list)
        self.get_list_of_users()
        self.sortByLogin.clicked.connect(self.sort_users)

    def get_list_of_users(self):
        list_of_logins = client.get_logins_of_users()
        self.listOfUsers.addItems(list_of_logins)

    def sort_users(self):
        self.listOfUsers.sortItems()

    def get_item_of_list(self):
        global users_list_item
        users_list_item = self.listOfUsers.currentItem().text()

    def change_user_login(self):
        change_login = ChangeUserLogin()
        widget.addWidget(change_login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def change_user_password(self):
        change_passw = ChangeUserPassword()
        widget.addWidget(change_passw)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def block_user(self):
        user = {"user_login": users_list_item, "is_blocked": True}
        res = client.block_user(user)
        if res == "Пользователь заблокирован":
            message = QMessageBox()
            message.setWindowTitle("Информация")
            message.setText("Пользователь заблокирован")
            message.setIcon(QMessageBox.Information)
            message.setStandardButtons(QMessageBox.Ok)
            message.exec_()
        else:
            message = QMessageBox()
            message.setWindowTitle("Ошибка!")
            message.setText("Этот пользователь уже заблокирован!")
            message.setIcon(QMessageBox.Warning)
            message.setStandardButtons(QMessageBox.Ok)
            message.exec_()

    def delete_user(self):
        user = {"user_login": users_list_item}
        res = client.delete_user(user)
        print(res.json())
        self.listOfUsers.clear()
        self.get_list_of_users()

    def return_to_menu(self):
        menu = AdminMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class ChangeUserLogin(QDialog):
    def __init__(self):
        super(ChangeUserLogin, self).__init__()
        loadUi('UI/changeLogin.ui', self)
        self.quitBtn.clicked.connect(self.close_window)
        self.changeBtn.clicked.connect(self.change_login)

    def close_window(self):
        changer = UserChangerMenu()
        widget.addWidget(changer)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def change_login(self):
        new_login = self.inputNewLogin.text()
        if not new_login:
            print("Введите логин!")
        else:
            global users_list_item
            change_user_data_model = {"old_login": users_list_item, "new_login":new_login}
            response = client.change_user_login(change_user_data_model)
            if response.json() == "Логин изменен":
                print("Логин изменен") #messagebox
                self.close_window()
            else:
                print("Пользователь с таким логином существует") #messagebox
                self.close_window()


class ChangeUserPassword(QDialog):
    def __init__(self):
        super(ChangeUserPassword, self).__init__()
        loadUi('UI/changePassword.ui', self)
        self.quitBtn.clicked.connect(self.close_window)
        self.changeBtn.clicked.connect(self.change_password)

    def close_window(self):
        changer = UserChangerMenu()
        widget.addWidget(changer)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def change_password(self):
        new_password = self.inputNewPassword.text()
        if not new_password:
            print("Введите пароль!") #messagebox
        else:
            global users_list_item
            change_user_data_model = {"old_login": users_list_item, "new_password": new_password}
            response = client.change_user_password(change_user_data_model)
            if response.json() == "Пароль изменен":
                print("Пароль изменен") #messagebox
                self.close_window()


class UnblockUsersMenu(QDialog):
    def __init__(self):
        super(UnblockUsersMenu, self).__init__()
        loadUi('UI/unblockUsersMenu.ui', self)
        self.quitBtn.clicked.connect(self.close_window)
        self.unblockBtn.clicked.connect(self.unblock)
        self.get_blocked_users()

    def get_blocked_users(self):
        blocked_users = client.get_blocked_users()
        for row in blocked_users:
            self.listOfBlockedUsers.addItem(row["user_login"])

    def close_window(self):
        admin = AdminMenu()
        widget.addWidget(admin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def unblock(self):
        login = self.listOfBlockedUsers.currentItem().text()
        model = {"user_login": login,
                 "is_blocked": False}
        res = client.unblock_user(model)
        print(res.json())
        self.listOfBlockedUsers.clear()
        self.get_blocked_users()


class UserMenu(QDialog):
    def __init__(self):
        super(UserMenu, self).__init__()
        loadUi('UI/userMenu.ui', self)
        self.quitBtn.clicked.connect(self.go_to_main)
        self.aimBtn.clicked.connect(self.work_with_aims)
        self.expensesBtn.clicked.connect(self.work_with_expenses)
        self.incomeBtn.clicked.connect(self.work_with_incomes)
        self.statBtn.clicked.connect(self.check_stats)
        self.feedbackBtn.clicked.connect(self.create_feedback)

    def go_to_main(self):
        main = MainWindow()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def work_with_aims(self):
        aims = AimsMenu()
        widget.addWidget(aims)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def work_with_expenses(self):
        exp = ExpensesMenu()
        widget.addWidget(exp)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def work_with_incomes(self):
        inc = IncomesMenu()
        widget.addWidget(inc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def check_stats(self):
        st = UserStatistics()
        widget.addWidget(st)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def create_feedback(self):
        feedb = FeedBackUser()
        widget.addWidget(feedb)
        widget.setCurrentIndex(widget.currentIndex()+1)


class UserStatistics(QDialog):
    def __init__(self):
        super(UserStatistics, self).__init__()
        loadUi("UI/userStatistics.ui", self)
        self.quitBtn.clicked.connect(self.close_window)
        self.set_values()

    def close_window(self):
        menu = UserMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def set_values(self):
        model = {"user_login": simple_user_login}
        res = client.get_values_for_user_stat(model)
        values_list = res.json()
        self.numIncomes.setText(str(values_list["num_incomes"]))
        self.numExpenses.setText(str(values_list["num_expenses"]))
        self.numAims.setText(str(values_list["num_aims"]))
        self.numCompletedAims.setText(str(values_list["num_completed_aims"]))
        self.numFeedbacks.setText(str(values_list["num_feedbacks"]))


class AimsMenu(QDialog):
    def __init__(self):
        super(AimsMenu, self).__init__()
        loadUi('UI/aimsMenu.ui', self)
        self.quitBtn.clicked.connect(self.close_window)
        self.addAimBtn.clicked.connect(self.add_aim)
        self.editAimBtn.clicked.connect(self.edit_aim)
        self.deleteAimBtn.clicked.connect(self.delete_aim)
        self.createReportBtn.clicked.connect(self.create_report)
        self.sortBtn.clicked.connect(self.sort_items)
        self.filterBtn.clicked.connect(self.filter_items)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.get_aims_of_user(type_of_sorting="По алфавиту")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def get_aims_of_user(self, **kwargs):
        user = {}
        if "type_of_sorting" in kwargs:
            user = {"user_login": simple_user_login, "type_of_sorting": kwargs["type_of_sorting"]}
        elif "type_of_filter" in kwargs:
            if kwargs["type_of_filter"] == "Выполненные цели":
                user = {"user_login": simple_user_login, "type_of_filter": kwargs["type_of_filter"],
                        "is_completed": True}
            elif kwargs["type_of_filter"] == "Невыполненные цели":
                user = {"user_login": simple_user_login, "type_of_filter": kwargs["type_of_filter"],
                        "is_completed": False}
            else:
                user = {"user_login": simple_user_login, "type_of_filter": kwargs["type_of_filter"]}
        a = client.get_aims(user)
        aims = a.json()
        if aims == "Нет значений":
            row = 0
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem("--"))

        else:
            row = 0
            self.tableWidget.setRowCount(len(aims))
            for aim in aims:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(aim["aim_name"]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(aim["start_date"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(aim["end_date"]))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(aim["summa"])))
                if aim["is_completed"]:
                    aim["is_completed"] = "Да"
                else:
                    aim["is_completed"] = "Нет"
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(aim["is_completed"]))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(aim["put_aside"])))
                row = row + 1

    def close_window(self):
        user_menu = UserMenu()
        widget.addWidget(user_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def add_aim(self):
        add = AddAimWindow()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def edit_aim(self):
        global aim_name, start_date
        aim_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        data = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        y = data[0:4]
        year = int(y)
        m = data[5:7]
        month = int(m)
        d = data[8:10]
        day = int(d)
        edit = EditAimMenu()
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex()+1)
        start_date = date(year, month, day)

    def delete_aim(self):
        row_to_delete = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        model = {"aim_name": row_to_delete, "user_login": simple_user_login}
        client.delete_aim(model)
        self.get_aims_of_user(type_of_sorting="По алфавиту")

    def create_report(self):
        model = {"user_login": simple_user_login}
        res = client.get_aims_for_report(model)
        values = res.json()
        f = open(f"reports/{simple_user_login}_цели.txt", 'w')
        try:
            for value in values:
                aim_name = value["aim_name"]
                end_date = value["end_date"]
                is_comp = value["is_completed"]
                if is_comp:
                    is_comp1 = "Да"
                else:
                    is_comp1 = "Нет"
                start = value["start_date"]
                summa = value["summa"]
                put_aside = value["put_aside"]

                f.write(f"Название: {aim_name} \n"
                        f"Дата постановки цели: {start}\n"
                        f"Дедлайн {end_date} \n"
                        f"Сумма для достижения: {summa} \n"
                        f"Отложенные средства: {put_aside} \n"
                        f"Является ли цель достигнутой: {is_comp1} \n"
                        f"________________________________________________________________________ \n")

        finally:
            f.close()
            print("Отчет создан") #messagebox

    def sort_items(self):
        s_type = str(self.sortBox.currentText())
        self.get_aims_of_user(type_of_sorting=s_type)

    def filter_items(self):
        f_type = str(self.filterBox.currentText())
        self.get_aims_of_user(type_of_filter=f_type)


class EditAimMenu(QDialog):
    def __init__(self):
        super(EditAimMenu, self).__init__()
        loadUi('UI/editAim.ui', self)
        self.editNameBtn.clicked.connect(self.edit_name)
        self.editSumBtn.clicked.connect(self.edit_sum)
        self.editDeadlineBtn.clicked.connect(self.edit_deadline)
        self.makeCompletedBtn.clicked.connect(self.make_completed)
        self.quitBtn.clicked.connect(self.close_window)

    def edit_name(self):
        global aim_name
        new_name = self.inputName.text()
        model = {"user_login": simple_user_login, "aim_name": aim_name, "new_name": new_name}
        res = client.edit_aim_name(model)
        print(res.json())
        aim_name = new_name

    def edit_sum(self):
        new_sum = self.inputSum.value()
        model = {"user_login": simple_user_login, "aim_name": aim_name, "summa": new_sum}
        res = client.edit_aim_sum(model)
        print(res.json())

    def edit_deadline(self):
        global start_date
        new_deadline = self.inputDate.date()
        new_deadline = new_deadline.toPyDate()
        if new_deadline <= start_date:
            print("Неверно введена дата!")#messagebox
        else:
            model = {"user_login": simple_user_login, "aim_name": aim_name, "end_date": new_deadline}
            res = client.edit_deadline(model)
            print(res.json())
            start_date = new_deadline

    def make_completed(self):
        model = {"user_login": simple_user_login, "aim_name": aim_name, "is_completed": True}
        res = client.make_aim_completed(model)
        print(res.json())

    def close_window(self):
        menu = AimsMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AddAimWindow(QDialog):
    def __init__(self):
        super(AddAimWindow, self).__init__()
        loadUi('UI/addAimWindow.ui', self)
        self.addAimBtn.clicked.connect(self.add_aim)
        self.quitBtn.clicked.connect(self.close_window)

    def add_aim(self):
        name = self.inputName.text()
        summa = self.inputSum.value()
        start_date = self.inputDate.date()
        start_date = start_date.toPyDate()
        deadline = self.inputDeadline.date()
        deadline = deadline.toPyDate()
        if not name:
            print("Введите название!")#messagebox
        if start_date > deadline or start_date == deadline:
            print("Неверно введены даты") #messagebox
        else:
            model = {"user_login": simple_user_login,
                     "aim_name": name,
                     "summa": summa,
                     "start_date": start_date,
                     "end_date": deadline,
                     "put_aside": 0,
                     "is_completed": False}
            res = client.add_aim(model)
            print(res.json())
            self.close_window()

    def close_window(self):
        menu = AimsMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class IncomesMenu(QDialog):
    def __init__(self):
        super(IncomesMenu, self).__init__()
        loadUi('UI/incomesMenu.ui', self)
        self.addBtn.clicked.connect(self.add_income)
        self.editBtn.clicked.connect(self.edit_income)
        self.deleteBtn.clicked.connect(self.delete_income)
        self.createReportBtn.clicked.connect(self.create_report)
        self.sortBtn.clicked.connect(self.sort_items)
        self.filterBtn.clicked.connect(self.filter_items)
        self.quitBtn.clicked.connect(self.close_window)
        self.get_incomes_of_the_user(type_of_sorting="По алфавиту")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def get_incomes_of_the_user(self, **kwargs):
        user = {}
        if "type_of_sorting" in kwargs:
            user = {"user_login": simple_user_login,
                    "type_of_sorting": kwargs["type_of_sorting"]}
        elif "type_of_filter" in kwargs:
            user = {"user_login": simple_user_login,
                    "type_of_filter": kwargs["type_of_filter"],
                    "is_const": True}
        incomes = client.get_incomes_of_user(user)
        if incomes == "Нет значений":
            row = 0
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("--"))

        else:
            row = 0
            self.tableWidget.setRowCount(len(incomes))
            for income in incomes:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(income["inc_name"]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(income["summa"])))
                if income["is_const"]:
                    income["is_const"] = "Да"
                else:
                    income["is_const"] = "Нет"
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(income["is_const"]))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(income["inc_date"]))
                row = row+1

    def add_income(self):
        add = AddIncome()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def edit_income(self):
        global income_name
        income_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        if not income_name:
            print("Строка не выбрана") #messagebox
        else:
            wind = EditIncome()
            widget.addWidget(wind)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def delete_income(self):
        row_to_delete = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        model = {"inc_name": row_to_delete, "user_login": simple_user_login}
        client.delete_income(model)
        self.get_incomes_of_the_user(type_of_sorting="По алфавиту")

    def create_report(self):
        model = {"user_login": simple_user_login}
        res = client.get_incomes_for_report(model)
        values = res.json()
        f = open(f"reports/{simple_user_login}_доходы.txt", 'w')
        try:
            for value in values:
                inc_name = value["inc_name"]
                summa = value["summa"]
                date = value["inc_date"]
                is_const = value["is_const"]
                if is_const:
                    is_comp1 = "Да"
                else:
                    is_comp1 = "Нет"

                f.write(f"Название дохода: {inc_name} \n"
                        f"Сумма дохода: {summa}\n"
                        f"Дата получения: {date} \n"
                        f"Является ли доход постоянным: {is_comp1} \n"
                        f"________________________________________________________________________ \n")

        finally:
            f.close()
            print("Отчет создан")  # messagebox

    def sort_items(self):
        s_type = str(self.sortBox.currentText())
        self.get_incomes_of_the_user(type_of_sorting=s_type)

    def filter_items(self):
        f_type = str(self.filterBox.currentText())
        self.get_incomes_of_the_user(type_of_filter=f_type)

    def close_window(self):
        usrmain = UserMenu()
        widget.addWidget(usrmain)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AddIncome(QDialog):
    def __init__(self):
        super(AddIncome, self).__init__()
        loadUi('UI/addIncome.ui', self)
        self.addBtn.clicked.connect(self.add_income)
        self.quitBtn.clicked.connect(self.close_window)

    def close_window(self):
        inc_menu = IncomesMenu()
        widget.addWidget(inc_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def add_income(self):
        name = self.inputName.text()
        summ = self.inputSum.value()
        date = self.inputDate.date()
        date = date.toPyDate()
        type = self.typeBox.currentText()
        if type == "Постоянный":
            type1 = True
        else:
            type1 = False
        income_model = {"user_login": simple_user_login,
                        "is_const": type1,
                        "inc_name": name,
                        "summa": summ,
                        "inc_date": date}
        res = client.add_income(income_model)
        print(res.json())
        self.close_window()


class EditIncome(QDialog):
    def __init__(self):
        super(EditIncome, self).__init__()
        loadUi('UI/editIncome.ui', self)
        self.editNameBtn.clicked.connect(self.edit_name)
        self.editSumBtn.clicked.connect(self.edit_sum)
        self.editDateBtn.clicked.connect(self.edit_date)
        self.editTypeBtn.clicked.connect(self.edit_type)
        self.quitBtn.clicked.connect(self.close_window)

    def edit_name(self):
        global income_name
        new_name = self.inputName.text()
        model = {"user_login": simple_user_login, "inc_name": income_name, "new_name": new_name}
        res = client.edit_income_name(model)
        print(res.json())
        income_name = new_name

    def edit_sum(self):
        new_sum = self.inputSum.value()
        model = {"user_login": simple_user_login, "inc_name": income_name, "summa": new_sum}
        res = client.edit_income_sum(model)
        print(res.json())

    def edit_date(self):
        new_date = self.inputDate.date()
        new_date = new_date.toPyDate()
        model = {"user_login": simple_user_login, "inc_name": income_name, "new_date": new_date}
        res = client.edit_income_date(model)
        print(res.json())

    def edit_type(self):
        new_type = self.typeBox.currentText()
        if new_type == "Постоянный":
            type1 = True
        else:
            type1 = False
        model = {"user_login": simple_user_login, "inc_name": income_name, "new_const": type1}
        res = client.edit_incomes_type(model)
        print(res.json())

    def close_window(self):
        wind = IncomesMenu()
        widget.addWidget(wind)
        widget.setCurrentIndex(widget.currentIndex()+1)


class ExpensesMenu(QDialog):
    def __init__(self):
        super(ExpensesMenu, self).__init__()
        loadUi('UI/expensesMenu.ui', self)
        self.addBtn.clicked.connect(self.add_item)
        self.editBtn.clicked.connect(self.edit_item)
        self.deleteBtn.clicked.connect(self.delete_item)
        self.createReportBtn.clicked.connect(self.create_report)
        self.sortBtn.clicked.connect(self.sort_items)
        self.filterBtn.clicked.connect(self.filter_items)
        self.quitBtn.clicked.connect(self.close_window)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.get_expenses(type_of_sorting="По алфавиту")

    def get_expenses(self, **kwargs):
        user = {}
        if "type_of_sorting" in kwargs:
            user = {"user_login": simple_user_login,
                    "type_of_sorting": kwargs["type_of_sorting"]}
        elif "type_of_filter" in kwargs:
            user = {"user_login": simple_user_login,
                     "type_of_filter": kwargs["type_of_filter"],
                     "is_put_aside": True}
        exps = client.get_expenses(user)
        #exps = e.json()
        if exps == "Нет значений":
            row = 0
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem("--"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("--"))

        else:
            row = 0
            self.tableWidget.setRowCount(len(exps))
            for exp in exps:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(exp["exp_name"]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(exp["summa"])))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(exp["exp_date"]))

                if exp["is_put_aside"]:
                    exp["is_put_aside"] = "Да"
                else:
                    exp["is_put_aside"] = "Нет"
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(exp["is_put_aside"]))
                row = row + 1

    def add_item(self):
        add = AddExpenses()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def edit_item(self):
        global exp_name
        exp_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        edit = EditExpenses()
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def delete_item(self):
        row_to_delete = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        model = {"exp_name": row_to_delete, "user_login": simple_user_login}
        res = client.delete_exp(model)
        self.get_expenses(type_of_sorting="По алфавиту")

    def create_report(self):
        model = {"user_login": simple_user_login}
        res = client.get_expenses_for_report(model)
        values = res.json()
        f = open(f"reports/{simple_user_login}_расходы.txt", 'w')
        try:
            for value in values:
                expense_name = value["exp_name"]
                summa = value["summa"]
                expense_date = value["exp_date"]
                is_put_aside = value["is_put_aside"]
                if is_put_aside:
                    is_comp1 = "Да"
                else:
                    is_comp1 = "Нет"

                f.write(f"Название расхода: {expense_name} \n"
                        f"Сумма расхода: {summa}\n"
                        f"Дата: {expense_date} \n"
                        f"Является ли сумма отложенной: {is_comp1} \n"
                        f"________________________________________________________________________ \n")

        finally:
            f.close()
            print("Отчет создан")  # messagebox

    def sort_items(self):
        s_type = str(self.sortBox.currentText())
        self.get_expenses(type_of_sorting=s_type)

    def filter_items(self):
        f_type = str(self.filterBox.currentText())
        self.get_expenses(type_of_filter=f_type)

    def close_window(self):
        user_menu = UserMenu()
        widget.addWidget(user_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class EditExpenses(QDialog):
    def __init__(self):
        super(EditExpenses, self).__init__()
        loadUi("UI/editExpenses.ui", self)
        self.editNameBtn.clicked.connect(self.edit_name)
        self.editSumBtn.clicked.connect(self.edit_sum)
        self.editDateBtn.clicked.connect(self.edit_date)
        self.quitBtn.clicked.connect(self.close_window)

    def edit_name(self):
        global exp_name
        new_name = self.inputName.text()
        model = {"user_login": simple_user_login, "exp_name": exp_name, "new_name": new_name}
        res = client.edit_exp_name(model)
        exp_name = new_name

    def edit_sum(self):
        summa = self.inputSum.value()
        model = {"user_login": simple_user_login, "exp_name": exp_name, "summa": summa}
        res = client.edit_exp_sum(model)

    def edit_date(self):
        date = self.inputDate.date()
        date = date.toPyDate()
        model = {"user_login": simple_user_login, "exp_name": exp_name, "exp_date": date}
        res = client.edit_exp_date(model)


    def close_window(self):
        exp = ExpensesMenu()
        widget.addWidget(exp)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AddExpenses(QDialog):
    def __init__(self):
        super(AddExpenses, self).__init__()
        loadUi('UI/addExpenses.ui', self)
        self.addBtn.clicked.connect(self.add_item)
        self.saveMoneyBtn.clicked.connect(self.save_money)
        self.quitBtn.clicked.connect(self.close_window)
        self.get_list_of_aims()

    def get_list_of_aims(self):
        model = {"user_login": simple_user_login}
        list_of_aims = client.get_aims_to_put_aside(model)
        self.listOfAims.addItems(list_of_aims)

    def add_item(self):
        item = self.inputName.text()
        summa = self.inputSum.value()
        date = self.inputDate.date()
        date = date.toPyDate()
        f = False
        model = {"user_login": simple_user_login,
                 "exp_name": item,
                 "summa": summa,
                 "exp_date": date,
                 "is_put_aside": f}
        res = client.add_exp(model)

    def save_money(self):
        global aims_list_item
        aims_list_item = self.listOfAims.currentItem().text()
        summa = self.inputSum2.value()
        date = self.inputDate2.date()
        date = date.toPyDate()
        model = {"user_login": simple_user_login,
                 "aim_name": aims_list_item,
                 "put_aside": summa}
        res = client.put_aside(model)
        print(res.json())

        exp_model = {"user_login": simple_user_login,
                     "exp_name": aims_list_item,
                     "summa": summa,
                     "exp_date": date,
                     "is_put_aside": True}
        client.add_exp(exp_model)
        print("Добавлено")

    def close_window(self):
        exp_menu = ExpensesMenu()
        widget.addWidget(exp_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


class FeedBackUser(QDialog):
    def __init__(self):
        super(FeedBackUser, self).__init__()
        loadUi("UI/userFeedback.ui", self)
        self.quitBtn.clicked.connect(self.close_window)
        self.sendBtn.clicked.connect(self.send_feedback)

    def send_feedback(self):
        text = self.textEdit.toPlainText()
        mark = self.spinBox.value()
        model = {"user_login": simple_user_login,
                 "feedback": text,
                 "mark": mark}
        res = client.send_feedback(model)
        print(res.json())
        self.close_window()

    def close_window(self):
        menu = UserMenu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication([])

widget = QtWidgets.QStackedWidget()
main_window = MainWindow()
widget.addWidget(main_window)
