from PIL import ImageGrab
import numpy as np
from pykeyboard import PyKeyboard
import time
from selenium import webdriver
# import matplotlib.pyplot as plt


class GameEnv(object):
    """T-Rex Game Environment"""
    a_size = 3
    s_shape = [64, 256, 3]

    def __init__(self):

        self._keyboard = PyKeyboard()

        self._browser = webdriver.Chrome()
        self._browser.set_window_size(600, 650)
        self._browser.set_window_position(0, 0)
        self._browser.get('chrome://dino')

        self._bbox = [40, 350, 1160, 650]

        self._actions = {0: self._stand,
                         1: self._jump,
                         2: self._duck}

    def reset(self, wait=True, refresh=True):
        """Reset game"""
        if wait:
            print '10 seconds before start, focus tab with game!'
            time.sleep(10)

        if refresh:
            self._browser.refresh()

        s = self._screen()
        self._jump()
        return np.reshape(s, [64*256*3]), 1.0, False

    def step(self, action):
        """Perform action and get new state"""
        self._actions[action]()
        s = self._screen()

        game_over = self._game_over(s)

        return (np.reshape(s, [64*256*3]), 0.0, True) if game_over else (np.reshape(s, [64*256*3]), 1.0, False)

    def exit(self):
        self._browser.quit()

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
        img = img.resize((256, 64))
        # self.testSight(img)
        img = np.array(img)[:, :, :3]
        img = img / 255.0

        return img

    def _game_over(self, s):
        """Check game over state"""
        end = [v*255.0 for v in s[31:44, 122, 0]]

        if 247.0 in end:
            return False
        return True

    def testSight(self, img):
        # plt.imsave('test.png', np.array(img))
        pass

if __name__ == '__main__':

    env = GameEnv()
    _, _, d = env.reset(wait=True, refresh=False)
    t = time.time()
    while not d:
        a = np.random.randint(0, 3, [1])[0]
        _, _, d = env.step(a)
        print 'Action:', a

    env.exit()
    print 'Game duration:', time.time() - t, 's'
