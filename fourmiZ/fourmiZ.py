﻿import pygame
from pygame.locals import *
pygame.init()
from random import randint
from math import *
from time import sleep

fenetre = pygame.display.set_mode((0,0), FULLSCREEN)

CRUSH = pygame.mixer.Sound("crush.wav")
RHAAA = pygame.mixer.Sound("cris.wav")

CURSOR1 = pygame.image.load("cursor1.png").convert_alpha()
CURSOR10 = pygame.image.load("cursor10.png").convert_alpha()
CURSOR100 = pygame.image.load("cursor100.png").convert_alpha()
CURSOR1000 = pygame.image.load("cursor1000.png").convert_alpha()
CURSORQUEEN = pygame.image.load("cursorqueen.png").convert_alpha()
ANT = pygame.image.load("ant.png").convert_alpha()
BLOOD = pygame.image.load('blood.png').convert_alpha()
FOOD1 = pygame.image.load("food1.png").convert_alpha() #cursor too
FOOD2 = pygame.image.load("food2.png").convert_alpha()
FOOD3 = pygame.image.load("food3.png").convert_alpha()
FOOD4 = pygame.image.load("food4.png").convert_alpha()
FOOD5 = pygame.image.load("food5.png").convert_alpha()
FOOD = [FOOD1,FOOD2,FOOD3,FOOD4,FOOD5]
QUEENANT = pygame.image.load("queenant.png").convert_alpha()
LARVA = pygame.image.load("larva.png").convert_alpha()

class Ant:
    def __init__(self, x, y, screenx, screeny, num, queen, food_generators):
        self.x = x
        self.y = y
        self.screenx = screenx
        self.screeny = screeny

        self.depart_timerwait, self.fin_timerwait = False, False
        self.waiting = 0
        self.depart_timermoove, self.fin_timermoove = False, False
        self.mooving = 0
        self.attendre = True
        self.bouger = False

        self.imageant = ANT
        self.angle = randint(0,360)
        self.anglerad = self.angle*(pi/180)
        self.vx = -cos(-self.anglerad)*5
        self.vy = -sin(-self.anglerad)*5
        self.imageantangle = self.imageant
        self.q = True
        self.changer = 0
        self.num = num
        self.killed = False

        self.pv = 100

        self.last_food = None
        self.food = False
        self.queen = queen

        self.food_generators = food_generators


    def mouvement(self):
        if self.killed:
            return

        self.anglerad = self.angle*(pi/180)
        self.vx = -cos(-self.anglerad)*5
        self.vy = -sin(-self.anglerad)*5

        if self.depart_timerwait == True:
            self.waiting = pygame.time.get_ticks() + randint(250,500)
            self.depart_timerwait = False
        if self.attendre:
            if pygame.time.get_ticks() > self.waiting:
                self.fin_timerwait = True

        if self.fin_timerwait == True:
            self.bouger = True
            self.attendre = False
            self.depart_timermoove = True
            self.fin_timerwait = False

        if self.depart_timermoove == True:
            self.mooving = pygame.time.get_ticks() + randint(500,1000)
            self.depart_timermoove = False

        if self.food or self.last_food:
            self.x = self.x+self.vx
            self.y = self.y+self.vy
        elif self.bouger:
            if pygame.time.get_ticks() > self.mooving:
                self.fin_timermoove = True
            if pygame.time.get_ticks() <= self.mooving:
                self.x = self.x+self.vx
                self.y = self.y+self.vy

        if self.food:
            x_a = self.x - self.queen.x
            y_a = self.y - self.queen.y
            Na = sqrt(x_a**2+y_a**2)
            c = x_a/Na
            s = y_a
            s = s/abs(s)
            self.angle = -s*acos(c) / 2 / pi * 360
            if self.x > self.queen.x-5 and self.x < self.queen.x + 80 and self.y > self.queen.y-5 and self.y < self.queen.y + 80:
                self.food = False
                self.queen.create_larva(fenetre)
        elif self.last_food:
            x_a = self.x - self.last_food[0]
            y_a = self.y - self.last_food[1]
            Na = sqrt(x_a**2+y_a**2)
            c = x_a/Na
            s = y_a
            s = s/abs(s)
            self.angle = -s*acos(c) / 2 / pi * 360
        else :
            if self.q and pygame.time.get_ticks()>self.changer:
                self.angle += 5
                self.changer = pygame.time.get_ticks() + 500
                self.q = False
            if not(self.q) and pygame.time.get_ticks()>self.changer:
                self.angle -= 5
                self.q = True
                self.changer = pygame.time.get_ticks() + 500

                if self.fin_timermoove == True:
                    self.angle = self.angle + randint(-45,45)
                    if self.angle < 0:
                        self.angle = 0
                    if self.angle > 360:
                        self.angle = 360
                    self.bouger = False
                    self.attendre = True
                    self.depart_timerwait = True
                    self.fin_timermoove = False

                if self.x<0:
                    self.x = 0
                    self.angle = 180
                if self.x>self.screenx-50:
                    self.x = self.screenx-50
                    self.angle = 0
                if self.y<0:
                    self.y = 0
                    self.angle = 90
                if self.y>self.screeny-50:
                    self.y = self.screeny-50
                    self.angle = 270

        if not self.food:
            there_is_food = False
            for i in self.food_generators:
                if self.x > i.x-5 and self.x < i.x+30 and self.y > i.y-5 and self.y < i.y + 30:
                    there_is_food = True
                    self.food = i.give_me_food()
                    self.last_food = (self.x, self.y)
                    if i.pv < 0:
                        self.last_food = None
            if self.last_food:
                if self.x > self.last_food[0]-5 and self.x < self.last_food[0]+30 and self.y > self.last_food[1]-5 and self.y < self.last_food[1] + 30 and not there_is_food:
                    self.last_food = None


    def affiche(self, fenetre):
        if self.killed:
            fenetre.blit(BLOOD, (self.x-15, self.y-15))
        else:
            self.rotation()
            fenetre.blit(self.imageant, (self.x, self.y)) #ant

    def rotation(self):
        self.imageant = ANT
        origine_rectangle = self.imageant.get_rect()
        rotation_image = pygame.transform.rotate(self.imageant, self.angle)
        rotation_rectangle = origine_rectangle.copy()
        rotation_rectangle.center = rotation_image.get_rect().center
        self.imageant = rotation_image.subsurface(rotation_rectangle).copy()

class FoodGenerator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pv = 4
        self.etat = 0
    def affiche(self, fenetre):
        fenetre.blit(FOOD[self.etat], (self.x, self.y))

    def give_me_food(self):
        if self.pv < 0:
            return False
        self.pv -= 1
        if self.etat < 4:
            self.etat += 1
        return True

class Larva(Ant):
    def __init__(self, num, queen, fenetre):
        self.x = queen.x + randint(-35, 70)
        self.y = queen.y + randint(-35, 70)
        self.screenx, self.screeny = fenetre.get_width(), fenetre.get_height()
        if self.x<0:
            self.x = 0
        if self.x>self.screenx-35:
            self.x = self.screenx-35
        if self.y<0:
            self.y = 0
        if self.y>self.screeny-35:
            self.y = self.screeny-35
        self.eclose = False
        self.time_eclose = pygame.time.get_ticks() + 10000
        self.q = True
        self.angle = randint(0,360)
        self.imagelarva = LARVA
        self.changer = 0
        self.num = num
        self.queen = queen
    def mouvement(self):
        if self.eclose:
            return
        if self.q and pygame.time.get_ticks()>self.changer:
            self.angle += randint(0,20)
            self.changer = pygame.time.get_ticks() + 1000
            self.q = False
        if not(self.q) and pygame.time.get_ticks()>self.changer:
            self.angle -= randint(0,20)
            self.q = True
            self.changer = pygame.time.get_ticks() + 1000
    def eclosion(self):
        if pygame.time.get_ticks() > self.time_eclose:
            self.queen.create_ant(self.num)
            self.eclose = True
    def affiche(self, fenetre):
        self.rotation()
        fenetre.blit(self.imagelarva, (self.x, self.y))
    def rotation(self):
        self.imagelarva = LARVA
        origine_rectangle = self.imagelarva.get_rect()
        rotation_image = pygame.transform.rotate(self.imagelarva, self.angle)
        rotation_rectangle = origine_rectangle.copy()
        rotation_rectangle.center = rotation_image.get_rect().center
        self.imagelarva = rotation_image.subsurface(rotation_rectangle).copy()

class Queen(Ant):
    def __init__(self, larva, ants):
        self.x, self.y = (randint(75,fenetre.get_width())-75), (randint(75,(fenetre.get_height())-75))
        self.angle = randint(0,360)
        self.imagequeen = QUEENANT
        self.killed = False
        self.changer = 0
        self.q = True
        self.larva = larva
        self.ants = ants

    def mouvement(self):
        if self.killed:
            return
        if self.q and pygame.time.get_ticks()>self.changer:
            self.angle += randint(0,45)
            self.changer = pygame.time.get_ticks() + 500
            self.q = False
        if not(self.q) and pygame.time.get_ticks()>self.changer:
            self.angle -= randint(0,45)
            self.q = True
            self.changer = pygame.time.get_ticks() + 500

    def affiche(self, fenetre):
        if self.killed:
            fenetre.blit(BLOOD, (self.x-15, self.y-15))
        else:
            self.rotation()
            fenetre.blit(self.imagequeen, (self.x, self.y)) #ant

    def rotation(self):
        self.imagequeen = QUEENANT
        origine_rectangle = self.imagequeen.get_rect()
        rotation_image = pygame.transform.rotate(self.imagequeen, self.angle)
        rotation_rectangle = origine_rectangle.copy()
        rotation_rectangle.center = rotation_image.get_rect().center
        self.imagequeen = rotation_image.subsurface(rotation_rectangle).copy()

    def create_larva(self, fenetre):
        self.larva.append(Larva(len(self.larva), self, fenetre))
    def create_ant(self, larva_num):
        l =  self.larva[larva_num]
        self.larva.pop(larva_num)
        for i in self.larva[larva_num:]:
            i.num -= 1
        x,y = l.x, l.y
        self.ants.append(Ant(x,y, fenetre.get_width(),fenetre.get_height(), len(self.ants), self, food_generators))


pygame.display.set_caption("Fourmiz")

jeu = True
ants = []
deads = []
food_generators = []
larva = []
queenant = Queen(larva, ants)

kill_all = False
nb_add = 1
pygame.mouse.set_visible(False)
cursor = CURSOR1

bg = pygame.Surface((fenetre.get_width(),fenetre.get_height()))
pygame.draw.rect(bg, (255,255,255), (0,0,bg.get_width(),bg.get_height()), 0)


while jeu:
    for event in pygame.event.get():
        if event.type == QUIT:
            jeu = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                jeu = False
            if event.key == K_RETURN:
                ants = []
                food_generators = []
                larva = []
                pygame.draw.rect(bg, (255,255,255), (0,0,bg.get_width(),bg.get_height()), 0)
                queenant = Queen(larva, ants)
            if event.key == K_r:
                nb_add = 1000
                cursor = CURSOR1000
            if event.key == K_e:
                nb_add = 100
                cursor = CURSOR100
            if event.key == K_z:
                nb_add = 10
                cursor = CURSOR10
            if event.key == K_a:
                nb_add = 1
                cursor = CURSOR1
            if event.key == K_t:
                nb_add = 0
                cursor = FOOD1
            if event.key == K_y:
                nb_add = -1
                cursor = CURSORQUEEN
        if event.type == MOUSEBUTTONDOWN and event.button == 2:
            kill_all = True
            RHAAA.play()
            queenant.killed = True
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            (x, y) = pygame.mouse.get_pos()
            for a in ants:
                if x > a.x and x < a.x + 50 and y > a.y and y < a.y+50:
                    a.killed = True
                    CRUSH.play()
                    ants.pop(a.num)
                    deads.append(a)
                    for i in ants[a.num:]:
                        i.num -= 1

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            (x, y) = pygame.mouse.get_pos()
            if nb_add > 0:
                for i in range(nb_add):
                    ants.append(Ant(x,y, fenetre.get_width(),fenetre.get_height(), len(ants), queenant, food_generators))
            if nb_add == 0:
                food_generators.append(FoodGenerator(x,y))
            if nb_add == -1:
                queenant.x = x-32
                queenant.y = y-32


    if kill_all:
        for i in ants:
            i.killed = True
            deads.append(i)
        ants = []
        kill_all = False
        sleep(1)

    for i in deads:
        i.affiche(bg)
    deads = []
    fenetre.blit(bg, (0,0))

    for x,f in enumerate(food_generators):
        if f.pv < 0:
            food_generators.pop(x)
        else:
            f.affiche(fenetre)

    for l in larva:
        l.mouvement()
        l.eclosion()
        l.affiche(fenetre)

    for a in ants:
        a.mouvement()
        a.affiche(fenetre)

    queenant.mouvement()
    queenant.affiche(fenetre)

    #affichage curseur
    (x, y) = pygame.mouse.get_pos()
    fenetre.blit(cursor, (x, y))


    pygame.display.flip()
    pygame.time.Clock().tick(20)

pygame.quit()
