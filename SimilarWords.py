from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem.wordnet import WordNetLemmatizer

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
def check_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
    #print(synsets1)
    #print(synsets2)
       # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = list([synset.path_similarity(ss) for ss in synsets2])
        best_score= list(filter(lambda a: a != None, best_score))
        if(best_score==[]):
            best_score =0
        else:
            best_score = max(best_score)
        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1
 
    # Average the values
    if (count!= 0):
        score /= count
    return score


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def preprocess(text):
    word_tokens = word_tokenize(text)
    filtered_sentence = " ".join([w for w in word_tokens if not w in stop_words])
    wnl = WordNetLemmatizer()
    Lemmatized = " ".join([wnl.lemmatize(i) for i in filtered_sentence.split()])
    return Lemmatized

 def returnSimilarity(s1 , s2):
 	    sim1 = check_similarity(query,ques+" ".join(qa[ques]))
	    sim2 = check_similarity(ques+" ".join(qa[ques]), query)
	    sim = (sim1 + sim2)/2
	    tfidf_cosine = cosine_sim(ques+" ".join(qa[ques]) , query)
	    if(sim>0.7):
	        print(ques+" ".join(qa[ques]) , "Similarity: ", sim)
	        similar_questions[ques+" ".join(qa[ques])] = sim
	        print("Common words" ,common_words)
	        print("Tfidf cosine" , tfidf_cosine)ss


 




