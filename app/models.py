from distutils.command.check import check

from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app_config import db

# класс студент

class Student(db.Model):
    __tablename__= 'student'
    stud_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    patronymic = db.Column(db.String(60), nullable=True, default="-")
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20))

# сущность преподаватель

class Lecturer(db.Model):
    __tablename__ = 'lecturer'
    lecturer_id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    patronymic = db.Column(db.String(60), nullable=True, default='-')
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(20), nullable=False)

# сущность дисциплина

class Discipline(db.Model):
    __tablename__ = 'discipline'
    discipline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.lecturer_id'))
    number_of_hours = db.Column(db.Integer, default="-")

# сущность ведомость

class Statement(db.Model):
    __tablename__ = 'statement'
    statement_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    date = db.Column(db.Date, nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.discipline_id'))
    lesson_type = db.Column(db.String(70))
    lesson_form = db.Column(db.String(70))

# сущность расписание

class Schedule(db.Model):
    __tablename__ = 'schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.discipline_id'))

# сущность группа

class Group(db.Model):
    __tablename__ = "group"
    group_id = db.Column(db.Integer, primary_key=True)
    group_number = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('lecturer.lecturer_id'))
    course = db.Column(db.Integer, nullable=False)


class LessonForm(db.Model):
    __tablename__ = "lesson-form"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(70), nullable=False)

class LessonType(db.Model):
    __tablename__ = "lesson-type"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(70), nullable=False)

class StudentInStatement(db.Model):
    __tablename__ = "student_in_statement"
    id = db.Column(db.Integer, primary_key=True)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.stud_id"))
    statement_id = db.Column(db.Integer, db.ForeignKey('statement.statement_id'))
    mark = db.Column(db.Integer)
    comment = db.Column(db.String(60))
    is_here = db.Column(db.Boolean)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# create table in database for storing users
class User(db.Model, UserMixin):
    tablename = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    # backreferences the user_id from roles_users table
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    fs_uniquifier = db.Column(db.String(255), unique=True)

    def set_psw(self, psw):
        self.password = generate_password_hash(psw)

    def check_psw(self, psw):
        return check_password_hash(self.password, psw)

# create table in database for storing roles
class Role(db.Model, RoleMixin):
    tablename = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)