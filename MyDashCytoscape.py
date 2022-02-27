import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import copy
from CreateGraphAndMax_weight_matching import CreateGraphAndMax_weight_matching
from MyDashBootStrap import MyDashBootStrap
from MyUtil import com_replace

class MyDashCytoscape(MyDashBootStrap):
  def buildbaselayout(self):

    # Step 1. NetworkXのGraphオブジェクトと重み最大マッチング結果リストを取得
    G, mw_list = CreateGraphAndMax_weight_matching()

    # Step 2. NetworkXのGraphオブジェクト ⇨ Cytoscape用のデータ形式
    cy_data = nx.readwrite.json_graph.cytoscape_data(G)

    # Step 3. Cytoscapeのデータ形式 ⇨ Dash Cytoscapeのデータ形式
    dash_cy_elements = cy_data["elements"]["nodes"] + cy_data["elements"]["edges"]

    aftele = copy.deepcopy(dash_cy_elements)
    for i in range(0, len(dash_cy_elements)):
      ele_list = dash_cy_elements[i]
      for ele_dict in ele_list:
        for dt in ele_list[ele_dict]:
          if "id" in ele_list[ele_dict].keys():
            # nodeの場合
            aftele[i][ele_dict]["id"] = com_replace(ele_list[ele_dict]["id"])
            aftele[i][ele_dict]["value"] = com_replace(ele_list[ele_dict]["value"])
            aftele[i][ele_dict]["name"] = com_replace(ele_list[ele_dict]["name"])+"さん"
            if "(1" in aftele[i][ele_dict]["id"]:
              # 突っ込みの場合
              aftele[i][ele_dict]["color"] = "red"
            else:
              # ボケの場合
              aftele[i][ele_dict]["color"] = "navy"
          else:
            # edgeの場合
            # idを付与する
            aftele[i][ele_dict]["id"] = com_replace(ele_list[ele_dict]["source"]) + "2" + com_replace(ele_list[ele_dict]["target"])
            aftele[i][ele_dict]["source"] = com_replace(ele_list[ele_dict]["source"])
            aftele[i][ele_dict]["target"] = com_replace(ele_list[ele_dict]["target"])
            # 線の太さの差異を強調する
            aftele[i][ele_dict]["weight_width"] = float(aftele[i][ele_dict]["weight"])*1.5
            # デフォルトカラー
            aftele[i][ele_dict]["color"] = "silver"
            for a in mw_list:
              # 重み最大マッチング結果に含まれる場合強調カラー
              if aftele[i][ele_dict]["source"] in set(a) and aftele[i][ele_dict]["target"] in set(a):
                aftele[i][ele_dict]["color"] = "black"
    
    elements = aftele
    # 設定値を確認したいとき
    #for ele in elements:
    #  print(ele)

    cyto_compo = cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={
            'name': 'circle','padding': 10
            # 'name': 'grid',"rows":2,"colmuns":5 # グリッドは枝の重みのラベルが重なりやすい
        },
        stylesheet=[{
            'selector': 'node',
            'style': {
                'width': '60px',
                'height': '60px',
                'content': 'data(name)',
                'pie-size': '80%',
                'background-color': 'data(color)',
            }
        }, {
            'selector': 'edge',
            'style': {
                'label': 'data(weight)',
                'width': 'data(weight_width)',
                'curve-style': 'bezier',
                #'target-arrow-shape': 'triangle', # 今回は無向グラフ
                'line-color': 'data(color)',
                'opacity': 0.5
            }
        }, {
            'selector': ':selected',
            'style': {
                'background-color': 'black',
                'line-color': 'black',
                'target-arrow-color': 'black',
                'source-arrow-color': 'black',
                'opacity': 1
            }
        }, {
            'selector': '.faded',
            'style': {
                'opacity': 0.25,
                'text-opacity': 0
            }
        }],
        style={
            'width': '100%',
            'height': '100%',
            'position': 'absolute',
            'left': 0,
            'top': 0
        }
    )
    return html.Div([cyto_compo])