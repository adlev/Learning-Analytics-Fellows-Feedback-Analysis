#!/usr/bin/env python

import csv, re, hashlib, numpy
from collections import defaultdict
from ngram import NGram
from math import log, fabs

#input file must be a csv of the form [stringfeedback, studentscore, possiblescore]
input_file = '/Users/adam/Desktop/POLSCI101-grades.csv'

pos_file = '/Users/adam/Desktop/positive-words.txt'
neg_file = '/Users/adam/Desktop/negative-words.txt'
freq_file = '/Users/adam/Desktop/english-freq-all.txt'


### Some methods can be edited to alter the way data is split

#returns True if the line is a duplicate
def remove_copy(line):
    h = hashlib.md5(line).hexdigest()
    if h in hash_dict.keys():
        return True
    else:
        hash_dict[h] = 1
        return False

#takes a list of feedback (unsplit), cleans it, and returns a dictionary of the number of times each word appears
def clean_word_counts(list):
    word_counts = defaultdict(int)
    for line in list:
        clean_line = re.sub(r'[^\w\s]', '', line)
        linewords = clean_line.split()
        clean_lines.append(clean_line)
        for word in linewords:#could do a regex match here
            word_counts[word.lower()] += 1
    return word_counts

#takes a list of words and returns a dict of the number of times each word appears
def word_count_from_list(list):
    count_dict = defaultdict(int)
    for word in list:
        if word in count_dict.keys():
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    return count_dict

#returns an int of all values in a dict
def total_word_counts(dict):
    total_words = 0
    for key in dict:
        total_words += dict[key]
    return total_words

#calculates the probability that a word will appear in all of the feedback for a course
def word_probability(p_dict, d_int):
    word_p = dict()
    for key in p_dict:
        word_p[key] = float(p_dict[key])/d_int
    return word_p

# compares a dict of feedback word frequencies with common english frequences and uses log in order to make differences more salient
def log_compare(p_dict):
    log_dict = dict()
    for key in p_dict:
        log_dict[key] = log((float(p_dict.get(key, 0)) + 0.000001)/(float(freq_dict.get(key, 0))+0.000001))
    #sorted_compare_dict = sorted(log_dict.keys(), key=lambda x: -log_dict[x])
    #for words in sorted_compare_dict:
    #    words+'\t'+str(sorted_compare_dict[words])
    #add print here for sorted list of relative frequency of words
    return log_dict

##### EDIT THIS METHOD to change upper and lower bounds. Un-comment the elif to add the c2 lower bound (you will also need to uncomment part of the main code
def cluster_string_by_score(fg,s):
    #### EDIT THIS: c1 is upper bound, c2 is lower bound
    c1 = numpy.percentile(s, 50)
    c2 = numpy.percentile(s, 50)
    print c1
    print c2
    cluster_dict_list = list()
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
    cluster_dict_list.append(c1_dict)
    cluster_dict_list.append(c2_dict)
    cluster_dict_list.append(c3_dict)
    return cluster_dict_list

###### Put all feedback strings into single grade bins
def feedback_bins(fg):
    bin_dict = defaultdict()

    for pair in fg:
        find_grade = re.search(r'(?<=\.)\d\d',(str(pair[1]) + '0'))
        grade = int(find_grade.group(0))
        clean_line = re.sub(r'[^\w\s]', '', pair[0])
        if grade == 00:
                grade = 100
        if grade in bin_dict.keys():

            bin_dict[grade] += (' ' + clean_line)
        else:
            bin_dict[grade] = clean_line
    return bin_dict

### returns a string giving the sentiment score of a dictionary and the number of words.
def sentiment_score(dict):
    cluster_score = 0
    pos = 0
    neg = 0
    words = 0
    for key in dict.keys():
        words += dict[key]
        if key in pos_dict.keys():
            cluster_score += dict[key]
            pos += dict[key]
        elif key in neg_dict.keys():
            cluster_score -= dict[key]
            neg += dict[key]
    return 'pos/neg: ' + str(pos/float(neg)) + ' words:' + str(words)

### returns a list of sentiment scores that also includes the positive and negative numbers of words in a list
def sentiment_score_posneg_brokenout(dict):
    cluster_score = 0
    pos = 0
    neg = 0
    pos_list = list()
    neg_list = list()
    for key in dict.keys():
        if key in pos_dict.keys():
            cluster_score += dict[key]
            pos += dict[key]
            pos_list.append(key)
        elif key in neg_dict.keys():
            cluster_score -= dict[key]
            neg += dict[key]
            neg_list.append(key)
    return [pos, neg, word_count_from_list(pos_list), word_count_from_list(neg_list)]

### returns list(type, ratio of pos to neg or total pos/neg depending on type, score, and total words)
def feedback_counts_with_score(fg):
    full = list()
    for pair in fg:
        add_list = list()
        clean_one = list()
        clean_one.append(pair[0])
        cleaned = clean_word_counts(clean_one)
        word_count = 0
        for key in cleaned:
            word_count += cleaned[key]
        s = sentiment_score_posneg_brokenout(cleaned)
        add_list.append(s[0])
        add_list.append(s[1])
        add_list.append(pair[1])
        add_list.append(word_count)
        add_list.append(s[2])
        add_list.append(s[3])
        full.append(add_list)
    return full

### used to find top positive and negative words in a bin of feedback
def bin_sort_select(bin_list):
    top_bin = list()
    for cdict in bin_list:
        for key in cdict:
            b = dict()
            sort_list = sorted(cdict[key], key=cdict[key].get, reverse=True)[:5]
            d = defaultdict()
            for word in sort_list:
                if cdict[key][word] > 1:
                    d[word] = cdict[key][word]
            b[key] = d
            top_bin.append(b)
    return top_bin



### Start main code

# Load Course Data
with open(input_file, 'rU') as csvfile:
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

<<<<<<< HEAD
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



### This area of the code is used to find relative word frequencies in all feedback compared to normal english
freq_load = open(freq_file, 'rU')

lines_read = 0
freq_dict = dict()
for line in freq_load:
    if lines_read >= 10000:
        break
    [a, term, freq, d] = line.split('\t')
    freq_dict[term] = freq
    lines_read += 1


clustered_dicts = cluster_string_by_score(feedback_grade, scores)
c1_total = total_word_counts(clustered_dicts[0])
c2_total = total_word_counts(clustered_dicts[1])
c3_total = total_word_counts(clustered_dicts[2])

c1_sorted = log_compare(word_probability(clustered_dicts[0], c1_total))
#c2_sorted = log_compare(word_probability(clustered_dicts[1], c2_total))
c3_sorted = log_compare(word_probability(clustered_dicts[2], c3_total))


c_diffs = defaultdict(int)

for key in c1_sorted:
    if key in c3_sorted:
        c_diffs[key] = c3_sorted[key] - c1_sorted[key]




#for key in c1_sorted:
    #if key in c3_sorted:
        #if (fabs(c3_sorted[key] - c1_sorted[key])) > 1.5:
            #print fabs(c3_sorted[key] - c1_sorted[key])
            #print 'under 92:  ' + key+'\t'+str(c1_sorted[key])
    #if key in c2_sorted:
    #    print 'middle 50:  ' + key+'\t'+str(c2_sorted[key])

            #print 'above 92:  ' + key+'\t'+str(c3_sorted[key])

#separate by low medium and high


###### Load Sentiment Dictionaries
sentiment_dict = dict()
pos_dict = dict()
neg_dict = dict()
### Load positives
pos_sent = open(pos_file, 'rU')
for key in pos_sent:
    clean_key = key.strip()
    sentiment_dict[clean_key] = 1
    pos_dict[clean_key] = 1
### Load negatives
neg_sent = open(neg_file, 'rU')
for key in neg_sent:
    clean_key = key.strip()
    sentiment_dict[clean_key] = -1
    neg_dict[clean_key] = -1


#### This is used to find top used negative and positive words for a bin of feedback
binned = feedback_bins(feedback_grade)
binned_pos = list()
binned_neg = list()
for key in binned:
    pos = defaultdict()
    neg = defaultdict()
    pos_words = list()
    neg_words = list()
    words = re.sub("[^\w]", " ",  binned[key]).split()
    for word in words:
        if word in pos_dict:
            pos_words.append(word)
        elif word in neg_dict:
            neg_words.append(word)
    pos_counts = word_count_from_list(pos_words)
    neg_counts = word_count_from_list(neg_words)
    pos[key] = pos_counts
    neg[key] = neg_counts
    binned_pos.append(pos)
    binned_neg.append(neg)



positive_words = bin_sort_select(binned_pos)
negative_words = bin_sort_select(binned_neg)

sentiment_gd = defaultdict(int)
count_gd = defaultdict(int)
number_gd = defaultdict(int)
feed = feedback_counts_with_score(feedback_grade)
for flist in feed:
    score = flist[0] - flist[1]
    find_grade = re.search(r'(?<=\.)\d\d',(str(flist[2]) + '0'))
    grade = int(find_grade.group(0))
    if grade == 00:
        grade = 100
    if grade in sentiment_gd.keys():
        number_gd[grade] += 1
        sentiment_gd[grade] += score
        count_gd[grade] += flist[3]
    else:
        sentiment_gd[grade] = score
        count_gd[grade] = flist[3]
        number_gd[grade] = 1

avg_sentiment_gd = defaultdict(int)
avg_count_gd = defaultdict(int)
for key in sentiment_gd.keys():
    avg_sentiment_gd[key] = (sentiment_gd[key] / float(number_gd[key]))
    avg_count_gd[key] = (count_gd[key] / float(number_gd[key]))

### OUT_FILES BELOW


with open('diff.csv', 'wb') as diff_csv:
    diff_write = csv.writer(diff_csv)
    diff_write.writerow(['word', 'Under 92', 'Above 92'])
    rows = list()

    for key in c1_sorted.keys():
        row = list()
        if key in c3_sorted.keys():
            row.append(key)
            row.append(c1_sorted[key])
            row.append(c3_sorted[key])
        else:
            row.append(key)
            row.append(c1_sorted[key])
        rows.append(row)

    for key in c3_sorted.keys():
        row = list()
        if key not in c1_sorted.keys():
            row.append(key)
            row.append('')
            row.append(c3_sorted[key])
            rows.append(row)
    for row in rows:
        diff_write.writerow(row)

with open('sentiment_grade_dict.csv', 'wb') as sentiment_gd_out:
    sentiment_gd_writer = csv.writer(sentiment_gd_out)
    sentiment_gd_writer.writerow(['grade','sentiment score average','average words', 'n'])
    for key in sentiment_gd.keys():
        sentiment_gd_writer.writerow([key, avg_sentiment_gd[key], avg_count_gd[key], number_gd[key]])

with open('sentiment.csv', 'wb') as sentiment_out:
    sentiment_writer = csv.writer(sentiment_out)
    sentiment_writer.writerow(['pos', 'neg', 'grade score', 'word count'])
    for row in feed:
        sentiment_writer.writerow(row)

with open('sentimentwords.csv', 'wb') as sentiment_w_out:
    sentiment_word_writer = csv.writer(sentiment_w_out)
    sentiment_word_writer.writerow(['Grade', 'pos'])
    prow = list()
    for cdict in positive_words:
        for key in cdict:
            pentry = ''
            for wkey in cdict[key].keys():
                pentry += (wkey + ': ' + str(cdict[key][wkey]) + ' ')
            prow.append([key, pentry])
    for row in prow:
        sentiment_word_writer.writerow(row)
    sentiment_word_writer.writerow(['Grade', 'neg'])
    nrow = list()
    for cdict in negative_words:
        for key in cdict:
            nentry = ''
            for wkey in cdict[key].keys():
                nentry += (wkey + ': ' + str(cdict[key][wkey]) + ' ')
            nrow.append([key,nentry])
    for row in nrow:
        sentiment_word_writer.writerow(row)

=======
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
>>>>>>> 42fc034a2ad0a13b2c625e7790f852e75625b553
