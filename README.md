# Quantum and Classical Random Walk Simulations

Simulation code for a PHYS 345 final project on quantum random walks.
Two scripts are provided:

- `quantum_walk.py` — discrete-time quantum random walk on an 8-node cycle, Hadamard coin, using the Qiskit Aer statevector simulator
- `classical_walk.py` — classical random walk on an 8-node cycle, using stochastic matrix iteration

---

## Requirements
```
Python >= 3.9
qiskit >= 1.0
qiskit-aer >= 0.13
numpy
matplotlib
```
Install all dependencies with:

```bash
pip install qiskit qiskit-aer numpy matplotlib
```

---

## quantum_walk.py

Simulates a Hadamard quantum walk on an 8-node cycle (1 coin qubit + 3 position qubits) using the Qiskit Aer statevector simulator.

### Basic usage

Run the walk at T=3 and display the probability distribution:

```bash
python quantum_walk.py
python quantum_walk.py --steps 3
```

### Multiple step counts

Pass multiple values to `--steps` to generate side-by-side subplots:

```bash
python quantum_walk.py --steps 1 2 3
```

### Circuit diagram

Display the Qiskit circuit diagram for the first value in `--steps`:

```bash
python quantum_walk.py --steps 1 --show-circuit
```

The circuit is printed as text to stdout and also drawn as a matplotlib figure.

### Saving figures

Add `--save` to write all generated plots as PNG files in the current directory:

```bash
python quantum_walk.py --steps 1 2 3 --save
python quantum_walk.py --steps 1 --show-circuit --save
```

Output filenames:
- `qwalk_T1_2_3.png`
- `circuit.png` (from --show-circuit)

### Shot count

The default is 8192 measurement shots. Increase for smoother distributions:

```bash
python quantum_walk.py --steps 1 2 3 --shots 32768
```

---

## classical_walk.py

Simulates a classical random walk on an 8-node cycle by iterating the stochastic transition matrix M. The walker starts at position 0.

### Basic usage

```bash
python classical_walk.py
python classical_walk.py --steps 3
```

### Multiple step counts

```bash
python classical_walk.py --steps 1 2 3
```

### Print the transition matrix

```bash
python classical_walk.py --show-matrix
```

Prints the full 8x8 stochastic matrix M to stdout.

### Saving figures

```bash
python classical_walk.py --steps 1 2 3 --save
```

Output filename:
- `cwalk_T1_2_3.png`

---

## Reproducing the paper figures

```bash
# Figure 1: quantum walk distributions T=1,2,3
python quantum_walk.py --steps 1 2 3 --save

# Figure 2: classical walk distributions T=1,2,3
python classical_walk.py --steps 1 2 3 --save

# Figure 3: circuit diagram for T=1
python quantum_walk.py --steps 1 --show-circuit --save
```

Upload `qwalk_T1_2_3.png`, `cwalk_T1_2_3.png`, and `circuit.png`
to the `figures/` folder in Overleaf.

---

## Notes

**Aer simulator vs real hardware.**
`quantum_walk.py` uses the Qiskit Aer statevector simulator throughout. Results match the exact theoretical distributions derived analytically. Running on real IBM-Q hardware would introduce gate noise, particularly from the multi-controlled X gates in the shift operator; the simulator eliminates this noise so that the figures directly confirm the theoretical predictions.

**Cycle boundary effects.**
Both simulations use a finite 8-node cycle. The variance scaling result sigma^2 ~ T^2/2 is derived for an infinite line; on the 8-node cycle, wrapping effects become visible around T=4 and beyond. The paper uses T=3 specifically to stay within the clean interference regime.