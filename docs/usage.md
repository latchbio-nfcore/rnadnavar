# nf-core/rnadnavar: Usage

## :warning: Please read this documentation on the nf-core website: [https://nf-co.re/rnadnavar/usage](https://nf-co.re/rnadnavar/usage)

> _Documentation of pipeline parameters is generated automatically from the pipeline schema and can no longer be found in markdown files._

## Introduction

RaVEX is an end-to-end workflow designed for detecting somatic mutations in bulk RNA sequencing data, with the option to apply it to whole genome or whole exome sequencing data. It follows
[GATK best practices](https://gatk.broadinstitute.org/hc/en-us/articles/360035531192-RNAseq-short-variant-discovery-SNPs-Indels-) for data cleanup, utilises
[Mutect2](https://gatk.broadinstitute.org/hc/en-us/articles/360037593851-Mutect2), [Strelka2](https://gatk.broadinstitute.org/hc/en-us/articles/360037593851-Mutect2)
and
[SAGE](https://github.com/hartwigmedical/hmftools/blob/master/sage/README.md)
for variant calling, and includes post-processing steps
such as VCF normalization, consensus of called variants
(resulting in a MAF file), and filtering. Additionally, an optional realignment with HISAT2 is performed only in the coordinates where mutations were detected during the variant calling subworkflow.

Originally, this pipeline was developed for human and
mouse data.

## Quickstart

The typical command for running the pipeline is as follows:

```
nextflow run nf-core/rnadnavar -r <VERSION> -profile <PROFILE> --input ./samplesheet.csv --outdir ./results --tools <TOOLS>
```

`-r <VERSION>` is optional but strongly recommended for reproducibility and should match the latest version.

`-profile <PROFILE>` is mandatory and should reflect either your own institutional profile or any pipeline profile specified in the profile section.

This will launch the pipeline and perform variant
calling, normalisation, consensus and filtering if specified in
`--tools`, see the [parameter section](https://nf-co.
re/rnadnavar/latest/parameters#tools) for details on the
tools. In the above example the pipeline runs with the docker configuration profile. See below for more information about profiles.

## Samplesheet input

You will need to create a samplesheet with information about the samples you would like to analyse before running the pipeline. It has to be a comma-separated file with columns, and a header row as shown in the examples below. It is recommended to use the absolute path of the files, but a relative path should also work.

An RNA tumor sample must be associated to a DNA normal
sample at the moment, specified with the
same `patient` ID. The sample
type can be specified with the `status`: 0 (normal DNA),
1 (tumour DNA) and 2 (tumour RNA). An
additional tumor sample (such as a
relapse for example), can be added if specified with the
same patient ID but different sample name, and the status
value 1 or 2.

The pipeline will output results in a different
directory for _each sample_.

These are the accepted columns for the sample sheet,
although not all of them are mandatory at the same time:

| Column    | Description                                                                                                                                                                                                                                                                                                 |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `patient` | **Custom patient ID**; designates the patient/subject; must be unique for each patient, but one patient can have multiple samples (e.g. normal and tumor).                                                                                                                                                  |
| `status`  | **Normal DNA /tumor DNA /tumor RNA status of sample**; can be 0 (normal DNA), 1 (tumor DNA) or 2 (tumor RNA). Optional, Default: 0                                                                                                                                                                          |
| `sample`  | **Custom sample ID for each tumor and normal sample**; more than one tumor sample for each subject is possible, i.e. a tumor and a relapse; samples can have multiple lanes for which the same ID must be used to merge them later (see also lane). Sample IDs must be unique for unique biological samples |
| `lane`    | Lane ID, used when the sample is multiplexed on several lanes. Must be unique for each lane in the same sample (but does not need to be the original lane name), and must contain at least one character. _Required for --step_mapping_                                                                     |
| `fastq_1` | Path to FastQ file for Illumina short reads 1. File has to be gzipped and have the extension ".fastq.gz" or ".fq.gz".                                                                                                                                                                                       |
| `fastq_2` | Path to FastQ file for Illumina short reads 2. File has to be gzipped and have the extension ".fastq.gz" or ".fq.gz".                                                                                                                                                                                       |
| `bam`     | Path to (u)BAM file.                                                                                                                                                                                                                                                                                        |
| `bai`     | Path to BAM index file.                                                                                                                                                                                                                                                                                     |
| `cram`    | Path to CRAM file.                                                                                                                                                                                                                                                                                          |
| `crai`    | Path to CRAM index file.                                                                                                                                                                                                                                                                                    |
| `table`   | Path to recalibration table file.                                                                                                                                                                                                                                                                           |
| `vcf`     | Path to vcf file.                                                                                                                                                                                                                                                                                           |
| `maf`     | Path to maf file.                                                                                                                                                                                                                                                                                           |

An [example samplesheet](../assets/samplesheet.csv) has been provided with the pipeline.

## Running the pipeline

The typical command for running the pipeline is as follows:

```bash
nextflow run nf-core/rnadnavar --input ./samplesheet.csv --outdir ./results --genome GRCh37 -profile docker
```

This will launch the pipeline with the `docker` configuration profile. See below for more information about profiles.

Note that the pipeline will create the following files in your working directory:

```bash
work                # Directory containing the nextflow working files
<OUTDIR>            # Finished results in specified location (defined with --outdir)
.nextflow_log       # Log file from Nextflow
# Other nextflow hidden files, eg. history of pipeline runs and old logs.
```

If you wish to repeatedly use the same parameters for multiple runs, rather than specifying each flag in the command, you can specify these in a params file.

Pipeline settings can be provided in a `yaml` or `json` file via `-params-file <file>`.

:::warning
Do not use `-c <file>` to specify parameters as this will result in errors. Custom config files specified with `-c` must only be used for [tuning process resource specifications](https://nf-co.re/docs/usage/configuration#tuning-workflow-resources), other infrastructural tweaks (such as output directories), or module arguments (args).
:::

The above pipeline run specified with a params file in yaml format:

```bash
nextflow run nf-core/rnadnavar -profile docker -params-file params.yaml
```

with `params.yaml` containing:

```yaml
input: './samplesheet.csv'
outdir: './results/'
genome: 'GRCh37'
<...>
```

You can also generate such `YAML`/`JSON` files via [nf-core/launch](https://nf-co.re/launch).

### Starting from different steps

The pipeline has the flexibility to start from different steps

- mapping will require: `patient,status,sample,lane,bam,bai` or `patient,status,sample,lane,cram,crai` or `patient,status,sample,lane,bam,bai,cram,crai`. When BAM and CRAM files are mixed BAMs will be converted to CRAMs to save on space.

- variant_calling will require: `patient,status,sample,lane,bam,bai` or `patient,status,sample,lane,cram,crai` or `patient,status,sample,lane,bam,bai,cram,crai`. When BAM and CRAM files are mixed BAMs will be converted to CRAMs to save on space.

- normalise will require: `patient,status,sample,vcf,variantcaller,normal_id` if not realignment step in tools.
  - `normal_id` is needed to properly create the id tag, which is going to be tumour_vs_normal style to match it with the rest of the pipeline (note that this will be simplified in the future to just id but it is not yet implemented).

### Updating the pipeline

When you run the above command, Nextflow automatically pulls the pipeline code from GitHub and stores it as a cached version. When running the pipeline after this, it will always use the cached version if available - even if the pipeline has been updated since. To make sure that you're running the latest version of the pipeline, make sure that you regularly update the cached version of the pipeline:

```bash
nextflow pull nf-core/rnadnavar
```

### Reproducibility

It is a good idea to specify a pipeline version when running the pipeline on your data. This ensures that a specific version of the pipeline code and software are used when you run your pipeline. If you keep using the same tag, you'll be running the same version of the pipeline, even if there have been changes to the code since.

First, go to the [nf-core/rnadnavar releases page](https://github.com/nf-core/rnadnavar/releases) and find the latest pipeline version - numeric only (eg. `1.3.1`). Then specify this when running the pipeline with `-r` (one hyphen) - eg. `-r 1.3.1`. Of course, you can switch to another version by changing the number after the `-r` flag.

This version number will be logged in reports when you run the pipeline, so that you'll know what you used when you look back in the future. For example, at the bottom of the MultiQC reports.

To further assist in reproducbility, you can use share and re-use [parameter files](#running-the-pipeline) to repeat pipeline runs with the same settings without having to write out a command with every single parameter.

:::tip
If you wish to share such profile (such as upload as supplementary material for academic publications), make sure to NOT include cluster specific paths to files, nor institutional specific profiles.
:::

## Core Nextflow arguments

:::note
These options are part of Nextflow and use a _single_ hyphen (pipeline parameters use a double-hyphen).
:::

### `-profile`

Use this parameter to choose a configuration profile. Profiles can give configuration presets for different compute environments.

Several generic profiles are bundled with the pipeline which instruct the pipeline to use software packaged using different methods (Docker, Singularity, Podman, Shifter, Charliecloud, Apptainer, Conda) - see below.

:::info
We highly recommend the use of Docker or Singularity containers for full pipeline reproducibility, however when this is not possible, Conda is also supported.
:::

The pipeline also dynamically loads configurations from [https://github.com/nf-core/configs](https://github.com/nf-core/configs) when it runs, making multiple config profiles for various institutional clusters available at run time. For more information and to see if your system is available in these configs please see the [nf-core/configs documentation](https://github.com/nf-core/configs#documentation).

Note that multiple profiles can be loaded, for example: `-profile test,docker` - the order of arguments is important!
They are loaded in sequence, so later profiles can overwrite earlier profiles.

If `-profile` is not specified, the pipeline will run locally and expect all software to be installed and available on the `PATH`. This is _not_ recommended, since it can lead to different results on different machines dependent on the computer enviroment.

- `test`
  - A profile with a complete configuration for automated testing
  - Includes links to test data so needs no other parameters
- `docker`
  - A generic configuration profile to be used with [Docker](https://docker.com/)
- `singularity`
  - A generic configuration profile to be used with [Singularity](https://sylabs.io/docs/)
- `podman`
  - A generic configuration profile to be used with [Podman](https://podman.io/)
- `shifter`
  - A generic configuration profile to be used with [Shifter](https://nersc.gitlab.io/development/shifter/how-to-use/)
- `charliecloud`
  - A generic configuration profile to be used with [Charliecloud](https://hpc.github.io/charliecloud/)
- `apptainer`
  - A generic configuration profile to be used with [Apptainer](https://apptainer.org/)
- `wave`
  - A generic configuration profile to enable [Wave](https://seqera.io/wave/) containers. Use together with one of the above (requires Nextflow ` 24.03.0-edge` or later).
- `conda`
  - A generic configuration profile to be used with [Conda](https://conda.io/docs/). Please only use Conda as a last resort i.e. when it's not possible to run the pipeline with Docker, Singularity, Podman, Shifter, Charliecloud, or Apptainer.

### `-resume`

Specify this when restarting a pipeline. Nextflow will use cached results from any pipeline steps where the inputs are the same, continuing from where it got to previously. For input to be considered the same, not only the names must be identical but the files' contents as well. For more info about this parameter, see [this blog post](https://www.nextflow.io/blog/2019/demystifying-nextflow-resume.html).

You can also supply a run name to resume a specific run: `-resume [run-name]`. Use the `nextflow log` command to show previous run names.

### `-c`

Specify the path to a specific config file (this is a core Nextflow command). See the [nf-core website documentation](https://nf-co.re/usage/configuration) for more information.

## Custom configuration

### Resource requests

Whilst the default requirements set within the pipeline will hopefully work for most people and with most input data, you may find that you want to customise the compute resources that the pipeline requests. Each step in the pipeline has a default set of requirements for number of CPUs, memory and time. For most of the steps in the pipeline, if the job exits with any of the error codes specified [here](https://github.com/nf-core/rnaseq/blob/4c27ef5610c87db00c3c5a3eed10b1d161abf575/conf/base.config#L18) it will automatically be resubmitted with higher requests (2 x original, then 3 x original). If it still fails after the third attempt then the pipeline execution is stopped.

To change the resource requests, please see the [max resources](https://nf-co.re/docs/usage/configuration#max-resources) and [tuning workflow resources](https://nf-co.re/docs/usage/configuration#tuning-workflow-resources) section of the nf-core website.

### Custom Containers

In some cases you may wish to change which container or conda environment a step of the pipeline uses for a particular tool. By default nf-core pipelines use containers and software from the [biocontainers](https://biocontainers.pro/) or [bioconda](https://bioconda.github.io/) projects. However in some cases the pipeline specified version maybe out of date.

To use a different container from the default container or conda environment specified in a pipeline, please see the [updating tool versions](https://nf-co.re/docs/usage/configuration#updating-tool-versions) section of the nf-core website.

### Custom Tool Arguments

A pipeline might not always support every possible argument or option of a particular tool used in pipeline. Fortunately, nf-core pipelines provide some freedom to users to insert additional parameters that the pipeline does not include by default.

To learn how to provide additional arguments to a particular tool of the pipeline, please see the [customising tool arguments](https://nf-co.re/docs/usage/configuration#customising-tool-arguments) section of the nf-core website.

### nf-core/configs

In most cases, you will only need to create a custom config as a one-off but if you and others within your organisation are likely to be running nf-core pipelines regularly and need to use the same settings regularly it may be a good idea to request that your custom config file is uploaded to the `nf-core/configs` git repository. Before you do this please can you test that the config file works with your pipeline of choice using the `-c` parameter. You can then create a pull request to the `nf-core/configs` repository with the addition of your config file, associated documentation file (see examples in [`nf-core/configs/docs`](https://github.com/nf-core/configs/tree/master/docs)), and amending [`nfcore_custom.config`](https://github.com/nf-core/configs/blob/master/nfcore_custom.config) to include your custom profile.

See the main [Nextflow documentation](https://www.nextflow.io/docs/latest/config.html) for more information about creating your own configuration files.

If you have any questions or issues please send us a message on [Slack](https://nf-co.re/join/slack) on the [`#configs` channel](https://nfcore.slack.com/channels/configs).

## Azure Resource Requests

To be used with the `azurebatch` profile by specifying the `-profile azurebatch`.
We recommend providing a compute `params.vm_type` of `Standard_D16_v3` VMs by default but these options can be changed if required.

Note that the choice of VM size depends on your quota and the overall workload during the analysis.
For a thorough list, please refer the [Azure Sizes for virtual machines in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes).

## Running in the background

Nextflow handles job submissions and supervises the running jobs. The Nextflow process must run until the pipeline is finished.

The Nextflow `-bg` flag launches Nextflow in the background, detached from your terminal so that the workflow does not stop if you log out of your session. The logs are saved to a file.

Alternatively, you can use `screen` / `tmux` or similar tool to create a detached session which you can log back into at a later time.
Some HPC setups also allow you to run nextflow within a cluster job submitted your job scheduler (from where it submits more jobs).

## Nextflow memory requirements

In some cases, the Nextflow Java virtual machines can start to request a large amount of memory.
We recommend adding the following line to your environment to limit this (typically in `~/.bashrc` or `~./bash_profile`):

```bash
NXF_OPTS='-Xms1g -Xmx4g'
```
