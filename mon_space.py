import pygame
import sys
import random

pygame.init()

LARGEUR_ECRAN, HAUTEUR_ECRAN = 800, 600
VITESSE_JOUEUR = 5
VITESSE_ENNEMI = 2
VITESSE_BALLE = 10
ENNEMIS_A_PASSER = 10

img_joueur = pygame.image.load('images/joueur.png')
img_ennemi = pygame.image.load('images/ennemi.png')
img_balle = pygame.image.load('images/balle.png')
img_fond = pygame.image.load('images/map.png')

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_joueur
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN - 30)
        self.vitesse = VITESSE_JOUEUR

    def update(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vitesse
        if touches[pygame.K_RIGHT] and self.rect.right < LARGEUR_ECRAN:
            self.rect.x += self.vitesse

class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_ennemi
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGEUR_ECRAN - self.rect.width)
        self.rect.y = -self.rect.height
        self.vitesse = VITESSE_ENNEMI

    def update(self):
        self.rect.y += self.vitesse
        if self.rect.top > HAUTEUR_ECRAN:
            self.kill()
            global ennemis_passes
            ennemis_passes += 1

class Balle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_balle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vitesse = VITESSE_BALLE

    def update(self):
        self.rect.y -= self.vitesse
        if self.rect.bottom < 0:
            self.kill()

def principal():
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption('Space Invaders by Leonard')
    horloge = pygame.time.Clock()

    groupe_joueur = pygame.sprite.Group()
    groupe_ennemi = pygame.sprite.Group()
    groupe_balle = pygame.sprite.Group()

    joueur = Joueur()
    groupe_joueur.add(joueur)

    score = 0
    global ennemis_passes
    ennemis_passes = 0

    while True:
        if ennemis_passes >= 10 and score < 10:  # Condition modifiée
            print("Game Over")
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    balle = Balle(joueur.rect.centerx, joueur.rect.top)
                    groupe_balle.add(balle)

        if random.random() < 0.02:
            ennemi = Ennemi()
            groupe_ennemi.add(ennemi)

        groupe_joueur.update()
        groupe_ennemi.update()
        groupe_balle.update()

        for balle in pygame.sprite.groupcollide(groupe_balle, groupe_ennemi, True, True).keys():
            score += 1  

        ecran.blit(img_fond, (0, 0))
        groupe_joueur.draw(ecran)
        groupe_ennemi.draw(ecran)
        groupe_balle.draw(ecran)

        police = pygame.font.Font(None, 36)
        texte_score = police.render(f'Score: {score}', True, (0, 0, 0))
        ecran.blit(texte_score, (10, 10))

        pygame.display.flip()
        horloge.tick(60)

if __name__ == "__main__":
    principal()
