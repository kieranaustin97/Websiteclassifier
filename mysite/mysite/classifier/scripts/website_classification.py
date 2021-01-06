#Webpage collection imports (Where each import is used)

import requests #collect_html
import html2text #trim_html
import re #tokenize_string
import csv

#Machine learning imports
import numpy
import pandas
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from collections import OrderedDict

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import nltk
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB

class WebsiteClassifier:
    
    def collect_html(self,url):
        try:
            webpage = requests.get(url, timeout=10) #Request webpage
            html_text = webpage.text         #HTML text from webpage
            return html_text
        except Exception as collect_html_err:
            print(collect_html_err)             #Print error message

    def clean_html_text(self,html_string):
        html2textObject = html2text.HTML2Text() #Create html2text object
        html2textObject.ignore_links = False     #Change setting to not convert links from HTML
        html2textObject.ignore_images = True
        try:
            handled_html_text = html2textObject.handle(html_string)
            clean_html_text = handled_html_text.replace("\n", " ")
            lower_clean_html_text = clean_html_text.lower().strip() #Lower String and strip leading/trailing whitespaces
            return lower_clean_html_text              #Return cleaned html text from html string
        except Exception as clean_html_text_err:
            print(clean_html_text_err)          #Print error message

    def class_collect_website(self,class_name,url):
        message_string = self.clean_html_text(self.collect_html(url))

        html_message_data = {'classification':class_name,'message':message_string}
        return(html_message_data)

    def create_dataframe(self,data):
        newDF = pandas.DataFrame(data=data)
        return(newDF)

    def predict_site_class(self,url): #Code run on form submit (User input)
        #Collect HTML from input url
        new_data_message_string = self.clean_html_text(self.collect_html(url))

        #String object
        new_data_message_string=[new_data_message_string]
        #Counts and transformation for model fitting
        new_data_counts = self.count_vect.transform(new_data_message_string)
        new_data_counts = self.transformer.transform(new_data_counts) 

        #Print classification from prediction
        val = (self.model.predict(new_data_counts)[0])
        
        for key, value in self.classification_dictionary.items(): 
            if val == value: 
                classification_string = key 

        return classification_string
        
    def __init__(self):
        
        #Create empty list
        data_for_dataframe = []

        #Open CSV file containing classified websites
        with open('classifier/scripts/training_websites.csv') as website_csv_file:
            website_csv_reader = csv.DictReader(website_csv_file)
            #Collect and clean HTML and append to data list
            for row in website_csv_reader:
                data_for_dataframe.append(self.class_collect_website(row['classification'],row['url']))

        #Create dataframe
        htmlDF = self.create_dataframe(data_for_dataframe)

        #Array of unique classes of websites from training data
        unique_values = htmlDF.classification.unique()

        #Build up dictionary which maps classes to numerical representation
        self.classification_dictionary = {}
        for i in range(len(unique_values)): #For each unique classification
            self.classification_dictionary[unique_values[i]] = i #Add classification to dicionary along with increasing number mapping
        
        #Replace classification name with number
        htmlDF['classification'] = htmlDF.classification.map(self.classification_dictionary)
        htmlDF['message'] = htmlDF.message.str.replace('[^\w\s]', '') 
        
        self.count_vect = CountVectorizer()
        counts = self.count_vect.fit_transform(htmlDF['message'])

        self.transformer = TfidfTransformer().fit(counts)

        counts = self.transformer.transform(counts)

        X_train, X_test, y_train, y_test = train_test_split(counts, htmlDF['classification'], test_size=0.4, random_state=69)
        
        self.model = MultinomialNB().fit(X_train, y_train)
        predicted = self.model.predict(X_test)

        #print(numpy.mean(predicted == y_test))