import pyautogui


class MouseController:
    def __init__(self, sensation_multiplier=1):
        self.screen_width, self.screen_height = pyautogui.size()
        self.mouse = pyautogui
        self.mouse.FAILSAFE = False
        self.sensation_multiplier = sensation_multiplier
        self.is_button_down = False

    def move_mouse(self, x, y):
        scaled_x = x * self.sensation_multiplier - self.screen_width / 1.33
        scaled_y = y * self.sensation_multiplier - self.screen_height * 1.65
        self.mouse.moveTo(scaled_x, scaled_y)

    def click_down(self):
        if not self.is_button_down:
            self.mouse.mouseDown()
            self.is_button_down = True

    def click_up(self):
        if self.is_button_down:
            self.mouse.mouseUp()
            self.is_button_down = False
