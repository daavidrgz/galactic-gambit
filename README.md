# Developing

Use Black Formatter

In order to work in a virtual environment:

```
python3 -m venv env
source env/bin/activate
```

And to leave the virtual environment, execute:

```
deactivate
```

To generate the requirements.txt file, execute:

```
pip freeze > requirements.txt
```

> Remember to be in the virtual environment before executing this.

# Running the game

To run the game, execute from the root directory:

```
pip install -r requirements.txt
python3 run_game.py
```
