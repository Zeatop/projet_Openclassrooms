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

    @staticmethod
    def create_matches(tournament, players_list):
        """Création de matchs, réunis en un un round (liste de matchs)"""
        match_list = list()
        transit_list = players_list.copy()
        while len(transit_list) >= 2 :
            random.shuffle(transit_list)
            match = Match(transit_list)
            match_list.append(match)
            transit_list.pop(0)
            transit_list.pop(0)
        round = Round(match_list)
        tournament.register_round_in_tournament(round)
    
    @staticmethod
    def set_score(match: Match):
        winner = View.display_set_scores(match)
        player1 = match.player1
        player2 = match.player2
        if winner == '1':
            match.score1 = 2
            player1.points += match.score1
            match.score2 = 0
        elif winner == '2':
            match.score2 = 2
            player2.points += match.score2
            match.score1 = 0
        elif winner == '3':
            match.score1 = 1
            match.score2 = 1
            player1.points += match.score1
            player2.points += match.score2
        
        match.round.tournament.save_to_json()

            
      

    @staticmethod
    def play_round(tournament):
        View.display_start_round(tournament)
        round = tournament.round_list[-1]
        for match in round.matches:
            Controller.set_score(match)
            print(round)
        View.display_scores(tournament)
            


tournament = Controller.create_tournament()
Controller.create_players(tournament)
for i in range(tournament.turns):
    Controller.create_matches(tournament, tournament.players_list)
    Controller.play_round(tournament)
