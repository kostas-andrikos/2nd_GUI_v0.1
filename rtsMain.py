import numpy as np
import os

import mass
import results
import towSteering
import json

from layup import Layup

from part import *
from material import *
from section import *
from assembly import *
from step import *  
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from odbAccess import openOdb


def main(**kwargs):
    setup = Setup()
    setup.get_user_input(kwargs)
    if not kwargs.get('symmetricLaminate') == 'OFF':
        setup.apply_symmetry()
    setup.create_stacking_sequence()
    setup.compute_rts()


class Setup:
    def __init__(self):
        self.APP_PATH = os.getcwd()
        self.ABQS_FILES_PATH = os.path.join(self.APP_PATH, "Abaqus")

    def get_user_input(self, kwargs):
        with open('tmp_dict.json', 'r') as file:
            dialog1_dict = json.load(file)
        self.model_name = str(dialog1_dict.get('model_name'))
        self.part_name = str(dialog1_dict.get('part_name'))
        self.method = int((dialog1_dict.get('method')))
        self.symmetry = bool(kwargs.get('symmetricLaminate'))
        self.rts_frequency = int(kwargs.get('freq'))
        self.nom_thickness = float(kwargs.get('nomThick'))
        self.nr_layers = int(kwargs.get('nrLayers'))
        rts_table = kwargs.get('rtsParams')
        rts_params = [rts_table[i][:-1] for i in range(len(rts_table))]
        rts_params = np.array(rts_params)
        material_names = [rts_table[i][-1:] for i in range(len(rts_table))]
        self.material_names = np.array(material_names)[:, 0]
        self.phi = rts_params[:, 0]
        self.t0 = rts_params[:, 1]
        self.t1 = rts_params[:, 2]

    def apply_symmetry(self):
        self.phi = np.concatenate((self.phi, self.phi[::-1]))
        self.t0 = np.concatenate((self.t0, self.t0[::-1]))
        self.t1 = np.concatenate((self.t1, self.t1[::-1]))
        self.material_names = np.concatenate((self.material_names, self.material_names[::-1]))
    
    def create_stacking_sequence(self):
        # setting up the model
        nomThick_list = [self.nom_thickness] * self.nr_layers
        self.SS = Layup(self.nr_layers)
        for i in range(self.nr_layers):
            self.SS.addLayer(i, self.material_names[i], self.phi[i], self.t0[i], self.t1[i], nomThick_list[i])  # noqa: E501

    def get_geometry_from_meshFile(self, meshPath):
        nodes, elements = [], []
        # import mesh pre-created in Abaqus CAE or elsewhere
        f = open(meshPath, "r")
        for line in f:
            if line == "*Node\n":
                flag = "nodes"
                continue
            elif line == "*Element\n":
                flag = "elements"
                continue
            elif line == "\n":
                continue
            if flag == "nodes":
                newLine = line[:-1].split(",")
                nodeArray = [int(newLine[0])]
                nodeArray.extend([float(num) for num in newLine[1:]])
                nodes.append(nodeArray)
            elif flag == "elements":
                elementArray = [int(num) for num in line[:-1].split(",")]
                elements.append(elementArray)
            self.nodes = np.array(nodes)
            self.elements = np.array(elements)
        f.close()

    def get_geometry_from_model(self, elem_set):
        # nodes
        all_nodes = mdb.models[self.model_name].parts[self.part_name].sets[elem_set].nodes
        node_nrs = np.zeros(len(all_nodes), dtype=int)
        node_coord = np.zeros((len(all_nodes), 3))
        np_nodes = np.zeros((len(all_nodes), 4))
        for i in range(len(all_nodes)):
            node_nrs[i] = int(all_nodes[i].label)
            node_coord[i,:] = np.array(all_nodes[i].coordinates)
            np_nodes[i] = np.concatenate((node_nrs[i].astype(int), node_coord[i,:]), axis=None)
        # self.nodes = np_nodes
        # elements
        all_elements = mdb.models[self.model_name].parts[self.part_name].sets[elem_set].elements
        elm_nrs = np.zeros(len(all_elements), dtype=int)
        elm_connect = np.zeros((len(all_elements), 4), dtype=int)
        np_elements = np.zeros((len(all_elements), 5), dtype=int)
        for i in range(len(all_elements)):
            elm_nrs[i] = int(all_elements[i].label)
            elm_connect[i,:] = np.array(all_elements[i].connectivity) + 1
            np_elements[i] = np.concatenate((elm_nrs[i].astype(int), elm_connect[i,:]), axis=None)  # noqa: E501
        # self.elements = np_elements

        return np_nodes, np_elements

    def compute_rts(self):
        # phi limit for two periods of shearing
        max_phi_2x = 75
        data = {}
        # Pick Element Sets
        elemsets_keys = [i[0] for i in mdb.models[self.model_name].parts[self.part_name].sets.summary() if 'Element' in i]
        for elemset in elemsets_keys:
            nodes, elements = self.get_geometry_from_model(elemset)
            towSteering.linearCustomVariation(nodes, elements, self.SS, frequency=self.rts_frequency)  # noqa: E501

            # Create a dictionary for the current elemset if it doesn't exist
            if elemset not in data:
                data[elemset] = {}

            for ply in self.nr_layers:    
                thick = self.SS.stackingSequence[ply].thickness
                vat = self.SS.stackingSequence[ply].angles

                # Create a dictionary for the current ply if it doesn't exist
                ply_label = 'Ply-{}'.format(ply)
                if ply_label not in data[elemset]:
                    data[elemset][ply_label] = {}

                # Assign the 'thick' and 'vat' values to the dictionary
                t_key = 't{}_{}'.format(elemset, ply)
                v_key = 'v{}_{}'.format(elemset, ply)
                data[elemset][ply_label][t_key] = thick
                data[elemset][ply_label][v_key] = vat

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
