#Task1
f1= open("input1.txt", 'r')
input_lines= f1.readlines()
height,width= map(int, input_lines[0].split())
entry_r, entry_c= map(int, input_lines[1].split())
exit_r, exit_c= map(int, input_lines[2].split())
#print(height, width, entry_r, entry_c, exit_r, exit_c)

import heapq

def heuristic_func(x, y):
    h= abs(x[0] - x[1]) + abs(y[0] - y[1])
    return(h)

Maze_list= []
for i in range(height):
    idx_line= input_lines[i + 3].strip()
    Maze_list.append(list(idx_line))
#print(Maze_list) -> [['#', '#', '#', '0', '#', '#', '#', '#'], ['#', '0', '0', '0', '0', '0', '0', '#'], ['#', '#', '#', '0', '#', '0', '0', '#'], ['#', '0', '0', '0', '#', '0', '0', '#'], ['#', '0', '#', '#', '#', '#', '#', '#'], ['#', '0', '0', '0', '0', '0', '0', '#'], ['#', '#', '#', '#', '#', '0', '#', '#']]

actions= {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

start_node= (entry_r, entry_c)
end_node= (exit_r, exit_c)
visited_tracker= set()
path_cost= {start_node: 0} #Dictionary for storing all the path costs for shortest path check 
priority= [(heuristic_func(start_node, end_node), 0, start_node, '')] #h(n), g(n), current node and sequence of action

goal_reached= False
while len(priority) > 0: #A* search
    H_of_n, G_of_n, current_node, action_seq= heapq.heappop(priority)
    if current_node== end_node:
        print(G_of_n)
        print(action_seq)
        goal_reached= True
        break
    if current_node not in visited_tracker:
        visited_tracker.add(current_node)
    elif current_node in visited_tracker:
        continue
    
    for action, (r,c) in actions.items():
        r_next= current_node[0] + r
        c_next= current_node[1] + c
        if Maze_list[r_next][c_next] == '#': #Block check
            continue
        if (height <= r_next < 0 and width <= c_next < 0): #Next node within boundary or not
            continue
        next_node= (r_next, c_next)
        updated_G_of_n= G_of_n + 1

        if next_node not in path_cost or updated_G_of_n < path_cost[next_node]: #Search for a better way or a new node
            path_cost[next_node]= updated_G_of_n
            heapq.heappush(priority, (updated_G_of_n + heuristic_func(next_node, end_node), updated_G_of_n, next_node, action_seq + action))

if goal_reached== False:
    print(-1)
f1.close()


#Task2
f2= open("input2.txt", 'r')
input_lines= f2.readlines()
vertices, edge= map(int, input_lines[0].split())
init_vertex, goal_vertex= map(int, input_lines[1].split())

heuristic_val= {}
edge_connection= {}

i= 2
while i < (2+vertices):
    vertex, val= map(int, input_lines[i].split())
    heuristic_val[vertex]= val
    i= i+1

j= i
while j < (i+edge):
    vertex_1, vertex_2= map(int, input_lines[j].split())
    if vertex_1 not in edge_connection:
        edge_connection[vertex_1]= []
    if vertex_2 not in edge_connection:
        edge_connection[vertex_2]= []
    edge_connection[vertex_1].append(vertex_2) 
    edge_connection[vertex_2].append(vertex_1)
    j= j+1

def breath_first_search(start_node, goal_node, edge_connection, vertices):
    Queue= [start_node]
    actual_distance= [-1] * (vertices+1) #-1 for infinity
    visited_node_list= [0] * (vertices+1) #0 for False
    visited_node_list[start_node]= 1 #1 for True
    actual_distance[start_node]= 0

    idx= 0
    while idx < len(Queue):
        Node= Queue[idx]
        idx= idx+1
        for Next_Node in edge_connection.get(Node, []):
            if visited_node_list[Next_Node]== 0:
                actual_distance[Next_Node]= actual_distance[Node]+1
                visited_node_list[Next_Node]= 1
                Queue.append(Next_Node)
    return actual_distance[goal_node]

Not_admissible_nodes= []
Node= 1
while Node < (vertices+1):
    actual_distance= breath_first_search(Node, goal_vertex, edge_connection, vertices)
    if heuristic_val[Node] <= actual_distance:
        pass
    else:
        Not_admissible_nodes.append(Node)
    Node= Node+1

if len(Not_admissible_nodes) != 0:
    print(0)
    if len(Not_admissible_nodes)== 1:
        print(f'Here node {Not_admissible_nodes[0]} is inadmissible.')
    else:
        print("Here nodes", end= ' ')
        for i in range(len(Not_admissible_nodes)-1):
            print(Not_admissible_nodes[i], end=', ')
        print(f'and {Not_admissible_nodes[-1]} are inadmissible.')
else:
    print(1)
f2.close()