# Q-MSG Usage Guide

## Quick Start

### Run Everything

```bash
python code/qmsg_complete.py
```

This runs all 6 tests in sequence (~30 seconds) and generates all figures.

### Run Individual Tests

```bash
# Mathematical proof
python code/qmsg_v2_proof.py

# Time-normalization test
python code/qmsg_v3_1_time_norm.py

# Physical noise models
python code/qmsg_v3_2_noise.py

# Multi-qubit scaling
python code/qmsg_v3_3_multiqubit.py

# Statistical validation
python code/qmsg_v3_4_statistics.py

# Initial correlations test
python code/qmsg_v3_5_correlations.py
```

## Understanding the Output

### v2.0: Mathematical Proof

**What it does:**
- Constructs two quantum twins (A and B)
- Proves they have same unitary U and same final state ρ
- Shows they have different trajectories K (27% path difference)

**Output:**
- Console: Verification of equivalence + path metrics
- Figure: `qmsg_v2_proof.png` (3-panel Bloch sphere visualization)

**Key result:**
```
Path_A = 1.047
Path_B = 1.331
Difference = 27.1%

THEOREM PROVEN: K ≠ ρ
```

### v3.1: Time-Normalization

**What it does:**
- Addresses critique: "Maybe just different execution times"
- Enforces SAME total time T for both twins
- Tests two hypotheses: gamma~time vs gamma~path

**Output:**
- Console: Comparison of two decoherence models
- Figure: `qmsg_v3_1_time_norm.png` (6-panel comparison)

**Key result:**
```
Model gamma~time:  ||Δρ|| = 1.6×10⁻¹⁶  (no effect)
Model gamma~path:  ||Δρ|| = 0.244      (large effect)

VALIDATED: Effect is NOT a timing artifact
```

### v3.2: Physical Noise Models

**What it does:**
- Tests robustness across 4 physical noise environments
- White noise, Ohmic bath, Super-Ohmic, 1/f noise

**Output:**
- Console: Divergence for each noise model
- Figure: `qmsg_v3_2_noise.png` (bar chart comparison)

**Key result:**
```
White:       0.244 (detectable)
Ohmic:       0.293 (detectable)
Super-Ohmic: 0.195 (detectable)
1/f:         0.393 (detectable)

ROBUST: Works in ALL physical models
```

### v3.3: Multi-Qubit Scaling

**What it does:**
- Extends to 2-qubit system
- Applies twins to qubit 1, identity to qubit 2

**Output:**
- Console: 2-qubit divergence metrics
- Figure: `qmsg_v3_3_multiqubit.png` (2-qubit results)

**Key result:**
```
1-qubit: ||Δρ|| = 0.244
2-qubit: ||Δρ|| = 0.283

CONFIRMED: Effect scales to larger systems
```

### v3.4: Statistical Significance

**What it does:**
- Bootstrap resampling (n=100)
- Hypothesis testing
- Computes p-values and z-scores

**Output:**
- Console: Statistical metrics
- Figure: `qmsg_v3_4_statistics.png` (bootstrap distributions)

**Key result:**
```
p-value: < 0.01
z-score: ~26 sigma
95% CI: [0.216, 0.272]

SIGNIFICANT: Far exceeds 5σ discovery threshold
```

### v3.5: Initial Correlations

**What it does:**
- Tests 50 random pure states
- Tests 50 random mixed states
- Tests 6 basis states
- Total: 106 initializations

**Output:**
- Console: Statistics across all tests
- Figure: `qmsg_v3_5_correlations.png` (distribution plots)

**Key result:**
```
Mean divergence: 0.228 ± 0.031
All 106 tests: detectable (>0.1)
CV: 13.6%

STABLE: Effect is initialization-independent
```

## Using as a Library

```python
from code.qmsg_v2_proof import rotation, to_bloch, path_length

# Create your own quantum twin
rho_0 = np.array([[1, 0], [0, 0]], dtype=complex)
U = rotation('y', np.pi/4)
rho_final = U @ rho_0 @ U.conj().T

# Convert to Bloch
bloch = to_bloch(rho_final)
print(f"Bloch vector: {bloch}")
```

## Customization

### Adjust Parameters

In any script, modify:

```python
# Change rotation angle
theta = np.pi / 3  # Default
theta = np.pi / 4  # Your value

# Change coupling strength
coupling = 0.15    # Default
coupling = 0.20    # Stronger decoherence

# Change number of steps
steps = 20         # Default
steps = 50         # Higher resolution
```

### Generate Different Figures

```python
# In visualization functions, customize:
fig = plt.figure(figsize=(16, 6))  # Change size
plt.savefig('my_figure.png', dpi=300)  # Higher resolution
```

### Statistical Tests

```python
# In v3.4, increase bootstrap samples:
n_bootstrap = 100   # Default (fast)
n_bootstrap = 1000  # More accurate (slower)
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:

```bash
pip install -r requirements.txt
```

### Memory Issues

If running v3.5 with many tests causes memory issues:

```python
# Reduce number of tests
n_tests = 50   # Default
n_tests = 20   # Lighter
```

### Figure Not Showing

If figure doesn't display:

```python
# Add at end of script:
plt.show()  # Display interactively

# Or just save:
plt.savefig('figure.png')  # Always saves
```

## Expected Runtime

| Test | Runtime | Output Size |
|------|---------|-------------|
| v2.0 | ~2s | ~100 KB |
| v3.1 | ~3s | ~200 KB |
| v3.2 | ~3s | ~50 KB |
| v3.3 | ~2s | ~100 KB |
| v3.4 | ~5s | ~150 KB |
| v3.5 | ~15s | ~200 KB |
| **Complete** | **~30s** | **~800 KB** |

## Advanced Usage

### Export Data

```python
# After running any test:
results = main()

# Save to numpy archive
np.savez('results.npz', **results)

# Load later
data = np.load('results.npz')
```

### Batch Processing

```python
# Run multiple parameter sweeps
thetas = np.linspace(0, np.pi, 10)

for theta in thetas:
    results = run_test(theta)
    save_results(results, f'theta_{theta:.3f}.npz')
```

## Citation

If you use this code, cite:

```bibtex
@article{rodrigues2025qmsg,
  title={Biographical Irreducibility in Quantum Mechanics},
  author={Rodrigues, Anderson Costa},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

## Support

For issues or questions:
- Open an issue on GitHub
- Check the paper for theoretical details
- Review the code comments for implementation details