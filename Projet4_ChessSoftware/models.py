import json


class Player:
    def __init__(self, name, surname, birthdate, chessID, points=0):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.chessID = chessID
        self.points = points

    def __str__(self):
        return f"{self.surname} {self.name}"

    def serialize(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'birthdate': self.birthdate,
            'chessID': self.chessID,
            'points': self.points
        }

    @classmethod
    def deserialize(cls, players_data):
        return Player(
            name=players_data['name'],
            surname=players_data["surname"],
            birthdate=players_data['birthdate'],
            chessID=players_data['chessID'],
            points=players_data['points']
        )


class Match:
    def __init__(self, players_list: list, score1=None, score2=None):
        self.player1 = players_list[0]
        self.player2 = players_list[1]
        self.match = (self.player1, self.player2)
        self.score1 = score1
        self.score2 = score2
        self.matchInfo = ([self.player1, self.score1], [self.player2, self.score2])

    def __str__(self):
        return f"{self.player1} ({self.score1}) vs {self.player2} ({self.score2})" if self.score1 else f"{self.player1} vs {self.player2}"

    def serialize(self):
        return {
            'player1': self.player1.serialize(),
            'player2': self.player2.serialize(),
            'score1': self.score1,
            'score2': self.score2,
        }

    @classmethod
    def deserialize(cls, match_data):
        player1 = Player.deserialize(match_data['player1'])
        player2 = Player.deserialize(match_data['player2'])
        return cls(
            players_list=[player1, player2],
            score1=match_data['score1'],
            score2=match_data['score2']
        )


class Round:
    def __init__(self, round_matches: list):
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
    def deserialize(cls, round_data):
        return cls(round_matches=round_data)


class Tournament:
    def __init__(self, name: str, place: str, start: str, end: str, max_players: int, turns: int = 10, save=True):
        self.players_list = list()
        self.round_list = list()
        self.name = name
        self.place = place
        self.start = start
        self.end = end
        self.max_players = int(max_players)
        self.turns = int(turns)
        if save:
            self.save_to_json()

    def add_player_to_tournament(self, player: Player, save=True):
        self.players_list.append(player)
        player.tournament = self
        if save:
            self.save_to_json()

    def register_round_in_tournament(self, round: Round, save=True):
        self.round_list.append(round)
        round.tournament = self
        if save:
            self.save_to_json()

    def serialize(self):
        return {
            'name': self.name,
            'max_players': self.max_players,
            'place': self.place,
            'start': self.start,
            'end': self.end,
            'players_list': [p.serialize() for p in self.players_list],
            'round_list': [r.serialize() for r in self.round_list] if self.round_list else [],
            'turns': int(self.turns)
        }

    def save_to_json(self):
        class_dict = self.serialize()
        tournament_data = json.dumps(class_dict, indent=4)
        with open(f"{self.name}.json", "w") as json_file:
            json_file.write(tournament_data)

    @classmethod
    def deserialize(cls, tournament_data):
        tournament = Tournament(
            name=tournament_data['name'],
            max_players=tournament_data['max_players'],
            place=tournament_data['place'],
            start=tournament_data['start'],
            end=tournament_data['end'],
            turns=tournament_data['turns'],
            save=False
        )
        players_list = tournament_data['players_list']
        for player in players_list:
            player = Player.deserialize(player)
            tournament.add_player_to_tournament(player, save=False)
        round_list = tournament_data['round_list']
        for round_data in round_list:
            matches = []
            for match in round_data['matches']:
                match = Match.deserialize(match_data=match)
                matches.append(match)
            round_obj = Round(matches)
            tournament.register_round_in_tournament(round_obj, save=False)
        return tournament
