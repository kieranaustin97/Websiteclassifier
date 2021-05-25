"""Website Classification Machine Learning and Data Science Script"""
#Webpage collection imports
import csv
import re #tokenize_string
import requests #collect_html
import html2text #trim_html

#Machine learning imports
import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class WebsiteClassification:

    def __init__(self):
        #Create empty list
        data_for_dataframe = []

        #Open CSV file containing classified websites
        with open('classifier/scripts/training_websites.csv') as website_csv_file:
            website_csv_reader = csv.DictReader(website_csv_file)
            #Collect and clean HTML and append to data list
            for row in website_csv_reader:
                try:
                    data_for_dataframe.append(self.class_collect_website(row['classification'],row['url']))
                except Exception as error:
                    continue
        #Create dataframe
        htmlDF = pandas.DataFrame(data_for_dataframe)
        
        #Array of unique classes of websites from training data
        self.unique_values = htmlDF.classification.unique()

        #Build up dictionary which maps classes to numerical representation
        self.classification_dictionary = {}
        for i in range(len(self.unique_values)): #For each unique classification
            self.classification_dictionary[self.unique_values[i]] = i #Add classification to dicionary along with increasing number mapping

        #Replace classification name with number
        htmlDF['classification'] = htmlDF.classification.map(self.classification_dictionary)

        self.count_vect = CountVectorizer()
        counts = self.count_vect.fit_transform(htmlDF['message'])

        self.transformer = TfidfTransformer().fit(counts)
        counts = self.transformer.transform(counts)

        X_train, X_test, y_train, y_test = train_test_split(counts, htmlDF['classification'], test_size=0.15, random_state=69)
        model = MultinomialNB().fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test,y_pred)*100
        print("Model Accuracy:")
        print(accuracy)

        #Fit model using every classification and URL provided
        #self.model = MultinomialNB().fit(counts, htmlDF['classification'])    

    def collect_html(self,url):
        try:
            webpage = requests.get(url, timeout=1) #Request webpage
        except requests.exceptions.Timeout as timeout_err:
            print(timeout_err) #Print error message
            raise
        except requests.exceptions.ConnectionError as http_err:
            print(http_err) #Print error message
            raise
        
        html_text = webpage.text #HTML text from webpage
        return html_text

    def clean_html_text(self,html_string):
        html_2_text_object = html2text.HTML2Text() #Create html2text object
        html_2_text_object.ignore_links = False #Change setting to not convert links from HTML
        html_2_text_object.ignore_images = True
        try:
            handled_html_text = html_2_text_object.handle(html_string)
            cleaned_html_text = re.sub(r'[^\w\s]', ' ',handled_html_text) #regex to take out special characters
            stripped_html_text = re.sub(r'\s+',' ', cleaned_html_text).lower().strip() #regex to take out multiple white spaces, Lower String and strip leading/trailing whitespaces
        except Exception as cleaned_html_text_error:
            print(cleaned_html_text_error) #Print error message
            raise
        
        return stripped_html_text #Return cleaned html text from html string

    def class_collect_website(self,class_name,url):
        try:
            message_string = self.clean_html_text(self.collect_html(url))
        except Exception:
            raise
        
        html_message_data = {'classification':class_name,'message':message_string}
        return(html_message_data)

    def predict_site_class(self,url): #Code run on form submit (User input)
        #Collect HTML from input url
        try:
            new_data_message_string = self.clean_html_text(self.collect_html(url))
        except Exception:
            raise
        
        #String object
        new_data_message_string=[new_data_message_string]
        #Counts and transformation for model fitting
        new_data_counts = self.count_vect.transform(new_data_message_string)
        new_data_counts = self.transformer.transform(new_data_counts) 

        val = self.model.predict(new_data_counts)[0]
        
        for key, value in self.classification_dictionary.items(): 
            if val == value: 
                classification_string = key 

        return url,classification_string

    def list_possible_classes(self):
        return self.unique_values
