import pydicom
import matplotlib.pyplot as plt
import argparse
import sys

def display_dicom(file_path):
    """Reads and displays a DICOM image from a given file path."""
    try:
        # Load the dataset
        ds = pydicom.dcmread(file_path)

        # Display the pixel data
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
        plt.title(f"DICOM: {file_path}")
        plt.axis('off')
        plt.show()

    except Exception as e:
        print(f"Error: Could not read file '{file_path}'. {e}")

if __name__ == "__main__":
    # 1. Setup the argument parser
    parser = argparse.ArgumentParser(description="Display a DICOM image file.")

    # 2. Add a positional argument for the file path
    parser.add_argument("filename", help="Path to the .dcm file you want to view")

    # 3. Parse the command line arguments
    args = parser.parse_args()

    # 4. Call the function with the provided filename
    display_dicom(args.filename)
