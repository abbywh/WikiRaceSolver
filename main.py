import sqlite3
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
#Mainfile for testing shortest paths


#we precompute the graph in parser.py
def valid(start,end,db):
    return get_adjlist(start,db) != [] and get_adjlist(end,db)!=[]

def get_adjlist(point,db):
    db.execute("SELECT links FROM links WHERE title =\'" + point.replace('\'','\'\'') +"\' LIMIT 1")
    return db.fetchall()

def to_list(v):
    ret = list()
    f = ET.fromstring(v[-1])
    for element in f:
        if element.tag=="link":
            ret.append(v[0:-1]+[element.text])
    return ret

def shortest_path(start,end,db):
    if not valid(start,end,db):
        return None
    queue = [[start]]
    while queue:
        v = queue.pop(0)
        try:
            unstack =to_list(v)
        except:
            unstack=[]
        if unstack != []:
            if (v[0:-1]+[end]) in unstack:
                return v[0:-1]+ [end]
            queue = queue+unstack
        elif v[-1].lower() == end.lower():
            return v
        else:
            for node in get_adjlist(v[-1],db):
                new_path = v+[node]
                queue.append(new_path)
    return None


def test(db):
    assert(valid(" kfdnsaj","afs fnkdj",db)==False)
    assert(valid("anarchism","hierarchy",db)==True)
    assert(shortest_path(" kfdnsaj","afs fnkdj",db) is None)
    assert(shortest_path("dog","dog",db)==["dog"])
    print("test 1")
    assert(shortest_path("anarchism","hierarchy",db)==["anarchism", "hierarchy"])
    print("test 2")
    assert(shortest_path("anarchism","partially ordered set",db)==["anarchism", "hierarchy","partially ordered set"])
    print(shortest_path("cat","partially ordered set",db))

database = "graph.db"
conn =sqlite3.connect(database)
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()

print(get_adjlist("benito mussolini",c))
test(c)
#print(shortest_path("adolf hitler","dog",c))
