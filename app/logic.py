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
    DidIJustEat     = False #check if I am about to grow, to omit the tail as a valid square (because I'm growing)
    Storage_dict    = {} # Stores the health of an individual snake

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
        GameBoard.SnakeBodyCount = 0
        temporary_count = 0
        GameBoard.Storage_dict = {}
        for snake in data["board"]["snakes"]:

            if(snake["id"]==data["you"]["id"]):
                continue

            temporary_count = 0 
            for bodypart in snake["body"]:
                self.board[bodypart["x"]][bodypart["y"]] = 2

                temporary_count+=1

            '''
            TODO: store each health into a dictionary (call the function called storage)
            '''
            GameBoard.Storage(snake["id"],temporary_count) # Stores each opponent snakes 

            if(temporary_count>GameBoard.SnakeBodyCount):
                GameBoard.SnakeBodyCount = temporary_count

            # add tail
            tail = snake["body"][-1]
            self.board[tail["x"]][tail["y"]] = 3
            # add head
            head = snake["body"][0]
            self.board[head["x"]][head["y"]] = [1, snake["id"]]
        
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

        print("This is the created board")
        self.printBoard()

    def printBoard(self):
        for x in range(0, self.height):
            for y in range(0, self.width):
                print(self.board[y][x], end=' ')

            print()
        print(GameBoard.DidIJustEat)

    def bfs(self, start, num, status=True):
        """
        Start is the point on the board we start looking from
        Num is the value (look at top) that we are looking for
        Status is used to overide the safety protocol, this will default to True, unless specified
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

            # print("queue:", queue)
            # print("tile: ", end='')
            # try:
            #     print("tile: ",str(tile)," ","queue[0]: ",queue[0])
            # except IndexError:
            #     print("tile: ",str(tile)," ","queue is empty")
            
            tile_val = self.board[tile.x][tile.y]
            if(isinstance(tile_val,list)):
                tile_val = tile_val[0]

            if str(tile) in visited:
                continue

            visited.add(str(tile))

            # print(str(tile)," starting tests")
            if (GameBoard.DidIJustEat) and (tile_val == 6):
                GameBoard.DidIJustEat = False
                continue
            # print(str(tile)," DidIJustEat passed")

            if((not(self.safety_protocol(tile,num))) and status):
                continue
            # print(str(tile)," safety protocol passed")
            if(self.trap_protocol(tile)):
                continue
            # print(str(tile)," trap protocol passed")
            

            print(tile_val,"==",num)
            if tile_val == num:
                print("tile_val==num")
                value = self.get_relative_direction(start, tile, pg)
                print(value)
                return value
            
            print("Im going to keep looking!")
            if tile_val == 0:
                self.enqueue_around_point(tile, queue, visited, pg, num)
        
        return -1  #it didnt find what it was looking for 

    def enqueue_around_head(self, tile, queue):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]

        valid_tiles = [0,3,6,7]

        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0: # to check if our value is out of bounds
                continue # if it is out of bounds, the iteration is skipped
            
            tile_val = self.board[point.x][point.y] 
            
            if(isinstance(tile_val,list)):
                tile_val = tile_val[0]

            if tile_val in valid_tiles: #queue is only filled with 0,3,6,7 to start with
                queue.append(point)

    def enqueue_around_point(self, tile, queue, visted, parent_graph, num):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]
        
        safety_protocol = self.safety_protocol(tile,num)
        
        for point in points:
            if (not (point in visted) and safety_protocol):
                queue.append(point)
                parent_graph[point] = tile  # The points point to the tile

    def get_relative_direction(self, start, end, pg):
        print("im in the relative func")
        temp = end
        print(temp)
        print(end)
        while temp in pg: # gets where the end point was generated from 
            temp = pg[temp]
        print(temp)
        if(self.board[temp.x][temp.y]==7):
            GameBoard.DidIJustEat = True
        print(start.x," ",start.y)
        print(temp.x," ",temp.y)


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


    '''
    TODO: need to say that it is safe to hit a head if I'm beside a snake with a lower health (not necessarily the biggest health)
    plan:
        implement other snake's ID or health to their head
    '''
    # returns false if the tile is dangerous (beside an opponent snake head)
    # return true if the tile is safe
    def safety_protocol(self,tile, num):
        
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]

        if(GameBoard.AmIAlpha()):
            print("safety_protocol returned true via alpha")
            return True
        
        for point in points:


            print("safety protocol checking point: ",point)
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
                continue
            tile_val = self.board[point.x][point.y]
            if(isinstance(tile_val,list)):
                tile_val = tile_val[0]
            
            print(tile_val)
            
            if(tile_val==1): #it is broken here
                print("safety_protocol returned false")
                return False

        print("safety_protocol returned true via completion")
        return True

    '''
    TODO: need to check further squares AND if the tail is not in sight only then will it be a trapped square 
    '''
    # Returns True if the next tile is a trapped tile 
    # A tile is considered to be trapped if there are no possible moves after
    def trap_protocol(self,tile):
        points = [Point(x=tile.x, y=(tile.y - 1)), Point(x=tile.x, y=(tile.y + 1)), Point(x=(tile.x - 1), y=tile.y), Point(x=(tile.x + 1), y=tile.y)]

        for point in points:
            if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
                points.remove(point)
                continue
            
            tile_val = self.board[point.x][point.y]
            if(isinstance(tile_val,list)):
                tile_val = tile_val[0]
            
            if(tile_val == 5 or tile_val ==1):
                points.remove(point)

        if(len(points)==0):
            print("trap_protocol returned true")
            return True
        
        print("trap_protocol returned false")
        return False


    @staticmethod
    def AmIAlpha():
        if(GameBoard.MyBodyCount>GameBoard.SnakeBodyCount):
            return True
        return False 
    
    # Stores the health of an individual snake
    # health = health of the snake , id = unique id of the snake 
    # dictionary will be in the form of {id:health}
    @staticmethod
    def Storage(id_string,health):
        GameBoard.Storage_dict[id_string]=health



    # Will Trap a snake in a corner situation 
    @staticmethod
    def TrapKill():
        pass


    # implement a turtle and survive strategy for super late game scenario and we are smaller by a lot
    def turtle():
        pass


    #BROKEN
    def kill_snakes(self, data):
        move_data = -1
        print("CountMyBody: ", GameBoard.MyBodyCount)
        print("CountSnakeBody: ", GameBoard.SnakeBodyCount)
        if(GameBoard.MyBodyCount>GameBoard.SnakeBodyCount+1 and data["turn"]>50):
            head = data["you"]["body"][0]
            move_data = GameBoard.bfs(self,Point(data=head), 1, False) # go for kill 
        return move_data







'''

Games with bugs :   https://play.battlesnake.com/g/393fcb86-fac1-4cad-b3fe-5e65162f92c7/
                    https://play.battlesnake.com/g/8395aa92-1b17-4b8c-a742-ef8d76258d4b/
                    https://play.battlesnake.com/g/a0bca1c3-9d6a-476b-b5d4-ec64d3736a99/#
                    https://play.battlesnake.com/g/470299fc-9a04-4583-82fa-ebfc57714553/
                    https://play.battlesnake.com/g/e115a725-e4d4-4873-9ac2-62e14da676ec/
                    https://play.battlesnake.com/g/25d4a494-58b9-4c75-bc02-7e6de190ec91/
                    https://play.battlesnake.com/g/25d4a494-58b9-4c75-bc02-7e6de190ec91/
                    https://play.battlesnake.com/g/e481ff16-799e-4545-8920-0befbaca2974/



                    https://play.battlesnake.com/g/212df3fd-6a7b-4704-8a43-1f9a94eb1c02/
                    
                    kill_snake bug (dies of starvation)
                    https://play.battlesnake.com/g/9a0e8a9c-8276-4311-b2e4-7c810a21b1ef/


                    trapped squares
                    https://play.battlesnake.com/g/1c2762c9-e322-49ac-9975-6510674ffd78/

'''