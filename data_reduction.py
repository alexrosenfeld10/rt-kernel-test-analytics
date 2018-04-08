'''
ftrace_df.py

Procedure
1. Cleans the log file created by bash script ftrace and strace
2. Creates a dataframe with the column names and datatypes specific to log type
3. Create output csv file based on the input filename

example: python data_reduction.py -i rt/logfile -s pi_stress -o rt/python-output/
example: python data_reduction.py -i non-rt/logfile -s pi_stress -o non-rt/python-output/
'''
import argparse
import pandas as pd
import os
import errno, sys
import glob


'''
Parser - comamnd line parser

@input:  void
@output: String         input_folder    - name of folder containing log files
@output: String[]       search_pid      - names of process ids to filter in
@output: String         output_folder   - name of folder containing output files
'''
def Parser():
    # set up cli
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action='store', dest='input_folder',
                        help="Input folder name")
    parser.add_argument("-s", action='store', dest='search_pid',
                        nargs='+', help="Search task-pid name")
    parser.add_argument("-o", action='store', dest='output_folder',
                        help="Output created csv to folder")

    # store user input
    args = parser.parse_args()

    # error handle and store values
    if args.input_folder == None:
        sys.exit(errno.EACCES)
    else:
        input_folder = args.input_folder

    if args.search_pid == None:
        sys.exit(errno.EACCES)
    else:
        search_pid = args.search_pid

    if args.output_folder == None:
        sys.exit(errno.EACCES)
    else:
        output_folder = args.output_folder

    # return output values
    return input_folder, search_pid, output_folder


'''
PathFinder - determine the output folder

@input:     String      input_filename      - input filename
@input:     String      output_folder       - output folder name
@output:    String      output_filename     - output filename
@output:    String      output_path         - file path to create output file
'''
def PathFinder(input_filename, output_folder):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    input_filename = input_filename.split('/')[-1]
    output_filename = input_filename[:-4] + ".csv"

    # determine output_path
    output_path = fileDir + "/" + output_folder + "/" + output_filename

    return output_filename, output_path


'''
FtraceFunction - read log file, filter process id, and create dataframe

@input:     String      filename    - name of log file
@input:     String[]    search_pid  - list of process ids to filter in
@output:    DataFrame   df          - created dataframe
'''
def FtraceFunction(filename, search_pid):
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

    with open(filename) as fp:
        for line_num, l in enumerate(fp):
            if line_num >= 13:
                line = l.split()
                # cleaning ftrace line to store in proper column
                for c, val in enumerate(line):
                    # storing task_pid col
                    if c == 0:
                        if val[:9] not in search_pid:
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
                            curr_char = ''
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
                # end for loop
        # end for loop
        fp.close()
    #end of fp

    if (len(task_pid) == len(cpu_num) == len(irq_off) ==
        len(need_resched) == len(need_resched_lazy) ==
        len(hardirq_softirq) == len(preempt_depth) ==
        len(timestamp) == len(child_process) == len(parent_process)):
        # create data frame
        df = pd.DataFrame({ header[0]: task_pid,
                            header[1]: cpu_num,
                            header[2]: irq_off,
                            header[3]: need_resched,
                            header[4]: need_resched_lazy,
                            header[5]: hardirq_softirq,
                            header[6]: preempt_depth,
                            header[7]: timestamp,
                            header[8]: child_process,
                            header[9]: parent_process })
        return df
    else:
        print("error")
        sys.exit(0)


'''
StraceTable - read log file, filter process id, and create dataframe

@input:     String      filename    - name of log file
@output:    DataFrame   df          - created dataframe
'''
def StraceTable(filename):
    # column names for data frame
    header = ["time",
              "seconds",
              "usecs/call",
              "calls",
              "errors",
              "syscall"]

    # column values for data frame
    time = []
    seconds = []
    usecs_call = []
    calls = []
    errors = []
    syscall = []

    with open(filename) as fp:
        # cleaning strace line to store in proper column
        for line_num, l in enumerate(fp):
            # skip headers in file
            if line_num >= 2:
                line = l.split()
                # line with end of data
                if line[0] == "------":
                    break
                # line without error value
                if len(line) == 5:
                    for i, val in enumerate(line):
                        if i == 0:
                            time.append(val)
                        elif i == 1:
                            seconds.append(val)
                        elif i == 2:
                            usecs_call.append(val)
                        elif i == 3:
                            calls.append(val)
                        elif i == 4:
                            errors.append(0)
                            syscall.append(val)
                # line with error value
                if len(line) == 6:
                    for i, val in enumerate(line):
                        if i == 0:
                            time.append(val)
                        elif i == 1:
                            seconds.append(val)
                        elif i == 2:
                            usecs_call.append(val)
                        elif i == 3:
                            calls.append(val)
                        elif i == 4:
                            errors.append(val)
                        elif i == 5:
                            syscall.append(val)
        # end of for loop
        fp.close()
    # end of fp

    # create data frame
    if (len(time) == len(seconds) == len(usecs_call) == len(calls) == len(errors) == len(syscall)):
        df = pd.DataFrame({ header[0]: time,
                            header[1]: seconds,
                            header[2]: usecs_call,
                            header[3]: calls,
                            header[4]: errors,
                            header[5]: syscall })
        return df
    else:
        print("error")
        sys.exit(0)


'''
StraceTimestamp - read log file, filter process id, and create dataframe

TODO: fix timestampe pid issue in strace bash script

@input:     String      filename    - name of log file
@output:    DataFrame   df          - created dataframe
'''
def StraceTimestamp(filename):
    pid = []
    process_time = []
    process_name = []
    parameter = []

    header = ["process_time",
              "process_name",
              "parameter"]

    with open(filename) as fp:
        for line_num, l in enumerate(fp):
                line = l.split()
                col = 0
                temp_parameter = ""
                if len(line) == 4:
                    for i, val in enumerate(line):
                        if col == 0:
                            process_time.append(val)
                            col += 1
                        elif col == 1:
                            if temp_parameter == "<...futex":
                                process_name.append("futex")
                                parameter.append("resumed")
                                col += 3
                            if temp_parameter == "<...clock_nanosleep":
                                process_name.append("clock_nanosleep")
                                parameter.append("resumed")
                                col += 3
                            for index, c in enumerate(val):
                                if c != '(' and c != ')':
                                    temp_parameter += c
                                if c == '(':
                                    process_name.append(val[:index])
                                    temp_parameter = temp_parameter[index:]
                                    col += 1
                                if c == ')':
                                    col += 1
                            # end of for loop
                        elif col == 2:
                            if i == len(line) - 1:
                                temp_parameter += val + " "
                                parameter.append(temp_parameter)
                            else:
                                for index, c in enumerate(val):
                                    if c == ')':
                                        val = val[:-1]
                                        col += 1
                            temp_parameter += val + " "
                        elif col == 3:
                            parameter.append(temp_parameter)
                            col += 1
                    # end of for loop

                    # end of for loop
        # end of for loop
        fp.close()
    # end of fp

    # create data frame
    if len(process_time) == len(process_name) == len(parameter):
        df = pd.DataFrame({ header[0]: process_time,
                            header[1]: process_name,
                            header[2]: parameter })
        return df
    else:
        print("error")
        sys.exit(0)


'''
LogType - return the log type

@input:     String      filename        - name of the log file to check
@output:    String      function_name   - the type of the log file
'''
def LogType(filename):
    function_name = ""

    with open(filename) as fp:
        for line_num, l in enumerate(fp):
            # strace_table identifier
            if line_num == 0:
                line = l.split()
                if line[0] == '%':
                    function_name = "strace_table"
            # ftrace identifier
            if line_num == 3:
                line = l.split()
                temp = line[2]
                if temp == 'function':
                    function_name = "ftrace_function"
                elif temp == 'function_graph':
                    function_name = "ftrace_graph"
                if function_name == '':
                    function_name = "strace_timestamp"
        # end of for loop
        fp.close()
    #end of fp

    return function_name


'''
Main - parse input, determine log type, create data frame, create csv

TODO: statistical data analysis using pandas

@input: void
@output: void
'''
def main():

    # command line parser
    input_folder, search_pid, output_folder = Parser()

    # open folder to read file
    for filename in glob.glob(os.path.join(input_folder, '*.txt')):
        logtype = LogType(filename)
        if logtype == 'ftrace_function':
            df = FtraceFunction(filename, search_pid)
        elif logtype == 'ftrace_graph':
            print("warning: ftrace_graph is not currently supported")
            continue
        elif logtype == 'strace_table':
            df = StraceTable(filename)
        elif logtype == 'strace_timestamp':
            df = StraceTimestamp(filename)

        output_filename, output_path = PathFinder(filename, output_folder)
        df.to_csv(output_path)
        print("created " + output_filename)
    # end of for loop


if __name__ == "__main__":
    main()
