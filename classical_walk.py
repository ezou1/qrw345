import argparse
import numpy as np
import matplotlib.pyplot as plt



def build_transition_matrix(n_nodes=8):
    M = np.zeros((n_nodes, n_nodes))
    for j in range(n_nodes):
        M[(j + 1) % n_nodes][j] += 0.5
        M[(j - 1) % n_nodes][j] += 0.5
    return M


def run_classical_walk(n_steps, n_nodes=8, start=0):
    M = build_transition_matrix(n_nodes)
    p = np.zeros(n_nodes)
    p[start] = 1.0
    for _ in range(n_steps):
        p = M @ p
    return p


def plot_distributions(steps_list, save):
    n    = len(steps_list)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, T in zip(axes, steps_list):
        p         = run_classical_walk(T)
        positions = np.arange(8)

        ax.bar(positions, p, color='#1D9E75', alpha=0.85, width=0.6)
        ax.set_title(f'$T = {T}$', fontsize=13)
        ax.set_xlabel('Position', fontsize=11)
        ax.set_xticks(positions)
        ax.set_xticklabels(positions, fontsize=9)
        ax.set_ylim(0, 1)

    axes[0].set_ylabel('Probability', fontsize=11)
    fig.suptitle('Classical random walk — 8-node cycle', fontsize=13)
    plt.tight_layout()

    if save:
        fname = f'cwalk_T{"_".join(str(t) for t in steps_list)}.png'
        fig.savefig(fname, dpi=150, bbox_inches='tight')
        print(f'Saved: {fname}')
    plt.show()


def print_matrix(n_nodes=8):
    M = build_transition_matrix(n_nodes)
    print(f'\nTransition matrix M ({n_nodes} x {n_nodes}):')
    print(np.array2string(M, precision=2, suppress_small=True))
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Classical random walk on an 8-node cycle.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--steps', type=int, nargs='+', default=[3],
        help='Step count(s) T to simulate.\nExample: --steps 1 2 3'
    )
    parser.add_argument(
        '--show-matrix', action='store_true',
        help='Print the 8x8 stochastic transition matrix to stdout.'
    )
    parser.add_argument(
        '--save', action='store_true',
        help='Save figure as PNG in the current directory.'
    )
    args = parser.parse_args()

    if args.show_matrix:
        print_matrix()

    plot_distributions(args.steps, args.save)


if __name__ == '__main__':
    main()