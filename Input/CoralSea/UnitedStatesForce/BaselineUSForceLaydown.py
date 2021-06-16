# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from Input.CoralSea.UnitedStatesForce.Ships.Carrier import *
from Input.CoralSea.UnitedStatesForce.Ships.Cruiser import *
from Input.CoralSea.UnitedStatesForce.Ships.Destroyer import *
from Input.CoralSea.UnitedStatesForce.Ships.Oiler import *
from Simulation.Communication.Network import Network
from Simulation.GeographyPhysics.Route import Route
from Simulation.Units.UnitGroup import UnitGroup


# Key Routes
def generate():
    AttackGroupRoute = [[-16.61325742288191, 161.2624376950124],
                        [-15.35373806064343, 161.3148868928264],
                        [-15.38675187566123, 162.2427751910915],
                        [-15.7786311345869, 162.0301041091591],
                        [-15.26419026143816, 159.6526568620639],
                        [-15.41351102360973, 159.1313209162425],
                        [-15.55887431344029, 159.3826949013127],
                        [-15.65336747114963, 159.9001806328554],
                        [-15.45510035677882, 159.9214277514328],
                        [-13.91326450221125, 154.9753518169748],
                        [-13.12907570734553, 155.0301252873949],
                        [-12.96626719259832, 155.586022633566],
                        [-12.47811092358964, 155.3289800758214],
                        [-12.67277198003261, 154.8518691855203],
                        [-12.98306002439211, 154.5807956244051],
                        [-13.23306772403876, 154.7248356535849],
                        [-13.48333012484096, 155.1400489169969],
                        [-13.58857530708372, 155.6180642761009],
                        [-14.7615647760328, 156.0415677766121]]
    CarrierGroupRoute = [[-13.1953703361602, 162.6115750992276],
                         [-14.2280427297137, 162.034964954163],
                         [-14.51699604557892, 161.9132150663179],
                         [-14.85473178248497, 162.0146980521283],
                         [-15.36911756254429, 161.6959115422963],
                         [-15.35617443845455, 161.526399588367],
                         [-15.46202421822671, 161.4887472919887],
                         [-15.60436529515835, 162.0375865086702],
                         [-15.79007697254667, 162.0206453433435],
                         [-15.26346412598481, 159.6581324711684],
                         [-15.30679981421354, 159.37373225082],
                         [-15.42990180251101, 159.1218442121272],
                         [-15.54601688723742, 159.3872975117759],
                         [-15.65014331350265, 159.9057265925478],
                         [-15.45883742388986, 159.9241054946916],
                         [-13.92833014147837, 154.9507472899614],
                         [-13.12129000098644, 155.0438272583939],
                         [-12.94887273910516, 155.6036999857182],
                         [-12.46254984964913, 155.3425554081582],
                         [-12.66922156911239, 154.8634259196641],
                         [-12.99315378584018, 154.574908765777],
                         [-13.00905479290225, 154.5743528827088],
                         [-13.20581987140899, 154.7308998857392],
                         [-13.45864940110844, 155.1467175604898],
                         [-13.5542823078383, 155.6495007365256],
                         [-14.78806060516232, 156.0684892715881]]
    SupportGroupRoute = [[-16.59834447299642, 161.2628537934368],
                         [-15.38626209407319, 161.3309429672238],
                         [-15.40303164237325, 162.1986514007808],
                         [-15.7742880332862, 162.015647415628],
                         [-15.26608513107971, 159.6461583237851],
                         [-15.42496916402085, 159.1511944019296],
                         [-15.54141720433583, 159.3914166361719],
                         [-15.64672142729021, 159.9015308788787],
                         [-15.46246654503964, 159.9035217515793],
                         [-13.90952080060524, 154.9897659377866],
                         [-12.56472607447933, 153.6840012296599],
                         [-11.99280222425065, 151.6379731824633],
                         [-12.45894612475293, 151.0150526597657],
                         [-12.78793387348092, 151.2712143503414],
                         [-12.46836791107876, 150.5016446788218]]
    FuelingGroupRoute = [[-16.59889466700974, 161.2578838985434],
                         [-15.38527468015399, 161.3325533893463],
                         [-15.40173284337855, 162.2084038659163],
                         [-15.77030075995826, 162.0112117746427],
                         [-15.25793528766928, 159.642634625678],
                         [-15.39888867768689, 159.1292677768703],
                         [-15.55924785448078, 159.378026323725],
                         [-15.64797349261584, 159.9089754912651],
                         [-15.51284429627344, 159.9106509156254],
                         [-15.34995163796034, 159.4912271281955],
                         [-15.34078382626441, 159.1587100385139],
                         [-15.59798946641972, 159.357057095539],
                         [-17.0066222246347, 159.0027379775643],
                         [-17.01458533781163, 159.1539829909298],
                         [-16.69444319541967, 159.2370017868244],
                         [-16.34460344520065, 158.4748809335572]]

    # AttackGroup
    AttackGroupUnits = [Minneapolis(), NewOrleans(), Astoria(), Chester(), Portland(), Phelps(), Dewey(), Farragut(),
                        Alywin(), Monaghan()]

    AttackGroup = UnitGroup.construct_unit_group("AttackGroup", AttackGroupUnits, leader=AttackGroupUnits[0],
                                                 route=Route(AttackGroupRoute))

    # CarrierGroup
    CarrierGroupUnits = [Yorktown(), Lexington(), Morris(), Anderson(), Hammann(), Russell()]
    CarrierGroup = UnitGroup.construct_unit_group("CarrierGroup", CarrierGroupUnits, leader=CarrierGroupUnits[0],
                                                  route=Route(CarrierGroupRoute))

    # SupportGroup
    SupportGroupUnits = [Australia(), Hobart(), Chicago(), Perkins(), Walke()]
    SupportGroup = UnitGroup.construct_unit_group("SupportGroup", SupportGroupUnits, leader=SupportGroupUnits[0],
                                                  route=Route(SupportGroupRoute))

    # FuelingGroup
    FuelingGroupUnits = [Neosho(), Tippecanoe(), Sims(), Worden()]
    FuelingGroup = UnitGroup.construct_unit_group("FuelingGroup", FuelingGroupUnits,
                                                  leader=FuelingGroupUnits[0],
                                                  route=Route(FuelingGroupRoute))
    all_units = AttackGroup + CarrierGroup + SupportGroup + \
                FuelingGroup

    Network('US', all_units)
    return all_units


BaselineUSForce = generate
