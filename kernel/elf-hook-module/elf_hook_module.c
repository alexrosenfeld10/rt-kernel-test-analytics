#include <linux/module.h> 		/* Needed by all modules */
#include <linux/init.h>			/* Needed for the macros */
#include <linux/kernel.h>		/* Needed for KERN_INFO */
#include <linux/elf.h>			/* Needed for elf_shdr */

/* extern system call declaration */
extern void (*elf_hook_module) (char * args);


void handle_elf_hook(char * args) {
    printk(KERN_INFO "Section contents (from module): %s\n", args);
}

/***
 * Initialize kernel module()...
 * Provided by Sarah Diesburg, Florida State University
 */
static int __init initialization_routine(void) {
	printk(KERN_INFO " <rt_module> Load module.\n");

	/* call local handle_elf_hook */	
	elf_hook_module=&(handle_elf_hook);	
	return 0;
}


/***
 * Remove kernel module()...
 */
static void __exit cleanup_routine(void) {	
	printk (KERN_INFO " <rt_module> Remove module.\n");
	elf_hook_module=NULL;
}

module_init(initialization_routine);
module_exit(cleanup_routine);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Leo Tomatsu");
MODULE_DESCRIPTION("CS591 Cyber Physical Systems");
