import os
import subprocess


def find_dicom_files(directory):
    """Return list of DICOM file paths found under directory.

    Paths are relative to directory (not including directory itself),
    suitable for use as arguments from the working directory.
    Uses the Linux `file` command to detect DICOM files.
    """
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                result = subprocess.run(
                    ["file", full_path],
                    capture_output=True,
                    text=True,
                )
                if "DICOM" in result.stdout:
                    results.append(os.path.relpath(full_path, directory))
            except Exception:
                pass
    return results
