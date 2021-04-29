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

def collect_html(url):
    try:
        webpage = requests.get(url, timeout=3) #Request webpage
    except requests.exceptions.Timeout as timeout_err:
        print(timeout_err) #Print error message
        raise
    except requests.exceptions.ConnectionError as http_err:
        print(http_err) #Print error message
        raise
    else:
        html_text = webpage.text #HTML text from webpage
        return html_text

def clean_html_text(html_string):
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
    else:
        return stripped_html_text #Return cleaned html text from html string

def class_collect_website(class_name,url):
    try:
        message_string = clean_html_text(collect_html(url))
    except Exception:
        raise
    else:
        html_message_data = {'classification':class_name,'message':message_string}
        return(html_message_data)

def predict_site_class(url): #Code run on form submit (User input)
    #Collect HTML from input url
    try:
        new_data_message_string = clean_html_text(collect_html(url))
    except Exception:
        raise
    else:
        #String object
        new_data_message_string=[new_data_message_string]
        #Counts and transformation for model fitting
        new_data_counts = count_vect.transform(new_data_message_string)
        new_data_counts = transformer.transform(new_data_counts) 

        val = model.predict(new_data_counts)[0]
    
        for key, value in classification_dictionary.items(): 
            if val == value: 
                classification_string = key 

        return url,classification_string

def list_possible_classes():
    return unique_values
    
#Script starts running here when server started due to function call in views.py file.

#Create empty list
data_for_dataframe = []

#Open CSV file containing classified websites
with open('classifier/scripts/training_websites.csv') as website_csv_file:
    website_csv_reader = csv.DictReader(website_csv_file)
    #Collect and clean HTML and append to data list
    for row in website_csv_reader:
        try:
            data_for_dataframe.append(class_collect_website(row['classification'],row['url']))
        except Exception:
            continue
#Create dataframe
htmlDF = pandas.DataFrame(data_for_dataframe)

#Array of unique classes of websites from training data
unique_values = htmlDF.classification.unique()

#Build up dictionary which maps classes to numerical representation
classification_dictionary = {}
for i in range(len(unique_values)): #For each unique classification
    classification_dictionary[unique_values[i]] = i #Add classification to dicionary along with increasing number mapping
 
#Replace classification name with number
htmlDF['classification'] = htmlDF.classification.map(classification_dictionary)
#htmlDF['message'] = htmlDF.message


count_vect = CountVectorizer()
counts = count_vect.fit_transform(htmlDF['message'])

transformer = TfidfTransformer().fit(counts)
counts = transformer.transform(counts)

#X_train, X_test, y_train, y_test = train_test_split(counts, htmlDF['classification'], test_size=0.3, random_state=69)
#model = MultinomialNB().fit(X_train, y_train)
#predicted = model.predict(X_test)

#Fit model using every classification and URL provided
model = MultinomialNB().fit(counts, htmlDF['classification'])
