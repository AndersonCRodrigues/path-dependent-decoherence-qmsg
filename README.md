# Path-Dependent Decoherence in Open Quantum Systems

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20896384.svg)](https://doi.org/10.5281/zenodo.20896384)

> *"Whoever seeks the answer loses the question; whoever guards the enigma finds both."*

This repository contains the complete scientific validation for
**path-dependent decoherence in open quantum systems** — the phenomenon,
termed here *biographical irreducibility*, whereby a quantum system's
dynamical trajectory $K$ has operational consequences not captured by
its instantaneous state $\rho$.

We construct and validate via simulation that two quantum processes
("twins") with identical unitaries ($U_A = U_B$) and identical final
states ($\rho_A = \rho_B$) diverge measurably under decoherence
($\rho'_A \neq \rho'_B$) when their trajectories differ ($K_A \neq K_B$)
and environmental coupling depends on dynamical activity
($\gamma \propto W_{\mathrm{bio}}$).

> **Scope note:** The decoherence model $\gamma = \alpha \cdot W_{\mathrm{bio}}$
> is phenomenological. A companion paper (Q-MSG framework, in preparation)
> provides a microscopic derivation via Nakajima-Zwanzig formalism, showing
> that $\gamma \approx \alpha_{\mathrm{eff}} \cdot W_{\mathrm{bio}}$ emerges
> as a leading-order approximation in the weak-coupling regime. The results
> here demonstrate internal consistency and motivate experimental tests.

---

## The Paper

The complete manuscript, including all 6 validation tests (v2.0–v3.5),
statistical analysis, and experimental protocol:

[**View the Full Paper (PDF)**](paper/Biographical_Irreducibility_in_Quantum_Mechanics.pdf)

---

## Key Numerical Results

All values are reproducible by running the scripts below (fixed seed = 2025).

| Quantity | Value |
|---|---|
| $W_A$ (Twin A path length) | 1.047 |
| $W_B$ (Twin B path length) | 2.375 |
| $\Delta W / W_A$ | 126.8% |
| $\gamma_A = \alpha \cdot W_A$ ($\alpha = 0.15$) | 0.157 |
| $\gamma_B = \alpha \cdot W_B$ ($\alpha = 0.15$) | 0.356 |
| $\|\rho'_A - \rho'_B\|_F$ | 0.244 |
| Purity difference $\Delta P$ | 14.5% |
| Bootstrap 95% CI | [0.216, 0.272] |
| $z$-score (vs. null distribution) | 21.1$\sigma$ |
| $p$-value | $< 10^{-6}$ |

---

## Reproducing All Results

```bash
# 1. Clone
git clone https://github.com/AndersonCRodrigues/path-dependent-decoherence-qmsg.git
cd path-dependent-decoherence-qmsg

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run all tests (~30 seconds)
python code/qmsg_complete.py
```

All figures are saved to `/figures`. Console output can be compared
against `code/run_final.log`.

> **Reproducibility:** `qmsg_v3_4_statistics.py` and
> `qmsg_v3_5_correlations.py` use `np.random.seed(2025)`.
> All other scripts are deterministic.

---

## Repository Structure

```
/paper      Final PDF manuscript
/code       Python scripts and run_final.log
  qmsg_complete.py          Master runner (all 6 tests)
  qmsg_v2_proof.py          Mathematical proof (K ≠ ρ)
  qmsg_v3_1_time_normalized.py  Time-normalization test
  qmsg_v3_2_noise.py        Physical noise models
  qmsg_v3_3_multiqubit.py   Multi-qubit scaling
  qmsg_v3_4_statistics.py   Bootstrap statistics (seed=2025)
  qmsg_v3_5_correlations.py Initial-state robustness (seed=2025)
/figures    Generated figures
/docs
  Q-MSG_FROM_PHILOSOPHY_TO_PROOF.md
  EXPERIMENTAL_PROTOCOL.md
  USAGE.md
```

---

## Validation Summary

| Test | Result | Status |
|---|---|---|
| Operational equivalence $\|U_A - U_B\|$ | $2.0 \times 10^{-16}$ | ✓ |
| State equivalence $\|\rho_A - \rho_B\|$ | $2.7 \times 10^{-16}$ | ✓ |
| Time-normalization ($\gamma \propto T$) | $1.6 \times 10^{-16}$ (no divergence) | ✓ |
| Time-normalization ($\gamma \propto W$) | 0.244 (divergence confirmed) | ✓ |
| Physical noise models (4 types) | All detectable | ✓ |
| Multi-qubit scaling (2-qubit) | 0.200 | ✓ |
| Bootstrap $p$-value | $< 10^{-6}$ | ✓ |
| Initial-state robustness (106 tests) | 106/106 detectable | ✓ |

---

## Citation

```bibtex
@article{rodrigues2025biographical,
  title   = {Path-Dependent Decoherence in Open Quantum Systems:
             Operational Signatures Beyond Instantaneous State Descriptions},
  author  = {Rodrigues, Anderson Costa},
  year    = {2025},
  doi     = {10.5281/zenodo.20896384},
  url     = {https://zenodo.org/records/20896384},
  note    = {Zenodo preprint. Code: https://github.com/AndersonCRodrigues/path-dependent-decoherence-qmsg}
}
```

---

## License

MIT — see `LICENSE`.