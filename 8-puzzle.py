import networkx as nx
from itertools import permutations
import heapq
import queue
import random



class Graph_8puzzle(nx.Graph):
    def __init__(self):
        super().__init__()                 #creating instance of graph

    def add_nodes(self): 
        nodes = permutations("012345678")
        for node in list(nodes):
            str = ''.join(node)
            self.add_node(str)

    def heuristic(self, h_fn, init_state, final_state):
        count = 0
        if(h_fn == 0):
            for i in range(9):
                if(init_state[i]!=final_state[i]):
                    count += 1
        else:
            for i in range(9):
                ind = final_state.find(init_state[i], 0, 8)
                row_f = int((ind)/3)
                row_i = int((i)/3)
                col_f = int((ind)%3)
                col_i = int((i)%3)
                count += (row_f-row_i)+(col_f-col_i)
        return count

    def add_edges(self):
        for node in self.nodes():
            ind = node.find('0',0,8)
            if ind == 0:
                self.add_edge(node, node[1]+'0'+node[2:])
                self.add_edge(node, node[3]+node[1:3]+'0'+node[4:])
            elif ind == 1:
                self.add_edge(node, '0'+node[0]+node[2:])
                self.add_edge(node, node[0]+node[2]+'0'+node[3:]) 
                self.add_edge(node, node[0]+node[4]+node[2:4]+'0'+node[5:])
            elif ind == 2:
                self.add_edge(node, node[0]+'0'+node[1]+node[3:])
                self.add_edge(node, node[0:2]+node[5]+node[3:5]+'0'+node[6:])
            elif ind == 3:
                self.add_edge(node, '0'+node[1:3]+node[0]+node[4:])
                self.add_edge(node, node[0:3]+node[4]+'0'+node[5:])
                self.add_edge(node, node[0:3]+node[6]+node[4:6]+'0'+node[7:])
            elif ind == 4:
                self.add_edge(node, node[0:3]+'0'+node[3]+node[5:])
                self.add_edge(node, node[0]+'0'+node[2:4]+node[1]+node[5:])
                self.add_edge(node, node[0:3]+'0'+node[3]+node[5:])
                self.add_edge(node, node[0:4]+node[7]+node[5:7]+'0'+node[8])
            elif ind == 5:
                self.add_edge(node, node[0:2]+'0'+node[3:5]+node[2]+node[6:])
                self.add_edge(node, node[0:4]+'0'+node[4]+node[6:])
                self.add_edge(node, node[0:5]+node[8]+node[6:8]+'0')
            elif ind == 6:
                self.add_edge(node, node[0:3]+'0'+node[4:6]+node[3]+ node[7:])
                self.add_edge(node, node[0:6]+node[7]+'0'+node[8])
            elif ind == 7:
                self.add_edge(node, node[0:4]+'0'+node[5:7]+node[4]+node[8])
                self.add_edge(node, node[0:6]+'0'+node[6]+node[8])
                self.add_edge(node, node[0:7]+node[8]+'0')
            elif ind == -1:
                self.add_edge(node, node[0:5]+'0'+node[6:8]+node[5])
                self.add_edge(node, node[0:7]+'0'+node[7])

    def expand(self, state, final_state, pq, depth, h_fn, distance_g, parent):
        q = queue.Queue(maxsize=400000)
        q.put((0,state))                                                                    #pushing depth of state (i.e. 0 initially) and the state. current_state[0]=depth and current_state[1]=node
        count=0
        while not q.empty():                                                                
            current_state = q.get() 
            if depth == current_state[0]:
                break
            for node in self.neighbors(current_state[1]):
                node_gdist =  distance_g[current_state[1]] + 1 
                if (node not in distance_g) or (distance_g[node] > (node_gdist)):
                    q.put((current_state[0]+1,node))
                    parent[node] = current_state[1]
                    distance_g[node] = node_gdist                                                               #updated g distance 
                    count = count+1

                    if node == final_state:
                        f_val = distance_g[node] 
                        heapq.heappush(pq, (f_val, node))
                        break

                    if depth == (current_state[0]+1):
                        f_val = distance_g[node] + self.heuristic(h_fn, node, final_state)
                        heapq.heappush(pq, (f_val, node))
        return count


    def astar(self, init_state, final_state, depth, h_fn, parent):
        distance_g={}
        pq = [(0,init_state)]           #priority queue initialization
        distance_g[init_state] = 0
        parent[init_state] = "-1"
        tot_nodes_gen = 1                 #total nodes generated inititalization
        max_len_fringe = 1                #maximum length of fringe (i.e. max-space occupied by priority queue) initialization

        current_state = (0, init_state) #declaring outside for scope purpose
        while pq != []:
            if max_len_fringe < len(pq):
                max_len_fringe = len(pq)

            current_state = heapq.heappop(pq)
            if current_state[1] == final_state:
                break
            else:
                tot_nodes_gen += self.expand(current_state[1], final_state, pq, depth, h_fn, distance_g, parent)

        if current_state[1] != final_state:                        
            print(f"current_state is {current_state[1]}")
            return (tot_nodes_gen, max_len_fringe, 0)
        else:
            return (tot_nodes_gen, max_len_fringe, 1)

    def giveAstarpath(self, parent, path, final_state):
        node = final_state
        while node != "-1":
           path.append(node)
           node = parent[node]

    def genTestcase(self, final_state):
        node = final_state
        l = random.randint(1, 100)

        for i in range(l):
            node = random.choice(list(self.neighbors(node)))

        d = random.randint(1, l)
        return (node, d)




print("\n\n****PROGRAM STARTS****")

G = Graph_8puzzle()
G.add_nodes()
G.add_edges()
final_state = "012345678" 

for i in range(10):
    print(f"\n\n\nTESTCASE NO. {i}")
    init_state, depth = G.genTestcase(final_state)
    print("\n")
    print(f"Initial state : {init_state}")
    print(f"Final state   : {final_state} ")
    print(f"Depth         : {depth}")
    exception=0
    try:
        expected_path = nx.astar_path(G, init_state, final_state) 
    except:
        exception=1


    h_fn=1
    parent = {}
    comp_cost = G.astar(init_state, final_state, depth, h_fn, parent)
    tot_nodes_gen = comp_cost[0]
    max_len_fringe = comp_cost[1]

    print("\n")
    print(f"Computational Costs Manhattan heuristic with depth d:")
    print(f"Total nodes generated     - {tot_nodes_gen}")
    print(f"Maximum length of fringe  - {max_len_fringe}")

    if comp_cost[2] == 1: 
        path = []
        G.giveAstarpath(parent, path, final_state)
        path.reverse()
        print(f"Length of Path calculated : {len(path)-1}")
        print(f"Calculated path           : {path}\n")
        print(f"Expected path length      : {len(expected_path)-1}")
        print(f"Expected Path             : {expected_path}\n")
    else:
        print(f"Calculated by custom function that cannot reach goal state")
        if exception == 1: 
            print(f"By using built-in function that cannot reach goal state")
        else:
            print(f"Expected path length      : {len(expected_path)-1}")
            print(f"Expected Path             : {expected_path}\n")





    h_fn=0
    parent = {}
    comp_cost = G.astar(init_state, final_state, depth, h_fn, parent)
    tot_nodes_gen = comp_cost[0]
    max_len_fringe = comp_cost[1]

    print("\n")
    print(f"Computational Costs Mismatch heuristic with depth d :")
    print(f"Total nodes generated     - {tot_nodes_gen}")
    print(f"Maximum length of fringe  - {max_len_fringe}")

    if comp_cost[2] == 1: 
        path = []
        G.giveAstarpath(parent, path, final_state)
        path.reverse()
        print(f"Length of Path calculated : {len(path)-1}")
        print(f"Calculated path           : {path}\n")
        print(f"Expected path length      : {len(expected_path)-1}")
        print(f"Expected Path             : {expected_path}\n")
    else:
        print(f"Calculated by custom function that cannot reach goal state")
        if exception == 1: 
            print(f"By using built-in function that cannot reach goal state")
        else:
            print(f"Expected path length      : {len(expected_path)-1}")
            print(f"Expected Path             : {expected_path}\n")


    h_fn=1
    parent = {}
    comp_cost = G.astar(init_state, final_state, 1, h_fn, parent)
    tot_nodes_gen = comp_cost[0]
    max_len_fringe = comp_cost[1]

    print("\n")
    print(f"Computational Costs Manhattan heuristic with depth 1:")
    print(f"Total nodes generated     - {tot_nodes_gen}")
    print(f"Maximum length of fringe  - {max_len_fringe}")

    if comp_cost[2] == 1: 
        path = []
        G.giveAstarpath(parent, path, final_state)
        path.reverse()
        print(f"Length of Path calculated : {len(path)-1}")
        print(f"Calculated path           : {path}\n")
        print(f"Expected path length      : {len(expected_path)-1}")
        print(f"Expected Path             : {expected_path}\n")
    else:
        print(f"Calculated by custom function that cannot reach goal state")
        if exception == 1: 
            print(f"By using built-in function that cannot reach goal state")
        else:
            print(f"Expected path length      : {len(expected_path)-1}")
            print(f"Expected Path             : {expected_path}\n")





    h_fn=0
    parent = {}
    comp_cost = G.astar(init_state, final_state, 1, h_fn, parent)
    tot_nodes_gen = comp_cost[0]
    max_len_fringe = comp_cost[1]

    print("\n")
    print(f"Computational Costs Mismatch heuristic with depth 1 :")
    print(f"Total nodes generated     - {tot_nodes_gen}")
    print(f"Maximum length of fringe  - {max_len_fringe}")

    if comp_cost[2] == 1: 
        path = []
        G.giveAstarpath(parent, path, final_state)
        path.reverse()
        print(f"Length of Path calculated : {len(path)-1}")
        print(f"Calculated path           : {path}\n")
        print(f"Expected path length      : {len(expected_path)-1}")
        print(f"Expected Path             : {expected_path}\n")
    else:
        print(f"Calculated by custom function that cannot reach goal state")
        if exception == 1: 
            print(f"By using built-in function that cannot reach goal state")
        else:
            print(f"Expected path length      : {len(expected_path)-1}")
            print(f"Expected Path             : {expected_path}\n")

    #print(f"Total number of nodes in graph is {G.number_of_nodes()}")

    #for edge in G.edges():
    #    print(f"{edge} {len(edge[0])} {len(edge[1])}")

    #print(f"Total number of edges present in Graph is {G.number_of_edges()}")

