# Auteurs: Hadjer Laimeche
# interface_dames.py
from tkinter import Tk, Label, Button, NSEW
from canvas_damier import CanvasDamier
from Partie1.partie import Partie
from Partie1.position import Position


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        quit_button (Button): Un bouton permettant à l'utilisateur de quitter le jeu. Lorsqu'il est cliqué, il déclenche la fermeture de l'interface graphique.
        new_game_button (Button): Un bouton qui permet de démarrer une nouvelle partie. En cliquant dessus, l'état du jeu est réinitialisé et une nouvelle partie commence.
        gagnant_overlay (Label): Un «widget» label utilisé pour afficher le gagnant de la partie à la fin du jeu. Il apparaît au-dessus de tous les autres éléments de l'interface pour annoncer le gagnant.
    """

    def __init__(self):
        super().__init__()
        # la partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(row=0, column=0, sticky=NSEW)
        self.canvas_damier.bind("<Button-1>", self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid(row=1, column=0)

        # Buttons Quitter et Button Nouvelle Partie
        self.quit_button = Button(self, text="Quitter", command=self.quitter_jeu)
        self.quit_button.grid(row=3, column=0, sticky=NSEW)
        self.new_game_button = Button(
            self, text="Nouvelle Partie", command=self.Nouvelle_Partie
        )
        self.new_game_button.grid(row=2, column=0, sticky=NSEW)

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Pour afficher le gagnant a la fin
        self.gagnant_overlay = Label(self, text="", bg="green", fg="white")
        self.gagnant_overlay.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=0.1
        )
        self.gagnant_overlay.lower()

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)
        self.messages["foreground"] = "black"
        self.messages["text"] = "Tour du joueur: {}".format(
            self.partie.couleur_joueur_courant
        )
        if not self.partie.damier.piece_de_couleur_peut_se_deplacer(
            self.partie.couleur_joueur_courant
        ):
            self.changer_tour()
            self.gagnant_overlay[
                "text"
            ] = f"LE GAGNANT EST: {self.partie.couleur_joueur_courant.capitalize()}"
            self.gagnant_overlay.lift()
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(
            self.partie.couleur_joueur_courant
        ):
            self.partie.doit_prendre = True
        else:
            self.partie.doit_prendre = False

        if self.partie.position_source_selectionnee is not None:
            self.selectionner_cible(position)
        else:
            self.selectionner_source(position)
        self.canvas_damier.actualiser()

    def selectionner_source(self, position):
        """
        Traite la sélection de la position source pour un déplacement de pièce. Vérifie si la pièce sélectionnée est valide et met à jour les messages du jeu.

          Args:
        position (Position): L'objet position représentant la case sélectionnée sur le damier.
        """
        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)
        if piece is None:
            self.messages["foreground"] = "red"
            self.messages["text"] = "Erreur: Aucune pièce à cet endroit."
        elif self.partie.doit_prendre:
            if self.partie.position_source_forcee is not None:
                self.messages["foreground"] = "red"
                self.messages[
                    "text"
                ] = " Doit prendre avec la pièce en position {}.".format(
                    self.partie.position_source_forcee
                )
                position = self.partie.position_source_forcee

            if self.partie.position_source_valide(position)[0]:
                self.partie.position_source_selectionnee = position
                self.messages["foreground"] = "black"
                self.messages[
                    "text"
                ] = "Position source sélectionnée: {} . Choisir la position cible ".format(
                    position
                )
            else:
                self.messages["foreground"] = "red"
                self.messages["text"] = self.partie.position_source_valide(position)[1]
        elif not self.partie.doit_prendre:
            if self.partie.position_source_valide(position)[0]:
                self.partie.position_source_selectionnee = position
                self.messages["foreground"] = "black"
                self.messages[
                    "text"
                ] = "Position source sélectionnée: {}. Choisir la position cible".format(
                    position
                )
            else:
                self.messages["foreground"] = "red"
                self.messages["text"] = self.partie.position_source_valide(position)[1]
        else:
            self.messages["foreground"] = "red"
            self.messages["text"] = self.partie.position_source_valide(position)[1]
        self.update_idletasks()

    def selectionner_cible(self, position_cible):
        """
          Gère la sélection de la position cible pour un déplacement de pièce. Vérifie la validité du déplacement et exécute le mouvement.

        Args:
        position_cible (Position): L'objet position représentant la case cible pour le déplacement de la pièce.
        """

        valide_2, message_2 = self.partie.position_cible_valide(position_cible)
        if valide_2:
            deplacement = self.partie.damier.deplacer(
                self.partie.position_source_selectionnee, position_cible
            )
            self.resultats_deplacement(deplacement, position_cible)
        else:
            self.partie.position_source_selectionnee = None
            self.messages["foreground"] = "red"
            self.messages["text"] = message_2
        self.update_idletasks()

    def resultats_deplacement(self, deplacement, position_cible):
        """
         Traite le résultat d'un déplacement de pièce, y compris la gestion des tours et des prises multiples.

        Args:
        deplacement (str): Le résultat du déplacement ('ok', 'prise').
         position_cible (Position): La position cible du déplacement effectué.
        """

        if deplacement == "ok":
            self.changer_tour()
            if self.partie.damier.piece_de_couleur_peut_faire_une_prise(
                self.partie.couleur_joueur_courant
            ):
                self.messages["foreground"] = "black"
                self.messages[
                    "text"
                ] = "Déplacement réussie,Tour du joueur: {} ---> Une prise obligatoire doit etre effectuée".format(
                    self.partie.couleur_joueur_courant
                )
            else:
                self.messages["foreground"] = "black"
                self.messages["text"] = "Déplacement réussie,Tour du joueur: {}".format(
                    self.partie.couleur_joueur_courant
                )
            self.partie.position_source_forcee = None
            self.partie.position_source_selectionnee = None
        elif deplacement == "prise":
            self.prise_multiple(position_cible)
        self.update_idletasks()

    def prise_multiple(self, position_cible):
        """
        Gère les actions après une prise, en particulier dans le cas de prises multiples.

        Args:
         position_cible (Position): La position de la pièce après la prise.
        """

        if self.partie.damier.piece_peut_faire_une_prise(position_cible):
            self.partie.position_source_forcee = position_cible
            self.partie.doit_prendre = True
            self.messages["foreground"] = "black"
            self.messages[
                "text"
            ] = "Prise multiple possible, continuez avec la pièce en position   {}  ".format(
                position_cible
            )
            self.partie.position_source_selectionnee = None
        else:
            self.changer_tour()
            self.messages["foreground"] = "black"
            self.messages[
                "text"
            ] = "Prise réussie,Tour du joueur: {} ---> Une prise obligatoire doit etre effectuée".format(
                self.partie.couleur_joueur_courant
            )
            self.partie.position_source_forcee = None
            self.partie.doit_prendre = False
            self.partie.position_source_selectionnee = None

    def changer_tour(self):
        """
         Change le tour au joueur suivant.

        Args:
        None
        """
        self.partie.couleur_joueur_courant = (
            "noir" if self.partie.couleur_joueur_courant == "blanc" else "blanc"
        )
        self.update_idletasks()

    def Nouvelle_Partie(self):
        """
        Démarre une nouvelle partie. Réinitialise le damier et l'état du jeu.

        Args:
        None
        """
        self.partie = Partie()
        self.canvas_damier.damier = self.partie.damier
        self.canvas_damier.actualiser()
        self.messages["text"] = "Tour du joueur: {}".format(
            self.partie.couleur_joueur_courant
        )
        self.gagnant_overlay.lower()
        self.update_idletasks()

    def quitter_jeu(self):
        """
        Ferme la fenêtre du jeu.

        Args:
         None
        """
        self.destroy()
