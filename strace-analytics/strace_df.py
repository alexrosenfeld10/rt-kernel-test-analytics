'''
strace_df.py

Procedure
1. Cleans the log file created by bash script strace
2. Creates a dataframe with the following column names and datatypes:
    for strace_graph files:
    * columan name:             Data type
    --------------------------------------
    * time                      float
    * seconds                   float
    * usecs/call                int
    * calls                     int
    * errors                    int
    * syscall                   String

    for strace_timestamp files:
    * columan name:             Data type
    --------------------------------------
    * pid                       int
    * process_time              float
    * process_name              String
    * parameter                 String

3. Create output csv file based on the input filename

usage: strace_df.py [-f [filenames]
example: python strace_df.py -f strace_table.txt strace_timestamps.txt
example output: strace_table.csv strace_timestamp.csv
'''
import argparse
import pandas as pd

# column names for data frame
header = ["time",
          "seconds",
          "usecs/call",
          "calls",
          "errors",
          "syscall"]

header2 = ["pid",
           "process_time",
           "process_name",
           "parameter"]

# list of files to read
list_filenames = []

# command line parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", action='store', dest='filename',
                    nargs="+", help="Filename of input log file")
args = parser.parse_args()
list_filenames = args.filename

# read every file
for filename in list_filenames:
    # column values for data frame
    time = []
    seconds = []
    usecs_call = []
    calls = []
    errors = []
    syscall = []

    pid = []
    process_time = []
    process_name = []
    parameter = []

    function_name = ""
    output_filename = filename[:-4] + ".csv"

    # read filename line by line
    with open(filename) as fp:
        for line_num, l in enumerate(fp):
            if line_num == 0:
                line = l.split()
                if line[0] == '%':
                    function_name = "strace_table"
                else:
                    function_name = "strace_timestamp"
            if function_name == "strace_table":
                if line_num >= 2:
                    line = l.split()
                    if line[0] == "------":
                        break
                    if len(line) == 5:
                        # line without error value
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
            if function_name == "strace_timestamp":
                if line_num >= 0:
                    line = l.split()
                    print(l)
                    print(line)
                    col = 0
                    temp_parameter = ""
                    for i, val in enumerate(line):
                        if col == 0:
                            print("pid: " + val)
                            pid.append(val)
                            col += 1
                        elif col == 1:
                            print("process_time: " + val)
                            process_time.append(val)
                            col += 1
                        elif col == 2:
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
                                    print("1st temp_parameter: " + temp_parameter)
                                if c == '(':
                                    print("process_name: " + val[:index])
                                    process_name.append(val[:index])
                                    temp_parameter = temp_parameter[index:]
                                    col += 1
                                if c == ')':
                                    col += 1
                        elif col == 3:
                            if i == len(line) - 1:
                                temp_parameter += val + " "
                                print("temp_parameter: " + temp_parameter)
                                parameter.append(temp_parameter)
                            else:
                                for index, c in enumerate(val):
                                    if c == ')':
                                        val = val[:-1]
                                        col += 1
                            temp_parameter += val + " "
                            print("temp_parameter: " + temp_parameter)
                        elif col == 4:
                            print("added")
                            parameter.append(temp_parameter)
                            col += 1
                        else:
                            print('---------')

    if function_name == "strace_table":
        df = pd.DataFrame({ header[0]: time,
                            header[1]: seconds,
                            header[2]: usecs_call,
                            header[3]: calls,
                            header[4]: errors,
                            header[5]: syscall})

        df.to_csv(output_filename, sep=',')
        print("created " + output_filename)
    else:
        if len(pid) == len(process_time) == len(process_name) == len(parameter):
            df = pd.DataFrame({ header2[0]: pid,
                                header2[1]: process_time,
                                header2[2]: process_name,
                                header2[3]: parameter})
            df.to_csv(output_filename, sep=",")
            print("created " + output_filename)
        else:
            print("error... could not create csv")
