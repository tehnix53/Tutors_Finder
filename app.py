from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired

import random

from data import teachers
from create_json import dict_to_json, unpack_json, \
    update_json, database_initialize
from teacher_day_name import teach_workday


def random_six():
    a = []
    i = 0
    while i < 6:
        b = (random.randint(0, 11))
        if b not in a:
            a += [b]
            i += 1
    return a


class MyForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired(message="Введите свое имя")])
    phone = StringField('Ваш телефон', [InputRequired(message="Введите свой телефон!")])
    this_day = StringField([InputRequired()])


class RequestForm(FlaskForm):
    target = RadioField(choices=[('✈ Для путешествий', '✈ Для путешествий'), ("🏫 Для школы", "🏫 Для школы"),
                                 ("⚒ Для работы", "⚒ Для работы"), ("🚃 Для переезда", "🚃 Для переезда"),
                                 ('💻 для программирования', '💻 для программирования')])
    time = RadioField(choices=[('1-2 часа в неделю', '1-2 часа/нед.'), ("3-5 часов в неделю", "3-5 часов/нед."),
                               ("5-7 часов в неделю", "5-7 часов/нед."), ("7-10 часов в неделю", "7-10 часов/нед.")])
    name = StringField(InputRequired())
    phone = StringField(InputRequired())


app = Flask(__name__)
app.secret_key = "randomstring"

goals_dict = {'relocate': "✈ для переезда", "travel": "🚗 для путешествий", 'work': "⚒ для работы",
              'study': "🏫 для учёбы", 'programing': "💻 для программирования"}


dict_to_json(teachers, "database.json")
teach_list = unpack_json('database.json')
empty_list = []
database_initialize(empty_list)


@app.route('/test')
def testing_test():
    return render_template('test.html')


@app.route('/')
def teach_main():
    return render_template('index.html', number=random_six(), teach_list=teach_list, goals_dict=goals_dict)


@app.route('/all/')
def teach_all():
    return render_template('all.html', teach_list=teach_list, goals_dict=goals_dict)


@app.route('/goals/<goal>/')
def teach_goals(goal):
    return render_template("goal.html", goal=goal, teach_list=teach_list, goals_dict=goals_dict)


@app.route('/profiles/<id>/')
def teach_himself(id):
    return render_template('profile.html', teach_list=teach_list, id=id, teach_workday=teach_workday,
                           goals_dict=goals_dict)


@app.route('/request/')
def teach_request():
    form = RequestForm()

    return render_template('request.html', name=form.name, time=form.time,
                           target=form.target, phone=form.phone)


@app.route("/booking/<id>/<day>/<time>/")
def teach_booking(id, day, time):
    form = MyForm()
    return render_template('booking.html', id=id, teach_list=teach_list,
                           day=day, time=time, name=form.name, phone=form.phone,
                           this_day=form.this_day)


@app.route('/request_done/', methods=["POST"])
def request_success():
    form = RequestForm()
    name = form.name.data
    phone = form.phone.data
    time = form.time.data
    target = form.target.data
    update_json({'name': name, 'phone': phone, 'target': target, 'time': time}, 'request.json')
    return render_template('request_done.html', name=name, phone=phone, time=time, target=target)


@app.route("/booking_done/<day>/<time>/", methods=["POST"])
def teach_booking_done(day, time):
    form = MyForm()
    name = form.name.data
    phone = form.phone.data
    update_json({'name': name, 'phone': phone, 'day': day, 'time': time}, 'booking.json')
    return render_template('booking_done.html', name=name, phone=phone,
                           day=day, time=time)


# app.run('127.0.0.1', 8000, debug=True)

if __name__ == '__main__':
    app.run()
