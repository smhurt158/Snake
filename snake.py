import pygame, sys, random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
HGREEN = (0, 254, 0)
TGREEN = (0, 253, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

snake_color = GREEN
snake_head_color = HGREEN
snake_tail_color = TGREEN
food_color = RED
backgroud_color = BLACK

game_width = 600
grid_size = 20
node_size = game_width // 20
node_border_width = 2

game_screen = pygame.display.set_mode((game_width, game_width))

speed = 10;
class node:
	def __init__(self, x, y, color):
		self.color = color
		self.x = x
		self.y = y
		self.next = None
	def draw(self):
		self.border_size = 1
		self.box = (self.x * node_size + node_border_width, self.y * node_size + node_border_width, node_size - node_border_width * 2, node_size - node_border_width * 2)
		pygame.draw.rect(game_screen, self.color, self.box)
	
class board:
	def __init__(self):
		self.score = 1
		self.grid = []
		#draws the initial Grid
		for i in range(grid_size):
			this_layer = []
			for j in range(grid_size):
				new_node = node(i, j, backgroud_color);
				this_layer.append(new_node)
				new_node.draw();
			self.grid.append(this_layer)
		self.head = self.grid[len(self.grid)//2][len(self.grid)//2]
		self.head.color = snake_head_color
		self.head.draw()
		self.tail = self.head
		self.tail.next = self.head
		self.dx = 0
		self.dy = 0
		self.last_dx = 0
		self.last_dy = -1
		self.move_snake(self.dx, self.dy, self.last_dx, self.last_dy)
		
	def get_next_node(self, dx, dy):
		if(dx != 0):
			if(dx == 1):
				if(self.head.x + 1 >= grid_size):
					return None
				else:
					return self.grid[self.head.x + dx][self.head.y + dy]
			if(dx == -1):
				if(self.head.x - 1 < 0):
					return None
				else:
					return self.grid[self.head.x + dx][self.head.y + dy]
		elif(dy != 0):
			if(dy == 1):
				if(self.head.y + 1 >= grid_size):
					return None
				else:
					return self.grid[self.head.x + dx][self.head.y + dy]
			if(dy == -1):
				if(self.head.y  - 1 < 0):
					return None
				else:
					return self.grid[self.head.x + dx][self.head.y + dy]
		else:
			return self.grid[self.head.x + dx][self.head.y + dy]
		
	def move_snake(self, dx, dy, last_dx, last_dy):
		test = self.get_next_node(dx, dy)
		output = ""
		if(test == None):
			return  "collide"
		elif(test.next == self.head or test == self.head):
			dx = last_dx
			dy = last_dy
			test = self.get_next_node(last_dx, last_dy)
			if(test == None):
				return  "collide"
			elif(test.color == snake_color):
				return "collide"
			output =  "invalid"
		elif(test.color == snake_color):
			return "collide"
		prev_head = self.head
		self.head.color = snake_color
		self.head.next = test
		self.head.draw()
		self.head = test
		if(test.color == food_color or prev_head == self.tail):
			self.score+= 1
			self.add_food()
		else:
			self.tail.color = backgroud_color
			self.tail.draw()
			prev_tail = self.tail
			output = self.tail.next == test
			self.tail = self.tail.next
			prev_tail.next = None
		self.head.color = snake_head_color
		self.head.draw()
		self.last_dx = dx
		self.last_dy = dy
		return output
	
	def add_food(self):
		x = random.randrange(0, grid_size)
		y = random.randrange(0, grid_size)
		node = self.grid[x][y]
		while(node.color == snake_color or node.color == snake_head_color):
			x = random.randrange(0, grid_size)
			y = random.randrange(0, grid_size)
			node = self.grid[x][y]
		node.color = food_color
		node.draw()
		
	def set_dir(self, dx, dy):
		self.dx = dx
		self.dy = dy
b = board()	
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_w):
				b.set_dir(0, -1)
			if (event.key == pygame.K_s):
				b.set_dir(0, 1)
			if (event.key == pygame.K_d):
				b.set_dir(1, 0)
			if (event.key == pygame.K_a):
				b.set_dir(-1, 0)
	if(b.move_snake(b.dx,b.dy,b.last_dx, b.last_dy) == "collide"):
		b = board()
	pygame.display.update()
	pygame.time.Clock().tick(speed)