

.. image:: https://badge.fury.io/py/sequana-pipetools.svg
    :target: https://pypi.python.org/pypi/sequana_pipetools

.. image:: https://github.com/sequana/sequana_pipetools/actions/workflows/main.yml/badge.svg?branch=main
    :target: https://github.com/sequana/sequana_pipetools/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/sequana/sequana_pipetools/badge.svg?branch=main
    :target: https://coveralls.io/github/sequana/sequana_pipetools?branch=main

.. image:: https://readthedocs.org/projects/sequana-pipetools/badge/?version=latest
    :target: https://sequana-pipetools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://app.codacy.com/project/badge/Grade/9031e4e4213e4e57a876fd5b792b5003
   :target: https://app.codacy.com/gh/sequana/sequana_pipetools/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI

:Overview: A set of tools to help building or using Sequana pipelines
:Status: Production
:Issues: Please fill a report on `github <https://github.com/sequana/sequana/issues>`__
:Python version: Python 3.8, 3.9, 3.10
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352,  `JOSS DOI doi:10.21105/joss.00352 <http://www.doi2bib.org/bib/10.21105%2Fjoss.00352>`_


What is sequana_pipetools ?
============================

**sequana_pipetools** is a collection of tools that assists with the management of `Sequana <https://sequana.readthedocs.io>`_ pipelines, which includes next-generation sequencing (NGS) pipelines like RNA-seq, variant calling, ChIP-seq, and others.

The aim of this package is to simplify the deployment of `Sequana pipelines <https://sequana.readthedocs.io>`_ by
creatin a pure Python library that includse commonly used tools for different pipelines.

Previously, the Sequana framework incorporated alll bioinformatics, Snakemake rules,
pipelines, and pipeline management tools into a single library (Sequana) as illustrated
in **Fig 1** below.

.. figure:: https://raw.githubusercontent.com/sequana/sequana_pipetools/main/doc/veryold.png
    :scale: 40%

    **Figure 1** Old Sequana framework will all pipelines and Sequana library in the same
    place including pipetools (this library).

Whenever changes were made to the Sequana library, a thorough check of the entire library was necessary, despite
having 80% test coverage. Adding new pipelines also necessitated the addition of new dependencies, and the process was becoming increasingly complex. To mitigate this issue, we initially made all pipelines independent, as illustrated in **Fig. 2**. This way, pipeline changes could be made without updating Sequana and vice versa, which was a significant improvment.

.. figure:: https://raw.githubusercontent.com/sequana/sequana_pipetools/main/doc/old.png
    :scale: 40%

    **Figure 2** v0.8 of Sequana moved the Snakemake pipelines in indepdendent
    repositories. A `cookie cutter <https://github.com/sequana/sequana_pipeline_template>`_ 
    ease the creation of scuh pipelines


However, certain tools, such as those used for user interface and input data sanity checks, were required by all pipelines, as depicted by the pipetools box in the figure. As new pipelines were being added every month, we aimed to make the pipelines and Sequana more modular. Consequently, we created a pure Python library known as **sequana_pipetools**, as shown in **Fig. 3**, to make the pipelines even more autonomous.

.. figure:: https://raw.githubusercontent.com/sequana/sequana_pipetools/main/doc/new.png
    :scale: 40%

    **Figure 3** New Sequana framework. The library contains the core and
    bioinformatics tools and is now distinct from  the pipelines. Additionally, the
    sequana_pipetools library supplies common tools to assist in the creaton and management of all pipelines, 
    such as shared parser for options.

Finally, we dropped the rules/ available in Sequana to build an independent package with a set of Snakemake
wrappers. These wrappers are available on https://github.com/sequana/sequana-wrappers and have also the advantage of being tested through continuous integration.

.. figure:: https://raw.githubusercontent.com/sequana/sequana_pipetools/main/doc/wrappers.png
    :scale: 40%

    **Figure 3** New Sequana framework 2021. The library itself with the core, the
    bioinformatics tools is now fully independent of the pipelines. 


Installation
============

from pypi website::

    pip install sequana_pipetools

No dependencies for this package except Python itself. In practice, this package
has no interest if not used with a Sequana pipeline. So, when using it,
you will need to install the relevant Sequana pipelines that you wish to use. For example::

    pip install sequana_rnaseq
    pip install sequana_fastqc
    ...


This package is for `Sequana <https://sequana.readthedocs.io>`_ developers.
To get more help, go to the doc directory and build the local sphinx directory using::

    make html
    browse build/html/index.html

Quick tour
==========

There are currently two standalone tools. The first one is for Linux users under
bash to obtain completion of a sequana pipeline command line arguments::

    sequana_completion --name fastqc

The second is used to introspect slurm files to get a summary of the SLURM log
files::

    sequana_slurm_status --directory .

Will print a short summary report with common errors (if any).


The library is intended to help Sequana developers to design their pipelines.
See the `Sequana organization repository for examples <https://github.com/sequana>`_.

In addition to those standalones, sequana_pipetools goal is to provide utilities to help Sequana developers. 
We currently provide a set of Options classes that should be used to
design the API of your pipelines. For example, the
sequana_pipetools.options.SlurmOptions can be used as follows inside a standard
Python module (the last two lines is where the magic happens)::

    import argparse
    from sequana_pipetools.options import *
    from sequana_pipetools.misc import Colors
    from sequana_pipetools.info import sequana_epilog, sequana_prolog

    col = Colors()
    NAME = "fastqc"

    class Options(argparse.ArgumentParser):
        def __init__(self, prog=NAME, epilog=None):
            usage = col.purple(sequana_prolog.format(**{"name": NAME}))
            super(Options, self).__init__(usage=usage, prog=prog, description="",
                epilog=epilog,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
            # add a new group of options to the parser
            so = SlurmOptions()
            so.add_options(self)


Developers should look at e.g. module sequana_pipetools.options
for the API reference and one of the official sequana pipeline (e.g.,
https://github.com/sequana/sequana_variant_calling) to get help from examples.

The Options classes provided can be used and combined to design pipelines. 


How to create skeleton of a Sequana pipeline with cookiecutter
=================================================================

In version 0.11 and below, there was a standalone called **sequana_start_pipeline** that would help you to automatically create the structure of a Sequana pipeline. This stadanlone was dropped in version 0.11.1

Since it is based on cookiecutter, it is quite easy to do it yourself as follows::

    pip install cookiecuter
    cookiecutter https://github.com/sequana/sequana_pipeline_template -o . --overwrite-if-exists

and then follow the instructions. You will be asked some questions such as the name of your pipeline (eg. variant), a description, keywords and the *project_slug* (just press enter).


Setting up and Running Sequana pipelines
=========================================


When you execute a sequana pipeline, e.g.::

    sequana_fastqc --input-directory data

a working directory is created (with the name of the pipeline; here fastqc). Moreover, the working directory
contains a shell script that will hide the snakemake command. This snakemake command with make use
of the sequana wrappers and will use the official sequana github repository by default
(https://github.com/sequana/sequana-wrappers). This may be overwritten. For instance, you may use a local clone. To do
so, you will need to create an environment variable::

    export SEQUANA_WRAPPERS="git+file:///home/user/github/sequana-wrappers

If you decide to use singularity/apptainer, one common error on a cluster is that non-standard paths are not found. You can bind them using the -B option but a more general set up is to create thos environment variable::

    export SINGULARITY_BINDPATH="  /path_to_bind"

for Singularity setup, or ::

    export APPTAINER_BINDPATH=" /path_to_bind"

for Apptainer setup.


What is Sequana ?
=================

**Sequana** is a versatile tool that provides 

#. A Python library dedicated to NGS analysis (e.g., tools to visualise standard NGS formats).
#. A set of Pipelines dedicated to NGS in the form of Snakefiles
   (Makefile-like with Python syntax based on snakemake framework) with more
   than 80 re-usable rules.
#. Standalone applications.

See the `sequana home page <https://sequana.readthedocs.io>`_ for details.


To join the project, please let us know on `github <https://github.com/sequana/sequana/issues/306>`_.



Changelog
=========

========= ======================================================================
Version   Description
========= ======================================================================
0.12.0    * factorise hash function to have url2hash easily accessible
          * Use pth file to retrieve data dir in editable mode
          * remove harcoded bind path for apptainer. Uses env variable instead
          * Fixes singularity-prefix path in shell script if not absolute
0.11.1    * fix regression, add codacy badge, applied black, remove 
            init_pipeline deprecated function.
0.11.0    * More robust code to check pip executable. 
0.10.2    * Fixes https://github.com/sequana/sequana_pipetools/issues/49
            that properly sets the apptainer prefix in defualt mode
0.10.1    * any python module can implement a Sequana pipeline.
0.10.0    * incorporate the sequana_start_template from sequana and refactorise
            the scripts into scripts/
0.9.6     * hotfix on apptainer to be back compatible if no apptainers section
            is found in the config file.
0.9.5     * replaced singularity word by apptainer (--use-aptainer instead of 
            --use-singularity)
0.9.4     * If timeout occurs while singularity is downloaded, catch the error
            remove truncated file.
0.9.3     * hotfix missing import when checking sequana version
          * add config2schema utility function for developers
0.9.2     * Udate asynchronous downloads to use aiohttp
0.9.1     * Ability to download automatically singularity images (as URLs) if 
            set in the  pipelines (container field). add the --use-singularity
            option in all pipelines (and --singualrity-prefix)
0.9.0     * **MAJOR update/Aug 2022**
          * new mechanism to handle  profile for Snakemake that will replace the
            cluster_config.yaml files
          * Major cleanup of PipelineManager (PipelineManagerGeneric was
            removed). The way input files are handled was also cleanup.
            Fixes https://github.com/sequana/sequana_pipetools/issues/37
            and also files starting with common prefixes
0.8.1     * Better schema validation
0.8.0     * removed 'required_binaries' attribute in module.py (not used)
          * removed 'copy_requirements' in sequana_config and fixed the one
            in the sequana_manager
          * switch from distutils to packaging
          * More tests reaching >90%
0.7.6     * simplify the setup() method in pipeline manager
0.7.5     * can set a SEQUANA_WRAPPERS env variable to use local wrappers
0.7.4     * switch biomics to biomicspole for the slurm queue (internal change)
0.7.3     * add schema pipeline manager directory & fix attrdict error with yaml 
0.7.2     * allows pipeline and rules to have the same name
0.7.1     * Fix the --from-project option
0.7.0     * Set the --wrapper-prefix to point to the  sequana-wrappers github
0.6.3     * Fix SequanaConfig file
0.6.2     * Fix script creation to include wrapper and take new snakemake 
            syntax into account
0.6.1     * update schema handling
0.6.0     * Move all modules related to pipelines rom sequana into 
            sequana_pipetools; This release should now be the entry point for 
            all Sequana pipelines (no need to import sequana itself).
0.5.3     * feature removed in sequana to deal with adapter removal and
            changes updated in the package (removed the 'design' option 
            from the cutadapt rules and needed)
          * Improve TrimmingOptions to provide specific list of tools 
            and a default trimming tool
0.5.2     * add TrimmingOptions class intended at replacing CutadaptOptions
          * to avoid extra spaces, add '-o nospace' in all completion files
0.5.1     * fix typo
0.5.0     * add new module called error to be added in onerror sections of all
            pipelines. Usual test update. Pin to stable version
0.4.3     * add MANIFEST to include missing requirements.txt
0.4.2     * add FeatureCounts options
0.4.1     * add slurm status utility (sequana_slurm_status)
0.4.0     * stable version
0.3.1     * comment the prin_newest_version, which is too slow
0.3.0     * stable release
0.2.6     * previous new feature led to overhead of a few seconds with --help
            in this version, we include it only when using --version
0.2.5     * include newest_version feature
0.2.4     * completion can now handle multiple directories/files properly 
          * better doc and more tests
0.2.3     * fix completion to avoir 2 scripts to overwrite each other
0.2.2     * add a deprecated warning + before_pipeline function
0.2.1     * add --from-project option to import existing config file
          * remove --paired-data option
0.2.0     add content from sequana.pipeline_common to handle all kind of 
          options in the argparse of all pipelines. This is independent of 
          sequana to speed up the --version and --help calls
0.1.2     add version of the pipeline in the output completion file 
0.1.1     release bug fix
0.1.0     creation of the package
========= ======================================================================
