#!/bin/bash

set -euo pipefail

BASE=$(pwd)
GENOME_DIR=${BASE}/genome/star_index
GTF=${BASE}/genome/{{cookiecutter.species}}.{{cookiecutter.__ref}}.112.gtf

THREADS={{ cookiecutter.threads }}
{% if cookiecutter.strand == "unstranded" %}
STRAND=0
{% elif cookiecutter.strand == "stranded" %}
STRAND=1
{% else %}
STRAND=2
{% endif %}
READ_LEN={{ cookiecutter.read_length }}
OVERHANG=$((READ_LEN - 1))


{% if cookiecutter.read_type == "paired_end" %}
SAMPLES=($(ls ${BASE}/raw_data/*_R1.fastq.gz 2>/dev/null | xargs -n 1 basename | sed 's/_R1\.fastq\.gz//' || true))
{% else %}
SAMPLES=($(ls ${BASE}/raw_data/*.fastq.gz 2>/dev/null | xargs -n 1 basename | sed 's/\.fastq\.gz//' || true))
{% endif %}

## Step 1: fastp QC
for SAMPLE in "${SAMPLES[@]}"; do
  echo "[fastp] ${SAMPLE}"
{% if cookiecutter.read_type == "paired_end" %}
  fastp \
    -i ${BASE}/raw_data/${SAMPLE}_R1.fastq.gz \
    -I ${BASE}/raw_data/${SAMPLE}_R2.fastq.gz \
    -o ${BASE}/qc/${SAMPLE}_R1_clean.fastq.gz \
    -O ${BASE}/qc/${SAMPLE}_R2_clean.fastq.gz \
    -j ${BASE}/qc/${SAMPLE}_fastp.json \
    -h ${BASE}/qc/${SAMPLE}_fastp.html \
    --thread ${THREADS} --detect_adapter_for_pe \
    --qualified_quality_phred 20 \
    --length_required 36 \
    --correction --overrepresentation_analysis
{% else %}
  fastp \
    -i ${BASE}/raw_data/${SAMPLE}.fastq.gz \
    -o ${BASE}/qc/${SAMPLE}_clean.fastq.gz \
    -j ${BASE}/qc/${SAMPLE}_fastp.json \
    -h ${BASE}/qc/${SAMPLE}_fastp.html \
    --thread ${THREADS} \
    --qualified_quality_phred 20 \
    --length_required 36
{% endif %}
done

## Step 2: STAR alignment
BAM_LIST=()
for SAMPLE in "${SAMPLES[@]}"; do
  echo "[STAR] ${SAMPLE}"
  OUTDIR=${BASE}/align/${SAMPLE}
  mkdir -p ${OUTDIR}
  
{% if cookiecutter.read_type == "paired_end" %}
  R1=${BASE}/qc/${SAMPLE}_R1_clean.fastq.gz
  R2=${BASE}/qc/${SAMPLE}_R2_clean.fastq.gz
{% else %}
  R1=${BASE}/qc/${SAMPLE}_clean.fastq.gz
  R2=""
{% endif %}
STAR \
    --runThreadN         ${THREADS} \
    --genomeDir          ${GENOME_DIR} \
    --readFilesIn        ${R1} ${R2} \
    --readFilesCommand   zcat \
    --outSAMtype         BAM SortedByCoordinate \
    --outSAMattributes   NH HI AS NM MD \
    --outFileNamePrefix  ${OUTDIR}/ \
    --quantMode          GeneCounts \
    --outFilterMultimapNmax 10 \
    --alignSJoverhangMin 8 \
    --outFilterMismatchNoverReadLmax 0.04 \
    --alignIntronMin     20 \
    --alignIntronMax     1000000 \
    --alignMatesGapMax   1000000
    
  samtools index ${OUTDIR}/Aligned.sortedByCoord.out.bam
  BAM_LIST+=("${OUTDIR}/Aligned.sortedByCoord.out.bam")
done

## Step 3: featureCounts
echo "[featureCounts] all samples"
{% if cookiecutter.read_type == "paired_end" %}
featureCounts \
  -T ${THREADS} -p --countReadPairs \
  -s ${STRAND} -t exon -g gene_id \
  -a ${GTF} \
  -o ${BASE}/counts/all_samples_counts.txt \
  "${BAM_LIST[@]}"
{% else %}
featureCounts \
  -T ${THREADS} \
  -s ${STRAND} -t exon -g gene_id \
  -a ${GTF} \
  -o ${BASE}/counts/all_samples_counts.txt \
  "${BAM_LIST[@]}"
{% endif %}

## Step 4: Exporting count matrix as a .txt file
cut -f1,7- ${BASE}/counts/all_samples_counts.txt \
  | tail -n +2 \
  > ${BASE}/counts/count_matrix.txt

echo "=== Pipeline complete: $(date) ==="
echo "Output: ${BASE}/counts/count_matrix.txt"
