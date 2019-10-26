# battleship-ai

A project to play Battleship against a CPU player.

### Usage

Requires Python 3.6 or greater

Install requirements:
```bash
pip install -r requirements.txt
python setup.py install # or python setup.py develop
```

Play the game:
```bash
python main.py
```

### Development

#### Install dev requirements
```bash
pip install -r dev-requirements.txt
python setup.py develop
```

### Tests
Install the dev requirements
```bash
pytest --cov=battleship battleship
```

### Linter
Install the dev requirements
```bash
flake8 battleship
```
