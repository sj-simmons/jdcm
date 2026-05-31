import os
import pydicom
from pydicom.misc import is_dicom

def _normalize(s):
    return s.lower().replace(" ", "").replace("_", "")

def find_metadata(ds, field_name):
    normalized = _normalize(field_name)
    for elem in ds:
        if _normalize(elem.keyword) == normalized or _normalize(elem.name) == normalized:
            return elem.name, str(elem.value)
    return field_name, None

def find_dicom_files(directory, metadata=[]):
    """Return list of DICOM file paths found under directory.

    Paths are relative to directory (not including directory itself),
    suitable for use as arguments from the working directory.

    metadata is a list of (field, values) tuples. Only files where every
    field matches one of its allowed values are returned. Pass an empty
    list to return all DICOM files.
    """
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                if not is_dicom(full_path):
                    continue
                if metadata:
                    ds = pydicom.dcmread(full_path)
                    if not all(
                        find_metadata(ds, field)[1] in values
                        for field, values in metadata
                    ):
                        continue
                results.append(os.path.relpath(full_path, directory))
            except Exception as e:
                print(f"Error checking '{full_path}': {e}")
    return results
