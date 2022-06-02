######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs
import random
import time
# Modules du dossier 'lib'
import Ressources_pong
import Gestion_controles
import Gestion_audio
#variable utiles
tempsFrame = 0.006
pause_start = 0
score_D_fin = 0
score_G_fin = 0
jeu = 0
fin = 0
######################################
#  INSTANCIATION DES OBJETS UTILES   #
######################################
#importe la librairie gestion_controles dans controles
controles = Gestion_controles.gestion_controles()
#importe la librairie lecteur_mp3 dans lecteur_mp3
lecteur_mp3 = Gestion_audio.gestion_audio()
#importe la librairie Ressources_pong dans ressources
ressources = Ressources_pong.pong()


def demarrage():
    #lance la musique de fond
    lecteur_mp3.dfplayer_mini.play(track=24)
    #ajoute le fond et la joueuse au groupe_elements
    ressources.groupe_elements.append(ressources.fond)
    ressources.groupe_elements.append(ressources.joueuse)
    #affiche tous les éléments de groupe_elements
    ressources.ecran.show(ressources.groupe_elements)
    # animation de démarage (arriver de la joueuse de la gauche)
    for x in range(-124, 0):
        ressources.joueuse.x = x
        time.sleep(0.001)
    #ajoute message_start a groupe_elements
    ressources.groupe_elements.append(ressources.message_start)


def spawn():
    deltaX = 1
    deltaY = 1
    #permet de prendre un angle au hasard :
    deltaX = random.randint(0,1)
    deltaY = random.randint(0,1)
    #remplace les 0 par des -1
    if deltaX == 0:
        deltaX = -1
    if deltaX == 1:
        deltaX = 1
    if deltaY == 0:
        deltaY = -1
    if deltaY == 1:
        deltaY = 1
    #replace les raquettes au centre
    ressources.raquette_D.y = 52
    ressources.raquette_G.y = 52
    #replace la balle au centre
    ressources.balle_bmp.x = 75
    #replace la balle sur l'axe des Y au hasard
    ressources.balle_bmp.y = random.randint(30,98)
    return deltaX,deltaY


def joueur_gauche():
    if controles.bouton_H.value == False:
        ressources.raquette_G.y = ressources.raquette_G.y - 1
    if ressources.raquette_G.y <=0:
        ressources.raquette_G.y = ressources.raquette_G.y + 1
    if controles.bouton_B.value == False:
        ressources.raquette_G.y = ressources.raquette_G.y + 1
    if ressources.raquette_G.y >= 104:
        ressources.raquette_G.y = ressources.raquette_G.y - 1


def joueur_droite():
    if controles.joystick_Y.value > 50000:
        ressources.raquette_D.y = ressources.raquette_D.y - 1
    if ressources.raquette_D.y <=0:
        ressources.raquette_D.y = ressources.raquette_D.y + 1
    if controles.joystick_Y.value < 15000:
        ressources.raquette_D.y = ressources.raquette_D.y + 1
    if ressources.raquette_D.y >= 104:
        ressources.raquette_D.y = ressources.raquette_D.y - 1


def affichage_elements():
    #cache la balle du jeu
    ressources.balle_bmp.hidden = True
    #montre les scores :
    ressources.groupe_elements.append(ressources.score_D)
    ressources.groupe_elements.append(ressources.score_G)
    time.sleep(1.5)
    #montre la balle
    ressources.balle_bmp.hidden = False
    #cache les scores en utilisant moins de ram
    ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.score_D))
    ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.score_G))


def balle_score(deltaX,deltaY,score_D_fin,score_G_fin,tempsFrame):
    time.sleep(0.005)
    #rebond mur haut
    if ressources.balle_bmp.y <= 0 :
        deltaY = -deltaY
    #rebond mur bas
    if ressources.balle_bmp.y >= 116 :
        deltaY = -deltaY
    #rebond droite (sur la raquette_D)
    if ressources.balle_bmp.x == (ressources.largeur_ecran - ressources.largeur_raquette - ressources.diametre_balle) \
            and ressources.balle_bmp.y > ressources.raquette_D.y - ressources.diametre_balle \
            and ressources.balle_bmp.y < ressources.raquette_D.y + ressources.hauteur_raquette :
        #inverse le signe de deltaX pour que la balle fasse un rebond
        deltaX = -deltaX
        #raccourcis la vittesse temps quelle n'est pas trop basse (pour ne pas quelle aille trop vite)
        if tempsFrame >= 0.0008:
            tempsFrame -= 0.0008
    if ressources.balle_bmp.x > 160:
        #ajoute 1 au score afficher a l'écran
        ressources.score_G.text = str(int(ressources.score_G.text)+1)
        #ajoute 1 a la variable score_G_fin
        score_G_fin += 1
        #appelle la fonction spawn et récupère deltaX, deltaY pour un tire au hasard
        deltaX,deltaY = spawn()
        #appelle la fonction affichage_elements
        affichage_elements()
        #remet la vittesse normale
        tempsFrame = 0.006
    #rebond gauche (sur la raquette_G)
    if ressources.balle_bmp.x == ressources.largeur_raquette \
            and ressources.balle_bmp.y > ressources.raquette_G.y - ressources.diametre_balle \
            and ressources.balle_bmp.y < ressources.raquette_G.y + ressources.hauteur_raquette:
        #inverse le signe de deltaX pour que la balle fasse un rebond
        deltaX = -deltaX
        #raccourcis la vittesse temps quelle n'est pas trop basse (pour ne pas quelle aille trop vite)
        if tempsFrame >= 0.0008:
            tempsFrame -= 0.0008
    if ressources.balle_bmp.x < 0:
        #ajoute 1 au score afficher a l'écran
        ressources.score_D.text = str(int(ressources.score_D.text)+1)
        #ajoute 1 a la variable score_D_fin
        score_D_fin += 1
        #appelle la fonction spawn et récupère deltaX, deltaY pour un tire au hasard
        deltaX,deltaY = spawn()
        affichage_elements()
        #remet la vittesse normale
        tempsFrame = 0.006
    return score_D_fin,score_G_fin, deltaX, deltaY,tempsFrame

demarrage()
####################
####################
#  BOUCLE INFINIE  #
####################
####################
while True:
    time.sleep(0.006)
    if jeu == 0:
        #permet de faire clignoter le message_start
        pause_start = (pause_start + 1) % 50
        if pause_start == 49:
            if ressources.message_start.color == 0xFFFFFF: #blanc
                ressources.message_start.color = 0x000000 #noir
            else:
                ressources.message_start.color = 0xFFFFFF #blanc
    try:
        #Si le bouton du joystick est appuié le jeu commence :
        if controles.bouton_JOYSTICK.value == False:
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.fond))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.joueuse))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.message_start))
            ressources.groupe_elements.append(ressources.terrain)
            ressources.groupe_elements.append(ressources.message)
            time.sleep(2)
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.message))
            ressources.groupe_elements.append(ressources.raquette_D)
            ressources.groupe_elements.append(ressources.raquette_G)
            ressources.groupe_elements.append(ressources.balle_bmp)
            deltaX,deltaY = spawn()
            jeu = 1
    except ValueError:
        pass
    if jeu == 1:
        while True:
            #fait varrier vitesse
            time.sleep(tempsFrame)
            joueur_droite()
            joueur_gauche()
            score_D_fin,score_G_fin,deltaX,deltaY,tempsFrame = balle_score(deltaX,deltaY,score_D_fin,score_G_fin,tempsFrame)
            #permet de faire bouger la balle
            ressources.balle_bmp.y = ressources.balle_bmp.y +deltaY
            ressources.balle_bmp.x = ressources.balle_bmp.x +deltaX
            #sort de la boucle quand un joueur a 10 point
            if score_D_fin == 10 or score_G_fin == 10:
                break
            fin = 1
        if fin == 1 :
            #change de musique
            lecteur_mp3.dfplayer_mini.play(track=1)
            #retire différent élements de l'écran
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.terrain))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.balle_bmp))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.raquette_D))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.raquette_G))
            if score_D_fin == 10:
                ressources.vainqueur.text = "Joueur\nDroite"
            if score_G_fin == 10:
                ressources.vainqueur.text = "Joueur\nGauche"
            #affiche le fond_gagnant
            ressources.groupe_elements.append(ressources.fond_gagnant)
            #affiche le vainqueur
            ressources.groupe_elements.append(ressources.vainqueur)
            time.sleep(5)
            #retire le fond_gagnant et le vainqueur
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.fond_gagnant))
            ressources.groupe_elements.pop(ressources.groupe_elements.index(ressources.vainqueur))
            jeu = 2
    if jeu == 2:
        #relance un nouvelle partie :
        #remet les variables à 0
        jeu = 0
        fin = 0
        score_D_fin = 0
        score_G_fin = 0
        tempsFrame = 0.006
        #remet a 0 les score afficher sur l'écran
        ressources.score_D.text = str(int(0))
        ressources.score_G.text = str(int(0))
        #relance l'animation de démarrage
        demarrage()
