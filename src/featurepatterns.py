import re

# Define pattern dictionary with descriptive keys and column names
FEATURE_PATTERNS = {
    "Keywords": (re.compile(r'(Features|Specifications)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Keywords"),
    "Name": (re.compile(r'(Name|Product)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Name"),
    "Brand": (re.compile(r'(Brand)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Brand"),
    "Quantity": (re.compile(r'(Quantity|Count)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Quantity"),
    "Price": (re.compile(r'Price:\s*(?:\$\s*)?(\d+(?:,\d{3})*(?:\.\d{2})?)'), "Price"),
    "ProductionDate": (re.compile(r'(Production|Prod)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Production Date"),
    "ExpirationDate": (re.compile(r'(Expiration|Exp)[:\s]*(.*?)(?=\n|$)', re.IGNORECASE), "Expiration Date"),
    "Parentheses": (re.compile(r'\((.*?)\)', re.IGNORECASE), "Parentheses"),
    "Brackets": (re.compile(r'\[(.*?)\]', re.IGNORECASE), "Brackets"),
    "ColonSeparated": (re.compile(r'([^:]+)\s*:\s*([\s\S]*?)(?=\n|$)'), "Colon Separated"),
    "Asterisks": (re.compile(r'\*\s*(.*)'), "Asterisks"),
    "Tabular": (re.compile(r'\|(.*)\|'), "Tabular"),
    "Quoted": (re.compile(r'"(.*?)"'), "Quoted"),
    "Braces": (re.compile(r'\{(.*)\}'), "Braces"),
    "Dashes": (re.compile(r'—\s*(.*)'), "Dashes"),
    "UpperCaseWord": (re.compile(r'\b[A-Z][A-Z\s]+\b'), "Upper Case Word"),
    "URL": (re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'), "URL"),
    "Phone": (re.compile(r'\b(\+\d{1,3})?\s?(\d{1,4}[-\s]?){1,3}\d{1,4}\b'), "Phone"),
    "Email": (re.compile(r'[a-zA-Z0-9_\-\.]+@([a-zA-Z0-9_\-\.]+)\.[a-zA-Z]{2,5}'), "Email"),
    # ... add more patterns here ...
}
