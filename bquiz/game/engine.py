from PySide6 import QtCore, QtWidgets, QtMultimedia

import vlc

from bquiz.types import State
from bquiz.game.toss import Toss
from bquiz.game.nuggets import Nuggets
from bquiz.game.selpoivre import SelPoivre
from bquiz.game.menus import Menus
from bquiz.game.addition import Addition

class Engine(QtCore.QObject):

    def __init__(self, hw, widget = None):
        super().__init__(widget)

        self.vlc = vlc.Instance("--no-xlib")
        self.buzzerPlayer = self.vlc.media_player_new()
        self.buzzerPlayer.audio_set_volume(100)
        self.buzzerPlayer.audio_output_device_enum()
        self.samplePlayer = self.vlc.media_player_new()
        self.samplePlayer.audio_set_volume(100)
        self.samplePlayer.audio_output_device_enum()

        self.buzzing = False
        self.state = State.TOSS
        self.mainWindow = widget
        self.toss = Toss(hw, self.mainWindow)
        self.nuggets = Nuggets(hw, self.mainWindow)
        self.selpoivre = SelPoivre(hw, self.mainWindow)
        self.menus = Menus(hw, self.mainWindow)
        self.addition = Addition(hw, self.mainWindow)

        hw.resetBtn.longPressed.connect(self.reset)
        hw.nuggetsBtn.pressed.connect(self.startNuggets)
        hw.selpoivreBtn.pressed.connect(self.startSelPoivre)
        hw.menusBtn.pressed.connect(self.startMenus)
        hw.additionBtn.pressed.connect(self.startAddition)
        hw.mayoBuzz.pressed.connect(self.mayoBuzz)
        hw.ketchupBuzz.pressed.connect(self.ketchupBuzz)
        self.hw = hw
        self.startToss()

    def errorNotNow(self, newState):
        if newState.value < self.state.value:
            return "L'épreuve %s est déjà terminée !" % newState.name
        elif newState.value == self.state.value:
            return "L'épreuve %s est déjà en cours !" % newState.name
        else:
            return "L'épreuve %s n'est pas tout de suite !" % newState.name

    def setState(self, state):
        self.state = state
        l = {
            State.TOSS.name: self.toss,
            State.NUGGETS.name: self.nuggets,
            State.SELPOIVRE.name: self.selpoivre,
            State.MENUS.name: self.menus,
            State.ADDITION.name: self.addition,
        }
        [ obj.frame.show() for name,obj in l.items() if name == self.state.name ]
        [ obj.frame.hide() for name,obj in l.items() if name != self.state.name ]
        self.current = getattr(self, state.name.lower())


    def stopLock(self):
        self.hw.mayoRelay.off()
        self.hw.ketchupRelay.off()
        self.buzzing = False

    def buzzlock(fn):
        def wrapper(self, *args, **kwargs):
            if not self.buzzing:
                self.buzzing = True
                self.timer = QtCore.QTimer.singleShot(3000, self.stopLock)
                fn(self, *args, **kwargs)
        return wrapper

    def playSound(self, name):
        filepath = self.current.resourcePath(name)
        self.samplePlayer.set_media(self.vlc.media_new(filepath))
        self.samplePlayer.play()

    def playSound2(self, name):
        filepath = self.current.resourcePath(name)
        self.buzzerPlayer.set_media(self.vlc.media_new(filepath))
        self.buzzerPlayer.play()

    @buzzlock
    @QtCore.Slot()
    def mayoBuzz(self):
        if self.state not in [ State.NUGGETS, State.MENUS ]:
            self.hw.mayoLED.blink(seconds=3)
            self.hw.mayoRelay.on()
            self.playSound2("buzz-mayo.mp3")

    @buzzlock
    @QtCore.Slot()
    def ketchupBuzz(self):
        if self.state not in [ State.NUGGETS, State.MENUS ]:
        self.hw.ketchupLED.blink(seconds=3)
        self.hw.ketchupRelay.on()
        self.playSound2("buzz-ketchup.mp3")

    @QtCore.Slot()
    def reset(self):
        self.toss.reset()
        self.nuggets.reset()
        self.menus.reset()
        self.addition.reset()
        self.startToss()

    def startToss(self):
        self.setState(State.TOSS)

    @QtCore.Slot()
    def startNuggets(self):
        if self.state != State.TOSS:
            return self.current.ephemeralError(self.errorNotNow(State.NUGGETS))
        if not self.toss.leader:
            return self.current.ephemeralError("Quelle équipe à la main ?")
        self.nuggets.clone(self.toss)
        self.setState(State.NUGGETS)
        self.playSound("nuggets.mp3")


    @QtCore.Slot()
    def startSelPoivre(self):
        if self.state != State.NUGGETS:
            return self.current.ephemeralError(self.errorNotNow(State.SELPOIVRE))
        self.selpoivre.clone(self.nuggets)
        self.setState(State.SELPOIVRE)
        self.playSound("sel-ou-poivre.mp3")

    @QtCore.Slot()
    def startMenus(self):
        if self.state != State.SELPOIVRE:
            return self.current.ephemeralError(self.errorNotNow(State.MENUS))
        self.menus.clone(self.selpoivre)
        self.setState(State.MENUS)
        self.playSound("menus.mp3")

    @QtCore.Slot()
    def startAddition(self):
        if self.state != State.MENUS:
            return self.current.ephemeralError(self.errorNotNow(State.ADDITION))
        self.addition.clone(self.menus)
        self.setState(State.ADDITION)
        self.playSound("addition.mp3")
