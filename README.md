# geqo
geqo is a framework for constructing and describing quantum circuits and executing them on simulators and on quantum hardware devices.

The documentation can be found [here](https://geqo.jos-quantum.de/intro.html).

## Installation

### From this fork (Recommended)
To install this version of geqo with all optional features (cupy, numpy, visualization, etc.) and recent updates:

```bash
pip install "geqo[sympy,numpy,cupy,visualization,dev] @ git+https://github.com/jordan0809/geqo.git"
```

### For Development
If you want to modify the code locally:

1. Clone the repository: `git clone https://github.com/jordan0809/geqo.git`
2. Install in editable mode with all options: `pip install -e ".[sympy,numpy,cupy,visualization,dev]"`


## Running a simple example
- the example task is to get unitary of a quantum circuit for the EPR pair generation
- start Python in the environment from the steps above
- run the following commands:

```
from geqo.gates import Hadamard, CNOT
from geqo.core import Sequence
seq=Sequence(["q1","q2"],[], [ (Hadamard(),["q1"], []), (CNOT(), ["q1","q2"], []) ])

from geqo.simulators import simulatorUnitarySymPy
sim=simulatorUnitarySymPy(2)
sim.apply(seq,[0,1])
sim.u
```

The expected result is
```
Matrix([
[sqrt(2)/2,         0,  sqrt(2)/2,          0],
[        0, sqrt(2)/2,          0,  sqrt(2)/2],
[        0, sqrt(2)/2,          0, -sqrt(2)/2],
[sqrt(2)/2,         0, -sqrt(2)/2,          0]])
```

