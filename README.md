

# Public Repository Overview

This repository hosts data and analyses for various evaluations and tests concerning security software and rule evaluation frameworks. Below, you will find a detailed description of each folder's contents and their respective roles in the overall project.

## Folder Descriptions

### RQ1 - Property Generation(Certora-based Evaluation Process)
**Contents:** This folder contains data and analyses pertaining to the original evaluation process using Certora rules. It focuses on the selection of 9 random projects, chosen based on the availability of sufficient specifications. The folder includes detailed breakdowns of the project selections and links to associated data files, offering specific counts of items like specifications for each evaluated project. A Markdown file within the folder provides further explanations of the Excel data.

### RQ2 - Vulnerability Detection(Comparative Evaluations and Settings)
- **cve**: This subfolder details the collection and evaluation process of CVEs, including comparisons with results from `gptscan`.
- **smartInv**: Contains comparisons of results between `smartInv` from RQ1 and detailed data collection and result generation information. A Markdown file within the folder provides explanations of the Excel data.
- **top k setting**: Shows precision and recall at various 'top k' settings in the experiments from RQ1. A Markdown file within the folder provides explanations of the Excel data.

### RQ3 - Abliation Study
**Contents:** This folder documents the success rates and timings generated during experiments. A Markdown file within the folder provides explanations of the Excel data.

### RQ4 - Real-world Application(Zero-Day Vulnerability Mining)
**Contents:** Contains analyses and data on zero-day vulnerability mining, detailing specific analytical processes. A Markdown file within the folder provides explanations of the Excel data.

### rule_classification
**Contents:** This folder showcases the classification of collected Certora rules, including classification codes and the classification process. Results of the classification are also included.

### spec_extractor
**Contents:** Details the methodology and data related to extracting rule information from original reports.

### weight_calcu
**Contents:** Includes extensive experimental data and methodologies for evaluating weights based on this data.

---

**Note**: Each folder equipped with Excel files also contains a corresponding Markdown file to assist in understanding the intricate details and methodologies applied within the data files.

--- 
