import settings
from faker import Faker
fake = Faker()

class View:
    

    @staticmethod
    def display_create_tournament():
        wish = input("Voulez-vous démarrer un tournoi ? \nOui: o\nNon: n")
        if wish != 'o':
            return
        
        print('#' * 79)
        print("Création d'un tournoi")
        print('#' * 79)

        if settings.AUTOCOMPLETION == True:
            name = 'Test'
            place = fake.city()
            start = fake.date_this_month(before_today = True)
            end = fake.date_this_month(after_today = True)
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
        print('#' * 79)
        print(f"Tournoi:")
        print("")
        print(f"Nom: {tournament.name} \nLieu: {tournament.place} \nDébut: {tournament.start} \nFin: {tournament.end} \nNombre de joueurs: {tournament.max_players} \nTours: {tournament.turns}")
        


    @staticmethod
    def display_add_players():
        print('#' * 79)
        if settings.AUTOCOMPLETION == True:
            name = fake.name()
            surname = fake.first_name()
            birthdate = fake.date_of_birth(minimum_age = 15)
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
        print('#' * 79)
        print('Liste des joueurs inscrits')
        for player in players: 
            print('_'*len(player.name))
            print(player)
        print('#' * 79)

    
    # @staticmethod
    # def display_create_matches(tournament):
    #     print('#' * 79)
    #     print('Matchs du Round: \n ')
    #     for i in 
        


            

