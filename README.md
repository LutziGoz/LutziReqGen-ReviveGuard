# LutziReqGen-ReviveGuard

### LutziReqGen is a Python tool designed to create precise requirements_filtered.txt files for specific projects by analyzing the imports in your main Python script. This reduces unnecessary dependencies, optimizing deployment and container sizes. Additionally, it includes ReviveGuard to protect against "Revival Hijack" attacks by ensuring only verified and required packages are used, safeguarding your project from malicious dependency reinjection.

## Key Features
1. Enhanced Security: Protects against Revival Hijack by validating and filtering only required packages.
2. Optimized Dependencies: Reduces the size of exported files, containers, or deployment packages, improving performance.
3. Streamlined Installations: Generates a refined requirements.txt tailored to your project's actual dependencie

## How It Works

### Step-by-Step Guide

1. **Generate Full Requirements**:

   Use `pip freeze > requirements.txt` to create a complete list of all installed packages in your Python environment.

2. **Select Main Project File**:

   The user selects the primary Python file (`main.py`) for the project. The script will analyze this file for all imported packages.

3. **Load Full Requirements**:

   Load the previously generated `requirements.txt` into the tool.

4. **Compare and Filter**:

   The script compares the imports from the main project file with the full list of installed packages.

   It then generates a new `requirements_filtered.txt`, including only the necessary packages.

5. **Generate Report and Review**:

   A report is generated, highlighting unmatched imports or discrepancies, allowing for manual review.

6. **Secure Installation**:

   The user is prompted to install the refined dependencies using the command:

   ```bash
   pip install -r requirements_filtered.txt

### Visual Explanation

## Dependency Management Workflow


| **Step** | **Action**                           | **Output**                                        |
|----------|--------------------------------------|---------------------------------------------------|
| 1        | Generate full requirements           | `requirements.txt` with all installed packages    |
| 2        | Select main project file             | Identifies actual imports used                    |
| 3        | Load pre-generated requirements      | Compares with actual imports                      |
| 4        | Filter and generate new requirements | `requirements_filtered.txt` with used packages    |
| 5        | Generate report                      | Log file with unmatched imports for review        |
| 6        | Install filtered requirements        | Secure and optimized environment                  |



## Security and Optimization Benefits
* Security: Prevents the installation of re-registered or deprecated packages that could be compromised.
* Efficiency: Streamlined requirements.txt results in faster installations, reduced bloat, and smaller project footprints.

### Usage Example
* Generate the full list of packages:
""pip freeze > requirements.txt""
* Run the script with administrator privileges:
""python LutziRequirementsGenerator.py""
Follow the on-screen instructions to select the main project file and load requirements.txt.
Review the filtered requirements and install them securely.
Conclusion
LutziReqGen & ReviveGuard provide a dual advantage of security and optimization. Whether you're deploying a lightweight container, securing your project against Revival Hijack, or simply managing dependencies more efficiently, this tool is your go-to solution!


