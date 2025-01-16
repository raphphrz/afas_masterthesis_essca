# Robo-Advisors vs. Traditional Advisors: Performance Analysis

## Overview
This research project investigates the comparative effectiveness of robo-advisory services against traditional financial advisory models, focusing on long-term risk management and portfolio performance. The study employs quantitative methods to analyze portfolio data from 2019-2023, examining cost efficiency, performance metrics, and behavioral patterns.

## Research Objectives
The study tests three main hypotheses:
1. Cost reduction through robo-advisory services
2. Performance comparison of hybrid advisory models
3. Impact on behavioral biases in investment decisions

## Data Sources
- Morningstar Direct database (portfolio performance)
- SEC Form ADV filings (cost structures)
- Bloomberg Terminal (market environment data)
- Platform fee disclosures and transaction records

## Technical Implementation

### Requirements
```python
# Core data analysis
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# Financial analysis
pypfopt>=1.5.0
empyrical>=0.5.0
arch>=4.19.0

# Data visualization
matplotlib>=3.4.0
seaborn>=0.11.0
plotly>=5.3.0

# Statistical modeling
statsmodels>=0.13.0
scikit-learn>=0.24.0
```

### Project Structure


## Analysis Framework

### Quantitative Analysis
- Time series analysis of returns
- Risk-adjusted performance metrics
- Fama-French five-factor model implementation
- GARCH modeling for volatility assessment

### Statistical Methods
- Panel regression analysis
- Bootstrap simulations
- Difference-in-differences analysis
- Cross-validation procedures


## Results
Analysis outputs and visualizations are stored in the `results/` directory. Key findings include:
- Cost efficiency comparisons
- Performance metrics across advisory models
- Behavioral pattern analysis

## Documentation
Detailed documentation is available in the `docs/` directory:
- Methodology overview
- Data dictionary
- Analysis procedures
- Technical implementation details

## Contributing
We welcome contributions to improve the analysis. Please read `CONTRIBUTING.md` for guidelines.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Citation
If you use this code or methodology in your research, please cite:
```
@article{zenou2024robo,
  title={Robo-advisors vs. Traditional advisors: A comparative Study of long-term Risk Management and Portfolio Performance},
  author={Zenou-Poehr, Raphaël},
  year={2024}
}
```

## Contact
Raphaël Zenou-Poehr - [email protected]

