#https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve
import sqlite3, re
from lxml import etree


def index_table(cursor):
    print("index table")
    sql = ("CREATE INDEX title_index ON links (title);")
    cursor.execute(sql)

def retrieve_data():
    #run this to pull the necceessary data from wikipedia. Used to update.
    #must unzip yourself
    url='https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2'
    dest="wiki_multistream.xml.bz2"
    urlretrieve(url,dest)

def striptag(text):
    return text[text.find("}")+1:]

def build_xml(links):
    start = etree.Element('start')
    for link in links:
        child = etree.SubElement(start,'link')
        child.text = link
    return etree.tostring(start,encoding="unicode")

def filter_text(text):
    links = list()
    if text is None:
        return links
    for link in re.findall('\[[^\[]+?\]',text):
        if '|' in link:
            links.append(link[1:link.find("|")].lower())
        elif "http://" in link or "upload.wikimedia.org/" in link or "https://" in link:
            pass
        else:
            links.append(link[1:-1].lower())
    return links

def parse_pikl():
    graph = {}
    data_path = "wiki_multistream.xml"
    title = ""
    links = list()
    buffer=""
    collect=False
    n=0
    for event, elem in ET.iterparse(data_path, events = ('start','end')):
        tname = striptag(elem.tag)
        if collect==True:
            buffer = buffer + ("" if elem.text is None else elem.text)
        if event == 'start':
            if tname == 'title':
                title = ("" if elem.text is None else elem.text.lower())
            if tname == 'text':
                if elem.text is not None:
                    links= links + filter_text(elem.text)
                else:
                    collect=True
        if event == "end" and tname == 'text':
            links = links + filter_text(buffer)
            buffer=""
            collect=False
        if event == "end" and tname == 'page':
            n=n+1
            graph[title]=links
            title=""
            links=list()
            if (n%500000==0):
                print(n)
                with open('graph.pkl', 'ab+') as pkl_file:
                    pickle.dump(graph, pkl_file)
                    graph={}
        elem.clear()
    with open('graph.pkl', 'ab+') as pkl_file:
        pickle.dump(graph, pkl_file)
        graph={}
def parse():
    conn = sqlite3.connect('graph.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE links (title text, links text)''')
    data_path = "wiki_multistream.xml"
    title = ""
    links = list()
    buffer=""
    collect=False
    n=0
    for event, elem in ET.iterparse(data_path, events = ('start','end')):
        tname = striptag(elem.tag)
        if collect==True:
            buffer = buffer + ("" if elem.text is None else elem.text)
        if event == 'start':
            if tname == 'title':
                title = ("" if elem.text is None else elem.text.lower())
            if tname == 'text':
                if elem.text is not None:
                    links= links + filter_text(elem.text)
                else:
                    collect=True
        if event == "end" and tname == 'text':
            links = links + filter_text(buffer)
            buffer=""
            collect=False
        if event == "end" and tname == 'page':
            n=n+1
            title = title.replace("\"","\"\"")
            links = [link.replace("\"","\"\"") for link in links]
            link_xml = build_xml(links)
            try:
                c.execute("INSERT INTO links VALUES (\"" + title +"\",\""+link_xml+"\")")
            except:
                print("INSERT INTO links VALUES (\"" + title +"\",\""+link_xml+"\")")
             #put each title name, and then what it links to
            if (n%1000000==0):
                    print(n)
                    conn.commit()
            title=""
            links=list()
        elem.clear()
    conn.commit()
    conn.close()
