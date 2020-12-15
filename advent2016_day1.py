import collections

INPUT_STRING = ["R4, R3, R5, L3, L5, R2, L2, R5, L2, R5, R5, R5, R1, R3, L2, L2, L1, R5, L3, R1, L2, R1, L3, L5, L1, "
                "R3, L4, R2, R4, L3, L1, R4, L4, R3, L5, L3, R188, R4, L1, R48, L5, R4, R71, R3, L2, R188, L3, R2, L3, "
                "R3, L5, L1, R1, L2, L4, L2, R5, L3, R3, R3, R4, L3, L4, R5, L4, L4, R3, R4, L4, R1, L3, L1, L1, R4, "
                "R1, L4, R1, L1, L3, R2, L2, R2, L1, R5, R3, R4, L5, R2, R5, L5, R1, R2, L1, L3, R3, R1, R3, L4, R4, "
                "L4, L1, R1, L2, L2, L4, R1, L3, R4, L2, R3, L1, L5, R4, R5, R2, R5, R1, R5, R1, R3, L3, L2, L2, L5, "
                "R2, L2, R5, R5, L2, R3, L5, R5, L2, R4, R2, L1, R3, L5, R3, R2, R5, L1, R3, L2, R2, R1"]

DIRECTIONS_MAP = [
    (0, 1),   # North
    (1, 0),   # East
    (0, -1),  # South
    (-1, 0)   # West
    ]

DIRECTIONS_ARRAY = []

for item in INPUT_STRING[0].split(","):
    item = item.strip()
    DIRECTIONS_ARRAY.append((item[0], int(item[1:])))

current_location = [0, 0]
current_direction = 0  # North
locations_list = [(0, 0)]

for item in DIRECTIONS_ARRAY:
    if item[0] == 'R':
        current_direction = (current_direction + 1) % 4
    elif item[0] == 'L':
        current_direction = (current_direction - 1) % 4

    x_sign = DIRECTIONS_MAP[current_direction][0]
    x_traveled = item[1] * x_sign
    # "Visit" each step along the route
    if x_sign != 0:
        for x in range(current_location[0] + x_sign, current_location[0] + x_traveled + x_sign, x_sign):
            new_location = [x, current_location[1]]
            if new_location in locations_list:
                print ("Found revisited location at %r, distance %d" % (new_location, sum([abs(x) for x in new_location])))
            locations_list.append(tuple(new_location))

    y_sign = DIRECTIONS_MAP[current_direction][1]
    y_traveled = item[1] * y_sign
    # "Visit" each step along the route
    if y_sign != 0:
        for y in range(current_location[1] + y_sign, current_location[1] + y_traveled + y_sign, y_sign):
            new_location = current_location[0], y
            if new_location in locations_list:
                print("Found revisited location at %r, distance %d" % (new_location, sum([abs(x) for x in new_location])))
            locations_list.append(tuple(new_location))

    current_location[0] += (item[1] * x_sign)
    current_location[1] += (item[1] * y_sign)

print("End location is %r" % current_location)
print("Distance is %s" % sum([abs(x) for x in current_location]))
print("Visited locations: %r" % locations_list)

seen_locations = set()
for item in locations_list:
    if item in seen_locations:
        print("First duplicate location: %r, manhattan distance: %s" % (item, abs(item[0]) + abs(item[1])))
        break
    seen_locations.add(item)


