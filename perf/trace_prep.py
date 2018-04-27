'''
Not optomized, but it works
file_dir is the path to the directory your log file is stored in
file_name is the expected name of the file(s)
This script assumes that they are numbered from 1 to n, following this format: file_dir/file_name1.txt
'''

import pandas as pd
import os

# defaults
num_logs = 5
file_dir = 'non-rt-perf/'
file_name= 'non-tr-log'
# for now, we are going to use python to write to the refined area until further expansion/development
#intermediate_zone= 'intermediate'
refined_zone = 'refined'

# Create intermediate and final data destinations
'''
if not os.path.exists(intermediate_zone):
	os.makedirs(intermediate_zone)
'''

if not os.path.exists(refined_zone):
	os.makedirs(refined_zone)

# create intermediate data
for i in range(1, num_logs + 1):
	refined_file = '%s/refined_non-rt-log%d.csv' % (refined_zone, i)
	
	outfile = open(refined_file, "w")
	file_path = file_dir + file_name + str(i) + '.txt'
	infile = open(file_path, 'r')
	lines = infile.readlines()
	print 'now refining: %s' % file_path

	# set up headers
	outfile.write("overhead\tpreempted_process\tprocess_id\tsched_status\tpreempting_process\tprocess_id\n")
	for line in lines[11: -5]:
		finalized_line = ''
	
		# parse each line
		vals = line.split()
		for val in vals:
			if val != '==>':
				if ':' in val:
					process = val.split(':')
					finalized_line = finalized_line + '\t'
					for pval in process[0:-1]:
						finalized_line = finalized_line + pval.strip()

					finalized_line = finalized_line + '\t' + process[-1].strip()
				elif '[' and ']' in val:
					finalized_line = finalized_line + '\t' + val[1:-1].strip()
				else:
					finalized_line = finalized_line + '\t' + val.strip()

		outfile.write(finalized_line + '\n')

	print 'Done'
	outfile.close()
	infile.close()
