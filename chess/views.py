from operator import attrgetter
from consolemenu.selection_menu import SelectionMenu

class View:
    def __init__(self, controller):
        self.controller = controller
        
    def show_data(self, tournament):
        '''Menu de selection et affichage des données'''

        print(tournament.description, '\n'*3)
        a_list = ["Afficher tous les joueurs par ordre alphabétique",
                "- par classement",
                "Afficher tous les tours",
                "Afficher tous les matchs"]

        menu = SelectionMenu(a_list, 'Le tournois à eu lieu à {} le '
                                    '{} en cadence {}'
                                    .format(tournament.place,
                                            tournament.date,
                                            tournament.cadence))

        menu.show()

        menu.join()

        selection = menu.selected_option
        dash = 20 * '-'
        if selection == 0:
            list_name = []
            for player in tournament.players:
                list_name.append(player.name)
            list_name.sort()
            for name in list_name:
                print(name)
                print(dash)
        elif selection == 1:
            classement_sort = tournament.players
            classement_sort = sorted(classement_sort,
                                    key=attrgetter('ranking'),
                                    reverse=True)
            for player in classement_sort:
                print('{:^10}{:^10}'.format(player.name, player.ranking))
                print(dash)
        elif selection == 2:
            for round in tournament.rondes_instances:
                print(round.round_name)
                print(dash)
                for result in round.results:
                    print('{:^10}{:^10}'.format(result[0], result[1]))
                print(dash)
        elif selection == 3:
            for round in tournament.rondes_instances:
                print(round.round_name)
                print(dash)
                for match in round.match_list:
                    print("{} s'opposait à {}".format(
                        match.player1.name, match.player2.name)
                        )
                    print(dash)
        else:
            menu.exit()
            
            self._tournament_console()
        input()


    def show_players():
        dash = '-'*30
        space = '\n'*3
        print(space, dash)
        for player in players:
            print('{:^10}{:^10}'.format(player.name, player.surname))
            print(dash)
        input('Appuyez sur entrée pour revenir au menu principal')
        
    def _tournament_console(self):
        self._tournaments = []
        self._load_tournament()
        tournaments_menu = ConsoleMenu('Tournois')
        for tournament in self._tournaments:
            name = tournament.name
            item = FunctionItem(name, show_data, args=[tournament])
            tournaments_menu.append_item(item)
        tournaments_menu.append_item(FunctionItem('Supprimer un tournois',
                                                self._remove_tournament,
                                                should_exit=True))
        tournaments_menu.show()