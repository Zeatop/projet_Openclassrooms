
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
            'birthdate' : self.birthdate,
            'chessID' : self.chessID,
            'points' : self.points
        }


class Match:
    
    def __init__(self, players_list:list, score1 = 0, score2 = 0):
            self.player1 = players_list[0]
            self.player2 = players_list[1]
            self.match = (self.player1, self.player2)
            self.score1 = score1
            self.score2 = score2
            self.matchInfo = ([self.player1, self.score1], [self.player2, self.score2])
    
    def __str__(self):
            return f"{self.player1} vs {self.player2}" if self.player2 else f"{self.player1}"
    
    def serialize(self):
        return {
            'matchInfo' : self.matchInfo
        }
                 
         

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
            'matches' : self.matches
        }
        

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

    def add_player_to_tournament(self, player:Player):
        self.players_list.append(player)
        player.tournament = self

    def register_round_in_tournament(self, round:Round):
        self.round_list.append(round.matches)

    def serialize(self):
        return {
            'name' : self.name,
            'max_players' : self.max_players,
            'place' : self.place,
            'start' : self.start,
            'end' : self.end,
            'players_list' : [],
            'round_list' : [],
            'turns' : self.turns
        }













