# parse_local_html.py

import re
import json
import json5
from bs4 import BeautifulSoup

def get_variants_from_html(html_file):
    """Extract variant data from locally saved HTML file."""
    
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # ✅ Find all script tags
    scripts = soup.find_all("script")
    print(f"Total scripts found: {len(scripts)}")

    for script in scripts:
        text = script.string
        if not text:
            continue

        if "twister-js-init-dpx-data" in text:
            match = re.search(r'var\s+dataToReturn\s*=\s*({[\s\S]*?})\s*;', text)
            if not match:
                print("dataToReturn not found")
                return None, None

            json_text = match.group(1)
            json_text = re.sub(r'"\s*\+\s*"', '', json_text)
            json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
            json_text = json_text.replace("\n", " ")

            try:
                data = json5.loads(json_text)
            except Exception as e:
                print(f"❌ Failed to parse twister JSON: {e}")
                return None, None

            print("✅ Parsed successfully")

            variant_keys = data["dimensions"]
            variants_raw = data["dimensionValuesDisplayData"]

            # ✅ Format variants
            formatted_variants = {
                asin: dict(zip(variant_keys, values))
                for asin, values in variants_raw.items()
            }

            print("Variant keys:", variant_keys)
            print("Variants:", json.dumps(formatted_variants, indent=2))

            return variant_keys, formatted_variants

    print("❌ No twister data found in HTML")
    return None, None


if __name__ == "__main__":
    variant_keys, formatted_variants = get_variants_from_html("product_detail.html")

    if formatted_variants:
        with open("variants_output.json", "w", encoding="utf-8") as f:
            json.dump({
                "variant_keys": variant_keys,
                "variants": formatted_variants
            }, f, indent=4, ensure_ascii=False)
        print("✅ Saved to variants_output.json")