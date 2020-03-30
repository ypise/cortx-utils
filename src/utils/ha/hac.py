#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          hac.py
 Description:       Entry point for HA Integration CLI

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
import traceback
import argparse
from datetime import datetime
from eos.utils.schema.conf import Conf

def usage():
    return """

Example:
Shorter parameter:
$ hac -v /my/spec/my_spec.json
$ hac –c /my/spec/dir -o eos_ha.spec
$ hac –g eos_ha.spec -o eos_pcs.sh -t pcs
$ hac -c /opt/seagate/ha_files/files/ -b /my/spec/dir

Longer parameter:
$ hac --validate /opt/seagate/ha_files/files/csm.json
$ hac --compile /my/spec/dir --output compiled.json
$ hac --generate compiled.json --output eos_pcs.sh --target pcs

"""

#TODO make resource name case insensitive
#TODO hac –d eos_ha.spec -t pcs


def main():
    from eos.utils.ha.compile import Compiler
    from eos.utils.ha import generate
    from eos.utils.ha import const

    provider = {
        "pcs": generate.PCSGeneratorResource,
        "k8s": generate.KubernetesGenerator
    }

    try:
        Conf.init()
        argParser = argparse.ArgumentParser(
            usage = "%(prog)s\n\n" +  usage(),
            formatter_class = argparse.RawDescriptionHelpFormatter)
        argParser.add_argument("-v", "--validate",
                help="Check input files for syntax errors")
        argParser.add_argument("-t", "--target", default="pcs",
                help="HA target to use. Example: pcs")
        argParser.add_argument("-c", "--compile",
                help="Path of ha_spec files.")
        argParser.add_argument("-o", "--output",
                help="Final spec/rule file for generator/compiler")
        argParser.add_argument("-g", "--generate",
                help="Ganerate script/rule for targeted HA tool. Eg: pcs")
        argParser.add_argument("-a", "--args_file",
                help="Args file for generator for dynamic input values")
        argParser.add_argument("-r", "--resources",
                help="Enter resorce list")
        args = argParser.parse_args()

        if args.generate is None:
            c = Compiler(args.compile, args.output, args.validate)
            if args.validate is None:
                c.parse_files()
                c.compile_graph()
                c.verify_schema()
                c.create_schema()
                c.draw_graph()
        else:
            com = provider[args.target](args.generate,
                                        args.output,
                                        args.args_file,
                                        args.resources)
            com.create_script()
    except Exception as e:
        #TODO: print traceback error properly
        with open(const.HAC_LOG, "w") as log:
            current_time = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            log.writelines(current_time + ":"+ str(traceback.format_exc()))
        print('Error: ' + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
