import pickle, sys
#Mainfile for testing shortest paths


#we precompute the graph in parser.py
partition=0
def find_graph(point,graph):
    global partition
    init_part = partition
    partition = (init_part+1) % 21
    while point not in graph and init_part != partition:
        print(partition)
        graph = to_graph(str(partition)+'graph.pkl')
        partition = (partition+1) % 20
    return graph

def to_graph(datafile):
    graph = {}
    with open(datafile, 'rb') as pkl_file:
        while 1:
            try:
                graph = pickle.load(pkl_file)
            except:
                break
    return graph

def shortest_path(start,end,graph):
    queue = [[start]]
    while queue:
        v = queue.pop(0)
        if v[-1].lower() == end.lower():
            print(v)
            return v
        else:
            if v[-1] not in graph:
                graph = find_graph(v[-1],graph)
            for node in graph[v[-1]]:
                new_path = v+[node]
                queue.append(new_path)
    return None


def test(data):
    assert(shortest_path("dog","dog",data)==["dog"])
    print("test 1")
    assert(shortest_path("anarchism","hierarchy",data)==["anarchism", "hierarchy"])
    print("test 2")
    assert(shortest_path("anarchism","partially ordered set",data)==["anarchism", "hierarchy","partially ordered set"])
data = to_graph('0graph.pkl')
test(data)
