import os
import pydicom
import matplotlib.pyplot as plt
import argparse
import sys

from lib import find_dicom_files, find_metadata

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

def browse_dicoms(file_paths, fields):
    state = {"index": 0}

    fig, ax = plt.subplots()

    def render(index):
        file_path = file_paths[index]
        try:
            ds = pydicom.dcmread(file_path)

            metadata_lines = []
            for field in fields:
                name, value = find_metadata(ds, field)
                metadata_lines.append(f"{name}: {value}" if value is not None else f"{field}: (not found)")

            ax.cla()
            ax.imshow(ds.pixel_array, cmap=plt.cm.bone)
            ax.set_title(f"DICOM ({index + 1}/{len(file_paths)}): {file_path}")
            ax.axis("off")

            for txt in fig.texts:
                txt.remove()

            if metadata_lines:
                fig.text(
                    0.01, 0.01,
                    "\n".join(metadata_lines),
                    fontsize=8,
                    verticalalignment="bottom",
                    color="white",
                    bbox=dict(boxstyle="round", facecolor="black", alpha=0.6),
                )

            fig.canvas.draw()

        except Exception as e:
            print(f"Error: Could not read file '{file_path}'. {e}")

    def on_key(event):
        if event.key == "right" and state["index"] < len(file_paths) - 1:
            state["index"] += 1
            render(state["index"])
        elif event.key == "left" and state["index"] > 0:
            state["index"] -= 1
            render(state["index"])

    fig.canvas.mpl_connect("key_press_event", on_key)
    render(0)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display a DICOM image file.")
    parser.add_argument("filename", help="Path to the .dcm file or directory you want to view")
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
    if os.path.isdir(args.filename):
        paths = [os.path.join(args.filename, p) for p in find_dicom_files(args.filename)]
        if not paths:
            print(f"No DICOM files found in '{args.filename}'.")
        elif len(paths) == 1:
            display_dicom(paths[0], args.fields)
        else:
            print(f"Found {len(paths)} DICOM files.")
            browse_dicoms(paths, args.fields)
    else:
        display_dicom(args.filename, args.fields)
