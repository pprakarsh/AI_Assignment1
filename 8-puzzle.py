import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
import heapq

print("Initial state and Final state have to be entered as a string.\n For example 120365487 deonotes first 3 characters represent first row, characters at pos 4,5,6 as elements of second row and last 3 characters last row\n")
init_state = input("Please enter the initial state of the Puzzle: ")
final_state = input("Please enter the final state of the Puzzle: ")

depth = int(input("Please enter depth of the bfs expand: "))
h_fn = int(input("Input 0 for mismatch heuristic and 1 for manhattan heuristic: "))

def heuristic(h_fn, init_state, final_state):
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

G = nx.Graph() #creating instance of graph
nodes = permutations("012345678")
for node in list(nodes):
    str = ''.join(node)
    G.add_node(str)

print(f"Total number of nodes in graph is {G.number_of_nodes()}")

for node in G.nodes():
    ind = node.find('0',0,8)
    if ind == 0:
        G.add_edge(node, node[1]+'0'+node[2:], weight=1)
        G.add_edge(node, node[3]+node[1:3]+'0'+node[4:], weight=1)
    elif ind == 1:
        G.add_edge(node, '0'+node[0]+node[2:], weight=1)
        G.add_edge(node, node[0]+node[2]+'0'+node[3:], weight=1) 
        G.add_edge(node, node[0]+node[4]+node[2:4]+'0'+node[5:], weight=1)
    elif ind == 2:
        G.add_edge(node, node[0]+'0'+node[1]+node[3:], weight=1)
        G.add_edge(node, node[0:2]+node[5]+node[3:5]+'0'+node[6:], weight=1)
    elif ind == 3:
        G.add_edge(node, '0'+node[1:3]+node[0]+node[4:], weight=1)
        G.add_edge(node, node[0:3]+node[4]+'0'+node[5:], weight=1)
        G.add_edge(node, node[0:3]+node[6]+node[4:6]+'0'+node[7:], weight=1)
    elif ind == 4:
        G.add_edge(node, node[0:3]+'0'+node[3]+node[5:], weight=1)
        G.add_edge(node, node[0]+'0'+node[2:4]+node[1]+node[5:], weight=1)
        G.add_edge(node, node[0:3]+'0'+node[3]+node[5:], weight=1)
        G.add_edge(node, node[0:4]+node[7]+node[5:7]+'0'+node[8], weight=1)
    elif ind == 5:
        G.add_edge(node, node[0:2]+'0'+node[3:5]+node[2]+node[6:], weight=1)
        G.add_edge(node, node[0:4]+'0'+node[4]+node[6:], weight=1)
        G.add_edge(node, node[0:5]+node[8]+node[6:8]+'0', weight=1)
    elif ind == 6:
        G.add_edge(node, node[0:3]+'0'+node[4:6]+node[3]+ node[7:], weight=1)
        G.add_edge(node, node[0:6]+node[7]+'0'+node[8], weight=1)
    elif ind == 7:
        G.add_edge(node, node[0:4]+'0'+node[5:7]+node[4]+node[8], weight=1)
        G.add_edge(node, node[0:6]+'0'+node[6]+node[8], weight=1)
        G.add_edge(node, node[0:7]+node[8]+'0', weight=1)
    elif ind == -1:
        G.add_edge(node, node[0:5]+'0'+node[6:8]+node[5], weight=1)
        G.add_edge(node, node[0:7]+'0'+node[7], weight=1)

#for edge in G.edges():
#    print(f"{edge} {len(edge[0])} {len(edge[1])}")

print(f"Total number of edges present in Graph is {G.number_of_edges()}")

print(nx.astar_path(G, init_state, final_state))
