.PHONY: setup download_genome run

setup:
	@sudo apt update && sudo apt upgrade -y
	@sudo apt install -y build-essential wget curl unzip pigz samtools
	@sh get_versions.sh
	@make download_genome
	@echo "Move your .fastq.gz files to ./raw_data/"
	@echo "To configure detailed pipeline parameters, manually edit ./run_pipeline.sh"


download_genome:
	wget -P genome https://ftp.ensembl.org/pub/release-112/fasta/{{cookiecutter.species.lower()}}/dna/{{cookiecutter.species}}.{{cookiecutter.__ref}}.dna.primary_assembly.fa.gz
	wget -P genome https://ftp.ensembl.org/pub/release-112/gtf/{{cookiecutter.species.lower()}}/{{cookiecutter.species}}.{{cookiecutter.__ref}}.112.gtf.gz
	pigz -d genome/*.gz
	STAR --runMode genomeGenerate \
		--runThreadN {{cookiecutter.threads}} \
		--genomeDir genome/star_index \
		--genomeFastaFiles genome/{{cookiecutter.species}}.{{cookiecutter.__ref}}.dna.primary_assembly.fa \
		--sjdbGTFfile genome/{{cookiecutter.species}}.{{cookiecutter.__ref}}.112.gtf \
		--sjdbOverhang $$(({{cookiecutter.read_length}} - 1))


run:
	@sh run_pipeline.sh
