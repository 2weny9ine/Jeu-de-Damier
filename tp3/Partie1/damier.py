# Auteurs: Mohammed Yacine Rouainia
import sys

sys.path.append("C:/Users/2weny9ine/Desktop/study/IFT 1004 programmation intro/tp3")

from tp3.Partie1.piece import Piece
from tp3.Partie1.position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes."""
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        if 0 <= (position.ligne) <= 7 and 0 <= (position.colonne) <= 7:
            return True
        else:
            return False

    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)
        if piece is None:
            return False  # to check if the position_piece not empty
        if (
            self.position_est_dans_damier(position_cible)
            and self.recuperer_piece_a_position(position_cible)
            is None  # to check if the position_cible exists and it's empty
        ):
            if piece.est_pion() and piece.est_blanche():
                if position_cible in Position.positions_diagonales_haut(position_piece):
                    return True
                else:
                    return False

            elif piece.est_pion() and piece.est_noire():
                if position_cible in Position.positions_diagonales_bas(position_piece):
                    return True
                else:
                    return False
            elif piece.est_dame():
                if position_cible in (
                    Position.positions_diagonales_bas(position_piece)
                    + Position.positions_diagonales_haut(position_piece)
                ):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """
        piece = self.recuperer_piece_a_position(position_piece)
        if piece is None:
            return False  # to check if the position_piece not empty
        elif (
            self.position_est_dans_damier(position_cible)
            and self.recuperer_piece_a_position(position_cible)
            is None  # to check if the position_cible exists and it's empty
        ):
            if position_cible in Position.quatre_positions_sauts(position_piece):
                if (
                    position_cible.ligne < position_piece.ligne
                    and position_cible.colonne > position_piece.colonne
                ):
                    piece_a_manger = self.recuperer_piece_a_position(
                        Position(position_piece.ligne - 1, position_piece.colonne + 1)
                    )
                elif (
                    position_cible.ligne < position_piece.ligne
                    and position_cible.colonne < position_piece.colonne
                ):
                    piece_a_manger = self.recuperer_piece_a_position(
                        Position(position_piece.ligne - 1, position_piece.colonne - 1)
                    )
                elif (
                    position_cible.ligne > position_piece.ligne
                    and position_cible.colonne > position_piece.colonne
                ):
                    piece_a_manger = self.recuperer_piece_a_position(
                        Position(position_piece.ligne + 1, position_piece.colonne + 1)
                    )
                elif (
                    position_cible.ligne > position_piece.ligne
                    and position_cible.colonne < position_piece.colonne
                ):
                    piece_a_manger = self.recuperer_piece_a_position(
                        Position(position_piece.ligne + 1, position_piece.colonne - 1)
                    )
            else:
                return False
            if piece_a_manger is None:
                return False
            elif piece.est_blanche() and piece_a_manger.est_noire():
                return True
            elif piece.est_noire() and piece_a_manger.est_blanche():
                return True
            else:
                return False
        else:
            return False

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        deplacement_possible = position_piece.quatre_positions_diagonales()
        if self.piece_peut_se_deplacer_vers(position_piece, deplacement_possible[0]):
            return True
        elif self.piece_peut_se_deplacer_vers(position_piece, deplacement_possible[1]):
            return True
        elif self.piece_peut_se_deplacer_vers(position_piece, deplacement_possible[2]):
            return True
        elif self.piece_peut_se_deplacer_vers(position_piece, deplacement_possible[3]):
            return True
        else:
            return False

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """
        sauts_possible = position_piece.quatre_positions_sauts()
        if self.piece_peut_sauter_vers(position_piece, sauts_possible[0]):
            return True
        elif self.piece_peut_sauter_vers(position_piece, sauts_possible[1]):
            return True
        elif self.piece_peut_sauter_vers(position_piece, sauts_possible[2]):
            return True
        elif self.piece_peut_sauter_vers(position_piece, sauts_possible[3]):
            return True
        else:
            return False

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """
        peut_deplacer = False
        positions = list(self.cases.keys())
        if couleur == "blanc":
            i = 0
            while not peut_deplacer and i < len(positions):
                if self.cases[positions[i]].est_blanche():
                    if self.piece_peut_se_deplacer(positions[i]):
                        peut_deplacer = True
                    i = i + 1
        elif couleur == "noir":
            i = 0
            while not peut_deplacer and i < len(positions):
                if self.cases[positions[i]].est_noire():
                    if self.piece_peut_se_deplacer(positions[i]):
                        peut_deplacer = True
                i = i + 1
        if peut_deplacer:
            return True
        else:
            return False

    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """
        peut_sauter = False
        positions = list(self.cases.keys())
        if couleur == "blanc":
            i = 0
            while not peut_sauter and i < len(positions):
                if self.cases[positions[i]].est_blanche():
                    if self.piece_peut_faire_une_prise(positions[i]):
                        peut_sauter = True
                i = i + 1
        elif couleur == "noir":
            i = 0
            while not peut_sauter and i < len(positions):
                if self.cases[positions[i]].est_noire():
                    if self.piece_peut_faire_une_prise(positions[i]):
                        peut_sauter = True
                i = i + 1
        if peut_sauter:
            return True
        else:
            return False

    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        piece_a_deplacer = self.recuperer_piece_a_position(position_source)
        if self.piece_peut_se_deplacer(
            position_source
        ) or self.piece_peut_faire_une_prise(position_source):
            if self.piece_peut_se_deplacer_vers(position_source, position_cible):
                self.cases[position_cible] = piece_a_deplacer
                self.cases.pop(position_source)
                if piece_a_deplacer.est_pion():
                    if piece_a_deplacer.est_blanche():
                        if position_cible.ligne == 0 and position_cible.colonne in (
                            1,
                            3,
                            5,
                            7,
                        ):
                            self.cases[position_cible].promouvoir()
                    elif piece_a_deplacer.est_noire():
                        if position_cible.ligne == 7 and position_cible.colonne in (
                            0,
                            2,
                            4,
                            6,
                        ):
                            self.cases[position_cible].promouvoir()
                return "ok"
            if self.piece_peut_sauter_vers(position_source, position_cible):
                self.cases[position_cible] = piece_a_deplacer
                self.cases.pop(position_source)
                if position_cible == position_source.quatre_positions_sauts()[0]:
                    position_mange = Position(
                        position_source.ligne - 1, position_source.colonne - 1
                    )
                elif position_cible == position_source.quatre_positions_sauts()[1]:
                    position_mange = Position(
                        position_source.ligne - 1, position_source.colonne + 1
                    )
                elif position_cible == position_source.quatre_positions_sauts()[2]:
                    position_mange = Position(
                        position_source.ligne + 1, position_source.colonne - 1
                    )
                elif position_cible == position_source.quatre_positions_sauts()[3]:
                    position_mange = Position(
                        position_source.ligne + 1, position_source.colonne + 1
                    )
                self.cases.pop(position_mange)
                if piece_a_deplacer.est_pion():
                    if piece_a_deplacer.est_blanche():
                        if position_cible.ligne == 0 and position_cible.colonne in (
                            1,
                            3,
                            5,
                            7,
                        ):
                            self.cases[position_cible].promouvoir()
                    elif piece_a_deplacer.est_noire():
                        if position_cible.ligne == 7 and position_cible.colonne in (
                            0,
                            2,
                            4,
                            6,
                        ):
                            self.cases[position_cible].promouvoir()
                return "prise"
            else:
                return "erreur"
        else:
            return "erreur"

    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i) + "| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)]) + " | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()
    assert un_damier.position_est_dans_damier(position=Position(5, 0)) == True
    assert un_damier.position_est_dans_damier(position=Position(-1, 0)) == False
    assert un_damier.position_est_dans_damier(position=Position(0, 8)) == False
    assert (
        un_damier.piece_peut_se_deplacer_vers(
            position_piece=Position(7, 1), position_cible=Position(6, 0)
        )
        == False  # position_piece vide
    )
    assert (
        un_damier.piece_peut_se_deplacer_vers(
            position_piece=Position(6, 1), position_cible=Position(5, 2)
        )
        == False  # position_cible occupée
    )
    assert (
        un_damier.piece_peut_se_deplacer_vers(
            position_piece=Position(5, 0), position_cible=Position(4, 1)
        )
        == True  # position_cible vide et piece de type pion et couleur blanc
    )
    assert (
        un_damier.piece_peut_se_deplacer_vers(
            position_piece=Position(2, 1), position_cible=Position(3, 0)
        )
        == True  # position_cible vide et piece de type pion et couleur noire
    )
    assert (
        un_damier.piece_peut_se_deplacer_vers(
            position_piece=Position(2, 1), position_cible=Position(2, 2)
        )
        == False  # position_cible pas dans diagonale
    )
    print(un_damier)
    un_damier.cases[Position(4, 3)] = Piece(couleur="noir", type_de_piece="pion")
    # we added a pion noir to test piece_peut_sauter_vers
    print(un_damier)
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(5, 2), position_cible=Position(3, 4)
        )
        == True
    )
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(5, 4), position_cible=Position(3, 6)
        )
        == False
    )
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(5, 4), position_cible=Position(3, 2)
        )
        == True
    )
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(5, 4), position_cible=Position(3, 2)
        )
        == True
    )
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(5, 3), position_cible=Position(3, 3)
        )
        == False
    )
    un_damier.cases[Position(3, 6)] = Piece(couleur="blanc", type_de_piece="pion")
    # we added a pion blanc to test piece_peut_sauter_vers
    print(un_damier)
    assert (
        un_damier.piece_peut_sauter_vers(
            position_piece=Position(2, 7), position_cible=Position(4, 5)
        )
        == True
    )
    assert un_damier.piece_peut_se_deplacer(position_piece=Position(4, 3)) == False
    assert un_damier.piece_peut_se_deplacer(position_piece=Position(5, 2)) == True
    assert un_damier.piece_peut_se_deplacer(position_piece=Position(7, 3)) == False
    assert un_damier.piece_peut_se_deplacer(position_piece=Position(0, 1)) == False

    assert un_damier.piece_peut_faire_une_prise(position_piece=Position(0, 1)) == False
    assert un_damier.piece_peut_faire_une_prise(position_piece=Position(2, 2)) == False
    assert un_damier.piece_peut_faire_une_prise(position_piece=Position(5, 2)) == True
    assert un_damier.piece_peut_faire_une_prise(position_piece=Position(2, 7)) == True
    assert un_damier.piece_de_couleur_peut_se_deplacer(couleur="blanc") == True
    damier_2 = Damier()
    print(damier_2)
    assert damier_2.deplacer(Position(5, 0), Position(4, 1)) == "ok"
    print(damier_2)
    assert damier_2.deplacer(Position(5, 0), Position(4, 1)) == "erreur"
    print(damier_2)
    assert damier_2.deplacer(Position(2, 3), Position(3, 2)) == "ok"
    print(damier_2)
    assert damier_2.deplacer(Position(4, 1), Position(2, 3)) == "prise"
    print(damier_2)
    assert damier_2.deplacer(Position(1, 4), Position(3, 2)) == "prise"
    print(damier_2)
    assert damier_2.deplacer(Position(3, 2), Position(2, 3)) == "erreur"
    print(damier_2)
    assert damier_2.deplacer(Position(5, 4), Position(4, 3)) == "ok"
    print(damier_2)
    assert damier_2.deplacer(Position(4, 3), Position(3, 4)) == "ok"
    print(damier_2)
    assert damier_2.deplacer(Position(3, 4), Position(2, 3)) == "ok"
    print(damier_2)
    assert damier_2.deplacer(Position(3, 2), Position(1, 4)) == "prise"
    print(damier_2)
    print("Test unitaires passés avec succès!")
    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
