# TODO update file path for rt-kernel
obj-m += elf_hook_module.o

build_module:
	make -C /lib/modules/`uname -r`/build SUBDIRS=$(PWD) modules


load: build_module
	insmod elf_hook_module.ko	

clean:
	make -C /lib/modules/`uname -r`/build SUBDIRS=$(PWD) clean

unload: clean
	rmmod elf_hook_module.ko
