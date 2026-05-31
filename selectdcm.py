import argparse

from lib import find_dicom_files

DEFAULT_METADATA = [('Series Description', ('L Spine LAT', 'L Spine EXT'))]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List DICOM files in a directory matching metadata criteria."
    )
    parser.add_argument("directory", help="Directory to search for DICOM files")
    args = parser.parse_args()

    paths = find_dicom_files(args.directory, metadata=DEFAULT_METADATA)
    if not paths:
        print(f"No matching DICOM files found in '{args.directory}'.")
    else:
        print(f"Found {len(paths)} matching DICOM file(s):")
        for path in paths:
            print(path)
