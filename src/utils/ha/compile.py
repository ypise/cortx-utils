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

from ha import const

class Validator:
    pass

class SyntaxValidator(Validator):
    """
    SyntaxValidator check syntax for each input file
    """
    @staticmethod
    def verify_file(file_name):
        """
        Verify file
        """
        if not os.path.isfile(file_name):
            raise Exception("%s is not a file." %file_name)

    @staticmethod
    def validate_json(input_file):
        """
        Remove comment from file and validate for json
        """
        try:
            with open(input_file, "r") as spec_file:
                output_file = input_file + ".parse"
                with open(output_file, "w") as parsed_file:
                    for a_line in spec_file.readlines():
                        line_no_spaces = a_line.strip()
                        if not line_no_spaces.startswith('#'):
                            parsed_file.writelines(a_line)
            with open(output_file, "r") as parsed_file:
                components = json.load(parsed_file)
            return components
        except Exception as e:
            raise Exception("Invalid json file %s: %s" %(input_file, e))

    @staticmethod
    def check_duplicate_resource(resource, compiled_schema):
        """
        Check if a resource is already defined
        """
        if resource in compiled_schema["resources"].keys():
            raise Exception("Resource [%s] is already defined in the component [%s]" %(res,compiled_schema["resources"][res]["component"]))

class SymanticValidator(Validator):
    """
    SymanticValidator validate graph and compiled schema
    """
    def __init__(self):
        pass

    def run(self, compiled_schema, order_graph):
        """
        Verify cluster for graph and schema
        """
        #TODO: Divide validation into single file and compiled schema
        self.compiled_schema = compiled_schema
        self.order_graph = order_graph
        self._verify_cycle()
        self._verify_resource_predecessors()
        self._verify_resource_colocation()
        self._verify_resource_relation()

    def _verify_resource_predecessors(self):
        """
        Verify predecessors for resource
        """
        error_msg = ""
        resource_set = self.compiled_schema["resources"]
        for resource in resource_set.keys():
            for predecessors_resource in resource_set[resource]["dependencies"]["predecessors"]:
                if predecessors_resource not in resource_set.keys():
                    error_msg = error_msg + "Invalid predecessors resource ["+predecessors_resource+"] in component [" \
                        +resource_set[resource]["component"]+"] \n"
        if error_msg != "":
            raise Exception(error_msg)

    def _verify_resource_colocation(self):
        """
        Verify colocation for resource
        """
        error_msg = ""
        resource_set = self.compiled_schema["resources"]
        for resource in resource_set.keys():
            for predecessors_resource in resource_set[resource]["dependencies"]["colocation"]:
                if predecessors_resource not in resource_set.keys():
                    error_msg = error_msg + "Invalid colocation resource ["+predecessors_resource+"] in component [" \
                        +resource_set[resource]["component"]+"] \n"
        if error_msg != "":
            raise Exception(error_msg)

    def _verify_resource_relation(self):
        """
        Verify relation for resource
        """
        error_msg = ""
        resource_set = self.compiled_schema["resources"]
        for resource in resource_set.keys():
            for predecessors_resource in resource_set[resource]["dependencies"]["relation"]:
                if predecessors_resource not in resource_set.keys():
                    error_msg = error_msg + "Invalid relation resource ["+predecessors_resource+"] in component [" \
                        +resource_set[resource]["component"]+"] \n"
        if error_msg != "":
            raise Exception(error_msg)

    def _verify_cycle(self):
        """
        Verify graph to find cycle
        """
        cycle_list = []
        cycle_gen = nx.simple_cycles(self.order_graph)
        for i in cycle_gen:
            cycle_list.append(i)
        if len(cycle_list) != 0:
            error_msg = ""
            for cycle in cycle_list:
                cycle.append(cycle[0])
                error_msg = error_msg + "Cycle found in graph " + str(cycle) + "\n"
            raise Exception(error_msg)

    def _validate_mode(self):
        """
        Validate mode for HA, It should be one of active_active, active_passive, master_slave
        Validate clone for mode of resources
        """
        pass

    def _validate_clone(self):
        """
        Validate clone
            :active passive: No clone
            :master slave: clone and master should be defined
            :active active: clone should be defined
            : other value is invalid
        """
        pass

    def _validate_component(self):
        """
        validate component for each resource
        """
        pass

    def _mandetory_parameter(self):
        """
        Check all required parameter for schema
        """
        pass

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
                "predecessors_isolate": [],
                "colocation_isolate": [],
                "colocation_edges": [],
                "resources": {}
            }
            self.file_list = []
            self.colocation_graph = nx.Graph()
            self.order_graph = nx.DiGraph()
            self._validate = SymanticValidator()

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
        for res in resource_set.keys():
            predecessors = resource_set[res]["dependencies"]["predecessors"]
            colocation = resource_set[res]["dependencies"]["colocation"]
            relation = resource_set[res]["dependencies"]["relation"]
        predecessors_isolate = []
        predecessors_edges = []
        colocation_isolate = []
        colocation_edges = []
        for res in resource_set.keys():
            predecessors = resource_set[res]["dependencies"]["predecessors"]
            predecessors.append(res)
            self._update_dependencies(predecessors, predecessors_isolate, predecessors_edges)
            colocations = resource_set[res]["dependencies"]["colocation"]
            colocations.append(res)
            self._update_dependencies(colocations, colocation_isolate, colocation_edges)
        self.compiled_schema["predecessors_edge"] = list(set(predecessors_edges))
        self.compiled_schema["colocation_edges"] = list(set(colocation_edges))
        self._isolate(predecessors_isolate, predecessors_edges, "predecessors_isolate")
        self._isolate(colocation_isolate, colocation_edges, "colocation_isolate")

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
        SyntaxValidator.verify_file(ha_spec_file)
        components = SyntaxValidator.validate_json(ha_spec_file)
        return components

    def _create_parse_file(self, directories, filenames):
        """
        Parse each file and validate for json
        """
        for filename in filenames:
            if filename.endswith('json'):
                components = self._verify_ha_spec_schema(self.source_path + filename)
                for component in components.keys():
                    for resource in components[component].keys():
                        SyntaxValidator.check_duplicate_resource(resource, self.compiled_schema)
                        self.compiled_schema["resources"][resource] = components[component][resource]
                        self.compiled_schema["resources"][resource]["component"] = component

    def _add_nodes(self, resource_set):
        """
        Add Node in resource set
        """
        for resource in resource_set.keys():
            self.order_graph.add_node(resource)
            self.colocation_graph.add_node(resource)

    def _update_dependencies(self, dependencies, isolate, edges):
        """
        Create edges for graph
        """
        #dependencies.reverse()
        if len(dependencies) <= 1:
            isolate.append(dependencies[0])
        else:
            for i in range(0, len(dependencies)-1):
                edges.append((dependencies[i], dependencies[i+1]))

    def _isolate(self, li, edges, key):
        """
        Find isolated resource
        """
        for edge in edges:
            for res in edge:
                if res in li:
                    li.remove(res)
        self.compiled_schema[key] = li

    def _verify_compiled_schema(self):
        """
        Verify all compiletion rule
        """
        self._validate.run(self.compiled_schema, self.order_graph)

    def _add_edge(self, graph, edges):
        """
        Add edges for graph
        """
        for edge in edges:
            graph.add_edge(*edge)
