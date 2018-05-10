# Kernel Modifications

We modified the linux kernel 4.14.35-bone-rt-r13 version released by Robert C Nelson. [link]("https://github.com/RobertCNelson/bb-kernel")

## Modifications

We have modified the kernel to read section headers of ELF files and look for a specific header. If found, the kernel will attempt to run a module that alters program behavior based on the contents of the section header found in the elf file.

Please see kernel_modifications/binfmt_elf.c for these changes. This file can be found in the linux kernel in the fs/ directory.

## How to cross-compile the linux kernel for BeagleBone on Ubuntu 16.04

Due to lack of storage in BeagleBone(ARM), we tried to cross-compile linux kernel on personal laptop(x86). For cross compilation, we need a few basic requirements: ARM Cross Compiler, Linux Kernel, and a set of scripts for rebuilding kernel for BeagleBone.

### ARM Cross Compiler

We used `gcc-arm-linux-gnueabi` to cross-compile the linux kernel. Install GCC cross-compilers by typing:

    $ sudo apt-get install gcc-arm-linux-gnueabi

### Linux Kernel and Build Scripts from bb-kernel repo

We built the kernel for BeagleBone with scripts and patches released by RobertCNelson. [link]("https://github.com/RobertCNelson/bb-kernel/tree/de4996e6e52767400c0f89a4c0f7d53e82199b1e") Because we modified and tested our modification on 4.14.35-bone-rt-r13 version, please checkout to the specific commit after cloning the repo.

    $ git clone -b am33x-rt-v4.14 --single-branch git@github.com:RobertCNelson/bb-kernel.git
    $ cd bb-kernel
    $ git checkout de4996e6e52767400c0f89a4c0f7d53e82199b1e

### Let's compile the kernel

In bb-kernel directory, build the kernel image by typing:

    $ ./build_kernel.sh
Please see deploy directory to find the kernel. If you want to modify the source and rebuild the kernel, please type `./tools/rebuild.sh`.