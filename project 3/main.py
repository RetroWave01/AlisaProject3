from flask import Flask, request
import logging
from flask_ngrok import run_with_ngrok
from random import choice

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
    print(sessionStorage[request.json['session']['user_id']]['room'])

    logging.info('Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        sessionStorage[user_id] = {
            'first_name': None,
            'start_game': False,
            'room': None,
            'win': False,
            'per': None,
            'end_chest': ['Золото', 'Вирус'],
            'chance': ["да", "нет", "нет", "нет"],
            'lose': False,
            'random_text': ["Сундук", "Ловушка"],
            # HP, ARMOR, DAMAGE
            'hero': [100, 0, 20],
            'weapon': None,
            'one': True,
            # HP, DAMAGE
            'enemys': ["Призрак", "Паук", "Чёрный рыцарь", "Элементаль", "Маг", "Скелет", "Зомби"],
            'Призрак': [45, 20],
            'Паук': [60, 15],
            'Чёрный рыцарь': [40, 35],
            'Элементаль': [25, 25],
            'Маг': [45, 30],
            'Скелет': [22, 15],
            'Зомби': [70, 10],
            'enemy': None,
            'chest': False,
            'enemy_hp': None,
            'enemy_attack': None,
            'first_text': True,
            'items': ["Зелье здоровья", "Кинжал", "Зелье защиты", "Ядовитые споры"],
            '1': False, '2': False, '3': False, '4': False, '5': False, '6': False, '7': False,
            '8': False, '9': False, '10': False, '11': False, '12': False, '13': False, '14': False, '15': False,
            '16': False, '17': False, '18': False, '19': False, '20': False, '21': False,
        }
        return

    if not sessionStorage[user_id]['start_game']:
        hello(user_id, res, req)
    if sessionStorage[user_id]['start_game']:
        first_text(user_id, res, req)
        if sessionStorage[user_id]['room'] == 1:
            first_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 2:
            second_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 3:
            third_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 4:
            fourth_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 5:
            five_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 6:
            six_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 7:
            seven_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 8:
            eight_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 9:
            nine_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 10:
            ten_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 11:
            eleven_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 12:
            twelve_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 13:
            thirteen_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 14:
            fourteen_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 15:
            fifteen_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 16:
            sixteen_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 17:
            seventeen_level(user_id, res, req)
        if sessionStorage[user_id]['room'] == 18:
            eighteen_level(user_id, res, req)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def item_from_chest(user_id, res):
    item = choice(sessionStorage[user_id]['items'])
    if item == 'Зелье здоровья':
        sessionStorage[user_id]['hero'][0] += 75
        res['response']['text'] = 'Вы открыли сундук и нашли' + ' ' + item + '.' + 'Теперь у вас ' + '' \
                                  + str(sessionStorage[user_id]['hero'][0]) + ' здоровья'
    if item == 'Зелье защиты':
        sessionStorage[user_id]['hero'][1] += 5
        res['response']['text'] = 'Вы открыли сундук и нашли' + ' ' + item + '.' + 'Теперь у вас ' + '' \
                                  + str(sessionStorage[user_id]['hero'][1]) + ' брони'
    if item == 'Кинжал':
        sessionStorage[user_id]['hero'][2] += 15
        res['response']['text'] = 'Вы открыли сундук и нашли' + ' ' + item + '.' + 'Теперь у вас ' + '' \
                                  + str(sessionStorage[user_id]['hero'][2]) + ' урона'
    if item == 'Ядовитые споры':
        sessionStorage[user_id]['hero'][0] -= 20
        if sessionStorage[user_id]['hero'][0] <= 0:
            res['response']['text'] = 'Вы открыли сундук, и почувствовали что что-то не так, она так и оказалось - ' + \
                                      'вы вдохнули ядовитые споры' + ' и теперь у вас' \
                                      + ' 0 здоровья и вы погибли.'
            res['response']['end_session'] = True
            return
        else:
            res['response']['text'] = 'Вы открыли сундук и почувствовали что что-то не так, она так и оказалось,' + \
                                      'вы вдохнули ядовитые споры' + \
                                      ' и теперь у вас ' + str(sessionStorage[user_id]['hero'][0]) + ' здоровья'
            sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
            res['response']['buttons'] = get_suggests(user_id)


def enemy_fight(user_id, res, enemy, req):
    res['response']['text'] = "Вы вошли в комнату, как перед вами появилось существо " + \
                              "'" + enemy + "'" + " у него " + str(sessionStorage[user_id][enemy][0]) + \
                              " Здоровья." + " У вас " + str(sessionStorage[user_id]['hero'][0]) + \
                              " Здоровья и " + \
                              str(sessionStorage[user_id]['hero'][2]) + " Урона. Что хотите сделать" \
                                                                        " - Атаковать или попытаться сбежать ?"
    sessionStorage[user_id]['suggests'] = ["Атаковать", "Попытаться уйти"]
    res['response']['buttons'] = get_suggests(user_id)
    if req['request']['original_utterance'].lower() in ['попытаться уйти']:
        if choice(sessionStorage[user_id]['chance']) == 'да':
            sessionStorage[user_id]['per'] = True
            res['response']['text'] = "У вас получилось убежать от врага!"
        else:
            sessionStorage[user_id]['hero'][0] = sessionStorage[user_id]['hero'][0] \
                                                 - sessionStorage[user_id][enemy][1] - \
                                                 sessionStorage[user_id]['hero'][1]
            res['response']['text'] = 'У вас не получилось сбежать, теперь у вас ' + \
                                      str(sessionStorage[user_id]['hero'][0]) + ' здоровья'
            if sessionStorage[user_id]['hero'][0] <= 0:
                res['response']['text'] = 'Вы погибли.'
                res['response']['end_session'] = True
                return
    elif req['request']['original_utterance'].lower() in ['атаковать']:
        sessionStorage[user_id]['hero'][0] = sessionStorage[user_id]['hero'][0] \
                                             - (sessionStorage[user_id][enemy][1] -
                                                sessionStorage[user_id]['hero'][1])
        sessionStorage[user_id][enemy][0] = sessionStorage[user_id][enemy][0] - sessionStorage[user_id]['hero'][2]
        if sessionStorage[user_id]['hero'][0] <= 0 and sessionStorage[user_id][enemy][0] <= 0:
            res['response']['text'] = "Вы ударили существо" + " '" + enemy + "' " + "теперь у него " + \
                                      str(sessionStorage[user_id][enemy][0]) + " здоровья"
            sessionStorage[user_id]['hero'][0] = sessionStorage[user_id]['hero'][0] + \
                                                 (
                                                         sessionStorage[user_id][enemy][1] -
                                                         sessionStorage[user_id]['hero'][1]
                                                 )
            sessionStorage[user_id]['per'] = True
        elif sessionStorage[user_id][enemy][0] > 0:
            res['response']['text'] = "Вы ударили существо" + " '" + enemy + "' " + "теперь у него " + \
                                      str(sessionStorage[user_id][enemy][0]) + \
                                      " здоровья. В ответ он ударил вас, теперь у вас " + \
                                      str(sessionStorage[user_id]['hero'][0]) + " здоровья."
            if sessionStorage[user_id]['hero'][0] <= 0:
                res['response']['text'] = 'Вы погибли.'
                res['response']['end_session'] = True
                return
        if sessionStorage[user_id][enemy][0] <= 0:
            sessionStorage[user_id]['per'] = True


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    return suggests


def hello(user_id, res, req):
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


def first_text(user_id, res, req):
    if sessionStorage[user_id]['first_text']:
        res['response']['text'] = "Вы вошли в подземелья в поисках приключений, дверь за вами захлопнулась" \
                                  ", остаётся идти только вперёд. " \
                                  "Правила просты: вы выбираете в какую из" \
                                  " сторон вам пойти, при этом после выбора вы уже" \
                                  " никак не можете выйти назад, ведь дверь за вами постоянно закрывается."
        sessionStorage[user_id]['suggests'] = ["Вперёд"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['first_text'] = False
        return
    if sessionStorage[user_id]['room'] is None and not sessionStorage[user_id]['first_text']:
        if req['request']['original_utterance'].lower() not in ['вперёд']:
            res['response']['text'] = 'Не поняла что вы сказали, повторите ещё раз.'
            return
        else:
            sessionStorage[user_id]['room'] = 1


def first_level(user_id, res, req):
    if not sessionStorage[user_id]['1']:
        res['response']['text'] = 'Вы прошли в первую комнату.' \
                                  ' Перед вами 2 прохода, налево и направо, какой выбираете ?'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['1'] = True
        return
    if req['request']['original_utterance'].lower() in ['налево']:
        sessionStorage[user_id]['room'] = 2
    if req['request']['original_utterance'].lower() in ['направо']:
        sessionStorage[user_id]['room'] = 3
    if sessionStorage[user_id]['room'] == 1:
        res['response']['text'] = 'Я вас не расслышала повторите снова'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def second_level(user_id, res, req):
    if not sessionStorage[user_id]['2']:
        res['response']['text'] = 'Вы решили пойти налево, перед вами сундук и два прохода.' \
                                  'Что хотите сделать - пойти налево, направо или открыть сундук?'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо", "Открыть сундук"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['2'] = True
        return
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        item_from_chest(user_id, res)
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['налево']:
        sessionStorage[user_id]['room'] = 4
    if req['request']['original_utterance'].lower() in ['направо']:
        sessionStorage[user_id]['room'] = 5
    if sessionStorage[user_id]['room'] == 2:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def third_level(user_id, res, req):
    if not sessionStorage[user_id]['3']:
        res['response']['text'] = 'Вы решили пойти направо, перед вами сундук и два прохода.' \
                                  'Что хотите сделать - пойти налево, направо или открыть сундук?'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо", "Открыть сундук"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['3'] = True
        return
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        item_from_chest(user_id, res)
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['налево']:
        sessionStorage[user_id]['room'] = 6
    if req['request']['original_utterance'].lower() in ['направо']:
        sessionStorage[user_id]['room'] = 7
    if sessionStorage[user_id]['room'] == 3:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def fourth_level(user_id, res, req):
    if not sessionStorage[user_id]['4']:
        res['response']['text'] = 'Вы прошли в комнату с цифрой 4.' \
                                  ' Перед вами 3 прохода, налево, прямо и направо, какой выбираете ?'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо", "Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['4'] = True
        return
    if req['request']['original_utterance'].lower() in ['налево']:
        res['response']['text'] = '8'
        sessionStorage[user_id]['room'] = 8
    if req['request']['original_utterance'].lower() in ['направо']:
        res['response']['text'] = '10'
        sessionStorage[user_id]['room'] = 10
    if req['request']['original_utterance'].lower() in ['прямо']:
        res['response']['text'] = '9'
        sessionStorage[user_id]['room'] = 9
    if sessionStorage[user_id]['room'] == 4:
        res['response']['text'] = 'Я вас не расслышала повторите снова'
        sessionStorage[user_id]['suggests'] = ["Налево", "Направо", "Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def five_level(user_id, res, req):
    if not sessionStorage[user_id]['5']:
        res['response']['text'] = 'Вы прошли в заросшую лианами комнату. Под лианами вы видите сундук.' \
                                  ' Так же перед вами 3 прохода, что хотите сделать - открыть сундук,' \
                                  ' пойти направо, пойти налево, пойти прямо'
        sessionStorage[user_id]['suggests'] = ["Налево", "Прямо", "Направо", "Открыть сундук"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['5'] = True
        return
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        item_from_chest(user_id, res)
        sessionStorage[user_id]['suggests'] = ["Налево", "Прямо", "Направо"]
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['налево']:
        res['response']['text'] = '10'
        sessionStorage[user_id]['room'] = 10
    if req['request']['original_utterance'].lower() in ['направо']:
        res['response']['text'] = '12'
        sessionStorage[user_id]['room'] = 12
    if req['request']['original_utterance'].lower() in ['прямо']:
        res['response']['text'] = '11'
        sessionStorage[user_id]['room'] = 11
    if sessionStorage[user_id]['room'] == 5:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        return


def six_level(user_id, res, req):
    if not sessionStorage[user_id]['6']:
        res['response']['text'] = 'Вы вошли в комнату с номеров 6' \
                                  ' Перед вами 2 прохода, вверх и вниз какой выбираете ?'
        sessionStorage[user_id]['suggests'] = ["Вниз", "Вверх"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['6'] = True
        return
    if req['request']['original_utterance'].lower() in ['вверх']:
        res['response']['text'] = '13'
        sessionStorage[user_id]['room'] = 13
    if req['request']['original_utterance'].lower() in ['вниз']:
        res['response']['text'] = '14'
        sessionStorage[user_id]['room'] = 14
    if sessionStorage[user_id]['room'] == 6:
        res['response']['text'] = 'Я вас не расслышала повторите снова'
        sessionStorage[user_id]['suggests'] = ["Вниз", "Вверх"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def seven_level(user_id, res, req):
    if not sessionStorage[user_id]['7']:
        res['response']['text'] = 'Вы прошли в комнату с водопадом из стены, вы что-то увидели в воде.' \
                                  ' Перед вами 2 прохода, что хотите сделать - пройти налево,' \
                                  ' пройти направо или открыть сундук?'
        sessionStorage[user_id]['suggests'] = ["Налево", "Вверх", "Открыть сундук"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['7'] = True
        return
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        item_from_chest(user_id, res)
        sessionStorage[user_id]['suggests'] = ["Налево", "Вверх"]
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['вверх']:
        res['response']['text'] = '14'
        sessionStorage[user_id]['room'] = 14
    if req['request']['original_utterance'].lower() in ['налево']:
        res['response']['text'] = '13'
        sessionStorage[user_id]['room'] = 13
    if sessionStorage[user_id]['room'] == 7:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        sessionStorage[user_id]['suggests'] = ["Налево", "Вверх"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def eight_level(user_id, res, req):
    if not sessionStorage[user_id]['8']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['8'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['per'] = False
        sessionStorage[user_id]['room'] = 15


def nine_level(user_id, res, req):
    if not sessionStorage[user_id]['9']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['9'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['per'] = False
        sessionStorage[user_id]['room'] = 15


def ten_level(user_id, res, req):
    if not sessionStorage[user_id]['10']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['10'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['per'] = False
        sessionStorage[user_id]['room'] = 15


def eleven_level(user_id, res, req):
    if not sessionStorage[user_id]['11']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['11'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['per'] = False
        sessionStorage[user_id]['room'] = 16


def twelve_level(user_id, res, req):
    if not sessionStorage[user_id]['12']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['12'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['per'] = False
        sessionStorage[user_id]['room'] = 16


def thirteen_level(user_id, res, req):
    if not sessionStorage[user_id]['13']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['13'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['room'] = 17


def fourteen_level(user_id, res, req):
    if not sessionStorage[user_id]['14']:
        sessionStorage[user_id]['enemy'] = choice(sessionStorage[user_id]['enemys'])
        sessionStorage[user_id]['enemys'].remove(sessionStorage[user_id]['enemy'])
        sessionStorage[user_id]['14'] = True
    enemy_fight(user_id, res, sessionStorage[user_id]['enemy'], req)
    if sessionStorage[user_id]['per']:
        sessionStorage[user_id]['room'] = 17


def fifteen_level(user_id, res, req):
    res['response']['text'] = "Вы вошли в комнату и увидели громадный сундук на полу" \
                              " и замочную скважину в стене, остаётся только открыть сундук."
    sessionStorage[user_id]['suggests'] = ["Открыть сундук"]
    res['response']['buttons'] = get_suggests(user_id)
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        if choice(sessionStorage[user_id]['end_chest']) == 'Вирус':
            res['response']['text'] = "К своему сожалению открыв сундук вы лишь выпустили из него вирус, от" \
                                      " которого вы станете монстром и будете вечно ходить по этим лабиринтам."
            res['response']['end_session'] = True
            return
        if choice(sessionStorage[user_id]['end_chest']) == 'Золото':
            res['response']['text'] = "Вы нашли в сундуке золото и ключ," \
                                      " просунув ключ в скажину открылся" \
                                      " потойной проход из подземелья, через который вы вышли из него богатым."
        if sessionStorage[user_id]['room'] == 16:
            res['response']['text'] = 'Я вас не расслышала повторите снова'
            sessionStorage[user_id]['suggests'] = ["Прямо"]
            res['response']['buttons'] = get_suggests(user_id)
            return


def sixteen_level(user_id, res, req):
    if not sessionStorage[user_id]['16']:
        res['response']['text'] = 'Вы уже видите выход из подземелья, осталось пройти лишь один коридор.'
        sessionStorage[user_id]['suggests'] = ["Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['16'] = True
        return
    if req['request']['original_utterance'].lower() in ['прямо']:
        if sessionStorage[user_id]['hero'][0] - 50 > 0:
            res['response']['text'] = 'Вы всё таки пошли по коридору,' \
                                      ' как из стен полетели стрелы, вас изрядно' \
                                      ' потрепало но вы выбралиь из подземелья живым.'
            res['response']['end_session'] = True
            return
        else:
            res['response']['text'] = 'Вы решили пойти по коридору, как вдруг' \
                                      ' из стен в вас полетели стрелы, к' \
                                      ' сожалению вы так и не смогли выбраться из подземелья.'
            res['response']['end_session'] = True
            return
    if sessionStorage[user_id]['room'] == 16:
        res['response']['text'] = 'Я вас не расслышала повторите снова'
        sessionStorage[user_id]['suggests'] = ["Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def seventeen_level(user_id, res, req):
    if not sessionStorage[user_id]['17']:
        res['response']['text'] = 'Вы прошли в семнадцатаю комнату.' \
                                  ' Перед собой вы видите только одиноко стоячий сундук и проход,' \
                                  ' вы можете пройти прямо, либо открыть сундук.'
        sessionStorage[user_id]['suggests'] = ["Прямо", "Открыть сундук"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['17'] = True
        return
    if req['request']['original_utterance'].lower() in ['открыть сундук']:
        if sessionStorage[user_id]['hero'][0] - 45 > 0:
            sessionStorage[user_id]['hero'][0] = sessionStorage[user_id]['hero'][0] - 45
            res['response']['text'] = 'Вы открыли сундук, но это оказался мимик, теперь у вас' \
                                      + str(sessionStorage[user_id]['hero'][0]) + ' здоровья.'
            sessionStorage[user_id]['suggests'] = ["Прямо"]
            res['response']['buttons'] = get_suggests(user_id)
            return
        else:
            res['response']['text'] = 'Вы погибли.'
            res['response']['end_session'] = True
            return

    if req['request']['original_utterance'].lower() in ['прямо']:
        res['response']['text'] = '18'
        sessionStorage[user_id]['room'] = 18
    if sessionStorage[user_id]['room'] == 17:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        sessionStorage[user_id]['suggests'] = ["Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


def eighteen_level(user_id, res, req):
    if not sessionStorage[user_id]['18']:
        res['response']['text'] = 'Как только вы прошли в 18 комнату, открылся люк в потолке и комнату' \
                                  ' начала наполнять вода,дверь перед вами закрылась,' \
                                  ' вы увидели кнопки на стене - вы можете нажать' \
                                  ' на "Первую", "Вторую", "Третью", "Четвёртую", "Пятую" и  "Шестую" кнопку.'
        sessionStorage[user_id]['suggests'] = ["Первую", "Вторую", "Третью", "Четвёртую", "Пятую", "Шестую"]
        res['response']['buttons'] = get_suggests(user_id)
        sessionStorage[user_id]['18'] = True
        return
    if req['request']['original_utterance'].lower() in ['четвёртую']:
        res['response']['text'] = 'Люк закрылся и вода убывает, путь свободен и вы смогли выйти из подземелья.'
        res['response']['end_session'] = True
        return
    if req['request']['original_utterance'].lower() not in ['четвёртую']:
        res['response']['text'] = 'К сожалению вы выбрали не правильную кнопку и вас затопило.'
        res['response']['end_session'] = True
        return
    if sessionStorage[user_id]['room'] == 18:
        res['response']['text'] = 'Я вас не расслышала повторите снова.'
        sessionStorage[user_id]['suggests'] = ["Прямо"]
        res['response']['buttons'] = get_suggests(user_id)
        return


if __name__ == '__main__':
    app.run()
