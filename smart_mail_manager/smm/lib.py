import re


def validate_and_extract(input_string):
    # Regex pattern for valid format: digit + space + unit (e.g., '2 days', '3 months')
    pattern = r'(\d+)\s*(days|months)'

    # Find all matches in the input string
    matches = re.findall(pattern, input_string)

    # Validation: Check if all words match the valid pattern and are not missing parts
    if not matches:
        return None, "Invalid format"

    # Extract digits (quantities)
    digits = [int(match[0]) for match in matches]

    # Check if original string structure matches pattern (to avoid partial matches like '2 3 days')
    cleaned_string = ' '.join([f"{match[0]} {match[1]}" for match in matches])
    if cleaned_string != input_string.strip():
        return None, "Invalid format"

    return digits, "Valid format"
