from random import randint
from PIL import Image  # Pillow module


# If you want to run the program with your own parameters and filepath, I made constants for that.
MAPWIDTH = 600
MAPHEIGHT = 400
OUTPUT_LOCATION = "C:\\Users\\My Dell\\Desktop\\"
OUTPUT_FILE_NAME = "output"
MAPTYPE = "globe"  # Viable options are "island", "globe", and "torus".


def build(width, height):
	"""Creates the map using the declared height and width."""
	output = []
	for y in range(height+1):
		row = []
		for x in range(width+1):
				row.append(0)
		output.append(row)
	return output


def walk(empty_map, surface="island"):
	"""Puts a 'walker' at the center of the map, then moves the walker 1 step in a random cardinal direction.
		After each step, the walker increments the value of the space it is on by 1."""
	output = empty_map
	HEIGHT = len(empty_map)
	WIDTH = len(empty_map[0])
	if surface.lower() in ["torus", "donut", "mug"]:
		TOPOLOGY = "torus"
	elif surface.lower() in ["globe", "sphere"]:
		TOPOLOGY = "globe"
	else:
		TOPOLOGY = "island"
	x_coordinate = int(WIDTH/2)
	y_coordinate = int(HEIGHT/2)
	for n in range(WIDTH*HEIGHT*2):  # Total number of steps is equal to area*2, so the final map has an average of 2 steps per 'tile'.
		direction = randint(1, 4)
		if direction == 1:
			y_coordinate += 1
		elif direction == 2:
			x_coordinate += 1
		elif direction == 3:
			y_coordinate -= 1
		else:
			x_coordinate -= 1
		if x_coordinate < 1:
			if TOPOLOGY in ["torus", "globe"]:
				x_coordinate = WIDTH-2
			else:
				x_coordinate = int(WIDTH/2)
				y_coordinate = int(HEIGHT/2)
		else:
			pass
		if x_coordinate > WIDTH-2:
			if TOPOLOGY in ["torus", "globe"]:
				x_coordinate = 1
			else:
				x_coordinate = int(WIDTH/2)
				y_coordinate = int(HEIGHT/2)
		else:
			pass
		if y_coordinate < 1:
			if TOPOLOGY == "globe":
				y_coordinate = 1
				x_coordinate = WIDTH-x_coordinate
			elif TOPOLOGY == "torus":
				y_coordinate = HEIGHT-2
			else:
				x_coordinate = int(WIDTH / 2)
				y_coordinate = int(HEIGHT / 2)
		else:
			pass
		if y_coordinate > HEIGHT-2:
			if TOPOLOGY == "globe":
				y_coordinate = HEIGHT-2
				x_coordinate = WIDTH-x_coordinate
			elif TOPOLOGY == "torus":
				y_coordinate = 1
			else:
				x_coordinate = int(WIDTH / 2)
				y_coordinate = int(HEIGHT / 2)
		else:
			pass
		output[y_coordinate][x_coordinate] += 1
	return output


def blur(finished_map):
	"""An optional filter to reduce 'spikeyness' on the map.
		Also clears out small isthmi, turning them into islands."""
	output = []
	for y in range(len(finished_map)):
		row = []
		for x in range(len(finished_map[y])):
			if y in [0, len(finished_map)-1] or x in [0, len(finished_map[y])-1]:
				row.append(0)
			else:
				row.append(int((finished_map[y+1][x]+finished_map[y-1][x]+finished_map[y][x+1]+finished_map[y][x-1]+4*finished_map[y][x])/8))
		output.append(row)
	return output


def no_lakes(finished_map):
	"""Attempts to remove inland bodies of water."""
	output = []
	for y in range(len(finished_map)):
		row = []
		for x in range(len(finished_map[y])):
			row.append(finished_map[y][x]+1)
		output.append(row)
	for y in range(len(output)):
		output[y][0] = 0
		output[y][-1] = 0
	for x in range(len(output[0])):
		output[0][x] = 0
		output[-1][x] = 0
	for n in range(4):
		for y in range(1, len(output)-1):
			for x in range(1, len(output[y])-1):
				if 0 in [output[y+1][x], output[y-1][x], output[y][x+1], output[y][x-1]] and output[y][x] == 1:
					output[y][x] = 0
		for x in range(1, len(output[0])-1)[::-1]:
			for y in range(1, len(output)-1):
				if 0 in [output[y+1][x], output[y-1][x], output[y][x+1], output[y][x-1]] and output[y][x] == 1:
					output[y][x] = 0
		for y in range(1, len(output)-1)[::-1]:
			for x in range(1, len(output[y])-1)[::-1]:
				if 0 in [output[y+1][x], output[y-1][x], output[y][x+1], output[y][x-1]] and output[y][x] == 1:
					output[y][x] = 0
		for x in range(1, len(output[0])-1):
			for y in range(1, len(output)-1)[::-1]:
				if 0 in [output[y+1][x], output[y-1][x], output[y][x+1], output[y][x-1]] and output[y][x] == 1:
					output[y][x] = 0
	return output


def save_to_image(finished_map, location, name):
	"""Saves the map as a .png file.
	Requires the Pillow python module."""
	finished_map = finished_map[1:-1]
	for n in range(len(finished_map)):
		finished_map[n] = finished_map[n][1:-1]
	WIDTH = len(finished_map[0])
	HEIGHT = len(finished_map)
	HIGHPOINT = max([max(y) for y in finished_map])
	cutoff = 64
	multiplier = 1
	for number in [16, 8, 4]:
		if HIGHPOINT < number:
			cutoff /= 2
			multiplier *= 2
	to_image = Image.new("RGB", (WIDTH, HEIGHT))
	output = []
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if finished_map[y][x] == 0:
				output.append(4202496)  # RGB hex -> decimal.
			elif finished_map[y][x] > cutoff:
				output.append(12644576)
			else:
				output.append(8192 + 131843*multiplier*finished_map[y][x])
	to_image.putdata(tuple(output))
	to_image.save(location+name+".png")


def post_to_screen(finished_map):
	finished_map = finished_map[1:-1]
	for n in range(len(finished_map)):
		finished_map[n] = finished_map[n][1:-1]
	for y in range(len(finished_map)):
		row = ""
		for x in range(len(finished_map[y])):
			row += str(finished_map[y][x])
			if x == len(finished_map[y])-1:
				pass
			else:
				row += "	"
		print(row)


# All the magic happens on this next line:
save_to_image(no_lakes(blur(walk(build(MAPWIDTH, MAPHEIGHT), MAPTYPE))), OUTPUT_LOCATION, OUTPUT_FILE_NAME)
