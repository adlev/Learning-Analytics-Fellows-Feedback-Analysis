#!/usr/bin/env python

import csv, re
from collections import defaultdict
from ngram import NGram
from math import log

feedback_and_percent = list()

with open('/Users/adam/Desktop/SI110-Gradeswh.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')   # this is supposed to remove unwanted commas?

    feedback = list()
    skipfirst = True    # skips first line

    for line in reader:
        if skipfirst == True:
            skipfirst = False
        else:
            this_line = list()
            if line[1] != '0' and line[2] != '0':    #ignores all 0 scores and assignments worth 0
                this_line.append(line[0])
                this_line.append(float(line[1])/float(line[2]))
                feedback.append(this_line)

#lists of lists that pair feedback with percent score on an assignment

clean_lines = list()
word_counts = defaultdict(int)
for line in feedback:
    clean_line = re.sub(r'[^\w\s]', '', line[0])
    linewords = clean_line.split()
    clean_lines.append(clean_line)
    for word in linewords:#could do a regex match here
        word_counts[word.lower()] += 1
        # allwords.append(word)

word_percents = defaultdict(int)
for line in feedback:
    linewords = line[0].split()
    for word in linewords:
        word_percents[word.lower()] += line[1]

#word, wordcount
sorted_word_count = sorted(word_counts.keys(), key=lambda x: word_counts[x])
#for words in sorted_word_count:
#    print words+'\t'+str(word_counts[words])



total_words = 0
for words in word_counts:
    total_words += word_counts[words]

print total_words

word_probability = dict()
for words in word_counts:
    word_probability[words] = float(word_counts[words])/total_words



freq_file = open('/Users/adam/Desktop/english-freq-all.txt', 'rU')

lines_read = 0
freq_dict = dict()
for line in freq_file:
    if lines_read >= 10000:
        break
    [a, term, freq, d] = line.split('\t')
    freq_dict[term] = freq
    lines_read += 1


compare_dict = dict()
for word in word_probability:
    compare_dict[word] = log((word_probability.get(word, 0) + 0.000001)/(float(freq_dict.get(word, 0))+0.000001))

sorted_compare_dict = sorted(compare_dict.keys(), key=lambda x: -compare_dict[x])
for words in sorted_compare_dict:
    words+'\t'+str(compare_dict[words])
    #add print here for sorted list of relative frequency of words



#NGram stuff
n = NGram()
for line1 in clean_lines:
    n.compare(line1)






