# Patch Notes 

### Beta 1.00

#### Class Attributes

SnakeBodyCount and MyBodyCount - keep track of how large my snake and the opponent snake(largest snake).

DidIJustEat - keeps track wheter or not my snake has eaten. (purpose: inorder not to collide with my tail once I have eaten a food). 

Storage_dict - A dictionary of all enemny snakes in the form of {id:size} to keep track of all snake sizes (how many food eaten).

#### New Functions

safety_protocol

trap_protocol

AmIAlpha

Storage

kill_snakes


#### Fixes

bfs - now returns -1 if queue becomes empty (exists the loop)


#### Replay Bugs


I wanted skippy to go down and not the food, not sure why safety_protocol was not working
https://play.battlesnake.com/g/6703ff00-9268-4c71-803f-febaed464385/#




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
