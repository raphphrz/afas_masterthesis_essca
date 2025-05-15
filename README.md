# Robo-Advisors vs. Traditional Advisors: A Comparative Study of Risk Management and Portfolio Performance

## Overview

This research project investigates whether robo-advisory platforms can offer cost-efficient, consistent, and risk-adjusted portfolio outcomes that match or surpass traditional financial advisors. The analysis is conducted in two empirical phases:

- Phase 1: Comparative analysis of advisory fee structures and tax efficiency.
- Phase 2: Risk-adjusted performance analysis over 1, 3, and 7-year horizons.

The study is based on a reproducible Python pipeline. All code, data, and outputs are fully documented and traceable.

## Research Objectives

This study tests the following hypotheses:

- H1: Robo-advisors reduce portfolio management costs.
- H2: Robo-advisors offer superior or comparable portfolio performance on a risk-adjusted basis.
- H3: Robo-advisors reduce investors’ behavioral biases (not tested due to lack of data).

## Data Sources

- Yahoo Finance — price and performance data
- Bloomberg Terminal — benchmark index returns
- Morningstar — traditional fund category classification
- Condor Capital, Wealthfront, Schwab, Betterment, etc. — platform data
- SEC Form ADV — fee structure disclosures

## Technical Implementation

Python 3.12 was used throughout the project. The code is modular and structured under the directory `performance_analysis/`.

## Output and Reproducibility

All statistical outputs (Welch’s t-test, descriptive statistics) and figures (300 DPI PNGs) are saved in the `results/` directory. Excel files contain structured results for direct inclusion in academic writing.

## Results

Key insights from the analysis include:

- Automated advisors demonstrate significantly lower expense ratios.
- No statistically significant return differences were observed between advisory models.
- 3-year volatility was significantly lower in the automated group, suggesting superior mid-term risk smoothing.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Citation

If you use this code or methodology in your work, please cite:
@article{zenou2025robo,
title={Robo-Advisors vs. Traditional Advisors: A Comparative Study of Risk Management and Portfolio Performance},
author={Zenou-Poehr, Raphaël},
year={2025}
}

