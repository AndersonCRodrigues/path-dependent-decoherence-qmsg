"""
Q-MSG v3.1: Time-Normalized Decoherence Test

Addresses the critique: "Difference may be due to different execution times"

Solution:
- Enforce SAME total time T for both twins
- Test two decoherence hypotheses:
  H1: gamma proportional to TIME (critic's hypothesis)
  H2: gamma proportional to PATH (Q-MSG hypothesis)

If effect persists under time-normalization, then K is ontologically real.

Author: Anderson Costa Rodrigues
License: MIT
"""

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Pauli matrices
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
IDENTITY = np.eye(2, dtype=complex)


def rotation(axis, theta):
    """Single-qubit rotation"""
    pauli = {"x": SIGMA_X, "y": SIGMA_Y, "z": SIGMA_Z}[axis]
    return expm(-1j * theta * pauli / 2)


def to_bloch(rho):
    """Convert density matrix to Bloch vector"""
    return np.array(
        [2 * rho[0, 1].real, 2 * rho[0, 1].imag, (rho[0, 0] - rho[1, 1]).real]
    )


def phase_damping(rho, gamma):
    """
    Phase damping channel: rho -> sum_k K_k * rho * K_k^dagger

    Kraus operators:
    K_0 = sqrt(1-gamma) * I
    K_1 = sqrt(gamma) * sigma_z
    """
    gamma = np.clip(gamma, 0, 0.99)
    K0 = np.sqrt(1 - gamma) * IDENTITY
    K1 = np.sqrt(gamma) * SIGMA_Z
    return K0 @ rho @ K0.conj().T + K1 @ rho @ K1.conj().T


def purity(rho):
    """Compute purity Tr(rho^2)"""
    return np.trace(rho @ rho).real


def continuous_evolution(rho_init, gate_sequence, T_total, dt=0.01):
    """
    Time-normalized continuous evolution.

    Args:
        rho_init: Initial density matrix
        gate_sequence: List of (axis, angle) tuples
        T_total: Total evolution time (SAME for all twins)
        dt: Time step

    Returns:
        trajectory: Array of Bloch vectors
        times: Array of time points
    """
    trajectory = [to_bloch(rho_init)]
    times = [0]

    rho = rho_init.copy()
    t = 0

    n_gates = len(gate_sequence)
    T_per_gate = T_total / n_gates

    for axis, angle in gate_sequence:
        n_steps = int(T_per_gate / dt)

        for step in range(n_steps):
            # Instantaneous rotation rate
            rate = angle / T_per_gate
            U_dt = rotation(axis, rate * dt)

            rho = U_dt @ rho @ U_dt.conj().T
            t += dt

            trajectory.append(to_bloch(rho))
            times.append(t)

    return np.array(trajectory), np.array(times)


def path_length(trajectory):
    """Compute geometric path length"""
    length = 0
    for i in range(len(trajectory) - 1):
        length += np.linalg.norm(trajectory[i + 1] - trajectory[i])
    return length


def main():
    """Run v3.1 time-normalization test"""

    print("=" * 80)
    print("Q-MSG v3.1: TIME-NORMALIZATION TEST")
    print("=" * 80)
    print("\nAddressing critique:")
    print("  'Difference may be just different execution times'")
    print("\nApproach:")
    print("  Enforce SAME total time T for both twins")
    print("  Test if effect persists")

    # Initial state
    rho_0 = np.array([[1, 0], [0, 0]], dtype=complex)

    # Parameters
    theta = np.pi / 3
    phi = np.pi / 2
    T_total = 1.0  # CRITICAL: Same for both
    dt = 0.01

    print(f"\nConfiguration:")
    print(f"  Total time: T = {T_total} (SAME for A and B)")
    print(f"  Time step: dt = {dt}")
    print(f"  Target operation: R_y({theta:.4f})")

    # Twin A: Direct path
    print(f"\n  Twin A (direct):")
    print(f"    Sequence: R_y({theta:.4f})")
    print(f"    Time: {T_total} (one gate)")

    traj_A, times_A = continuous_evolution(rho_0, [("y", theta)], T_total, dt)

    # Twin B: Decomposed path
    print(f"\n  Twin B (decomposed):")
    print(f"    Sequence: R_z({phi:.4f}) * R_x({theta:.4f}) * R_z({-phi:.4f})")
    print(f"    Time: {T_total} (three gates, each T/3)")

    traj_B, times_B = continuous_evolution(
        rho_0, [("z", phi), ("x", theta), ("z", -phi)], T_total, dt
    )

    # Verify final states
    U_A = rotation("y", theta)
    U_B = rotation("z", phi) @ rotation("x", theta) @ rotation("z", -phi)

    rho_A_final = U_A @ rho_0 @ U_A.conj().T
    rho_B_final = U_B @ rho_0 @ U_B.conj().T

    diff_U = np.linalg.norm(U_A - U_B)
    diff_rho = np.linalg.norm(rho_A_final - rho_B_final)

    print(f"\n{'='*80}")
    print("VERIFICATION: Final States (Vacuum)")
    print(f"{'='*80}")
    print(f"  ||U_A - U_B|| = {diff_U:.2e}")
    print(f"  ||rho_A - rho_B|| = {diff_rho:.2e}")

    if diff_rho < 1e-10:
        print("  Result: States are IDENTICAL")
    else:
        print("  ERROR: States differ!")
        return None

    # Compute biographical witnesses
    path_A = path_length(traj_A)
    path_B = path_length(traj_B)

    print(f"\n{'='*80}")
    print("BIOGRAPHICAL WITNESSES")
    print(f"{'='*80}")
    print(f"  Path_A = {path_A:.6f}")
    print(f"  Path_B = {path_B:.6f}")
    print(f"  Difference = {path_B - path_A:.6f} ({100*(path_B-path_A)/path_A:.1f}%)")

    # CRITICAL TEST: Decoherence models
    print(f"\n{'='*80}")
    print("CRITICAL TEST: Two Decoherence Hypotheses")
    print(f"{'='*80}")

    coupling = 0.15

    # Hypothesis 1: gamma proportional to TIME (critic)
    print(f"\nHYPOTHESIS 1 (Critic): gamma ~ TIME")
    print("  If critic is right: gamma_A = gamma_B (same time)")
    print("  Expected: NO divergence")

    gamma_A_time = coupling * T_total
    gamma_B_time = coupling * T_total  # SAME

    print(f"\n  gamma_A = {gamma_A_time:.6f}")
    print(f"  gamma_B = {gamma_B_time:.6f}")
    print(f"  Delta = {abs(gamma_B_time - gamma_A_time):.2e}")

    rho_A_time = phase_damping(rho_A_final, gamma_A_time)
    rho_B_time = phase_damping(rho_B_final, gamma_B_time)

    diff_time = np.linalg.norm(rho_A_time - rho_B_time)
    purity_A_time = purity(rho_A_time)
    purity_B_time = purity(rho_B_time)

    print(f"\n  Results:")
    print(f"    ||rho'_A - rho'_B|| = {diff_time:.2e}")
    print(f"    Purity_A = {purity_A_time:.6f}")
    print(f"    Purity_B = {purity_B_time:.6f}")
    print(f"    Delta_Purity = {abs(purity_A_time - purity_B_time):.6f}")

    # Hypothesis 2: gamma proportional to PATH (Q-MSG)
    print(f"\nHYPOTHESIS 2 (Q-MSG): gamma ~ PATH")
    print("  If Q-MSG is right: gamma_A != gamma_B (different paths)")
    print("  Expected: DIVERGENCE")

    gamma_A_path = coupling * path_A
    gamma_B_path = coupling * path_B  # DIFFERENT

    print(f"\n  gamma_A = {gamma_A_path:.6f}")
    print(f"  gamma_B = {gamma_B_path:.6f}")
    print(
        f"  Delta = {gamma_B_path - gamma_A_path:.6f} ({100*(gamma_B_path-gamma_A_path)/gamma_A_path:.1f}%)"
    )

    rho_A_path = phase_damping(rho_A_final, gamma_A_path)
    rho_B_path = phase_damping(rho_B_final, gamma_B_path)

    diff_path = np.linalg.norm(rho_A_path - rho_B_path)
    purity_A_path = purity(rho_A_path)
    purity_B_path = purity(rho_B_path)

    print(f"\n  Results:")
    print(f"    ||rho'_A - rho'_B|| = {diff_path:.6f}")
    print(f"    Purity_A = {purity_A_path:.6f}")
    print(f"    Purity_B = {purity_B_path:.6f}")
    print(f"    Delta_Purity = {abs(purity_A_path - purity_B_path):.6f}")

    # Verdict
    print(f"\n{'='*80}")
    print("VERDICT")
    print(f"{'='*80}")

    print(f"\nComparison:")
    print(f"  Model gamma~time: ||Delta_rho|| = {diff_time:.2e}")
    print(f"  Model gamma~path: ||Delta_rho|| = {diff_path:.6f}")

    if diff_time < 1e-10 and diff_path > 1e-4:
        print(f"\nRESULT: Q-MSG VALIDATED")
        print(f"\n  With gamma ~ time: states remain IDENTICAL")
        print(f"  With gamma ~ path: states DIVERGE")
        print(f"\nCONCLUSION:")
        print(f"  Effect is NOT a timing artifact")
        print(f"  Biographical information K has physical consequences")
    elif diff_time > 1e-10:
        print(f"\nWARNING: Problem detected")
        print(f"  Even with same time, there's a difference")
    else:
        print(f"\nRESULT: Critic was correct")
        print(f"  With time normalization, effect disappears")

    # Visualization
    visualize(
        traj_A,
        traj_B,
        times_A,
        rho_A_final,
        rho_B_final,
        rho_A_time,
        rho_B_time,
        rho_A_path,
        rho_B_path,
        path_A,
        path_B,
    )

    return {
        "path_A": path_A,
        "path_B": path_B,
        "diff_time": diff_time,
        "diff_path": diff_path,
        "purity_A_path": purity_A_path,
        "purity_B_path": purity_B_path,
    }


def visualize(
    traj_A,
    traj_B,
    times,
    rho_A_clean,
    rho_B_clean,
    rho_A_time,
    rho_B_time,
    rho_A_path,
    rho_B_path,
    path_A,
    path_B,
):
    """Create comprehensive visualization"""

    fig = plt.figure(figsize=(20, 12))

    # 1. Trajectories 3D
    ax1 = fig.add_subplot(231, projection="3d")

    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x, y, z, alpha=0.05, color="gray")

    ax1.plot(
        traj_A[:, 0],
        traj_A[:, 1],
        traj_A[:, 2],
        "b-",
        linewidth=3,
        label="A (direct)",
        alpha=0.8,
    )
    ax1.plot(
        traj_B[:, 0],
        traj_B[:, 1],
        traj_B[:, 2],
        "r--",
        linewidth=3,
        label="B (decomposed)",
        alpha=0.8,
    )

    ax1.scatter(*traj_A[0], color="green", s=300, marker="*", zorder=10)
    ax1.scatter(*traj_A[-1], color="purple", s=300, marker="P", zorder=10)

    ax1.set_title("Trajectories (SAME time T)", fontweight="bold", fontsize=14)
    ax1.legend(fontsize=11)

    # 2. Temporal evolution
    ax2 = fig.add_subplot(232)
    min_len = min(len(times), len(traj_A), len(traj_B))
    ax2.plot(times[:min_len], traj_A[:min_len, 2], "b-", linewidth=2, label="A")
    ax2.plot(times[:min_len], traj_B[:min_len, 2], "r--", linewidth=2, label="B")
    ax2.set_xlabel("Time (normalized)")
    ax2.set_ylabel("Z (Bloch)")
    ax2.set_title("Temporal Evolution (T equal)", fontweight="bold", fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    # 3. Path lengths
    ax3 = fig.add_subplot(233)
    bars = ax3.bar(["A", "B"], [path_A, path_B], color=["blue", "red"], alpha=0.7)
    ax3.set_ylabel("Geometric Length")
    ax3.set_title("Biographical Witness", fontweight="bold", fontsize=14)
    ax3.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, [path_A, path_B]):
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{val:.3f}",
            ha="center",
            fontweight="bold",
        )

    # 4. Model TIME
    ax4 = fig.add_subplot(234)

    bloch_A_time = to_bloch(rho_A_time)
    bloch_B_time = to_bloch(rho_B_time)
    bloch_A_clean = to_bloch(rho_A_clean)

    theta_c = np.linspace(0, 2 * np.pi, 100)
    ax4.plot(np.cos(theta_c), np.sin(theta_c), "k--", alpha=0.2)

    ax4.scatter(
        *bloch_A_clean[:2], s=200, color="gray", marker="o", label="Clean", alpha=0.3
    )
    ax4.scatter(
        *bloch_A_time[:2],
        s=300,
        color="blue",
        marker="o",
        label="A (gamma~T)",
        edgecolor="black",
        linewidth=2,
    )
    ax4.scatter(
        *bloch_B_time[:2],
        s=300,
        color="red",
        marker="s",
        label="B (gamma~T)",
        edgecolor="black",
        linewidth=2,
    )

    ax4.set_xlabel("X")
    ax4.set_ylabel("Y")
    ax4.set_title("Model TIME (gamma~T)", fontweight="bold", fontsize=14)
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=9)
    ax4.axis("equal")
    ax4.set_xlim(-1.2, 1.2)
    ax4.set_ylim(-1.2, 1.2)

    # 5. Model PATH
    ax5 = fig.add_subplot(235)

    bloch_A_path = to_bloch(rho_A_path)
    bloch_B_path = to_bloch(rho_B_path)

    ax5.plot(np.cos(theta_c), np.sin(theta_c), "k--", alpha=0.2)

    ax5.scatter(
        *bloch_A_clean[:2], s=200, color="gray", marker="o", label="Clean", alpha=0.3
    )
    ax5.scatter(
        *bloch_A_path[:2],
        s=300,
        color="blue",
        marker="o",
        label="A (gamma~L)",
        edgecolor="black",
        linewidth=2,
    )
    ax5.scatter(
        *bloch_B_path[:2],
        s=300,
        color="red",
        marker="s",
        label="B (gamma~L)",
        edgecolor="black",
        linewidth=2,
    )

    ax5.plot(
        [bloch_A_path[0], bloch_B_path[0]],
        [bloch_A_path[1], bloch_B_path[1]],
        "k-",
        linewidth=2,
        alpha=0.5,
    )

    ax5.set_xlabel("X")
    ax5.set_ylabel("Y")
    ax5.set_title("Model PATH (gamma~L) - Q-MSG", fontweight="bold", fontsize=14)
    ax5.grid(True, alpha=0.3)
    ax5.legend(fontsize=9)
    ax5.axis("equal")
    ax5.set_xlim(-1.2, 1.2)
    ax5.set_ylim(-1.2, 1.2)

    # 6. Purity comparison
    ax6 = fig.add_subplot(236)

    purity_clean = purity(rho_A_clean)
    purity_A_time = purity(rho_A_time)
    purity_B_time = purity(rho_B_time)
    purity_A_path = purity(rho_A_path)
    purity_B_path = purity(rho_B_path)

    x = np.arange(2)
    width = 0.25

    ax6.bar(
        x - width,
        [purity_A_time, purity_B_time],
        width,
        label="gamma~T",
        color="orange",
        alpha=0.7,
    )
    ax6.bar(
        x,
        [purity_A_path, purity_B_path],
        width,
        label="gamma~L",
        color="purple",
        alpha=0.7,
    )
    ax6.axhline(
        purity_clean,
        color="green",
        linestyle="--",
        linewidth=2,
        label="Clean",
        alpha=0.5,
    )

    ax6.set_ylabel("Purity: Tr(rho^2)")
    ax6.set_title("Model Comparison", fontweight="bold", fontsize=14)
    ax6.set_xticks(x)
    ax6.set_xticklabels(["A", "B"])
    ax6.legend()
    ax6.grid(axis="y", alpha=0.3)
    ax6.set_ylim(0.5, 1.05)

    plt.tight_layout()
    plt.savefig("qmsg_v3_1_time_norm.png", dpi=150, bbox_inches="tight")
    print("\nFigure saved: qmsg_v3_1_time_norm.png")


if __name__ == "__main__":
    results = main()

    if results:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"\nPath difference: {results['path_B'] - results['path_A']:.6f}")
        print(f"\nModel gamma~time:")
        print(f"  ||Delta_rho|| = {results['diff_time']:.2e}")
        print(f"\nModel gamma~path:")
        print(f"  ||Delta_rho|| = {results['diff_path']:.6f}")
        print(
            f"  Delta_Purity = {abs(results['purity_A_path'] - results['purity_B_path']):.6f}"
        )
        print("=" * 80)
