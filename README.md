# CheckMateCalculations
Repository for CheckMate related stuff for Master thesis

#### Author: Rafal Maselek
#### email: rafalmaselek@gmail.com

## 1) auto_checkmate.sh

**auto_checkmate.sh** is a bash script that enables running CheckMATE with SUSYHit for many SLHA file with a single command.

#### 0. Prerequisites
**auto_checkmate.sh** requires bash console and the following software:

* CheckMATE2; available at https://checkmate.hepforge.org

* SUSYHit; located in res/ folder. To install SUSYHit, extract the archive and build the programme using the `make` command.

#### 1. Installation:
**auto_checkmate** is a single-file bash scripts and does not require any installation. However user have to specify some parameters:

* path to CheckMATE executable (variable CHECKMATE)

* path to SUSYHit executable (variable SUSYHIT)

**NOTE:** In order not to change above paths after upgrading to a newer version of the script, there is a possibility to use an external file with paths to executables. That file will not be overwritten after pulling a new version from GitHub. The file should be located in the same directory as auto_checkmate.sh script and should be named *input_paths.txt*. It should contain two lines with two absolute paths to CheckMATE and SUSYHit accordingly.

User have to also specify CheckMATE parameters or use the default ones. All CheckMATE parameters can be set by modifying the variable
definitions at the beginning of the script. The meaning of those parameters can be found in CheckMATE article:  https://arxiv.org/pdf/1611.09856.pdf

#### 2. Runnning:
There are two running modes for the script:

* The first one allows to run CheckMATE for a single SLHA file:
`./auto_checkmate.sh name_of_SLHA_file.slha`

* The second mode allows user to run CheckMATE for many SLHA files by providing a text file with names of SLHA files, one name per row. 
`./auto_checkmate.sh name_of_list_file.txt`  
Such file looks in a following way:  

> file1.slha  
> file2.slha  
> file3

**NOTE:** The extension is non-mandatory.  
**NOTE2:** Leading/following white spaces are truncated.

#### 3. Folder hierarchy:
User can specify output directory by variable called *OUTDIR*. The default behavior in many-files mode is to create a subdirectory named after the name of the list file, and in it subdirectories named after natural numbers. One subdirectory for each execution of CheckMATE.  
The folder hierarchy looks then as follows:
```
.
└── slha_list
    ├── 1
        ├── best_signal_regions.txt
        ├── pythia_process.log
        ├── result.txt
        └── total_results.txt
    ├── 2
        ├── best_signal_regions.txt
        ├── pythia_process.log
        ├── result.txt
        └── total_results.txt
```
It might be useful to use SLHA files' names to label subdirectories instead of using numbers. It can be enabled by setting `USE_FILE_NAMES='true'` at the very top of the script.  The folder hierarchy looks then as follows:  
```
.
└── slha_list
    ├── file1
        ├── best_signal_regions.txt
        ├── pythia_process.log
        ├── result.txt
        └── total_results.txt
    ├── file2
        ├── best_signal_regions.txt
        ├── pythia_process.log
        ├── result.txt
        └── total_results.txt
```

#### 4. Output:
Each output directory contains four files:
* pythia_process.log -- logs of pythia with cross-sections
* result.txt --final result of CheckMATE
* total_results.txt -- detailed results for each of the signal regions
* best_signal_regions.txt -- can be used to establish which signal regions are the best for theory testing