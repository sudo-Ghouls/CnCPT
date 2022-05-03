from Input.CoralSea.CnCPT_Experiments.VariableMainBombsAway import run as BArun
from Input.CoralSea.CnCPT_Experiments.VariableMainCarrierCarnage import run as CCrun
from Input.CoralSea.CnCPT_Experiments.VariableMainEndersGame import run as EGrun
from Input.CoralSea.PostProcessing.SetMetricGeneration import run as SetProcessor

# CCrun()
# BArun()
# EGrun()


SetProcessor(path=r"D:\Thesis\CoralSeaBaseline\Baseline\2021-07-24-212344",
              output=r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis\LyX Thesis\figures\BaselinePerformanc")
SetProcessor(path=r"D:\Thesis\CnCPT_Tests\CoralSeaCarrierCarnagePeakArch\CarrierCarnage\2021-07-27-211706",
              output=r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis\LyX Thesis\figures\CarrierCarnage")
SetProcessor(path=r"D:\Thesis\CnCPT_Tests\CoralSeaBombsAwayPeakArch\BombsAway\2021-07-27-211703",
             output=r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis\LyX Thesis\figures\BombsAway")
SetProcessor(path=r"D:\Thesis\CnCPT_Tests\CoralSeaEndersGamePeakArch\EndersGame\2021-07-27-211700",
             output=r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis\LyX Thesis\figures\EndersGame")
