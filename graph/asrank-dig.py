import numpy as np
import matplotlib.pyplot as plt
import json

asns = []
asnLinks = []
asnOrgs = []

with open('/Users/levi.zhou/PycharmProjects/bandwidth/graph/asns.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        asns.append(data)
maxClientConeSize = asns[0]["cone"]["numberAsns"]

# with open('/Users/levi.zhou/PycharmProjects/bandwidth/graph/organizations.jsonl', 'r') as f:
#     for line in f.readlines():
#         data = json.loads(line)
#         asnOrgs.append(data)
#
with open('/Users/levi.zhou/PycharmProjects/bandwidth/graph/asnLinks.jsonl', 'r') as f:
# with open('/Users/levi.zhou/PycharmProjects/bandwidth/graph/test.jsonl', 'r') as f:

    for line in f.readlines():
        data = json.loads(line)
        asnLinks.append(data)

# process asns
mpAsns = {}
for asn in asns:
    asn0 = asn['asn']
    mpAsns[asn0] = asn

# process link relation

mpProvider = {"init": 0}
mpPeer = {"init": 0}
mpCustomer = {"init": 0}

for link in asnLinks:
    asn0 = link['asn0']['asn']
    asn1 = link['asn1']['asn']

    if link['relationship'] == 'provider':
        if asn0 in mpProvider:
            mpProvider[asn0].append(asn1)
        else:
            mpProvider[asn0] = [asn1]
    elif link['relationship'] == 'peer':
        if asn0 in mpPeer:
            if mpPeer[asn0] is not None:
                mpPeer[asn0].append(asn1)
            else:
                mpPeer[asn0] = [asn1]
        else:
            mpPeer[asn0] = [asn1]
    elif link['relationship'] == 'customer':
        if asn0 in mpCustomer:
            if mpCustomer[asn0] is not None:
                mpCustomer[asn0].append(asn1)
            else:
                mpCustomer[asn0] = [asn1]
        else:
            mpCustomer[asn0] = [asn1]
    pass


for asn in asns:
    if asn["country"]["iso"] != 'ID':
        continue
    print(asn["asn"], asn["asnName"], asn["organization"]["orgName"], asn["cone"]["numberAsns"], sep="\t")
    pass