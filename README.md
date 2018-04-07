# PREEMPT-RT-LINUX


### Ftrace Analytics

###### Ftrace function
To data reduce ftrace function log files run this command:

`python ftrace_df.py -f out_pi_stress/out_pi_stress_0.txt out_pi_stress/out_pi_stress_1.txt -l pi_stress`

* The `-f` represents the log files
* The `-l` represents the process-id that you would be filtering in

This command will output two csv files as such:

`created out_pi_stress/out_pi_stress_0.csv`

`created out_pi_stress/out_pi_stress_1.csv`

###### Ftrace function graph
ftrace_graph is not yet supported

---

### Strace Analytics

###### Strace log files
To data reduce strace function log files run this command:

`python strace_df.py -f strace_table.txt strace_timestamps.txt`
`

This command will output two csv files as such:

`created strace_table.csv`

`created strace_timestamps.csv`

Side note: Not every function call in strace_timestamps log files and may throw an error. This is indicated as follows:

`error... could not create csv`

If this occurs, please notify using github issues.
