# Modifications

We have modified the kernel to read section headers of ELF files and look for a specific header. If found, the kernel will attempt to run a module that alters program behavior based on the contents of the section header found in the elf file.

Please see binfmt_elf.c for these changes. This file can be found in the linux kernel in the fs/ directory.
