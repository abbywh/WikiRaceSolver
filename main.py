import funcs_pq, funcs_hash, funcs_queue,wikiparse,pickle, time, sqlite3

try:
    conn =sqlite3.connect("graph.db")
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
except:
    print("Parsing db...")
    wikiparse.parse()

try:
    open('graph.pkl')
except:
    "Parsing pikl..."
    wikiparse.parse_pikl()

dir = input("Enter 1 for a Priority Queue, 2 for a Queue, 3 for a hashmap in memory\n")

if dir != "1" and dir != "2" and dir != "3":
    print("please enter a legal response.")
    exit()

start = input("Enter the starting path\n")

finish = input("Enter end path\n")

time_start = time.time()
if dir =="1":
    print(funcs_pq.shortest_path(start,finish,c))
if dir == "2":
    print(funcs_queue.shortest_path(start,finish,c))
else:
    data = funcs_hash.to_graph('graph.pkl')
    print(funcs_hash.shortest_path(start,finish,data))

print(time.time() - time_start)
