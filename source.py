from random import randint

MAPWIDTH = 25
MAPHEIGHT = 25
ISISLAND = True
output = []


def build():
	"""Creates the map using the declared height and width."""
	for n in range(MAPHEIGHT):
		output.append([])
	for x in output:
		for y in range(MAPWIDTH):
			x.append(0)


def walk():
	"""Puts a 'walker' at the center of the map, then moves the walker 1 step in a random cardinal direction.
		After each step, the walker increments the value of the space it is on by 1."""
	xcoordinate = int(MAPWIDTH/2)
	ycoordinate = int(MAPHEIGHT/2)
	for n in range(MAPWIDTH*MAPHEIGHT*2):  # Total number of steps is equal to area*2, so the final map has an average of 2 steps per 'tile'.
		direction = randint(1, 4)
		if direction == 1:
			ycoordinate += 1
		elif direction == 2:
			xcoordinate += 1
		elif direction == 3:
			ycoordinate -= 1
		else:
			xcoordinate -= 1
		if xcoordinate < 1 or xcoordinate >= (MAPWIDTH-1) or ycoordinate < 1 or ycoordinate >= (MAPHEIGHT-1):  # Looks clunky. Surely there's a shortcut/cleaner way?
			xcoordinate, ycoordinate = int(MAPWIDTH/2), int(MAPHEIGHT/2)
		else:
			pass
		output[ycoordinate][xcoordinate] += 1


build()
walk()
for i in range(MAPHEIGHT):  # Printed this way for ease of data usage during testing.
	row = ""
	for j in range(MAPWIDTH):
		row += str(output[i][j])
		if j < MAPWIDTH - 1:
			row += "	"
		else:
			pass
	print(row)
