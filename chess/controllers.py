from .models import Model, Player, Tournament, Match, Round
from .processors import TournamentProcessor
from .views import View

from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.selection_menu import SelectionMenu


class Application:
    """Our only one controller for the app.
    The *Application* will hold references to both the model and the view.
    Internally, they will be defined through the *self._model* and
    *self._view*. They are hidden outside the scope of the *Application* class.
    """

    def __init__(self, database_path):
        self._players = []
        self._tournaments = []

        self._model = Model(database_path)
        self._view = View(self)
        self._tournament_processor = None
        self._round_processor = None

        self._load_players()
        self._load_tournaments()

    @property
    def model(self):
        return self._model

    def run(self):
        self._display_console_menu()

    def _save_players(self):
        '''Sauvegarde les joueurs de la liste "players"'''

        # global players
        self._model.players_table.truncate()
        for player in self._players:
            serialized_player = {
                "name": player.name,
                "surname": player.surname,
                "born": player.born,
                "gender": player.gender,
                "ranking": player.ranking,
                "score": player.score,
            }
            self._model.players_table.insert(serialized_player)

    def _add_player(self):
        """Créer un joueur"""

        while True:
            try:
                name = str(input("Prénom du joueur à ajouter \n"))
                if name == "":
                    raise ValueError
                surname = str(input("Nom du joueur à ajouter\n"))
                if surname == "":
                    raise ValueError
                born = str(input("Date de naissance du joueur à ajouter\n"))
                if born == "":
                    raise ValueError
                gender = str(input("Genre du joueur à ajouter ('M' ou 'F')\n"))
                if gender == "":
                    raise ValueError
                ranking = int(input("Classement du joueur à ajouter\n"))
                if ranking == "":
                    raise ValueError
                break
            except ValueError:
                print(
                    "Information obligatoire ou incorrecte, veuillez réessayer"
                )

        new = Player(
            name=name,
            surname=surname,
            born=born,
            gender=gender,
            ranking=ranking,
        )
        self._players.append(new)
        self._save_players()

    def _display_console_menu(self):
        """Menu Principal"""
        menu = ConsoleMenu("Menu de selection", "Choisissez une option")
        function_item1 = FunctionItem(
            "Démarrer un tournois",
            self._tournaments_information,
            should_exit=True,
        )
        function_item3 = FunctionItem("Ajouter un joueur", self._add_player)
        function_item5 = FunctionItem("Liste des joueurs", self._show_players)
        function_item4 = FunctionItem("Supprimer un joueur", self._del_player)

        submenu_reports = FunctionItem("Rapports", self._tournament_console)

        function_item2 = FunctionItem(
            "Reprendre un tournois", self._resume_tournament
        )

        menu.append_item(function_item1)
        menu.append_item(function_item2)
        menu.append_item(function_item3)
        menu.append_item(function_item4)
        menu.append_item(function_item5)
        menu.append_item(submenu_reports)
        menu.show()

    def _tournaments_information(self):
        """Créer un tournois"""

        if len(self._players) < 4:
            print("Trop peu de gens pour faire un tournois...")
            input()
            self._display_console_menu()
        print("Vous pouvez quitter à tout moment en tappant exit \n")
        while True:
            try:
                possible_rounds_count = len(self._players) - 1
                nb_round = input(
                    "Combien de rondes voulez-vous ?"
                    " {} rondes possibles \n".format(possible_rounds_count)
                )
                # Nombre de tours du tournois     
                nb_round = int(nb_round) if nb_round.isdigit() else 4
                
                if nb_round > len(self._players) - 1 or nb_round < 0:
                    raise ValueError
                name = str(input("Nom du tournois\n"))
                if name == "":
                    raise ValueError
                place = str(input("Lieu du tournois\n"))
                if place == "":
                    raise ValueError
                date = str(input("Date du tournois \n"))
                if date == "":
                    raise ValueError
                cadence = str(input("Cadence du tournois\n"))
                if cadence == "":
                    raise ValueError
                description = str(input("Description du tournois\n"))
                break
            except ValueError:
                print("Réponse non valide")
        tournament = Tournament(
            name,
            place,
            date,
            cadence,
            description,
            players=self._players,
            rounds=[],
            round_count=nb_round,
        )
        self._tournament_processor = TournamentProcessor(
            controller=self, tournament=tournament
        )
        self._tournament_processor.process()

    def _show_players(self):
        self._view.show_players(self._players)

    def _del_player(self):
        """Supprime un joueur si il n'est pas lié
        à un tournois en base de donnée"""

        can_delete = True
        while True:
            names = []
            for player in self._players:
                names.append(player.name)
            menu = SelectionMenu(names, "Quel joueur supprimer ?")
            menu.show()
            menu.join()
            selection = menu.selected_option
            if selection == len(self._players):
                menu.exit()
            else:
                for tournament in self._tournaments:
                    for player in tournament.players:
                        if player.name == self._players[selection].name:
                            print(
                                "Vous ne pouvez pas supprimer ce joueur, "
                                "il fait parti du tournois : {}".format(
                                    tournament.name
                                )
                            )
                            print(
                                "Supprimez le tournois dans la base de donnée "
                                "pour supprimer ce joueur"
                            )
                            input()
                            can_delete = False
                if can_delete:
                    self._model.delete_player(self._players[selection])
                    self._players.pop(selection)
                else:
                    continue
            break

    def _tournament_console(self):
        self.reload_tournaments()
        tournaments_menu = ConsoleMenu("Tournois")
        for tournament in self._tournaments:
            name = tournament.name
            item = FunctionItem(name, self._view.show_data, args=[tournament])
            tournaments_menu.append_item(item)
        tournaments_menu.append_item(
            FunctionItem(
                "Supprimer un tournois",
                self._remove_tournament,
                should_exit=True,
            )
        )
        tournaments_menu.show()

    def _remove_tournament(self):
        """Supprime un tournoi de la base de donnée avec
        un affichage console"""
        names = []
        for tournament in self._tournaments:
            names.append(tournament.name)
        menu = SelectionMenu(names, "Quel tournoi supprimer ?")
        menu.show()
        selection = menu.selected_option

        self._model.delete_tournament(self._tournaments[selection])
        self._tournaments.delete(self._tournaments[selection])
        self._tournament_console()

    def _resume_tournament(self):
        names = []
        selected_tournaments = []
        self.reload_tournaments()
        for tournament in self._tournaments:
            finish = True
            for round_ in tournament.rounds:
                if len(round_.results) != len(tournament.players):
                    finish = False
            if (
                len(tournament.rounds) != tournament.round_count
                or not finish
            ):
                names.append(tournament.name)
                selected_tournaments.append(tournament)
        menu = SelectionMenu(names, "Quel tournoi continuer ?")
        menu.should_exit = True
        menu.show()
        selection = menu.selected_option
        try:
            tournament_processor = TournamentProcessor(
                self, selected_tournaments[selection]
            )
        except IndexError:
            print("Mauvais choix ")
        else:
            tournament_processor.process()
            
    def _load_players(self):
        """Charge tout les joueurs vers la liste "players"
        depuis la base de données."""
        serialized_players = self._model.players_table.all()
        for serial in serialized_players:
            name = serial["name"]
            surname = serial["surname"]
            born = serial["born"]
            gender = serial["gender"]
            ranking = serial["ranking"]
            score = serial["score"]
            self._players.append(
                Player(name, surname, born, gender, ranking, score)
            )

    def del_tournament(self, tournament):
        """Supprime un tournois de la base de donnée sans affichage console"""

        # Delete the tournament from the database.
        self._model.delete_tournament(tournament)

        # Then delete it from the internal list.
        for i in range(len(self._tournaments)-1):
            if self._tournaments[i].name == tournament.name:
                self._tournaments.pop(i)

    def reload_tournaments(self):
        """Reload the tournaments from the database."""
        self._tournaments = []
        self._load_tournaments()

    def _load_tournaments(self):
        """Charge les tournois vers la liste tournaments
        depuis la base de donnée"""
        players_no_ser = []
        round_no_ser = []
        player1 = None
        player2 = None
        match_no_ser = []
        serialized_tournaments = self._model.tournaments_table.all()
        for serial in serialized_tournaments:
            place = serial["place"]
            date = serial["date"]
            cadence = serial["cadence"]
            round_count = serial["round_count"]
            rounds = serial["rounds"]
            round_no_ser = []
            for ronde in rounds:
                match_no_ser = []
                round_name = ronde["round_name"]
                results = ronde["results"]
                match_list = ronde["match_list"]
                for match in match_list:
                    for player in self._players:
                        if match["player1"] == player.name:
                            player1 = player
                        if match["player2"] == player.name:
                            player2 = player
                    match_no_ser.append(Match(player1, player2))
                round_no_ser.append(
                    Round(round_name, results, match_list=match_no_ser)
                )
            players_ser = serial["players"]
            players_no_ser = []
            for serial_p in players_ser:
                name = serial_p["name"]
                surname = serial_p["surname"]
                born = serial_p["born"]
                gender = serial_p["gender"]
                ranking = serial_p["ranking"]
                score = serial_p["score"]
                players_no_ser.append(
                    Player(name, surname, born, gender, ranking, score)
                )
            name = serial["name"]
            description = serial["description"]
            turn = serial["turn"]
            opponents = serial["opponents"]
            self._tournaments.append(
                Tournament(
                    name,
                    place,
                    date,
                    cadence,
                    description,
                    round_count,
                    round_no_ser,
                    players_no_ser,
                    turn,
                    opponents,
                )
            )

    def _save_current_tournament(self, serialized_tournament):
        """Save *serialized_tournament*."""
        self._model.tournaments_table.insert(serialized_tournament)