from random import seed, randint, randrange
from sys import maxsize
import json


class Medium:
    default_accuracy = 0.5

    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            dct = {'class': str(obj.__class__)}
            dct.update(obj.get_params())
            return dct

    def json_dumps(self):
        return json.dumps(self, cls=Medium.JSONEncoder)

    @staticmethod
    def json_loads(json_string):
        def as_medium(dct):
            if str(Medium) == dct.get('class'):
                return Medium(**dct)

        return json.loads(json_string, object_hook=as_medium)

    @staticmethod
    def get_random_for_seed():
        seed()  # use now()
        return randrange(maxsize)

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', Medium.get_random_for_seed())
        self._credibility = kwargs.get('credibility', [])
        self._history = kwargs.get('history', [])

    @property
    def id(self):
        return self._id

    @property
    def credibility(self):
        return self._credibility

    @property
    def history(self):
        return self._history

    @property
    def last_accuracy(self):
        return self._credibility[-1] if len(self._credibility) > 0 else Medium.default_accuracy

    def get_params(self):
        return {k[1:]: v for k, v in self.__dict__.items()}

    def get_divination(self):
        seed(Medium.get_random_for_seed())
        rndm = randint(10, 99)
        self._history.append(rndm)
        self._credibility.append(self.last_accuracy)  # добавляем точность
        return rndm

    def refresh_accuracy(self, user_answer):
        if self._history[-1] != user_answer:
            self._credibility[-1] = round(self.last_accuracy - 0.01, 2)
        else:
            self._credibility[-1] = round(self.last_accuracy + 0.01, 2)

    def __repr__(self):
        return f'{self.__class__} {self.__dict__}'
