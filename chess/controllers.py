from . import Player, Tournament, Match, Round

from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.selection_menu import SelectionMenu

from tinydb import TinyDB, where

class Application:
    def __init__(self):
        self._players = []
        self._tournaments = []
        self._db = TinyDB("db.json")
    
        self._load_players()
        self._load_tournaments()
        
    
    def run(self):
        self._display_console_menu()
        
        
    def _save_players(self):
        '''Sauvegarde les joueurs de la liste "players"'''

        #global players
        players_table = self._db.table('players')
        players_table.truncate()
        for player in players:
            serialized_player = {
                'name': player.name,
                'surname': player.surname,
                'born': player.born,
                'gender': player.gender,
                'ranking': player.ranking,
                'score': player.score
                }
            players_table.insert(serialized_player)
            
    def _add_player(self):
        '''Créer un joueur'''

        while True:
            try:
                name = str(input('Prénom du joueur à ajouter \n'))
                if name == '':
                    raise ValueError
                surname = str(input('Nom du joueur à ajouter\n'))
                if surname == '':
                    raise ValueError
                born = str(input('Date de naissance du joueur à ajouter\n'))
                if born == '':
                    raise ValueError
                gender = str(input("Genre du joueur à ajouter ('M' ou 'F')\n"))
                if gender == '':
                    raise ValueError
                ranking = int(input("Classement du joueur à ajouter\n"))
                if ranking == '':
                    raise ValueError
                break
            except ValueError:
                print('Information obligatoire ou incorrecte, veuillez réessayer')

        new = Player(name=name, surname=surname, born=born,
                    gender=gender, ranking=ranking)
        self._players.append(new)
        self._save_players()
        
        
    def _display_console_menu(self):
        '''Menu Principal'''
        menu = ConsoleMenu("Menu de selection", "Choisissez une option")
        function_item1 = FunctionItem('Démarrer un tournois',
                                    self._tournaments_information, should_exit=True)
        function_item3 = FunctionItem('Ajouter un joueur', self._add_player)
        function_item5 = FunctionItem('Liste des joueurs', self._show_players)
        function_item4 = FunctionItem('Supprimer un joueur', self._del_player)

        submenu_reports = FunctionItem('Rapports', self._tournament_console)

        function_item2 = FunctionItem('Reprendre un tournois', self._resume_tournament)

        menu.append_item(function_item1)
        menu.append_item(function_item2)
        menu.append_item(function_item3)
        menu.append_item(function_item4)
        menu.append_item(function_item5)
        menu.append_item(submenu_reports)
        menu.show()
        

    def _tournaments_information(self):
        '''Créer un tournois'''

        if len(self._players) < 4:
            print('Trop peu de gens pour faire un tournois...')
            input()
            self._display_console_menu()
        print('Vous pouvez quitter à tout moment en tappant exit \n')
        while True:
            try:
                nb_round = int(input('Combien de rondes voulez-vous ?'
                                    ' {} rondes possibles \n'
                                    .format(str(len(players)-1))))
                if nb_round > len(players)-1 or nb_round < 0:
                    raise ValueError
                name = str(input('Nom du tournois\n'))
                if name == '':
                    raise ValueError
                place = str(input('Lieu du tournois\n'))
                if place == '':
                    raise ValueError
                date = str(input('Date du tournois \n'))
                if date == '':
                    raise ValueError
                cadence = str(input('Cadence du tournois\n'))
                if cadence == '':
                    raise ValueError
                description = str(input('Description du tournois\n'))
                break
            except ValueError:
                print("Réponse non valide")
        tournois = Tournament(name, place,
                            date, cadence,
                            description, rondes_instances=[],
                            round=nb_round)
        tournois.start_tournament()


    
    def _show_players(self):
        dash = '-'*30
        space = '\n'*3
        print(space, dash)
        for player in self._players:
            print('{:^10}{:^10}'.format(player.name, player.surname))
            print(dash)
        input('Appuyez sur entrée pour revenir au menu principal')
    
    def _del_player(self):
        '''Supprime un joueur si il n'est pas lié
        à un tournois en base de donnée'''

        can_delete = True
        while True:
            db = TinyDB('db.json')
            players_table = db.table('players')
            names = []
            for player in self._players:
                names.append(player.name)
            menu = SelectionMenu(names, 'Quel joueur supprimer ?')
            menu.show()
            menu.join()
            selection = menu.selected_option
            if selection == len(self._players):
                menu.exit()
            else:
                for tournament in self._tournaments:
                    for player in tournament.players:
                        if player.name == self._players[selection].name:
                            print('Vous ne pouvez pas supprimer ce joueur, '
                                'il fait parti du tournois : {}'
                                .format(tournament.name))
                            print('Supprimez le tournois dans la base de donnée '
                                'pour supprimer ce joueur')
                            input()
                            can_delete = False
                if can_delete:
                    players_table.remove(where('name') == names[selection])
                    self._players.pop(selection)
                else:
                    continue
            break
    
    
    
    def _tournament_console(self):
        pass
    
    def _resume_tournament(self):
        pass




        
    def _load_players(self):
        '''Charge tout les joueurs vers la liste "players"
        depuis la base de donnée'''

        players_table = self._db.table('players')
        serialized_players = players_table.all()
        for serial in serialized_players:
            name = serial['name']
            surname = serial['surname']
            born = serial['born']
            gender = serial['gender']
            ranking = serial['ranking']
            score = serial['score']
            self._players.append(Player(name, surname, born, gender, ranking, score))
            
    def _load_tournaments(self):
        '''Charge les tournois vers la liste tournaments
        depuis la base de donnée'''

        tournaments_table = self._db.table('tournaments')
        players_no_ser = []
        round_no_ser = []
        player1 = None
        player2 = None
        match_no_ser = []
        serialized_tournaments = tournaments_table.all()
        for serial in serialized_tournaments:
            place = serial['place']
            date = serial['date']
            cadence = serial['cadence']
            round = serial['round']
            rondes_instances = serial['rondes_instances']
            round_no_ser = []
            for ronde in rondes_instances:
                match_no_ser = []
                round_name = ronde['round_name']
                results = ronde['results']
                match_list = ronde['match_list']
                for match in match_list:
                    for player in self._players:
                        if match['player1'] == player.name:
                            player1 = player
                        if match['player2'] == player.name:
                            player2 = player
                    match_no_ser.append(Match(player1, player2))
                round_no_ser.append(Round(round_name,
                                        results,
                                        match_list=match_no_ser))
            players_ser = serial['players']
            players_no_ser = []
            for serial_p in players_ser:
                name = serial_p['name']
                surname = serial_p['surname']
                born = serial_p['born']
                gender = serial_p['gender']
                ranking = serial_p['ranking']
                score = serial_p['score']
                players_no_ser.append(Player(name,
                                            surname,
                                            born,
                                            gender,
                                            ranking,
                                            score))
            name = serial['name']
            description = serial['description']
            turn = serial['turn']
            opponents = serial['opponents']
            self._tournaments.append(Tournament(name, place,
                                        date, cadence,
                                        description, round,
                                        round_no_ser, players_no_ser,
                                        turn, opponents))
        