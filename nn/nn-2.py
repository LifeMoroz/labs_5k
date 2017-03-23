import math
import random


class Neuron:
    def __init__(self):
        self.value = None

    def activate(self, value):
        pass


class InputNeuron(Neuron):
    NORMALIZE_VALUE = 0

    def activate(self, value):  # Lazy normalization
        self.value = value / self.NORMALIZE_VALUE


class OutputNeuron(Neuron):
    pass


class HiddenNeuron(Neuron):
    def activate(self, values):
        return math.tanh(sum(values)/len(values))


class Layer:
    AUTO_INCREMENT = 0
    NEURONS = {}
    LINKS = {}
    REVERSE_LINKS = {}

    @classmethod
    def __inc(cls):
        try:
            return cls.AUTO_INCREMENT
        finally:  # cheat :)
            cls.AUTO_INCREMENT += 1

    @classmethod
    def get_neuron(cls, id):
        return cls.NEURONS[id]

    @classmethod
    def register(cls, neuron):
        _id = cls.__inc()
        cls.NEURONS[_id] = neuron
        return _id

    @classmethod
    def subscribe(cls, sender, receiver):
        cls.LINKS.setdefault(sender, [])
        init_weight = random.random()
        cls.LINKS[sender].append((receiver, init_weight))
        cls.REVERSE_LINKS.setdefault(receiver, [])
        cls.REVERSE_LINKS[receiver].append((sender, init_weight))

    def __init__(self, _class, count):
        self.neurons = []
        for _ in range(count):
            self.neurons.append(self.register(_class()))

    def activate(self, values):
        tmp = {}
        for i, n_id in enumerate(self.neurons):
            tmp[n_id] = self.get_neuron(n_id).activate(values[i])

        for i, item in enumerate(self.REVERSE_LINKS.items()):
            receiver, senders = item
            values = [tmp[s] for s in senders]
            Layer.get_neuron(receiver).activate(values)



class Web:
    def __init__(self, n_input, n_hidden, n_output):
        self.il = Layer(InputNeuron, n_input)
        self.hl = Layer(HiddenNeuron, n_hidden)
        self.ol = Layer(OutputNeuron, n_output)

    def put(self, values):
        self.il.activate(values)

if __name__ == '__main__':
    size = (10, 10)
    width, height = size
    web = Web(width * height, height, 10)
    # Строим архитектуру
    for i, n_id in enumerate(web.il.neurons):
        Layer.subscribe(n_id, web.hl.neurons[i % height])


print(1)
