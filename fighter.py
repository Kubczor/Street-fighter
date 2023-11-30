import pygame

class Fighter():
    def __init__(self, player, x , y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_cooldown = 0
        self.running = False
        self.attack_type = 0
        self.health = 100
        self.special = 0
        self.alive = True
        self.hit = False
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:stoi 1:biegnie 2:skok 3:atak1 4:atak2 5:obrazenia 6:smierc
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.attack_sound = sound

        self.update_time = pygame.time.get_ticks()



    def load_images(self, sprite_sheet, animation_steps):
        #wyciagniecie klatek z pliku png
        animation_list = []
        for y, animation in enumerate(animation_steps):       
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    def move(self, s_width, s_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #poruszanie sie
        key = pygame.key.get_pressed()
        
        #sprawdzanie, ktory to gracz
        if self.alive == True and round_over == False:
            if self.player == 1 and self.hit == False:
                #predkosc
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                #skok
                if key[pygame.K_w] and self.jump == False and self.hit == False:
                    self.vel_y=-20
                    self.jump = True
            
                #grawitacja 
                dy += self.vel_y
                self.vel_y += GRAVITY


                if self.attacking == False:
                    #atak
                    if key[pygame.K_r] or key[pygame.K_t]:
                        self.attack(surface, target)

                        #rodzaj ataku
                        if key[pygame.K_r]:
                            self.attack_type = 1
                        if key[pygame.K_t]:    
                            self.attack_type = 2
        if self.alive == True and round_over == False:
            if self. player == 2 and self.hit == False:
                #predkosc
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                #skok
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y=-20
                    self.jump = True
            
                #grawitacja 
                dy += self.vel_y
                self.vel_y += GRAVITY
                

                if self.attacking == False:
                    #atak
                    if key[pygame.K_o] or key[pygame.K_p]:
                        self.attack(surface, target)

                        #rodzaj ataku
                        if key[pygame.K_o]:
                            self.attack_type = 1
                        if key[pygame.K_p]:    
                            self.attack_type = 2                       

            #dluzsze przerwy miedzy atakami
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
    
            

        #ramka gry
        if self.rect.left + dx < 0:
            dx =- self.rect.left
        if self.rect.right + dx > s_width:
            dx = s_width - self.rect.right
        if self.rect.bottom + dy > s_height - 110:
            self.vel_y = 0
            dy = s_height - 110 - self.rect.bottom
            self.jump = False

        #poruszanie sie    
        self.rect.x += dx
        self.rect.y += dy

        #odwracanie sie
        if self.alive == True:
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

    #zmiana animacji
    def update(self):
        if self.alive <= False:
            self.update_action(6)
            self.health = 0
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:   
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)    
        
        animation_cd = 50
        #akutalizacja animacji
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            #sprawdzenie czy przeciwnik jest martwy
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0
            #sprawdzanie czy animacja ataku sie skonczyla
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
            #sprawdzanie czy animacja uderzenai sie skonczyla
                if self.action == 5:
                    self.hit = False
                    #jezeli gracz byl w srodku ataku, uderzenie ma przerwac animacje
                    self.attacking = False
                    self.attack_cooldown = 30
            




    def update_action(self, new_action):
        #sprawdz czy to nowa animacja
        if new_action != self.action:
            self.action = new_action
            #powrot do pierwszej klatki z rzedu
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx -(2*self.rect.width*self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
               
               #ładowanie ataku specjalnego
                if self.special + 10 > 50:
                    self.special = 50
                else:
                    self.special += 10
                if target.special + 15 > 50:    
                    target.special = 50
                else:
                    target.special += 15
                    
                
                if target.health <= 0:
                    target.alive = False
                   
            
            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        

        
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))