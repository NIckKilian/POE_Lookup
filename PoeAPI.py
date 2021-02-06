import json, sys
import requests

from PyQt5 import QtWidgets


class PoeAPI():
    def __init__(self):
        self.settings = {}

    def loadAPISettings(self, settings):
        # load restlink.txt to get the rest url
        with open(settings) as file:
            self.settings = json.load(file)
        file.close()

    def requestAccount(self, accountName):
        self.params = {
            'accountName': accountName
        }
        headers = {'user-agent': 'Mozilla/5.0'}
        requestURL = self.settings['characterURL']
        req = requests.get(requestURL, headers=headers, params=self.params)
        if req.ok:
            return req.json()
        else:
            return '1'

    def requestLadder(self, league, name):
        ladder = {}
        headers = {'user-agent': 'Mozilla/5.0'}
        LadderRequestURL = self.settings['ladderURL'] + league
        print(LadderRequestURL)
        req = requests.get(LadderRequestURL, headers=headers)
        ladder = req.json()
        if req.ok:
            userfound = False;
            userRank = ''
            for key in ladder['entries']:
                user = key['character']
                if name == user['name']:
                    userfound = True
                    userRank = str(key['rank'])
                    break
            if userfound:
                print('Ranked')
                return 'Rank ' + userRank
            else:
                return 'Not Ranked'
        else:
            return 'No Ladder'

    def returnAccountName(self):
        return self.settings['characterURL']
