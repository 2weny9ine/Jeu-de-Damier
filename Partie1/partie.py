# Auteurs: Mohammed Yacine Rouainia

from Partie1.damier import Damier
from Partie1.position import Position


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """

    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        piece_selectionne = self.damier.recuperer_piece_a_position(position_source)
        if piece_selectionne is not None:
            if piece_selectionne.couleur == self.couleur_joueur_courant:
                if self.doit_prendre:
                    if self.damier.piece_peut_faire_une_prise(position_source):
                        if self.position_source_forcee is None:
                            return True, ""
                        elif position_source == self.position_source_forcee:
                            return True, ""
                        else:
                            return (
                                False,
                                "Erreur:une prise forcée doit etre effectuée",
                            )
                    else:
                        return False, "Erreur:une prise forcée doit etre effectuée"
                elif self.damier.piece_peut_faire_une_prise(
                    position_source
                ) or self.damier.piece_peut_se_deplacer(position_source):
                    return True, ""
                else:
                    return False, "Erreur:piece ne peut ni deplacer ni faire une prise"
            else:
                return False, "Erreur:piece selectionnée est du couleur adverse"
        else:
            return False, "Erreur:position vide/n'existe pas"

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """
        if self.damier.position_est_dans_damier(position_cible):
            if self.damier.recuperer_piece_a_position(position_cible) is None:
                if self.doit_prendre:
                    if self.damier.piece_peut_sauter_vers(
                        self.position_source_forcee, position_cible
                    ):
                        return True, ""
                    else:
                        return (
                            False,
                            "Erreur:tu peux pas deplacer ici y'a une prise obligatoire",
                        )
                else:
                    if self.damier.piece_peut_sauter_vers(
                        self.position_source_selectionnee, position_cible
                    ):
                        return True, ""
                    elif self.damier.piece_peut_se_deplacer_vers(
                        self.position_source_selectionnee, position_cible
                    ):
                        return True, ""
                    else:
                        return False, "Erreur:piece ne peut deplacer/sauter ici"
            else:
                return False, "Erreur:position occupée"
        else:
            return False, "Erreur:position invalide"

    def selectionner_piece(self, text):
        """
         Cette méthode continue de demander des coordonnées jusqu'à ce qu'une position valide soit entrée. Si les valeurs
         entrées ne sont pas numériques ou si la position n'est pas valide, un message d'erreur approprié est affiché et
         l'utilisateur est invité à réessayer.

        Parameters:
            text (str): Un message à afficher avant de demander les coordonnées de la pièce.

        Returns:
           Position: Position source valide.

        """
        print(text)
        while True:
            ligne = input("Ligne (entre 0 et 7): ")
            colonne = input("Colonne (entre 0 et 7): ")
            if ligne.isnumeric() and colonne.isnumeric():
                position_piece = Position(int(ligne), int(colonne))
                if self.position_source_valide(position_piece):
                    return position_piece
                else:
                    print("Position sélectionnée invalide")
            else:
                print("Valeur entrée invalide")

    def selectionner_cible(self, text):
        """
         Cette méthode continue de demander des coordonnées jusqu'à ce qu'une position cible valide soit entrée. Si les valeurs
         entrées ne sont pas numériques ou si la position cible n'est pas valide, un message d'erreur approprié est affiché et
         l'utilisateur est invité à réessayer.

        Parameters:
            text (str): Un message à afficher avant de demander les coordonnées de la pièce.

        Returns:
           Position: Position cible valide.

        """
        print(text)
        while True:
            ligne = input("Ligne (entre 0 et 7): ")
            colonne = input("Colonne (entre 0 et 7): ")
            if ligne.isnumeric() and colonne.isnumeric():
                position_cible = Position(int(ligne), int(colonne))
                if self.position_cible_valide(position_cible):
                    return position_cible
                else:
                    print("Position sélectionnée invalide")
            else:
                print("Valeur entrée invalide")

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        position_piece = self.selectionner_piece("Sélectionner la position du piece")
        position_cible = self.selectionner_cible("Sélectionner la position cible")
        return position_piece, position_cible

    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(
            self.couleur_joueur_courant
        ):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(
                    " Doit prendre avec la pièce en position {}.".format(
                        self.position_source_forcee
                    )
                )
        else:
            print("")

        # Demander les positions
        self.position_source_selectionnee = self.demander_positions_deplacement()[0]
        position_cible = self.demander_positions_deplacement()[1]

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        self.damier.deplacer(self.position_source_selectionnee, position_cible)
        # Mettre à jour les attributs de la classe
        if (
            self.damier.deplacer(self.position_source_selectionnee, position_cible)
            == "ok"
        ):
            if self.couleur_joueur_courant == "blanc":
                self.couleur_joueur_courant = "noir"
            else:
                self.couleur_joueur_courant = "blanc"
            self.position_source_forcee = None
            self.doit_prendre = False
        elif (
            self.damier.deplacer(self.position_source_selectionnee, position_cible)
            == "prise"
        ):
            if self.damier.piece_peut_faire_une_prise(position_cible):
                self.doit_prendre = True
                self.position_source_forcee = position_cible
            else:
                if self.couleur_joueur_courant == "blanc":
                    self.couleur_joueur_courant = "noir"
                else:
                    self.couleur_joueur_courant = "blanc"
                self.position_source_forcee = None
                self.doit_prendre = False
        else:
            self.position_source_selectionnee = self.demander_positions_deplacement()[0]
            position_cible = self.demander_positions_deplacement()[1]

    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(
            self.couleur_joueur_courant
        ) or self.damier.piece_de_couleur_peut_faire_une_prise(
            self.couleur_joueur_courant
        ):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"
