# PREEMPT-RT-LINUX

### Adding log files
Please consider if you're kernel is running real-time or non-real-time and push into the respected folder called logfiles

### Creating csv files
After inserting log files into the respected logfiles folder, please run this command:

##### for rt
`python data_reduction.py -i rt/logfiles -s pi_stress -o rt/python-output`

##### for non-rt
`python data_reduction.py -i non-rt/logfiles -s pi_stress -o non-rt/python-output`

The output csv files will be created in the folder python-output

### Future work
* Statistical analysis on data frames created
* Refactor into Object-Orientated Design

### Possible issues
If these issues arise, please notify in github issues or on discord.
* Our strace output file is missing process id
* The timestamp log file may contain errors that the data_reduction.py does not recognize
