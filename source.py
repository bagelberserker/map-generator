from random import randint

MAPWIDTH = 25
MAPHEIGHT = 25
output = []


def build():
	"""Creates the map using the declared height and width."""
	for n in range(MAPHEIGHT):
		output.append([])
	for x in output:
		for y in range(MAPWIDTH):
			x.append(0)


def walk(island=True):
	"""Puts a 'walker' at the center of the map, then moves the walker 1 step in a random cardinal direction.
		After each step, the walker increments the value of the space it is on by 1."""
	xcoordinate = int(MAPWIDTH/2)
	ycoordinate = int(MAPHEIGHT/2)
	output[ycoordinate][xcoordinate] += 1
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
		if island:  # Simulates a volcanic island. When the walker would reach the edge, it's location is reset to the starting point.
  			if xcoordinate < 1 or xcoordinate >= (MAPWIDTH-1) or ycoordinate < 1 or ycoordinate >= (MAPHEIGHT-1):  # Looks clunky. Surely there's a shortcut/cleaner way?
				xcoordinate, ycoordinate = int(MAPWIDTH/2), int(MAPHEIGHT/2)
			else:
				pass
		else:  # Attempts to simulate landmasses of a large scale, such as continents. When the walker would reach the edge, it's location along that axis is semi-randomized.
			if xcoordinate < 1:
				xcoordinate = randint(int(MAPWIDTH/4), int(MAPWIDTH/2))
			elif xcoordinate >= (MAPWIDTH-1):
				xcoordinate = randint(int(MAPWIDTH/2), int(3*MAPWIDTH/4))
			elif ycoordinate < 1:
				ycoordinate = randint(int(MAPHEIGHT/4), int(MAPHEIGHT/2))
			elif ycoordinate >= (MAPHEIGHT-1):
				ycoordinate = randint(int(MAPHEIGHT/2), int(3*MAPHEIGHT/4))
			else:
				pass
		output[ycoordinate][xcoordinate] += 1


build()
walk()
for i in output:  # Printed this way for ease of data usage during testing.
	print(i)
