#Webpage collection imports

import requests #collect_html
import html2text #trim_html
import re #tokenize_string

#Machine learning imports
import numpy as np
import pandas
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import nltk
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB

def collect_html(url):

    try:
        webpage = requests.get(url)         #Request webpage
        html_text = webpage.text         #HTML text from webpage
        return html_text

    except Exception as collect_html_err:
        print(collect_html_err)             #Print error message

def clean_html_text(html_string):
    html2textObject = html2text.HTML2Text() #Create html2text object
    html2textObject.ignore_links = True     #Change setting to not convert links from HTML

    try:
        handled_html_text = html2textObject.handle(html_string)
        clean_html_text = handled_html_text.replace("\n", " ")
        return clean_html_text              #Return cleaned html text from html string

    except Exception as clean_html_text_err:
        print(clean_html_text_err)          #Print error message

def tokenize_string(input_string):
    token_list = [i for i in re.split(r'([\d.]+|\W+)', input_string) if i]
    return(token_list)

#webpage_html_content = collect_html('http://www.brainjar.com/java/host/test.html') #Example Site
#cleaned_html_content_string = clean_html_text(webpage_html_content)
cleaned_html_content_string = clean_html_text("coke coke coke apple pen pen")
word_list = tokenize_string(cleaned_html_content_string)
#counted_dictionary = (dict((x,word_list.count(x)) for x in set(word_list)))

#Replace from here
df = pandas.read_csv('site_keywords.csv',sep='\t',header=None,names=['label','message'])  #Read in CSV
df['label'] = df.label.map({'ham': 0, 'spam': 1})                                         #Convert class names to numbers
df['message'] = df.message.map(lambda x: x.lower())                                       #Lower string
print(df.head)
df['message'] = df.message.str.replace('[^\w\s]', '')                                     #Replace anything other than a word and spaces
df['message'] = df['message'].apply(nltk.word_tokenize)                                   #tokenize the messages into into single words
print(df.head)
df['message'] = df['message'].apply(lambda x: ' '.join(x))                                # This converts the list of words into space-separated strings
print(df.head)
#To here with code to collect from HTML Pages

count_vect = CountVectorizer()
counts = count_vect.fit_transform(df['message'])

transformer = TfidfTransformer().fit(counts)

counts = transformer.transform(counts)

X_train, X_test, y_train, y_test = train_test_split(counts, df['label'], test_size=0.1, random_state=69)
model = MultinomialNB().fit(X_train, y_train)
predicted = model.predict(X_test)

print(np.mean(predicted == y_test))

#Machine Learning code
#df = pandas.read_csv('classification_csv.csv')
#x = df.drop('diabetes',axis=1)
#y= df['diabetes']
#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25,random_state=42)

#model = GaussianNB()
#model.fit(x_train,y_train)

#y_pred = model.predict(x_test)
#accuracy = accuracy_score(y_test, y_pred)*100
#print(accuracy)

#new_data = OrderedDict([
#    ('glucose',50),
#    ('bloodpressure',80)
#])
#new_data = pandas.Series(new_data).values.reshape(1,-1)

#print(model.predict(new_data))