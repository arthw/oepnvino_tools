import onnx
import os, sys
from onnx import AttributeProto, helper

def split_min_max_input(input):
    left = []
    removed = []
    for i in input:
        if "min" not in i and "max" not in i:
            left.append(i)
        else:
            removed.append(i)

    return left, removed

def remove_nodes_by_output(removed_nodes, op_type, graph):
    nodes = []
    for i in range(len(graph.node)):
        node = graph.node[i]

        if node.op_type == op_type:
            tmp = [val for val in removed_nodes if val in node.output]
            if len(tmp)>0:
                nodes.append(node)

    for node in nodes:
        graph.node.remove(node)

def get_values(removed, graph):
    min, max = 0,0
    for i in range(len(graph.node)):
        node = graph.node[i]

        if node.op_type == "Constant":
            tmp = [val for val in removed if val in node.output]
            if len(tmp)>0:
                for att in node.attribute:
                    if att.name == "value":
                        # print(att)
                        # print(att.t)
                        if "min" in att.t.name:
                            min = att.t.float_data[0]
                        if "max" in att.t.name:
                            max = att.t.float_data[0]
    return min, max

def correct_clip(input_model, output_model):
    onnx_model = onnx.load(input_model)

    graph = onnx_model.graph
    removed_nodes = []

    for i in range(len(onnx_model.graph.node)):
        node = onnx_model.graph.node[i]
        input = node.input
        op_type =node.op_type

        if "Clip" == op_type:
            left, removed = split_min_max_input(input)

            removed_nodes.extend(removed)

            for rm in removed:
                input.remove(rm)

            min, max = get_values(removed, graph)
            min = helper.make_attribute("min", min)
            max = helper.make_attribute("max", max)
            node.attribute.extend([min, max])


    remove_nodes_by_output(removed_nodes, 'Constant', graph)
    onnx.save(onnx_model, output_model)

    print("Done!")


def help():
    print("Miss parameters: input_model output_model")

if __name__ == "__main__":
    if len(sys.argv)<3:
        help()
        sys.exit(1)

    input_model = sys.argv[1]
    output_model = sys.argv[2]
    correct_clip(input_model, output_model)
