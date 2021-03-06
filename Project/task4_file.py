from task2_file import get_wordnet_pos
from sematch.semantic.similarity import YagoTypeSimilarity
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
# ----------------------------------------------------------------
'''
Description  ------------------------------------------------------------------------
Function will define YAGO concepts and calculate calculates similarity score between
sentence 1 and sentence 2 (very similar to PartialSim-function).

Inputs  ------------------------------------------------------------------------------
s1      sentence 1 (string)
s2      sentence 2 (string)
method  "wpath" or "wpath_graph" (string)

Outputs ----------------------------------------------------------------------------
Returns the similarity value in numeric format (between 1 and 0).
'''
#Load YAGO
sim_yago = YagoTypeSimilarity()

#Function for calculating the sentence similarities using YAGO concepts
def task4Yago(s1,s2,method):
    #Format the input sentences to desired form
    s1=s1.lower()
    s2=s2.lower()
    #Separate sentence into words. Aka list of words.
    s1_words = word_tokenize(s1)
    s2_words = word_tokenize(s2)
    #POS tags for each word in sentence.
    pos1 = pos_tag(s1_words)
    pos2 = pos_tag(s2_words)
    #Remove stop words from the pos, tagged sentences
    pos1 = [word for word in pos1 if word[0] not in stopwords.words('english')]
    pos2 = [word for word in pos2 if word[0] not in stopwords.words('english')]
    #Calculate similarity for all words in pos1  (pos1 is a modified "s1". AKA modified sentence 1)
    s1_total=0
    count=0
    s1_sim=0
    for a in pos1:
        word1 = str(a[0])
        pos_tag1_incompatible = str(a[1])                   # get the incompatible pos tag that was received
                                                            # from nltk.pos_tag(...) function.
        pos_tag1 = get_wordnet_pos(pos_tag1_incompatible)   #converting to compatible pos tag.s
        if pos_tag1 == '':
            continue                                        #could not find pos tag. Let's skip this word

        #Mapping a word to yago links in DBpedia
        word1_mapped = sim_yago.word2yago(word1)            # e.g. 'http://dbpedia.org/class/yago/Dancer109989502' for word 'dancer'

        biggest_similarity=-9999999999

        for b in pos2:
            word2 = str(b[0])
            pos_tag2_incompatible = str(b[1])
            pos_tag2 = get_wordnet_pos(pos_tag2_incompatible)
            if pos_tag2 == '':
                continue                                    #could not find pos tag. Let's skip this word

            #Mapping a word to yago links in DBpedia
            word2_mapped = sim_yago.word2yago(word2)

            temp_number = 0
            for c in word1_mapped:
                for d in word2_mapped:
                    #Measuring YAGO concept similarity through WordNet taxonomy and corpus based information content
                    if method=="wpath":
                        temp_number = sim_yago.yago_similarity(c, d, 'wpath')
                    #Measuring YAGO concept similarity based on graph-based IC
                    elif method=="wpath_graph":
                        temp_number = sim_yago.yago_similarity(c, d, 'wpath_graph')
                    if (temp_number is not None) and (temp_number > biggest_similarity):
                        biggest_similarity = temp_number

        if (biggest_similarity != -9999999999):
            count=count+1
            s1_sim=s1_sim+biggest_similarity
        #else:
            #print("\"biggest_similarity\" is still the default value after looping all the words. --> No similarity found.  The word in question is word1: "+str(word1))

    if(count > 0):
        s1_total=(s1_sim / count)
    else:
        s1_total = 0
    return (round(s1_total,3))
'''
Description  ------------------------------------------------------------------------
Function will iterate through sentencepairs and print similarity score between
sentences using task4Yago-function.

Inputs  ------------------------------------------------------------------------------
sentencePairs - array containing sentence pairs ([[sentence1, sentence2],[sentence1, sentence2], ...])

Outputs ----------------------------------------------------------------------------
None
'''
def task4(sentencePairs):
    #Measuring YAGO concept similarity through WordNet taxonomy and corpus based information content
    print("\nMeasuring YAGO concept similarity through WordNet taxonomy and corpus based information content:\n")
    for i in range(0,len(sentencePairs)):
        s1 = sentencePairs[i][0]
        s2 = sentencePairs[i][1]
        print("Similarity: " + str(task4Yago(s1,s2,"wpath")).ljust(5) + " for sentence pair: "+ str(sentencePairs[i]))

    #Measuring YAGO concept similarity based on graph-based IC
    print("\nMeasuring YAGO concept similarity based on graph-based IC:\n")
    for i in range(0,len(sentencePairs)):
        s1 = sentencePairs[i][0]
        s2 = sentencePairs[i][1]
        print("Similarity: " + str(task4Yago(s1,s2,"wpath_graph")).ljust(5) + " for sentence pair: "+ str(sentencePairs[i]))
