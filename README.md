# Scheduling Cores Gantt
This project aims to plot a gantt chart given a json file with a resulting scheduling.

# Installing
The following command create a conda environment.

```
conda env create -f environment.yml
```

# Usage

First, activate your environment with:

```
conda activate gantt
```

Then, you can execute the help command to see the options:

```
python gantt.py -h
usage: gantt.py [-h] -f FILE [-s FILE]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file to evaluate
  -s FILE, --save FILE  Output file
```

# Example
The following command outputs the gantt result:

```
python gantt.py -f example/scheduling.json
```

The expected gantt is:
![alt text](example/scheduling.png)

You can also directly save this file using:

```
python gantt.py -f example/scheduling.json -s example/scheduling.png
```