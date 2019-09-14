import random
from collections import namedtuple

import numpy as np
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.random import set_seed

set_seed(2)


Experience = namedtuple('Experience', ['state', 'action', 'reward'])


class ReplayBuffer(object):
    """
    ReplayBuffer used to store the different simulations in order to be able to accumulate enough experience,
    between agent learning steps. It has a limited capacity, overwriting the oldest values in case it requires to
    store new ones.
    """

    def __init__(self, capacity: int = 10000):
        """
        ReplayBuffer initializer
        :param capacity: indicates the ReplayBuffer capacity
        """
        self.data = [None for _ in range(capacity)]
        self.capacity = capacity
        self.saved_id = 0

    def add(self, state: np.ndarray, action: np.ndarray, reward: int):
        """
        Adds the new experience on the list, in case of not having enough memory, it overrides the older record
        :param state: initial passengers description
        :param action: order assigned to the queue of passengers
        :param reward: time elapsed till the boarding is fully completed
        """
        self.data[self.saved_id % self.capacity] = Experience(state=self.transform_queue(state),
                                                              action=action,
                                                              reward=reward)
        self.saved_id += 1

    def sample(self, num_experiences: int) -> (np.ndarray, np.ndarray, np.ndarray):
        """
        Samples random experiences in order to train the into the reinforcement learning agent
        :param num_experiences: number of experience we want to sample, without replacement
        :return: random states, actions and rewards from our ReplayBuffer
        """
        random_indexes = random.sample(population=range(self.capacity), k=num_experiences)

        states = np.array([self.data[random_index].state for random_index in random_indexes])
        actions = np.array([self.data[random_index].action for random_index in random_indexes])
        rewards = np.array([self.data[random_index].reward for random_index in random_indexes])

        return states, actions, rewards

    @staticmethod
    def transform_queue(queue: list) -> np.ndarray:
        """
        Given a passenger's queue in environment suited format, transform in into a more suitable neural network
        format
        :param queue: the passenger's queue to transform
        :return: the passenger's queue properly formatted
        """
        temp_structure = []
        for passenger in queue:
            temp_structure.append([passenger.seat[0],
                                   passenger.seat[1],
                                   passenger.baggage])

        return np.array(temp_structure)


class QAproximator(object):
    """ Action-value approximator based in neural networks """

    def __init__(self):
        self.network = None

    def generate_action_value(self, queue_shape: tuple, model_name='q_network'):
        """
        Generates the neural network structure to use as Q-approximator
        :param queue_shape: input shape of the state
        :param model_name: model of the neural network
        :return:
        """
        queue_input = keras.Input(shape=queue_shape, name='queue_input')
        queue_dense = layers.Dense(64, activation='relu', name='queue_dense')(queue_input)
        dense = layers.Dense(64, activation='relu', name='Dense_1')(queue_dense)
        dense = layers.Dense(32, activation='relu', name='Dense_2')(dense)
        outputs = layers.Dense(1, activation='softmax', name='Output')(dense)
        model = keras.Model(inputs=queue_input, outputs=outputs, name=model_name)

        self.network = model

    def learn(self, experiences: np.array):
        pass

    def predict(self) -> np.array:
        pass

    def copy_weights(self, network_to_copy: object):
        """
        Copy weights from a given Q, action-value approximator, to another
        :param network_to_copy: network which will be used as origin of the weights
        :return: None
        """
        self.network.set_weights(network_to_copy.get_weights())
