import json

ixs = []

# Load ixs file
with open('/dataset/ixps/ixs_202107.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        ixs.append(data)
        # if 'country' not in data:
        #     continue
        # if data['country'] == 'MY':
        #     print(data)

# mpIxs = {}
# for ix in ixs:
#     ix0 = ix['ix-id']
#     mpIxs[ix0] = ix

# Load ixs-asn file and Generate
ix_asns = []
mpIxs = {}

with open('/dataset/ixps/ix-asns_202107.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        ix_asns.append(data)
        ix_id = data['ix_id']
        if ix_id in mpIxs:
            mpIxs[ix_id].append(data)
        else:
            mpIxs[ix_id] = [data]

for ix in ixs:
    if 'country' not in ix:
        continue
    if ix['country'] == 'SG':
        x = ix['ix_id']
        if x not in mpIxs:
            print('null', ix)
        print(len(mpIxs[x]), ix)