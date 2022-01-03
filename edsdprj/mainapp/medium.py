from random import seed, randint, randrange
from sys import maxsize


class Medium:
    default_accuracy = 0.5

    def __init__(self, options=None):
        if options:
            self._options = options
        else:
            opt = {
                'id': Medium.get_random_for_seed(),
                'accuracy': [],
                'history': []
            }
            self._options = opt

    @property
    def last_accuracy(self):
        return self._options['accuracy'][-1] if len(self._options['accuracy']) > 0 else Medium.default_accuracy

    @staticmethod
    def get_random_for_seed():
        seed()  # use now()
        return randrange(maxsize)

    def get_options(self):
        return self._options

    def get_divination(self):
        seed(Medium.get_random_for_seed())
        rndm = randint(10, 99)
        self._options['history'].append(rndm)
        self._options['accuracy'].append(self.last_accuracy)  # добавляем точность
        return rndm

    def refresh_accuracy(self, user_answer):
        if self._options['history'][-1] != user_answer:
        # # сделал поблажку, а то совсем не прет ребятам =)
        # if abs(self._options['history'][-1] - user_answer) > 20:
            self._options['accuracy'][-1] = round(self.last_accuracy - 0.01, 2)
        else:
            self._options['accuracy'][-1] = round(self.last_accuracy + 0.01, 2)

    def __repr__(self):
        return f'{self.__class__} {self._options}'
