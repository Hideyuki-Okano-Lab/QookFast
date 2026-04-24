<h1 align="center">
<img src=https://github.com/yo-aka-gene/QookFast/blob/main/logo/logo.png?raw=true width="400">
</h1><br>

![QookFast Version](https://img.shields.io/github/v/tag/yo-aka-gene/QookFast?label=QookFast&color=blue)


# QookFast: The "Bento" Pipeline for converting FastQ files into a count matrix.

Got raw FastQ files but dreading the pipeline setup? I feel you. And the headache doesn't stop there—modern science demands your entire environment to be 100% reproducible. But here’s your ultimate hack: grab this preset template and spin up a fully automated, containerized RNA-seq pipeline. Absolute reproducibility, perfectly packed into one box, and ready to serve in just a few keystrokes. Launch your project with this one-liner pipeline, the data will be ready to go! Enjoy "qooking" biology!

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- **Git**: For version control.
- **Apptainer**: Required for containerized, reproducible execution.
- **Python 3 & pip**: Required to install the template engine.
- **Cookiecutter & jinja2-time**: Required for project configuration in QookFast.

**For macOS**

Using [Homebrew](https://brew.sh/) is the easiest way:
```bash
brew install git apptainer
pip install cookiecutter jinja2-time
```

**For Windows (WSL2 / Ubuntu)**

Run the following command to install all the prerequisites at once:
```bash
sudo apt update && sudo apt install -y git apptainer python3 python3-pip
pip install cookiecutter jinja2-time
```

## User Guide
1. Run:
```bash
cookiecutter git@github.com:yo-aka-gene/QookFast.git
```

2. Answer the prompts to configure project details
    - `project_name`: name of the project
    - `description`: description for the project
    - `author_name`: the owner name (probably your name)
    - `email`: the owner contact
    - `species`: choose from `Homo_sapiens` or `Mus_musculus`
    - `read_length`: read length (default: `150`)
    - `read_type`: choose from `single_end` or `pair_end`
    - `threads`: thread numbers (default: `4`)
    - `strand`: choose from `unstranded`, `stranded`, or `rev-stranded`

:warning: **Important**: Please ensure you provide an accurate `project_name`, `author_name`, and `email` during the initialization. Since the `.sif` container file required for absolute reproducibility is too large to be hosted on GitHub, leaving accurate contact information is essential. This allows future collaborators to easily reach out and request the original container file from you.

:warning: **Note**: Parameters such as `read_length`, `read_type`, and `strand` vary depending on the sequencing platform used. Please verify these details prior to configuration.

You'll have a directory like this:
```
<your_project_name>/
    ├── align/
    │   └── (.bam files will be generated here)
    ├── counts/
    │   └── (count matrix will be generated here)
    ├── genome/
    │   ├── star_index/
    │   │   └── (STAR index files will be automatically generated here)
    │   └── (reference genome files are automatically downloaded here)
    ├── qc/
    │   └── (fastp outputs will be generated here)
    ├── raw_data/
    │   └── (manually move your .fastq.gz files here)
    ├── <your_project_name>.def
    ├── get_versions.sh
    ├── Makefile
    ├── README.md
    └── run_pipeline.sh
```

3. Run:
```bash
cd <your_project_directory>
make setup
```

4. Move all your `.fastq.gz` files into the `raw_data/` directory.
5. Run:
```
make run
```

### Note on Reproducibility
QookFast downloads the latest tools at the time of initialization to build your `.sif` container. To ensure absolute reproducibility for your collaborators, please secure an external method to store and share your generated `.sif` file (e.g., Google Drive, Zenodo, or AWS S3). Since `.sif` files are too large for GitHub, you cannot push them like regular code files, meaning your collaborators won't be able to simply clone them.


### :octocat: Git and Large Files
- **Automatic Initialization**: `git init` is automatically performed upon project creation. You can start tracking your scripts immediately.
- **NEVER Push Large Files**: Do not add or push large biological data to GitHub. This includes:
    - Apptainer container (`*.sif`)
    - Raw data (`raw_data/*.fastq.gz`)
    - Processed QC data (`qc/*.fastq.gz`)
    - Alignment files (`align/**/*.bam`)
    - Genome indices and FASTA files (`genome/*`)
- **Storage Limit**: GitHub has strict file size limits. If you accidentally attempt to push these files, the operation will fail and may corrupt your local environment's Git state.
---
## For developers
0. Additional prerequisite: `poetry`
1. Clone this repository:
```bash
git clone git@github.com:yo-aka-gene/QookFast.git
cd QookFast
```
2. Run:
```bash
poetry install
poetry run pre-commit install
```
