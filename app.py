import pandas as pd
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import pandas as pd
import main
import random
app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False
users = pd.read_csv('src/users.csv', encoding='utf-8')
tarif = pd.read_csv('src/tarif.csv')


@app.route('/user/<int:id>', methods=['GET'])
def user(id):
    for step in users.to_dict('records'):
        if step['id'] == id:
            return step
    return 'Такого пользователя нет'

@app.route('/users/all', methods=['GET'])
def get_users():
    a = dict()
    a['all_users'] = users.to_dict('record')
    return a

@app.route('/user/<int:id>', methods=['POST'])
def add_user(id):
    global users
    parser = reqparse.RequestParser()
    parser.add_argument("id")
    parser.add_argument("Активный тариф")
    parser.add_argument("Возраст")
    parser.add_argument("Временная метка последней активности")
    parser.add_argument("Город проживания")
    parser.add_argument("Дата добавления")
    parser.add_argument("Текущий баланс")
    params = parser.parse_args()

    for quote in users.to_dict('records'):
        if (id == quote["id"]):
            return f"User with id {id} already exists", 400

    new_user = {
            "id": int(id),
            "Активный тариф": params["Активный тариф"],
            "Возраст": params["Возраст"],
            "Временная метка последней активности": params["Временная метка последней активности"],
            "Город проживания": params["Город проживания"],
            "Дата добавления": params["Дата добавления"],
            "Текущий баланс": params["Текущий баланс"]
      }

    add_users = pd.DataFrame([new_user])
    users = pd.concat([users, add_users], axis = 0)
    a = dict()
    a['new_users'] = new_user
    return a, 201


@app.route('/user/<int:id>', methods=['DELETE'])
def del_user(id):
    global users
    for step in users.to_dict('records'):
        if step["id"] == id:
            users = users[users['id'] != id]
            return f"User with id {id} is deleted.", 200

    return f"User with id {id} does not exist", 400


@app.route('/user/<int:id>', methods=['PUT'])
def put_user(id):
    global users
    parser = reqparse.RequestParser()
    parser.add_argument("id")
    parser.add_argument("Активный тариф")
    parser.add_argument("Возраст")
    parser.add_argument("Временная метка последней активности")
    parser.add_argument("Город проживания")
    parser.add_argument("Дата добавления")
    parser.add_argument("Текущий баланс")
    params = parser.parse_args()

    for step in users.to_dict('records'):
        if step["id"] == id:
            users = users[users['id'] != id]
            new_user = {
                "id": int(id),
                "Активный тариф": params["Активный тариф"],
                "Возраст": params["Возраст"],
                "Временная метка последней активности": params["Временная метка последней активности"],
                "Город проживания": params["Город проживания"],
                "Дата добавления": params["Дата добавления"],
                "Текущий баланс": params["Текущий баланс"]
            }

            add_user = pd.DataFrame([new_user])
            users = pd.concat([users, add_user], axis=0).sort_values(by='id')
            a = dict()
            name = f'User_with_id_{id}_is_update'
            a[name] = new_user
            return a, 201

    return f"User with id {id} does not exist", 400


if __name__ == '__main__':
    app.run(debug=True)