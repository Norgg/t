import irc.bot
import irc.strings
import re
from random import random
irc.client.ServerConnection.buffer_class.errors = u'replace'

replace_strings = [
    u"tee",
    u"te",
    u"ty",
    u"tio",
    u"ti"
]

replace_with=ur"tea"
replace_prob=0.01

server = u'irc.imaginarynet.org.uk'
port = 6667
channels = [u'#teatest', u'#compsoc', u'#compsoc-minecraft']

class TeaBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nick, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
        self.channels_to_join = channels
        self.nick = nick
        self.replace_check = re.compile(replace_with, re.I|re.U)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        for channel in self.channels_to_join:
            c.join(channel)

    def on_notify(selc, ctx, evt):
        print(evt.arguments[0])

    def on_privmsg(self, ctx, evt):
        pass

    def on_pubmsg(self, ctx, evt):
        msg = evt.arguments[0]
        addressed = msg.startswith(u"{}: ".format(self.nick))
        
        if addressed:
            this_replace_prob = 1
        else:
            this_replace_prob = replace_prob

        channel = evt.target
        print(channel, msg)
        for s in replace_strings:
            match = re.compile(ur"(\w*({})\w*)".format(s), re.I|re.U).search(msg)
            if match and random() < this_replace_prob:
                word = match.groups()[0]
                replace = match.groups()[1]
                
                if self.replace_check.search(word):
                    continue
                response = word.replace(replace, replace_with).title()
                response = u"{}.".format(response)
                self.connection.privmsg(channel, response)
                return
        
        if addressed:
            self.connection.privmsg(channel, u"No tea.")
        


def main():
    TeaBot(channels, u't', server, port).start()

if __name__ == u"__main__":
    main()


