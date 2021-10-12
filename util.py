import copy
from networkx.algorithms.community import k_clique_communities
from LT import *
from icommunity.community_louvain import *


def Initial_Blocks(G, k_cli):
    dictclique = dict()
    listpart = list(k_clique_communities(G, k_cli))
    for i in range(len(listpart)):
        # print i, listpart[i]
        for node in listpart[i]:
            dictclique[node] = i
        # print (dictclique)

    nodestmp = set(dictclique.keys())
    nodes = set(G.nodes())
    nodes_rest = nodes - nodestmp

    maxcomID = len(listpart)
    # print maxcomID
    for node in nodes_rest:
        dictclique[node] = maxcomID
        maxcomID = maxcomID + 1
    return dictclique


def read_cover(filename):
    cover = {}
    global S
    nodes = set()
    with open(filename) as f:
        for line in f:
            node, c = line.split()
            nodes.add(node)
            if c not in cover:
                cover[c] = {node}
            else:
                cover[c].add(node)
    S = len(nodes)
    return cover, nodes


def mutual_info(c_A, c_B):
    N_mA = len(c_A)
    N_mB = len(c_B)
    # print  "CA",c_A
    # print  "CB",c_B
    I_num = 0
    for i in c_A:
        for j in c_B:
            n_i = len(c_A[i])
            n_j = len(c_B[j])
            n_ij = len(c_A[i] & c_B[j])
            if n_ij == 0:
                continue
            log_term = math.log((n_ij * S * 1.0) / (n_i * n_j))

            I_num += n_ij * log_term
    I_num *= -2

    I_den = 0
    for i in c_A:
        n_i = len(c_A[i])
        I_den += n_i * math.log(n_i * 1.0 / S)

    for j in c_B:
        n_j = len(c_B[j])
        I_den += n_j * math.log(n_j * 1.0 / S)

    I = I_num / I_den
    return I


####################################

def Reassemble_Modularity_Optimization(G, Initial_Partition):
    # part= Move_Nodes(G, Initial_Partition)
    # dictfoundcomm=dict()
    # for k,v in part.items():
    # if v not in dictfoundcomm:
    # dictfoundcomm[v] = set([k])
    # else:
    # dictfoundcomm[v].add(k)
    # return dictfoundcomm
    part = Move_Nodes_Modularity(G, Initial_Partition)
    return part


def Reassemble_Influence_Spread(G, Partition, T_simu, delta):
    G_d = nx.DiGraph()
    for (u, v) in G.edges():
        try:
            G_d[u][v]['weight'] += 1
        except KeyError:
            G_d.add_edge(u, v, weight=1)
        try:
            G_d[v][u]['weight'] += 1
        except KeyError:
            G_d.add_edge(v, u, weight=1)
    n = G_d.number_of_nodes()
    Ewu = uniformWeights(G_d)

    Target = dict()
    S = list()
    for i_node, com in Partition.items():  # (Partition.items(), key=lambda d:d[0], reverse = False):
        S = []
        T_i = dict()
        Target[i_node] = T_i
        S.append(i_node)
        for t in range(0, T_simu, 1):
            T = runLT(G_d, S, Ewu)
            for j in range(0, len(T), 1):
                t = T[j]
                # if T_i.has_key(t):
                if t in T_i:
                    T_i[t] = T_i[t] + 1
                else:
                    T_i[t] = 1
        # print (Target[i_node])
    part = dict()
    for k, v in Partition.items():
        if v not in part:
            part[v] = {k}
        else:
            part[v].add(k)
    # return dictfoundcomm

    exp_com = dict()
    for k, com in part.items():
        new_com = copy.deepcopy(com)
        for node in com:
            dictnode = Target[node]
            for key, freq in dictnode.items():
                if freq >= delta:
                    new_com.add(key)
        exp_com[k] = new_com
    overlapcom = mincover(exp_com)

    return overlapcom


def changdu(item):
    return len(item)


def mincover(dictcomm):
    dict1 = dict()
    listtmp = list(dictcomm.values())

    listtmp.sort(key=changdu, reverse=False)

    i = 0
    while i < len(listtmp) - 1:
        j = i + 1
        while j < len(listtmp):
            if listtmp[i].issubset(listtmp[j]):
                listtmp.remove(listtmp[i])
                i -= 1
                # print i
                break
            j += 1
        i += 1
    for i in range(len(listtmp)):
        dict1[i] = listtmp[i]

    return dict1
