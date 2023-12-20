
class Player:
 
    def __init__(self, name, surname, birthdate, chessID, points=0):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.chessID = chessID
        self.points = points
        
    
    def __str__(self):
        return f"{self.name}"


class Match:
    
    def __init__(self, players_list:list):
            self.player1 = players_list[0]
            try:
                self.player2 = players_list[1]
            except: pass
            

    def set_match_score (self, score1:int,score2:int):
        self.score1 = score1
        self.score2 = score2
        self.matchInfo = ([self.player1, self.score1], [self.player2, self.score2])
         


class Round:
    
    def __init__(self, matches_round:list):
        self.matches_round = matches_round
        

    def add_match_to_round(self, match:Match):
        self.matches.append(match)
        match.round = self


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
    
    def which_round(self):
        self.which_round = len(self.round_list)













