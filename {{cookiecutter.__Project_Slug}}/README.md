# {{cookiecutter.project_name}}
{%- if cookiecutter.description != "" %}
{{cookiecutter.description}}
{%- endif %}

- Generation date: {{cookiecutter.__timestamp}}

## Project Owner
- Name: {{cookiecutter.author_name}}
- Contact: [{{cookiecutter.email}}](mailto:{{cookiecutter.email}})


## Pipeline Details
- species: `{{cookiecutter.species}}`
- reference gemone: `{{cookiecutter.__ref}}`
- reference genome version: `112`
- read type: `{{cookiecutter.read_type}}`
- strand: `{{cookiecutter.strand}}`
- thred numbers: `{{cookiecutter.threads}}`
- dependency versions: detailed in `software_versions.yaml`

## User Guide
Now you have a directory like this:
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

1. Run:
```bash
cd <your_project_directory>
make setup
```

2. Move all your `.fastq.gz` files into the `raw_data/` directory.
3. Run:
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
