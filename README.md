
# SRI Hash Validator

This script fetches the HTML content of specified URLs, extracts tags with Subresource Integrity (SRI) attributes, and validates the integrity of the resources by comparing the provided SRI hashes with computed hashes of the fetched resources.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Install Python 3.x if you don't have it installed.
2. Install the required libraries using pip:
   ```sh
   pip install requests beautifulsoup4
   ```

## Usage

1. Update the list of URLs you want to process in the `urls` variable.
   ```python
   urls = ["https://cash.app/", "https://www.google.com/", "https://www.cyberghostvpn.com/"]
   ```
2. Run the script:
   ```sh
   python sri_validator.py
   ```

## Script Overview

1. **fetch_html(url)**: Fetches the HTML content of the given URL.
2. **extract_sri_tags(html)**: Extracts tags (`<script>` and `<link>`) with SRI attributes from the HTML content.
3. **extract_integrity_info(tags)**: Extracts the URL and SRI hash from the tags.
4. **validate_integrity(info)**: Validates the integrity of the resources by fetching them and comparing the provided SRI hash with the computed hash.

## Example Output

For each URL, the script will print messages indicating whether the hashes match or if there are any errors during processing.

```plaintext
Processing https://cash.app/
Hash matches for https://example.com/script.js
Hash mismatch for https://example.com/style.css
Provided hash: abcdef...
Computed hash: 123456...
No SRI tags for https://www.google.com/
```

This output helps you verify the integrity of resources loaded by the URLs you are processing.

## Notes

Please note that testing and the URLs provided in the script are all active Bugcrowd targets at the time of the creation of this script.

## Edge Cases

- Dynamically loaded URLs will not work as can be seen on https://www.humblebundle.com.
- Nonces for inline scripts are not checked.
