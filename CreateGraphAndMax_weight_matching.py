import networkx as nx
from CreateGraph import CreateGraph
from MyUtil import com_replace

def CreateGraphAndMax_weight_matching():
    G = CreateGraph()
    
    # 重み最大マッチング
    mw = nx.max_weight_matching(G)

    # 扱いやすいように重み最大マッチングの結果のノード名を置換してリストに格納する
    mw_list = []
    for a in mw:
      fromtolist = []
      for b in a:
        fromtolist.append((com_replace(b)))
      mw_list.append(fromtolist)
    
    return G, mw_list