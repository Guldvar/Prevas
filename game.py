import pygame
import math
import sys
import random
import rollercoaster as rc

# ------------------------------------------------
# BIG, ALL-IN-ONE PYGAME BOILERPLATE:
#
#   Features:
#   - States: INTRO, GAME, PAUSE, GAME_OVER
#   - Delta time
#   - Scrolling background
#   - Basic bounding-box + circle collision
#   - Stub for per-pixel collision
#   - Simple animation
#   - Sound (music + SFX)
#   - Particles
#   - Optional text input (type your name in INTRO)
#   - Hints for tiling
#
#   It's well beyond a typical jam skeleton, but you
#   can strip it down or pick the bits you need.
# ------------------------------------------------

# ----------------- CONSTANTS --------------------
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600
FPS           = 60   # Target framerate

# Colors
COLOR_BG       = (50,  50,  50)   # Dark gray background
COLOR_WHITE    = (255, 255, 255)
COLOR_PLAYER   = (0,   255, 0)
COLOR_ENEMY    = (255, 0,   0)
COLOR_PARTICLE = (255, 200, 50)

# For the scrolling background
SCROLL_SPEED   = 100  # px/sec

# States
STATE_INTRO     = "INTRO"
STATE_GAME      = "GAME"
STATE_PAUSE     = "PAUSE"
STATE_GAME_OVER = "GAME_OVER"


# ----------------- COLLISION HELPERS --------------------
def rect_rect_collision(rect_a, rect_b):
    """
    Simple bounding-box collision. If they overlap, returns True.
    """
    return rect_a.colliderect(rect_b)

def circle_circle_collision(x1, y1, r1, x2, y2, r2):
    """
    Circle vs Circle collision.
    Returns True if distance between centers < sum of radii.
    """
    dist_sq = (x1 - x2)**2 + (y1 - y2)**2
    radius_sum = r1 + r2
    return dist_sq < (radius_sum * radius_sum)

def pixel_perfect_collision(sprite1, sprite2, offset_x, offset_y):
    """
    STUB for per-pixel collision detection, as per Lazy Foo #28.
    Not fully implemented here, but this is how you'd integrate it:
      1) Lock surfaces or convert to a pixel array.
      2) Check overlapping region for any pixel != transparent in both images.
    We'll just return False to show you where it would fit.
    """
    # For a real approach:
    #   - convert_alpha() on each surface
    #   - read pixel data from each surface
    #   - for each overlapping pixel: if both are non-transparent => collision
    return False


# ----------------- PARTICLE SYSTEM --------------------
class Particle:
    """
    A simple particle. This can be used for explosions, dust, etc.
    Position, velocity, lifetime, color. We'll just draw them as circles.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-50, 50)
        self.vy = random.uniform(-50, 50)
        self.life = random.uniform(0.5, 1.5)  # seconds
        self.color = COLOR_PARTICLE
        self.radius = random.randint(2, 5)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Optionally reduce radius over time or fade color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)




# ----------------- MAIN GAME CLASS --------------------
class Game:
    def __init__(self):
        """
        1) Init Pygame and screen
        2) Load or create assets (player sprite, enemies, background, sounds)
        3) Set initial state (INTRO)
        4) Prepare a dictionary for animations if needed
        5) Setup text input for player name
        6) Initialize any desired systems (particles, scoreboard, etc.)
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mega Boilerplate")
        self.clock = pygame.time.Clock()

        # Current game state
        self.state = STATE_INTRO

        # Optional: track time in each state if needed
        self.state_time = 0.0

        # Scrolling background: Load or generate
        # For a tile-based approach, you'd store a 2D array of tiles and draw them with an offset.
        # We'll just do a single image repeated.
        self.bg_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_image.fill((70, 70, 100))  # a dull color
        self.bg_scroll_y = 0  # We'll scroll vertically. If you want horizontal, do bg_scroll_x.

        # If you had a real image: self.bg_image = pygame.image.load("scroll_bg.png").convert()
        # and you'd possibly store its height to replicate it.

        # Player and animation setup
        self.player_frames = []
        self.load_player_frames()
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.1  # switch frames every 0.1s
        self.player_rect = pygame.Rect(100, 200, 40, 40)  # bounding box for collision
        self.player_speed = 80
        self.player_health = 3
        self.moved = 0
        # Enemies
        self.enemy_image = pygame.Surface((30, 30))
        self.enemy_image.fill(COLOR_ENEMY)
        self.enemies = []
        self.spawn_timer = 0.0
        self.spawn_interval = 2.0

        # Particles
        self.particles = []
        self.vel_y = 0

        self.coaster = rc.Rollercoaster()
        #Bullets 
        self.bullets = []
        # Score
        self.score = 0

        # Rollercoaster
        self.coaster = rc.Rollercoaster()
        self.coaster_timer = 0

        # Font for text rendering
        self.font = pygame.font.SysFont(None, 24)

        # For the INTRO text input (type your name, for example)
        self.player_name = ""

        # Load or init sound/music
        self.init_audio()

        # Flag to run main loop
        self.running = True

    def init_audio(self):
        """
        Load music and sounds. For real usage, do:
          pygame.mixer.music.load("music.ogg")
          pygame.mixer.music.play(-1)
        """
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        # This tries to start an audio device; handle exceptions if needed
        # For placeholders:
        # pygame.mixer.music.load("background_music.ogg")
        # pygame.mixer.music.play(-1)

        # self.sfx_collision = pygame.mixer.Sound("collision.wav")

    def load_player_frames(self):
        """
        Load frames for animated player. We'll just create colored squares for demonstration.
        In a real game, you'd do something like:
          frame_img = pygame.image.load(f"player_frame{i}.png").convert_alpha()
          self.player_frames.append(frame_img)
        """
        # Let's pretend we have 4 frames
        for i in range(4):
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Just fill with a different shade each time
            surf.fill((0, 255 - i*50, 0))
            self.player_frames.append(surf)

    def run(self):
        """
        Main loop: keep ticking until self.running = False.
        1) dt = time since last frame
        2) handle_events()
        3) update(dt)
        4) draw()
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    # ----------------- EVENT HANDLING -----------------
    def handle_events(self):
        """
        Dispatch events to state-specific handlers if needed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # If we're in INTRO, we might want to handle text input
                if self.state == STATE_INTRO:
                    self.handle_intro_input(event)
                elif self.state == STATE_GAME:
                    # Handle game-specific input
                    if event.key == pygame.K_c:
                        self.player_shoot(event)
                
                    if event.key == pygame.K_p:
                        # Toggle pause
                        self.state = STATE_PAUSE
                        self.state_time = 0.0
                elif self.state == STATE_PAUSE:
                    if event.key == pygame.K_p:
                        # Return to game
                        self.state = STATE_GAME
                        self.state_time = 0.0
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        # Restart the entire game
                        self.restart_game()

    def player_shoot(self, event):
        player_pos = self.player_rect.center
        
        mouse_pos = pygame.mouse.get_pos()
        
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]

        distance = math.hypot(dx, dy)
        if distance > 0:  
            dx /= distance
            dy /= distance

        bullet = {
            'rect': pygame.Rect(player_pos[0] - 5, player_pos[1] - 5, 10, 10),
            'velocity': (dx * 300, dy * 300),  # Speed of 300 pixels per second
            'color': (0, 200, 255)  # Cyan color
        }

        self.bullets.append(bullet)
        
        # We'll need to add code to update and draw projectiles
        # in update_game() and draw_game() methods
        
    def handle_intro_input(self, event):
        """
        If we want to let the player type their name or press Enter to start the game.
        """
        if event.key == pygame.K_RETURN:
            # Move on to the GAME state
            self.state = STATE_GAME
            self.state_time = 0.0
            # Possibly do something with self.player_name
        elif event.key == pygame.K_BACKSPACE:
            # Remove last character
            if len(self.player_name) > 0:
                self.player_name = self.player_name[:-1]
        else:
            # If it's a letter, number, or symbol, append it
            # We'll keep it simple—no shift or special keys
            char = event.unicode
            if char.isprintable():
                self.player_name += char

    # ----------------- UPDATE LOGIC -----------------
    def update(self, dt):
        """
        State machine approach: update only the relevant state’s logic.
        """
        self.state_time += dt

        if self.state == STATE_INTRO:
            self.update_intro(dt)
        elif self.state == STATE_GAME:
            self.update_game(dt)
        elif self.state == STATE_PAUSE:
            self.update_pause(dt)
        elif self.state == STATE_GAME_OVER:
            self.update_game_over(dt)

    def update_intro(self, dt):
        """
        Possibly animate a title screen, or do nothing but wait for input.
        We'll do minimal logic here.
        """
        # If you want a fancy animated background, you can do it here
        self.update_scrolling_bg(dt)

    def update_game(self, dt):
        """
        Main gameplay logic:
         - Scroll background
         - Animate player sprite
         - Move player
         - Spawn/move enemies
         - Collisions
         - Update particles
         - Check if health <= 0 => GAME_OVER
        """
        # 1) Scroll background
        self.update_scrolling_bg(dt)

        # 2) Animate player
        self.update_player_animation(dt)

        # 3) Move player with WASD (or arrow keys)
        self.update_player_movement(dt)

        # 4) Enemies
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_enemy()

        self.update_enemies(dt)

        # 5) Particles
        self.update_particles(dt)
        
        # Update bullets
        self.update_bullets(dt)
        
        # 6) Check if dead
        if self.player_health <= 0:
            self.state = STATE_GAME_OVER
            self.state_time = 0.0

        self.coaster_timer += dt
        if(self.coaster_timer > 0.05):
            print(self.coaster.update())
            print(self.coaster_timer)
            self.coaster_timer = 0

    def update_pause(self, dt):
        """
        Pause logic—basically do nothing except wait for unpause input.
        You could animate a "paused" overlay if you like.
        """
        pass

    def update_game_over(self, dt):
        """
        Game over screen logic. Maybe play a final animation, or press R to restart.
        """
        # You could add a timer before letting them restart.
        # We'll do nothing special here besides rely on handle_events().
        pass

    # ----------- HELPER UPDATES -----------
    def update_scrolling_bg(self, dt):
        """
        Scroll the background vertically. We'll just shift our "bg_scroll_y" up
        and wrap it so it loops. If you want a bigger background image, you can
        draw it multiple times or do a camera offset for tile-based games.
        """
        self.bg_scroll_y += SCROLL_SPEED * dt
        # If the background is the same size as the window, we can just wrap it once
        if self.bg_scroll_y >= WINDOW_HEIGHT:
            self.bg_scroll_y = 0

    def update_player_animation(self, dt):
        """
        Cycle through player frames over time.
        """
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            self.frame_timer = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.player_frames)

    def update_player_movement(self, dt):
        """
        WASD movement with bounding-box collision or screen clamp.
        If you want fancy collisions with platforms or shapes,
        implement that here.
        """
        
        
        # Calculate the current position on the coaster
        keys = pygame.key.get_pressed()
        move_x = 0  # Constant forward movement

        # Find which segment of the coaster we're on
        segment_width = 80
        current_segment = min(len(self.coaster.points) - 2, self.player_rect.x // segment_width)

        # Calculate interpolation point within segment (0.0 to 1.0)
        segment_progress = (self.player_rect.x % segment_width) / segment_width

        # Linear interpolation between two points on the coaster
        start_y = 400 - self.coaster.points[current_segment] * 40
        end_y = 400 - self.coaster.points[current_segment + 1] * 40
        target_y = start_y + segment_progress * (end_y - start_y) - 30

        # Smooth movement toward the target y position
        self.player_rect.y += (target_y - self.player_rect.y) * 0.2

        # Handle jump with gravity
        if keys[pygame.K_SPACE] and abs(self.player_rect.y - target_y) < 5:
            self.vel_y = -15

        # Apply gravity
        self.vel_y += 0.8
        self.player_rect.y += self.vel_y

        # Don't fall below the coaster
        if self.player_rect.y > target_y:
            self.player_rect.y = target_y
            self.vel_y = 0

        # Move forward
        self.player_rect.x += int(move_x * self.player_speed * dt)
        self.moved += int(move_x * self.player_speed * dt)

        # Keep player within screen bounds
        if self.player_rect.right > WINDOW_WIDTH:
            self.player_rect.right = WINDOW_WIDTH
        if self.player_rect.top < 0:
            self.player_rect.top = 0

    def update_bullets(self, dt):
        """
        Update bullet positions and check for collisions with enemies.
        """
        for bullet in self.bullets[:]:
            bullet['rect'].x += int(bullet['velocity'][0] * dt)
            bullet['rect'].y += int(bullet['velocity'][1] * dt)

            # Check for collision with enemies
            for enemy_rect in self.enemies[:]:
                if rect_rect_collision(bullet['rect'], enemy_rect):
                    self.enemies.remove(enemy_rect)
                    self.bullets.remove(bullet)
                    self.score += 1
                    
    def update_enemies(self, dt):
        """
        Move enemies downward and check collisions with player.
        """
        for enemy_rect in self.enemies[:]:
            enemy_rect.y += int(100 * dt)  # speed
            # Check bounding-box collision with player
            if rect_rect_collision(enemy_rect, self.player_rect):
                self.player_health -= 1
                self.enemies.remove(enemy_rect)
                # Could play a collision SFX, spawn some particles
                self.spawn_particles(self.player_rect.centerx, self.player_rect.centery, count=10)
                continue

            # Offscreen removal
            if enemy_rect.top > WINDOW_HEIGHT:
                self.enemies.remove(enemy_rect)

    def update_particles(self, dt):
        """
        Update and remove dead particles.
        """
        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)

    # ----------------- SPAWNING STUFF -----------------
    def spawn_enemy(self):
        """
        Just drop an enemy at the top in a random x position.
        """
        new_rect = self.enemy_image.get_rect()
        new_rect.x = random.randint(0, WINDOW_WIDTH - new_rect.width)
        new_rect.y = -new_rect.height
        self.enemies.append(new_rect)

    def spawn_particles(self, x, y, count=20):
        """
        Create 'count' new particles at the given position.
        """
        for _ in range(count):
            self.particles.append(Particle(x, y))

    # ----------------- DRAWING -----------------
    def draw(self):
        """
        Dispatch to state-specific draws.
        """
        if self.state == STATE_INTRO:
            self.draw_intro()
        elif self.state == STATE_GAME:
            self.draw_game()
        elif self.state == STATE_PAUSE:
            self.draw_pause()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_intro(self):
        """
        Maybe draw a scrolling background + a big "Press Enter to start" sign.
        """
        self.draw_scrolling_bg()

        # Title text
        title_text = self.font.render("Welcome to the Mega Boilerplate!", True, COLOR_WHITE)
        press_text = self.font.render("Press ENTER to start, or type your name below:", True, COLOR_WHITE)
        name_text  = self.font.render(self.player_name, True, COLOR_WHITE)

        # Center them roughly
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 200))
        press_rect = press_text.get_rect(center=(WINDOW_WIDTH//2, 250))
        name_rect  = name_text.get_rect(center=(WINDOW_WIDTH//2, 300))

        self.screen.blit(title_text, title_rect)
        self.screen.blit(press_text, press_rect)
        self.screen.blit(name_text, name_rect)

    def draw_game(self):
        """
        Draw the gameplay elements: background, player, enemies, particles, HUD
        """
        self.draw_scrolling_bg()

        # Draw player with animation
        frame_surf = self.player_frames[self.current_frame_index]
        self.screen.blit(frame_surf, self.player_rect)

        # Draw enemies
        for e in self.enemies:
            self.screen.blit(self.enemy_image, e)

        # Draw particles
        for p in self.particles:
            p.draw(self.screen)

        # Draw coaster
        for i in range(len(self.coaster.points) - 1):
            pygame.draw.line(self.screen, (0, 0, 0), (80 * i, 400 - self.coaster.points[i]*  30),
                              (80.6 * (i+1), 400 - self.coaster.points[i+1] *  30))

        for bullet in self.bullets:
            pygame.draw.rect(self.screen, bullet['color'], bullet['rect'])
        
        # HUD (health, score)
        hp_text    = self.font.render(f"HP: {self.player_health}", True, COLOR_WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_WHITE)
        pause_hint = self.font.render("Press P to pause", True, COLOR_WHITE)
        self.screen.blit(hp_text, (10, 10))
        self.screen.blit(score_text, (10, 30))
        self.screen.blit(pause_hint, (10, 50))

    def draw_pause(self):
        """
        Draw a "PAUSED" overlay on top of the game scene.
        """
        # First, draw the game under it (like a screenshot). Then overlay a semi-transparent rect.
        self.draw_game()

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # black with alpha 150
        self.screen.blit(overlay, (0, 0))

        paused_text = self.font.render("PAUSED - Press P to Resume", True, COLOR_WHITE)
        pt_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(paused_text, pt_rect)

    def draw_game_over(self):
        """
        Draw a game over screen with an option to restart.
        """
        self.draw_game()

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 0, 0, 150))  # a red-ish overlay
        self.screen.blit(overlay, (0, 0))

        go_text = self.font.render("GAME OVER", True, COLOR_WHITE)
        inst_text = self.font.render("Press R to Restart or ESC to Quit", True, COLOR_WHITE)
        go_rect  = go_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
        inst_rect= inst_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
        self.screen.blit(go_text, go_rect)
        self.screen.blit(inst_text, inst_rect)

    def draw_scrolling_bg(self):
        """
        Draw the scrolling background. We'll replicate self.bg_image
        at offset positions to achieve a continuous scroll effect.
        """
        # We'll scroll vertically downward, so the top of the image
        # is drawn at -self.bg_scroll_y and  -self.bg_scroll_y + image_height
        y1 = -self.bg_scroll_y
        y2 = y1 + WINDOW_HEIGHT

        # Blit the same image twice
        self.screen.blit(self.bg_image, (0, y1))
        self.screen.blit(self.bg_image, (0, y2))

    # ----------------- RESTART / EXIT -----------------
    def restart_game(self):
        """
        Reset game variables so we can start fresh from the GAME state.
        """
        self.state = STATE_GAME
        self.state_time = 0.0
        self.player_health = 3
        self.player_rect.x = 100
        self.player_rect.y = 300
        self.enemies.clear()
        self.particles.clear()
        self.score = 0
        self.spawn_timer = 0.0
        print("Game restarted!")


# -------------- ENTRY POINT --------------
if __name__ == "__main__":
    game = Game()
    game.run()
