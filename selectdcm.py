import argparse
import os
import shutil

from lib import find_dicom_files

#DEFAULT_METADATA = [('Series Description', ('L Spine LAT', 'L Spine EXT'))]
DEFAULT_METADATA = [('Series Description', ('L Spine LAT',))]

def make_dest_name(path):
    name = path.replace("/", "").replace("\\", "").replace("-", "")
    name = name.replace("POSTOP", "postop").replace("PREOP", "preop")
    return name + ".dcm"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy matching DICOM files into a new directory."
    )
    parser.add_argument("directory", help="Directory to search for DICOM files")
    parser.add_argument("dest", help="Destination directory to create and copy files into")
    args = parser.parse_args()

    if os.path.exists(args.dest):
        print(f"Error: '{args.dest}' already exists.")
    else:
        paths = find_dicom_files(args.directory, metadata=DEFAULT_METADATA)
        if not paths:
            print(f"No matching DICOM files found in '{args.directory}'.")
        else:
            os.makedirs(args.dest)
            print(f"Found {len(paths)} matching DICOM file(s). Copying to '{args.dest}'.")
            for path in paths:
                dest_name = make_dest_name(path)
                shutil.copy2(
                    os.path.join(args.directory, path),
                    os.path.join(args.dest, dest_name),
                )
                print(f"  {path} -> {dest_name}")
