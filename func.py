from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import docx2txt
import re
import pickle

def parse(doc_path):
    STOPWORDS = set(stopwords.words('english'))
    with open("skills.pk", "rb") as handler:
        skills= list(pickle.load(handler))
    
    text = extract_text_from_doc(doc_path)
    
    name = extract_name(text)
    emails = extract_email(text)
    phones = extract_phone_number(text)
    skl = extract_skills(text,skills)
    educations = extract_education(text)
    experiences = extract_experience(text)
    
    return {
        "name" : name, 
        "emails": emails, 
        "phones" : phones, 
        "skills": skl, 
        "educations" : educations, 
        "experiences": experiences
        }
    

def extract_text_from_doc(doc_path):
    '''
    extract plain text from .doc or .docx files
    
    '''
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def extract_email(text):
    emails = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    return emails

def extract_phone_number(text):
    cp = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone = cp.findall(text)
    return phone

def clean_punc(word):
    punctuations = """\n'√,.":)ʹ'̈'´'̇'￼(-!?|;\'&/[]=#*\\•~·{}©^®"""
    no_punct= ""
    for char in word:
        if char not in punctuations:
            no_punct=no_punct + char
    return no_punct;

def extract_skills(nlp_text, skills):
    
    tokens = [clean_punc(token.lower()) for token in text.lower().split() if not token in STOPWORDS]
    skillset = set()
    
    for token in tokens:
        if token in skills:
            skillset.add(token)
    
    return skillset
    
def extract_education(nlp_text):
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text.split()):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]
    
    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education
    
def extract_experience(text):
    
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization 
    word_tokens = nltk.word_tokenize(text)

    # remove stop words and lemmatize  
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words] 
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)
    
    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)
    
    test = []
    
    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x
    
def extract_name(text):
    text_lines =[]
    
    for line in text.split("\n"):
        text_lines.append(line)
        
    nlp = spacy.load("en_core_web_sm")
    
    for i in range(4):
        doc = nlp(text_lines[i])
        for token in doc:
            if not token.is_stop and token.is_alpha and token.pos == 96 and token.tag == 15794550382381185553 and token.shape_== "Xxxxx":
                print(token.text)