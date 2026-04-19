# Simulating Health Gains from Achieving Optimal Blood Pressure Control

> A rapid review of simulation models and a proportional multistate lifetable analysis estimating population health gains under three systolic blood pressure control targets in Nepal.

[![OSF Registration](https://img.shields.io/badge/OSF-Preregistered-blue)](https://osf.io/4wyqp)
[![Python](https://img.shields.io/badge/Python-3.9.5-green)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

This repository contains the data, model code, and results for:

**Mishra SR, Bam K, Acharya B, Acharya K, Bhandari B, Satheesh G, Schutte A.**  
*Simulating health gains from achieving optimal blood pressure control in Nepal: A rapid review and life-table analysis.*  
Preregistration: [https://osf.io/4wyqp](https://osf.io/4wyqp)

The study has two components:

1. **Rapid review** — a scoping review of 39 published simulation models estimating population health gains from blood pressure (BP) interventions, mapping model types, parameterisation approaches, outcomes reported, and gaps in the evidence base.

2. **Lifetable modelling** — a proportional multistate lifetable (PMSLT) model estimating health-adjusted life years (HALYs) gained from achieving optimal BP control in the adult Nepalese population in 2023, under three progressively intensive systolic BP (SBP) control targets compared with a business-as-usual (BAU) scenario.

---

## Key Findings

### Rapid review (n = 39 studies)
- Markov state-transition models were the most common approach (30.8%), followed by microsimulation (28.2%)
- Most studies focused on cardiovascular outcomes, QALYs, and cost-effectiveness
- Only a minority incorporated socioeconomic inequalities (10.3%) or were conducted in low- and middle-income settings
- Urban–rural stratification was absent from all included studies

### Nepal lifetable model — primary scenario (SBP < 140 mmHg)

| Outcome | 20-year (2023–2043) | Lifetime |
|---|---|---|
| Total HALYs gained (undiscounted) | 1.4 million (95% UI: 0.9–2.0M) | 27.8 million (95% UI: 19.0–39.9M) |
| HALYs per 1,000 population (undiscounted) | 51.0 (95% UI: 35.3–72.5) | 1,005.8 (95% UI: 687.9–1,437.0) |
| Total HALYs gained (3% discount) | 1.0 million (95% UI: 0.6–1.3M) | 6.8 million (95% UI: 4.5–9.6M) |
| HALYs per 1,000 population (3% discount) | 33.7 (95% UI: 23.2–47.8) | 245.0 (95% UI: 169.8–346.5) |

**Sex-stratified gains (undiscounted, per 1,000 population, 20-year horizon):**
- Males: 61.1 HALYs (95% UI: 42.0–85.8)
- Females: 41.8 HALYs (95% UI: 28.5–59.4)

### Sensitivity analyses — more intensive BP targets

| Scenario | 20-year HALYs (undiscounted, millions) | Lifetime HALYs (undiscounted, millions) |
|---|---|---|
| SBP < 140 mmHg (standard control) | 1.4 (0.9–2.0) | 27.8 (19.0–39.9) |
| SBP < 130 mmHg (intensive control) | 1.9 (1.3–2.7) | 38.5 (26.6–54.7) |
| SBP < 120 mmHg (very intensive control) | 2.4 (1.8–3.4) | 50.1 (35.3–70.2) |

---

## Model Description

### Proportional Multistate Lifetable (PMSLT)

The PMSLT is a macro-simulation model that simultaneously simulates sex-stratified cohorts of the Nepalese population forward in time from 2023, tracking disease incidence, mortality, and HALYs under counterfactual policy scenarios. It is implemented in Python 3.9.5 and run with 2,000 Monte Carlo iterations to propagate uncertainty across all input parameters.

**Five BP-associated diseases are modelled simultaneously:**
- Ischaemic heart disease
- Stroke
- Hypertensive heart disease
- Chronic kidney disease
- Atrial fibrillation and flutter

### Intervention Scenarios

Three counterfactual SBP control targets are modelled, each compared against BAU:

| Scenario | Target | Population eligible |
|---|---|---|
| Standard control | SBP < 140 mmHg | Individuals with SBP ≥ 140 mmHg |
| Intensive control | SBP < 130 mmHg | Individuals with SBP ≥ 130 mmHg |
| Very intensive control | SBP < 120 mmHg | Individuals with SBP ≥ 120 mmHg |

### Population Impact Fractions (PIFs)

The study uses the relative risk (RR) shift method to calculate PIFs linking BP intervention to disease incidence. The generic formula is:

$$\text{PIF}_{itd} = \frac{\sum_{i=1}^{n} P_i RR_{id} - \sum_{i=1}^{n} P'_i RR_{id}}{\sum_{i=1}^{n} P_i RR_{id}}$$

Where:
- `i` — age × sex stratum
- `d` — disease
- `t` — yearly time step
- `P_i` — proportion of the population in each SBP category under BAU
- `P'_i` — counterfactual SBP proportion after the intervention shift
- `RR` — disease-specific incidence rate ratio for each SBP level (from GBD 2023)

PIFs are assumed constant across time steps (BAU SBP distribution is held fixed). A lag time of 3 years (log-normal distribution, ±20%) is applied to all CVD outcomes.

### Key Model Parameters

| Parameter | Source |
|---|---|
| SBP distributions by age and sex | Nepal Demographic and Health Survey (NDHS) 2022 |
| All-cause mortality and morbidity rates | GBD 2023 (ghdx.healthdata.org) |
| Disease-specific incidence, prevalence, case-fatality rates | GBD 2023 |
| SBP–disease relative risks | GBD 2023 |
| Population baseline (2023) | Nepal Statistics Office (NSO) — 29.1 million |
| Discount rates | 0% and 3% per annum |
| Uncertainty (RRs, effect sizes, baseline rates) | Monte Carlo, 2,000 iterations |

Full parameter details and sources are in `data/processed/bau_parameters.csv` and eSupplementary Table 7.

---

## Data Sources

| Dataset | Description | Access |
|---|---|---|
| Nepal DHS 2022 | SBP distributions by age and sex for baseline model inputs | [dhsprogram.com](https://dhsprogram.com) — public |
| GBD 2023 | Disease-specific rates, relative risks, and uncertainty intervals | [ghdx.healthdata.org](http://ghdx.healthdata.org) — public |
| Nepal Statistics Office 2025 | National population estimates by age and sex for 2023 | [cbs.gov.np](https://cbs.gov.np) — public |

> **Note:** SBP data from NDHS 2022 were measured using a standardised three-reading clinical protocol during household survey visits. Population-level model inputs are not affected by the single-occasion measurement limitation.

---

## Reproducing the Analysis

### Requirements

```
Python >= 3.9.5
numpy
pandas
scipy
matplotlib
seaborn
jupyter
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the model

```bash
# Run the primary scenario (SBP <140 mmHg) with 2,000 Monte Carlo iterations
python model/pmslt_nepal.py --scenario standard --iterations 2000 --discount 0.03

# Run all three scenarios
python model/pmslt_nepal.py --scenario all --iterations 2000 --discount 0.03

# Run undiscounted
python model/pmslt_nepal.py --scenario all --iterations 2000 --discount 0.00
```

Or step through the analysis interactively:

```bash
jupyter notebook notebooks/03_pmslt_run.ipynb
```

### Expected runtime

A single scenario with 2,000 Monte Carlo iterations runs in approximately 8–12 minutes on a standard laptop (16 GB RAM, 8-core CPU). All three scenarios together take approximately 25–35 minutes.

---

## Reporting Standards

- **Rapid review:** PRISMA extension for Scoping Reviews (PRISMA-ScR)
- **Simulation reporting:** GATHER checklist (Stevens et al., *The Lancet*, 2016)
- **Preregistration:** Open Science Framework — [https://osf.io/4wyqp](https://osf.io/4wyqp)

---

## Limitations

1. SBP inputs were measured on a single household visit rather than across repeated clinical encounters; this is unlikely to substantially bias population-level model inputs.
2. The model does not incorporate new births or migration; excluding births has minimal impact on 20-year HALY estimates given that BP-related burden concentrates in middle and older age groups.
3. The BAU scenario assumes a fixed SBP distribution; given Nepal's rapid epidemiological transition, HALY gains may be underestimated if the unintervened population becomes more hypertensive over time.
4. Mental health gains associated with BP reduction are not captured, as these are absent from GBD-derived outcome estimates.
5. Health gains are not stratified by socioeconomic status; pronounced SES gradients in hypertension awareness and treatment in Nepal mean equity-disaggregated estimates are an important priority for future work.

---

## Citation

If you use this code or data, please cite:

```bibtex
@article{mishra2025nepal_bp_simulation,
  title   = {Simulating health gains from achieving optimal blood pressure control
             in Nepal: A rapid review and life-table analysis},
  author  = {Mishra, Shiva Raj and Bam, Kiran and Acharya, Baburam and
             Acharya, Kiran and Bhandari, Buna and Satheesh, Gautam and
             Schutte, Aletta},
  journal = {[Journal name]},
  year    = {2025},
  note    = {OSF preregistration: https://osf.io/4wyqp}
}
```

---

## Related Work

This model extends the PMSLT framework previously applied by the team to:
- Cold housing eradication in Australia (Mishra et al., *Social Science & Medicine*, 2023)
- Optimal BMI in Australia (Bohora, Mishra et al., *Lancet Regional Health — Western Pacific*, 2024)

It is also directly related to the global hypertension capacity analysis:
- Mishra et al. Bridging hypertension care shortfalls between provider capacity and patient needs: a pooled analysis from 199 countries. *Hypertension*, 2025.

---

## Authors and Affiliations

| Author | Affiliation |
|---|---|
| Shiva Raj Mishra (corresponding) | School of Medicine, Western Sydney University; Nepal Development Society |
| Kiran Bam | Nepal Development Society; La Trobe University |
| Baburam Acharya | Nepal Development Society |
| Kiran Acharya | New ERA, Kathmandu |
| Buna Bhandari | Indiana University South Bend |
| Gautam Satheesh | University of Sydney |
| Aletta Schutte | The George Institute for Global Health; UNSW Sydney |

**Correspondence:** Dr Shiva Raj Mishra — Liverpool School of Medicine, Western Sydney University

---

## Funding and Conflicts of Interest

- **Funding:** None declared
- **Conflicts of interest:** None declared

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details. Model code and processed data are freely available for reuse and adaptation with attribution.
