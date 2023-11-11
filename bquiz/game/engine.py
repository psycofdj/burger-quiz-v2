from PySide6 import QtCore, QtWidgets, QtMultimedia

import vlc
import time

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
        self.backgroundPlayer = self.vlc.media_list_player_new()
        self.buzzerPlayer = self.vlc.media_player_new()
        self.samplePlayer = self.vlc.media_player_new()
        self.samplePlayer.audio_set_volume(100)
        self.buzzerPlayer.audio_set_volume(100)

        self.current = None
        self.buzzing = False
        self.state = State.TOSS
        self.mainWindow = widget

        hw.resetBtn.longPressed.connect(self.reset)
        hw.nuggetsBtn.pressed.connect(self.startNuggets)
        hw.selpoivreBtn.pressed.connect(self.startSelPoivre)
        hw.menusBtn.pressed.connect(self.startMenus)
        hw.additionBtn.pressed.connect(self.startAddition)
        hw.mayoBuzz.pressed.connect(self.mayoBuzz)
        hw.ketchupBuzz.pressed.connect(self.ketchupBuzz)
        hw.sample1Btn.pressed.connect(self.sample1)
        hw.sample2Btn.pressed.connect(self.sample2)
        hw.sample3Btn.pressed.connect(self.sample3)
        hw.sample4Btn.pressed.connect(self.sample4)
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
            State.TOSS.name: Toss,
            State.NUGGETS.name: Nuggets,
            State.SELPOIVRE.name: SelPoivre,
            State.MENUS.name: Menus,
            State.ADDITION.name: Addition,
        }
        handler = l[state.name]
        new = handler(self.hw, self.mainWindow)
        if self.current != None:
            new.clone(self.current)
            self.current.frame.hide()
            self.current.finalize()
        self.current = new
        self.current.frame.show()

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


    def playBackground(self, name):
        filepath = self.current.resourcePath(name)
        media = self.vlc.media_new(filepath)
        media_list = self.vlc.media_list_new()
        media_list.add_media(media)
        self.backgroundPlayer.set_media_list(media_list)
        self.backgroundPlayer.set_playback_mode(vlc.PlaybackMode.loop)
        self.backgroundPlayer.play()

    @buzzlock
    @QtCore.Slot()
    def mayoBuzz(self):
        if self.state not in [ State.NUGGETS, State.MENUS ]:
            self.hw.mayoRelay.on()
            self.hw.mayoLED.blink(seconds=3)
            self.playSound2("buzz-mayo.mp3")

    @buzzlock
    @QtCore.Slot()
    def ketchupBuzz(self):
        if self.state not in [ State.NUGGETS, State.MENUS ]:
            self.hw.ketchupRelay.on()
            self.hw.ketchupLED.blink(seconds=3)
            self.playSound2("buzz-ketchup.mp3")

    @QtCore.Slot()
    def reset(self):
        self.current.reset()
        self.startToss()

    def startToss(self):
        self.setState(State.TOSS)
        self.playSound("intro.mp3")
        self.playBackground("silence.mp3")

    @QtCore.Slot()
    def startNuggets(self):
        if self.state != State.TOSS:
            return self.current.ephemeralError(self.errorNotNow(State.NUGGETS))
        if not self.current.leader:
            return self.current.ephemeralError("Quelle équipe à la main ?")
        self.setState(State.NUGGETS)
        self.playSound("nuggets.mp3")

    @QtCore.Slot()
    def startSelPoivre(self):
        if self.state != State.NUGGETS:
            return self.current.ephemeralError(self.errorNotNow(State.SELPOIVRE))
        self.setState(State.SELPOIVRE)
        self.playSound("sel-ou-poivre.mp3")

    @QtCore.Slot()
    def startMenus(self):
        if self.state != State.SELPOIVRE:
            return self.current.ephemeralError(self.errorNotNow(State.MENUS))
        self.setState(State.MENUS)
        self.playSound("menus.mp3")

    @QtCore.Slot()
    def startAddition(self):
        if self.state != State.MENUS:
            return self.current.ephemeralError(self.errorNotNow(State.ADDITION))
        self.setState(State.ADDITION)
        self.playSound("addition.mp3")

    @QtCore.Slot()
    def sample1(self):
        self.playSound("arrete.mp3")
    @QtCore.Slot()
    def sample2(self):
        self.playSound("fermez.mp3")
    @QtCore.Slot()
    def sample3(self):
        self.playSound("con.mp3")
    @QtCore.Slot()
    def sample4(self):
        self.playSound("doigts.mp3")
