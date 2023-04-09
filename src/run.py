from maze import Maze

move_keys = {"w": 0, "s": 2, "d": 1, "a": 3}
move_keys_inv = {0: "w", 2: "s", 1: "d", 3: "a"}
colored_maze = Maze(width = 10, height = 10)

colored_maze.generate_walls()
colored_maze.put_runner()
pressed = ""

print("w: up\nd: right\ns: down\na: left\n")

while not pressed == "X":
    colored_maze.print()
    print()
    directions = [move_keys_inv[i] for i in colored_maze.get_all_valid_directions()]
    print("available directions:", directions)
    pressed = input("Enter move: ")

    while pressed not in move_keys.keys():
        print("w: up\nd: right\ns: down\na: left\n")
        pressed = input("Valid keys should be as above. Enter move: ")

    colored_maze.move_runner(move_keys[pressed])

colored_maze.print()
print(colored_maze.get_all_valid_moves())
