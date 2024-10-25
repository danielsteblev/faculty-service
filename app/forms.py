from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email



class CreateStudentForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired(), Length(max=50)])
    surname = StringField("Фамилия: ", validators=[DataRequired(), Length(max=50)])
    patronymic = StringField("Отчество: ", validators=[Length(max=50)])
    group_id = SelectField("ID группы: ", validators=[DataRequired()])
    phone_number = StringField("Номер телефона: ", validators=[DataRequired(), Length(max=15)] )
    email = EmailField("Email: ", validators=[DataRequired(), Email()])
    birthday = DateField("Дата рождения: ", format='%d-%m-%Y', validators=[DataRequired()])
    city = StringField("Город: ", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Создать студента')


class RegistrationForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    role = SelectField('Роль: ', validators=[DataRequired()])
    submit = SubmitField("Войти")
