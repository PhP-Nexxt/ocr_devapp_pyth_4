from operator import attrgetter
import time

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
                 round=5, rondes_instances=[], players=None, turn=1,
                 opponents=[]):
        self.__init__
        self.name = name
        self.place = place
        self.date = date
        self.cadence = cadence
        self.round = round
        self.rondes_instances = rondes_instances
        if players is None:
            self.players = []
        else:
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