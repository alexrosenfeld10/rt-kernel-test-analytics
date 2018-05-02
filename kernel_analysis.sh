#!/bin/bash

# chmod u+x rt_kernel_analysis.sh

# Local variables
folder_path=/root/gitclones/rt-tests      # folder that contains rt-tests
USAGE="Usage: ./rt_kernel_analysis.sh [-h] [-n program name] [-t type (rt | non-rt)]"
outpath=""                                # trace logfiles will be stored here
csvpath=""                                # csv files will be stored here
program_name=""                           # program name to run traces
search_flag=0                             # flag to check validity of program

# check if arguments are empty
if [ $# == 0 ]; then
  echo $USAGE
  exit 1
fi

# check if user inputs includes program name
while getopts "n:t:h" opt; do
  case ${opt} in
    h)
      echo $USAGE
      exit 0
      ;;
    n)
      program_name="$OPTARG"
      ;;
    # -t flag determines the outpath to either be stored in rt or non-rt
    t)
      if [ "$OPTARG" == "rt" ] || [ "$OPTARG" == "non-rt"]; then
        outpath="$OPTARG/logfiles"
        csvpath="$OSTARG/python-output"
        echo $outpath
      else
        echo "Invalid -t argment"
        echo $USAGE
        exit 1
      fi
      ;;
    \? )
      echo "Invalid arguments."
      echo $USAGE
      exit 1
      ;;
    : )
      echo "Missing argument."
      echo $USAGE
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

# check if type or -t flag was not empty
if [ "$outpath" == "" ]; then
  echo "Please provide -t argument"
  echo $USAGE
  exit 1
fi

# loop over files in folder to validate program name
for f in $folder_path
do
  filename=${f##*/}
  if [ "$filename" == "$program_name" ];
    then
      search_flag=1
  fi
done

if [ "$search_flag" == "0" ];
  then
    echo "Program name missing in /root/gitclones/rt-tests/"
    echo "Please check program name"
    exit 1
fi

# trace ftrace_graph
./ftrace_graph.sh --outfile $outpath/ftrace_graph_1 --test $program_name --duration=5
# trace ftrace functions
./ftrace_functions.sh --outfile $outpath/ftrace_functions_1 --test $program_name --duration=5
./ftrace_functions.sh --outfile $outpath/ftrace_functions_2 --test $program_name --duration=5
./ftrace_functions.sh --outfile $outpath/ftrace_functions_3 --test $program_name --duration=5
./ftrace_functions.sh --outfile $outpath/ftrace_functions_4 --test $program_name --duration=5
./ftrace_functions.sh --outfile $outpath/ftrace_functions_5 --test $program_name --duration=5
# trace strace table
./strace -o $outpath/strace_table_1 -c $program_name
./strace -o $outpath/strace_table_2 -c $program_name
./strace -o $outpath/strace_table_3 -c $program_name
./strace -o $outpath/strace_table_4 -c $program_name
./strace -o $outpath/strace_table_5 -c $program_name
# trace strace timestamp
strace -r -o $outpath/strace_timestamp_1 $program_name
strace -r -o $outpath/strace_timestamp_2 $program_name
strace -r -o $outpath/strace_timestamp_3 $program_name
strace -r -o $outpath/strace_timestamp_4 $program_name
strace -r -o $outpath/strace_timestamp_5 $program_name
# trace perf context switches
perf record -e sched:sched_switch $program_name; perf report --stdio > perf_context_switches_1.txt
perf record -e sched:sched_switch $program_name; perf report --stdio > perf_context_switches_2.txt
perf record -e sched:sched_switch $program_name; perf report --stdio > perf_context_switches_3.txt
perf record -e sched:sched_switch $program_name; perf report --stdio > perf_context_switches_4.txt
perf record -e sched:sched_switch $program_name; perf report --stdio > perf_context_switches_5.txt
# trace perf cache profiling
perf record -e cache-misses $program_name; perf report --stdio > perf_cache_profile_1.txt
perf record -e cache-misses $program_name; perf report --stdio > perf_cache_profile_2.txt
perf record -e cache-misses $program_name; perf report --stdio > perf_cache_profile_3.txt
perf record -e cache-misses $program_name; perf report --stdio > perf_cache_profile_4.txt
perf record -e cache-misses $program_name; perf report --stdio > perf_cache_profile_5.txt
# python parsing
python data_reduction.py -i $outpath -s $program_name -o $csvpath

echo "success."
