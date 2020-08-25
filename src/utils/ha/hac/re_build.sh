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

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/lnet_c1_c2.sh --args /var/lib/eos/ha/args.yaml --resources "lnet-c1 lnet-c2"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/hax_c1_c2.sh --args /var/lib/eos/ha/args.yaml --resources "hax-c1 hax-c2"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/motr_iso_c1_c2.sh --args /var/lib/eos/ha/args.yaml --resources "motr-ios-c1 motr-ios-c2"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/s3auth.sh --args /var/lib/eos/ha/args.yaml --resources "s3auth"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/el_ha_st.sh --args /var/lib/eos/ha/args.yaml --resources "els-search statsd haproxy"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/s3server.sh --args /var/lib/eos/ha/args.yaml --resources "s3server-c1-1 s3server-c1-2 s3server-c1-3 s3server-c1-4 s3server-c1-5 s3server-c1-6 s3server-c1-7 s3server-c1-8 s3server-c1-9 s3server-c1-10 s3server-c1-11 s3server-c2-1 s3server-c2-2 s3server-c2-3 s3server-c2-4 s3server-c2-5 s3server-c2-6 s3server-c2-7 s3server-c2-8 s3server-c2-9 s3server-c2-10 s3server-c2-11"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/s3back.sh --args /var/lib/eos/ha/args.yaml --resources "s3backprod s3backcons"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/sspl.sh --args /var/lib/eos/ha/args.yaml --resources "sspl"

hac --generate /var/lib/eos/ha/compiled.json  --output /var/lib/eos/ha/script/csm.sh --args /var/lib/eos/ha/args.yaml --resources "kibana-vip"

