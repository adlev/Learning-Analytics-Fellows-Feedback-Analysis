import sys
from lxml import etree
from xml.etree import ElementTree
from xml.etree.ElementTree import parse

# next steps:
#
# sentiment for adjectives/modifiers
# start thinking about generative model (see macauley paper)
# compute aspect space sentiment score per dimension.  with conf scores.
# better modifier phrase collection
# cluster modifiers by synonyms

# experiments:
#
# compute same canonical summary for different sections of large class
# start looking at relationships between eval text variables and eval score variables


exam_words = list(['exam', 'exams', 'test', 'tests', 'quiz', 'quizzes'])
homework_words = list(['assignments', 'homework'])
content_words = list(['content', 'material', 'slides'])
lecture_words = list(['lecture', 'lectures'])
textbook_words = list(['book', 'text', 'textbook', 'books', 'texts', 'textbooks'])

def output_concept_description(concept, output_header, top_k):
    print output_header
    sorted_keys = sorted(concept.keys(), key=lambda x: -concept[x])
    for key in sorted_keys:
        top_k = top_k - 1
        if (top_k < 0):
            break
        print '\t' + key + ': ' + str(concept[key])
        
# create a merged set of modifiers from a list of words that define a concept
def concept_summary(targets, concept_words):
    mod_list_merged = dict()
    if (concept_words == None):
        concept_words = targets.keys()
    
    for w in concept_words:
        if (w in targets):
            modlist = targets[w]
            for mod in modlist:
                initial_count = mod_list_merged.get(mod, 0)
                mod_list_merged[mod] = initial_count + modlist[mod]
            
    return mod_list_merged

allText = ""
filename = sys.argv[1]
dom = parse(filename) ###'c:\\Users\\kevynct.REDMOND\\Dropbox\\um-course-fb\\sample-course2-sentences.txt.xml')
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
recordlist = dom.getroot()
documentlist = recordlist[0].getiterator('document')  
sentencelist = documentlist[0].getiterator('sentences')

course_aspects = dict()
targets = dict()
for sentence in sentencelist[0]:
    for element in sentence:     # for each <Filing>...</Filing> group
        issues = element.getiterator('dependencies')    
        if len(issues) > 0: 
            issuelist = issues[0].getiterator('dep')
            for i in issuelist:
                # governor has modifier, dependent has target
                d = i.find('dependent').text
                d = d.lower()
                g = i.find('governor').text
                g = g.lower()

                tag = i.attrib.get('type')
                if (tag == 'neg'):
                    # dependent has negation
                    # governor has target
                    for key in targets:
                        modlist = targets[key]
                        if g in modlist:
                            modlist['not ' + g] = modlist[g]
                            del modlist[g]
                            
                    continue
                
                if (tag == 'nsubj' or tag == 'nsubjpass'):
                    if (d == 'i' or d == 'my' or d == 'he' or d == 'she' or d == 'we' or d == 'they' or d == 'it' or d == 'them' or d == 'they' or d == 'that' or d== 'me' or d=='you' or d=='us' or d=='this' or d == 'his'):
                        continue
                    if (g == 'going' or g == 'went' or g == 'got' or g == 'seem' or g == 'seemed' or g == 'are' or g == 'is' or g == 'were' or g == 'was' or g == 'has' or g == 'had' or g == 'have'):
                        continue

                    targmodifiers = targets.get(d, dict())
                    targets[d] = targmodifiers
                    count = targmodifiers.get(g, 0)
                    targmodifiers[g] = count + 1

top_k = 10
exam_desc = concept_summary(targets, exam_words)
output_concept_description(exam_desc, 'Exams:', top_k)
print
content_desc = concept_summary(targets, content_words)
output_concept_description(content_desc, 'Course content:', top_k)
print
lecture_desc = concept_summary(targets, lecture_words)
output_concept_description(lecture_desc, 'Lectures:', top_k)
print
homework_desc = concept_summary(targets, homework_words)
output_concept_description(homework_desc, 'Homework:', top_k)
print
#all_desc = concept_summary(targets, None)
#output_concept_description(all_desc, 'All:', 100)
#print
