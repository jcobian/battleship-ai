# battleship-ai

A project to play Battleship against a CPU player.

The CPU is "smart" enough in that it keeps track of the last successful moves it has made, and then tries moves near that spot until it has taken down a ship.

The game is played in the terminal. In game prompts and instructions should help you navigate and play.

If the game is too big or too small to fit in your window, consider adjusting your text size in the terminal.

### Usage

#### Without docker:
Requires Python 3.6 or greater. As of now, there are no major dependencies so this should be fine. If you run into issues, use docker.

Run:
```bash
python main.py
```

#### With docker:
First, build the docker image
```bash
docker build . -t battleship-ai
```

Now run the container to play:
```bash
docker run -it battleship-ai
```

### Development

#### Install dev requirements
```bash
pip install -r dev-requirements.txt
python setup.py develop
```

### Tests
Install the dev requirements, then run:
```bash
pytest --cov=battleship battleship
```

### Linter
Install the dev requirements, then run:
```bash
flake8 battleship
```

### mypy
This repo uses mypy to make sure any type annotations are correct.
To run, install the dev requirements, then run:
```bash
mypy battleship
```
