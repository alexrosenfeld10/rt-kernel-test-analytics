#include <linux/module.h> 		/* Needed by all modules */
#include <linux/init.h>			/* Needed for the macros */
#include <linux/kernel.h>		/* Needed for KERN_INFO */

/***
 * Initialize kernel module()...
 */
static int __init initialization_routine(void) {
	printk(KERN_INFO " <rt_module> Load module.\n");
	
	/* add code here */
	
	return 0;
}


/***
 * Remove kernel module()...
 */
static void __exit cleanup_routine(void) {	
	printk (KERN_INFO " <rt_moduel> Remove module.\n");
}

module_init(initialization_routine);
module_exit(cleanup_routine);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Boston University RT-OS Team");
MODULE_DESCRIPTION("cs591 Cyber Physical Systems");