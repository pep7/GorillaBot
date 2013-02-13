# Copyright (c) 2013 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

__all__ = ["CommandManager"]

class CommandManager(object):
    
    def __init__(self, bot, connection):
        self._bot = bot
        self._connection = connection
        self._bot_nick = connection._nick
        
    def check_command(self, line):
        '''Messages of type PRIVMSG will be passed through this function to check if they are
        commands.'''
        
        # Format message more nicely
        raw_nick = line.pop(0)
        r = re.search(":(.*?)!", raw_nick)
        if r:
            sender = r.group(1)
        line.pop(0)
        private = False
        raw_chan = line.pop(0)
        if raw_chan == self._bot_nick:
            private = True
        line[0] = line[0][1:]
        # line is now a list containing just the message contents.
        
        # Check if a private message contains a command
        # First looks for words beginning with an exclamation point. If none are found, it assumes
        #     the first word of the message is the command.
        command = ""
        command_type = ""
        if private:
            for word in line:
                if word[0] == "!":
                    command = word[1:]
            if command == "":
                command = line[0]
            command_type = "private"
        # Check for a message directly addressed to the bot
        elif self._bot_nick in line[0]:
            if line[1][0] == "1":
                command = line[1][1:]
            else:
                command = line[1]
            command_type = "direct"
        #Check for a message preceded by an exclamation point
        else:
            for idx, word in enumerate(line):
                if word[0] == "!":
                    command = word[1:]
                    command_type = "exclamation"
                    if idx == 0:
                        command_type = "exclamation_first"
        
        if command != "":
            print(command)
            print(command_type)

    def nickserv_reply(self, line):
        pass
    
    def process_numcode(self, numcode, line):
        pass