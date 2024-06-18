
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'split_fastq': NextflowParameter(
        type=typing.Optional[int],
        default=50000000,
        section_title=None,
        description=None,
    ),
    'step': NextflowParameter(
        type=typing.Optional[str],
        default='mapping',
        section_title=None,
        description='Starting step',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'save_mapped': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save mapped files.',
    ),
    'save_bam_mapped': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save mapped BAMs.',
    ),
    'save_output_as_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Saves output from Markduplicates & Baserecalibration as BAM file instead of CRAM',
    ),
    'rna': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='True if there are RNA samples to be analysed',
    ),
    'dna': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='True if there are DNA samples to be analysed',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default='GRCh38',
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'hisat2_index': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to STAR index folder or compressed file (tar.gz)',
    ),
    'splicesites': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Splice sites file required for HISAT2.',
    ),
    'star_index': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to STAR index folder or compressed file (tar.gz)',
    ),
    'star_twopass': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Enable STAR 2-pass mapping mode.',
    ),
    'star_ignore_sjdbgtf': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Do not use GTF file during STAR index buidling step',
    ),
    'star_max_memory_bamsort': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Option to limit RAM when sorting BAM file. Value to be specified in bytes. If 0, will be set to the genome index size.',
    ),
    'star_bins_bamsort': NextflowParameter(
        type=typing.Optional[int],
        default=50,
        section_title=None,
        description='Specifies the number of genome bins for coordinate-sorting',
    ),
    'star_max_collapsed_junc': NextflowParameter(
        type=typing.Optional[int],
        default=1000000,
        section_title=None,
        description='Specifies the maximum number of collapsed junctions',
    ),
    'read_length': NextflowParameter(
        type=typing.Optional[float],
        default=76.0,
        section_title=None,
        description='Read length',
    ),
    'nucleotides_per_second': NextflowParameter(
        type=typing.Optional[float],
        default=200000.0,
        section_title=None,
        description='Estimate interval size.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'fasta_fai': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to FASTA reference index.',
    ),
    'known_snps': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='If you use AWS iGenomes, this has already been set for you appropriately.\n\nPath to known snps file.',
    ),
    'known_snps_tbi': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to known snps file snps.',
    ),
    'save_reference': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save built references.',
    ),
    'build_only_index': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Only built references.',
    ),
    'download_cache': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Download annotation cache.',
    ),
    'hisat2_build_memory': NextflowParameter(
        type=typing.Optional[str],
        default='200.GB',
        section_title=None,
        description='Minimum memory required to use splice sites and exons in the HiSAT2 index build process.',
    ),
    'gtf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to GTF annotation file.',
    ),
    'gff': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to GFF3 annotation file.',
    ),
    'exon_bed': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to BED file containing exon intervals. This will be created from the GTF file if not specified.',
    ),
    'trim_fastq': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='FASTQ Preprocessing',
        description='Run FastP for read trimming',
    ),
    'tools': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Pipeline stage options',
        description='Tools to use for variant calling and/or for annotation.',
    ),
    'skip_tools': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Disable specified tools.',
    ),
    'wes': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Enable when exome or panel data is provided.',
    ),
    'aligner': NextflowParameter(
        type=typing.Optional[str],
        default='bwa-mem',
        section_title='Alignment options',
        description='Specify aligner to be used to map reads to reference genome.',
    ),
    'save_unaligned': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Where possible, save unaligned reads from aligner to the results directory.',
    ),
    'save_align_intermeds': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the intermediate BAM files from the alignment step.',
    ),
    'bam_csi_index': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Create a CSI index for BAM files instead of the traditional BAI index. This will be required for genomes with larger chromosome sizes.',
    ),
    'remove_duplicates': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title='Variant calling',
        description=None,
    ),
    'no_intervals': NextflowParameter(
        type=typing.Optional[bool],
        default=False,
        section_title=None,
        description=None,
    ),
    'intervals': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to target bed file in case of whole exome or targeted sequencing or intervals file.',
    ),
    'gatk_interval_scatter_count': NextflowParameter(
        type=typing.Optional[int],
        default=25,
        section_title=None,
        description=None,
    ),
    'joint_mutect2': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Runs Mutect2 in joint (multi-sample) mode for better concordance among variant calls of tumor samples from the same patient. Mutect2 outputs will be stored in a subfolder named with patient ID under `variant_calling/mutect2/` folder. Only a single normal sample per patient is allowed. Tumor-only mode is also supported.',
    ),
    'genesplicer': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Annotation',
        description='Enable the use of the VEP genesplicer plugin.',
    ),
    'whitelist': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to BED file with variants to whitelist during filtering',
    ),
    'blacklist': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to BED file with positions to blacklist during filtering (e.g. regions difficult to map)',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

