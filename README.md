# PREEMPT-RT-LINUX

## Kernel Modifications

We modified the linux kernel 4.14.21-bone-rt-r13 version released by Robert C Nelson. [(link)](https://github.com/RobertCNelson/bb-kernel)

## Modifications

We have modified the kernel to read section headers of ELF files and look for a specific header. If found, the kernel will attempt to run a module that alters program behavior based on the contents of the section header found in the elf file.

Please see kernel_modifications/binfmt_elf.c for these changes. This file can be found in the linux kernel in the fs/ directory.

## How to cross-compile the linux kernel for BeagleBone on Ubuntu 16.04

Due to lack of storage in BeagleBone(ARM), we tried to cross-compile linux kernel on personal laptop(x86). For cross compilation, we need a few basic requirements: ARM Cross Compiler, Linux Kernel, and a set of scripts for rebuilding kernel for BeagleBone.

### ARM Cross Compiler

We used `gcc-arm-linux-gnueabi` to cross-compile the linux kernel. Install GCC cross-compilers by typing:
    
    $ sudo apt-get install gcc-arm-linux-gnueabi

### Linux Kernel and Build Scripts from bb-kernel repo

We built the kernel for BeagleBone with scripts and patches released by RobertCNelson. [(link)](https://github.com/RobertCNelson/bb-kernel/tree/de4996e6e52767400c0f89a4c0f7d53e82199b1e) Because we modified and tested our modification on 4.14.21-bone-rt-r13 version, please checkout to the specific commit after cloning the repo.
    
    $ git clone -b am33x-rt-v4.14 --single-branch git@github.com:RobertCNelson/bb-kernel.git
    $ cd bb-kernel
    $ git checkout de4996e6e52767400c0f89a4c0f7d53e82199b1e

### Replace binfmt_elf.c

Please view the kernel/kernel-modifications/binfmt_elf.c file for kernel code changes. Please see binfmt_elf.c for these changes. This file can be found in the linux kernel in the KERNEL/fs/ directory.

### Compile the kernel

In bb-kernel directory, build the kernel image by typing:

    $ ./build_kernel.sh
Please see deploy directory to find the kernel. If you want to modify the source and rebuild the kernel, please type `./tools/rebuild.sh`.

## Configuration
Please give permissions to run the bash script `chmod u+x rt_kernel_analysis.sh`.


## Bash Script
### Usage
`Usage: ./rt_kernel_analysis.sh [-h (help)] [-n program name] [-t type (rt | non-rt)]`
* h flag will echo the Usage string
* n flag will assign the program name to run the rt-kernel analysis
* t flag will assign the type of the kernel to be either rt or non-rt

### What it will run
The following executions will be made:
* Error handle user input and validate if program is in rt-kernel
* ftrace graph
* ftrace functions
* strace table
* strace timestamp
* perf context switching
* perf cache profiling
* python data_reduction.py

The output of each trace function will be output to either non-rt/logfiles or rt/logfiles. The python script will read from those directories and store the created csv files into non-rt/python-output or rt/python-output.

### TODO
1. Get kernel module working with modded kernel.
2. Possibly read data from the python-output file.
3. Incorporate assembly code analysis using `perf annotate --stdio > perf_assembly.txt`

## Python Script
### Adding log files
Please consider if you're kernel is running real-time or non-real-time and push into the respected folder called logfiles

### Creating csv files
After inserting log files into the respected logfiles folder, please run this command:

##### for rt
`python data_reduction.py -i rt/logfiles -s pi_stress -o rt/python-output`

##### for non-rt
`python data_reduction.py -i non-rt/logfiles -s pi_stress -o non-rt/python-output`

The output csv files will be created in the folder python-output

### Future work
* Statistical analysis on data frames created
* Refactor into Object-Orientated Design

### Possible issues
If these issues arise, please notify in github issues or on discord.
* Our strace output file is missing process id
* The timestamp log file may contain errors that the data_reduction.py does not recognize
