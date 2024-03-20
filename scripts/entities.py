import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        # Assigning the value passed by the game parameter to the object's game property
        # Atribuindo o valor passado pelo parâmetro game à propriedade game do objeto
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    # Creating the collision rectangle
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        # Vector that represents how much the entity should be moved in this frame
        # based on how much we want to force it to move on this particular frame,
        # plus how however much there already is on velocity
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # ----- X Collision -----
        # Actually moving
        self.pos[0] += frame_movement[0]
        # Defining the collision rectangle to the entity
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            # If there is a collision bewtween entity rectangle and the tile rectangle
            if entity_rect.colliderect(rect):
                # Moving right
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                # Moving left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # ----- Y Collision -----
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            # If there is a collision bewtween entity rectangle and the tile rectangle
            if entity_rect.colliderect(rect):
                # Moving down
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                # Moving up
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # 5 represents the maximum velocity while falling
        # If velocity is less than 5, then it takes the second part, increaing itself 0.1 per frame
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))