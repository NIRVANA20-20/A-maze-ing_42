VENV = venv
PYTHON = $(VENV)/bin/python
SYS_PYTHON = python3
PIP = $(VENV)/bin/pip
FILES = Controlling/maze.py \
		Controlling/maze_controller.py \
		Parsing/parser.py \
		Mazegen/generater.py\
		my_mlx/my_mlx.py\
		Rendring/CellImage.py\
		Rendring/rendrer.py\
		Themes/themes.py\
		a_maze_ing.py\

install: $(VENV)
	$(PIP) install flake8
	$(PIP) install mypy
	$(PIP) install ./*.whl

run: 
	$(PYTHON)  a_maze_ing.py config.txt
	
$(VENV):
	$(SYS_PYTHON) -m venv $(VENV)
clean:
	rm -rf  __pycache__ */__pycache__ */*/__pycache__
	rm -rf $(VENV)

lint:
	$(VENV)/bin/flake8 $(FILES) 
	$(VENV)/bin/mypy $(FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs	

pdb:
	$(PYTHON) -m pdb A_maze_ing/amazing.py config.txt
