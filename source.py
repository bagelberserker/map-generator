from random import randint

MAPWIDTH = 25
MAPHEIGHT = 25


def build(width, height):
	"""Creates the map using the declared height and width."""
	output = []
	for n in range(height):
		output.append([])
	for x in output:
		for y in range(width):
			x.append(0)
	return output


def walk(empty_map):
	"""Puts a 'walker' at the center of the map, then moves the walker 1 step in a random cardinal direction.
		After each step, the walker increments the value of the space it is on by 1."""
	HEIGHT = len(empty_map)
	WIDTH = len(empty_map[0])
	xcoordinate = int(WIDTH/2)
	ycoordinate = int(HEIGHT/2)
	for n in range(WIDTH*HEIGHT*2):  # Total number of steps is equal to area*2, so the final map has an average of 2 steps per 'tile'.
		direction = randint(1, 4)
		if direction == 1:
			ycoordinate += 1
		elif direction == 2:
			xcoordinate += 1
		elif direction == 3:
			ycoordinate -= 1
		else:
			xcoordinate -= 1
		if xcoordinate < 1 or xcoordinate >= (WIDTH-1) or ycoordinate < 1 or ycoordinate >= (HEIGHT-1):  # Looks clunky. Surely there's a shortcut/cleaner way?
			xcoordinate, ycoordinate = int(WIDTH/2), int(HEIGHT/2)
		else:
			pass
		empty_map[ycoordinate][xcoordinate] += 1
	return empty_map


ISLAND = build(MAPWIDTH, MAPHEIGHT)
FINAL_RESULT = walk(ISLAND)

for i in range(len(FINAL_RESULT)):  # Printed this way for ease of data usage during testing.
	row = ""
	for j in range(len(FINAL_RESULT[0])):
		row += str(FINAL_RESULT[i][j])
		if j < len(FINAL_RESULT[0]) - 1:
			row += "	"
		else:
			pass
	print(row)
