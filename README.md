# File Organiser (Auto‑Installer Edition)

File Organiser tidies a folder by moving files into dated subfolders based on their type. This edition bootstraps its own Python dependencies on first run, then performs the sorting.

- Automatically installs: python-docx, PyPDF2 (only if missing)
- Categorises common Images, Videos, Audio, Documents, Archives, Applications (extensible)
- Creates YYYY-MM subfolders inside each category for tidy, chronological organisation
- Avoids name collisions by generating unique filenames
- Prints a clear summary of all moves

## How it works

1) On startup, the script checks for required packages and installs any that are missing via pip.  
2) It scans the script’s directory for regular files (excluding itself and hidden files).  
3) Each file is categorised by extension and moved to:
   - //  
4) A progress log is printed, followed by a final summary.

Note: python-docx and PyPDF2 are prepared for future content‑aware features; current categorisation is extension‑based.

## Requirements

- Python 3.8+  
- Internet access on first run (to install missing dependencies)  
- pip available in the environment

## Installation

```bash
# Clone or download the repository
git clone 
cd 

# Optional: use a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

## Usage

Important: Place the tools in the folder that needs organising.

- Put organise.py (and optionally add_exclusion.bat) inside the exact folder to be sorted.
- Run the commands from that folder.

```bash
# From the directory that you want to organise (where organise.py is located)
python organise.py
```

What happens:
- The script prints “Installing …” if a dependency is missing, then continues.  
- Files in the same directory as organise.py are moved into category/YYYY-MM/ subfolders.  
- A summary shows how many files were moved successfully.

## Windows Defender false positives (add an exclusion)

Some Windows setups may quarantine or delete downloaded scripts or executables even when they are safe. If Defender flags or removes this tool (or anything you download alongside it) unnecessarily, add the current folder as an exclusion so the files are not blocked.

Two options:

- Manual (Windows Security UI)
  - Windows Security → Virus & threat protection → Manage settings → Exclusions → Add or remove exclusions → Add an exclusion → Folder.
  - Select the folder that contains organise.py.

- Automated (provided script)
  - Use add_exclusion.bat from inside the folder that you want to organise.
  - Right‑click add_exclusion.bat and choose “Run as administrator”.
  - It adds the current folder to Defender’s exclusion list via PowerShell.
  - To remove later, open Windows Security and delete the exclusion from the Exclusions list.

Important:
- Only exclude folders that are trusted. Exclusions reduce protection for the excluded path.
- Run the batch file from inside the target folder so the correct path is excluded.

## Customisation

- Extend categories:
  - Edit self.categories in SmartAutoSort.__init__ to add extensions or new groups.
- Change folder naming:
  - Modify monthly_folder() (e.g., “%Y/%m” or “%Y-%m-%d”).
- Collision behaviour:
  - uniq_name() appends “_1”, “_2”, … to avoid overwriting.

## Safety notes

- Files are moved (not copied) using shutil.move.  
- Hidden files and the script itself are skipped.  
- On failure (permissions/locks), the error is shown and processing continues.  
- Always test in a small folder before running on large collections.

## Troubleshooting

- “Could not install ”
  - Ensure internet access and pip availability: python -m pip install python-docx PyPDF2
- “No files to organise”
  - Confirm files are in the same directory as organise.py and not hidden.
- Wrong categorisation
  - Add the file’s extension to the desired category list.

## License

MIT License. See LICENSE for details.

## Disclaimer

Use at your own risk. While File Organiser aims to be safe and predictable, always keep backups of important files before bulk operations.