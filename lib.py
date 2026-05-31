import os
from pydicom.misc import is_dicom


def find_dicom_files(directory):
    """Return list of DICOM file paths found under directory.

    Paths are relative to directory (not including directory itself),
    suitable for use as arguments from the working directory.
    """
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                if is_dicom(full_path):
                    results.append(os.path.relpath(full_path, directory))
            except Exception as e:
                print(f"Error checking '{full_path}': {e}")
    return results
