VENV = venv
PYTHON = $(VENV)/bin/python
SYS_PYTHON = python3
PIP = $(VENV)/bin/pip
FILES = A_maze_ing/maze.py \
		A_maze_ing/mazecontroller.py \
		Parsing/parser.py \
		Generating/generater.py\
		Generating/maze\
		my_mlx/my_mlx.p\
		Rendring/CellImage.py\
		Rendring/rendrer.py\
		themes/themes.py\
		amazing.py\

install: $(VENV)
	$(PIP) install flake8
	$(PIP) install mypy

run: 
	$(PYTHON)  amazing.py config.txt
	
$(VENV):
	$(SYS_PYTHON) -m venv $(VENV)
clean:
	rm -rf  __pycache__ */__pycache__ */*/__pycache__
	rm -rf $(VENV) dist/ *egg-info build *dist-info

lint:
	$(VENV)/bin/flake8 $(FILES) 
	$(VENV)/bin/mypy $(FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs	


pdb:
	$(PYTHON) -m pdb A_maze_ing/amazing.py config.txt

.PHONY: dependecies clean lint install