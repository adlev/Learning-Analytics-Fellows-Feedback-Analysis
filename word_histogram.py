#!/usr/bin/env python

import csv
from collections import defaultdict

feedback_and_percent = list()

with open('/Users/adam/Desktop/SI110-Gradeswh.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')   # this is supposed to remove unwanted commas?

    feedback = list()
    skipfirst = True    # skips first line
    total_lines = 0

    for line in reader:
        if skipfirst == True:
            skipfirst = False
        else:
            this_line = list()
            if line[1] != '0' and line[2] != '0':    #ignores all 0 scores and assignments worth 0
                this_line.append(line[0])
                this_line.append(float(line[1])/float(line[2]))
                feedback.append(this_line)
                total_lines += 1


print(total_lines)


#lists of lists that pair feedback with percent score on an assignment

allwords = list()
word_counts = defaultdict()
for line in feedback:
    linewords = line[0].split()
    for word in allwords:           #could do a regex match here
        word_counts[word] = word_counts[word] + 1
        # allwords.append(word)

#word_counts = defaultdict(int)
#for word in allwords:
    #word_counts[word] += 1
sorted_keys = sorted(word_counts.keys(), key=lambda x: -word_counts[x])
for key in sorted_keys:
    print key+'\t'+word_counts[key]
    #create a dictionary with lists of words with the value as the percent score
