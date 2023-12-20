from models import Player, Tournament, Match, Round
from views import View
import random

class Controller:

    @staticmethod
    def create_tournament():
        data = View.display_create_tournament()
        tournament = Tournament(**data)
        View.display_tournament(tournament)
        return tournament
    
    @staticmethod
    def create_players(tournament):
        i = 0
        while i < tournament.max_players:
            data = View.display_add_players()
            player = Player(**data)
            tournament.add_player_to_tournament(player)
            i += 1
        View.display_players_list(tournament.players_list)

    # def create_match(tournament):
    #     player_list = tournament.players_list
    #     random_player_1 = random.choices(tournament.players_list, k=1)

    @staticmethod
    def create_matches(players_list):
        match_list = list()
        transit_list = players_list
        while len(transit_list) != 0 :
            random.shuffle(transit_list)
            match = Match(transit_list)
            print(len(transit_list))
            transit_list.pop(0)
            try:
                transit_list.pop(1)
            except: pass
            try:
                match_list.append((match.player1, match.player2 ))
            except:
                match_list.append(match.player1)
            
        for i in range(len(match_list)):
            print(f"match: {match_list[i]} \n {'*'*20}")
            

       
tournament = Controller.create_tournament()
Controller.create_players(tournament)
print(f'longueur de la liste: {len(tournament.players_list)} \n{tournament.players_list}')
Controller.create_matches(tournament.players_list)