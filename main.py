import pygame
import random
import sys
import time
import os
import requests

os.environ['SDL_VIDEO_CENTERED'] = '1'

clock = pygame.time.Clock()
WIN_W = 32*32
WIN_H = 32*20
fps = 60
black = (0,0,0)
white = (255,255,255)
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
tile_width = tile_height = 32
wizard_image = pygame.image.load("tempwizard.png").convert_alpha()
imaqtpie_image = pygame.image.load("imaqtpie.png").convert_alpha()
battleback = pygame.image.load("battleback.jpg").convert_alpha()
kappa_image = pygame.image.load("kappa.png").convert_alpha()
lul_image = pygame.image.load("LUL.png").convert_alpha()
rng_image = pygame.image.load("blessrng.png").convert_alpha()
lightning_image = pygame.image.load("lightning.png").convert_alpha()
jebaited_image = pygame.image.load("jebaited.png").convert_alpha()
pogchamp_image = pygame.image.load("pogchamp.png").convert_alpha()
frankerz_image = pygame.image.load("frankerz.png").convert_alpha()
kappapride_image = pygame.image.load("kappapride.png").convert_alpha()
heart_image = pygame.image.load("heart.png").convert_alpha()
zard_image = pygame.image.load("zard.png").convert_alpha()
floor_tile = pygame.image.load("floor_tile.JPG").convert_alpha()
background = pygame.image.load("background.png").convert_alpha()
twitchlogo = pygame.image.load("twitchlogo.png").convert_alpha()
background = pygame.transform.scale(background, (WIN_W, WIN_H))
backgroundrect = background.get_rect()
qtp_right_face = pygame.transform.scale(imaqtpie_image, (64, 64))
qtp_left_face = pygame.transform.flip(qtp_right_face, True, False)
zard_left_face = pygame.transform.scale(zard_image, (64, 64))
zard_right_face = pygame.transform.flip(zard_left_face, True, False)
wizard_right_face = pygame.transform.scale(wizard_image, (64, 64))
wizard_left_face = pygame.transform.flip(wizard_right_face, True, False)
battleback = pygame.transform.scale(battleback, (WIN_W, WIN_H))
battlebackrect = battleback.get_rect()
battlebackrect = battlebackrect.move(0,0)
twitchlogo = pygame.transform.scale(twitchlogo, (WIN_W, WIN_H))
twitchlogorect = twitchlogo.get_rect()
global fighting
global intro
global play
global elapsedtime
elapsedtime = 0
fighting = False


pygame.init()

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Emote Wizard"
        self.health = 100
        self.spells = ["Kappa Laser", "LUL", "Pray to RNGesus", "Jebaited", "PogChamp Armor", "FrankerZ", "KappaPride"]
        self.magic = 10
        self.mspeed = 5
        self.defense = 0
        self.image = wizard_image
        self.image = wizard_right_face
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = WIN_H - (8 * 32)
        self.direction = 0
        self.grounded = True
        self.fallSpeed = 2
        self.jumpCounter = 0
        self.jumpSpeed = 20
        self.jumpCD = 0
        self.counterAttack = False
        self.armorReduce = 0

    def update(self, np_tile_group, monster_group):
        left = right = up = down = False
        self.rect.y += 8
        if self.jumpCD is not 0:
            self.jumpCD -= 1
        up_collide_fix = (self.jumpSpeed - self.jumpCounter)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.mspeed
            left = True
        if key[pygame.K_RIGHT] and self.rect.x < WIN_W - 32:
            self.rect.x += self.mspeed
            right = True
        if key[pygame.K_UP] and self.jumpCD is 0:
            up = True
            self.jumpCounter += .7
            self.grounded = False
            self.rect.y -= up_collide_fix
        self.facing(left, right)
        self.collide(np_tile_group, left, right, down, up, up_collide_fix, monster_group)
    def collide(self, np_tile_group, left, right, down, up, up_collide_fix, monster_group):
        for p in np_tile_group:
            if pygame.sprite.collide_rect(self, p) :
                if not self.grounded:
                    self.jumpCD = 15
                self.grounded = True
                if not up and (not right or not left):
                    self.jumpCounter = 0
                self.rect.y -= 8
            if pygame.sprite.collide_rect(self, p) and right:
                self.rect.x -= self.mspeed
                if self.jumpCounter < self.fallSpeed:
                    self.rect.y += 8
                self.jumpCounter += 1
            if pygame.sprite.collide_rect(self, p) and left:
                self.rect.x += self.mspeed
                if self.jumpCounter < self.fallSpeed:
                    self.rect.y += 8
                self.jumpCounter += 1
            if pygame.sprite.collide_rect(self, p) and up:
                self.rect.y += up_collide_fix
                self.jumpCounter = 25
        for m in monster_group:
            if pygame.sprite.collide_rect(self, m):
                self.battle(m, monster_group)
                m.kill()
                zard = Monster(64, 200, "zard")
                monster_group.add(zard)
    def facing(self, left, right):
        if right and fighting == False:
            self.image = wizard_right_face
        elif left and fighting == False:
            self.image = wizard_left_face

    def battle(self, m, monster_group):
        fighting = True
        savespotx = self.rect.x
        savespoty = self.rect.y
        savemagic = self.magic
        self.image = pygame.transform.scale(wizard_right_face, (128, 128))
        if m.type is "imaqtpie":
            m.image = pygame.transform.scale(qtp_left_face, (128, 128))
        elif m.type == "zard":
            m.image = pygame.transform.scale(zard_left_face, (128, 128))
        self.rect.x = 256 - 96
        self.rect.y = WIN_H/2 + 64
        m.rect.x = 768
        m.rect.y = WIN_H/2 + 64

        global elapsedtime
        print (elapsedtime)
        random.seed(elapsedtime)
        rand = random.randint(0,6)
        print(rand)
        spell_1 = self.spells[rand]
        spell_2 = self.spells[(rand+1) % 7]
        spell_3 = self.spells[(rand + 2) % 7]

        #0 Kappa: Kappa Laser, fires laser that does 10(+120% magic) damage
        #1 LUL: LUL, doubles your magic and gives 10 health
        #2 BlessRNG: Pray to RNGesus, has a 65/35 chance to either do 5(+300% magic) damage to enemy or
        #  deal that same damage to yourself.
        #3 Jebaited: Jebaited, deflects next enemy attack, dealing 150% of the original damage to enemy.
        #4 PogChamp: PogChamp Armor, grants +7 defense for two turns.
        #5 FrankerZ: FrankerZ, Magically bite your enemy, dealing 5(+100% magic) damage and healing
        #  for half of that.
        #6 KappaPride: KappaPride, deals 5(+50% magic) damage to enemy and prevents them from
        #  attacking for this turn.
        chosen_spells = [spell_1, spell_2, spell_3]
        spelltitles = ["", "", ""]
        spellfont = pygame.font.Font(None, 30)
        for i in range(0,3):
            if chosen_spells[i] == "Kappa Laser":
                spelltitles[i] = "Kappa Laser: Blast your enemy dealing moderate damage."
            if chosen_spells[i] == "LUL":
                spelltitles[i] = "LUL: Increases your magical strength and regenerates some of your health."
            if chosen_spells[i] == "Pray to RNGesus":
                spelltitles[i] = "Pray to RNGesus (BlessRNG): Either deals massive damage to your enemy or to you."
            if chosen_spells[i] == "Jebaited":
                spelltitles[i] = "Jebaited: Deflects enemy attack, dealing its damage plus more."
            if chosen_spells[i] == "PogChamp Armor":
                spelltitles[i] = "PogChamp Armor: Grants a high amount of armor for 2 turns."
            if chosen_spells[i] is "FrankerZ":
                spelltitles[i] = "FrankerZ: Deal moderate damage and heal for half of it."
            if chosen_spells[i] == "KappaPride":
                spelltitles[i] = "KappaPride: Deals decent damage and prevents your enemy from attacking for one turn."

        bigfont = pygame.font.Font(None, 80)
        spellTitle1 = spellfont.render(spelltitles[0], 1, black)
        spellTitle1pos = spellTitle1.get_rect()
        spellTitle1pos.centerx = screen.get_rect().centerx
        spellTitle1pos.centery = screen.get_rect().centery - 200
        spellTitle2 = spellfont.render(spelltitles[1], 1, black)
        spellTitle2pos = spellTitle2.get_rect()
        spellTitle2pos.centerx = screen.get_rect().centerx
        spellTitle2pos.centery = screen.get_rect().centery - 150
        spellTitle3 = spellfont.render(spelltitles[2], 1, black)
        spellTitle3pos = spellTitle3.get_rect()
        spellTitle3pos.centerx = screen.get_rect().centerx
        spellTitle3pos.centery = screen.get_rect().centery - 100
        victorytitle = bigfont.render("YOU WON!", 1, black)
        victorytitlepos = victorytitle.get_rect()
        victorytitlepos.x = screen.get_rect().centerx - 400
        victorytitlepos.y = screen.get_rect().centery - 200
        defeattitle = bigfont.render("You lost . . .", 1, black)
        defeattitlepos = defeattitle.get_rect()
        defeattitlepos.x = screen.get_rect().centerx - 400
        defeattitlepos.y = screen.get_rect().centery - 200

        while fighting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                    sys.exit()

            healthfont = pygame.font.Font(None, 50)
            herohealth = healthfont.render(str(self.health) + "HP", 1, (0, 255, 0))
            herohealthpos = herohealth.get_rect()
            herohealthpos.x = self.rect.x
            herohealthpos.y = self.rect.y - 50
            monsterhealth = healthfont.render(str(m.health) + "HP", 1, (255, 0, 0))
            monsterhealthpos = monsterhealth.get_rect()
            monsterhealthpos.x = m.rect.x
            monsterhealthpos.y = m.rect.y - 50
            maintitle = bigfont.render("CHOOSE YOUR SPELL, CHAT:", 1, black)
            maintitlepos = maintitle.get_rect()
            maintitlepos.x = screen.get_rect().centerx - 400
            maintitlepos.y = screen.get_rect().centery - 300
            spellchoicetitle = spellfont.render("", 1, black)
            spellchoicetitlepos = spellchoicetitle.get_rect()
            spellchoicetitlepos.x = screen.get_rect().centerx - 150
            spellchoicetitlepos.y = screen.get_rect().centery + 250

            spell_cast = ""
            key = pygame.key.get_pressed()
            if key[pygame.K_1]:
                spell_cast = spell_1
            if key[pygame.K_2]:
                spell_cast = spell_2
            if key[pygame.K_3]:
                spell_cast = spell_3


            if not spell_cast == "":
                if self.armorReduce == 0:
                    pass
                else:
                    self.armorReduce -= 1
                    if self.armorReduce == 0:
                        self.defense -= 7
                string = spell_cast + " has been chosen!"
                spellchoicetitle = spellfont.render(string, 1, white)
                screen.blit(spellchoicetitle, spellchoicetitlepos)
                if spell_cast == "Kappa Laser":
                    for i in range(180):
                        kappa_laser = pygame.transform.scale(kappa_image, (50 + 4 * i, 32))
                        kappa_laserpos = kappa_image.get_rect()
                        kappa_laserpos.x = self.rect.right
                        kappa_laserpos.y = self.rect.y
                        screen.blit(kappa_laser, kappa_laserpos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        clock.tick(180)
                        pygame.display.flip()
                    m.health -= 10 + (1.2 * self.magic) - m.defense
                if spell_cast == "LUL":
                    for i in range(180):
                        lul = pygame.transform.scale(lul_image, (64+i, 64+i))
                        lulpos = lul_image.get_rect()
                        lulpos.x = self.rect.x+32
                        lulpos.y = self.rect.y
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        screen.blit(lul, lulpos)
                        clock.tick(120)
                        pygame.display.flip()
                    self.magic *= 2
                    self.health += 10
                if spell_cast == "Pray to RNGesus":
                    rng = random.randint(1,100)
                    for i in range(250):
                        blessrng = pygame.transform.scale(rng_image, (92, 92))
                        blessrngpos = rng_image.get_rect()
                        blessrngpos.x = screen.get_rect().centerx
                        blessrngpos.y = screen.get_rect().centery + (200 - i)
                        lightning = pygame.transform.scale(lightning_image, (300, 550))
                        lightningpos = lightning_image.get_rect()
                        lightningpos.x = self.rect.x - 100
                        lightningpos.y = self.rect.y - 400
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        screen.blit(blessrng, blessrngpos)
                        if i > 150:
                            if rng > 36:
                                lightningpos.x = m.rect.x - 100
                                lightningpos.y = m.rect.y - 400
                            screen.blit(lightning, lightningpos)
                        clock.tick(120)
                        pygame.display.flip()


                    if rng < 36:
                        self.health -= (5 + (3 * self.magic) - self.defense)
                    else:
                        m.health -= (5 + (3 * self.magic) - m.defense )
                if spell_cast == "Jebaited":
                    for i in range(136):
                        jebaited = pygame.transform.scale(jebaited_image, (i, i))
                        jebaitedpos = jebaited_image.get_rect()
                        jebaitedpos.x = m.rect.x - 92
                        jebaitedpos.y = m.rect.y
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        screen.blit(jebaited, jebaitedpos)
                        clock.tick(92)
                        pygame.display.flip()

                    self.counterAttack = True
                if spell_cast == "PogChamp Armor":
                    self.armorReduce = 2
                    for i in range(180):
                        pogchamp = pygame.transform.scale(pogchamp_image, (96, 96))
                        pogchamppos = pogchamp_image.get_rect()
                        pogchamppos.x = self.rect.x + 64
                        pogchamppos.y = self.rect.y - (180 - i)
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        clock.tick(120)
                        pygame.display.flip()

                    self.defense += 7
                if spell_cast == "FrankerZ":
                    frankerz = pygame.transform.scale(frankerz_image, (96, 96))
                    frankerzpos = frankerz_image.get_rect()
                    frankerzpos.x = self.rect.x
                    frankerzpos.y = self.rect.y
                    for i in range(100):
                        if i < 25:
                            frankerzpos.x += (i)
                            frankerzpos.y -= i
                        elif i < 50:
                            frankerzpos.x += i-25
                            frankerzpos.y += i-25
                        elif i < 75:
                            frankerzpos.x -= i-50
                            frankerzpos.y += i-50
                        else:
                            frankerzpos.x -= i-75
                            frankerzpos.y -= i-75
                        frankerz = pygame.transform.rotate(frankerz_image, i * 15)
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        screen.blit(frankerz, frankerzpos)
                        clock.tick(50)
                        pygame.display.flip()
                    dmg = 5 + self.magic
                    self.health += dmg/2.0
                    m.health -= dmg - m.defense
                if spell_cast == "KappaPride":
                    for i in range(180):
                        kappapride = pygame.transform.scale(kappapride_image, (64, 64))
                        kappapridepos = kappapride_image.get_rect()
                        kappapridepos.x = self.rect.x + 7*i
                        kappapridepos.y = self.rect.y
                        heart = pygame.transform.scale(heart_image, (96, 96))
                        heartpos = heart_image.get_rect()
                        heartpos.x = m.rect.x
                        heartpos.y = m.rect.y - i
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)
                        if i < 90:
                            screen.blit(kappapride, kappapridepos)
                        else:
                            screen.blit(heart, heartpos)
                        clock.tick(90)
                        pygame.display.flip()
                    m.health -= 5 + (0.5 * self.magic) - m.defense
                    m.noAttack = True
                screen.blit(herohealth, herohealthpos)
                screen.blit(monsterhealth, monsterhealthpos)

                if m.noAttack == True:
                    m.noAttack = False
                else:
                    for i in range(0,17):
                        if i > 1 and i <= 6:
                            m.rect.x -= 15
                        if i == 8:
                            if self.counterAttack == True:
                                m.health -= (m.strength * 1.5) - m.defense
                                self.counterAttack = False
                            else:
                                if self.defense > m.strength:
                                    pass
                                else:
                                    self.health -= m.strength - self.defense

                        if i > 10 and i <= 15:
                            m.rect.x += 15
                        monster_group.draw(screen)
                        screen.fill(black)
                        screen.blit(background, backgroundrect)
                        screen.blit(self.image, self.rect)
                        screen.blit(m.image, m.rect)
                        screen.blit(spellTitle1, spellTitle1pos)
                        screen.blit(spellTitle2, spellTitle2pos)
                        screen.blit(spellTitle3, spellTitle3pos)
                        screen.blit(herohealth, herohealthpos)
                        screen.blit(monsterhealth, monsterhealthpos)
                        screen.blit(maintitle, maintitlepos)
                        screen.blit(spellchoicetitle, spellchoicetitlepos)
                        if self.counterAttack == True:
                            screen.blit(jebaited, jebaitedpos)
                        if not self.armorReduce == 0:
                            screen.blit(pogchamp, pogchamppos)

                        clock.tick(fps)
                        pygame.display.flip()



            screen.fill(black)
            screen.blit(background, backgroundrect)
            screen.blit(self.image, self.rect)
            screen.blit(m.image, m.rect)
            screen.blit(spellTitle1, spellTitle1pos)
            screen.blit(spellTitle2, spellTitle2pos)
            screen.blit(spellTitle3, spellTitle3pos)
            screen.blit(herohealth, herohealthpos)
            screen.blit(monsterhealth, monsterhealthpos)
            screen.blit(maintitle, maintitlepos)
            screen.blit(spellchoicetitle, spellchoicetitlepos)
            if not self.armorReduce == 0:
                screen.blit(pogchamp, pogchamppos)

            if m.health <= 0:
                monsterhealth = healthfont.render(str(m.health) + "HP", 1, (255, 0, 0))
                herohealth = healthfont.render(str(self.health) + "HP", 1, (0, 255, 0))
                m.image = pygame.transform.rotate(m.image, -90)
                for i in range(180):
                    screen.fill(black)
                    screen.blit(background, backgroundrect)
                    screen.blit(self.image, self.rect)
                    screen.blit(m.image, m.rect)
                    screen.blit(herohealth, herohealthpos)
                    screen.blit(monsterhealth, monsterhealthpos)
                    screen.blit(victorytitle, victorytitlepos)

                    clock.tick(fps)
                    pygame.display.flip()
                fighting = False
            if self.health <= 0:
                herohealth = healthfont.render(str(self.health) + "HP", 1, (0, 255, 0))
                self.image = pygame.transform.rotate(self.image, 90)
                for i in range(180):
                    screen.fill(black)
                    screen.blit(background, backgroundrect)
                    screen.blit(self.image, self.rect)
                    screen.blit(m.image, m.rect)
                    screen.blit(herohealth, herohealthpos)
                    screen.blit(monsterhealth, monsterhealthpos)
                    screen.blit(defeattitle, defeattitlepos)

                    clock.tick(fps)
                    pygame.display.flip()
                fighting = False
                global intro
                intro = True
                global play
                play = False
            clock.tick(fps)
            pygame.display.flip()
        self.magic = savemagic
        self.rect.x = savespotx
        self.rect.y = savespoty

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = self.type(Type)
    def type(self, Type):
        if Type == "G":
            self.image = pygame.transform.scale(floor_tile, (32,32))
            type = "G"
        if Type == "A":
            type = "A"
        return type

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64,64)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = self.type(Type)
        self.jumpCounter = 0
        self.jumpCD = 0
        self.mspeed = 5
        self.grounded = False
        self.dir = 1
        self.noAttack = False
        self.hitanimation = 0

    def type(self, Type):
        if Type == "imaqtpie":
            self.image = qtp_right_face
            self.health = random.randrange(70,90)
            self.strength = random.randrange(9,17)
            self.defense = random.randrange(1,4)
            self.exp = random.randrange(50,81)
            mtype = "imaqtpie"
        if Type == "zard":
            self.image = zard_right_face
            self.health = random.randrange(150,200)
            self.strength = random.randrange(21,32)
            self.defense = random.randrange(3,6)
            self.exp = random.randrange(50,81)
            mtype = "zard"
        return mtype
    def update(self, np_tile_group):
        self.rect.y += 9
        left = right = False
        if self.jumpCD is not 0:
            self.jumpCD -= 1
            self.dir = random.randint(1, 2)
        if self.dir is 1 and self.jumpCD is 0 and self.grounded:
            right = True
            if self.type == "imaqtpie":
                self.image = qtp_right_face
            elif self.type == "zard":
                self.image = zard_right_face
            if self.jumpCounter < 13 and self.rect.x < WIN_W - 64:
                self.rect.x += self.mspeed
            else:
                self.grounded = False
            self.jumpCounter += .7
            self.rect.y -= 15 - self.jumpCounter
        elif self.dir is 2 and self.jumpCD is 0:
            left = True
            if self.type == "imaqtpie":
                self.image = qtp_left_face
            elif self.type == "zard":
                self.image = zard_left_face
            if self.jumpCounter < 13 and self.rect.x > 0:
                self.rect.x -= self.mspeed
            else:
                self.grounded = False
            self.jumpCounter += .7
            self.rect.y -= 15 - self.jumpCounter
        self.collide(np_tile_group, left, right)
    def collide(self, np_tile_group, left, right):
        for p in np_tile_group:
            if pygame.sprite.collide_rect(self, p):
                if not self.grounded:
                    self.jumpCD = 90
                    self.jumpCounter = 0
                self.grounded = True
                self.rect.y -= 9
            if pygame.sprite.collide_rect(self, p) and right:
                self.rect.x -= self.mspeed
                #if self.jumpCounter < 9:
                 #   self.rect.y += 9
                #self.jumpCounter += 1
            if pygame.sprite.collide_rect(self, p) and left:
                self.rect.x += self.mspeed
                #if self.jumpCounter < 9:
                 #   self.rect.y += 9
                #self.jumpCounter += 1

def roomSet(room,p_tile, np_tile):
    with open(room, "r") as f:
        data = f.readlines()
        x = y = 0
        for line in data:
            for i in line:
                if i is "G":
                    p = Tile(x, y, "G")
                    np_tile.add(p)
                if i is "A":
                    pass
                x += 32
            y += 32
            x = 0


def main():
    pygame.display.set_caption("Emote Wizard")
    global intro
    global play
    intro = True
    play = False
    p_tile_group = pygame.sprite.Group()
    np_tile_group = pygame.sprite.Group()
    roomSet("room1.txt", p_tile_group, np_tile_group)
    wizard = Hero()
    qtp = Monster(500, 300, "imaqtpie")
    monster_group = pygame.sprite.Group()
    monster_group.add(qtp)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                pygame.display.flip()
                pygame.time.wait(1)
                intro = False
                play = True
        introfont = pygame.font.Font(None, 80)
        introfont2 = pygame.font.Font(None, 60)
        introtitle = introfont.render("Welcome to Emote Wizard", 1, white)
        introtitle2 = introfont2.render("Press Enter or Click to Start", 1, white)
        introtitlepos = introtitle.get_rect()
        introtitle2pos = introtitle.get_rect()
        introtitlepos.centerx = screen.get_rect().centerx
        introtitlepos.centery = screen.get_rect().centery - 200
        introtitle2pos.centerx = screen.get_rect().centerx + 75
        introtitle2pos.centery = screen.get_rect().centery + 200
        screen.fill(black)
        screen.blit(twitchlogo, twitchlogorect)
        screen.blit(introtitle, introtitlepos)
        screen.blit(introtitle2, introtitle2pos)

        clock.tick(fps)
        pygame.display.flip()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                sys.exit()
        global elapsedtime
        elapsedtime += 1
        screen.fill(white)
        screen.blit(background, backgroundrect)
        p_tile_group.draw(screen)
        np_tile_group.draw(screen)
        wizard.update(np_tile_group, monster_group)
        screen.blit(wizard.image, (wizard.rect.x, wizard.rect.y))
        monster_group.update(np_tile_group)
        monster_group.draw(screen)



        clock.tick(fps)
        pygame.display.flip()
    if (intro):
        main()

if __name__ == "__main__":
    main()
