from collections import deque
import random
import numpy as np


class ExperienceBuffer(object):
    """RL Agent's experience buffer"""
    def __init__(self, buffer_size):

        self._buffer_size = buffer_size
        self._buffer = deque(maxlen=buffer_size)

    def add(self, experience):
        """Add new experience"""
        if len(self._buffer) + len(experience) > self._buffer_size:
            self._popN(len(self._buffer)+len(experience)-self._buffer_size)

        self._buffer.extend(experience)

    def batch(self, batch_size):
        """Sample experience"""
        return np.reshape(np.array(random.sample(self._buffer, batch_size)), [batch_size, 5])

    def _popN(self, n):
        """Pop n oldest experiences from buffer"""
        for _ in range(n):
            self._buffer.popleft()
