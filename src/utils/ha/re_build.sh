#!/bin/bash

# Perform cleanup
rm -rf /var/lib/eos/ha/script
mkdir -p /var/lib/eos/ha/script

hac --compile /var/lib/eos/ha/specs/ --output /var/lib/eos/ha/compiled.json

if [ $? != 0 ]; then
    echo "Compilation of spec failed !!!"
    exit 1
fi

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/eos-pcs.sh --args /var/lib/eos/ha/args.yaml


