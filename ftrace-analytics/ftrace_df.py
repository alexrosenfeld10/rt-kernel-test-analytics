'''
ftrace_df.py

Procedure
1. Cleans the log file created by bash script ftrace
2. Creates a dataframe with the following column names and datatypes:
    * columan name:             Data type
    --------------------------------------
    * task-pid:                 String
    * cpu#:                     String
    * irqs-off:                 Character ['null']
    * need-resched:             Character ['null']
    * need-resched_lazy:        Character ['null']
    * hardirq-softirq:          Character ['null']
    * preempt-depth:            Character ['null']
    * timestamp:                Float
    * parent-process:           String
    * child-process:            String
3. Create output csv file based on the input filename

usage: ftrace_df.py [-f [filenames] [-l [task-pid names to filter]]
example: python ftrace_df.py -f out_pi_stress_0.txt -l ftrace.sh-3764
example output: out_pi_stress_0.csv
'''
import argparse
import pandas as pd

# column names for data frame
header = ['task-pid',
          'cpu#',
          'irqs-off',
          'need-resched',
          'need-resched_lazy',
          'hardirq-softirq',
          'preempt-depth',
          'timestamp',
          'child-process',
          'parent-process']

# list of files to read
list_filenames = []

# list of task names to filter
list_filter = []

# command line parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", action='store', dest='filename',
                    nargs="+", help="Filename of input log file")
parser.add_argument("-l", action='store', dest='list_filter',
                    nargs='+', help="Filter un-wanted tasks-pid")
args = parser.parse_args()
list_filenames = args.filename
if args.list_filter != None:
    list_filter = args.list_filter

# read every file
for filename in list_filenames:
    # column values for data frame
    task_pid  = []
    cpu_num = []
    irq_off = []
    need_resched = []
    need_resched_lazy = []
    hardirq_softirq = []
    preempt_depth = []
    timestamp = []
    child_process = []
    parent_process = []

    function_name = ""
    output_filename = filename[:-4] + ".csv"

    # read filename line by line
    with open(filename) as fp:
        for line_num, l in enumerate(fp):
            # ignoring header lines
            if line_num == 3:
                line = l.split()
                function_name = line[2]
            if function_name == "function":
                if line_num >= 13:
                    line = l.split()
                    # cleaning ftrace line to store in proper column
                    for c, val in enumerate(line):
                        # storing task_pid col
                        if c == 0:
                            if val in list_filter:
                                break
                            task_pid.append(val)
                        # storing cpu# col
                        elif c == 1:
                            str_len = len(val)
                            temp_str = ''
                            for i in range(0, str_len):
                                if val[i] != '[' and val[i] != ']':
                                    temp_str += val[i]
                            cpu_num.append(temp_str)
                        # storing irq_off, need_resched, need_resched_lazy,
                        # hardirq_softirq, and preempt_depth cols
                        elif c == 2:
                            str_len = len(val)
                            for i in range (0, str_len):
                                curr_char = 'null'
                                if val[i] == '.':
                                    curr_char = 'null'
                                else:
                                    curr_char = val[i]
                                if i == 0:
                                    irq_off.append(curr_char)
                                elif i == 1:
                                    need_resched.append(curr_char)
                                elif i == 2:
                                    need_resched_lazy.append(curr_char)
                                elif i == 3:
                                    hardirq_softirq.append(curr_char)
                                elif i == 4:
                                    preempt_depth.append(curr_char)
                        # storing timestamp col
                        elif c == 3:
                            str_len = len(val)
                            temp_str = ''
                            for i in range(0, str_len):
                                if val[i] != ':':
                                    temp_str += val[i]
                            timestamp_val = float(temp_str)
                            timestamp.append(timestamp_val)
                        # storing child_process col
                        elif c == 4:
                            child_process.append(val)
                        # storing parent_process col
                        elif c == 5:
                            val = val.rstrip()
                            str_len = len(val)
                            temp_str = ''
                            for i in range(0, str_len):
                                if val[i] != '<' and val [i] != '-':
                                    temp_str += val[i]
                            parent_process.append(temp_str)
            if function_name == "function_graph":
                print("currently do not have a dataframe for ftrace-function_graph")
                break



    if function_name == "function":
        df = pd.DataFrame({ header[0]: task_pid,
                            header[1]: cpu_num,
                            header[2]: irq_off,
                            header[3]: need_resched,
                            header[4]: need_resched_lazy,
                            header[5]: hardirq_softirq,
                            header[6]: preempt_depth,
                            header[7]: timestamp,
                            header[8]: child_process,
                            header[9]: parent_process})

        df.to_csv(output_filename, sep=',')
        print("created " + output_filename)
