import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests

DEFAULT_FACT_TAGS = [
    "us-gaap:Revenues",
    "us-gaap:Assets",
    "us-gaap:NetIncomeLoss",
    "dei:EntityCommonStockSharesOutstanding",
    "ifrs-full:Revenue",
    "ifrs-full:Assets",
    "ifrs-full:ProfitLoss",
    "ifrs-full:Equity",
]


class CompanyFactsExtractor:
    """Extracts and processes SEC company facts data from JSON files or API."""

    def __init__(self, fact_tags: Optional[List[str]] = None):
        self.fact_tags = fact_tags or DEFAULT_FACT_TAGS

    def extract_from_file(self, json_file_path: str) -> Tuple[Dict, pd.DataFrame]:
        """Extract company facts from a local JSON file."""
        file_path = Path(json_file_path)

        # If file doesn't exist, try relative to script location
        if not file_path.exists():
            script_dir = Path(__file__).parent
            file_path = script_dir / json_file_path

        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return self._process_company_data(data)

    # def extract_from_api(
    #     self, cik: str, headers: Dict[str, str]
    # ) -> Tuple[Dict, pd.DataFrame]:
    #     """Extract company facts from SEC API."""
    #     url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()
    #     data = response.json()

    #     return self._process_company_data(data)

    def _process_company_data(self, data: Dict) -> Tuple[Dict, pd.DataFrame]:
        """Process raw company data into metadata and facts DataFrame."""
        metadata = self._extract_metadata(data)
        facts_df = self._extract_facts(data)

        return metadata, facts_df

    def _extract_metadata(self, data: Dict) -> Dict[str, str]:
        """Extract company metadata from SEC data."""
        return {
            "cik": data.get("cik", ""),
            "name": data.get("entityName", ""),
            "sic": data.get("sic", ""),
        }

    def _extract_facts(self, data: Dict) -> pd.DataFrame:
        """Extract and structure facts data into DataFrame."""
        facts_list = []

        for taxonomy in data.get("facts", {}):
            self._current_taxonomy = taxonomy  # Store current taxonomy
            facts_by_taxonomy = data["facts"][taxonomy]
            facts_list.extend(self._process_taxonomy_facts(facts_by_taxonomy))

        facts_df = pd.DataFrame(facts_list)

        if not facts_df.empty:
            facts_df = facts_df.sort_values(
                ["filed_date", "fiscal_year", "fiscal_period"], ascending=False
            )

        return facts_df

    def _process_taxonomy_facts(self, facts_by_taxonomy: Dict) -> List[Dict]:
        """Process facts for a specific taxonomy."""
        facts_list = []

        for tag, tag_data in facts_by_taxonomy.items():
            # Build full tag name with taxonomy prefix
            full_tag = f"{self._current_taxonomy}:{tag}"

            if full_tag not in self.fact_tags:
                continue

            tag_label = tag_data.get("label", "")

            for unit, unit_data in tag_data.get("units", {}).items():
                for fact in unit_data:
                    fact_entry = self._create_fact_entry(
                        full_tag, tag_label, unit, fact
                    )
                    facts_list.append(fact_entry)

        return facts_list

    def _create_fact_entry(self, tag: str, label: str, unit: str, fact: Dict) -> Dict:
        """Create a structured fact entry."""
        return {
            "tag": tag,
            "label": label,
            "unit": unit,
            "value": fact.get("val", ""),
            "start_date": fact.get("start", ""),
            "end_date": fact.get("end", ""),
            "fiscal_year": fact.get("fy", ""),
            "fiscal_period": fact.get("fp", ""),
            "form": fact.get("form", ""),
            "filed_date": fact.get("filed", ""),
            "accession_number": fact.get("accn", ""),
        }

    def filter_by_period(
        self, facts_df: pd.DataFrame, period_filter: str
    ) -> pd.DataFrame:
        """Filter facts by fiscal period (e.g., '2024FY')."""
        if facts_df.empty:
            return facts_df

        period_mask = (
            facts_df["fiscal_year"].astype(str) + facts_df["fiscal_period"]
        ) == period_filter

        return facts_df[period_mask]


def save_facts_to_csv(facts_df: pd.DataFrame, cik: str, output_dir: str = ".") -> str:
    """Save facts DataFrame to CSV file."""
    output_path = Path(output_dir) / f"company_facts_{cik}.csv"
    facts_df.to_csv(output_path, index=False)
    return str(output_path)


def display_company_summary(metadata: Dict, facts_df: pd.DataFrame) -> None:
    """Display company metadata and facts summary."""
    print("\nCompany Metadata:")
    print(f"CIK: {metadata['cik']}")
    print(f"Name: {metadata['name']}")
    print(f"SIC: {metadata['sic']}")

    if facts_df.empty:
        print("\nNo facts found for specified criteria.")
        return

    print(f"\nExtracted {len(facts_df)} facts:")
    display_columns = [
        "tag",
        "label",
        "value",
        "unit",
        "end_date",
        "fiscal_year",
        "fiscal_period",
        "form",
        "filed_date",
    ]
    print(facts_df[display_columns].to_string())


def extract_company_facts(
    json_file: Optional[str] = None,
    cik: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    fact_tags: Optional[List[str]] = None,
    period_filter: Optional[str] = None,
) -> Tuple[Dict, pd.DataFrame]:
    """Legacy function for backward compatibility."""
    extractor = CompanyFactsExtractor(fact_tags)

    if json_file:
        metadata, facts_df = extractor.extract_from_file(json_file)
    # elif cik and headers:
    #     metadata, facts_df = extractor.extract_from_api(cik, headers)
    else:
        raise ValueError("Must provide either json_file or cik with headers.")

    if period_filter:
        facts_df = extractor.filter_by_period(facts_df, period_filter)

    return metadata, facts_df


def main():
    """Main function demonstrating usage of the CompanyFactsExtractor."""
    # json_file_path = "CIK0002007191.json"
    json_file_path = "CIK0001930021.json"
    period_filter = "2024FY"

    # First, let's see what tags are actually available
    file_path = Path(json_file_path)
    if not file_path.exists():
        script_dir = Path(__file__).parent
        file_path = script_dir / json_file_path

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print("Available tags in the data:")
    available_tags = []
    for taxonomy in data.get("facts", {}):
        for tag in data["facts"][taxonomy]:
            full_tag = f"{taxonomy}:{tag}"
            available_tags.append(full_tag)

    # Show key financial tags that we're interested in
    key_tags = [
        tag
        for tag in available_tags
        if any(
            keyword in tag.lower()
            for keyword in [
                "revenue",
                "assets",
                "profit",
                "equity",
                "entitycommonstockshares",
            ]
        )
    ]

    print("\nKey financial tags found:")
    for tag in sorted(key_tags):
        print(f"  {tag}")

    # Use the actual available tags
    fact_tags = [
        "dei:EntityCommonStockSharesOutstanding",
        "ifrs-full:Revenue",
        "ifrs-full:Assets",
        "ifrs-full:ProfitLoss",
        "ifrs-full:Equity",
    ]

    extractor = CompanyFactsExtractor(fact_tags)

    try:
        metadata, facts_df = extractor.extract_from_file(json_file_path)

        print(f"\nTotal facts extracted: {len(facts_df)}")

        if not facts_df.empty:
            print("\nAvailable fiscal periods:")
            available_periods = (
                facts_df["fiscal_year"].astype(str) + facts_df["fiscal_period"]
            )
            unique_periods = available_periods.unique()
            print(sorted(unique_periods))

        if period_filter:
            facts_df = extractor.filter_by_period(facts_df, period_filter)

        display_company_summary(metadata, facts_df)

        if not facts_df.empty:
            output_file = save_facts_to_csv(facts_df, metadata["cik"])
            print(f"\nFacts saved to {output_file}")

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except requests.RequestException as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
