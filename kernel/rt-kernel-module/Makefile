# Compile module under Linux 2.6.x using something like:
# make -C /lib/modules/`uname -r`/build SUBDIRS=$(PWD) modules
obj-m += rt_kernel_module.o

build_module:
	make -C /lib/modules/`uname -r`/build SUBDIRS=$(PWD) modules


load: build_module
	insmod rt_kernel_module.ko	

clean:
	make -C /lib/modules/`uname -r`/build SUBDIRS=$(PWD) clean

unload: clean
	rmmod rt_kernel_module.ko
