from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], save_mapped: typing.Optional[bool], save_bam_mapped: typing.Optional[bool], save_output_as_bam: typing.Optional[bool], hisat2_index: typing.Optional[str], splicesites: typing.Optional[LatchFile], star_index: typing.Optional[str], star_twopass: typing.Optional[bool], star_ignore_sjdbgtf: typing.Optional[bool], fasta: typing.Optional[LatchFile], fasta_fai: typing.Optional[str], known_snps: typing.Optional[str], known_snps_tbi: typing.Optional[str], save_reference: typing.Optional[bool], build_only_index: typing.Optional[bool], download_cache: typing.Optional[bool], gtf: typing.Optional[str], gff: typing.Optional[str], exon_bed: typing.Optional[str], trim_fastq: typing.Optional[bool], tools: typing.Optional[str], skip_tools: typing.Optional[str], wes: typing.Optional[bool], save_unaligned: typing.Optional[bool], save_align_intermeds: typing.Optional[bool], bam_csi_index: typing.Optional[bool], intervals: typing.Optional[str], joint_mutect2: typing.Optional[bool], genesplicer: typing.Optional[bool], whitelist: typing.Optional[str], blacklist: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], split_fastq: typing.Optional[int], step: typing.Optional[str], rna: typing.Optional[bool], dna: typing.Optional[bool], genome: typing.Optional[str], star_max_memory_bamsort: typing.Optional[int], star_bins_bamsort: typing.Optional[int], star_max_collapsed_junc: typing.Optional[int], read_length: typing.Optional[float], nucleotides_per_second: typing.Optional[float], hisat2_build_memory: typing.Optional[str], aligner: typing.Optional[str], remove_duplicates: typing.Optional[bool], no_intervals: typing.Optional[bool], gatk_interval_scatter_count: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('split_fastq', split_fastq),
                *get_flag('step', step),
                *get_flag('outdir', outdir),
                *get_flag('save_mapped', save_mapped),
                *get_flag('save_bam_mapped', save_bam_mapped),
                *get_flag('save_output_as_bam', save_output_as_bam),
                *get_flag('rna', rna),
                *get_flag('dna', dna),
                *get_flag('genome', genome),
                *get_flag('hisat2_index', hisat2_index),
                *get_flag('splicesites', splicesites),
                *get_flag('star_index', star_index),
                *get_flag('star_twopass', star_twopass),
                *get_flag('star_ignore_sjdbgtf', star_ignore_sjdbgtf),
                *get_flag('star_max_memory_bamsort', star_max_memory_bamsort),
                *get_flag('star_bins_bamsort', star_bins_bamsort),
                *get_flag('star_max_collapsed_junc', star_max_collapsed_junc),
                *get_flag('read_length', read_length),
                *get_flag('nucleotides_per_second', nucleotides_per_second),
                *get_flag('fasta', fasta),
                *get_flag('fasta_fai', fasta_fai),
                *get_flag('known_snps', known_snps),
                *get_flag('known_snps_tbi', known_snps_tbi),
                *get_flag('save_reference', save_reference),
                *get_flag('build_only_index', build_only_index),
                *get_flag('download_cache', download_cache),
                *get_flag('hisat2_build_memory', hisat2_build_memory),
                *get_flag('gtf', gtf),
                *get_flag('gff', gff),
                *get_flag('exon_bed', exon_bed),
                *get_flag('trim_fastq', trim_fastq),
                *get_flag('tools', tools),
                *get_flag('skip_tools', skip_tools),
                *get_flag('wes', wes),
                *get_flag('aligner', aligner),
                *get_flag('save_unaligned', save_unaligned),
                *get_flag('save_align_intermeds', save_align_intermeds),
                *get_flag('bam_csi_index', bam_csi_index),
                *get_flag('remove_duplicates', remove_duplicates),
                *get_flag('no_intervals', no_intervals),
                *get_flag('intervals', intervals),
                *get_flag('gatk_interval_scatter_count', gatk_interval_scatter_count),
                *get_flag('joint_mutect2', joint_mutect2),
                *get_flag('genesplicer', genesplicer),
                *get_flag('whitelist', whitelist),
                *get_flag('blacklist', blacklist),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_rnadnavar", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_rnadnavar(input: str, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], save_mapped: typing.Optional[bool], save_bam_mapped: typing.Optional[bool], save_output_as_bam: typing.Optional[bool], hisat2_index: typing.Optional[str], splicesites: typing.Optional[LatchFile], star_index: typing.Optional[str], star_twopass: typing.Optional[bool], star_ignore_sjdbgtf: typing.Optional[bool], fasta: typing.Optional[LatchFile], fasta_fai: typing.Optional[str], known_snps: typing.Optional[str], known_snps_tbi: typing.Optional[str], save_reference: typing.Optional[bool], build_only_index: typing.Optional[bool], download_cache: typing.Optional[bool], gtf: typing.Optional[str], gff: typing.Optional[str], exon_bed: typing.Optional[str], trim_fastq: typing.Optional[bool], tools: typing.Optional[str], skip_tools: typing.Optional[str], wes: typing.Optional[bool], save_unaligned: typing.Optional[bool], save_align_intermeds: typing.Optional[bool], bam_csi_index: typing.Optional[bool], intervals: typing.Optional[str], joint_mutect2: typing.Optional[bool], genesplicer: typing.Optional[bool], whitelist: typing.Optional[str], blacklist: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], split_fastq: typing.Optional[int] = 50000000, step: typing.Optional[str] = 'mapping', rna: typing.Optional[bool] = True, dna: typing.Optional[bool] = True, genome: typing.Optional[str] = 'GRCh38', star_max_memory_bamsort: typing.Optional[int] = 0, star_bins_bamsort: typing.Optional[int] = 50, star_max_collapsed_junc: typing.Optional[int] = 1000000, read_length: typing.Optional[float] = 76.0, nucleotides_per_second: typing.Optional[float] = 200000.0, hisat2_build_memory: typing.Optional[str] = '200.GB', aligner: typing.Optional[str] = 'bwa-mem', remove_duplicates: typing.Optional[bool] = False, no_intervals: typing.Optional[bool] = False, gatk_interval_scatter_count: typing.Optional[int] = 25) -> None:
    """
    nf-core/rnadnavar

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, split_fastq=split_fastq, step=step, outdir=outdir, save_mapped=save_mapped, save_bam_mapped=save_bam_mapped, save_output_as_bam=save_output_as_bam, rna=rna, dna=dna, genome=genome, hisat2_index=hisat2_index, splicesites=splicesites, star_index=star_index, star_twopass=star_twopass, star_ignore_sjdbgtf=star_ignore_sjdbgtf, star_max_memory_bamsort=star_max_memory_bamsort, star_bins_bamsort=star_bins_bamsort, star_max_collapsed_junc=star_max_collapsed_junc, read_length=read_length, nucleotides_per_second=nucleotides_per_second, fasta=fasta, fasta_fai=fasta_fai, known_snps=known_snps, known_snps_tbi=known_snps_tbi, save_reference=save_reference, build_only_index=build_only_index, download_cache=download_cache, hisat2_build_memory=hisat2_build_memory, gtf=gtf, gff=gff, exon_bed=exon_bed, trim_fastq=trim_fastq, tools=tools, skip_tools=skip_tools, wes=wes, aligner=aligner, save_unaligned=save_unaligned, save_align_intermeds=save_align_intermeds, bam_csi_index=bam_csi_index, remove_duplicates=remove_duplicates, no_intervals=no_intervals, intervals=intervals, gatk_interval_scatter_count=gatk_interval_scatter_count, joint_mutect2=joint_mutect2, genesplicer=genesplicer, whitelist=whitelist, blacklist=blacklist, email=email, multiqc_title=multiqc_title, multiqc_methods_description=multiqc_methods_description)

