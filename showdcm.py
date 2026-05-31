import pydicom
import matplotlib.pyplot as plt
import argparse
import sys

def _normalize(s):
    return s.lower().replace(" ", "").replace("_", "")

def find_metadata(ds, field_name):
    normalized = _normalize(field_name)
    for elem in ds:
        if _normalize(elem.keyword) == normalized or _normalize(elem.name) == normalized:
            return elem.name, str(elem.value)
    return field_name, None

def display_dicom(file_path, fields):
    try:
        ds = pydicom.dcmread(file_path)

        metadata_lines = []
        for field in fields:
            name, value = find_metadata(ds, field)
            metadata_lines.append(f"{name}: {value}" if value is not None else f"{field}: (not found)")

        fig, ax = plt.subplots()
        ax.imshow(ds.pixel_array, cmap=plt.cm.bone)
        ax.set_title(f"DICOM: {file_path}")
        ax.axis("off")

        if metadata_lines:
            fig.text(
                0.01, 0.01,
                "\n".join(metadata_lines),
                fontsize=8,
                verticalalignment="bottom",
                color="white",
                bbox=dict(boxstyle="round", facecolor="black", alpha=0.6),
            )

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error: Could not read file '{file_path}'. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display a DICOM image file.")
    parser.add_argument("filename", help="Path to the .dcm file you want to view")
    DEFAULT_FIELDS = ["Series Description", "Study Description"]
    parser.add_argument(
        "--fields", "-f",
        nargs="+",
        default=DEFAULT_FIELDS,
        metavar="FIELD",
        help=(
            "Metadata field names to display (case-insensitive). "
            f"Default: {DEFAULT_FIELDS}"
        ),
    )
    args = parser.parse_args()
    display_dicom(args.filename, args.fields)
