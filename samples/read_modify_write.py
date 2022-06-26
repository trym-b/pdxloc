"""Show how to read, modify and write localisation to files"""

from pathlib import Path
from pprint import PrettyPrinter
from typing import OrderedDict

from pdxloc.util import read_localisation, write_localisation


def _main() -> None:
    current_dir = Path(__file__).parent
    typical_localisation_file = current_dir / "typical_loc_file.yml"
    print(f"Reading localisation file '{typical_localisation_file}'")
    data = read_localisation(typical_localisation_file)
    print("Original data:")
    pretty_printer = PrettyPrinter(indent=4)
    pretty_printer.pprint(data)
    modified_data: OrderedDict[str, OrderedDict[str, str]] = OrderedDict(
        {"l_english": OrderedDict()}
    )
    print("Changing some values")
    for key, value in data["l_english"].items():
        modified_data["l_english"][key] = f"{value} - My new suffix"
    print("Modified data:")
    pretty_printer.pprint(modified_data)
    output_dir = current_dir.parent / "build" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "modified_loc_file.yml"
    print(f"Writing to output location '{output_file}'")
    write_localisation(modified_data, output_file)


if __name__ == "__main__":
    _main()
