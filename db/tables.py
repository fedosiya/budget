from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, JSON, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    user_login = Column(String(100), unique=True)
    user_password = Column(String(100), unique=True)
    is_admin = Column(Boolean)
    is_blocked = Column(Boolean)


class Expense(Base):
    __tablename__ = 'expenses'

    exp_id = Column(Integer, primary_key=True, server_default=text("nextval('expences_exp_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    exp_name = Column(String(20))
    summa = Column(Float)
    exp_date = Column(Date)
    is_put_aside = Column(Boolean)

    user = relationship('User')


class Feedback(Base):
    __tablename__ = 'feedback'

    feedb_id = Column(Integer, primary_key=True, server_default=text("nextval('feedback_feedb_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    feedback = Column(Text)
    appresial = Column(Integer)
    user_login = Column(String(30))

    user = relationship('User')


class Financeaim(Base):
    __tablename__ = 'financeaim'

    aim_id = Column(Integer, primary_key=True, server_default=text("nextval('financeaim_aim_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    aim_name = Column(String(30))
    start_date = Column(Date)
    end_date = Column(Date)
    summa = Column(Float)
    is_completed = Column(Boolean)
    put_aside = Column(Float)

    user = relationship('User')


class Income(Base):
    __tablename__ = 'incomes'

    income_id = Column(Integer, primary_key=True, server_default=text("nextval('incomes_income_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    inc_name = Column(String(20))
    summa = Column(Float)
    inc_date = Column(Date)
    is_const = Column(Boolean)

    user = relationship('User')


class Report(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True, server_default=text("nextval('reports_report_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    incomes_report = Column(Text)
    expences_report = Column(Text)
    incomes_diagran_data = Column(JSON)
    expenses_diagram_data = Column(JSON)

    user = relationship('User')

