class ScreenManager:

    __activeScreen = None
    __screens = []

    @staticmethod
    def isShown(screen):
        if ScreenManager.__activeScreen != None:
            ScreenManager.__activeScreen.hide()
            ScreenManager.__screens.append(ScreenManager.__activeScreen)

        ScreenManager.__activeScreen = screen

    @staticmethod
    def pop():
        return ScreenManager.__screens.pop()

    @staticmethod
    def back():
        if ScreenManager.__activeScreen != None:
            ScreenManager.__activeScreen = None
        previous_screen = ScreenManager.pop()
        print(previous_screen)
        previous_screen.show()