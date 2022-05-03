# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from Input.CoralSea.JapaneseForce.Ships.Carrier import *
from Input.CoralSea.JapaneseForce.Ships.Destroyer import *
from Input.CoralSea.JapaneseForce.Ships.Gunboat import *
from Input.CoralSea.JapaneseForce.Ships.HeavyCruiser import *
from Input.CoralSea.JapaneseForce.Ships.LightCarrier import *
from Input.CoralSea.JapaneseForce.Ships.LightCrusier import *
from Input.CoralSea.JapaneseForce.Ships.Minelayer import *
from Input.CoralSea.JapaneseForce.Ships.Tanker import *
from Input.CoralSea.JapaneseForce.Ships.Transport import *
from Simulation.Communication.Network import Network
from Simulation.GeographyPhysics.Route import Route
from Simulation.Units.UnitGroup import UnitGroup


# Key Routes
def generate():
    CarrierStrikingForceRoute = [[-6.309272411760459, 159.269167854891],
                                 [-7.558709775869595, 161.9059842859587],
                                 [-11.30819453390537, 163.6609407134918],
                                 [-12.19881727899489, 163.2803879513366],
                                 [-10.06322277511949, 157.7454091606563],
                                 [-12.96746843263909, 157.9575578328857],
                                 [-12.99293897639469, 157.7670866453124],
                                 [-12.2307435141775, 157.7063900952184],
                                 [-12.2061259977582, 157.956405201686],
                                 [-13.15180442893302, 158.4639395269611],
                                 [-13.84759854012279, 158.2079359051129],
                                 [-14.06610195157517, 158.4546978145111],
                                 [-14.11335325382331, 158.9276829806527],
                                 [-13.96360695809203, 159.3147434392297],
                                 [-14.1519343337154, 158.9068191537002],
                                 [-13.81829924809434, 158.7415314291814],
                                 [-13.86126795101436, 158.4186404298945],
                                 [-13.61147936998388, 157.1623566429119],
                                 [-13.48125892034495, 156.6165890721359],
                                 [-13.32302378369696, 156.5111900532701],
                                 [-13.38326470153421, 156.9586720190962],
                                 [-12.14453265165522, 156.9119657926101]]
    TulagiInvasionForceRoute = [[-9.16923234376902, 160.3698927247138],
                                [-9.306110422730338, 160.1360708149053],
                                [-8.759667381613435, 159.7080411605896],
                                [-8.245177202229819, 158.7053473214262],
                                [-7.755087130650972, 157.6115771325726],
                                [-7.302258527282516, 156.4537025029807],
                                [-7.222800068276611, 155.3201671166482],
                                [-7.659402815144152, 154.3758438984474],
                                [-7.937752335117173, 154.1999120925358]]
    CoveringForceRoute = [[-8.937177345301652, 157.8861550323069],
                          [-9.309559511108707, 157.820629810522],
                          [-8.275640288089235, 155.7096152276701],
                          [-7.892760437312715, 155.7820399029006],
                          [-7.243020574554216, 155.9901720182435],
                          [-6.893707789309331, 155.8873115586983],
                          [-6.920954430287448, 155.4955673167401],
                          [-9.793555662250636, 154.7473059086399],
                          [-9.981134944054315, 154.4560144399041],
                          [-10.02089688903483, 154.7463513491011],
                          [-9.689671030924304, 154.8424920100337],
                          [-9.96619443401533, 153.7097871464988],
                          [-10.35146598775312, 154.0960935491734],
                          [-9.040361776854992, 154.8015359632598],
                          [-9.039914004175531, 155.1384279878075],
                          [-9.9988359684667, 155.067314549984]]
    PortMoresbyLandingForceRoute = [[-5.943349586170182, 152.9059613006714],
                                    [-6.867785049426172, 153.1694644704978],
                                    [-7.730683952862431, 153.7290208169704],
                                    [-8.474415337742805, 154.4923128526306],
                                    [-9.414565602433751, 154.6981648383449],
                                    [-10.39441628668191, 153.4672413729005],
                                    [-10.04617555897115, 153.2194367361948],
                                    [-10.47087367822104, 153.9091789776863],
                                    [-8.757624299856138, 154.1466911295505],
                                    [-8.167073300484102, 153.9355641690252]]

    # CarrierStrikingForce
    CarrierStrikingForceUnits = [Zuikaku(), Shokaku(), Myoko(), Haguro(), Ariake(), Yugure(), Shigure(), Ushio(),
                                 Akebono(),
                                 TohoMaru()]
    CarrierStrikingForce = UnitGroup.construct_unit_group("CarrierStrikingForce",
                                                          CarrierStrikingForceUnits,
                                                          leader=CarrierStrikingForceUnits[0],
                                                          route=Route(CarrierStrikingForceRoute,
                                                                      end_time_sec=3 * 24 * 3600.0))

    # TulagiInvasionForce
    TulagiInvasionForceUnits = [Kinugasa(), Furutaka(), Yubari(), Tenryu(), Tatsuta(), Sazanami(), Oite(), Tsugaru(),
                                KeijoMaru(), SeikaiMaru(), NikkaiMaru()]
    TulagiInvasionForce = UnitGroup.construct_unit_group("TulagiInvasionForce",
                                                         TulagiInvasionForceUnits, leader=TulagiInvasionForceUnits[0],
                                                         route=Route(TulagiInvasionForceRoute,
                                                                     end_time_sec=3 * 24 * 3600.0))

    # CoveringForce
    CoveringForceUnits = [Shoho(), Aoba(), Kako(), Uzuki(), Asamagi(), Mutsuki(), Yunagi(), Yayoi()]
    CoveringForce = UnitGroup.construct_unit_group("CoveringForce",
                                                   CoveringForceUnits, leader=CoveringForceUnits[0],
                                                   route=Route(CoveringForceRoute, end_time_sec=3 * 24 * 3600.0))

    # PortMoresbyLandingForce
    PortMoresbyLandingForceUnits = [Kaikuzuki(), Yuzuki(), Okinoshima(), KoeiMaru(), AsumanMaru()]
    PortMoresbyLandingForce = UnitGroup.construct_unit_group("PortMoresbyLandingForce",
                                                             PortMoresbyLandingForceUnits,
                                                             leader=PortMoresbyLandingForceUnits[0],
                                                             route=Route(PortMoresbyLandingForceRoute,
                                                                         end_time_sec=3 * 24 * 3600.0))
    all_units = CarrierStrikingForce + TulagiInvasionForce + CoveringForce + \
                PortMoresbyLandingForce
    Network("JapaneseForce", all_units)
    return all_units


BaselineJapaneseForce = generate
