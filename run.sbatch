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

# DEM is in James' user directory on Oak.
# --cleanenv overrides all my environment variables - prevents leakage into the container's runtime
#   This also prevents a problem I encoutered where my $HOME directory had a local install of
#   pygeoprocessing that the container was trying to import.
singularity run --cleanenv "docker://ghcr.io/natcap/devstack:2025-07-01" python test-script.py aligned_dem_TFA1000_float32.tif
