from .views import MEDIUMS_KEY, USER_ANSWER_HISTORY_KEY


def set_context_data(request):
    mediums_data = request.session.get(MEDIUMS_KEY)
    user_answers_history = request.session.get(USER_ANSWER_HISTORY_KEY)

    if mediums_data and len(mediums_data) > 0:
        mediums_ids = tuple(v['id'] for v in mediums_data)
        table_data = [[] for _ in range(len(mediums_data[0]['history']))]  # пустой список в размерность кол-ва строк

        # собираем строки для таблицы данных:
        # O - ответ, Т - точность, Э - экстрасенс, П - пользователь
        #
        # О1 П, (<Э1> О1, Т1), (<Э2> О1, Т1), ...
        # О2 П, (<Э1> О2, Т2), (<Э2> О2, Т2), ...
        # О3 П, (<Э1> О3, Т3), (<Э2> О3, Т3), ...
        # О2 П, (О2 Э1, Т2 Э1), (О2 Э2, Т2 Э2), ...
        #
        # для начала собираем (<Э1>[О1, О2, ...], [Т1, т2, ...]), (<Э2>[О1, О2, ...], [Т1, т2, ...]), ...
        for x in zip((v['history'] for v in mediums_data), (v['accuracy'] for v in mediums_data)):
            # для каждого Э(x) собираем <Э1>(О1, Т1), <Э1>(О2, Т2), ...
            for i, y in enumerate(((hist, acc) for hist, acc in zip(x[0], x[1]))):
                # расширяем нужную строчку:
                # [(<Э1> О1, Т1),
                #  (<Э1> О2, Т2),
                #  ...
                # ]
                #
                # -> (новые данные появятся при следующем x)
                #
                # [[(<Э1> О1, Т1), (<Э2> О1, Т1)],
                #  [(<Э1> О2, Т2), (<Э2> О2, Т2)],
                #  ...
                # ]
                table_data[i].append(y)
        # смешиваем строчки с ответами пользователя
        table_data = zip(user_answers_history, table_data)

        return {
            'mediums_ids': mediums_ids,
            'table_data': table_data
        }
