import numpy as np

def elementAreas(nodes, elements):
    areas = []
    for elem in elements:
        nodeCoords = nodes[elem[1:]-1,1:]
        nodeCoords1 = np.array([[nodeCoords[0,0], nodeCoords[1,0], nodeCoords[2,0]],
                                [nodeCoords[0,1], nodeCoords[1,1], nodeCoords[2,1]],
                                [1, 1, 1]])
        nodeCoords2 = np.array([[nodeCoords[0, 0], nodeCoords[3, 0], nodeCoords[2, 0]],
                                [nodeCoords[0, 1], nodeCoords[3, 1], nodeCoords[2, 1]],
                                [1, 1, 1]])
        area = 0.5*np.abs(np.linalg.det(nodeCoords1)) + 0.5*np.abs(np.linalg.det(nodeCoords2))
        areas.append([elem[0], area])

    return areas

def computeMass(areas, SS):
    elemMass = []
    for area in areas:
        elemNr = area[0]
        areaVal = area[1]

        thickDense = 0
        for layer in SS.stackingSequence:
            thickDense += (layer.material.rho * layer.thickness[elemNr-1][1])
        elemMass.append(thickDense*areaVal)

    return sum(elemMass)