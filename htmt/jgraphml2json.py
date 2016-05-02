import os
import json
import networkx as nx

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

filename_output="network.json"
filename_output=BASE_DIR+"/../static/htmt/data/network.json"
#    }, open("../data/network.json", "w"), indent=4)

def get_node_index(nodes, node_id):
    for index, node in enumerate(nodes):
        if node["id"] == node_id:
            return index
    raise IndexError


def main():
    filename=BASE_DIR+"/../static/htmt/temp/gml_out.graphml"
    graph= nx.read_graphml(filename)
    #gml_to_json#  graph = nx.read_gml("../data/network.gml")

#    for _, data in graph.nodes(data=True):
#        print "Y: "+str(data)
#        print " iY: "+str(_)
#        data['']


#org    nodes = [{
#org        "id": data['id'],
#org        "id": _,
#org        "name": data.get("name") or "(Null)",
#org        "group": data['group'],
#org        "x": data["graphics"]["x"],
#org        "y": data["graphics"]["y"],
#org        "w": data["graphics"]["w"],
#org        "h": data["graphics"]["h"],
#org        "weight": data["weight"],
#org        "fixed": True,
#org    } for _, data in graph.nodes(data=True)]

    nodes = [{
        "id": _,
        "name": data.get("name") or "(Null)",
        "group": "Publication",
        "x": data["x"],
        "y": data["y"],
        "w": data["size"], #width
        "h": data["size"], #height
        "weight": data["weight"],
        "fixed": True,
    } for _, data in graph.nodes(data=True)]
    
    links = [{
        "source": get_node_index(nodes, source),
        "target": get_node_index(nodes, target),
        "name": "Mentions",#data["label"],
        "value": float(data["weight"])
    } for source, target, data in graph.edges(data=True)]
    
    for node in nodes:
        node['id']=int(float(node['id']))

    json.dump({
        "nodes": nodes,
        "links": links
    }, open(filename_output, "w"), indent=4)

if __name__ == "__main__":
    main()


