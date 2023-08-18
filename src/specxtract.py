import argparse
import logging
import os
import re
import sys
import csv
import xml.etree.ElementTree as ET
import zipfile
from glob import glob
from collections import defaultdict
from featurepatterns import FEATURE_PATTERNS

# Constants
DOCX_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

class FeatureExtractor:
    def __init__(self):
        self.feature_counts = defaultdict(int)

    def extract_features(self, text, document_id):
        extracted_features = []
        records = re.split(r'\n{3,}', text)
        
        for record_id, record_text in enumerate(records, start=1):
            feature_matches = defaultdict(list)  # Store matches for each pattern
            for line in record_text.split('\n'):
                for pattern_name, (pattern, _) in FEATURE_PATTERNS.items():
                    match = pattern.match(line)
                    if match:
                        if pattern_name in ["Email", "Phone"]:
                            full_match = match.group(0)  # Captures the entire matched content
                            feature_matches[pattern_name].append((document_id, record_id, pattern_name, full_match, ""))
                        elif pattern_name == "UpperCaseWord":
                            uppercase_word = match.group(0)  # Captures the entire uppercase word
                            # Check if the uppercase word is not represented in ColonSeparated, Quantity, or Name patterns
                            colon_pattern = FEATURE_PATTERNS["ColonSeparated"][0]
                            quantity_pattern = FEATURE_PATTERNS["Quantity"][0]
                            name_pattern = FEATURE_PATTERNS["Name"][0]
                            if not (colon_pattern.search(uppercase_word) or quantity_pattern.search(uppercase_word) or name_pattern.search(uppercase_word)):
                                feature_matches[pattern_name].append((document_id, record_id, pattern_name, uppercase_word, ""))
                        else:
                            features = match.group(1).strip() if match.group(1) else ""
                            value_search = re.search(r':\s*(.*)', line)
                            value = value_search.group(1).strip() if value_search else ""
                            feature_matches[pattern_name].append((document_id, record_id, pattern_name, features, value))
                            self.feature_counts[features] += 1

            # Use non-"ColonSeparated" patterns when same content is matched by both "ColonSeparated" and another pattern
            for pattern_name, matches in feature_matches.items():
                if pattern_name != "ColonSeparated":
                    extracted_features.extend(matches)
            if not feature_matches.get("ColonSeparated"):
                for pattern_name, matches in feature_matches.items():
                    extracted_features.extend(matches)

        extracted_features.sort(key=lambda x: (x[1], self.feature_counts[x[3]]), reverse=True)
        return extracted_features

class DocumentParser:
    def __init__(self, docx_path, extractor):
        self.docx_path = docx_path
        self.extractor = extractor

    def parse_document(self, document_id):
        extracted_features = []
        with zipfile.ZipFile(self.docx_path) as zipf:
            filelist = zipf.namelist()

            for fname in filelist:
                if re.match(r'word/(header|document|footer)[0-9]*.xml', fname):
                    text = self.xml2text(zipf.read(fname))
                    extracted_features.extend(self.extractor.extract_features(text, document_id))

        return extracted_features

    def xml2text(self, xml):
        text = ''
        root = ET.fromstring(xml)
        for child in root.iter():
            if child.tag == self.qn('w:t'):
                t_text = child.text
                text += t_text if t_text is not None else ''
            elif child.tag in (self.qn('w:tab'), self.qn('w:cr')):
                text += '\t'
            elif child.tag == self.qn('w:br'):
                text += '\n'
            elif child.tag == self.qn("w:p"):
                text += '\n\n'
        return text

    def qn(self, tag):
        prefix, tagroot = tag.split(':')
        uri = DOCX_NS
        return f'{{{uri}}}{tagroot}'

def process_args():
    parser = argparse.ArgumentParser(description='A utility to extract text from docx files.')
    parser.add_argument("docx_path", help="path of the docx file or directory containing docx files")
    parser.add_argument('-o', '--output_csv', help='path of the output CSV file')
    args = parser.parse_args()

    if not os.path.exists(args.docx_path):
        logging.error('Path %s does not exist.', args.docx_path)
        sys.exit(1)

    return args

def write_to_csv(data, output_path):
    sorted_data = sorted(data, key=lambda x: (x[0], x[1]))  # Sort by Document ID and then Record ID
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Document ID', 'Record ID', 'Pattern', 'Matched Content', 'Value'])
        csv_writer.writerows(sorted_data)

def main():
    args = process_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logging.info("Extracting features from documents...")

    extractor = FeatureExtractor()

    if os.path.isfile(args.docx_path):
        parser = DocumentParser(args.docx_path, extractor)
        extracted_features = parser.parse_document(os.path.basename(args.docx_path))
    else:
        docx_files = glob(os.path.join(args.docx_path, '*.docx'))
        extracted_features = []

        for docx_file in docx_files:
            parser = DocumentParser(docx_file, extractor)
            extracted_features.extend(parser.parse_document(os.path.basename(docx_file)))

    if args.output_csv:
        write_to_csv(extracted_features, args.output_csv)
        logging.info("Features extracted and saved to %s", args.output_csv)

if __name__ == '__main__':
    main()
    