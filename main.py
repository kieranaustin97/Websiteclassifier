import requests #collect_html
import html2text # trim_html

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
        clean_html_text = html_text.replace("\n", " ")
        return clean_html_text              #Return cleaned html text from html string

    except Exception as clean_html_text_err:
        print(clean_html_text_err)          #Print error message

webpage_html_content = collect_html('https://www.york.ac.uk/teaching/cws/wws/webpage1.html')
clean_html_text(webpage_html_content)