#!/bin/bash

FASTP_VER=$(fastp --version 2>&1 | awk '{print $2}')
STAR_VER=$(STAR --version)
SUBREAD_VER=$(featureCounts -v 2>&1 | grep "featureCounts" | awk '{print $2}')
SAMTOOLS_VER=$(samtools --version | head -n 1 | awk '{print $2}')

cat <<EOF > software_versions.yaml
project: {{ cookiecutter.project_name}}
timestamp: "$(date +"%Y-%m-%d %H:%M:%S")"
software_versions:
  fastp: "${FASTP_VER}"
  STAR: "${STAR_VER}"
  subread_featureCounts: "${SUBREAD_VER}"
  samtools: "${SAMTOOLS_VER}"
EOF
