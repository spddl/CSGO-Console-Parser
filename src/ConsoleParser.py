from CSGOGame import CSGOGame

class ConsoleParser:
    def __init__(self, console_tailer, link):
        self.console_tailer = console_tailer
        self.link = link
        self.csgo_game = CSGOGame()
        self.clear_dmg()
        self.lastkiller = False
        self.lastkillerkiller = ""

    def listen(self):
        try:
            while True:
                next_line = self.console_tailer.poll()
                self.handle(next_line)
        except KeyboardInterrupt:
            self.console_tailer.stop()

    def handle(self, log_line):
        if 'Counter-Strike: Global Offensive' in log_line:
            self.csgo_game = CSGOGame()
            self.clear_dmg()
        elif '-------------------------' in log_line:
            self.damage_string(link=self.link, line=log_line)
        elif 'Map:' in log_line:
            self.csgo_game.set_map(log_line.split(' ')[1])
        elif 'Damage' in log_line:
            self.damage_report(log_line)
        elif '0:  Reinitialized' in log_line:
            self.csgo_game.start_round()
            self.clear_dmg()
        elif 'Shutdown function' in log_line:
            self.csgo_game.end_last_round()

    def clear_dmg(self):
        self.lastkillerkiller = ""
        text_file = open(self.link+'\cfg\dmg.cfg', "w")
        text_file.write("")
        text_file.close()

    def damage_string(self, link, line):
        if self.lastkiller:
            self.lastkiller = False
            text_file = open(link+'\cfg\dmg.cfg', "w")
            text_file.write(self.lastkillerkiller)
            text_file.close()
        else:
            self.lastkiller = True

    def player_connected(self, log_line):
        split_line = log_line.split(' ')
        self.csgo_game.register_player(split_line[0])

    def damage_report(self, log_line):
        if 'Damage Taken from' in log_line:
            self.damage_received(log_line)
        elif 'Damage Given to "' in log_line:
            self.damage_given(log_line)

    def damage_given(self, log_line):
        given_to, damage_amount, hits = self.parse_damage_line(log_line)
        self.csgo_game.damage_given(given_to, damage_amount, hits)
        if self.lastkiller:
            if float(damage_amount) <= 99:
                self.lastkillerkiller = "say_team Damage Given to "+given_to+" - "+damage_amount+" in "+hits+" hits"
        
    def damage_received(self, log_line):
        given_by, damage_amount, hits = self.parse_damage_line(log_line)
        self.csgo_game.damage_received(given_by, damage_amount, hits)

    def parse_damage_line(self, log_line):
        split_quote = log_line.split('"')
        player = split_quote[1]
        split_space = split_quote[2].split(' ')
        return player, split_space[2], split_space[4]
