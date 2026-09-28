"""A small, self-contained Mario-style platform game.

Requires: pip install pygame
Run: python mario.py
"""
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24, bold=True)

GRAVITY = 0.7
SPEED = 5
JUMP = -13


class Player:
	def __init__(self):
		self.rect = pygame.Rect(70, 420, 34, 44)
		self.velocity = pygame.Vector2()
		self.coins = 0
		self.lives = 3

	def reset(self):
		self.rect.topleft = (70, 420)
		self.velocity.update(0, 0)

	def update(self, keys, platforms):
		self.velocity.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
		if keys[pygame.K_SPACE] and self.on_ground(platforms):
			self.velocity.y = JUMP
		self.velocity.y += GRAVITY

		self.rect.x += int(self.velocity.x)
		for platform in platforms:
			if self.rect.colliderect(platform):
				if self.velocity.x > 0:
					self.rect.right = platform.left
				elif self.velocity.x < 0:
					self.rect.left = platform.right

		self.rect.y += int(self.velocity.y)
		for platform in platforms:
			if self.rect.colliderect(platform):
				if self.velocity.y > 0:
					self.rect.bottom = platform.top
					self.velocity.y = 0
				elif self.velocity.y < 0:
					self.rect.top = platform.bottom
					self.velocity.y = 0

	def on_ground(self, platforms):
		probe = self.rect.move(0, 2)
		return any(probe.colliderect(platform) for platform in platforms)

	def draw(self, surface, camera):
		r = self.rect.move(-camera, 0)
		pygame.draw.rect(surface, (210, 35, 35), (r.x, r.y, r.w, 15))
		pygame.draw.rect(surface, (245, 175, 120), (r.x + 5, r.y + 12, 24, 17))
		pygame.draw.rect(surface, (35, 70, 190), (r.x + 3, r.y + 29, 28, 15))


def make_level():
	platforms = [pygame.Rect(0, 490, 2600, 50)]
	platforms += [pygame.Rect(260, 410, 150, 20), pygame.Rect(500, 340, 150, 20),
				  pygame.Rect(760, 420, 160, 20), pygame.Rect(1030, 350, 160, 20),
				  pygame.Rect(1320, 430, 180, 20), pygame.Rect(1610, 360, 170, 20),
				  pygame.Rect(1900, 410, 180, 20), pygame.Rect(2200, 330, 180, 20)]
	coins = [pygame.Rect(x, y, 18, 18) for x, y in
			 [(300, 375), (540, 305), (800, 385), (1080, 315), (1380, 395),
			  (1660, 325), (1960, 375), (2260, 295)]]
	return platforms, coins


def game():
	player = Player()
	platforms, coins = make_level()
	goal = pygame.Rect(2470, 390, 25, 100)
	running = True
	won = False
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				player = Player()
				platforms, coins = make_level()
				won = False

		if not won:
			keys = pygame.key.get_pressed()
			player.update(keys, platforms)
			for coin in coins[:]:
				if player.rect.colliderect(coin):
					coins.remove(coin)
					player.coins += 1
			if player.rect.y > HEIGHT:
				player.lives -= 1
				if player.lives <= 0:
					player = Player()
				else:
					player.reset()
			if player.rect.colliderect(goal):
				won = True

		camera = max(0, min(player.rect.x - 250, 2600 - WIDTH))
		screen.fill((110, 190, 245))
		pygame.draw.circle(screen, (255, 240, 130), (820, 80), 42)
		for platform in platforms:
			r = platform.move(-camera, 0)
			pygame.draw.rect(screen, (125, 75, 35), r)
			pygame.draw.rect(screen, (45, 175, 65), (r.x, r.y, r.w, 8))
		for coin in coins:
			r = coin.move(-camera, 0)
			pygame.draw.circle(screen, (255, 215, 20), r.center, 9)
		pygame.draw.rect(screen, (245, 245, 245), goal.move(-camera, 0))
		pygame.draw.rect(screen, (235, 45, 45), (goal.x - camera, goal.y, 55, 30))
		player.draw(screen, camera)
		screen.blit(font.render(f"Coins: {player.coins}   Lives: {player.lives}", True, (20, 20, 20)), (20, 20))
		if won:
			msg = font.render("You win! Press R to play again", True, (20, 20, 20))
			screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 100)))
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	game()
