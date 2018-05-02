# TODO update file path for rt-kernel
obj-m += elf_hook_module.o

build_module:
	make ARCH=arm CROSS_COMPILE=/usr/bin/arm-linux-gnueabi- -C /home/whyjun/Documents/GitHub/bb-kernel-src/KERNEL SUBDIRS=$(PWD) modules

load: build_module
	insmod elf_hook_module.ko	

clean:
	make ARCH=arm CROSS_COMPILE=/usr/bin/arm-linux-gnueabi- -C /home/whyjun/Documents/GitHub/bb-kernel-src/KERNEL SUBDIRS=$(PWD) clean

unload: clean
	rmmod elf_hook_module.ko
