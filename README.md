# AHP-TOPSIS Decision Support System

A professional GUI application that integrates Analytic Hierarchy Process (AHP) and TOPSIS (Technique for Order Preference by Similarity to Ideal Solutions) for multi-criteria decision analysis.

## Features

- **AHP Module**
  - Define criteria hierarchy
  - Perform pairwise comparisons
  - Calculate priority weights
  - Check consistency ratio
  - Visualize results

- **TOPSIS Module**
  - Import performance data
  - Apply AHP weights
  - Calculate rankings
  - Export results

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ahp-topsis-dss
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

3. TOPSIS Analysis:
   - Import performance data (CSV format)
   - Apply AHP weights
   - View rankings
   - Export results

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
- PyQt6
- NumPy
- Pandas
- Matplotlib
- Seaborn

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 