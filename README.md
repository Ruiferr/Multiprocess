# Multiprocess
File reader multiprocess &amp; multithread in Python

Shell input:
	python3 pgrepP [-p n] {files} value
	python3 pgrepT [-p n] {files} value
	
	Em que:
      n : 	number of processes
	files : 	.txt files
	value : 	word/value/expression to be searched in the files.

Output:
  The program should respond with an output revealing the process ID (PID), file name and rows where the value was found.

Excepcions:
  The number of processes/Threads(n) should be > 0 and <= the amount of files to be read.

Observation:
  MacOS has some problems with Queue.qsize() method and raises and error 'NotImplementedError'
