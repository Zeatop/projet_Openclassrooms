import settings
from faker import Faker
from prettytable import PrettyTable
import json
fake = Faker()


def print_table(table):
    x = PrettyTable(table[0])
    for row in table[1:]:
        x.add_row(row)

    print(x)




class View:
    

    @staticmethod
    def display_start_menu():
        wish = input("Démarrer un tournoi ? (press 1) \nRelancer un tournoi: press(2) \nRapports: (press 3) \nQuitter: (press anything else) \nRéponse: ")
        if wish != '1' and wish !='2' and wish !='3':
            return
        elif wish == '3':
            which = input("De quel tournoi voulez-vous le rapport ? (sans extension) \nRéponse: ")
            wish = (wish, which)
            print (wish)
            return wish
        elif wish == '2':
            which = input("Quel tournoi voulez-vous Redémarrer ? (sans extension)\nRéponse: ")
            wish = (wish, which)
            print (wish)
            return wish
        elif wish =='1': 
            return wish

    def display_create_tournament(): 
        print('#' * 20)
        print("Création d'un tournoi")
        print('#' * 20)
    
        if settings.AUTOCOMPLETION == True:
            name = 'Test'
            place = fake.city()
            start = 'date'
            end = 'date'
            max_players = 10
            turns = fake.pyint(max_value = 10)
            return {
                'name': name,
                'place': place,
                'start': start,
                'end': end,
                'max_players': max_players,
                'turns': turns
            }
    
        name = input("Nom du tournoi: ")
        place = input("Lieu du tournoi:  ")
        start = input("Date de début: ")
        end = input("De de fin: ")
        max_players = int(input("Nombre de joueurs: "))
        turns = input("Nombre de tours: ")
        return {
            'name': name,
            'place': place,
            'start': start,
            'end': end,
            'max_players': max_players,
            'turns': turns
        }


    @staticmethod
    def display_tournament(tournament):
        print("")       
        print(f"Tournoi:")
        table_tournoi = [
        ["Nom", "Lieu", "Début", "Fin", "Nombre de joueurs", "Tours"],
        [tournament.name, tournament.place, tournament.start, tournament.end, tournament.max_players, tournament.turns]
        ]
        print_table(table_tournoi)
        


    @staticmethod
    def display_add_players():
        if settings.AUTOCOMPLETION == True:
            name = fake.last_name()
            surname = fake.first_name()
            birthdate = 'date'
            chessID = fake.bothify(text='??-#####')
            return {
                'name': name, 
                'surname': surname,
                'birthdate': birthdate,
                'chessID' : chessID
            }
    
        name = input('Nom: ')
        surname = input('Prénom: ')
        birthdate = input('Date de naissance: ')
        chessID = input('ChessID: ')
        return {
            'name': name, 
            'surname': surname,
            'birthdate': birthdate,
            'chessID' : chessID
        }
    
    @staticmethod
    def display_players_list(players):
        print('#' * 20)
        print('Liste des joueurs inscrits')
        for player in players: 
            print('_'*len(player.name))
            print(player)
        print('#' * 20)

    @staticmethod
    def display_start_round(tournament):
        wish = input(f"Appuyez sur 'Enter'pour démarrer le Round n°{len(tournament.round_list)} \nAppuyez sur une autre touche pour quitter.")
        if wish != '':
            wish = input(f"Appuyez sur 'Enter' pour quitter \nAppuyez sur une autre touche pour revenir en arrière.")
            if wish != '':
                View.display_start_round(tournament)
            return
    
    @staticmethod
    def display_set_scores(match):
        print('#' * 20)
        print(f'{match.player1} vs. {match.player2}:')
        if settings.AUTOCOMPLETION == True:
            random_number = fake.pyint(min_value=1, max_value=3)
            winner = str(random_number)
            return winner
        winner = input('Quel joueur a gagné le match ? \n 1 pour Joueur 1, 2 pour joueur 2 et 3 pour match nul. \nRéponse: ')
        if winner != "1" and winner != "2" and winner != "3":
            print(f"{'#'* 5}Erreur de saisie {'#'* 5}")
            View.display_set_scores()
        return winner
    
    @staticmethod
    def display_scores(tournament, report=False):
        if report == False:
            print(f"\n{'#'* 20} \nFin du round n°{len(tournament.round_list)}")
        round = tournament.round_list[-1]
        players_score = list()
        headers = ["Nom", "Prénom", "Score"]
        players_score.append(headers)
        for match in round.matches:
            player1 = match.player1
            player1 = [player1.name, player1.surname, player1.points]
            player2 = match.player2
            player2 = [player2.name, player2.surname, player2.points]
            players_score.append(player1)
            players_score.append(player2)
        print_table(players_score)

    @staticmethod
    def display_end(tournament):
        print('*'*40)
        print(f"Le Tournoi {tournament.name} est Terminé. \n Le vainqueur est: {tournament.players_list[0]} ")
        View.display_report(tournament)
        wish = input("\n \nVoulez-vous relancer un tournoi ? \nOui: o\nNon: n \nRéponse: ")
        if wish != 'o':
            return
        print('*'*40)
        return wish
    
    @staticmethod
    def display_report(tournament):
        print('*' * 40 )
        print(f"\n Rapport du tournoi: {tournament.name} \n")
        View.display_scores(tournament, report=True)
        print('\n'+('*' * 40) )
        return
    
    def report(self):
        print("*"*50,
              "\nRapport de tournoi d'échecs")
        tournament = View.display_tournament(self)
        print(tournament)
        View.display_scores(self, report=True)
        print("*"*50)
    
    @staticmethod
    def display_report_from_start(rapport:dict):
        print('*' * 40 )
        print(f"\n Rapport du tournoi: {rapport['name']} \n")
        print(json.dumps(rapport, sort_keys=True,indent=4,separators=(',', ': ')))
        print('\n'+('*' * 40) )
        return
    
    @staticmethod
    def last_choice():
        wish = input("Rapport rapide: (press 1) \nRapport détaillé: (press 2) \nQuitter: (press anything else) \nRéponse: ")
        if wish != '1' and wish !='2' and wish !='3':
            pass
        elif wish == '1':
            return wish 
        elif wish == '2':
            return wish 





