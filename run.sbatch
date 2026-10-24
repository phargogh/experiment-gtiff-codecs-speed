#!/bin/bash
#
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jdouglass@stanford.edu
#SBATCH --partition=serc,hns,normal
#SBATCH --job-name="InVEST routing codec tests"
#SBATCH --output=/scratch/users/jadoug06/slurm-logfiles/slurm-%j.%x.out

hostname
cat /proc/cpuinfo

singularity run "docker://ghcr.io/natcap/devstack:2025-07-01" python test-script.py
