# jdcm

Utilities for browsing and selecting DICOM medical imaging files.

## Dependencies

- [pydicom](https://pydicom.github.io/)
- [matplotlib](https://matplotlib.org/)

## Scripts

### showdcm.py

Display a DICOM file or browse all DICOM files in a directory.

```
python showdcm.py <file_or_directory> [--fields FIELD ...]
```

- **file_or_directory** — path to a single `.dcm` file or a directory to search recursively.
- **--fields / -f** — metadata field names to overlay on the image (case-insensitive). Default: `Series Description`, `Study Description`.

When a directory is given, all DICOM files found are loaded into a browser. Use the **left/right arrow keys** to step through them. Navigation stops at the first and last image.

### selectdcm.py

Find DICOM files matching a metadata filter and copy them to a new directory with flattened, normalised filenames.

```
python selectdcm.py <directory> <dest>
```

- **directory** — root directory to search recursively for DICOM files.
- **dest** — destination directory to create. Exits with an error if it already exists.

Files are filtered by `DEFAULT_METADATA` (defined at the top of `selectdcm.py`). Currently selects files whose `Series Description` is `L Spine LAT`.

Destination filenames are derived from the source relative path by removing all slashes and dashes, replacing `POST-OP`/`PRE-OP` with `postop`/`preop`, and appending `.dcm`.

## Library

### lib.py

Shared functions used by the scripts above.

- **`find_dicom_files(directory, metadata=[])`** — recursively find DICOM files under `directory`, optionally filtered by metadata. Returns relative paths.
- **`find_metadata(ds, field_name)`** — look up a metadata field in a pydicom Dataset by name (case-insensitive).
