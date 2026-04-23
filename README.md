<h1 align="center">
<img src=https://github.com/Hideyuki-Okano-Lab/QookingFever/blob/main/logo/logo.png?raw=true width="500">
</h1><br>


# QookingFever
Pipeline for converting FastQ files into count matrix

:warning: **Work in Progress**: This tool is currently under active development and is not yet guaranteed to be fully functional. We will notify all stakeholders once it is ready!

:warning: **Note**: Currently, this tool is specifically designed to run on the shared desktop in Room 3C. Other environments are not supported at this time.

## User Guide
1. Run:
```bash
cookiecutter git@github.com:Hideyuki-Okano-Lab/QookingFever.git
```
>:bulb: Tip: Alternatively, on the shared desktop in Room 3C at KRM, you can run the following commands inside WSL:
>```bash
>cd ~/develop
>make countmatrix
>```

2. Answer to the prompts to configure project details
    - `project_name`: name of the project
    - `description`: description for the project
    - `author_name`: the owner name (probably your name)
    - `email`: the owner contact
    - `species`: choose from `Homo_sapiens` or `Mus_mulculus`
    - `read_type`: choose from `single_end` or `pair_end`
    - `threads`: thread numbers (default: `8`)
    - `strand`: choose from `unstranded`, `stranded`, or `rev-stranded`

:warning: **Important**: Please ensure you provide an accurate `project_name`, `author_name`, and `email`. This information is crucial for administrative purposes, such as contacting you for permission to clean up old projects when the shared desktop storage becomes full.

:warning: **Note**: Parameters such as `read_type` and `strand` vary depending on the sequencing platform used. Please verify these details prior to configuration.

You'll have a directory like this:
```
<your_project_name>/
    ├── align/
    │   └── (.bam files will be generated here)
    ├── counts/
    │   └── (count matrix will be generated here)
    ├── genome/
    │   ├── star_index/
    │   │   └── (STAR index is automatically generated here)
    │   └── (reference genome files are automatically downloaded here)
    ├── qc/
    │   └── (fastp outputs will be generated here)
    ├── raw_data/
    │   └── (:bulb: manually move your .fastq.gz files here)
    ├── get_versions.sh
    ├── Makefile
    ├── README.md
    ├── run_pipeline.sh
    └── software_versions.yaml
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

### :octocat: Git and Large Files
- **Automatic Initialization**: `git init` is automatically performed upon project creation. You can start tracking your scripts immediately.
- **NEVER Push Large Files**: Do not add or push large biological data to GitHub. This includes:
    - Raw data (`raw_data/*.fastq.gz`)
    - Processed QC data (`qc/*.fastq.gz`)
    - Alignment files (`align/**/*.bam`)
    - Genome indices and FASTA files (`genome/*`)
- **Storage Limit**: GitHub has strict file size limits. If you accidentally attempt to push these files, the operation will fail and may corrupt your local environment's Git state.
---
## For developpers
0. Prerequisites: `poetry`
1. Clone this repository:
```bash
git clone git@github.com:Hideyuki-Okano-Lab/QookingFever.git
cd QookingFever
```
2. Run:
```bash
poetry install
poetry run pre-commit install
```
