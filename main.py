import requests #collect_html
import html2text #trim_html
import re # 

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

webpage_html_content = collect_html('http://www.brainjar.com/java/host/test.html')
cleaned_html_content_string = clean_html_text(webpage_html_content)
print(tokenize_string(cleaned_html_content_string))