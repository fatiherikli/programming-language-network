import sys
import json
import networkx as nx

reload(sys)
sys.setdefaultencoding("utf-8")

database = json.load(open("../data/data.json"))

GROUP_MAPPING = {
    "Influenced by": "Programming Language",
    "Designed by": "Computer Scientist",
    "Developer": "Foundation",
    "Dialects": "Dialect",
    "Major implementations": "Implementation",
    "Implementation language": "Programming Language",
}

network = {
    "nodes": [],
    "links": []
}


def calculate_node_weight(label):
    weight = 1
    data = database.get(label)

    if data and "Influenced" in data:
        weight += len(data["Influenced"])

    return weight


def add_node(label, group):
    node = {
        "name": label,
        "id": len(network["nodes"]),
        "group": group,
        "weight": calculate_node_weight(label)
    }
    network["nodes"].append(node)
    return node


def find_node_by_label(label):
    for node in network["nodes"]:
        if node["name"] == label:
            return node


def main():

    for language, properties in database.items():

        source_node = add_node(language, GROUP_MAPPING["Influenced by"])

        for edge_type, group in GROUP_MAPPING.iteritems():
            if edge_type in properties:
                nodes = properties[edge_type]

                for node in nodes:

                    if not node:
                        continue

                    target_node = find_node_by_label(node)

                    if not target_node:
                        target_node = add_node(node, group)

                    network["links"].append({
                        "source": source_node["id"],
                        "target": target_node["id"],
                        "type": edge_type,
                    })

    graph = nx.MultiDiGraph()
    for node in network["nodes"]:
        graph.add_node(node["name"].encode("utf-8"), node)

    for link in network["links"]:
        graph.add_edge(network["nodes"][link["source"]]["name"].encode("utf-8"),
                       network["nodes"][link["target"]]["name"].encode("utf-8"),
                       label=link["type"], weight=1)

    # set weights
    for source, target, payload in graph.edges(data=True):
        if payload["label"] == "Designed by":
            payload["weight"] += (graph.in_degree(target) * 4)

        if payload["label"] == "Developer":
            payload["weight"] += (graph.in_degree(target) * 2)

        if payload["label"] == "Dialect":
            payload["weight"] += 4

        if payload["label"] == "Major implementations":
            payload["weight"] += 3

        if payload["label"] == "Implementation language":
            payload["weight"] += 4

    nx.write_gml(graph, '../data/network.gml')


if __name__ == "__main__":
    main()
