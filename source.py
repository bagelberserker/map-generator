from random import randint
from PIL import Image


def build(width, height):
    """Creates a grid of 0's using the declared height and width."""
    return [[0 for y in range(height +2)] for x in range(width +2)]


def walk(empty_map, surface="island"):
    """Puts a 'walker' at the center of the map, then moves the walker 1 step in a random cardinal direction.
        After each step, the walker increments the value of the space it is on by 1."""
    walked_map = empty_map
    HEIGHT = len(empty_map)
    WIDTH = len(empty_map[0])
    if surface.lower() in ["torus", "donut", "mug"]:
        topology = "torus"
    elif surface.lower() in ["globe", "sphere"]:
        topology = "globe"
    else:
        topology = "island"
    walker_x = int(WIDTH / 2)
    walker_y = int(HEIGHT / 2)
    for n in range(WIDTH * HEIGHT * 2):  # Total number of steps is equal to area*2, so the final map has an average of 2 steps per 'tile'.
        direction = randint(1, 4)
        if direction == 1:
            walker_y += 1
        elif direction == 2:
            walker_x += 1
        elif direction == 3:
            walker_y -= 1
        else:
            walker_x -= 1
        if walker_x < 1:
            if topology in ["torus", "globe"]:
                walker_x = WIDTH - 2
            else:
                walker_x = int(WIDTH / 2)
                walker_y = int(HEIGHT / 2)
        else:
            pass
        if walker_x > WIDTH - 2:
            if topology in ["torus", "globe"]:
                walker_x = 1
            else:
                walker_x = int(WIDTH / 2)
                walker_y = int(HEIGHT / 2)
        else:
            pass
        if walker_y < 1:
            if topology == "globe":
                walker_y = 1
                walker_x = WIDTH-walker_x
            elif topology == "torus":
                walker_y = HEIGHT - 2
            else:
                walker_x = int(WIDTH / 2)
                walker_y = int(HEIGHT / 2)
        else:
            pass
        if walker_y > HEIGHT - 2:
            if topology == "globe":
                walker_y = HEIGHT - 2
                walker_x = WIDTH-walker_x
            elif topology == "torus":
                walker_y = 1
            else:
                walker_x = int(WIDTH / 2)
                walker_y = int(HEIGHT / 2)
        else:
            pass
        walked_map[walker_y][walker_x] += 1
    return walked_map


def blur(walked_map):
    """Reduces 'spikeyness' on the map and clears out small isthmi, turning them into islands."""
    blurred_map = []
    for y in range(len(walked_map)):
        row = []
        for x in range(len(walked_map[y])):
            if y in [0, len(walked_map) - 1] or x in [0, len(walked_map[y]) - 1]:
                row.append(0)
            else:
                row.append(
                    int(
                        (
                            walked_map[y + 1][x]
                            + walked_map[y - 1][x]
                            + walked_map[y][x + 1]
                            + walked_map[y][x - 1]
                            + 4 * walked_map[y][x]
                        ) / 8
                    )
                )
        blurred_map.append(row)
    return blurred_map


def delake(blurred_map):
    """Attempts to remove inland bodies of water."""
    finished_map = []
    for y in range(len(blurred_map)):
        row = []
        for x in range(len(blurred_map[y])):
            row.append(blurred_map[y][x]+1)
        finished_map.append(row)
    for y in range(len(finished_map)):
        finished_map[y][0] = 0
        finished_map[y][-1] = 0
    for x in range(len(finished_map[0])):
        finished_map[0][x] = 0
        finished_map[-1][x] = 0
    for n in range(4):
        for y in range(1, len(finished_map) - 1):
            for x in range(1, len(finished_map[y]) - 1):
                if finished_map[y][x] == 1 and 0 in [
                    finished_map[y + 1][x], 
                    finished_map[y - 1][x], 
                    finished_map[y][x + 1], 
                    finished_map[y][x - 1]
                ]:
                    finished_map[y][x] = 0
        for x in range(1, len(finished_map[0]) - 1)[::-1]:
            for y in range(1, len(finished_map) - 1):
                if finished_map[y][x] == 1 and 0 in [
                    finished_map[y + 1][x], 
                    finished_map[y - 1][x], 
                    finished_map[y][x + 1], 
                    finished_map[y][x - 1]
                ]:
                    finished_map[y][x] = 0
        for y in range(1, len(finished_map) - 1)[::-1]:
            for x in range(1, len(finished_map[y]) - 1)[::-1]:
                if finished_map[y][x] == 1 and 0 in [
                    finished_map[y + 1][x], 
                    finished_map[y - 1][x], 
                    finished_map[y][x + 1], 
                    finished_map[y][x - 1]
                ]:
                    finished_map[y][x] = 0
        for x in range(1, len(finished_map[0]) - 1):
            for y in range(1, len(finished_map) - 1)[::-1]:
                if finished_map[y][x] == 1 and 0 in [
                    finished_map[y + 1][x], 
                    finished_map[y - 1][x], 
                    finished_map[y][x + 1], 
                    finished_map[y][x - 1]
                ]:
                    finished_map[y][x] = 0
    return finished_map


def save_to_image(finished_map, location, name):
    """Saves the map as a .png file."""
    final_map = finished_map[1:-1]
    for n in range(len(final_map)):
        final_map[n] = final_map[n][1:-1]
    WIDTH = len(final_map[0])
    HEIGHT = len(final_map)
    highpoint = max([max(y) for y in final_map])
    cutoff = 64
    multiplier = 1
    for number in [16, 8, 4]:
        if highpoint < number:
            cutoff /= 2
            multiplier *= 2
    to_image = Image.new("RGB", (WIDTH, HEIGHT))
    output = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if final_map[y][x] == 0:
                output.append(4202496)  # RGB hex -> decimal.
            elif final_map[y][x] > cutoff:
                output.append(12644576)
            else:
                output.append(8192 + 131843 * multiplier * final_map[y][x])
    to_image.putdata(tuple(output))
    to_image.save(location+name+".png")


def post_raw_data(finished_map):
    final_map = finished_map[1:-1]
    for n in range(len(final_map)):
        final_map[n] = final_map[n][1:-1]
    for y in range(len(final_map)):
        row = ""
        for x in range(len(final_map[y])):
            row += str(final_map[y][x])
            if x == len(final_map[y])-1:
                pass
            else:
                row += "	"
        print(row)


# If you want to run the program with your own parameters and filepath, I made constants for that.
MAPWIDTH = 600
MAPHEIGHT = 400
DESIRED_LOCATION = "C:\\Users\\My Dell\\Desktop\\"
DESIRED_FILENAME = "map"
MAPTYPE = "island"  # Viable options are "island", "globe", and "torus".

save_to_image(
    delake(
        blur(
            walk(
                build(MAPWIDTH, MAPHEIGHT), 
                MAPTYPE
            )
        )
    ), 
    DESIRED_LOCATION, 
    DESIRED_FILENAME
)
