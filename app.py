from flask import Flask, render_template, url_for
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from random import random, shuffle
import operator

app = Flask(__name__)
app.config['SECRET_KEY'] = "X_secret-file!"


class FormFilter(FlaskForm):
    filter_list = SelectField('filter_teacher', choices=[('in_rand_order', 'В случайном порядке'),
                                                         ('the_best_rating', 'Сначала лучшие по рейтингу'),
                                                         ('high_price', 'Сначала дорогие'),
                                                         ('low_price', 'Сначала недорогие')])
    submit = SubmitField("Отфильтровать")


def get_date():
    """
    Получаем данные из JSON файла
    :return: возвращаем массив с данными
    """
    with open('data.JSON', 'r', encoding='UTF-8') as data_base:
        all_data = json.load(data_base)
    return all_data


# главной / – здесь будет главная
@app.route('/')
@app.route('/index')
def index():
    all_data = get_date()
    return render_template('index.html', teacher_info=all_data)


# все преподаватели /all - здесь будут преподаватели
@app.route('/all/', methods=['POST', 'GET'])
def get_all():
    all_data = get_date()  # Обработка данных из БД
    form_filter = FormFilter()
    option_filter = form_filter.filter_list.data
    if option_filter == 'in_rand_order':
        shuffle(all_data)
    elif option_filter == 'the_best_rating':
        all_data.sort(key=operator.itemgetter('rating'), reverse=True)
    elif option_filter == 'high_price':
        all_data.sort(key=operator.itemgetter('price'), reverse=True)
    elif option_filter == 'high_price':
        all_data.sort(key=operator.itemgetter('price'))
    else:
        return render_template('all.html', teacher_info=all_data, form=form_filter, option_filter=option_filter)

    return render_template('all.html', teacher_info=all_data, form=form_filter, option_filter=option_filter)

# цели /goals/<goal>/  – здесь будет цель <goal>
@app.route('/goals/<goal>/')
def goals():
    return "здесь будет цель <goal>"


# профиля учителя /profiles/<id учителя>/ – здесь будет преподаватель <id учителя>
@app.route('/profiles/<id_teacher>/')  # id учителя
def profiles():
    return "здесь будет преподаватель <id учителя>"


# заявки на подбор /request/ – здесь будет заявка на подбор
@app.route('/request/')
def request():
    return "здесь будет заявка на подбор"


# принятой заявки на подбор /request_done/ – заявка на подбор отправлена
@app.route('/request_done/')
def request_done():
    return "заявка на подбор отправлена"


# формы бронирования /booking/<id учителя>/<день недели>/<время>/ – здесь будет форма бронирования <id учителя>
@app.route('/booking/<id_teacher>/<day>/<time>/')
def booking():
    return "здесь будет форма бронирования <id учителя>"


# принятой заявки на подбор /booking_done/   – заявка отправлена
app.route('/booking_done/')


def booking_done():
    return 'заявка отправлена'


if __name__ == '__main__':
    app.run(debug=True)
