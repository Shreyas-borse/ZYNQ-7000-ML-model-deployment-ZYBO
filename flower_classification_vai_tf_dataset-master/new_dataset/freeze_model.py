#! /usr/bin/python3
# coding=utf-8
#####################

import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.
​
    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
    return frozen_graph

keras.backend.set_learning_phase(0)
loaded_model= keras.models.load_model('./flower_classification_weights.h5')

# make list of output and input node names
input_names=[out.op.name for out in loaded_model.inputs]
output_names=[out.op.name for out in loaded_model.outputs]
print('input  node is{}'.format(input_names))
print('output node is{}'.format(output_names))

f = open("input_output_node_name.txt", "w+")
f.write('input  node is{}'.format(input_names) + "\n")
f.write('output node is{}'.format(output_names) + "\n")
f.close()

frozen_graph = freeze_session(keras.backend.get_session(), output_names=output_names)

tf.train.write_graph(frozen_graph, "./", "frozen_graph.pb", as_text=False)