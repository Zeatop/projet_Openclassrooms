import json
from views import View

class Player:
 
    def __init__(self, name, surname, birthdate, chessID, points=0):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.chessID = chessID
        self.points = points

    def add_match_to_player(self, match):
        pass
        
    
    def __str__(self):
        return f"{self.surname} {self.name}"
    
    def serialize(self):
        return {
            'name' : self.name,
            'surname' : self.surname,
            'birthdate' : self.birthdate.strftime("%Y-%m-%d"),
            'chessID' : self.chessID,
            'points' : self.points
        }
    
    @classmethod
    def deserialize(cls, players_data):
        return Player(**players_data)
        





class Match:
    
    def __init__(self, players_list:list, score1 = 0, score2 = 0):
            self.player1 = players_list[0]
            self.player2 = players_list[1]
            self.match = (self.player1, self.player2)
            self.score1 = score1
            self.score2 = score2
            self.matchInfo = ([self.player1, self.score1], [self.player2, self.score2])

    @property
    def match_Info(self):
            self.matchInfo = ([self.player1, self.score1], [self.player2, self.score2])
    
    def __str__(self):
            return f"{self.player1} vs {self.player2}" if self.player2 else f"{self.player1}"
    
    def serialize(self):
        return {
            'player1': self.player1.serialize(),
            'player2': self.player2.serialize(),
            'score1': self.score1,
            'score2': self.score2,
        }
    
    def convert_to_json(self):
        class_dict = self.serialize
        tournament_data = json.dumps(class_dict, indent = 4)
        with open(f"{self.name}.json", "w") as json_file:
            json_file.write(tournament_data)
        json_file.close()

    def deserialize(cls, match_data):
        return Match(**match_data)
                 
         

class Round:
    
    def __init__(self, round_matches:list):
        self.matches = list()
        for match in round_matches:
            self.matches.append(match)
            match.round = self

    def __str__(self):
        match_str_list = [str(match) for match in self.matches]
        return "\n".join(match_str_list)
    
    def serialize(self):
        return {
            'matches': [match.serialize() for match in self.matches]
        }
    
    @classmethod
    def deserialize(cls, tournament_data):
        round_list = tournament_data['round_list']
        for round in round_list:
            match_list = round_list[round]
            for match in match_list:
                Match.deserialize(match, save = False)

            
        

class Tournament:

    def __init__(self, name:str, place:str, start:str, end:str, max_players:int, turns:int=10,):
        self.players_list = list()
        self.round_list = list()
        self.name = name
        self.place = place
        self.start = start
        self.end = end
        self.max_players = max_players
        self.turns = turns
        self.save_to_json()


    def add_player_to_tournament(self, player:Player, save=True):
        self.players_list.append(player)
        player.tournament = self
        if save:
            self.save_to_json()


    def register_round_in_tournament(self, round:Round):
        self.round_list.append(round)
        round.tournament = self
        self.save_to_json()


    def serialize(self):
        return {
            'name' : self.name,
            'max_players' : self.max_players,
            'place' : self.place,
            'start' : self.start.strftime("%Y-%m-%d"),
            'end' : self.end.strftime("%Y-%m-%d"),
            'players_list' : [p.serialize() for p in self.players_list],
            'round_list' : [r.serialize() for r in self.round_list] if self.round_list else [],
            'turns' : self.turns
        }
    
    def save_to_json(self):
        class_dict = self.serialize()
        tournament_data = json.dumps(class_dict, indent = 4)
        with open(f"{self.name}.json", "w") as json_file:
            json_file.write(tournament_data)
        json_file.close()

    @classmethod
    def deserialize(cls, json_file):
        with open(f"{json_file}.json", "r") as json_file:
            tournament_data = json.load(json_file)
        json_file.close()
        tournament = Tournament(name=tournament_data['name'], max_players=tournament_data['max_players'],
                                place=tournament_data['place'], start=tournament_data['start'], 
                                end=tournament_data['end'], turns=tournament_data['turns'])
        players_list = tournament_data['players_list']
        for player in players_list:
            Player.deserialize(player)
            tournament.add_player_to_tournament(player, save=False)
        round_list = tournament_data['round_list']
        for data in round_list:
            round = Round.deserialize(data, save=False)
        return tournament

    def is_tournament_finished(self):
        if self.turns == len(self.round_list):
            wish = View.display_end()
        

        













