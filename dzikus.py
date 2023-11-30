import pygame
from fighter import Fighter

class Dzikus(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, sound)
        # Add any additional attributes or modify existing ones specific to the SpecialFighter class
        self.special_attack = False
        self.speedy = 0
        self.jumping = 0
    
    def special_ability(self, target):
        key = pygame.key.get_pressed()
        if key[pygame.K_y] and self.player == 1:
            if self.special == 50:
                self.special = 0
                self.speedy += 5
                self.jumping += 5
        if key[pygame.K_i] and self.player == 2:
            if self.special == 50:
                self.special = 0
                self.speedy += 5
                self.jumping += 5
                

    # Override the move() method from the parent class
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
            if self. player == 1 and self.hit == False:
                #predkosc
                if key[pygame.K_a]:
                    dx = -SPEED - self.speedy
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED + self.speedy
                    self.running = True

                #skok
                if key[pygame.K_w] and self.jump == False and self.hit == False:
                    self.vel_y=-20 - self.jumping
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
                    dx = -SPEED - self.speedy
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED + self.speedy
                    self.running = True

                #skok
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y= -20 - self.jumping
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

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx -(3*self.rect.width*self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                if self.special_attack == False:
                    target.health -= 10
                else:
                    target.health -= 30
                    self.special_attack = False
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

    # Override the draw() method from the parent class
    def draw(self, surface):
        # Implement the drawing logic specific to SpecialFighter
        super().draw(surface)
        # Add any additional logic or modifications specific to SpecialFighter's drawing

    # Add any additional methods or modify existing ones as needed
