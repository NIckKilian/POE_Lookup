from tkinter import *
from PyQt5 import QtWidgets
from poeFrame import Ui_MainWindow
from PoeAPI import PoeAPI
import time, json,sys

second = 0
remaining = 0


class Poe_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.second = 20
        self.btnReady = True
        self.setRemaining(second)
        self.settings = {}
        self.accountResults = {}
        self.pAPI = PoeAPI()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupUIComponents()

    def setupUIComponents(self):
        self.getSettings()
        self.ui.pushButton.clicked.connect(lambda: self.poeSearch())
        if self.btnReady:
            self.ui.cmbCharList.currentTextChanged.connect(
                lambda: self.loadSelectedAcount(self.ui.cmbCharList.currentIndex()))
        self.show()

    def setRemaining(self, remaining):
        self.remaining = remaining

    def getRemaining(self):
        return self.remaining

    def poeSearch(self):
        self.btnReady = False
        self.ui.cmbCharList.clear()
        #Set the API Urls to use
        self.pAPI.loadAPISettings('Settings.txt')
        #get characters for the account
        self.accountResults = self.pAPI.requestAccount(self.ui.txtCharSearch.text())
        #fill combo box dropdown with all the characters under the account
        if self.accountResults != '1':
            for keys in self.accountResults:
                comboString = keys['name'] + '  ' + str(keys['level']) + '   ' + keys['league']
                self.ui.cmbCharList.addItem(comboString)
                self.btnReady = True
        else:
            self.ui.txtCharSearch.setText("No Account Found")

    def loadSelectedAcount(self, indexSelected):
        if self.btnReady:
            keys = {}
            keys = self.accountResults[indexSelected]
            #link to POE profile page
            urlLink = self.settings['profileURL'] + self.ui.txtCharSearch.text() + '/characters">' + \
                      keys['name'] + '</a>'
            # Load labels with  selected charactername
            self.ui.lblNAME.setOpenExternalLinks(True)
            self.ui.lblNAME.setText(urlLink)
            self.ui.lblLevel.setText('LVL ' + str(keys['level']))
            self.ui.lblLeague.setText(keys['league'])
            self.ui.lblClass.setText(keys['class'])
            self.ui.lblXP.setText('EXP: ' + str(keys['experience']))
            self.getLadderInfoForChar(keys['league'], keys['name'])
            self.setSettings()

    def getLadderInfoForChar(self, league, name):
        # LadderInfo For Character
        ladderJSON = ''
        ladderJSON = self.pAPI.requestLadder(league, name)
        self.ui.lblLadder.setText(ladderJSON)
        # TODO have a timer countdown and refresh the character data
        # self.poe_startTimer()

    def poe_startTimer(self):
        if self.remaining > 0:
            print(self.remaining)
            self.setRemaining(self.remaining - 1)
            time.sleep(1)
            self.poe_startTimer()
            print(self.remaining)
        elif self.remaining == 0:
            self.setRemaining(self.second)
            list_index = self.ui.cmbCharList.currentIndex()
            self.poeSearch()
            self.loadSelectedAcount(list_index)

    def getSettings(self):
        # load restlink.txt to get the rest url
        with open('settings.txt') as file:
            self.settings = json.load(file)
        file.close()
        self.ui.txtCharSearch.setText(self.settings['LastSearched'])

    def setSettings(self):
        # load restlink.txt to get the rest url
        self.settings['LastSearched'] = self.ui.txtCharSearch.text()
        with open('settings.txt', 'w') as file:
            json.dump(self.settings, file, sort_keys=True, indent=4,
                      ensure_ascii=False)
        file.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Poe_UI()
    sys.exit(app.exec_())
