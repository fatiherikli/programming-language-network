import json
import networkx as nx

graph_in="./jout_layoutg.gml"
graph_out="../data/network.json"
graph_out="jout.json"

def get_node_index(nodes, node_id):
    for index, node in enumerate(nodes):
        if node["id"] == node_id:
            return index
    raise IndexError

def main():
    graph = nx.read_gml(graph_in)

    nodes = [{
        "id": int(data['id']),
        "name": data.get("name") or "(Null)",
#        "group": data['group'],
        "group": "Publication",
        "x": data["graphics"]["x"],
        "y": data["graphics"]["y"],
        "w": data["graphics"]["w"],
        "h": data["graphics"]["h"],
        "weight": data["weight"],
        "fixed": True,
    } for _, data in graph.nodes(data=True)]

    links = [{
        "source": get_node_index(nodes, source),
        "target": get_node_index(nodes, target),
#        "name": data["label"],
        "name": "Mentions",
        "value": data["value"]
    } for source, target, data in graph.edges(data=True)]

    json.dump({
        "nodes": nodes,
        "links": links
    }, open(graph_out, "w"), indent=4)

if __name__ == "__main__":
    main()
