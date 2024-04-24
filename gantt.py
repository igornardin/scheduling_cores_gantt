#! /usr/bin/python3

import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from argparse import ArgumentParser
import matplotlib.ticker as ticker

class Jobs:
    def __init__(self, id, startTime, finishTime, machine, nbcores):
        self.id = id
        self.startTime = startTime
        self.finishTime = finishTime
        self.machine = machine
        self.nbcores = nbcores
        self.cores = []

    def __repr__(self):
        return "Jobs Object (id {})".format(self.id, self.startTime, self.finishTime, self.machine, self.nbcores, self.cores)
    
    def __str__(self):
        return self.__repr__()

class Scheduling:
    def __init__(self):
        self.scheduling = []
        self.min_date = 0
        self.max_date = math.inf
        self.jobs : List[Jobs] = []
        self.y_height = 2
        self.y_positions = {}

    def intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def readFile(self, filename):
        with open(filename,) as f:
            data = json.load(f)
            
            self.min_date = int(data["config"]["min_time"])
            self.max_date = int(data["config"]["max_time"])

            self.scheduling = [{} for x in range(0, self.max_date - self.min_date + 1)]
            y_pos = 0
            for machine_key, machine_value in data["machines"].items():
                self.y_positions[machine_key] = {}
                for core in range(0, machine_value["cores"]):
                    self.y_positions[machine_key][core] = y_pos
                    y_pos += self.y_height
                for x in range(0, self.max_date - self.min_date + 1):
                    self.scheduling[x][int(machine_key)] = [c for c in range(0, machine_value["cores"])]

            for job_key, job_value in data["jobs"].items():
                self.jobs.append(Jobs(job_key, job_value["start_time"], job_value["finish_time"], job_value["machine"], job_value["cores"]))

    def createScheduling(self):
        for job in self.jobs:
            startingPoint = job.startTime - self.min_date
            finishingPoint = job.finishTime - self.min_date
            coresAvailable = self.scheduling[startingPoint][job.machine]
            for step in range(startingPoint + 1, finishingPoint + 1):
                coresAvailable = self.intersection(coresAvailable, self.scheduling[step][job.machine])
            if len(coresAvailable) < job.nbcores:
                raise NameError("Scheduling problem!! Machine {} does not have enough cores avaiable for job {} with {} demanded cores".format(job.machine, job.id, job.nbcores))
            job.cores = coresAvailable[:job.nbcores]
            for step in range(startingPoint, finishingPoint + 1):
                for core in job.cores:
                    self.scheduling[step][job.machine].remove(core)

    def plotGantt(self, savefig=None):
        fig, ax = plt.subplots(figsize=(20, 20))
        y_labels = []
        y_positions = []
        y_cores_position = []
        y_labels_position = []
        y_max = 0
        for y_machine, y_cores in self.y_positions.items():
            for label, pos in y_cores.items():
                if label == 0:
                    y_labels.append(y_machine)
                    y_positions.append(pos)
                y_cores_position.append(pos)
                y_max = pos
            y_labels_position.append(y_max - (len(y_cores) / 2))
        colors = ["tab:blue", 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
        h = list("/|X")
        colorIndex = 0
        hIndex = 0
        for job in self.jobs:
            if (colorIndex >= len(colors)):
                colorIndex = 0
                hIndex += 1
                if (hIndex >= len(h)):
                    hIndex = 0
            x0 = job.startTime
            duration = job.finishTime - job.startTime
            for core in job.cores:
                rect = patches.Rectangle(
                    (x0, self.y_positions[str(job.machine)][core]),
                    duration,
                    self.y_height,
                    edgecolor='black',
                    linewidth=0.5,
                    facecolor=colors[colorIndex],
                    hatch=h[hIndex]
                )
                ax.add_artist(rect)
                rect.axes.annotate(
                    str(job.id),
                    (x0+(duration/2), self.y_positions[str(job.machine)][core]+1),
                    color='black',
                    fontsize='small',
                    ha='center',
                    va='center'
                )                
            colorIndex += 1
        y_max += self.y_height
        ax.set_xlabel('Time', size=16)
        ax.set_ylabel('Machine/Core', size=16)
        ax.yaxis.set_ticks(y_positions, y_labels)
        ax.set_xlim(self.min_date, self.max_date)
        ax.set_ylim(0, y_max)
        ax.set_yticks(y_cores_position, minor=True)
        ax.tick_params(axis='y', which="major", length=8, pad=5)
        ax.grid(visible=True, which='both')

        fig.tight_layout()

        if savefig:
            plt.savefig(savefig)
            plt.close()
        else:
            plt.show()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Input file to evaluate", metavar="FILE", required=True)
    parser.add_argument("-s", "--save", dest="savefig",
                        help="Output file ", metavar="FILE")
    
    args = parser.parse_args()    

    scheduling = Scheduling()
    scheduling.readFile(args.filename)
    scheduling.createScheduling()
    scheduling.plotGantt(args.savefig)