# SpecXtract - Specification Parser for DOCX Files

![specxtract_logo](https://github.com/psibir/specxtract/blob/main/specxtract_logo.png?raw=true)

The `specxtract` program is a utility designed to extract product specifications, features, and related information from DOCX files. It uses regular expressions to identify specific patterns in the text and extracts relevant data.

## Usage

To use the `specxtract` utility, you can run it from the command line with the following syntax:

```bash
python specxtract.py docx_path -o OUTPUT_CSV [-h]
```

- `docx_path`: Path to the DOCX file or directory containing DOCX files for parsing.
- `-o OUTPUT_CSV`: Path of the output CSV file to store extracted data.

## Features

- Extracts product feature categories and their related information from DOCX files.
- Extracts data based on predefined feature patterns using regular expressions.
- Handles both email addresses and phone numbers separately, capturing the entire address/number.
- Outputs the extracted data in a CSV file if specified using the `-o` flag.

## Business Use Case

Imagine you are part of a market research team tasked with gathering information from product specification documents in DOCX format. These documents contain a variety of structured information, including email addresses, phone numbers, and key product features. Manually extracting this information from multiple documents can be time-consuming and error-prone.

SpecXtract comes to the rescue in this scenario. By using this utility, you can automate the extraction of key product features, contact details, and other relevant information from the documents. The utility's extensible pattern matching allows you to tailor the extraction to your specific needs. After processing the documents, you will have a consolidated CSV report that can be easily analyzed and integrated into your market research process.

### Example: XYZ Electronics

#### Situation: Extracting Product Feature Categories

XYZ Electronics, a company that manufactures and sells electronic gadgets, often receives product specification documents from their suppliers in DOCX format. These documents contain information about the features, specifications, and contact details of various products.

XYZ Electronics uses the `specxtract` utility to automatically extract and categorize product feature information from these documents. This helps their team quickly analyze and compare different products based on features, specifications, and contact details.

**Workflow:**

1. The `specxtract` utility is executed with the path to the directory containing the DOCX files received from suppliers.

2. The utility processes each DOCX file in the directory using the `DocumentParser` class and the predefined `FeatureExtractor` class.

3. It extracts relevant product feature categories and related information using regular expression patterns defined in `FEATURE_PATTERNS`.

4. The extracted data is organized and saved into a CSV file, which XYZ Electronics' team can then review and analyze.

**Benefits:**

- Automation: The utility automates the process of extracting product feature information, saving time and effort for XYZ Electronics' team.
- Data Organization: The extracted data is neatly organized into feature categories and values, making it easier to compare products.
- Efficient Analysis: By having the data in CSV format, the team can quickly analyze and make decisions regarding product procurement.

The `specxtract` utility streamlines the extraction of product feature categories from supplier documents, enhancing XYZ Electronics' efficiency in product evaluation and decision-making.

Sure, here's the section you can add to your `README` to explain how to run tests using the `specxtract` program:

## Testing

To run tests for the `specxtract` program, you can use the following command:

```bash
python3 specxtract.py ../tests/input.docx -o ../tests/output.csv
```

Here's what this command does:

- `python3 specxtract.py`: This command runs the `specxtract` program using Python 3.

- `../tests/input.docx`: This is the path to the input DOCX file that you want to parse. Make sure to replace `../tests/input.docx` with the actual path to your test input file.

- `-o ../tests/output.csv`: This specifies the output CSV file where the extracted data will be saved. Replace `../tests/output.csv` with the desired path for your output CSV file.

Running this command will execute the `specxtract` program on the specified input DOCX file, extract the data based on the predefined feature patterns, and save the extracted data in the specified output CSV file. You can then review the output CSV file to verify if the program is working correctly for your test case.

Make sure that you have the necessary dependencies and the `specxtract.py` file in the correct directory before running the tests. If needed, you might also want to provide additional input files and adjust the paths accordingly.
