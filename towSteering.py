import numpy as np
import math

def linearCustomVariation(nodes, elements, SS, frequency):
    # x and y coordinates of nodes
    x = nodes[:,1]
    y = nodes[:,2]

    # Calculate the lengths Lx and Ly
    Lx = np.amax(x) - np.amin(x)
    Ly = np.amax(y) - np.amin(y)
    D = math.sqrt(Lx**2 + Ly**2)

    # store element centroids
    nrElems = len(elements)
    centroid = np.zeros((nrElems,4))

    # Extract the element numbers from the 'elements' array and store them in the 'centroid' array
    elemNrs = [int(nr) for nr in elements[:,0]]
    centroid[:,0] = elemNrs

    # Calculate the centroids of each element and store them in the 'centroid' array
    for elem in elements:
        # nodeCoords = nodes[elem[1:]-1,1:]
        nodeCoords = filter(lambda n: n[0] in elem, nodes)
        nodeCoords = list(map(lambda n: n[1:], nodeCoords))
        nodeCoords = np.array(nodeCoords)

        centroid[elem[0]-1,1:] = np.mean(nodeCoords,axis=0)

    for layerNr in range(SS.nrLayers):
        layer = SS.stackingSequence[layerNr]
        phi = layer.phi * math.pi / 180

        # Calculate the distance 'd' from the centroid to the nearest edge along the angle 'phi'
        if abs(phi) == 0:
            d = Lx/2
        elif abs(phi) == 90 * math.pi / 180:
            d = Ly/2
        else:
            d = D/2

        # Calculate the x-coordinate of the centroid projected along the angle 'phi'
        xphi = centroid[:, 1] * np.cos(phi) + centroid[:, 2] * np.sin(phi)
        angles = []
        thickness = []

        # Loop through each element to compute angles and thicknesses
        for i in range(nrElems):
            for p in range(frequency):

                # Determine the angle for the current element at position 'p'
                if (-d + 2 * p * d / frequency) <= xphi[i] < (-d + (2 * p + 1) * d / frequency):
                    angle = layer.phi - (layer.t1 - layer.t0) / (d / frequency) * (xphi[i] + d - (2 * p + 1) * d / frequency) + layer.t0
                    angles.append([elemNrs[i], angle])
                elif (-d + (2 * p + 1) * d / frequency) <= xphi[i] < (-d + 2 * (p + 1) * d / frequency):
                    angle = layer.phi + (layer.t1 - layer.t0) / (d / frequency) * (xphi[i] + d - (2 * p + 1) * d / frequency) + layer.t0
                    angles.append([elemNrs[i], angle])
            # Calculate the thickness for the current element based on the computed angle
            thick = layer.nomThick / np.cos(np.abs(angle - layer.phi) * math.pi / 180)
            thickness.append([elemNrs[i], thick])
        # Update the current layer's angles and thicknesses properties  
        layer.towSteering(angles, thickness)
    return
