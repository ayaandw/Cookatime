import sys
import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600

bg_color = (30, 30, 40)         # Midnight blue
text_color = (245, 238, 220)    # Cream
accent_color = (255, 170, 90)   # Neon orange
default_color = (240, 198, 116) # Buttery yellow
dash_color = (255, 220, 150)    # Brighter when dashing
tomato_color = (235, 64, 52)    # Red
lettuce_color = (52, 235, 119)  # Green

screen = pygame.display.set_mode((screen_width, screen_height)) # Screen Width 800, Screen Height 600
pygame.display.set_caption("Cookatime MVP Ship 1.0")
clock = pygame.time.Clock()

def main():
    running = True

    # Attributes
    player_width = 40
    player_height = 40
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height // 2 - player_height // 2

    player_speed = 4.5
    dash_speed = 14

    last_dx = 0
    last_dy = 1

    dash_left = 0
    dash_cooldown = 0

    score = 0
    carried_item = None
    current_order = random.choice(["Tomato", "Lettuce"])

    tomato_station = pygame.Rect(180, 160, 90, 50)
    lettuce_station = pygame.Rect(530, 160, 90, 50)

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
                elif event.key == pygame.K_SPACE:
                    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

                    if player_rect.colliderect(tomato_station.inflate(20, 20)):
                        carried_item = "Tomato"
                    elif player_rect.colliderect(lettuce_station.inflate(20, 20)):
                        carried_item = "Lettuce"

                    customer_rect = pygame.Rect(280, 530, 240, 50)
                    if player_rect.colliderect(customer_rect.inflate(20, 20)):
                        if carried_item == current_order:
                            score += 1
                            current_order = random.choice(["Tomato", "Lettuce"])
                            carried_item = None

        if dash_cooldown > 0:
            dash_cooldown -= 1
        
        # 2 Game States
        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
    
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
        if player_x < 40:
            player_x = 40
        elif player_x > screen_width - 40 - player_width:
            player_x = screen_width - 40 - player_width

        if player_y < 140:
            player_y = 140
        elif player_y > screen_height - 60 - player_height:
            player_y = screen_height - 60 - player_height
        
        # 3 Rendering and Graphics
        screen.fill(bg_color)

        font_title = pygame.font.SysFont(None, 24)
        font_large = pygame.font.SysFont(None, 28)
        font_small = pygame.font.SysFont(None, 20)

        pygame. draw.line(screen, accent_color, (50, 140), (750, 140), 3)
        pygame.draw.rect(screen, tomato_color, tomato_station, border_radius = 6)
        pygame.draw.rect(screen, lettuce_color, lettuce_station, border_radius = 6)
        screen.blit(font_title.render("Tomato [SPACE]", True, (255, 255, 255)), (190, 175))
        screen.blit(font_title.render("Lettuce [SPACE]", True, (255, 255, 255)), (540, 175))
        
        ## Boundary Line
        pygame.draw.line(screen, accent_color, (40, 90), (760, 90), 3)

        ## Text

        screen.blit(font_title.render("Cookatime MVP Prep Week 1", True, accent_color), (40, 20))
        screen.blit(font_small.render("Listen up, chef! WASD/ARROWS: Move | SHIFT: Dash | SPACE: Grab/Serve", True, text_color), (40, 50))

        ## Customer Stuff
        order_box = pygame.Rect(280, 530, 240, 50)
        pygame.draw.rect(screen, (50, 50, 70), order_box, border_radius = 10)
        pygame.draw.rect(screen, accent_color, order_box, 2, border_radius = 10)
        order_text = font_large.render(f"Order: {current_order}", True, text_color)
        screen.blit(order_text, (order_box.centerx - order_text.get_width() // 2, order_box.centery - order_text.get_height() // 2))

        ## Score/Inventory
        score_text = font_large.render(f"Dishes Served: {score}", True, accent_color)
        screen.blit(score_text, (screen_width - 240, 20))

        item_text = font_title.render(f"Carrying: {carried_item if carried_item else 'Nothing'}", True, text_color)
        screen.blit(item_text, (screen_width - 240, 48))

        instruction_text = font_small.render("Listen up, chef! WASD/ARROWS: Move | SHIFT: Dash | SPACE: Grab/Serve", True, text_color)
        screen.blit(instruction_text, (50, 70))

        ## Sprite
        chef_color = dash_color if dash_left > 0 else default_color
        pygame. draw.rect(screen, chef_color, (player_x, player_y, player_width, player_height), border_radius = 8)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()