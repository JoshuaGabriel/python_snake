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
    SnakeBodyCount  = 0 
    MyBodyCount     = 0 
    MyPreviousTile  = -1 # Stores the value of the previous tile Skippy has been on

    DidIJustEat     = 0 # Check if I am about to grow, to omit the tail as a valid square (because I'm growing) #broken


    def __init__(self, data=None):
        """Creates a new game board"""
        if data == None:
            print("Data not set... its going to crash")
            return
        self.data = data
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
        GameBoard.SnakeBodyCount = 0
        temporary_count = 0
        for snake in data["board"]["snakes"]:

            if(snake["id"]==data["you"]["id"]):
                continue

            temporary_count = 0 
            for bodypart in snake["body"]:
                self.board[bodypart["x"]][bodypart["y"]] = 2

                temporary_count+=1
            if(temporary_count>GameBoard.SnakeBodyCount):
                GameBoard.SnakeBodyCount = temporary_count

            # add tail
            tail = snake["body"][-1]
            self.board[tail["x"]][tail["y"]] = 3
            # add head
            head = snake["body"][0]
            self.board[head["x"]][head["y"]] = 1
        
        # go through the food and add it to the board
        for food in data["board"]["food"]:
            self.board[food["x"]][food["y"]] = 7

        # go through self
        GameBoard.MyBodyCount = 0
        for you in data["you"]["body"]:
            self.board[you["x"]][you["y"]] = 5
            GameBoard.MyBodyCount+=1

        # get the head from the us
        you_tail = data["you"]["body"][-1]
        # set the board at head to the you head value (6)
        self.board[you_tail["x"]][you_tail["y"]] = 6
        you_head = data["you"]["body"][0]
        self.board[you_head["x"]][you_head["y"]] = 4

        # print("This is the created board")
        # self.printBoard()
    def GetBoard(self):
        return self.board

    def printBoard(self):
        for x in range(0, self.height):
            for y in range(0, self.width):
                print(self.board[y][x], end=' ')

            print()
        print(GameBoard.DidIJustEat)
        print(self.Storage_dict)

    def bfs(self, start, num, status_safety=True,status_trap=True):
        """
        Start is the point on the board we start looking from
        Num is the value (look at top) that we are looking for
        Status is used to overide the safety protocol, this will default to True, unless specified
        """ 
        queue = []
        visited = set()
        pg = {} # parent graph
        # add the tiles around the head
        self.enqueue_around_head(start, queue)

        # While we are still in the queue
        while len(queue) != 0:
            # print("Visited: ", visited)

            tile = queue.pop(0)
            if tile.x >= self.width or tile.x < 0 or tile.y >= self.height or tile.y < 0:
                continue


            # print("queue:", queue)
            # print("tile: ", end='')
            # print(str(tile))

            tile_val = self.board[tile.x][tile.y]

            if str(tile) in visited:
                continue

            visited.add(str(tile))

            if(tile==start):
                continue

            if (GameBoard.DidIJustEat) and (tile_val == 6) :
                continue

            if(not(self.safety_protocol(tile,num)) and status_safety):
                continue

            if(self.trap_protocol(tile) and status_trap):
                continue

            if tile_val == num:
                return self.get_relative_direction(start, tile, pg)

            if tile_val == 0 or tile_val == 7:
                self.enqueue_around_point(tile, queue, visited, pg, num)
        
        return -1  #it didnt find what it was looking for 

    def enqueue_around_head(self, tile, queue):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]
        valid_tiles = [0,6,7]
        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0: # to check if our value is out of bounds
                continue # if it is out of bounds, the iteration is skipped
            tile_val = self.board[point.x][point.y] 
            if tile_val in valid_tiles: #queue is only filled with 0,3,6,7 to start with
                queue.append(point)

    def enqueue_around_point(self, tile, queue, visted, parent_graph, num):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]
    
        for point in points:
            if (not (point in visted)):
                queue.append(point)
                parent_graph[point] = tile  # The points point to the tile

    # Gets the direction of the chosen square so skippy knows where to turn
    def get_relative_direction(self, start, end, pg):
        temp = end
        
        while temp in pg: # gets where the end point was generated from 
            temp = pg[temp]


        if(self.board[temp.x][temp.y]==7):
            GameBoard.DidIJustEat = True
        else:
            GameBoard.DidIJustEat = False
        
        # print("The tile I am going to is: ",temp)
        # print("tile value of: ",self.board[temp.x][temp.y])

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

    # returns false if the tile is dangerous (beside an opponent snake head)
    # return true if the tile is safe
    def safety_protocol(self,tile, num):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]
        
        if(GameBoard.AmIAlpha()):
            return True

        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
                continue

            if(self.board[point.x][point.y]==1):
                for snake in self.data["board"]["snakes"]:
                    print("length of snakes",len(self.data["board"]["snakes"]))
                    print("snake.x: ",snake["body"][0]["x"]," snake.y: ",snake["body"][0]["y"])
                    print("point.x: ",point.x," point.y: ",point.y)
                    print(str(snake["body"][0]["x"])==str(point.x) and str(snake["body"][0]["y"])==str(point.y))
                    if(str(snake["body"][0]["x"])==str(point.x) and str(snake["body"][0]["y"])==str(point.y)):
                        count = len(snake["body"])
                        if(GameBoard.AmIAlpha(count)):
                            return True
                        break
                return False
        return True

    #Returns a list of good points (IN STR FORMAT)
    def neighbors(self,tile): 
        invalid_squares = [1,2,4,5]
        head = None
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]
        good_points = []
        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
                continue
            if(self.board[point.x][point.y]==1):
                head = point       
            if (self.board[point.x][point.y] in invalid_squares):
                continue
            good_points.append(point)
        return good_points,head

    # Returns True if the next tile is a trapped tile 
    # A tile is considered to be trapped if there are no possible moves after
    def trap_protocol(self,tile,previous_tile=None):
        searching, head = self.neighbors(tile)
        
        if(previous_tile!=None):
            count=0
            for square in searching:
                if(square.x==previous_tile.x and square.y==previous_tile.y):
                    searching.pop(count)
                    break
                count+=1

        if(len(searching)>1):
            return False
        elif(len(searching)==0):
            return True
        else:
            if(head!=None):          
                vector1 = Point(x=searching[0].x-tile.x,y=searching[0].y-tile.y)
                vector2 = Point(x=head.x-tile.x,y=head.y-tile.y)
                dot_product = vector1.x*vector2.x + vector1.y*vector2.y
                print(dot_product)
                if(dot_product==0):
                    return True
            previous_tile = Point(x=tile.x,y=tile.y)
            return self.trap_protocol(tile=searching[0],previous_tile=previous_tile)


    @staticmethod
    def AmIAlpha(count=None):
        if(count!=None):
            if(GameBoard.MyBodyCount>count):
                return True
            else:
                return False
        
        if(GameBoard.MyBodyCount>GameBoard.SnakeBodyCount):
            return True
        else:
            return False 
    

    # Fills the board with deadends
    def deadend(self):
        pass










    '''
    Get relative direction of enemy snake
    https://play.battlesnake.com/g/bf1f56d2-403e-482d-a324-8d0222a0cdb1/#
    my head is at: (3,1) 
    for example ((1,1) (9,1) (1,9) (9,9)) for 11x11 grid 
        if (((head.x == edge.x) or (head.y==edge.y)) and (im not at the width or height)) and (enemeny head is at the edge and I'm beside it +1):
            go for the end of board to kill them
        elif(if im at the end of the board)
            return -1
        else: 
            return -1
        to see how I am inside I need to get my head's coords 
    
    if(im inside of ((1,1) (9,1) (1,9) (9,9)))
    '''
    @staticmethod
    def TrapKill():
        pass

    # implement a turtle and survive strategy for super late game scenario and we are smaller by a lot
    def turtle(self,data):
        move_data = -1
        # print("CountMyBody: ", GameBoard.MyBodyCount)
        # print("CountSnakeBody: ", GameBoard.SnakeBodyCount)
        head = data["you"]["body"][0]
        if(GameBoard.MyBodyCount+7<GameBoard.SnakeBodyCount and data["you"]["health"]<50): 
            move_data = GameBoard.bfs(self,Point(data=head), 7) #go for food
        elif(GameBoard.MyBodyCount+7<GameBoard.SnakeBodyCount):
            move_data = GameBoard.bfs(self,Point(data=head), 6,False,False) #go for tail
        return move_data

    def kill_snakes(self, data):
        move_data = -1
        # print("CountMyBody: ", GameBoard.MyBodyCount)
        # print("CountSnakeBody: ", GameBoard.SnakeBodyCount)
        if(GameBoard.MyBodyCount>GameBoard.SnakeBodyCount+1 and data["turn"]>50 and data["you"]["health"]>28):
            head = data["you"]["body"][0]
            move_data = GameBoard.bfs(self,Point(data=head), 1) # go for kill 
        return move_data