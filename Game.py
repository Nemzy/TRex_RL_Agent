from PIL import ImageGrab
import numpy as np
from pykeyboard import PyKeyboard
import time


class GameEnv(object):
    """T-Rex Game Environment"""
    a_size = 3
    s_shape = [64, 128, 3]

    def __init__(self, screen_width):

        self._keyboard = PyKeyboard()

        x = (screen_width-1200)/2
        self._bbox = [x, 265, x+1200, 565]

        self._actions = {0: self._stand,
                         1: self._jump,
                         2: self._duck}

    def reset(self, wait=True):
        """Reset game"""
        if wait:
            print '10 seconds before start.\nOpen game tab in full screen mode!'
            time.sleep(10)

        s = self._screen()
        self._jump()
        return np.reshape(s, [128*64*3]), 1.0, False

    def step(self, action):
        """Perform action and get new state"""
        self._actions[action]()
        s = self._screen()

        game_over = self._game_over(s)

        return (np.reshape(s, [128*64*3]), 0.0, True) if game_over else (np.reshape(s, [128*64*3]), 1.0, False)

    def _jump(self):
        """Jump"""
        self._keyboard.tap_key(' ')

    def _duck(self):
        """Duck"""
        self._keyboard.press_key('Down')

    def _stand(self):
        """Stand"""
        self._keyboard.release_key('Down')

    def _screen(self):
        """Capture game screen"""
        img = ImageGrab.grab(bbox=self._bbox)
        img = img.resize((128, 64))
        img = np.array(img)[:, :, :3]
        img = img / 255.0

        return img

    def _game_over(self, s):
        """Check game over state"""
        end = [v*255.0 for v in s[33:45, 61, 0]]

        if 247.0 in end:
            return False
        return True

if __name__ == '__main__':

    env = GameEnv(2560)
    _, _, d = env.reset()
    t = time.time()
    while not d:
        a = np.random.randint(0, 3, [1])[0]
        _, _, d = env.step(a)
        print 'Action:', a

    print 'Game duration:', time.time() - t, 's'
