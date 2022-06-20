import time

from tinydb import TinyDB, where


class Model:
    """Database class.
    Encapsulate TinyDB usage and references to tables (that can be called
    from the controller).
    """

    def __init__(self, path):

        # Private database.
        # There is no need to access it directly outside the model.
        self._db = TinyDB(path)

        # These ones are public.
        self.players_table = self._db.table("players")
        self.tournaments_table = self._db.table("tournaments")

    def delete_tournament(self, tournament):
        """Delete a tournament."""
        self.tournaments_table.remove(where("name") == tournament.name)

    def delete_player(self, player):
        """Delete a player."""
        self.players_table.remove(where("name") == player.name)


class Tournament:
    """
    Classe des tournois
    -name : Nom
    -place : Lieu
    -date : Date
    -cadence : "Blitz" par exemple
    -round : Nombre de rondes
    -rounds : Liste des instances de rondes
    -players : Liste des joueurs qui participent
    -description : Description du tournois
    -turn : Ronde actuelle
    -opponents : Liste de couple [joueur1,joueur2] qui se sont
                 déjà rencontrés
    """

    def __init__(
        self,
        name,
        place,
        date,
        cadence,
        description,
        round_count=5,
        rounds=None,
        players=None,
        turn=1,
        opponents=None,
    ):
        self.__init__
        self.name = name
        self.place = place
        self.date = date
        self.cadence = cadence
        self.round_count = round_count
        self.players = players or []
        self.rounds = rounds or []
        self.opponents = opponents or []
        self.description = description
        self.turn = turn


class Round:
    """
    Classe Round:
    -match_list : La liste des matchs de la ronde
    -time_start : L'heure de début
    -time_end : L'heure de fin
    -results : Une lise de [Joueur,Score] des résultats des matchs
    -round_name : Nom de la ronde
    """

    def __init__(self, round_name, results=None, match_list=None):
        self.match_list = match_list or []
        self.time_start = time.strftime("%H:%M")
        self.time_end = None
        self.results = results or []
        self.round_name = round_name

    def start(self):
        print('Heure de début de ronde : {}'.format(self.time_start))

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
        self.time_end = time.strftime("%H:%M")
        print("Heure de fin de ronde : {}".format(self.time_end))


class Match:
    """
    Classe Match:
    -player1 : Joueur 1
    -player2 : Joueur 2
    """

    def __init__(self, player1, player2):
        self.score1 = player1.score
        self.score2 = player2.score
        self.player1 = player1
        self.player2 = player2
        tuple1 = [player1, self.score1]
        tuple2 = [player2, self.score2]
        self.match = (tuple1, tuple2)

    def result(self):
        """Demande le résultat du match actuel"""
        while True:
            result = str(
                input(
                    "Entrez le résultat du match "
                    "entre {} et {} "
                    "('1/2', '1-0' ou '0-1') \n".format(
                        self.player1.name, self.player2.name
                    )
                )
            )
            if result == "1/2":
                self.player1.score += 0.5
                self.player2.score += 0.5
                return (0.5, 0.5)
            elif result == "1-0":
                self.player1.score += 1
                return (1, 0)
            elif result == "0-1":
                self.player2.score += 1
                return (0, 1)
            elif result == "exit":
                return (-1, -1)
            else:
                print("Ce n'est pas un résultat valide, réessayez")
                continue


class Player:
    """Classe Joueur explicite"""

    def __init__(self, name, surname, born, gender, ranking, score=0):
        self.name = name
        self.surname = surname
        self.born = born
        self.gender = gender
        self.ranking = ranking
        self.score = score