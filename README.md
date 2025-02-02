# Empirical Analysis of Software Maintainability Metrics in DevOps Environments

This repository contains scripts used for extracting and analyzing software maintainability metrics in DevOps environments. The scripts facilitate data collection from GitHub repositories and analyze key metrics such as pull request activity, code deployment frequency, code churn rate, and code complexity.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Fetching Pull Request Data](#fetching-pull-request-data)
  - [Analyzing Code Deployment Frequency](#analyzing-code-deployment-frequency)
  - [Calculating Code Churn Rate](#calculating-code-churn-rate)
  - [Measuring Code Complexity](#measuring-code-complexity)
- [Dependencies](#dependencies)
- [Results and Outputs](#results-and-outputs)
- [License](#license)

## Introduction
This project is part of a research paper focusing on empirical analysis of software maintainability metrics in DevOps environments. The scripts automate data extraction and analysis to understand software evolution patterns.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Install required Python libraries:
   ```sh
   pip install requests pandas scipy lizard openpyxl
   ```

## Usage
### Fetching Pull Request Data
This script retrieves pull request (PR) information from a specified GitHub repository.
```sh
python request_test.py
```
Outputs PR titles and creation dates.

### Analyzing Code Deployment Frequency
This script fetches and analyzes release data from GitHub to determine deployment frequency.
```sh
python code_deployment_frequency.py
```
Outputs deployment frequency metrics in an Excel file.

### Calculating Code Churn Rate
This script computes code churn statistics such as commits, file changes, lines added, and lines deleted.
```sh
python code_churn_rate.py
```
Outputs statistics and calculates Pearson correlation between function count and commits.

### Measuring Code Complexity
This script analyzes the complexity of code releases using Lizard, extracting metrics like cyclomatic complexity and function count.
```sh
python code_complexity.py
```
Outputs results in an Excel file.

## Dependencies
- Python 3.7+
- `requests` for API requests
- `pandas` for data processing
- `scipy` for statistical analysis
- `lizard` for code complexity analysis
- `openpyxl` for Excel file handling

## Results and Outputs
Each script generates reports in CSV/Excel formats summarizing the extracted data and analysis. These results are valuable for understanding trends in software maintainability.

## License
This project is licensed under the MIT License.

---

### Notes:
- Ensure you replace the GitHub token (`token = 'ghp_XXXXXXXXXX'`) with your own secure access token.
- Do not share your token publicly.
- Modify repository paths in `code_churn_rate.py` and `code_complexity.py` as per your local setup.

For any questions or contributions, feel free to open an issue or submit a pull request!

