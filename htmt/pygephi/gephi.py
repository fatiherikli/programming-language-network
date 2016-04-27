#/usr/local/bin/jython
import java
import os, glob, sys
import classpath; 
path = os.path.realpath(__file__)
toolkit = os.path.join(os.path.dirname(path), 'gephi-toolkit.jar')
classpath.addFile(toolkit)
# TODO: need /Users/jason/Code/gephi/toolkit/gephi-toolkit/org-openide-util.jar?

# necessary for save - there should be a less scattershot way to do this?
#for j in glob.glob('/Users/jason/Code/gephi/platform/platform/modules/*.jar'): classpath.addFile(j)

import org.openide.util.Lookup as Lookup
Lookup = Lookup.getDefault().lookup


RELAX_STEPS=1000#5000


def lookup(name, namespace='org.gephi.'):
    return Lookup(java.lang.Class.forName(namespace + name))

ProjectController = lookup('project.api.ProjectController')
ExportController = lookup('io.exporter.api.ExportController')
ImportController = lookup('io.importer.api.ImportController')
GraphController = lookup('graph.api.GraphController')
PreviewController = lookup('preview.api.PreviewController')


"""
http://pastebin.com/nFX0jHFV
import org.gephi.project.api as project
import org.gephi.data.attributes.api as attributes
import org.gephi.filters.api as filters
import org.gephi.graph.api as graph
import org.gephi.io.exporter.api as exporter
import org.gephi.io.generator.api as generator
import org.gephi.io.importer.api as importer
import org.gephi.layout.api as layout
import org.gephi.partition.api as partition
import org.gephi.preview as preview
import org.gephi.project.api as project
import org.gephi.ranking.api as ranking
import org.gephi.statistics as statistics
import org.gephi.utils as utils
"""
def show():
    """ adapted from here: http://wiki.gephi.org/index.php/Toolkit_-_Reuse_the_Preview_Applet"""
    from javax.swing import JFrame
    from java.awt import BorderLayout

    pc = PreviewController
    pc.refreshPreview();
     
    # New Processing target, get the PApplet
    target = pc.getRenderTarget("processing")
    applet = target.getApplet()
    applet.init()
     
    # Refresh the preview and reset the zoom
    try:
        pc.render(target) 
    except Exception:
        # throws sun.dc.pr.PRError: sun.dc.pr.PRError: setPenT4: invalid pen transformation (singular)
        pass
    target.refresh()
    target.resetZoom()
     
    # Add the applet to a JFrame and display
    frame = JFrame("Preview")
    frame.setLayout(BorderLayout())
     
    # frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
    frame.add(applet, BorderLayout.CENTER)
     
    frame.pack()
    frame.setVisible(True)

def adjust_sizes(nodes, attribute="in_degree", scale=None):
    node_attributes = nodes[0].getNodeData().attributes.values
    try: ix = [v.column.title for v in node_attributes].index(attribute)
    except:
	#JC#
        print "Debug ERROR:  No title for node -- skipping adjust_sizes"
	return

    if not scale:
        m = max([n.getNodeData().attributes.values[ix].value for n in nodes])
        scale = lambda f : m-f

    for node in nodes:
        node_data = node.getNodeData()
        value = float(node_data.attributes.values[ix].value)
        node_data.setSize(1 + scale(value)) # avoid problem with 0 sizes
        print "changed %s size from %s to %s" % (node_data.getLabel(), value, (1 + scale(value)))

def jadjust_sizes(nodes, attribute="weight", scale=None):
    
    
    node_attributes = nodes[0].getNodeData().attributes.values
    try: ix = [v.column.title for v in node_attributes].index(attribute)
    except:
	#JC#
        print "Debug ERROR:  No title for node -- skipping adjust_sizes"
	return

    #Jon scale with max at 30
    #scale=lambda f : 4 * (4-f)
    min_node_size=10
    max_node_size=20+min_node_size
    if not scale:
        m = max([float(n.getNodeData().attributes.values[ix].value) for n in nodes])
        m=float(m)
        print "Max node: "+str(m)+" type: "+str(type(m)) #~1000
        scale = lambda f : max_node_size*(f/m)

    for node in nodes:
        node_data = node.getNodeData()
        value = float(node_data.attributes.values[ix].value)
        node_data.setSize(1 + scale(value)) # avoid problem with 0 sizes
        print "changed %s size from %s to %s" % (node_data.getLabel(), value, (min_node_size + scale(value)))

    return

def layout(graph_file='./graph.gexf', out_gexf='./new_graph.gexf', layout=True, save_pdf=True, save_gephi=False):
    print "loading graph"
    # tips:
    #   http://wiki.gephi.org/index.php/Toolkit_portal
    #   it helps to open the jar to see what's in it.
    #   work through stuff here: https://wiki.gephi.org/index.php/Toolkit_-_Headless_Gephi
    #   look at gephi-toolkit demos and look for gexf import
    #   find out where shit is by cloning git://github.com/gephi/gephi.git and grepping
    #   Layout http://gephi.org/docs/toolkit/org/gephi/layout/plugin/forceAtlas/ForceAtlasLayout.html
    #   Plugins: https://wiki.gephi.org/index.php/How_to_use_Gephi_plug-ins_with_the_Gephi_Toolkit
    ProjectController.newProject() 
    w = ProjectController.getCurrentWorkspace()

    print "D graph file: "+str(graph_file)
    graph = ImportController.importFile(java.io.File(graph_file))
    print "D: "+str(type(graph))

    edge_default = graph.getEdgeDefault()
    graph.setEdgeDefault(edge_default.values()[0])#DIRECTED, UNDIRECTED, MIXED

    dp = lookup('io.processor.plugin.DefaultProcessor')
    ImportController.process(graph, dp, w)

    if layout:

        #  Layout
        ##################################################################
        fa = lookup('layout.plugin.forceAtlas.ForceAtlas')
        force_atlas = fa.buildLayout()
        force_atlas.setGraphModel(GraphController.getModel())

        force_atlas.resetPropertiesValues() # set defaults
        # for p in sorted(a, key=lambda p: (p.category, p.displayName, p.name)): 
        #    print "%s -> '%s' (%s) = %s" % (p.category, p.displayName, p.name, p.value)
        force_atlas.adjustSizes = True
        force_atlas.attractionStrength = 8
        force_atlas.repulsionStrength = 2000 #too close
        force_atlas.repulsionStrength = 200000 #too far
        force_atlas.repulsionStrength = 100000 #almost
        force_atlas.repulsionStrength = 50000

        force_atlas.initAlgo()
        steps = 50000
        steps = 5000
        steps=RELAX_STEPS

        print "running force atlas for %d steps" % steps
        while steps and force_atlas.canAlgo() and not force_atlas.isConverged():
            if steps % 1000 == 0:
                print "step %d" % steps
            force_atlas.goAlgo()
            steps -= 1
            
            

        #  Adjust labels
        ##################################################################
        # I think there's a bug in label adjust so that it doesn't work in the toolkit?
        # http://forum.gephi.org/viewtopic.php?t=1435
        lab = lookup('layout.plugin.labelAdjust.LabelAdjustBuilder')
        label_adjust = lab.buildLayout()
        label_adjust.resetPropertiesValues()
        label_adjust.setGraphModel(GraphController.getModel())

        label_adjust.initAlgo()
        steps = 50000
        steps = 5000
        steps=RELAX_STEPS
        print "running label adjust for %d steps" % steps
        while steps and label_adjust.canAlgo() and not label_adjust.isConverged():
            if steps % 1000 == 0:
                print "step %d" % steps
            label_adjust.goAlgo()
            steps -= 1

    # Adjust node sizes (Force Atlas changes them?)
    gm = GraphController.getModel()
    gv = gm.getGraphVisible()
    nodes = list(gv.getNodes())
    print "D: adjusting nodes size: "+str(len(nodes))
    jadjust_sizes(nodes)

    # adjust the look a bit for the pdf
    preview = PreviewController.getModel()
    preview.properties.putValue('node.border.width', 0)
    #JC# preview.properties.putValue('node.label.show', True) #?boolean error?
    PreviewController.refreshPreview() # necessary?
    
    # When done, save what we did
    # 1) GEXF
    ExportController.exportFile(java.io.File(out_gexf))
    
    # 2) PDF
    save_pdf=False
    if save_pdf:
        # reset node sizes, small ones cause problems for pdf render
        adjust_sizes(nodes, scale=lambda f : 4 * (4-f))
        part, ext = os.path.splitext(out_gexf)
        out_pdf = part + '.pdf'
        pdf = ExportController.getExporter("pdf")
        pdf.landscape = True
        ExportController.exportFile(java.io.File(out_pdf), pdf)

    # 3) GEPHI (how do you save a gephi file?)
    if save_gephi:
        saver = ProjectController.saveProject(ProjectController.getCurrentProject(), java.io.File("new_graph.gephi"))
        saver.run()

    # 4) GraphML gml file
    #//Export to Writer
    #Exporter exporterGraphML = ec.getExporter("graphml");     //Get GraphML exporter
    #exporterGraphML.setWorkspace(workspace);
    #StringWriter stringWriter = new StringWriter();
    #ec.exportWriter(stringWriter, (CharacterExporter) exporterGraphML);
    #//System.out.println(stringWriter.toString());   //Uncomment this line

    gml = ExportController.getExporter("graphml")
    gml_out="gml_out.graphml"

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    gml_out_relative=BASE_DIR+"/../../static/htmt/temp/gml_out.graphml"


    ExportController.exportFile(java.io.File(gml_out_relative), gml)
    print "Output to "+gml_out_relative




    
if __name__ == '__main__':
    # from optparse import OptionParser
    # parser = OptionParser()
    try:
        layout(sys.argv[1], sys.argv[2])
    except IndexError:
        layout()
