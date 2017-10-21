'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
from threading import Timer, Thread

global K
global L
global P
global B
global J
global F
global K_P
K = 0
L = 0
P = 0
B = 0
J = 0
F = 0
K_P = 0

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, updateEmotes):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.updateEmotes = updateEmotes

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == 'K':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'appa':
                print('Received command: K' + cmd)
                self.updateEmotes('Kappa')
            #self.do_command(e, cmd)
        elif e.arguments[0][:1] == 'L':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'UL':
                print('Recieved command: L' + cmd)
                self.updateEmotes('LUL')

        elif e.arguments[0][:1] == 'P':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'ogChamp':
                print('Recieved command: P' + cmd)
                self.updateEmotes('PogChamp')

        elif e.arguments[0][:1] == 'B':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'lessRNG':
                print('Recieved command: B' + cmd)
                self.updateEmotes('BlessRNG')

        elif e.arguments[0][:1] == 'J':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'ebaited':
                print('Recieved command: J' + cmd)
                self.updateEmotes('Jebaited')

        elif e.arguments[0][:1] == 'F':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'rankerZ':
                print('Recieved command: F' + cmd)
                self.updateEmotes('FrankerZ')

        elif e.arguments[0][:1] == 'K':
            cmd = e.arguments[0].split(' ')[0][1:]
            if cmd == 'appaPride':
                print('Recieved command: K' + cmd)
                self.updateEmotes('KappaPride')
        return


def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username = sys.argv[1]
    client_id = sys.argv[2]
    token = sys.argv[3]
    channel = sys.argv[4]

    emotes = {}

    def updateEmotes(emote):
        if emote == 'Kappa':
            global K
            K = K+1
        elif emote == 'LUL':
            global L
            L = L+1
        elif emote == 'PogChamp':
            global P
            P = P+1
        elif emote == 'BlessRNG':
            global B
            B = B+1
        elif emote == 'Jebaited':
            global J
            J = J+1
        elif emote == 'FrankerZ':
            global F
            F = F+1
        elif emote == 'KappaPride':
            global K_P
            K_P = K_P+1



    def printEmotes():
        global K
        print(K)
        K = 0

        global L
        print(L)
        L = 0

        global P
        print(P)
        P = 0

        global B
        print(B)
        B = 0

        global J
        print(J)
        J = 0

        global F
        print(F)
        F = 0

        global K_P
        print(K_P)
        K_P = 0

        interval = Timer(30, printEmotes)
        interval.start()
    #while loop goes here

    printEmotes()
    bot = TwitchBot(username, client_id, token, channel, updateEmotes)
    bot.start()


if __name__ == "__main__":
    main()
