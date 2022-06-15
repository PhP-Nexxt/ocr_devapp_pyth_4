from operator import attrgetter
import time
from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.selection_menu import SelectionMenu
from tinydb import TinyDB, where

# Ensemble des joueurs (chargés au démarrage)
#players = []
# Ensemble des tournois (chargés au démarrage)
#tournaments = []

# Vues


def show_data(tournament):
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
        tournament_console()
    input()


def show_players():
    dash = '-'*30
    space = '\n'*3
    print(space, dash)
    for player in players:
        print('{:^10}{:^10}'.format(player.name, player.surname))
        print(dash)
    input('Appuyez sur entrée pour revenir au menu principal')


def console_menu():
    '''Menu Principal'''
    menu = ConsoleMenu("Menu de selection", "Choisissez une option")
    function_item1 = FunctionItem('Démarrer un tournois',
                                  tournaments_informations, should_exit=True)
    function_item3 = FunctionItem('Ajouter un joueur', add_player)
    function_item5 = FunctionItem('Liste des joueurs', show_players)
    function_item4 = FunctionItem('Supprimer un joueur', del_player)

    submenu_reports = FunctionItem('Rapports', tournament_console)

    function_item2 = FunctionItem('Reprendre un tournois', resume_tournament)

    menu.append_item(function_item1)
    menu.append_item(function_item2)
    menu.append_item(function_item3)
    menu.append_item(function_item4)
    menu.append_item(function_item5)
    menu.append_item(submenu_reports)
    menu.show()


def tournament_console():
    global tournaments
    tournaments = []
    load_tournament()
    tournaments_menu = ConsoleMenu('Tournois')
    for tournament in tournaments:
        name = tournament.name
        item = FunctionItem(name, show_data, args=[tournament])
        tournaments_menu.append_item(item)
    tournaments_menu.append_item(FunctionItem('Supprimer un tournois',
                                              remove_tournament,
                                              should_exit=True))
    tournaments_menu.show()


# Modèles


class Tournament:
    '''
    Classe des tournois
    -name : Nom
    -place : Lieu
    -date : Date
    -cadence : "Blitz" par exemple
    -round : Nombre de rondes
    -rondes_instances : Liste des instances de rondes
    -players : Liste des joueurs qui participent
    -description : Description du tournois
    -turn : Ronde actuelle
    -opponents : Liste de couple [joueur1,joueur2] qui se sont
                 déjà rencontrés
    '''
    def __init__(self, name, place, date, cadence, description,
                 round=5, rondes_instances=[], players=players, turn=1,
                 opponents=[]):
        self.__init__
        self.name = name
        self.place = place
        self.date = date
        self.cadence = cadence
        self.round = round
        self.rondes_instances = rondes_instances
        self.players = players
        self.description = description
        self.turn = turn
        self.opponents = opponents

    def conditions_duo(self, player1, player2, round):
        '''Conditions à remplir pour que 2 joueurs soient appariés'''
        for match in round.match_list:
            if (match.player1.name == player1.name
                    or match.player2.name == player2.name):
                return False
            if (match.player2.name == player1.name
                    or match.player1.name == player2.name):
                return False
        in_opp = [player1.name, player2.name] in self.opponents
        in_opp2 = [player2.name, player1.name] in self.opponents
        return not (in_opp or in_opp2)

    def switzerland(self):
        '''Met en place le système d'appariement Suisse'''

        dash = 60*'-'
        # Si c'est la première ronde, on divise en deux groupes, on apparie
        if self.turn == 1:
            while True:
                name = str(input("Nom de la Ronde 1 : "))
                if name != 'exit':
                    round0 = Round(round_name=name, match_list=[], results=[])
                    break
                else:
                    print("Vous ne pouvez pas sortir d'un tournois non créer")
                    continue
            self.players = sorted(self.players,
                                  key=attrgetter('ranking'),
                                  reverse=True)
            first_part = []
            second_part = []

            for i in range(len(self.players)):
                if i+1 <= len(self.players)/2:
                    first_part.append(self.players[i])
                else:
                    second_part.append(self.players[i])

            for i in range(len(first_part)):
                match = Match(first_part[i], second_part[i])
                self.opponents.append(
                    [first_part[i].name, second_part[i].name]
                    )
                print(dash)
                print("{:^11s} {:<11s}     s'oppose à {:^11s} {:<11s}"
                      .format(first_part[i].name, first_part[i].surname,
                              second_part[i].name, second_part[i].surname))

                # On ajoute les matchs a la ronde 1
                round0.match_list.append(match)

            # On ajoute la ronde au tournois
            self.rondes_instances.append(round0)
            print(dash)

        else:
            # Si ce n'est pas la première ronde,
            # on trie et on apparie
            name = str(input("Nom de la {}ème ronde : "
                             .format(self.turn)))
            if name != 'exit':
                roundx = Round(round_name=name, match_list=[], results=[])
            else:
                del_tournament(self)
                self.save_tournament()
                exit()
            self.players = sorted(self.players,
                                  key=attrgetter('score', 'ranking'),
                                  reverse=True)

            # On apparie les joueurs par score
            actual = 0
            next = 1
            pb = 1
            opp = []
            while True:
                while (actual < len(self.players)
                        and actual + 1 < len(self.players)):
                    matched = False
                    while matched is False and (next < len(self.players)):
                        if self.conditions_duo(self.players[actual],
                                               self.players[next],
                                               roundx):
                            matched = True
                            match = Match(self.players[actual],
                                          self.players[next])

                            # On ajoute les matchs a la ronde x
                            roundx.match_list.append(match)
                            # On ajoute les adversaires à la liste
                            self.opponents.append(
                                [self.players[actual].name,
                                 self.players[next].name]
                                )
                            opp.append([self.players[actual],
                                        self.players[next]])
                        else:
                            next += 1

                    if next == actual + 1:
                        actual += 2
                        next = actual + 1
                    else:
                        actual += 1
                        next = actual + 1

                # Résoud le bug 1-2/3-4/5-6/7x8
                # Annule les infos du round et recommence
                # différement
                if len(roundx.match_list) != (len(self.players)/2):
                    roundx.match_list = []
                    for couple in opp:
                        [c1, c2] = couple
                        self.opponents.remove([c1.name, c2.name])
                    opp = []
                    next = pb + 1
                    pb += 1
                    actual = 0
                    continue
                for couple in opp:
                    [player_name1, player_name2] = couple
                    print(dash)
                    print("{:^11s} {:<11s}     s'oppose à {:^11s} {:<11s}"
                          .format(player_name1.name,
                                  player_name1.surname,
                                  player_name2.name,
                                  player_name2.surname))
                print(dash)
                break

            # On ajoute la ronde au tournois
            self.rondes_instances.append(roundx)

    def rounds_score(self):
        '''Affiche proprement en tableau les résultats
        des rondes passées du tournois

        Utilise la liste des joueurs et celle des instances de rondes'''

        dash = '-' * (11 * (len(self.rondes_instances)+1) + 15)

        self.players = sorted(self.players,
                              key=attrgetter('score', 'ranking'),
                              reverse=True)

        # Première ligne, on affiche l'en-tête : le nom de(s) ronde(s) et Total
        print('{:>10s}'.format(' '), end=' |')
        for round in self.rondes_instances:
            print('{:^11s}'.format(round.round_name), end='|')
        print('{:^11s}'.format('Total'), end='|')
        print('\n', dash)

        # On affiche le résultat de chaque joueur dans chaque ronde
        for player in self.players:
            round_index = 0
            for round in self.rondes_instances:
                for name_score in round.results:
                    if player.name == name_score[0] and round_index == 0:
                        print('{:<10s}{:>3s}{:^9s}'
                              .format(
                               name_score[0], ' | ', str(name_score[1])),
                              end=' | ')
                        round_index += 1
                    else:
                        if player.name == name_score[0]:
                            print('{:^9s}'
                                  .format(str(name_score[1])), end=' | ')
            print('{:^9s}'.format(str(player.score)), end=' | ')
            print('\n', dash)

    def start_tournament(self):
        '''Démarre le tournois et apparie'''
        while self.turn != self.round+1 and self.turn != len(players):
            if self.turn == 1:
                self.switzerland()
                exit_yorn = self.rondes_instances[0].end()
            else:
                self.switzerland()
                exit_yorn = self.rondes_instances[self.turn-1].end()
            if exit_yorn == 'exit':
                del_tournament(self)
                self.save_tournament()
                exit()

                # Nombre d'appariements max pour un nombre de personne
                # Pour 4 : (4*3)/2 = 6 couples possibles
            if (len(self.opponents)
                    == (len(self.players)*(len(self.players)-1))/2):
                self.end_tournament()
                break

            self.turn += 1
            # On affiche le tableau des scores
            self.rounds_score()
        self.end_tournament()

    def end_tournament(self):
        '''Messages et affichage de fin de tournois'''

        self.players = sorted(self.players,
                              key=attrgetter('score', 'ranking'),
                              reverse=True)
        print('Fin du tournois, voici le tableau des scores : ')
        self.rounds_score()
        i = 0
        if self.players[i].score == self.players[i+1].score:
            while (i+1 != len(self.players)) and (
                self.players[i].score == self.players[i+1].score
            ):
                if i == 0:
                    print('Félicitations aux gagnants {}, {}'
                          .format
                          (self.players[i].name, self.players[i+1].name),
                          end='')
                    i += 1
                else:
                    print(', ' + self.players[i+1].name, end='')
                    i += 1
        else:
            print('Félicitations au gagnant : {} {}'
                  .format(self.players[0].name, self.players[0].surname))
        input()
        del_tournament(self)
        self.save_tournament()
        for player in players:
            player.score = 0
        console_menu()

    def save_tournament(self):
        '''Sauvegarde le tournois actuel'''
        db = TinyDB('db.json')
        tournaments_table = db.table('tournaments')
        rounds_ser = []
        players_ser = []
        match_ser = []
        for ronde in self.rondes_instances:
            match_ser = []
            for match in ronde.match_list:
                serialized_match = {
                    'player1': match.player1.name,
                    'player2': match.player2.name
                }
                match_ser.append(serialized_match)
            serialized_round = {
                'round_name': ronde.round_name,
                'results': ronde.results,
                'match_list': match_ser
            }
            rounds_ser.append(serialized_round)

        for player in players:
            serialized_player = {
                'name': player.name,
                'surname': player.surname,
                'born': player.born,
                'gender': player.gender,
                'ranking': player.ranking,
                'score': 0
                }
            players_ser.append(serialized_player)
        serialized_tournament = {
            'name': self.name,
            'place': self.place,
            'date': self.date,
            'cadence': self.cadence,
            'round': self.round,
            'rondes_instances': rounds_ser,
            'players': players_ser,
            'description': self.description,
            'turn': self.turn,
            'opponents': self.opponents
            }
        tournaments_table.insert(serialized_tournament)


class Round:
    '''
    Classe Round:
    -match_list : La liste des matchs de la ronde
    -time_start : L'heure de début
    -time_end : L'heure de fin
    -results : Une lise de [Joueur,Score] des résultats des matchs
    -round_name : Nom de la ronde
    '''
    def __init__(self, round_name, results=[], match_list=[]):
        self.match_list = match_list
        self.time_start = time.strftime('%H:%M')
        print('Heure de début de ronde : {}'.format(self.time_start))
        self.time_end = None
        self.results = results
        self.round_name = round_name

    def end(self):
        '''Demande le résultat de tout les matchs de la ronde actuelle'''
        input('Appuyez sur une entrée pour rentrer les résultats...\n')
        for match in self.match_list:
            already_played = False
            for result in self.results:
                [name, score] = result
                if name == match.player1.name or name == match.player2.name:
                    already_played = True
            if not already_played:
                (result_1, result_2) = match.result()
                if result_1 == -1:
                    return 'exit'
                self.results.append([match.player1.name, result_1])
                self.results.append([match.player2.name, result_2])
        self.time_end = time.strftime('%H:%M')
        print('Heure de fin de ronde : {}'.format(self.time_end))


class Match:
    '''
    Classe Match:
    -player1 : Joueur 1
    -player2 : Joueur 2
    '''
    def __init__(self, player1, player2):
        self.score1 = player1.score
        self.score2 = player2.score
        self.player1 = player1
        self.player2 = player2
        tuple1 = [player1, self.score1]
        tuple2 = [player2, self.score2]
        self.match = (tuple1, tuple2)

    def result(self):
        '''Demande le résultat du match actuel'''
        while True:
            result = str(input("Entrez le résultat du match "
                               "entre {} et {} "
                               "('1/2', '1-0' ou '0-1') \n"
                               .format(self.player1.name, self.player2.name)))
            if result == "1/2":
                self.player1.score += 0.5
                self.player2.score += 0.5
                return (0.5, 0.5)
            elif result == "1-0":
                self.player1.score += 1
                return (1, 0)
            elif result == '0-1':
                self.player2.score += 1
                return (0, 1)
            elif result == 'exit':
                return(-1, -1)
            else:
                print("Ce n'est pas un résultat valide, réessayez")
                continue


class Player:
    '''Classe Joueur explicite'''
    def __init__(self, name, surname, born, gender, ranking, score=0):
        self.name = name
        self.surname = surname
        self.born = born
        self.gender = gender
        self.ranking = ranking
        self.score = score


# Contrôleurs

def save_players():
    '''Sauvegarde les joueurs de la liste "players"'''

    global players
    db = TinyDB('db.json')
    players_table = db.table('players')
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


def add_player():
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
    players.append(new)
    save_players()


def del_player():
    '''Supprime un joueur si il n'est pas lié
    à un tournois en base de donnée'''

    can_delete = True
    while True:
        db = TinyDB('db.json')
        players_table = db.table('players')
        names = []
        for player in players:
            names.append(player.name)
        menu = SelectionMenu(names, 'Quel joueur supprimer ?')
        menu.show()
        menu.join()
        selection = menu.selected_option
        if selection == len(players):
            menu.exit()
        else:
            for tournament in tournaments:
                for player in tournament.players:
                    if player.name == players[selection].name:
                        print('Vous ne pouvez pas supprimer ce joueur, '
                              'il fait parti du tournois : {}'
                              .format(tournament.name))
                        print('Supprimez le tournois dans la base de donnée '
                              'pour supprimer ce joueur')
                        input()
                        can_delete = False
            if can_delete:
                players_table.remove(where('name') == names[selection])
                players.pop(selection)
            else:
                continue
        break


def load_players():
    '''Charge tout les joueurs vers la liste "players"
    depuis la base de donnée'''

    db = TinyDB('db.json')
    players_table = db.table('players')
    serialized_players = players_table.all()
    for serial in serialized_players:
        name = serial['name']
        surname = serial['surname']
        born = serial['born']
        gender = serial['gender']
        ranking = serial['ranking']
        score = serial['score']
        players.append(Player(name, surname, born, gender, ranking, score))


def load_tournament():
    '''Charge les tournois vers la liste tournaments
    depuis la base de donnée'''

    db = TinyDB('db.json')
    tournaments_table = db.table('tournaments')
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
                for player in players:
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
        tournaments.append(Tournament(name, place,
                                      date, cadence,
                                      description, round,
                                      round_no_ser, players_no_ser,
                                      turn, opponents))


def remove_tournament():
    '''Supprime un tournois de la base de donnée avec un affichage console'''

    global tournaments
    names = []
    for tournament in tournaments:
        names.append(tournament.name)
    menu = SelectionMenu(names, 'Quel tournois à supprimer ?')
    menu.show()
    selection = menu.selected_option
    db = TinyDB('db.json')
    table = db.table('tournaments')
    try:
        table.remove(where('name') == names[selection])
        tournaments.pop(selection)
    except IndexError:
        pass
    tournament_console()


def del_tournament(tournament):
    '''Supprime un tournois de la base de donnée sans affichage console'''

    db = TinyDB('db.json')
    table = db.table('tournaments')
    table.remove(where('name') == tournament.name)
    for i in range(len(tournaments)-1):
        if tournaments[i].name == tournament.name:
            tournaments.pop(i)


def resume_tournament():
    '''Permet de reprendre un tournois'''

    names = []
    selections = []
    global tournaments
    tournaments = []
    load_tournament()
    for tournament in tournaments:
        finish = True
        for round in tournament.rondes_instances:
            if len(round.results) != len(tournament.players):
                finish = False
        if len(tournament.rondes_instances) != tournament.round or not finish:
            names.append(tournament.name)
            selections.append(tournament)
    menu = SelectionMenu(names, 'Quel tournois continuer ?')
    menu.should_exit = True
    menu.show()
    selection = menu.selected_option
    try:
        dash = 50*'-'
        to_continue = selections[selection]
        for round in to_continue.rondes_instances:
            for result in round.results:
                [name, score] = result
                for player in to_continue.players:
                    if player.name == name:
                        player.score += score
        for round in to_continue.rondes_instances:
            if (len(round.results) != len(to_continue.players)
               or (len(round.results) == 0 and round.round_name is not None)):
                print('Reprise au round : {}'.format(round.round_name))
                for match in round.match_list:
                    print(dash)
                    print('{:^13}{:^13}{:^13}'.format(
                                                    match.player1.name,
                                                    "s'oppose à",
                                                    match.player2.name))
                print(dash, '\n')
                exit_yor = round.end()
                del_tournament(to_continue)
                to_continue.save_tournament()
                if exit_yor == 'exit':
                    exit()
                else:
                    to_continue.turn += 1
                    to_continue.start_tournament()
            elif (len(to_continue.rondes_instances) != to_continue.round
                  and round == to_continue.rondes_instances[-1]):
                if len(round.results) < len(to_continue.players):
                    round.end()
                else:
                    to_continue.start_tournament()
    except IndexError:
        pass


def tournaments_informations():
    '''Créer un tournois'''

    if len(players) < 4:
        print('Trop peu de gens pour faire un tournois...')
        input()
        console_menu()
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

# main.py
def start():
    '''Démarre le programme'''

    load_players()
    load_tournament()
    console_menu()

