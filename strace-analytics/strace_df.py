'''
ftrace_df.py

Procedure
1. Cleans the log file created by bash script ftrace
2. Creates a dataframe with the following column names and datatypes:
    * columan name:             Data type
    --------------------------------------
    * time                      float
    * seconds                   float
    * usecs/call                int
    * calls                     int
    * errors                    int
    * syscall                   String
3. Create output csv file based on the input filename

usage: strace_df.py [-f [filenames]
example: python strace_df.py -f strace_table.txt
example output: strace_table.csv
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

    function_name = ""
    output_filename = filename[:-4] + ".csv"

    # read filename line by line
    with open(filename) as fp:
        for line_num, l in enumerate(fp):
            line = l.split()
            if line[0] == '%':
                function_name = "strace_table"
            if function_name == "strace_table":
                if line_num >= 2:
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
        df = pd.DataFrame({ header[0]: time,
                            header[1]: seconds,
                            header[2]: usecs_call,
                            header[3]: calls,
                            header[4]: errors,
                            header[5]: syscall})

        df.to_csv(output_filename, sep=',')
        print("created " + output_filename)
