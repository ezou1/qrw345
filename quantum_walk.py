import argparse
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator



def build_shift(qc, coin, pos):
    n = len(pos)
    c = coin[0]

    # S+ (coin=0 → increment)
    qc.x(c)
    qc.cx(c, pos[0])
    for k in range(1, n):
        controls = [c] + [pos[j] for j in range(k)]
        for j in range(k):
            qc.x(pos[j])
        qc.mcx(controls, pos[k])
        for j in range(k):
            qc.x(pos[j])
    qc.x(c)

    # S- (coin=1 → decrement): S+ in reverse
    for k in range(n - 1, 0, -1):
        controls = [c] + [pos[j] for j in range(k)]
        for j in range(k):
            qc.x(pos[j])
        qc.mcx(controls, pos[k])
        for j in range(k):
            qc.x(pos[j])
    qc.cx(c, pos[0])


def build_walk_circuit(n_steps):
    coin_reg = QuantumRegister(1, 'coin')
    pos_reg  = QuantumRegister(3, 'pos')
    meas_reg = ClassicalRegister(3, 'meas')
    qc = QuantumCircuit(coin_reg, pos_reg, meas_reg)

    for _ in range(n_steps):
        qc.h(coin_reg[0])
        qc.barrier()
        build_shift(qc, coin_reg, pos_reg)
        qc.barrier()

    qc.measure(pos_reg, meas_reg)
    return qc



def run_circuit(qc, shots=8192):
    sim    = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    probs  = {i: 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        probs[int(bitstring, 2)] = count / shots
    return probs



def plot_distributions(steps_list, shots, save):
    n    = len(steps_list)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, T in zip(axes, steps_list):
        qc    = build_walk_circuit(T)
        probs = run_circuit(qc, shots=shots)
        positions = list(probs.keys())
        values    = list(probs.values())

        ax.bar(positions, values, color='#378ADD', alpha=0.85, width=0.6)
        ax.set_title(f'$T = {T}$', fontsize=13)
        ax.set_xlabel('Position', fontsize=11)
        ax.set_xticks(positions)
        ax.set_xticklabels(positions, fontsize=9)
        ax.set_ylim(0, 1)

    axes[0].set_ylabel('Probability', fontsize=11)
    fig.suptitle('Quantum random walk — Hadamard coin, 8-node cycle',
                 fontsize=13)
    plt.tight_layout()

    if save:
        fname = f'qwalk_T{"_".join(str(t) for t in steps_list)}.png'
        fig.savefig(fname, dpi=150, bbox_inches='tight')
        print(f'Saved: {fname}')
    plt.show()


def show_circuit(n_steps):
    qc = build_walk_circuit(n_steps)
    print(f'\nHadamard walk circuit, T={n_steps}:')
    print(qc.draw(output='text', fold=120))
    fig = qc.draw(output='mpl', fold=60, style='clifford')
    fig.suptitle(f'Hadamard walk circuit, T={n_steps}', fontsize=12)
    plt.tight_layout()
    plt.show()



def main():
    parser = argparse.ArgumentParser(
        description='Quantum random walk, 8-node cycle, Hadamard coin, Aer simulator.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--steps', type=int, nargs='+', default=[3],
        help='Step count(s) T to simulate.\nExample: --steps 1 2 3'
    )
    parser.add_argument(
        '--show-circuit', action='store_true',
        help='Display the circuit diagram for the first value in --steps.'
    )
    parser.add_argument(
        '--shots', type=int, default=8192,
        help='Number of measurement shots (default: 8192).'
    )
    parser.add_argument(
        '--save', action='store_true',
        help='Save figure as PNG in the current directory.'
    )
    args = parser.parse_args()

    if args.show_circuit:
        show_circuit(args.steps[0])

    plot_distributions(args.steps, args.shots, args.save)


if __name__ == '__main__':
    main()