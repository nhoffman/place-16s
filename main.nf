seqs = Channel.fromPath('testfiles/seqs.fasta')
refpkg = 'testfiles/bei-hm27-plus-1.0.refpkg/'

process taxon_file {
    container 'taxtastic:0.8.11'

    label 'med_cpu_mem'

    input:
        file('taxtable.csv') from file(refpkg + 'taxtable.csv')
        file('seq_info.csv') from file(refpkg + 'lonelyfilled.seqinfo.csv')

    output:
        // value channel - https://www.nextflow.io/docs/latest/channel.html#value-channel
        file('ref_taxonomy.txt') into ref_taxonomy

    """
    taxit lineage_table --taxonomy-table ref_taxonomy.txt taxtable.csv seq_info.csv
    """
}

process cmalign {
    label 'med_cpu_mem'

    input:
        file('seqs.fasta') from seqs
        file('RRNA_16S_BACTERIA.cm') from file(refpkg + 'RRNA_16S_BACTERIA.cm')

    output:
        file('alignment.sto') into alignment

    """
    cmalign --cpu 8 --dnaout --noprob -o alignment.sto RRNA_16S_BACTERIA.cm seqs.fasta
    """
}

process merge {
    label 'med_cpu_mem'

    input:
        file('alignment.sto') from alignment
        file('refpkg.sto') from file(refpkg + 'alignment.sto')

    output:
        tuple file('query.fa'), file('refalign.fa') into merged

    """
    merge.py --binary esl-alimerge refpkg.sto alignment.sto refalign.fa query.fa
    """
}

process get_model_descriptor {
    label 'med_cpu_mem'

    input:
        file('tree_raxml.stats') from file(refpkg + 'tree_raxml.stats')

    output:
        stdout model_descriptor

    """
    get_model_descriptor.py tree_raxml.stats
    """
}

process epa {
    container 'epa-ng:v0.3.6'

    label 'med_cpu_mem'

    input:
        tuple file('query.fa'), file('refalign.fa') from merged
        file('tree.txt') from file(refpkg + 'tree_raxml.tre')
        file('tree_raxml.stats') from file(refpkg + 'tree_raxml.stats')
        val model from model_descriptor.trim()

    output:
        file('epa_result.jplace') into placements

    """
    epa-ng --model ${model} --query query.fa --ref-msa refalign.fa --tree tree.txt
    """
}

process gappa {
    container 'gappa:v0.6.0'

    label 'med_cpu_mem'

    input:
        file('epa_result.jplace') from placements
        file('ref_taxonomy.txt') from ref_taxonomy

    output:
        file('per_query.tsv') into per_query

    """
    gappa examine assign --jplace-path epa_result.jplace --out-dir . --taxon-file ref_taxonomy.txt
    """
}

process get_classifications {
    label 'med_cpu_mem'

    input:
        file('per_query.tsv') from per_query

    output:
        file('classifications.csv')
        file('lineages.csv')

    publishDir params.output, overwrite: true

    """
    get_classifications.py --classifications classifications.csv --lineages lineages.csv --min-afract 0.30 --min-total 0.45 per_query.tsv
    """
}
