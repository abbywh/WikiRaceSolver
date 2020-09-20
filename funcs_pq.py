import sqlite3
from xml.etree import ElementTree as ET
import spacy
nlp = spacy.load('en_core_web_md')
#Mainfile for testing shortest paths


#we precompute the graph in parser.py
def priority_place(queue,path,final):
    if queue is None:
        queue = [path]
        return
    if queue == []:
        queue.append(path)
        return
    node = path[-1]

    def bst(start,end) -> int:
        middle = (start+end) // 2
        print(middle)
        try:
             queue[middle+1]
        except:
            return middle
        if start>=end:
            return middle
        if len(queue[middle]) > len(path):
            return bst(start,middle-1)
        elif len(queue[middle]) < len(path):
            return bst(middle+1,end)
        else:
            if nlp(final).similarity(nlp(queue[middle+1][-1])) <= nlp(final).similarity(nlp(node)) and nlp(final).similarity(nlp(queue[middle][-1])) >= nlp(final).similarity(nlp(node)):
                return middle
            elif nlp(final).similarity(nlp(queue[middle+1][-1])) > nlp(final).similarity(nlp(node)):
                return bst(middle+1,end)
            else:
                return bst(start,middle-1)

    index = bst(0,len(queue)-1)
    queue.insert(index,path)
    print(index,path)
def valid(start,end,db):
    return get_adjlist(start,db) != [] and get_adjlist(end,db)!=[]

def get_adjlist(point,db):
    db.execute("SELECT links FROM links WHERE title =\'" + point.replace('\'','\'\'') +"\' LIMIT 1")
    return db.fetchall()

#modifieds queue, returns true if it unpacked anything
def unpack(to_unpack,queue,visited,final):
    try:
        f = ET.fromstring(to_unpack[-1])
    except:
        return False
    for element in f:
        if element.tag=="link":
            if element.text not in visited:
                priority_place(queue,to_unpack[0:-1]+[element.text],final)
                visited[element.text] = 1
    return True
def shortest_path(start,end,db):
    if not valid(start,end,db):
        return None
    visited  = {start: 1}
    queue = [[start]]
    while queue:
        v = queue.pop(0)
        #see if we need to unpack
        unpacked = unpack(v,queue,visited,end)
        if unpacked:
            if v+[end] in queue:
                return v+[end]
        elif v[-1].lower() == end.lower():
            return v
        else:
            for node in get_adjlist(v[-1],db):
                new_path = v+[node]
                #adds the adjacent nodes to the queue WITHOUT UNPACKING
                #lazy application
                if (len(new_path) < 4 and node not in visited):
                    queue.append(new_path)
                    visited[node] = 1
    return None


def test(db):
    assert(valid(" kfdnsaj","afs fnkdj",db)==False)
    assert(valid("anarchism","hierarchy",db)==True)
    assert(shortest_path(" kfdnsaj","afs fnkdj",db) is None)
    assert(shortest_path("dog","dog",db)==["dog"])
    assert(shortest_path("anarchism","hierarchy",db)==["anarchism", "hierarchy"])
    assert(shortest_path("anarchism","partially ordered set",db)==["anarchism", "hierarchy","partially ordered set"])
