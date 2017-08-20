import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib.layers import xavier_initializer
from Game import GameEnv


class DQN(object):
    """Deep Q Network"""
    def __init__(self):

        # placeholders
        self.x = tf.placeholder(tf.float32, [None, GameEnv.s_shape[0] * GameEnv.s_shape[1] * 3], 'x')
        self.x_reshaped = tf.reshape(self.x, [-1, GameEnv.s_shape[0], GameEnv.s_shape[1], 3])
        self.targetQ = tf.placeholder(tf.float32, [None], 'target')
        self.actions = tf.placeholder(tf.int32, [None], 'actions')

        # --- Q Network ---
        # First convolutional layer
        self.conv1 = slim.conv2d(inputs=self.x_reshaped, num_outputs=32, kernel_size=[5, 5], stride=[2, 2], padding='VALID',
                                 biases_initializer=None)

        # Second convolutional layer
        self.conv2 = slim.conv2d(inputs=self.conv1, num_outputs=64, kernel_size=[5, 5], stride=[2, 2], padding='VALID',
                                 biases_initializer=None)

        # Third convolutional layer
        self.conv3 = slim.conv2d(inputs=self.conv2, num_outputs=64, kernel_size=[5, 5], stride=[2, 2], padding='VALID',
                                 biases_initializer=None)

        # Forth convolutional layer
        self.conv4 = slim.conv2d(inputs=self.conv3, num_outputs=128, kernel_size=[5, 5], stride=[2, 2], padding='VALID',
                                 biases_initializer=None)

        # Flatten the output of convolutions
        self.flat = slim.flatten(self.conv4)

        # Output layer
        init = xavier_initializer()
        w = tf.Variable(init([1664, GameEnv.a_size]))

        self.q_vals = tf.matmul(self.flat, w)
        self.predict = tf.argmax(self.q_vals, axis=1)

        # Loss
        self.actions_one_hot = tf.one_hot(self.actions, GameEnv.a_size, dtype=tf.float32)
        self.Q = tf.reduce_sum(tf.multiply(self.q_vals, self.actions_one_hot), axis=1)

        self.loss = tf.reduce_mean(tf.square(self.Q - self.targetQ))

        # Optimizer
        self.train = tf.train.AdamOptimizer().minimize(self.loss)
