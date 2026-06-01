import os
import pydicom
from pydicom.misc import is_dicom


def _normalize(s):
    """Normalize a string for case-insensitive, whitespace-insensitive comparison.

    Args:
        s: String to normalize.

    Returns:
        Lowercase string with spaces and underscores removed.
    """
    return s.lower().replace(" ", "").replace("_", "")


def find_metadata(ds, field_name):
    """Search a DICOM dataset for a field by name, matching case-insensitively.

    Args:
        ds:         pydicom Dataset to search.
        field_name: Field name to look up (case-insensitive, spaces/underscores ignored).

    Returns:
        Tuple of (actual_field_name, value_as_str) if found,
        or (field_name, None) if the field is not present in the dataset.
    """
    normalized = _normalize(field_name)
    for elem in ds:
        if _normalize(elem.keyword) == normalized or _normalize(elem.name) == normalized:
            return elem.name, str(elem.value)
    return field_name, None


def find_dicom_files(directory, metadata=[]):
    """Return DICOM file paths found by recursively descending directory.

    Paths are relative to directory (not including directory itself),
    suitable for use as arguments from the working directory.

    Args:
        directory: Root directory to search.
        metadata:  List of (field, values) tuples used to filter results.
                   Only files where every field's value appears in its
                   corresponding values tuple are included. Pass an empty
                   list (default) to return all DICOM files.

    Returns:
        List of relative file paths (str) for matching DICOM files.
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
