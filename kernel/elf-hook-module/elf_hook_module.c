#include <linux/module.h> 		/* Needed by all modules */
#include <linux/init.h>			/* Needed for the macros */
#include <linux/kernel.h>		/* Needed for KERN_INFO */
#include <linux/elf.h>			/* Needed for elf_shdr */

/* extern system call declaration */
extern void (*elf_hook_module) (void * args);

/***
 * Helper functions to read elf_shdr
 * Provided by wiki.osdev.org
 */
static struct elf_shdr *elf_sheader(struct elfhdr *hdr) {
	return (struct elf_shdr *)((int)hdr + hdr->e_shoff);
}

static struct elf_shdr *elf_section(struct elfhdr *hdr, int idx) {
	return &elf_sheader(hdr)[idx];
}

static char *elf_str_table(struct elfhdr *hdr) {
	if (hdr->e_shstrndx == SHN_UNDEF) return NULL;
	return (char *)hdr + elf_section (hdr, hdr->e_shstrndx)->sh_offset;
}

static char *elf_lookup_string(struct elfhdr *hdr, int offset) {
	char *strtab = elf_str_table(hdr);
	if (strtab == NULL) return NULL;
	return strtab + offset;
}

/***
 * Handling struct elf_shdr
 */
void handle_elf_hook(struct elfhdr elf_ex, struct elf_shdr *elf_spnt) {
 	printk(KERN_INFO " <rt_module> Call read_elf_hook.\n");

	char * section_name = elf_lookup_string(&(elf_ex), elf_spnt->sh_offset);
	if (section_name != NULL)
		printk(KERN_INFO " <rt_module> Read section %s.\n", section_name); 
	else
		printk(KERN_INFO " <rt_module> Error handle_elf_hook.\n");
	/* add additional functionality */
}

/***
 * Initialize kernel module()...
 * Provided by Sarah Diesburg, Florida State University
 */
static int __init initialization_routine(void) {
	printk(KERN_INFO " <rt_module> Load module.\n");

	/* call local handle_elf_book */	
	elf_hook_module=&(handle_elf_hook);	
	return 0;
}


/***
 * Remove kernel module()...
 */
static void __exit cleanup_routine(void) {	
	printk (KERN_INFO " <rt_moduel> Remove module.\n");
	elf_hook_module=NULL;
}

module_init(initialization_routine);
module_exit(cleanup_routine);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Leo Tomatsu");
MODULE_DESCRIPTION("CS591 Cyber Physical Systems");
