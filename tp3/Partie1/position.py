# Auteurs: Messaouda Yassamine Safer Tabi


class Position:
    """Une position à deux coordonnées: ligne et colonne. La convention utilisée est celle de la notation matricielle :
    le coin supérieur gauche d'une matrice est dénoté (0, 0) (ligne 0 et colonne 0). On additionne une unité de colonne
    lorsqu'on se déplace vers la droite, et une unité de ligne lorsqu'on se déplace vers le bas.

    +-------+-------+-------+-------+
    | (0,0) | (0,1) | (0,2) |  ...  |
    | (1,0) | (1,1) | (1,2) |  ...  |
    | (2,0) | (2,1) | (2,2) |  ...  |
    |  ...  |  ...  |  ...  |  ...  |
    +-------+-------+-------+-------+

    Attributes:
        ligne (int): La ligne associée à la position.
        colonne (int): La colonne associée à la position

    """

    def __init__(self, ligne, colonne):
        """Constructeur de la classe Position. Initialise les deux attributs de la classe.

        Args:
            ligne (int): La ligne à considérer dans l'instance de Position.
            colonne (int): La colonne à considérer dans l'instance de Position.

        """
        self.ligne = int(ligne)
        self.colonne = int(colonne)

    def positions_diagonales_bas(self):
        """Retourne une liste contenant les deux positions diagonales bas à partir de la position actuelle.

        Note:
            Dans cette méthode et les prochaines, vous n'avez pas à valider qu'une position est "valide", car dans le
            contexte de cette classe toutes les positions (même négatives) sont permises.

        Returns:
            list: La liste des deux positions.

        """
        return [
            Position(self.ligne + 1, self.colonne - 1),
            Position(self.ligne + 1, self.colonne + 1),
        ]

    def positions_diagonales_haut(self):
        """Retourne une liste contenant les deux positions diagonales haut à partir de la position actuelle.

        Returns:
            list: La liste des deux positions.

        """

        return [
            Position(self.ligne - 1, self.colonne - 1),
            Position(self.ligne - 1, self.colonne + 1),
        ]

    def quatre_positions_diagonales(self):
        """Retourne une liste contenant les quatre positions diagonales à partir de la position actuelle.

        Returns:
            list: La liste des quatre positions.

        """
        return self.positions_diagonales_haut() + self.positions_diagonales_bas()

    def quatre_positions_sauts(self):
        """Retourne une liste contenant les quatre "sauts" diagonaux à partir de la position actuelle. Les positions
        retournées sont donc en diagonale avec la position actuelle, mais a une distance de 2.

        Returns:
            list: La liste des quatre positions.

        """
        return [
            Position(self.ligne - 2, self.colonne - 2),
            Position(self.ligne - 2, self.colonne + 2),
            Position(self.ligne + 2, self.colonne - 2),
            Position(self.ligne + 2, self.colonne + 2),
        ]

    # try this if that one doesn't work :
    # return [Position(self.ligne + i, self.colonne + j) for i in [-2, 2] for j in [-2, 2]]

    def __eq__(self, other):
        """Méthode spéciale indiquant à Python comment vérifier si deux positions sont égales. On compare simplement
        la ligne et la colonne de l'objet actuel et de l'autre objet.

        """
        return (self.ligne, self.colonne) == (other.ligne, other.colonne)

    def __repr__(self):
        """Méthode spéciale indiquant à Python comment représenter une instance de Position par une chaîne de
        caractères. Notamment utilisé pour imprimer une position à l'écran.

        """
        return f"({self.ligne}, {self.colonne})"

    def __hash__(self):
        """Méthode spéciale indiquant à Python comment "hasher" une Position. Cette méthode est nécessaire si on veut
        utiliser une classe que nous avons définie nous mêmes comme clé d'un dictionnaire.
        Les étudiants(es) curieux(ses) peuvent consulter wikipédia pour en savoir plus:
            https://fr.wikipedia.org/wiki/Fonction_de_hachage

        """
        return hash((self.ligne, self.colonne))


if __name__ == "__main__":
    print('Test unitaires de la classe "Position"...')
    # Test position
    pos1 = Position(2, 3)
    assert pos1.ligne == 2
    assert pos1.colonne == 3
    pos2 = Position(3, 4)
    assert pos2.ligne == 3
    assert pos2.colonne == 4

    # Test positions_diagonales_bas
    diagonales_bas = pos1.positions_diagonales_bas()
    assert diagonales_bas == [Position(3, 2), Position(3, 4)]
    diagonales_bas = pos2.positions_diagonales_bas()
    assert diagonales_bas == [Position(4, 3), Position(4, 5)]

    # Test positions_diagonales_haut
    diagonales_haut = pos1.positions_diagonales_haut()
    assert diagonales_haut == [Position(1, 2), Position(1, 4)]
    diagonales_haut = pos2.positions_diagonales_haut()
    assert diagonales_haut == [Position(2, 3), Position(2, 5)]

    # Test quatre_positions_diagonales
    quatre_diagonales = pos1.quatre_positions_diagonales()
    assert quatre_diagonales == [
        Position(1, 2),
        Position(1, 4),
        Position(3, 2),
        Position(3, 4),
    ]
    quatre_diagonales = pos2.quatre_positions_diagonales()
    assert quatre_diagonales == [
        Position(2, 3),
        Position(2, 5),
        Position(4, 3),
        Position(4, 5),
    ]
    # Test quatre_positions_sauts
    quatre_sauts = pos1.quatre_positions_sauts()
    assert quatre_sauts == [
        Position(0, 1),
        Position(0, 5),
        Position(4, 1),
        Position(4, 5),
    ]
    quatre_sauts = pos2.quatre_positions_sauts()
    assert quatre_sauts == [
        Position(1, 2),
        Position(1, 6),
        Position(5, 2),
        Position(5, 6),
    ]

    print("Test unitaires passés avec succès!")
