from flask import Flask, request
import logging
from flask_ngrok import run_with_ngrok

import json

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'start_game': False,
            'room': None,
            # HP, ARMOR, DAMAGE
            'hero': [100, 0, 5],
            'weapon': None,
            'first_text': True,
            'items': ["Зелье здоровья", "Кинжал", "Меч", "Доспехи"]
        }
        return

    if not sessionStorage[user_id]['start_game']:
        if sessionStorage[user_id]['first_name'] is None:
            # в последнем его сообщение ищем имя.
            first_name = get_first_name(req)
            # если не нашли, то сообщаем пользователю что не расслышали.
            if first_name is None:
                res['response']['text'] = \
                    'Не расслышала имя. Повтори, пожалуйста!'
                return
            # если нашли, то приветствуем пользователя.
            # И спрашиваем какой город он хочет увидеть.
            else:
                sessionStorage[user_id]['suggests'] = ["Нет", "Отстань", "Ладно", "Хорошо"]
                sessionStorage[user_id]['first_name'] = first_name
                res['response'][
                    'text'] = 'Приятно познакомиться, ' \
                              + first_name.title() \
                              + '. Я - Алиса. Хочешь сыграть в игру "Подземелья" ?'
            res['response']['buttons'] = get_suggests(user_id)
        else:
            if req['request']['original_utterance'].lower() in ['отстань', 'нет']:
                res['response']['text'] = 'Пока!'
                res['response']['end_session'] = True

            if req['request']['original_utterance'].lower() in ['ладно', 'хорошо']:
                sessionStorage[user_id]['start_game'] = True

    if sessionStorage[user_id]['start_game']:
        if sessionStorage[user_id]['first_text']:
            res['response']['text'] = "Вы вошли в тёмную комнату, дверь назад закрылась, остаётся идти только вперёд."
            sessionStorage[user_id]['suggests'] = ["Вперёд"]
            res['response']['buttons'] = get_suggests(user_id)
            sessionStorage[user_id]['first_text'] = False
            return
        if sessionStorage[user_id]['room'] is None and not sessionStorage[user_id]['first_text']:
            if req['request']['original_utterance'].lower() not in ['вперёд']:
                res['response']['text'] = 'Не поняла что вы сказали, повторите ещё раз.'
                sessionStorage[user_id]['suggests'] = ["Вперёд"]
                res['response']['buttons'] = get_suggests(user_id)
                return
            else:
                sessionStorage[user_id]['room'] = 1
        if sessionStorage[user_id]['room'] == 1:
            res['response']['text'] = 'Вы прошли в первую комнату.' \
                                      ' Перед вами 2 прохода, налево и направо, какой выбираете ?'

            return


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    return suggests


if __name__ == '__main__':
    app.run()
