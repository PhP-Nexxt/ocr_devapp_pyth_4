import time

from operator import attrgetter
from .models import Match, Round


class TournamentProcessor:
    def __init__(self, controller, tournament):
        self._controller = controller
        self._tournament = tournament

    def conditions_duo(self, player1, player2, round_):
        """Conditions à remplir pour que 2 joueurs soient appariés"""
        for match in round_.match_list:
            if (
                match.player1.name == player1.name
                or match.player2.name == player2.name
            ):
                return False
            if (
                match.player2.name == player1.name
                or match.player1.name == player2.name
            ):
                return False
        in_opp = [player1.name, player2.name] in self._tournament.opponents
        in_opp2 = [player2.name, player1.name] in self._tournament.opponents
        return not (in_opp or in_opp2)

    def switzerland(self):
        """Met en place le système d'appariement Suisse"""

        dash = 60 * "-"
        # Si c'est la première ronde, on divise en deux groupes, on apparie
        name = f"Ronde {self._tournament.turn}"
        if self._tournament.turn == 1:
            
            round0 = Round(round_name=name, match_list=[], results=[])
            round0.start()
            self._tournament.players = sorted(
                self._tournament.players,
                key=attrgetter("ranking"),
                reverse=True,
            )
            first_part = []
            second_part = []

            for i in range(len(self._tournament.players)):
                if i + 1 <= len(self._tournament.players) / 2:
                    first_part.append(self._tournament.players[i])
                else:
                    second_part.append(self._tournament.players[i])

            for i in range(len(first_part)):
                match = Match(first_part[i], second_part[i])
                self._tournament.opponents.append(
                    [first_part[i].name, second_part[i].name]
                )
                print(dash)
                self.display_opponents(first_part[i], second_part[i])

                # On ajoute les matchs a la ronde 1
                round0.match_list.append(match)

            # On ajoute la ronde au tournois
            self._tournament.rounds.append(round0)
            print(dash)

        else:
            # Si ce n'est pas la première ronde,
            # on trie et on apparie
            roundx = Round(round_name=name, match_list=[], results=[])
            roundx.start()
            
            self._tournament.players = sorted(
                self._tournament.players,
                key=attrgetter("score", "ranking"),
                reverse=True,
            )

            # On apparie les joueurs par score
            actual = 0
            next_ = 1
            pb = 1
            opp = []
            players = self._tournament.players
            while True:
                while actual < len(players) and actual + 1 < len(players):
                    matched = False
                    while matched is False and (next_ < len(players)):
                        if self.conditions_duo(
                            players[actual],
                            players[next_],
                            roundx,
                        ):
                            matched = True
                            match = Match(
                                players[actual],
                                players[next_],
                            )

                            # On ajoute les matchs a la ronde x
                            roundx.match_list.append(match)
                            # On ajoute les adversaires à la liste
                            self._tournament.opponents.append(
                                [
                                    players[actual].name,
                                    players[next_].name,
                                ]
                            )
                            opp.append(
                                [players[actual], players[next_]]
                            )
                        else:
                            next_ += 1

                    if next_ == actual + 1:
                        actual += 2
                        next_ = actual + 1
                    else:
                        actual += 1
                        next_ = actual + 1

                # Résoud le bug 1-2/3-4/5-6/7x8
                # Annule les infos du round et recommence
                # différement
                if len(roundx.match_list) != (len(players) / 2):
                    roundx.match_list = []
                    for couple in opp:
                        [c1, c2] = couple
                        self._tournament.opponents.remove([c1.name, c2.name])
                    opp = []
                    next_ = pb + 1
                    pb += 1
                    actual = 0
                    continue
                for couple in opp:
                    [player_name1, player_name2] = couple
                    print(dash)
                    self.display_opponents(player_name1, player_name2)
                print(dash)
                break

            # On ajoute la ronde au tournois
            self._tournament.rounds.append(roundx)
        shall_exit = input("Voulez-vous continuer ? (O/N)\n")
        if shall_exit.lower() == "n":   
            self._controller.del_tournament(self._tournament)
            self.save_tournament()
            raise SystemExit(0)  # Not good.
            
        

    def display_opponents(self, player1, player2):
        print(
            "{:^11s} {:<11s}     s'oppose à {:^11s} {:<11s}".format(
                player1.name,
                player1.surname,
                player2.name,
                player2.surname,
            )
        )

    def rounds_score(self):
        """Affiche proprement en tableau les résultats
        des rondes passées du tournois

        Utilise la liste des joueurs et celle des instances de rondes"""

        dash = "-" * (11 * (len(self._tournament.rounds) + 1) + 15)

        self._tournament.players = sorted(
            self._tournament.players,
            key=attrgetter("score", "ranking"),
            reverse=True,
        )

        # Première ligne, on affiche l'en-tête : le nom de(s) ronde(s) et Total
        print("{:>10s}".format(" "), end=" |")
        for round_ in self._tournament.rounds:
            print("{:^11s}".format(round_.round_name), end="|")
        print("{:^11s}".format("Total"), end="|")
        print("\n", dash)

        # On affiche le résultat de chaque joueur dans chaque ronde
        for player in self._tournament.players:
            round_index = 0
            for round_ in self._tournament.rounds:
                for name_score in round_.results:
                    if player.name == name_score[0] and round_index == 0:
                        print(
                            "{:<10s}{:>3s}{:^9s}".format(
                                name_score[0], " | ", str(name_score[1])
                            ),
                            end=" | ",
                        )
                        round_index += 1
                    else:
                        if player.name == name_score[0]:
                            print(
                                "{:^9s}".format(str(name_score[1])), end=" | "
                            )
            print("{:^9s}".format(str(player.score)), end=" | ")
            print("\n", dash)

    def process(self):
        self._start_tournament()
        self._end_tournament()

    def _start_tournament(self):
        """Démarre le tournois et apparie"""
        players = self._tournament.players
        while (
            self._tournament.turn != self._tournament.round_count + 1
            and self._tournament.turn != len(players)
        ):
            if self._tournament.turn == 1:
                self.switzerland()
                exit_yorn = self._tournament.rounds[0].end()
            else:
                self.switzerland()
                exit_yorn = self._tournament.rounds[
                    self._tournament.turn - 1
                ].end()
            if exit_yorn == "exit":
                self._controller.del_tournament(self._tournament)
                self.save_tournament()
                raise SystemExit(0)  # Should not be here.

                # Nombre d'appariements max pour un nombre de personne
                # Pour 4 : (4*3)/2 = 6 couples possibles
            if (
                len(self._tournament.opponents)
                == (len(players) * (len(players) - 1)) / 2
            ):
                break

            self._tournament.turn += 1
            # On affiche le tableau des scores
            self.rounds_score()

    def _end_tournament(self):
        """Messages et affichage de fin de tournois"""
        players = sorted(
            self._tournament.players,
            key=attrgetter("score", "ranking"),
            reverse=True,
        )
        print("Fin du tournois, voici le tableau des scores : ")
        self.rounds_score()
        i = 0
        if (
            players[i].score
            == players[i + 1].score
        ):
            while (i + 1 != len(players)) and (
                players[i].score
                == players[i + 1].score
            ):
                if i == 0:
                    print(
                        "Félicitations aux gagnants {}, {}".format(
                            players[i].name,
                            players[i + 1].name
                        ),
                        end="",
                    )
                    i += 1
                else:
                    print(", " + players[i + 1].name, end="")
                    i += 1
        else:
            print(
                "Félicitations au gagnant : {} {}".format(
                    players[0].name,
                    players[0].surname
                )
            )
        input()
        self._controller.del_tournament(self._tournament)
        self.save_tournament()
        for player in players:
            player.score = 0
        # console_menu()

    def get_serialized_tournament(self):
        """Retourne un dictionnaire du tournoi."""
        rounds_ser = []
        players_ser = []
        match_ser = []
        for round_ in self._tournament.rounds:
            match_ser = []
            for match in round_.match_list:
                serialized_match = {
                    "player1": match.player1.name,
                    "player2": match.player2.name,
                }
                match_ser.append(serialized_match)
            serialized_round = {
                "round_name": round_.round_name,
                "results": round_.results,
                "match_list": match_ser,
            }
            rounds_ser.append(serialized_round)

        for player in self._tournament.players:
            serialized_player = {
                "name": player.name,
                "surname": player.surname,
                "born": player.born,
                "gender": player.gender,
                "ranking": player.ranking,
                "score": 0,
            }
            players_ser.append(serialized_player)
        return {
            "name": self._tournament.name,
            "place": self._tournament.place,
            "date": self._tournament.date,
            "cadence": self._tournament.cadence,
            "round_count": self._tournament.round_count,
            "rounds": rounds_ser,
            "players": players_ser,
            "description": self._tournament.description,
            "turn": self._tournament.turn,
            "opponents": self._tournament.opponents,
        }

    def save_tournament(self):
        self._controller._save_current_tournament(
            self.get_serialized_tournament()
        )


class RoundProcessor:
    def __init__(self, round_):
        self._round = round_

    def start(self):
        print("Heure de début de ronde : {}".format(self._round.time_start))

    def end(self):
        """Demande le résultat de tout les matchs de la ronde actuelle"""
        input("Appuyez sur une entrée pour rentrer les résultats...\n")
        for match in self.match_list:
            already_played = False
            for result in self.results:
                [name, score] = result
                if name == match.player1.name or name == match.player2.name:
                    already_played = True
            if not already_played:
                (result_1, result_2) = match.result()
                if result_1 == -1:
                    return "exit"
                self.results.append([match.player1.name, result_1])
                self.results.append([match.player2.name, result_2])
        self.round_.time_end = time.strftime("%H:%M")
        print("Heure de fin de ronde : {}".format(self.time_end))