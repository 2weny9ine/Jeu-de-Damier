import sys

sys.path.append("C:/Users/2weny9ine/Desktop/study/IFT 1004 programmation intro/tp3")
# Remarque : La classe "Partie" est importée du package "tp3.Partie2".
# Assurez-vous que le répertoire "tp3" se trouve dans le répertoire de travail courant
# lors de l'exécution de ce script.
from tp3.Partie2.interface_dames import FenetrePartie

if __name__ == "__main__":
    # Point d'entrée principal
    fenetre = FenetrePartie()
    fenetre.mainloop()
