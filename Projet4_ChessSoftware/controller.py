import models
import views
import random
import json


class Controller:
    @staticmethod
    def create_tournament():
        data = views.View.display_start_menu()
        print(data)
        if data[0] == '2':
            print(data[1])
            with open(f"{data[1]}.json", "r") as json_file:
                tournament_data = json.load(json_file)
            tournament = models.Tournament.deserialize(tournament_data)
            Controller.start_tournament(tournament)

        if data[0] == '3':
            with open(f"{data[1]}.json", "r") as json_file:
                tournament_data = json.load(json_file)
            # json_report = views.View.display_report_from_start(tournament_data)
            tournament = models.Tournament.deserialize(tournament_data)
            tables = tournament.create_report()
            views.View.display_end(tournament, tables)
            tournament.players_list.sort(key=lambda x: x.points, reverse=True)
        if data == '1':
            tournament = views.View.display_create_tournament()
            tournament = models.Tournament(**tournament)
            views.View.display_tournament(tournament)
            return tournament
        return

    @staticmethod
    def create_players(tournament):
        while len(tournament.players_list) < tournament.max_players:
            data = views.View.display_add_players()
            player = models.Player(**data)
            tournament.add_player_to_tournament(player)
        views.View.display_players_list(tournament.players_list)

    @staticmethod
    def create_matches(tournament, players_list):
        """Création de matchs, réunis en un un round (liste de matchs)"""
        match_list = list()
        transit_list = players_list.copy()
        while len(transit_list) >= 2:
            random.shuffle(transit_list)
            match = models.Match(transit_list)
            match_list.append(match)
            transit_list.pop(0)
            transit_list.pop(0)
        round = models.Round(match_list)
        tournament.register_round_in_tournament(round)

    @staticmethod
    def set_score(match: models.Match):
        winner = views.View.display_set_scores(match)
        print(f"Winner for match {match}: {winner}")
        player1 = match.player1
        player2 = match.player2
        print(f"Scores for match {match}: {match.score1}, {match.score2}")
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
        print(f"Scores after saving: {match.score1}, {match.score2}")

    @staticmethod
    def play_round(tournament):
        views.View.display_start_round(tournament)
        try:
            tournament.round_list[-2]
        except IndexError:
            round = tournament.round_list[-1]
        else:
            round = tournament.round_list[-2]
        for match in round.matches:
            Controller.set_score(match)
            match.round.tournament.save_to_json()
            # print(round) # Uniquement là pour le AUTOCOMPLETION == TRUE

    @staticmethod
    def start_tournament(tournament=None):
        if tournament is None:
            tournament = Controller.create_tournament()
        if isinstance(tournament, models.Tournament):
            Controller.create_players(tournament)
            try:
                tournament.round_list[-2]
            except IndexError:
                print("Except")
                while len(tournament.round_list) < tournament.turns:
                    print(f'Round n°{len(tournament.round_list)+1} / {tournament.turns}')
                    Controller.create_matches(tournament, tournament.players_list)
                    Controller.play_round(tournament)
                    views.View.display_scores(tournament)
            else:
                while len(tournament.round_list) < tournament.turns:
                    Controller.create_matches(tournament, tournament.players_list)
                    Controller.play_round(tournament)
                    views.View.display_scores(tournament)
        tournament.players_list.sort(key=lambda x: x.points, reverse=True)
        tables = tournament.create_report()
        print('********DEBUG********')
        for match in tournament.round_list[-1].matches:
            print(match.player1, match.player2, match.score1, match.score2)
        for match in tournament.round_list[-2].matches:
            print(match.player1, match.player2, match.score1, match.score2)
        restart = views.View.display_end(tournament, tables)

        if restart == 'o':
            Controller.start_tournament()

