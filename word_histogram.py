#!/usr/bin/env python

import csv, re, hashlib, numpy
from collections import defaultdict
from ngram import NGram
from math import log,fabs

def remove_copy(line):
    h = hashlib.md5(line).hexdigest()
    if h in hash_dict.keys():
        return True
    else:
        hash_dict[h] = 1
        return False

def clean_word_counts(list):
    word_counts = defaultdict(int)
    for line in list:
        clean_line = re.sub(r'[^\w\s]', '', line)
        linewords = clean_line.split()
        clean_lines.append(clean_line)
        for word in linewords:#could do a regex match here
            word_counts[word.lower()] += 1
    return word_counts


#infile must be a csv of the form [stringfeedback, studentscore, possiblescore]
with open('/Users/adam/Desktop/SI110-Gradeswh.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')   # this is supposed to remove unwanted commas

    feedback_grade = list()
    skipfirst = True    # skips first line
    hash_dict = dict()
    scores = list()
    for line in reader:
        if skipfirst == True:
            skipfirst = False
        else:
            if remove_copy(line[0]):    #feedback = line[0]
                continue
            this_line = list()
            if line[1] != '0' and line[2] != '0':    #ignores all 0 scores and assignments worth 0, appends the grade to feedback_grade
                this_line.append(line[0])
                this_line.append(float(line[1])/float(line[2]))
                feedback_grade.append(this_line)
                scores.append(float(line[1])/float(line[2]))


#lists of lists that pair feedback with percent score on an assignment

clean_lines = list()

word_percents = defaultdict(int)
for line in feedback_grade:
    linewords = line[0].split()
    for word in linewords:
        word_percents[word.lower()] += line[1]

#word, wordcount
#sorted_word_count = sorted(total_word_counts.keys(), key=lambda x: total_word_counts[x])
#for words in sorted_word_count:
#    print words+'\t'+str(word_counts[words])


def total_word_counts(dict):
    total_words = 0
    for key in dict:
        total_words += dict[key]
    return total_words


def word_probability(p_dict, d_int):
    word_p = dict()
    for key in p_dict:
        word_p[key] = float(p_dict[key])/d_int
    return word_p



freq_file = open('/Users/adam/Desktop/english-freq-all.txt', 'rU')

lines_read = 0
freq_dict = dict()
for line in freq_file:
    if lines_read >= 10000:
        break
    [a, term, freq, d] = line.split('\t')
    freq_dict[term] = freq
    lines_read += 1

def log_compare(p_dict):
    log_dict = dict()
    for key in p_dict:
        log_dict[key] = log((float(p_dict.get(key, 0)) + 0.000001)/(float(freq_dict.get(key, 0))+0.000001))
    #sorted_compare_dict = sorted(log_dict.keys(), key=lambda x: -log_dict[x])
    #for words in sorted_compare_dict:
    #    words+'\t'+str(sorted_compare_dict[words])
    #add print here for sorted list of relative frequency of words
    return log_dict



#NGram stuff

def cluster_string_by_score(fg,s):
    c1 = numpy.percentile(s, 50)
    c2 = numpy.percentile(s, 50)
    print c1
    print c2
    cluster_list = list()
    c1_list = list()
    c2_list = list()
    c3_list = list()

    for pair in fg:
        if pair[1] < c1:
            c1_list.append(pair[0])
        #elif pair[1] ==c2:
        #    c2_list.append(pair[0])
        else:
            c3_list.append(pair[0])

    c1_dict = clean_word_counts(c1_list)
    c2_dict = clean_word_counts(c2_list)
    c3_dict = clean_word_counts(c3_list)

    cluster_list.append(c1_dict)
    cluster_list.append(c2_dict)
    cluster_list.append(c3_dict)
    return cluster_list


clustered_dicts = cluster_string_by_score(feedback_grade, scores)

c1_total = total_word_counts(clustered_dicts[0])
c2_total = total_word_counts(clustered_dicts[1])
c3_total = total_word_counts(clustered_dicts[2])

c1_sorted = log_compare(word_probability(clustered_dicts[0], c1_total))
#c2_sorted = log_compare(word_probability(clustered_dicts[1], c2_total))
c3_sorted = log_compare(word_probability(clustered_dicts[2], c3_total))

for key in c1_sorted:

    if key in c3_sorted:
        if (fabs(c3_sorted[key] - c1_sorted[key])) > 2.5:
            print fabs(c3_sorted[key] - c1_sorted[key])
            print 'under 92:  ' + key+'\t'+str(c1_sorted[key])
    #if key in c2_sorted:
    #    print 'middle 50:  ' + key+'\t'+str(c2_sorted[key])

            print '100+    :  ' + key+'\t'+str(c3_sorted[key])

#separate by low medium and high

