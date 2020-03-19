#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          compile.py
 Description:       Verify and Compile ha_spec

 Creation Date:     03/13/2020
 Author:            Ajay Paratmandali

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import os
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

from eos.utils.ha import const
from eos.utils.ha.validation import SyntaxValidator
from eos.utils.ha.validation import SymanticValidator

class Compiler:
    def __init__(self, source_path, compile_file, ha_spec_file):
        """
        Initialize Compiler
        source_path: Source path for multiple component HA_SPEC Files
        compile_file: Name of compiled spec file
        ha_spec_file: Filename to verify file
        """
        if ha_spec_file is not None:
            self._verify_ha_spec_schema(ha_spec_file)
        else:
            self.source_path = source_path
            self.build_path = const.BUILD_PATH
            self.compiled_file = compile_file
            self.compiled_schema = {
                "predecessors_edge": [],
                "colocation_edges": [],
                "isolate_resources": [],
                "resources": {}
            }
            self.file_list = []
            self.colocation_graph = nx.Graph()
            self.order_graph = nx.DiGraph()

    def parse_files(self):
        """
        Parse source_path for all component spec file
        """
        for root, directories, filenames in os.walk(self.source_path):
            self._create_parse_file(directories, filenames)

    def create_schema(self):
        """
        Dump Compiled spec to output file
        """
        with open(self.compiled_file, 'w') as fp:
            json.dump(self.compiled_schema, fp, indent=4)

    def compile_graph(self):
        """
        Compile graph for predecessors, colocation, relation
        """
        resource_set = self.compiled_schema["resources"]
        predecessors_edges = []
        colocation_edges = []
        isolate_resources = []
        for res in resource_set.keys():
            predecessors = resource_set[res]["dependencies"]["predecessors"]
            self._update_dependencies(predecessors, predecessors_edges, res)
            colocations = resource_set[res]["dependencies"]["colocation"]
            self._update_dependencies(colocations, colocation_edges, res)
            relation = resource_set[res]["dependencies"]["relation"]
            isolate_resources.extend(relation)
        self.compiled_schema["predecessors_edge"] = list(set(predecessors_edges))
        self.compiled_schema["colocation_edges"] = list(set(colocation_edges))
        self._isolate(isolate_resources)

    def draw_graph(self):
        """
        Drow graph
        """
        options = {
            'node_color': 'blue',
            'node_size': 100,
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 12,
            'font_weight': 'bold',
            'with_labels': True
        }
        nx.draw(self.order_graph, **options)
        plt.savefig(self.build_path + "dependency_graph.png")
        nx.draw(self.colocation_graph, **options)
        plt.savefig(self.build_path + "colocation_graph.png")

    def verify_schema(self):
        """
        add edge and verify schema for cycle
        """
        self._add_nodes(self.compiled_schema["resources"])
        self._add_edge(self.order_graph, self.compiled_schema["predecessors_edge"])
        self._add_edge(self.colocation_graph, self.compiled_schema["colocation_edges"])
        self._verify_compiled_schema()

    def _verify_ha_spec_schema(self, ha_spec_file):
        """
        Verify ha spec file
        """
        validator = SyntaxValidator(ha_spec_file)
        validator.execute()
        return validator.get_schema()

    def _create_parse_file(self, directories, filenames):
        """
        Parse each file and validate for json
        """
        for filename in filenames:
            if filename.endswith('json'):
                components = self._verify_ha_spec_schema(self.source_path + filename)
                for component in components.keys():
                    for resource in components[component].keys():
                        if resource in self.compiled_schema["resources"].keys():
                            raise Exception("Resource [%s] is already defined in the component [%s]"\
                                    %(res,compiled_schema["resources"][res]["component"]))
                        self.compiled_schema["resources"][resource] = components[component][resource]
                        self.compiled_schema["resources"][resource]["component"] = component

    def _add_nodes(self, resource_set):
        """
        Add Node in resource set
        """
        for resource in resource_set.keys():
            self.order_graph.add_node(resource)
            self.colocation_graph.add_node(resource)

    def _update_dependencies(self, dependencies, edges, resource):
        """
        Create edges for graph
        """
        for res_name in dependencies:
            edges.append((res_name, resource))

    def _isolate(self, isolate_resources):
        """
        Find isolated resource
        """
        predecessors = self.compiled_schema["predecessors_edge"]
        for edge in predecessors:
            for res in edge:
                if res in isolate_resources:
                    isolate_resources.remove(res)
        self.compiled_schema["isolate_resources"] = isolate_resources

    def _verify_compiled_schema(self):
        """
        Verify all compiletion rule
        """
        validator = SymanticValidator(self.compiled_schema, self.order_graph)
        validator.execute()

    def _add_edge(self, graph, edges):
        """
        Add edges for graph
        """
        for edge in edges:
            graph.add_edge(*edge)
