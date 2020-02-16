# Patch Notes 

### Beta 1.10

#### What is next

Add a combination of Astar algorithm to be able to provide a 'heuristic' for each square.
Being able to optimize each square so skippy knows where to go.
I
#### Class Attributes

SnakeBodyCount and MyBodyCount - keep track of how large my snake and the opponent snake(largest snake).

DidIJustEat - keeps track wheter or not my snake has eaten. (purpose: inorder not to collide with my tail once I have eaten a food). 

Storage_dict - A dictionary of all enemny snakes in the form of {id:size} to keep track of all snake sizes (how many food eaten).

#### New Functions

safety_protocol - returns false if the tile is dangerous (beside an opponent snake head), if safe then returns true

trap_protocol - returns True if the next tile is a trapped tile, A tile is considered to be trapped if there are no possible moves after

AmIAlpha - returns True if I am the biggest snake in the arena, false otherwise

Storage - stores a the id and size of opponent snakes into Storage_dict, id:size

kill_snakes - Will target the head of opponent snakes if skippy is bigger by 1, e.g skippy:16 opponent:15 it will execute 
while skippy:15 opponent:15, skippy will go for food(or the next request)


#### Fixes

bfs - now returns -1 if queue becomes empty (exists the loop)


#### Replay and Bugs

Skippy needs to read the future and avoid dying like this
https://play.battlesnake.com/g/67d67cd6-c825-48d1-b23a-e9d6498055a6/#

I wanted skippy to go down and not the food, not sure why safety_protocol was not working (needs implementing)
https://play.battlesnake.com/g/6703ff00-9268-4c71-803f-febaed464385/#

Enemy Snake grew by 1 and I went for their tail
https://play.battlesnake.com/g/9ed71d45-d54e-4b12-90e4-efcd9eeaaa3c/#

kill_snakes - skippy will keep on hunting enenmy head until he starves or until they grow bigger than him 
and skippy will proceed to eat to match them. 

Should have gone for the green tail
https://play.battlesnake.com/g/c00d8640-432a-41a4-a4c2-5ed594af1967/#


#### End of Patch Notes


# starter-snake-python

A simple [Battlesnake AI](http://battlesnake.io) written in Python. 

Visit [https://github.com/battlesnakeio/community/blob/master/starter-snakes.md](https://github.com/battlesnakeio/community/blob/master/starter-snakes.md) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/battlesnakeio/starter-snake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:<your github username>/starter-snake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Test your snake by sending a curl to the running snake
```
curl -XPOST -H 'Content-Type: application/json' -d '{ "hello": "world"}' http://localhost:8080/start
```

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```

## Questions?

Email [hello@battlesnake.com](mailto:hello@battlesnake.com), or tweet [@battlesnakeio](http://twitter.com/battlesnakeio).
