class Layup:
    def __init__(self, nrLayers):
        self.nrLayers = nrLayers
        self.stackingSequence = [0]*nrLayers

    def addLayer(self, layerNumber, material, phi, t0, t1, nomThick):
        self.stackingSequence[layerNumber] = Layer(material, phi, t0, t1, nomThick)

class Layer:
    def __init__(self, material, phi, t0, t1, nomThick):
        self.material = material
        self.phi = phi
        self.t0 = t0
        self.t1 = t1
        self.nomThick = nomThick
        self.angles = []
        self.thickness = []

    def towSteering(self, angles, thickness):
        self.angles = angles
        self.thickness = thickness
