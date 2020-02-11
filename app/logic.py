'''
As of now, the bfs is a good search algorithm to find it's desired target 

Problems arise when 

'''


class Point:
    def __init__(self, data=None, x=0, y=0):
        if data != None:
            self.x = data["x"]
            self.y = data["y"]
            return
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)


class GameBoard():
    """
    0 - Empty space
    1 - Snake head
    2 - Snake body
    3 - Snake tail
    4 - You head
    5 - You body
    6 - You tail
    7 - food
    """

    def __init__(self, data=None):
        """Creates a new game board"""
        if data == None:
            print("Data not set... its going to crash")
            return

        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = []  # array of arrays
        
        # init board
        for _ in range(0, self.width):
            column = []
            for _ in range(0, self.height):
                column.append(0)
            self.board.append(column)

        # go through all the snakes and add them to the board
        max_prev_count = 0 
        for snake in data["board"]["snakes"]:
            count_snake_body = 0
            for bodypart in snake["body"]:
                self.board[bodypart["x"]][bodypart["y"]] = 2
                count_snake_body+=1
            # add tail
            tail = snake["body"][-1]
            self.board[tail["x"]][tail["y"]] = 3
            # add head
            head = snake["body"][0]
            self.board[head["x"]][head["y"]] = 1

            if(count_snake_body>max_prev_count):
                max_prev_count = self.count_snake_body

        count_snake_body = max_prev_count

        # go through the food and add it to the board
        for food in data["board"]["food"]:
            self.board[food["x"]][food["y"]] = 7

        # go through self
        for you in data["you"]["body"]:
            self.board[you["x"]][you["y"]] = 5
            count_my_body += 1

        # get the head from the us
        you_tail = data["you"]["body"][-1]
        # set the board at head to the you head value (6)
        self.board[you_tail["x"]][you_tail["y"]] = 6
        you_head = data["you"]["body"][0]
        self.board[you_head["x"]][you_head["y"]] = 4

        print("This is the created board")
        self.printBoard()

    #returns how big you are
    @staticmethod
    def bodycount():
        return count_my_body
    
    #returns the biggest snake body count
    @staticmethod
    def snakebodycount():
        return count_snake_body


    def printBoard(self):
        for x in range(0, self.height):
            for y in range(0, self.width):
                print(self.board[y][x], end=' ')
            print()

    def bfs(self, start, num):
        """
        Start is the point on the board we start looking from
        Num is the value (look at top) that we are looking for
        """ 

        queue = []
        visited = set()
        pg = {} # parent graph
        """
        The parent graph (point:tile) points to the direction where it was generated
        """
        # add the tiles around the head
        self.enqueue_around_head(start, queue)

        # While we are still in the queue
        while len(queue) != 0:
            # print("Visited: ", visited)

            tile = queue.pop(0)
            if tile.x >= self.width or tile.x < 0 or tile.y >= self.height or tile.y < 0:
                continue


            # print("tile: ", end='')
            # print(str(tile))

            # print("queue:", queue)

            tile_val = self.board[tile.x][tile.y]

            if str(tile) in visited:
                continue

            visited.add(str(tile))

            if tile_val == num:
                return self.get_relative_direction(start, tile, pg)

            if tile_val == 0:
                self.enqueue_around_point(tile, queue, visited, pg)
        
        return -1  #it didnt find what it was looking for 

    def enqueue_around_head(self, tile, queue):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]

        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0: # to check if our value is out of bounds
                continue # if it is out of bounds, the iteration is skipped
            val = self.board[point.x][point.y] 
            if (val == 0 or val == 3 or val == 7): #queue is only filled with 0,3,7 to start with
                queue.append(point)

    def enqueue_around_point(self, tile, queue, visted, parent_graph):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]

        for point in points:
            if not (point in visted):
                queue.append(point)
                parent_graph[point] = tile  # The points point to the tile

    def get_relative_direction(self, start, end, pg):
        temp = end

        while temp in pg: # gets where the end point was generated from 
            temp = pg[temp]

        diff_x = start.x - temp.x
        diff_y = start.y - temp.y

        if diff_x == -1:
            return 3
        if diff_x == 1:
            return 2
        if diff_y == -1:
            return 1
        if diff_y == 1:
            return 0

    def turtle():
        pass