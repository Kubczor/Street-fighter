import pygame
from fighter import Fighter

class Lowca(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, sound)
        # Add any additional attributes or modify existing ones specific to the SpecialFighter class
        self.special_attack = False
        self.poison = 0.05
        self.poisoning = False
       
    
    def special_ability(self, target):
        key = pygame.key.get_pressed()
        if key[pygame.K_y] and self.player == 1:
            if self.special == 50:
                self.special = 0
                self.special_attack = True
        if key[pygame.K_i] and self.player == 2:
            if self.special == 50:
                self.special = 0
                self.special_attack = True
        if self.special_attack == True and self.poisoning == True:
            target.health -= self.poison
            if target.health < 10:
                self.poison = 0
        

                

    # Override the move() method from the parent class
    def move(self, s_width, s_height, surface, target, round_over):
        # Implement the movement logic specific to SpecialFighter
        super().move(s_width, s_height, surface, target, round_over)
        # Add any additional logic or modifications specific to SpecialFighter's movement

    # Override the attack() method from the parent class
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx -(3*self.rect.width*self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                if self.special_attack == True:
                    self.poisoning = True

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
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
