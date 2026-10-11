import random
import sys
import pygame
import os

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
prep_color = (150, 100, 200)    # Purple

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cookatime Recipe MVP")
clock = pygame.time.Clock()

def main():
    running = True

    # Attributes
    player_width = 40
    player_height = 40
    player_x = screen_width // 2 - player_width // 2
    player_y = 300

    player_speed = 4.5
    dash_speed = 14

    last_dx = 0
    last_dy = 1

    dash_left = 0
    dash_cooldown = 0
    stamina = 100

    score = 0
    carried_item = None
    prep_item = None

    order_target = random.randint(4, 7)
    orders_completed = 0
    shift_active = True

    tutorial_active = True
    tutorial_page = 1
    total_pages = 3

    shift_start_ticks = 0
    final_shift_time = 0  # Frozen time when shift ends
    session_best_time = float('inf')
    stars_awarded = 0

    recipes = ["Tomato Soup", "Lettuce Salad", "Lettuce Tomato Medley Salad"]
    current_order = random.choice(recipes)

    tomato_station = pygame.Rect(80, 150, 140, 55)
    lettuce_station = pygame.Rect(330, 150, 140, 55)
    prep_station = pygame.Rect(580, 150, 140, 55)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    star_filled_path = os.path.join(script_dir, "star_filled.png")
    star_empty_path = os.path.join(script_dir, "star_empty.png")

    star_filled_raw = pygame.image.load(star_filled_path).convert_alpha()
    star_empty_raw = pygame.image.load(star_empty_path).convert_alpha()
    
    icon_size = (30, 30)
    
    star_filled = pygame.transform.smoothscale(star_filled_raw, icon_size)
    star_empty = pygame.transform.smoothscale(star_empty_raw, icon_size)

    customer_y_offset = 0
    customer_leaving = False

    player_rect = pygame.Rect(0, 0, 0, 0)
    while running:

        if not tutorial_active and shift_active:
            current_time = (pygame.time.get_ticks() - shift_start_ticks) / 1000
        else:
            current_time = final_shift_time

        # 1 Constant Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    if dash_cooldown == 0 and dash_left == 0 and stamina >= 100:
                        dash_left = 10
                        dash_cooldown = 45
                        stamina = 0
                elif event.key == pygame.K_SPACE:
                    if tutorial_active:
                        tutorial_page += 1
                        if tutorial_page > total_pages:
                            tutorial_active = False
                            shift_start_ticks = pygame.time.get_ticks()
                    elif shift_active:
                        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

                    if player_rect.colliderect(tomato_station.inflate(20, 20)):
                        carried_item = "Tomato"
                    elif player_rect.colliderect(lettuce_station.inflate(20, 20)):
                        carried_item = "Lettuce"

                    elif player_rect.colliderect(prep_station.inflate(20, 20)):
                        if carried_item in ["Tomato", "Lettuce"]:
                            if prep_item is None:
                                prep_item = carried_item
                                carried_item = None
                            elif prep_item != carried_item:
                                carried_item = "Lettuce Tomato Medley Salad"
                                prep_item = None
                        elif carried_item is None:
                            if prep_item == "Tomato":
                                carried_item = "Tomato Soup"
                                prep_item = None
                            elif prep_item == "Lettuce":
                                carried_item = "Lettuce Salad"
                                prep_item = None

                    customer_rect = pygame.Rect(280, 530, 240, 50)
                    if player_rect.colliderect(customer_rect.inflate(20, 20)):
                        if carried_item == current_order:
                            score += 100
                            orders_completed += 1
                            carried_item = None
                            customer_leaving = True

                            if orders_completed >= order_target:
                                shift_active = False
                                final_shift_time = (pygame.time.get_ticks() - shift_start_ticks) / 1000
                                avg_time_per_order = final_shift_time / order_target

                                threshold = order_target * 3
                                if final_shift_time <= threshold:
                                    stars_awarded = 3
                                elif final_shift_time <= threshold * 1.5:
                                    stars_awarded = 2
                                else:
                                    stars_awarded = 1

                                if avg_time_per_order < session_best_time:
                                    session_best_time = avg_time_per_order
                            else:
                                current_order = random.choice(recipes)

                elif event.key == pygame.K_r and not shift_active and not tutorial_active:
                    orders_completed = 0
                    order_target = random.randint(4, 7)
                    score = 0
                    shift_start_ticks = pygame.time.get_ticks()
                    shift_active = True
                    current_order = random.choice(recipes)

        if dash_cooldown > 0:
            dash_cooldown -= 1
        
        if stamina < 100 and dash_left == 0:
            stamina += 1.5
        
        if customer_leaving:
            customer_y_offset += 4
            if customer_y_offset > 60:
                customer_y_offset = 0
                customer_leaving = False

        # 2 Game States
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
    
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        if dx != 0 or dy != 0:
            last_dx, last_dy = dx, dy
            if dx != 0 and dy != 0:
                last_dx *= 0.7071
                last_dy *= 0.7071

        ## Diagonal Speed Calculation
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

        font_title = pygame.font.SysFont(None, 22)
        font_large = pygame.font.SysFont(None, 26)
        font_small = pygame.font.SysFont(None, 18)

        ## Draw Stations
        pygame.draw.rect(screen, tomato_color, tomato_station, border_radius = 8)
        pygame.draw.rect(screen, lettuce_color, lettuce_station, border_radius = 8)
        pygame.draw.rect(screen, prep_color, prep_station, border_radius = 8)

        t_text = font_title.render("Tomato [SPACE]", True, (255, 255, 255))
        screen.blit(t_text, (tomato_station.centerx - t_text.get_width() // 2, tomato_station.centery - t_text.get_height() // 2))

        l_text = font_title.render("Lettuce [SPACE]", True, (255, 255, 255))
        screen.blit(l_text, (lettuce_station.centerx - l_text.get_width() // 2, lettuce_station.centery - l_text.get_height() // 2))

        prep_label = f"Prep: {prep_item if prep_item else 'Empty'}"
        p_text = font_title.render(prep_label, True, (255, 255, 255))
        screen.blit(p_text, (prep_station.centerx - p_text.get_width() // 2, prep_station.centery - p_text.get_height() // 2))
        
        ## Boundary Line
        pygame.draw.line(screen, accent_color, (40, 90), (760, 90), 3)

        ## Header and Final Stats
        screen.blit(font_title.render("Cookatime Shifts MVP", True, accent_color), (40, 15))
        score_text = font_large.render(f"Score: {score}", True, accent_color)
        screen.blit(score_text, (screen_width - 200, 15))

        screen.blit(font_small.render("WASD: Move | SHIFT: Dash | SPACE: Grab/Serve", True, text_color), (40, 45))
        item_text = font_title.render(f"Carrying: {carried_item if carried_item else 'Nothing'}", True, text_color)
        screen.blit(item_text, (screen_width - 200, 45))

        best_str = f"{session_best_time:.2f}s/ord" if session_best_time != float('inf') else "None"
        screen.blit(font_small.render(f"Session Best: {best_str}", True, text_color), (40, 70))
        
        pygame.draw.rect(screen, (70, 70, 90), (screen_width - 200, 72, 120, 12), border_radius = 4)
        pygame.draw.rect(screen, accent_color, (screen_width - 200, 72, int(1.2 * stamina), 12), border_radius = 4)
        screen.blit(font_small.render("Stamina", True, text_color), (screen_width - 255, 70))

        if shift_active:
            timer_text = font_small.render(f"Time: {current_time:.1f}s", True, accent_color)
            screen.blit(timer_text, (250, 70))

        ## Customer Stuff
        if shift_active and not tutorial_active:
            order_text = font_large.render(f"Order: {current_order}", True, text_color)
            progress_text = font_small.render(f"Shift Progress: {orders_completed}/{order_target} orders", True, text_color)
            
            box_width = max(260, order_text.get_width() + 40)
            order_box = pygame.Rect(400 - box_width // 2, 530, box_width, 55)
            
            pygame.draw.rect(screen, (50, 50, 70), order_box, border_radius = 10)
            pygame.draw.rect(screen, accent_color, order_box, 2, border_radius = 10)
            
            screen.blit(order_text, (order_box.centerx - order_text.get_width() // 2, order_box.y + 8))
            screen.blit(progress_text, (order_box.centerx - progress_text.get_width() // 2, order_box.y + 32))

            ### Customer Icon
            cust_x, cust_y = order_box.x - 45, 545 + customer_y_offset
            pygame.draw.circle(screen, (220, 180, 140), (cust_x, cust_y), 14)
            pygame.draw.rect(screen, (100, 140, 200), (cust_x - 12, cust_y + 14, 24, 16), border_radius=4)
        elif not shift_active and not tutorial_active:
            summary_box = pygame.Rect(200, 180, 400, 280)
            pygame.draw.rect(screen, (40, 40, 55), summary_box, border_radius = 12)
            pygame.draw.rect(screen, accent_color, summary_box, 3, border_radius = 12)

            win_title = font_large.render("Shift Complete!", True, accent_color)
            screen.blit(win_title, (summary_box.centerx - win_title.get_width() // 2, summary_box.y + 20))

            stat_line1 = font_title.render(f"Total Time: {current_time:.2f} seconds", True, text_color)
            screen.blit(stat_line1, (summary_box.centerx - stat_line1.get_width() // 2, summary_box.y + 75))

            avg_line = font_title.render(f"Avg Time/Order: {current_time / order_target:.2f}s", True, text_color)
            screen.blit(avg_line, (summary_box.centerx - avg_line.get_width() // 2, summary_box.y + 110))

            total_stars_width = (3 * 35) - 5
            star_start_x = summary_box.centerx - (total_stars_width // 2)
            star_y_pos = summary_box.y + 158
            star_spacing = 35
            
            for i in range(3):
                star_x = star_start_x + (i * star_spacing)
                if i < stars_awarded:
                    screen.blit(star_filled, (star_x, star_y_pos))
                else:
                    screen.blit(star_empty, (star_x, star_y_pos))
        
            restart_prompt = font_small.render("Press 'R' to start next shift or ESC to quit", True, text_color)
            screen.blit(restart_prompt, (summary_box.centerx - restart_prompt.get_width() // 2, summary_box.y + 230))

        if tutorial_active:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(180)
            overlay.fill((10, 10, 15))
            screen.blit(overlay, (0, 0))

            tut_box = pygame.Rect(175, 140, 450, 320)
            pygame.draw.rect(screen, (40, 40, 55), tut_box, border_radius = 12)
            pygame.draw.rect(screen, accent_color, tut_box, 3, border_radius = 12)

            tut_title = font_large.render(f"How to Play (Step {tutorial_page} / {total_pages})", True, accent_color)
            screen.blit(tut_title, (tut_box.centerx - tut_title.get_width() // 2, tut_box.y + 20))

            if tutorial_page == 1:
                line1 = "Welcome to Cookatime, Chef!"
                line2 = "• Use WASD or arrow keys to move around the kitchen."
                line3 = "• Hold SHIFT to dash, but watch your stamina meter!"
            elif tutorial_page == 2:
                line1 = "Gathering & Preparing Ingredients:"
                line2 = "• Walk to the tomato or lettuce stations & press SPACE"
                line3 = "• Drop items at the prep station to combine/make recipes!"
            elif tutorial_page == 3:
                line1 = "Serving Customers & Winning:"
                line2 = "• Deliver orders to the bottom counter and earn points"
                line3 = "• Finish all orders quickly to earn 3 gold stars!"

            screen.blit(font_title.render(line1, True, text_color), (tut_box.x + 30, tut_box.y + 85))
            screen.blit(font_title.render(line2, True, text_color), (tut_box.x + 30, tut_box.y + 130))
            screen.blit(font_title.render(line3, True, text_color), (tut_box.x + 30, tut_box.y + 175))

            prompt_text = font_large.render("Press [SPACE] to continue ->", True, accent_color)
            screen.blit(prompt_text, (tut_box.centerx - prompt_text.get_width() // 2, tut_box.y + 250))

        ## Sprite
        chef_color = dash_color if dash_left > 0 else default_color
        if not tutorial_active:
            pygame.draw.rect(screen, chef_color, (player_x, player_y, player_width, player_height), border_radius = 8)
        
        if carried_item:
            ind_color = tomato_color if "Tomato" in carried_item else (lettuce_color if "Lettuce" in carried_item else (200, 100, 200))
            pygame.draw.rect(screen, ind_color, (player_x + 10, player_y + 10, 20, 20), border_radius = 4)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()