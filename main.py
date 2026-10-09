import sys
import pygame

pygame.init()

screen_width = 800
screen_height = 600

bg_color = (30, 30, 40)         # Midnight blue
text_color = (245, 238, 220)    # Cream
accent_color = (255, 170, 90)   # Neon orange
default_color = (240, 198, 116)    # Buttery yellow
dash_color = (255, 220, 150) # Brighter when dashing

screen = pygame.display.set_mode((screen_width, screen_height)) # Screen Width 800, Screen Height 600
pygame.display.set_caption("Cookatime Prep Week 1")
clock = pygame.time.Clock()

def main():
    running = True

    # Attributes
    player_width = 50
    player_height = 50
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height // 2 - player_height // 2

    player_speed = 7
    dash_speed = 12

    last_dx = 0
    last_dy = 1

    dash_left = 0
    dash_cooldown = 0

    while running:
        # 1 Constant Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    if dash_cooldown == 0 and dash_left == 0:
                        dash_left = 10
                        dash_cooldown = 60

        if dash_cooldown > 0:
            dash_cooldown -= 1
        
        # 2 Game States
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
    
        ## Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        ## Vertical movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        ## Diagonal Cancellation
        if dx != 0 or dy != 0:
            last_dx, last_dy = dx, dy
            if dx != 0 and dy != 0:
                last_dx *= 0.7071
                last_dy *= 0.7071

        ## Dashing vs Movement
        if dash_left > 0:
            player_x += last_dx * dash_speed
            player_y += last_dy * dash_speed
            dash_left -= 1
        else:
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
            
            player_x += dx * player_speed
            player_y += dy * player_speed

        ## Boundaries
        if player_x < 50:
            player_x = 50
        elif player_x > screen_width - 50 - player_width:
            player_x = screen_width - 50 - player_width

        if player_y < 150:
            player_y = 150
        elif player_y > screen_height - 50 - player_height:
            player_y = screen_height - 50 - player_height
        
        # 3 Rendering and Graphics
        screen.fill(bg_color)

            # Boundary Line
        pygame.draw.line(screen, accent_color, (50, 140), (750, 140), 3)

            # Text
        font = pygame.font.SysFont(None, 32)
        title_surface = font.render("Cookatime Prep Week 1", True, accent_color)
        screen.blit(title_surface, (50, 30))

        instruction_surface = font.render("Use WASD or Arrow Keys to move, chef! Press ESC to exit", True, text_color)
        screen.blit(instruction_surface, (50, 70))

            # Sprite
        chef_color = dash_color if dash_left > 0 else default_color
        pygame. draw.rect(screen, chef_color, (player_x, player_y, player_width, player_height), border_radius = 8)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()