from flask_login import LoginManager
from flask_security import Security, login_user, SQLAlchemySessionUserDatastore, roles_accepted
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from models import StudentInStatement, User, Role
from models import LessonForm, Discipline
from models import LessonType
from models import Student, Lecturer, Group, Statement
from app_config import app, db
from flask import render_template, request, jsonify

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/personal", methods=['GET'])
def my_personal_info():

    return render_template('personal.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    # if the form is submitted
    if request.method == 'POST':
        # check if user already exists
        user = User.query.filter_by(email=request.form['email']).first()
        msg = ""
        # if user already exists render the msg
        if user and user.check_psw(request.form['psw']):
            msg = "User already exist"
            # render signup.html if user exists
            return render_template('signup.html', msg=msg)

        # if user doesn't exist

        # store the user to database
        user = User(email=request.form['email'], active=1, password=generate_password_hash(request.form['password']))
        # store the role
        role = Role.query.filter_by(id=request.form['options']).first()
        user.roles.append(role)

        # commit the changes to database
        db.session.add(user)
        db.session.commit()

        # login the user to the app
        # this user is current user
        login_user(user)
        # redirect to index page
        return redirect('/students')

    # case other than submitting form, like loading the page itself
    else:
        return render_template("signup.html", msg=msg)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if check_password_hash(user.password, request.form['password']):
                # if password matches, login the user
                login_user(user)
                return redirect('/students')
            # if password doesn't match
            else:
                msg = "Wrong password"

        # if user does not exist
        else:
            msg = "User doesn't exist"
        return render_template('signin.html', msg=msg)

    else:
        return render_template("signin.html", msg=msg)


@app.route("/students")
def get_students():
    rows = Student.query.order_by(Student.stud_id.asc()).all()
    # не знаю правильно ли так делать
    # закачиваю группы что выбирать только из тех которые есть
    groups = Group.query.order_by(Group.group_id.asc()).all()
    return render_template('students.html', rows=rows, groups=groups)


@app.route("/students/<int:stud_id>/delete", methods=['POST'])
def delete_student(stud_id):
    student = Student.query.get_or_404(stud_id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect("/students")
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/create-student", methods=["POST"])
def create_student():
    # form = CreateStudentForm()
    #
    # if form.validate_on_submit():
    #     student = Student(
    #         name=form.name.data,
    #         surname=form.surname.data,
    #         patronymic=form.patronymic.data,
    #         group_id=form.group_id.data,
    #         phone_number=form.phone_number.data,
    #         email=form.email.data,
    #         birthday=form.birthday.data,
    #         city=form.city.data,
    #     )
    #
    #     form.group_id.choices = [gr.group_id for gr in Group.query.all()]

        name = request.form.get("name")
        surname = request.form.get("surname")
        patronymic = request.form.get("patronymic")
        group_id = request.form.get("group_id")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        birthday = request.form.get("birthday")
        city = request.form.get("city")

        student = Student(name=name, surname=surname, patronymic=patronymic, group_id=group_id,
                           phone_number=phone_number, email=email, birthday=birthday, city=city)

        try:
            db.session.add(student)
            db.session.commit()
            return redirect("/students")

        except Exception as e:
            return jsonify({'error': str(e)}), 400




@app.route("/students/update/<int:stud_id>", methods=['POST'])
def student_update(stud_id):
    student = Student.query.get(stud_id)

    student.name = request.form['name']
    student.surname = request.form['surname']
    student.patronymic = request.form['patronymic']
    student.group_id = request.form['group_id']
    student.phone_number = request.form['phone_number']
    student.email = request.form['email']
    student.birthday = request.form['birthday']
    student.city = request.form['city']

    try:
        db.session.commit()
        return redirect("/students")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/lecturers")
def get_lecturers():
    rows = Lecturer.query.order_by(Lecturer.lecturer_id.asc()).all()
    return render_template('lecturers.html', rows=rows)


@app.route("/create-lect", methods=['POST'])
def create_lecturer():
    name = request.form.get("name")
    surname = request.form.get("surname")
    patronymic = request.form.get("patronymic")
    phone_number = request.form.get("phone_number")
    email = request.form.get("email")
    position = request.form.get("position")

    lecturer = Lecturer(name=name, surname=surname, patronymic=patronymic,
                        phone_number=phone_number, email=email, position=position)
    try:
        db.session.add(lecturer)
        db.session.commit()
        return redirect("/lecturers")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/lecturers/<int:lecturer_id>/delete", methods=['POST'])
def delete_lecturer(lecturer_id):
    lecturer = Lecturer.query.get_or_404(lecturer_id)
    try:
        db.session.delete(lecturer)
        db.session.commit()
        return redirect("/lecturers")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/lecturers/update/<int:lecturer_id>", methods=['POST'])
def lecturer_update(lecturer_id):
    lecturer = Lecturer.query.get_or_404(lecturer_id)

    lecturer.name = request.form['name']
    lecturer.surname = request.form['surname']
    lecturer.patronymic = request.form['patronymic']
    lecturer.phone_number = request.form['phone_number']
    lecturer.email = request.form['email']
    lecturer.position = request.form['position']

    try:
        db.session.commit()
        return redirect("/lecturers")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/statements")
def get_statements():
    statements = Statement.query.all()
    types = LessonType.query.all()
    forms = LessonForm.query.all()
    groups = Group.query.order_by(Group.group_id.asc()).all()
    disciplines = Discipline.query.all()
    return render_template('statements.html', statements=statements,
                           types=types, forms=forms, groups=groups, disciplines=disciplines)


@app.route("/create-statement", methods=["POST"])
def create_statement():
    group_id = request.form.get("group_id")
    date = request.form.get("date")
    discipline_id = request.form.get("discipline_id")
    lesson_type = request.form.get("lesson_type")
    lesson_form = request.form.get("lesson_form")
    print(group_id)
    print(date)
    print(discipline_id)
    print(lesson_type)
    print(lesson_form)

    students = Student.query.filter_by(group_id=group_id).all()
    students = sorted(students, key=lambda x: x.surname)
    discipline = Discipline.query.filter_by(discipline_id=discipline_id).all()
    statement = Statement(group_id=group_id, date=date, discipline_id=discipline_id, lesson_type=lesson_type,
                          lesson_form=lesson_form)
    print(statement)
    try:
        db.session.add(statement)
        db.session.commit()
        return render_template("stud-group.html", students=students, statement=statement,
                               discipline_name=discipline[0].name)

    except Exception as e:
        print("err")
        return jsonify({'error': str(e)}), 400


@app.route("/statements/<int:statement_id>/delete", methods=['POST'])
def delete_statement(statement_id):
    statement = Statement.query.get_or_404(statement_id)
    try:
        db.session.delete(statement)
        db.session.commit()
        return redirect("/statements")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/statements/update/<int:statement_id>", methods=['POST'])
def statement_update(statement_id):
    statement = Statement.query.get_or_404(statement_id)

    statement.group_id = request.form['group_id']
    statement.date = request.form['group_id']
    statement.discipline_id = request.form['discipline_id']
    statement.lesson_type = request.form['lesson_type']
    statement.lesson_form = request.form['lesson_form']

    try:
        db.session.commit()
        return redirect("/statements")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/create-statement/create-stud-lesson", methods=['POST', 'GET'])
def create_stud_lesson():
    data = request.get_json()
    print(data)
    try:
        # Перебираем отправленные данные и сохраняем их в базе
        for student in data:
            print(student)
            stud_id = student.get("stud_id")
            statement_id = student.get("statement_id")
            mark = student.get("mark")
            comment = student.get("comment")
            is_here = student.get("is_here")
            stud_in_statement = StudentInStatement(stud_id=stud_id, statement_id=statement_id, mark=mark,
                                                   comment=comment, is_here=is_here)
            db.session.add(stud_in_statement)

        db.session.commit()
        return redirect("/statements")

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/create-st', methods=['POST', 'GET'])
def create_st():
    form = CreateStudentForm()
    if request.method == 'POST':
        # Заполнение полей выбора ID группы из БД
        if form.validate_on_submit():
            new_student = Student(
                name=form.name.data,
                surname=form.surname.data,
                patronymic=form.patronymic.data,
                group_id=form.group_id.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
                birthday=form.birthday.data,
                city=form.city.data
            )

        return redirect('/students')  # Перенаправление на страницу успеха

    # Заполнение списка групп
    form.group_id.choices = [group.group_id for group in Group.query.all()]

    return render_template('create-st.html', form=form)


@app.route("/get-student/<int:student_id>")
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'name': student.name,
        'surname': student.surname,
        'patronymic': student.patronymic,
        'group_id': student.group_id,
        'phone_number': student.phone_number,
        'email': student.email,
        'birthday': student.birthday.isoformat(),  # Форматируем дату
        'city': student.city
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
