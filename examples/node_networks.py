import pyhapi as ph
import numpy as np

def main():
    session     = ph.HSessionManager.GetOrCreateDefaultSession()

    #load hda asset and instantiate
    hdaAsset    = ph.HAsset(session, "hda/FourShapes.hda")
    asset_node  = hdaAsset.Instantiate(node_name = "Processor").Cook()
    child_nodes = asset_node.GetChildNodes()
    print("FourShapes's child nodes include: {0}".format(",".join([node.Name for node in child_nodes])))

    #create a sop node, set input
    another_box = ph.HNode(session, "geo", "ProgrammaticBox", parent_node = asset_node)
    input_node  = another_box\
    		.ConnectNodeInput(child_nodes[0])\
		    .Cook()\
		    .GetNodeInput(0)
    print("ProgrammaticBox's input node is {0}".format(input_node.Name))

    #log all nodes inside FourShapes
    print("\nFourShapes's child nodes after connecting include: {0}".format(",".join([node.Name for node in asset_node.GetChildNodes()])))

    #delete sop node
    another_box\
    		.DisconnectNodeInput(0)\
    		.Delete()

    #log all nodes inside FourShapes
    print("\nFourShapes's child nodes after disconnecting include: {0}".format(",".join([node.Name for node in asset_node.GetChildNodes()])))

    session.SaveHIP("modifiedScene.hip")


if __name__ == "__main__":
    main()