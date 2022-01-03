from django.shortcuts import render
from random import random, seed

from django.utils.timezone import now
from django.views.generic import TemplateView, FormView

from .forms import MainForm
from .medium import Medium

MEDIUMS_KEY = 'mediums'
USER_ANSWER_HISTORY_KEY = 'user_answers_history'


class MainView(TemplateView):
    template_name = 'mainapp/index.html'
    form_class = MainForm

    @staticmethod
    def prepare_context_data(mediums, user_answer_history):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            if 'answer' in self.request.POST:
                form = MainForm(self.request.POST)
                form.is_valid()
            else:
                form = MainForm()
        else:
            form = MainForm()
        context['form'] = form
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.session or not request.session.session_key:
            request.session.save()
            request.session.setdefault(MEDIUMS_KEY, [Medium().get_options() for _ in range(3)])  # сделаем три экстрасенса
            request.session.setdefault(USER_ANSWER_HISTORY_KEY, [])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Вообще создание объектов тут избыточно.
        # Я бы хранил созданные объекты где-нить в отдельном потоке
        # и обращался к ним по каким-нибудь ИД (раз уже просят хранить в сессии);
        # чтобы не плодились много - дропать их вместе с сессией или по таймеру.
        # Но с многопоточностью у меня мало опыта + там тоже свои нюансы,
        # поэтому чтоб не плодить откровенно плохой код - так.
        #
        # Если еще упрощать, то хватило бы словаря (для хранения истории предсказаний, точности и сида)
        # и отдельной функции получения предсказания по рандом.сиду,
        # но раз просят через ООП - вот и гоняю объекты туда-сюда.

        # вспоминаем данные из сессии
        mediums = [Medium(opt) for opt in request.session.get(MEDIUMS_KEY)]
        user_answers_history = request.session.get(USER_ANSWER_HISTORY_KEY)
        # инфа начнет отображаться криво, если несколько раз нажать на ЗАГАДАЛ.
        # для исправления можно user_answers_history заполнять None (я так сделал),
        # либо отключать кнопку ЗАГАДАЛ, пока не узнаем результаты экстрасенсов (кнопка ОТВЕТ)
        #
        # та же история с ОТВЕТом. Если несколько раз подряд нажимать - будет менять последнее значение.
        # Исправить можно также: отключать кнопки по очереди.
        #
        # Если следовать по шагам ТЗ, то проблем нет.
        if 'guess' in request.POST:  # кнопка ЗАГАДАЛ
            for medium in mediums:
                medium.get_divination()
            user_answers_history.append(None)
        elif 'answer' in request.POST:
            user_answers_history[-1] = context['form'].cleaned_data['user_answer']
            for medium in mediums:
                medium.refresh_accuracy(user_answers_history[-1])

        # сохраняем данные в сессию
        request.session[MEDIUMS_KEY] = [medium.get_options() for medium in mediums]
        request.session[USER_ANSWER_HISTORY_KEY] = user_answers_history

        # готовим данные для вывода на странице

        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)
