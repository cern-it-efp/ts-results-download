# ts-results-download

Use this tool to fetch result files (JSON) from the results bucket on the CERN cloud using their pre-signed URLs.

```bash
python3 main.py -p FILE_LIST_PS_URLS -d DESTINATION
```

### Options

- **-p, --pre-signed-URLs**

Use this option to indicate the path to a file listing pre-signed URLs (Required).

- **-d, --destination**

Use this option to indicate the location where to save fetched files. If this option is not used, the files will be located in the current directory.
