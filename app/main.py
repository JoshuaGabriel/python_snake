import json
import os
import random
import bottle


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

    print("turn: ",data["turn"])


    if(move_data==-1):
        move_data = board.kill_snakes(data)

    # returns -1 if he is trapped (no food)
    if(move_data==-1):
        move_data = board.bfs(Point(data=head), 7) # go for your Food

    if(move_data==-1):
        move_data = board.bfs(Point(data=head), 6) # go for your tail

    # last resort option
    #1 Priority
    '''
    TODO: Not enter Trap phases (1 block beside a snake if im smaller)
    
    #Essential Priority (survival)
    TODO: Kill strategy, their head on the edge and mine is x+1,y x-1,y x,y+1 x,y-1 then trap them (also implement to AVOID dying to this) (mid game3) 
            - Implemented not trapping myself in a 2x2 radius of an enemy head 
    TODO: Start phase, when both snakes have to take the same spots try not to die
    
    
    #Bonus Priority
    TODO: If I'm the biggest snake by 2-3 foods then I'll kill (done) 
    TODO: If it is a 1vs1 scenario and I am smaller then I need to collect food 
    '''

    if(move_data==-1):
        move_data = board.bfs(Point(data=head), 3) # go for enemy tail
    
    if(move_data==-1):
        move_data = board.bfs(Point(data=head), 0) # go for empty spaces


    direction = directions[move_data]
    print("Direction: ", direction)

    return move_response(direction)






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
