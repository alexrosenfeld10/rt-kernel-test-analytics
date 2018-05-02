#!/bin/bash

# Set up script variables
tracing_dir="/sys/kernel/debug/tracing"
test_dir="/root/gitclones/rt-tests"

# iterate over arguments
args=""
outfile=""
while [ ! -z "$1" ]
do
  case $1 in
    --outfile)
      shift
      outfile="$1"
      shift
      ;;
   --help)
      echo "usage: --outfile <name> --test <test with args>"
      exit 0
      ;;
   --test)
      shift
      while [ ! -z "$1" ]
      do
        args="$args$1 "
        shift
      done
      ;;
  esac
done

outfile_path="$outfile".txt

# Create logfile header with job run and timestamp
echo "$args" > $outfile_path
echo "$(date +'%m-%d-%Y %H:%M:%S')" >> $outfile_path
echo "" >> $outfile_path

# Tell the user what tests they're running
echo "You're running the following tests:"
echo "$args"

# Set up the trace and clean up the history
echo 0 > $tracing_dir/tracing_on
echo function > $tracing_dir/current_tracer
# this doesn't work properly, it only results in the calls from this script, not pi_stress
# echo $$ > $tracing_dir/set_ftrace_pid
echo "" > $tracing_dir/trace
echo 1 > $tracing_dir/tracing_on

# Run the tests
$test_dir/$args

# Turn off tracing after the tests are run
echo 0 > $tracing_dir/tracing_on
cat $tracing_dir/trace >> $outfile_path
