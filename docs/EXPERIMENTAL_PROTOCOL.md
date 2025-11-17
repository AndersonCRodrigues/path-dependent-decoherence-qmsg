# Experimental Protocol: Photonic Implementation

## Overview

This document describes a feasible experimental protocol to test Q-MSG predictions using single-photon polarization qubits.

**Key prediction:** Different gate decompositions realizing the same rotation will exhibit different decoherence rates under controlled noise.

## Required Equipment

### Light Source
- **Spontaneous Parametric Down-Conversion (SPDC)** source
  - Type-I or Type-II BBO crystal
  - Pump: 405 nm laser
  - Output: 810 nm photon pairs (signal + idler)
- **Alternative:** Heralded single-photon source

### Optical Elements
- **Wave plates:**
  - Half-wave plates (HWP): λ/2 @ 810 nm
  - Quarter-wave plates (QWP): λ/4 @ 810 nm
  - Precision: < 1° angular tolerance
  - Retardance accuracy: < λ/100

- **Polarizers:**
  - Glan-Thompson or Glan-Taylor calcite polarizers
  - Extinction ratio: > 10⁵:1

### Noise Source
- **Controlled birefringent medium:**
  - Variable thickness birefringent glass
  - OR: Liquid crystal variable retarder
  - OR: Stress-induced birefringence (tunable)
  - Requirement: Calibrated phase damping

### Detection
- **Avalanche Photodiodes (APDs):**
  - Quantum efficiency: > 50% @ 810 nm
  - Dark count rate: < 100 Hz
  - Timing resolution: < 500 ps
  - Count rate capability: > 1 MHz

- **Coincidence logic:**
  - Time-to-digital converter (TDC)
  - Coincidence window: ~3 ns

### Data Acquisition
- **Computer control:**
  - Motorized rotation stages for wave plates
  - Automated data collection
  - Real-time tomography analysis

## Protocol Steps

### Phase 1: Calibration (1 day)

#### 1.1 Source Characterization
```
Goal: Verify single-photon statistics
Measurements:
  - g²(0) < 0.1 (single-photon regime)
  - Brightness: > 10⁴ pairs/s
  - Spectral width: ~10 nm (interference filters)
```

#### 1.2 Wave Plate Calibration
```
Goal: Verify rotation accuracy
Method:
  1. Set polarizer to H (0°)
  2. Rotate HWP through 360°
  3. Measure transmission vs angle
  4. Fit to Malus' law
  5. Extract systematic errors
Expected: < 0.5° deviation
```

#### 1.3 State Tomography Calibration
```
Goal: Validate density matrix reconstruction
Method:
  1. Prepare known states (H, V, D, A, R, L)
  2. Perform tomography (16 measurements)
  3. Compare reconstructed vs expected
  4. Compute fidelity
Target: F > 0.99
```

### Phase 2: Twin Preparation (3 days)

#### 2.1 Twin A: Direct Rotation

**Configuration:**
```
|H⟩ → HWP(θ/2) → |ψ_A⟩

Where: θ = 60° (π/3 radians)
HWP angle: 30°
```

**Implementation:**
1. Prepare horizontal photon: |H⟩
2. Apply single HWP at 30°
3. Output: |ψ_A⟩ = cos(30°)|H⟩ + sin(30°)|V⟩

**Verification:**
- Perform full tomography
- Measure Bloch vector: r⃗_A
- Expected: [0, 0.866, 0.5] (within 2%)

#### 2.2 Twin B: Decomposed Rotation

**Configuration:**
```
|H⟩ → QWP(45°) → HWP(30°) → QWP(-45°) → |ψ_B⟩

Implements: R_z(π/2) · R_x(π/3) · R_z(-π/2)
```

**Implementation:**
1. Prepare horizontal photon: |H⟩
2. QWP at 45° (creates R_z(π/2))
3. HWP at 30° (creates R_x(π/3))
4. QWP at -45° (creates R_z(-π/2))
5. Output: |ψ_B⟩

**Verification:**
- Perform full tomography
- Measure Bloch vector: r⃗_B
- Compare: ||r⃗_A - r⃗_B|| < 0.01

**Critical check:**
If ||r⃗_A - r⃗_B|| > 0.01, recalibrate wave plates.

### Phase 3: Noise Characterization (2 days)

#### 3.1 Dephasing Implementation

**Method 1: Birefringent Glass**
```
Material: Quartz plate
Thickness: Variable (0-5 mm)
Orientation: Ordinary axis at 45° to H/V

Effect: Pure phase damping
Strength: γ = f(thickness)
```

**Method 2: Liquid Crystal**
```
Device: Variable retarder (Meadowlark, Thorlabs)
Control: Voltage-tunable
Range: 0-2π retardance

Advantage: Precise electronic control
```

**Calibration:**
1. Prepare |D⟩ = (|H⟩ + |V⟩)/√2
2. Pass through noise source
3. Measure purity: Tr(ρ²)
4. Map noise strength vs control parameter
5. Fit: γ(V) = a·V + b

#### 3.2 Noise Model Validation
```
Test: Apply calibrated noise to |+i⟩, |-i⟩, |R⟩, |L⟩
Measure: Purity decay
Verify: Consistent with phase damping model
```

### Phase 4: Main Experiment (5 days)

#### 4.1 Data Collection Protocol

**For each twin (A and B):**

1. **Prepare initial state:**
   - Heralding: Detect idler photon → signal photon ready
   - Initial polarization: |H⟩

2. **Apply twin transformation:**
   - Twin A: Single HWP
   - Twin B: QWP-HWP-QWP sequence

3. **Verify equivalence (10⁴ counts):**
   - Perform tomography on both
   - Confirm ||ρ_A - ρ_B|| < 0.01

4. **Apply calibrated noise:**
   - Range: γ ∈ [0, 0.3] (7 values)
   - For each γ:
     - Twin A: Measure purity decay
     - Twin B: Measure purity decay
     - Repeat 5 times

5. **Data per point:**
   - Tomography: 16 measurements × 10⁴ counts = 1.6×10⁵ photons
   - Time per point: ~30 minutes
   - Total points: 7 γ values × 2 twins × 5 reps = 70 points
   - Total time: ~35 hours

#### 4.2 Expected Results

**Hypothesis:**
```
Purity decay model: P(γ) = Tr(ρ_γ²)

Twin A: P_A(γ) = 1 - c·γ·L_A
Twin B: P_B(γ) = 1 - c·γ·L_B

Where: L_A < L_B (different path lengths)
```

**Prediction:**
```
For same γ:
P_B < P_A (Twin B loses purity faster)

Quantitative:
ΔP = |P_A - P_B| ≈ c·γ·(L_B - L_A)
                  ≈ c·γ·0.27·L_A
```

**Example numbers:**
```
At γ = 0.15:
P_A ≈ 0.87  (13% purity loss)
P_B ≈ 0.82  (18% purity loss)
ΔP ≈ 0.05   (5% differential - detectable!)
```

### Phase 5: Data Analysis (2 days)

#### 5.1 Tomography Reconstruction
```python
# For each dataset
rho = reconstruct_density_matrix(counts)
purity = np.trace(rho @ rho)
fidelity = compute_fidelity(rho, rho_ideal)
```

#### 5.2 Statistical Analysis
```python
# Bootstrap analysis
bootstrap_results = []
for i in range(1000):
    sample = resample(measurements)
    rho_sample = reconstruct(sample)
    purity_sample = np.trace(rho_sample @ rho_sample)
    bootstrap_results.append(purity_sample)

# Confidence intervals
ci_95 = np.percentile(bootstrap_results, [2.5, 97.5])
```

#### 5.3 Hypothesis Test
```
H0: P_A = P_B (no biographical effect)
H1: P_A > P_B (biographical effect exists)

Test statistic: t = (P_A - P_B) / SE
Critical value: t > 2.5 (95% confidence)
```

## Error Budget

| Error Source | Magnitude | Impact on ΔP |
|--------------|-----------|--------------|
| Wave plate angle | ±0.5° | ±0.001 |
| Retardance error | ±λ/100 | ±0.002 |
| Detection efficiency | ±2% | ±0.001 |
| Tomography fitting | ±0.01 | ±0.005 |
| Shot noise (10⁴ counts) | ±0.005 | ±0.005 |
| **Total systematic** | | **±0.008** |

**Signal-to-noise ratio:**
```
ΔP_predicted = 0.05
σ_total = 0.008
SNR = 0.05 / 0.008 ≈ 6

Detection threshold: 3σ = 0.024
Conclusion: Effect is DETECTABLE
```

## Alternative Platforms

### Ion Trap Implementation
```
Platform: Trapped ⁴⁰Ca⁺ or ¹⁷¹Yb⁺
Qubit: Hyperfine or Zeeman levels
Gates: Laser pulses (Raman or microwave)
Noise: Motional heating, laser phase noise
Advantage: Higher fidelity, longer coherence
Challenge: More complex setup
```

### Superconducting Qubits
```
Platform: Transmon qubits
Gates: Microwave pulses (single-qubit rotations)
Noise: Dephasing from 1/f flux noise
Advantage: Fast operations, multi-qubit capability
Challenge: Low T₂ times (~10-100 μs)
```

## Timeline Summary

| Phase | Duration | Personnel |
|-------|----------|-----------|
| Setup & Calibration | 1 week | 2 people |
| Twin verification | 3 days | 2 people |
| Noise characterization | 2 days | 1 person |
| Main data collection | 5 days | 2 people |
| Analysis | 2 days | 1 person |
| **Total** | **~3 weeks** | **2-3 people** |

## Budget Estimate

| Item | Cost (USD) |
|------|------------|
| SPDC source (if not available) | $5,000 - $15,000 |
| Wave plates (precision) | $2,000 - $5,000 |
| APDs (if not available) | $10,000 - $20,000 |
| Liquid crystal retarder | $3,000 - $5,000 |
| Optical table & mounts | $5,000 - $10,000 |
| Data acquisition | $2,000 - $5,000 |
| **Total (new setup)** | **$27,000 - $60,000** |

**If using existing quantum optics lab:** $5,000 - $10,000 (wave plates + retarder)

## Key Success Criteria

1. **State equivalence verified:** ||ρ_A - ρ_B|| < 0.01
2. **Differential purity loss detected:** ΔP > 3σ
3. **Linear relationship:** ΔP ∝ γ (R² > 0.95)
4. **Reproducibility:** 5 independent runs agree within 2σ

## References

- Nielsen & Chuang, "Quantum Computation and Quantum Information" (2010)
- James et al., "Measurement of qubits," Phys. Rev. A 64, 052312 (2001)
- Altepeter et al., "Photonic state tomography," Adv. At. Mol. Opt. Phys. 52, 105 (2005)