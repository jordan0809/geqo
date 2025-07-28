# GEQO

The first step towards our own quantum programming language.


## Installation

### Remote installation

To install the package remotely using `git+ssh`, follow these steps:

#### with pip
```bash
pip install -I git+ssh://gitlabserv/josq/geqo.git
```

#### with uv
```bash
uv add git+ssh://gitlabserv/josq/geqo.git
```

### Local Installation (for development)

To install the package locally, follow these steps:

1. Clone the repository:
```bash
git clone gitlabserv:josq/geqo
```
2. Install it
#### with pip
```bash
pip install -e .[dev,visualization,sympy]
```


#### with uv
The `pyproject.toml` is already configured to support uv
```bash
uv sync --extra visualization --extra sympy
```

## Optional Installation Extras

The GEQO package supports the following optional installation extras:

 - `[dev]`: Includes development dependencies, such as testing and linting tools.
 - `[visualization]`: Includes functions for data visualization. This includes functions to plot quantum circuits in both LaTeX and Matplotlib, as well as create bar plots for measurement outcomes
 - `[sympy]`: Includes the SymPy library for symbolic mathematics. This enables the use of SymPy-based simulators for symbolic math operations.

You can choose to install any combination of these extras by including them in the installation command, as shown in the examples above. For example, to install the core functionality and the visualization extras, you would use:

```bash
pip install -I git+ssh://gitlabserv/josq/geqo.git[dev,visualization]
```
or
```bash
uv add git+ssh://gitlabserv/josq/geqo.git --optional dev --optional visualization
```
This allows you to customize the installation to include only the features you need for your specific use case.

## Contributing
Please ensure that your code is formatted using ruff before submitting code.

To format your code using ruff, follow these steps:

#### with pip
To install ruff:
```bash
pip install ruff
```
To format:
```bash
ruff check --fix .
ruff format .
```
#### with uv
You can use ruff as a tool, there is no need to install it
```bash
uvx ruff check --fix .
uvx ruff format .
```

## Unit test
Please ensure that your code does not break any core functionalities and passes all `pytest` tests. 

To test for errors in the package, please run the following command from the project root:

```bash
python -m pytest tests/ -v --cov=src/ --cov-report=term-missing
```
