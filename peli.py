import pygame
import math
from pygame.constants import K_LEFT
taustavari = (180, 240, 240)

def main():
    peli = Peli()
    peli.aja()
 
 
class Peli:
    def __init__(self):
        self.ajossa = True
        self.naytto = None
        self.leveys = 800
        self.korkeus = 600
        self.nayton_koko = (self.leveys, self.korkeus)
 
    def aja(self):
        self.alustus()
        while self.ajossa:
            for event in pygame.event.get():
                self.tapahtuma(event)
            self.pelilogiikka()
            self.renderointi()
        self.lopetus()
 
    def alustus(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.naytto = pygame.display.set_mode(
            self.nayton_koko, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.kuva_iso = pygame.image.load("Pogey.png")
        self.kuva_pieni = pygame.transform.rotozoom(self.kuva_iso, 0, 0.25)
        self.kulma = 0
        self.pyorimisvauhti = 0
        self.sijainti = (400, 300)
        self.vauhti = 0
        self.hiiren_nappi_pohjassa = False
        self.voima = 0
        self.voimanlisays = False
        self.laukaisu = False
 
    def tapahtuma(self, event):
        if event.type == pygame.QUIT: 
            self.ajossa = False
        # Hiiren tapahtumat ------------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.hiiren_nappi_pohjassa = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.hiiren_nappi_pohjassa = False
        # Näppäimen painaminen alas ----------------------------
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                self.pyorimisvauhti = 3
            elif event.key == pygame.K_RIGHT:
                self.pyorimisvauhti = -3
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = True
        # Näppäimen nosto ylös ---------------------------------
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.pyorimisvauhti = 0
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = False
                self.laukaisu = True


 
    def pelilogiikka(self):
        if self.hiiren_nappi_pohjassa:
            self.sijainti = pygame.mouse.get_pos()

        if self.pyorimisvauhti != 0:
            self.kulma = (self.kulma + self.pyorimisvauhti) % 360

        if self.voimanlisays:
            self.voima = min(self.voima + 2,100)
        
        if self.laukaisu:
            # print(f"Pam! {self.voima}")
            self.vauhti = self.voima ** 2 / 200.0
            self.voima = 0
            self.laukaisu = False
        
        if self.vauhti > 0.1:
            vauhti_x = -self.vauhti * math.sin(self.kulma / 180 * math.pi)
            vauhti_y = -self.vauhti * math.cos(self.kulma / 180 * math.pi)
            uusi_x = self.sijainti[0] + vauhti_x
            uusi_y = self.sijainti[1] + vauhti_y
            self.sijainti = (uusi_x, uusi_y)
            self.vauhti *= 0.97


 
    def renderointi(self):
        self.naytto.fill(taustavari) # (Red, Green, Blue)
        kuva = pygame.transform.rotozoom(self.kuva_pieni, self.kulma, 1)
        laatikko = kuva.get_rect(center=self.sijainti)
        self.naytto.blit(kuva, laatikko.topleft)
        pygame.draw.rect(self.naytto, (0, 0, 0), (2, self.korkeus - 19, 102, 17))
        pygame.draw.rect(self.naytto, (251, 79, 20), (3, self.korkeus - 18, self.voima, 15))
        suuntapallo_x = self.leveys - 35
        suuntapallo_y = self.korkeus - 35
        suuntavektori_x = -30 * math.sin(self.kulma / 180 * math.pi)
        suuntavektori_y = -30 * math.cos(self.kulma / 180 * math.pi)
        pygame.draw.circle(self.naytto, (0,0,0), (suuntapallo_x, suuntapallo_y), 30)
        pygame.draw.line(self.naytto, (251, 79, 20),
                        (suuntapallo_x, suuntapallo_y),
                        (suuntapallo_x + suuntavektori_x, suuntapallo_y + suuntavektori_y))
        pygame.display.flip()
        self.kello.tick(60) # 60 FPS (Frames Per Second)
 
    def lopetus(self):
        pygame.quit()
 
 
if __name__ == "__main__" :
    main()