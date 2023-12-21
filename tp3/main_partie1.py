import sys

sys.path.append("C:/Users/2weny9ine/Desktop/study/IFT 1004 programmation intro/tp3")

# Remarque : La classe "Partie" est importée du package "tp3.Partie1".
# Assurez-vous que le répertoire "tp3" se trouve dans le répertoire de travail courant
# lors de l'exécution de ce script.

from tp3.Partie1.partie import Partie

if __name__ == "__main__":
    # Point d'entrée du programme. On initialise une nouvelle partie, et on appelle la méthode jouer().
    partie = Partie()

    gagnant = partie.jouer()

    print("------------------------------------------------------")
    print("Partie terminée! Le joueur gagnant est le joueur", gagnant)
