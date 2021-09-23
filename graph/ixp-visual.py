import json
import folium

ixs = []
m = folium.Map(location=[1.28000, 103.85000], tiles = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
m.save("temp_index.html")

# Load ixs file
with open('/Users/levi.zhou/PycharmProjects/bandwidth/dataset/ixps/ixs_202107.jsonl', 'r') as f:
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

# Load ixs-asn file and Generate ix asn map
ix_asns = []
mpIxs = {}

with open('/Users/levi.zhou/PycharmProjects/bandwidth/dataset/ixps/ix-asns_202107.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        ix_asns.append(data)
        pdb_fac_id = data['ix_id']
        if pdb_fac_id in mpIxs:
            mpIxs[pdb_fac_id].append(data)
        else:
            mpIxs[pdb_fac_id] = [data]

# load facilities

facilities = []
mpFacilities = {}

with open('/Users/levi.zhou/PycharmProjects/bandwidth/dataset/ixps/facilities_202107.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        facilities.append(data)
        pdb_fac_id = data['fac_id']
        if pdb_fac_id in mpFacilities:
            mpFacilities[pdb_fac_id].append(data)
        else:
            mpFacilities[pdb_fac_id] = [data]

# load geo dataset

geos = []
mpGeos = {}

with open('/Users/levi.zhou/PycharmProjects/bandwidth/dataset/ixps/locations_202107.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        geos.append(data)
        pdb_fac_id = data['geo_id']
        if pdb_fac_id in mpGeos:
            mpGeos[pdb_fac_id].append(data)
        else:
            mpGeos[pdb_fac_id] = [data]

# process ixs
for fac in ixs:
    if 'country' not in fac:
        continue
    # if fac['country'] in ['SG', 'VN', 'TH', "MY", "ID", "PH", "TW"]:
    if fac['country'] in ["ID"]:
        # if True:
        x = fac['ix_id']
        lenAsn = 0
        if x not in mpIxs:
            print('null', fac)
        else:
            print(len(mpIxs[x]), fac)
            lenAsn = len(mpIxs[x])
        if 'geo_id' not in fac:
            continue
        if fac['geo_id'] not in mpGeos:
            continue
        geo = mpGeos[fac['geo_id']]

        folium.CircleMarker(
            location=tuple([geo[0]['latitude'], geo[0]['longitude']]),
            radius= 15.0,
            popup=fac['name'],
            color="#3186cc",
            fill=True,
            fill_color="#3186cc",
        ).add_to(m)


# process fac
for fac in facilities:
    if 'country' not in fac:
        continue
    # if fac['country'] in ['SG', 'VN', 'TH', "MY", "ID", "PH", "TW"]:
    if fac['country'] in ["ID"]:

    # if True:
    #     x = fac['ix_id']
    #     lenAsn = 0
    #     if x not in mpIxs:
    #         print('null', fac)
    #     else:
    #         print(len(mpIxs[x]), fac)
    #         lenAsn = len(mpIxs[x])
        r = 1
        if 'num_asn' in fac:
            r = fac['num_asn']
        if 'latitude' not in fac:
            continue
        if 'longitude' not in fac:
            continue
        folium.CircleMarker(
            location=tuple([fac['latitude'], fac['longitude']]),
            radius=r * 10.0,
            popup=fac['name'],
            color="#FF6100",
            fill=True,
            fill_color="#FF6100",
        ).add_to(m)

m.save("ipx_geo.html")
