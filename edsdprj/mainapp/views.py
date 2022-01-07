from operator import methodcaller

from django.views.generic import TemplateView

from .forms import AnswerForm
from .medium import Medium
from .mixins import GetMediumsContextMixin

MEDIUMS_KEY = 'mediums'
USER_ANSWER_HISTORY_KEY = 'user_answers_history'


class MainView(TemplateView):
    template_name = 'mainapp/index.html'

    def dispatch(self, request, *args, **kwargs):
        print('MAIN VIEW dispatch')
        if not request.session or not request.session.session_key:
            request.session.save()
            request.session.setdefault(MEDIUMS_KEY,
                                       [Medium().json_dumps() for _ in range(3)])  # сделаем три экстрасенса
            request.session.setdefault(USER_ANSWER_HISTORY_KEY, [])
        return super().dispatch(request, *args, **kwargs)


class GuessView(GetMediumsContextMixin, TemplateView):
    template_name = 'mainapp/guesses.html'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST and 'answer' in self.request.POST:
            form = AnswerForm(self.request.POST)
            form.is_valid()
        else:
            form = AnswerForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # вспоминаем данные из сессии
        mediums = [Medium.json_loads(opt) for opt in request.session.get(MEDIUMS_KEY)]
        user_answers_history = request.session.get(USER_ANSWER_HISTORY_KEY)
        if 'guess' in request.POST:  # кнопка ЗАГАДАЛ
            for medium in mediums:
                medium.get_divination()
            user_answers_history.append('Нет ответа')
        elif 'answer' in request.POST:
            user_answers_history[-1] = context['form'].cleaned_data['user_answer']
            for medium in mediums:
                medium.refresh_accuracy(user_answers_history[-1])

        # сохраняем данные в сессию
        request.session[MEDIUMS_KEY] = [medium.json_dumps() for medium in mediums]
        request.session[USER_ANSWER_HISTORY_KEY] = user_answers_history

        # готовим данные для вывода на странице
        context.update(self.get_mediums_context(mediums, user_answers_history))
        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)
