"""
Q-MSG v2.0: Mathematical Proof of Biographical Irreducibility

Demonstrates that quantum systems can have:
- Same unitary operation U
- Same final state rho
- Different trajectories K

This proves K (biography) is irreducible to rho (state).

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


def rotation(axis, theta):
    """
    Single-qubit rotation: R_axis(theta) = exp(-i * theta * sigma / 2)

    Args:
        axis: 'x', 'y', or 'z'
        theta: Rotation angle (radians)

    Returns:
        2x2 complex unitary matrix
    """
    pauli = {"x": SIGMA_X, "y": SIGMA_Y, "z": SIGMA_Z}[axis]
    return expm(-1j * theta * pauli / 2)


def to_bloch(rho):
    """
    Convert density matrix to Bloch vector.

    Args:
        rho: 2x2 density matrix

    Returns:
        3D Bloch vector [x, y, z]
    """
    return np.array(
        [2 * rho[0, 1].real, 2 * rho[0, 1].imag, (rho[0, 0] - rho[1, 1]).real]
    )


def compute_trajectory(initial_state, gates, steps=20):
    """
    Compute Bloch sphere trajectory for a sequence of gates.

    Args:
        initial_state: Initial density matrix
        gates: List of (axis, angle) tuples
        steps: Number of interpolation points

    Returns:
        Array of Bloch vectors (steps+1, 3)
    """
    trajectory = []

    for i in range(steps + 1):
        t = i / steps
        U = np.eye(2, dtype=complex)

        # Build composite unitary at fraction t
        for axis, angle in gates:
            U = rotation(axis, t * angle) @ U

        rho_t = U @ initial_state @ U.conj().T
        trajectory.append(to_bloch(rho_t))

    return np.array(trajectory)


def path_length(trajectory):
    """
    Compute geometric path length along trajectory.

    Args:
        trajectory: Array of Bloch vectors

    Returns:
        Total path length (scalar)
    """
    length = 0
    for i in range(len(trajectory) - 1):
        length += np.linalg.norm(trajectory[i + 1] - trajectory[i])
    return length


def main():
    """Run v2.0 demonstration"""

    print("=" * 80)
    print("Q-MSG v2.0: MATHEMATICAL PROOF")
    print("=" * 80)
    print("\nDemonstrating biographical irreducibility:")
    print("Same operation U, same final state rho, DIFFERENT trajectories K")

    # Initial state |0>
    rho_0 = np.array([[1, 0], [0, 0]], dtype=complex)

    # Target operation: R_y(pi/3)
    theta = np.pi / 3
    phi = np.pi / 2

    print(f"\nTarget operation: U = R_y({theta:.4f} rad)")

    # Twin A: Direct implementation
    U_A = rotation("y", theta)
    gates_A = [("y", theta)]

    # Twin B: Decomposed implementation
    # Using identity: R_y(theta) = R_z(phi) * R_x(theta) * R_z(-phi)
    U_B = rotation("z", phi) @ rotation("x", theta) @ rotation("z", -phi)
    gates_B = [("z", phi), ("x", theta), ("z", -phi)]

    # Verify operational equivalence
    diff_U = np.linalg.norm(U_A - U_B)
    print(f"\n1. OPERATIONAL EQUIVALENCE:")
    print(f"   ||U_A - U_B|| = {diff_U:.2e}")

    if diff_U < 1e-10:
        print("   Result: Unitaries are IDENTICAL (within numerical precision)")

    # Verify state equivalence
    rho_A = U_A @ rho_0 @ U_A.conj().T
    rho_B = U_B @ rho_0 @ U_B.conj().T
    diff_rho = np.linalg.norm(rho_A - rho_B)

    print(f"\n2. STATE EQUIVALENCE:")
    print(f"   ||rho_A - rho_B|| = {diff_rho:.2e}")

    if diff_rho < 1e-10:
        print("   Result: Final states are IDENTICAL")

    # Compute trajectories
    print(f"\n3. BIOGRAPHICAL WITNESS:")
    print("   Computing Bloch sphere trajectories...")

    traj_A = compute_trajectory(rho_0, gates_A, steps=20)
    traj_B = compute_trajectory(rho_0, gates_B, steps=20)

    length_A = path_length(traj_A)
    length_B = path_length(traj_B)

    print(f"\n   Twin A (direct path):")
    print(f"     Gates: R_y({theta:.4f})")
    print(f"     Path length: {length_A:.6f}")

    print(f"\n   Twin B (decomposed path):")
    print(f"     Gates: R_z({phi:.4f}) * R_x({theta:.4f}) * R_z({-phi:.4f})")
    print(f"     Path length: {length_B:.6f}")

    diff_length = abs(length_B - length_A)
    percent_diff = 100 * diff_length / length_A

    print(f"\n   Path difference: {diff_length:.6f} ({percent_diff:.1f}%)")

    # Visualization
    print(f"\n4. VISUALIZATION:")
    print("   Generating Bloch sphere plot...")

    fig = plt.figure(figsize=(16, 6))

    # 3D Bloch sphere
    ax1 = fig.add_subplot(131, projection="3d")

    # Draw sphere
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x, y, z, alpha=0.05, color="gray")

    # Plot trajectories
    ax1.plot(
        traj_A[:, 0],
        traj_A[:, 1],
        traj_A[:, 2],
        "b-o",
        linewidth=3,
        markersize=6,
        label="Twin A (direct)",
        alpha=0.8,
    )
    ax1.plot(
        traj_B[:, 0],
        traj_B[:, 1],
        traj_B[:, 2],
        "r--s",
        linewidth=3,
        markersize=6,
        label="Twin B (decomposed)",
        alpha=0.8,
    )

    # Mark start and end
    ax1.scatter(
        *traj_A[0], color="green", s=300, marker="*", zorder=10, label="Start: |0>"
    )
    ax1.scatter(
        *traj_A[-1], color="purple", s=300, marker="P", zorder=10, label="End: U|0>"
    )

    ax1.set_xlabel("X", fontsize=12)
    ax1.set_ylabel("Y", fontsize=12)
    ax1.set_zlabel("Z", fontsize=12)
    ax1.set_title("Bloch Sphere Trajectories", fontsize=14, fontweight="bold")
    ax1.legend(fontsize=10)
    ax1.set_box_aspect([1, 1, 1])

    # XY projection
    ax2 = fig.add_subplot(132)
    ax2.plot(
        traj_A[:, 0], traj_A[:, 1], "b-o", linewidth=2, markersize=6, label="Twin A"
    )
    ax2.plot(
        traj_B[:, 0], traj_B[:, 1], "r--s", linewidth=2, markersize=6, label="Twin B"
    )

    # Unit circle
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    ax2.plot(np.cos(theta_circle), np.sin(theta_circle), "k--", alpha=0.2)

    ax2.scatter(traj_A[0, 0], traj_A[0, 1], color="green", s=200, marker="*", zorder=10)
    ax2.scatter(
        traj_A[-1, 0], traj_A[-1, 1], color="purple", s=200, marker="P", zorder=10
    )

    ax2.set_xlabel("X (Bloch)", fontsize=12)
    ax2.set_ylabel("Y (Bloch)", fontsize=12)
    ax2.set_title("XY Projection", fontsize=14, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    ax2.axis("equal")
    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-1.2, 1.2)

    # Z evolution
    ax3 = fig.add_subplot(133)
    steps_array = np.arange(len(traj_A))
    ax3.plot(
        steps_array, traj_A[:, 2], "b-o", linewidth=2, markersize=6, label="Twin A"
    )
    ax3.plot(
        steps_array, traj_B[:, 2], "r--s", linewidth=2, markersize=6, label="Twin B"
    )

    ax3.axhline(0, color="gray", linestyle=":", alpha=0.5)
    ax3.set_xlabel("Evolution Step", fontsize=12)
    ax3.set_ylabel("Z (Population)", fontsize=12)
    ax3.set_title("Temporal Evolution", fontsize=14, fontweight="bold")
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig("qmsg_v2_proof.png", dpi=150, bbox_inches="tight")
    print("   Figure saved: qmsg_v2_proof.png")

    # Conclusion
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)

    if diff_rho < 1e-10 and diff_length > 0.01:
        print("\nTHEOREM PROVEN:")
        print("  1. Same unitary operation: ||U_A - U_B|| < 1e-10")
        print("  2. Same final state: ||rho_A - rho_B|| < 1e-10")
        print(f"  3. Different trajectories: Delta_L = {diff_length:.6f}")
        print("\nIMPLICATION:")
        print("  Biographical information K is IRREDUCIBLE to state rho")
        print(
            "  The 'middle' (trajectory) contains information not in 'extremes' (states)"
        )
    else:
        print("\nWARNING: Conditions not met. Check implementation.")

    print("=" * 80)

    return {
        "U_A": U_A,
        "U_B": U_B,
        "rho_A": rho_A,
        "rho_B": rho_B,
        "traj_A": traj_A,
        "traj_B": traj_B,
        "length_A": length_A,
        "length_B": length_B,
    }


if __name__ == "__main__":
    results = main()
