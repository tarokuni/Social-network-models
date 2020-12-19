import networkx as nx
import matplotlib.pyplot as plt
import random as rd

# Parameters

LAMBDA_1 = 0.5 # Connetction probability for influential nodes
LAMBDA_2 = 0.1 # Connetction probability for noninfluential nodes
NODES = 500 # Number of nodes
INFL = 3 # Number of influential nodes
ROBUST = 1 #How robust influential nodes are

# Initialize

network = nx.DiGraph()

for i in range(NODES):
    network.add_node(i, opinion=rd.uniform(-1,1), influential=False)

inf_op = []
for i in rd.sample(range(NODES), INFL):
    network.nodes[i]['influential'] = True
    inf_op.append(network.nodes[i]['opinion'])

inf_var = max(inf_op) - min(inf_op)

# Create network and update opinion
def create_network():
    for i in network.nodes():
        for j in network.nodes():
            if i != j:
                if network.nodes[i]['influential'] == True \
                    and abs(network.nodes[i]['opinion']-network.nodes[j]['opinion']) < LAMBDA_1 \
                    and rd.uniform(0,1) < 0.95:
                    network.add_edge(i, j)

                elif network.nodes[i]['influential'] == False \
                    and abs(network.nodes[i]['opinion']-network.nodes[j]['opinion']) < LAMBDA_2 \
                    and rd.uniform(0,1) < 0.05:
                    network.add_edge(i, j)

def update_network():
    for i in network.nodes(): # influencer
        inf_neighbor = []
        non_inf_neighbor = []
        for j in network.nodes():
            if i != j:
                if abs(network.nodes[i]['opinion']-network.nodes[j]['opinion']) < LAMBDA_1:
                    inf_neighbor.append(j)
                if abs(network.nodes[i]['opinion']-network.nodes[j]['opinion']) < LAMBDA_2:
                    non_inf_neighbor.append(j)
     
        i_succ = []
        i_succ[:] = network.successors(i)
        for j in i_succ: # influencee
            if network.nodes[i]['influential'] == True \
                    and network.nodes[j]['influential'] == True \
                    and rd.uniform(0,1) < 0.05:
                network.remove_edge(i, j)
                rd.shuffle(inf_neighbor)
                for connect_cand in inf_neighbor:
                    if (i, connect_cand) not in network.edges():
                        network.add_edge(i, connect_cand)
                        break

            elif network.nodes[i]['influential'] == True \
                    and network.nodes[j]['influential'] == False \
                    and rd.uniform(0,1) < 0.1:
                network.remove_edge(i, j)        
                rd.shuffle(inf_neighbor)        
                for connect_cand in inf_neighbor:
                    if (i, connect_cand) not in network.edges():
                        network.add_edge(i, connect_cand)
                        break

            elif network.nodes[i]['influential'] == False \
                    and network.nodes[j]['influential'] == True \
                    and rd.uniform(0,1) < 0.00:
                network.remove_edge(i, j)
                rd.shuffle(non_inf_neighbor)
                for connect_cand in non_inf_neighbor:
                    if (i, connect_cand) not in network.edges():
                        network.add_edge(i, connect_cand)
                        break

            elif network.nodes[i]['influential'] == False \
                    and network.nodes[j]['influential'] == False \
                    and rd.uniform(0,1) < 0.5:
                network.remove_edge(i, j)                
                rd.shuffle(non_inf_neighbor)
                for connect_cand in non_inf_neighbor:
                    if (i, connect_cand) not in network.edges():
                        network.add_edge(i, connect_cand)
                        break


def update_opinion():
    opinion_temp = []
    for i in network.nodes():
        if network.nodes[i]['influential'] == True:
            normfac = network.in_degree(i) + ROBUST
            opinion_temp.append(network.nodes[i]['opinion']*ROBUST/normfac)
            for j in network.predecessors(i):
                opinion_temp[i] = opinion_temp[i] + network.nodes[j]['opinion']/normfac
        elif network.nodes[i]['influential'] == False:
            normfac = network.in_degree(i) + 1
            opinion_temp.append(network.nodes[i]['opinion']/normfac)
            for j in network.predecessors(i):
                opinion_temp[i] = opinion_temp[i] + network.nodes[j]['opinion']/normfac           

    for i in network.nodes():
        network.nodes[i]['opinion'] = opinion_temp[i]

if __name__ == "__main__":
    create_network()
    update_opinion()
    for i in range(50):
        update_network()
        update_opinion()


    opinions = []
    for node in network.nodes():
       opinions.append(network.nodes[node]['opinion'])
    plt.hist(opinions, range=(-1, 1))

    # node_color = []
    # node_size = []
    # for i in network.nodes():
    #     if network.nodes[i]['influential'] == True:
    #         node_color.append('red')
    #         node_size.append(5)
    #     elif network.nodes[i]['influential'] == False:
    #         node_color.append('blue')
    #         node_size.append(2)
    # nx.draw(network, node_color=node_color, node_size=node_size)

    plt.show()
