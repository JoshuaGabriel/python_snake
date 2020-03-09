import json
import os
import random
import bottle
import time

from app.api import ping_response, start_response, move_response, end_response
from app.logic import *

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#0398fc"
    headType = "pixel"
    tailType = "pixel"

    return start_response(color,headType,tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json
    directions = ['up', 'down', 'left', 'right']
    move_data = -1 
    board = GameBoard(data=data)
    head = data["you"]["body"][0]
    print(data["you"]["shout"])
    print("turn: ",data["turn"])
    # start = time.time()
    if(move_data==-1):
        # print("trying turtle")
        move_data = board.turtle(data)

    if(move_data==-1):
        # print("trying kill")
        move_data = board.kill_snakes(data)
        
    if(move_data==-1):
        # print("trying food")
        move_data = board.bfs(Point(data=head), 7) # go for your Food

    if(move_data==-1):
        # print("trying my tail")
        move_data = board.bfs(Point(data=head), 6) # go for your tail

    if(move_data==-1):
        # print("trying my tail")
        move_data = board.bfs(Point(data=head), 6, False, False) # go for your tail

    # last resort option
    if(move_data==-1):
        # print("trying enemy tail")
        move_data = board.bfs(Point(data=head), 3) # go for enemy tail

    if(move_data==-1):
        # print("trying enemy tail")
        move_data = board.bfs(Point(data=head), 3, False,False) # go for enemy tail

    if(move_data==-1):
        # print("trying empty space")
        move_data = board.bfs(Point(data=head), 0,False) # go for empty spaces
    
    if(move_data==-1):
        # print("trying empty space v2")
        move_data = board.bfs(Point(data=head), 0,False,False) # go for empty spaces

    # Keep going in the same direction as you were (more likely to be the best move)
    
    direction = directions[move_data]

    # print("Direction: ", direction)
    # end = time.time()
    
    # print("Time elapsed: ",end - start)
    matrix = board.GetBoard()


    return move_response(direction,str(data["turn"]))

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )