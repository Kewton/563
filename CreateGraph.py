import networkx as nx
def CreateGraph():
    G = nx.Graph()

    # ※networkxにてgridグラフでの表現出来るように(x座標, y座標)のタプルで各ノードを定義
    # ※dash_cytoscapeでcricleで可視化する際、ノード名の昇順で反時計回りに並べていると思われる

    # 5人のボケ
    B_1 = (0,4)
    B_2 = (0,3)
    B_3 = (0,2)
    B_4 = (0,1)
    B_5 = (0,0)

    # 5人の突っ込み
    T_1 = (1,4)
    T_2 = (1,3)
    T_3 = (1,2)
    T_4 = (1,1)
    T_5 = (1,0)

    # ノードを追加
    G.add_node(B_1)
    G.add_node(B_2)
    G.add_node(B_3)
    G.add_node(B_4)
    G.add_node(B_5)
    G.add_node(T_1)
    G.add_node(T_2)
    G.add_node(T_3)
    G.add_node(T_4)
    G.add_node(T_5)

    # 各ボケから見た突っ込みの上位３人
    B_edge_weight = {}
    B_edge_weight[(B_1, T_1)]=3
    B_edge_weight[(B_1, T_2)]=2
    B_edge_weight[(B_1, T_3)]=1

    B_edge_weight[(B_2, T_2)]=3
    B_edge_weight[(B_2, T_3)]=2
    B_edge_weight[(B_2, T_4)]=1

    B_edge_weight[(B_3, T_1)]=3
    B_edge_weight[(B_3, T_2)]=2
    B_edge_weight[(B_3, T_3)]=1

    B_edge_weight[(B_4, T_2)]=3
    B_edge_weight[(B_4, T_3)]=2
    B_edge_weight[(B_4, T_1)]=1

    B_edge_weight[(B_5, T_2)]=3
    B_edge_weight[(B_5, T_3)]=2
    B_edge_weight[(B_5, T_1)]=1

    # 各突っ込みから見たボケの上位３人
    T_edge_weight = {}
    T_edge_weight[(B_1, T_1)]=3
    T_edge_weight[(B_2, T_1)]=2
    T_edge_weight[(B_4, T_1)]=1

    T_edge_weight[(B_2, T_2)]=3
    T_edge_weight[(B_1, T_2)]=2
    T_edge_weight[(B_3, T_2)]=1

    T_edge_weight[(B_5, T_3)]=3
    T_edge_weight[(B_2, T_3)]=2
    T_edge_weight[(B_1, T_3)]=1

    T_edge_weight[(B_1, T_4)]=3
    T_edge_weight[(B_2, T_4)]=2
    T_edge_weight[(B_3, T_4)]=1

    T_edge_weight[(B_3, T_5)]=3
    T_edge_weight[(B_2, T_5)]=2
    T_edge_weight[(B_5, T_5)]=1

    for (u,v) in B_edge_weight:
      G.add_edge(u, v)

    for (u,v) in T_edge_weight:
      G.add_edge(u, v)

    def getval(_edge_weight, _u, _v):
      if (_u, _v) in _edge_weight.keys():
        return _edge_weight[_u, _v]
      else:
        return 0

    for (u,v) in G.edges:
      # ボケからみた突っ込み評価点と突っ込みから見たボケの評価点を加算して重みとする
      G[u][v]["weight"] = getval(B_edge_weight,u,v) + getval(T_edge_weight,u,v)
    
    return G