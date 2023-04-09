from colorama import init, Fore
import random

# colorama needs to be initialized in order to be used
init()

# Values
# - = empty
# X = wall
# 0 = road
# S = runner
# 1 = colored road

# Directions
# 0 = up
# 1 = right
# 2 = down
# 3 = left


class Cell:
    def __init__(self, x, y, value = "-"):
        self.value = value
        self.x = x
        self.y = y


    def __str__(self):
        return self.value; 



class Runner:
    def move(self, direction):
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y -= 1


    def change_position(self, x, y):
        self.x = x
        self.y = y


    def __init__(self, x, y):
        self.x = x
        self.y = y



class Maze:
    board = []
    runner = Runner(0, 0)

    # initialize empty Maze with given width and height or given board directly
    def __init__(self, height = 0, width = 0, board = None):
        if board:
            for x in range(len(board)):
                row = []
                for y in range(len(board[x])):
                    cell = Cell(x, y, board[x][y])
                    row.append(cell)
                self.board.append(row)
                return
        self.board_template(width=width, height=height)


    # to generate empty board
    def board_template(self, height = 10, width = 10):
        self.board.clear()
        for x in range(height):
            row = []
            for y in range(width):
                cell = Cell(x, y, "-")
                row.append(cell)
            self.board.append(row)


    # get surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.board[rand_wall[0]-1][rand_wall[1]].value == '0'):
            s_cells += 1
        if (self.board[rand_wall[0]+1][rand_wall[1]].value == '0'):
            s_cells += 1
        if (self.board[rand_wall[0]][rand_wall[1]-1].value == '0'):
            s_cells +=1
        if (self.board[rand_wall[0]][rand_wall[1]+1].value == '0'):
            s_cells += 1
        return s_cells


    # wall and road generation inspired by: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
    def generate_walls(self):
        if "0" in [element.value for row in self.board for element in row]:
            self.board_template(len(self.board), len(self.board[0]))

        height = len(self.board)
        width = len(self.board[0])

        # randomize starting point and set it a cell
        starting_height = int(random.random()*height)
        starting_width = int(random.random()*width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == width-1):
            starting_width -= 1

        # mark it as cell and add surrounding walls to the list
        self.board[starting_height][starting_width].value = "0"
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # denote walls in maze
        self.board[starting_height-1][starting_width].value = 'X'
        self.board[starting_height][starting_width - 1].value = 'X'
        self.board[starting_height][starting_width + 1].value = 'X'
        self.board[starting_height + 1][starting_width].value = 'X'

        while (walls):
            # pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.board[rand_wall[0]][rand_wall[1]-1].value == '-' and self.board[rand_wall[0]][rand_wall[1]+1].value == '0'):
                    # find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # denote the new path
                        self.board[rand_wall[0]][rand_wall[1]].value = '0'

                        # mark the new walls
                        # upper cell
                        if (rand_wall[0] != 0):
                            if (self.board[rand_wall[0]-1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]-1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])


                        # bottom cell
                        if (rand_wall[0] != height-1):
                            if (self.board[rand_wall[0]+1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]+1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.board[rand_wall[0]][rand_wall[1]-1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]-1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                    

                    # delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.board[rand_wall[0]-1][rand_wall[1]].value == '-' and self.board[rand_wall[0]+1][rand_wall[1]].value == '0'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # denote the new path
                        self.board[rand_wall[0]][rand_wall[1]].value = '0'

                        # mark the new walls
                        # upper cell
                        if (rand_wall[0] != 0):
                            if (self.board[rand_wall[0]-1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]-1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.board[rand_wall[0]][rand_wall[1]-1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]-1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # rightmost cell
                        if (rand_wall[1] != width-1):
                            if (self.board[rand_wall[0]][rand_wall[1]+1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]+1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # check the bottom wall
            if (rand_wall[0] != height-1):
                if (self.board[rand_wall[0]+1][rand_wall[1]].value == '-' and self.board[rand_wall[0]-1][rand_wall[1]].value == '0'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # denote the new path
                        self.board[rand_wall[0]][rand_wall[1]].value = '0'

                        # mark the new walls
                        if (rand_wall[0] != height-1):
                            if (self.board[rand_wall[0]+1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]+1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.board[rand_wall[0]][rand_wall[1]-1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]-1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != width-1):
                            if (self.board[rand_wall[0]][rand_wall[1]+1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]+1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)


                    continue

            # check the right wall
            if (rand_wall[1] != width-1):
                if (self.board[rand_wall[0]][rand_wall[1]+1].value == '-' and self.board[rand_wall[0]][rand_wall[1]-1].value == '0'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # denote the new path
                        self.board[rand_wall[0]][rand_wall[1]].value = '0'

                        # mark the new walls
                        if (rand_wall[1] != width-1):
                            if (self.board[rand_wall[0]][rand_wall[1]+1].value != '0'):
                                self.board[rand_wall[0]][rand_wall[1]+1].value = 'X'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != height-1):
                            if (self.board[rand_wall[0]+1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]+1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.board[rand_wall[0]-1][rand_wall[1]].value != '0'):
                                self.board[rand_wall[0]-1][rand_wall[1]].value = 'X'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)
            


        # mark the remaining unvisited cells as walls
        for i in range(0, height):
            for j in range(0, width):
                if (self.board[i][j].value == '-'):
                    self.board[i][j].value = 'X'


    # put runner to random available position
    def put_runner(self):
        available_indexes =[]

        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y].value == "0":
                    available_indexes.append([x, y]) 
        
        if available_indexes:
            indexes = random.choice(available_indexes)
            self.runner.change_position(indexes[0], indexes[1])
            self.board[indexes[0]][indexes[1]].value = "S"
            return indexes
        
        print("There is no available spot for runner. Please check if your maze is ok.")

    def move_runner(self, direction):
        if direction  not in [0, 1, 2, 3]:
            print("Valid directions are: 0(up), 1(right), 2,(down), 3(left)")
            return
            
        if direction == 0 and self.valid_move(self.runner.x-1, self.runner.y):
            self.board[self.runner.x][self.runner.y].value = "1"
            self.board[self.runner.x-1][self.runner.y].value = "S"
            self.runner.move(0)
        elif direction == 1 and self.valid_move(self.runner.x, self.runner.y+1):
            self.board[self.runner.x][self.runner.y].value = "1"
            self.board[self.runner.x][self.runner.y+1].value = "S"
            self.runner.move(1)
        elif direction == 2 and self.valid_move(self.runner.x+1, self.runner.y):
            self.board[self.runner.x][self.runner.y].value = "1"
            self.board[self.runner.x+1][self.runner.y].value = "S"
            self.runner.move(2)
        elif direction == 3 and self.valid_move(self.runner.x, self.runner.y-1):
            self.board[self.runner.x][self.runner.y].value = "1"
            self.board[self.runner.x][self.runner.y-1].value = "S"
            self.runner.move(3)
        else:
            print("You cannot move there!")


    def valid_move(self, x, y):
        # cant move beyond boundaries
        if (x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0])):
            return False
        # cant move to wall
        if (self.board[x][y].value == "X"):
            return False
        return True


    def get_all_valid_moves(self):
        x = self.runner.x
        y = self.runner.y
        supposed_valid = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
        
        # return array of possible directions to go ex. [up, down]
        return [move for move in supposed_valid if self.valid_move(move[0], move[1])]

    def get_all_valid_directions(self):
        x = self.runner.x
        y = self.runner.y
        supposed_valid = {2: [x+1, y], 1: [x, y+1], 0: [x-1, y], 3: [x, y-1]}
        
        # return array of possible directions to go ex. [up, down]
        return [direction for direction in supposed_valid.keys() if self.valid_move(supposed_valid[direction][0], supposed_valid[direction][1])]


    # print maze
    def print(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                if self.board[i][j].value == 'X':
                    print(Fore.WHITE, f'{self.board[i][j]}', end="")
                elif self.board[i][j].value == '0':
                    print(Fore.BLACK, f'{self.board[i][j]}', end="")
                elif self.board[i][j].value == '1':
                    print(Fore.RED, f'{self.board[i][j]}', end="")
                elif self.board[i][j].value == 'S':
                    print(Fore.GREEN, f'{self.board[i][j]}', end="")  
            print('\n', end='')
