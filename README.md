# AHP-TOPSIS Decision Support System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)

A professional GUI application that integrates Analytic Hierarchy Process (AHP) and TOPSIS (Technique for Order Preference by Similarity to Ideal Solutions) for multi-criteria decision analysis. This tool helps decision-makers evaluate alternatives based on multiple criteria using a systematic and mathematical approach.

## Features

- **AHP Module**
  - Define criteria hierarchy
  - Perform pairwise comparisons
  - Calculate priority weights
  - Check consistency ratio
  - Visualize results
  - Export comparison matrices

- **TOPSIS Module**
  - Import performance data
  - Apply AHP weights
  - Calculate rankings
  - Export results
  - Visualize rankings
  - Support for both benefit and cost criteria

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OzdemirTarik/ahp-topsis.git
cd ahp-topsis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. AHP Analysis:
   - Set the number of criteria
   - Enter criteria names
   - Fill in the pairwise comparison matrix
   - View weights and consistency ratio
   - Export results if needed

3. TOPSIS Analysis:
   - Import performance data (CSV format)
   - Apply AHP weights
   - View rankings
   - Export results
   - Visualize the results

## Input Format

### Performance Matrix CSV Format
The CSV file should have:
- First column: Alternative names
- Remaining columns: Criteria values
- No header row required

Example:
```
Alt1,10,5,8
Alt2,8,7,6
Alt3,9,6,7
```

## Dependencies

- Python 3.10+
- PyQt6 >= 6.4.0
- NumPy >= 1.21.0
- Pandas >= 1.3.0
- Matplotlib >= 3.4.0
- Seaborn >= 0.11.0
- openpyxl >= 3.0.0

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite it as:

```
@software{ahp_topsis_dss,
  author = {Tarik Sahin Ozdemir},
  title = {AHP-TOPSIS Decision Support System},
  year = {2024},
  url = {https://github.com/OzdemirTarik/ahp-topsis}
}
```

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for their invaluable tools and libraries 
