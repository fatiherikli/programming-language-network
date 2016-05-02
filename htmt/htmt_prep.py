import re
import sys
import networkx as nx
import os
reload(sys)
sys.setdefaultencoding("utf-8")

#0v2# JC Apr 18, 2016
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
filename_temp_csv=BASE_DIR+"/../static/htmt/temp/"+"144cufoff.csv"
gml_filename=BASE_DIR+"/../static/htmt/temp/"+"/jout.gml"


network = {
    "nodes": [],
    "links": []
}
node_id={}

class NestedDict(dict):
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, NestedDict()) 

def add_node(label, group, weight):
    id=len(network["nodes"])
    node_id[label]=int(id)

    node = {
        "name": label,
        "id": id,
        "group": group,
        "weight": weight,
    }
#        "size": weight
    network["nodes"].append(node)
    return node

def rawtxt2gml(filename,contents):
    oa=[]

    filename_out=filename_temp_csv
    fout=open(filename_out,'w')
    
    dd=NestedDict()
    node_size={}
    nodes=[]
    fp=False
    
    if contents:
        print "GOT LENGTH: "+str(len(contents))+" type: "+str(type(contents))
        #lines=re.split(r'\n',contents)
        lines=contents
    else:
        fp=open(filename,'r')
        lines=fp.readlines()
    
    for line in lines:
        line=re.sub(r'\n','',line)
        
        #"UYSAL M-NO PUB-9999" "APX J-NO PUB-9999" 11.0
        elem=re.split(r'\"',line)
        if len(elem)>3:
            try: mentions=int(float(re.sub(r'.*\" ','',line)))
            except:mentions=0
            
            fto=elem[1]
            tfrom=elem[3]
            
            to_name=re.sub(r' .*','',fto)
            to_pub=re.sub(r'^\w+ ','',fto)
            from_name=re.sub(r' .*','',tfrom)
            from_pub=re.sub(r'^\w+ ','',tfrom)

            #liner=to_name+","+to_pub+","+from_name+","+from_pub+","+str(mentions)
            #liner=to_name+" "+to_pub+","+from_name+" "+from_pub+","+str(mentions)+","+to_name+","+to_pub+","+from_name+","+from_pub
            liner=to_name+" "+to_pub+","+from_name+" "+from_pub+","+str(mentions)
            print liner

            fout.write(liner+"\n")

            node1=from_name+" "+from_pub
            node2=to_name+" "+to_pub
            
            #Rule for weight: node1+mentions, node2+1
            #    "Jordan"     "Jon" 11 so the node Jordan will be sized at 11 bc it is cited by Jon 11 times. 
            #    node2 to     node1 from
            if not node2 in node_size: node_size[node2]=mentions
            else: node_size[node2]+=mentions

            if not node1 in node_size: node_size[node1]=1 #minimum 1
            
            #Store for lookup
            dd[node1][node2]=mentions
            if not node1 in nodes:nodes.append(node1)
            if not node2 in nodes:nodes.append(node2)
            
            
    #Setup for GML
    #################
    
    graph = nx.MultiDiGraph()

    #Add nodes
    node_count=0
    for node in nodes:
        node_count+=1
        node_data=add_node(node,"group",node_size[node])
        graph.add_node(node.encode("utf-8"), node_data)

    
    #Add links
    for node1 in dd:
        for node2 in dd[node1]:
            edge_type="edge"
            network["links"].append({
                "source": node_id[node1],
                "target": node_id[node2],
                "type": edge_type,
            })

            mentions_n2n=dd[node1][node2]
            graph.add_edge(node1.encode("utf-8"),
                           node2.encode("utf-8"),
                           label="", weight=mentions_n2n)
                 
    nx.write_gml(graph, gml_filename)
    print "Outputed "+str(node_count)+" nodes to: "+gml_filename
        
    fout.close()
    if fp: fp.close()
    valid=True
    return oa,valid,gml_filename


if __name__ == '__main__':            
    filename="144cutoff.txt"
    rawtxt2gml(filename,"") #optional contents to pass
   



