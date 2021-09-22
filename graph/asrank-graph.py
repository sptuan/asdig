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



r = np.array([])
theta = np.array([])

r_ex = np.array([])
theta_ex = np.array([])

r_ex2 = np.array([])
theta_ex2 = np.array([])

# get avg longitude



# matplotlib

# find ID Geo
counter = 0.0
avgLongitude = 0.0
for asn in asns:
    if asn["country"]["iso"] != 'ID':
        continue
    if asn["longitude"]>0.001:
        avgLongitude = avgLongitude + asn["longitude"]
        counter = counter + 1
avgLongitude = avgLongitude / counter


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Draw ID AS point
counter = 0
counter0 = 0

for asn in asns:
    if asn["country"]["iso"] != 'ID':
        continue
    # print("Add point theta, r \t", theta, "\t", r)
    if asn["longitude"]<0.001:
        # print(asn)
        asn["longitude"] = avgLongitude
        counter0 = counter0 + 1
    counter = counter + 1

    theta = np.append(theta, np.deg2rad(asn["longitude"]))
    r = np.append(r, 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize))

    # ax.plot(np.deg2rad(asn["longitude"]), 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize), '*', markersize=15.0 - 1.0 + 2.0 * np.log10(asn["cone"]["numberAsns"]/maxClientConeSize), color='r' )


# Draw ID AS link
for asn in asns:
    if asn["country"]["iso"] != 'ID':
        continue
    # select link set
    if asn["asn"] not in mpProvider:
        continue
    for link in mpProvider[asn["asn"]]:
        # draw link edge:
        if mpAsns[link]["country"]["iso"] == 'ID':
            th1 = np.deg2rad(asn["longitude"])
            th2 = np.deg2rad(mpAsns[link]["longitude"])
            r1 = 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize)
            r2 = 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"]/maxClientConeSize)
            ax.plot(np.array([th1, th2]), np.array([r1, r2]), color="b", linewidth=0.3)

        # add external AS
        if mpAsns[link]["country"]["iso"] != 'ID':
            th1 = np.deg2rad(asn["longitude"])
            th2 = np.deg2rad(mpAsns[link]["longitude"])
            r1 = 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize)
            r2 = 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"]/maxClientConeSize)
            ax.plot(np.array([th1, th2]), np.array([r1, r2]), color="green", linewidth=0.3)

            theta_ex = np.append(theta_ex, np.deg2rad(mpAsns[link]["longitude"]))
            r_ex = np.append(r_ex, 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize))

            ax.plot(np.deg2rad(mpAsns[link]["longitude"]), 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize), '.',
                    markersize=10.0 - 1.0 + 1.0 * np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize), color='black')

for asn in asns:
    if asn["country"]["iso"] != 'ID':
            continue
    # select link set
    if asn["asn"] not in mpPeer:
        continue
    for link in mpPeer[asn["asn"]]:
        # draw link edge:
        if mpAsns[link]["country"]["iso"] == 'ID':
            th1 = np.deg2rad(asn["longitude"])
            th2 = np.deg2rad(mpAsns[link]["longitude"])
            r1 = 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize)
            r2 = 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"]/maxClientConeSize)
            ax.plot(np.array([th1, th2]), np.array([r1, r2]), color="violet", linewidth=0.3)

        # add external AS
        if mpAsns[link]["country"]["iso"] != 'ID':
            th1 = np.deg2rad(asn["longitude"])
            th2 = np.deg2rad(mpAsns[link]["longitude"])
            r1 = 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize)
            r2 = 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"]/maxClientConeSize)
            ax.plot(np.array([th1, th2]), np.array([r1, r2]), color="green", linewidth=0.1, alpha=0.5)

            theta_ex = np.append(theta_ex, np.deg2rad(mpAsns[link]["longitude"]))
            r_ex = np.append(r_ex, 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize))

            ax.plot(np.deg2rad(mpAsns[link]["longitude"]), 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize), '.',
                    markersize=10.0 - 1.0 + 1.0 * np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize), color='black')

#
# for asn in asns:
#     if asn["country"]["iso"] != 'ID':
#         continue
#     # select link set
#     if asn["asn"] not in mpPeer:
#         continue
#     for link in mpPeer[asn["asn"]]:
#         # draw link edge:
#         th1 = np.deg2rad(asn["longitude"])
#         th2 = np.deg2rad(mpAsns[link]["longitude"])
#         r1 = 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize)
#         r2 = 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"]/maxClientConeSize)
#         ax.plot(np.array([th1, th2]), np.array([r1, r2]), color="black", linewidth=0.5, alpha=0.5)
#         # add external AS
#         if mpAsns[link]["country"]["iso"] != 'ID':
#             theta_ex2 = np.append(theta_ex2, np.deg2rad(mpAsns[link]["longitude"]))
#             r_ex2 = np.append(r_ex2, 1.0 - np.log10(mpAsns[link]["cone"]["numberAsns"] / maxClientConeSize))


# final INFO
print("[INFO] With geoinfo and without:",counter, counter0)


# print final plt

# ax.set_rmax(2)
# ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
# ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
# ax.grid(True)
# ax.plot(theta, r, 'r.')
# ax.plot(theta_ex, r_ex, '.', color="black")
ax.plot(theta_ex2, r_ex2, 'y.')

for asn in asns:
    if asn["country"]["iso"] != 'ID':
        continue
    # print("Add point theta, r \t", theta, "\t", r)
    if asn["longitude"]<0.001:
        # print(asn)
        asn["longitude"] = avgLongitude
        counter0 = counter0 + 1
    counter = counter + 1

    # theta = np.append(theta, np.deg2rad(asn["longitude"]))
    # r = np.append(r, 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize))

    ax.plot(np.deg2rad(asn["longitude"]), 1.0 - np.log10(asn["cone"]["numberAsns"]/maxClientConeSize), '*', markersize=15.0 - 1.0 + 2.0 * np.log10(asn["cone"]["numberAsns"]/maxClientConeSize), color='r' )


ax.set_title("ID AS rank & Geo", va='bottom')
plt.show()
print()