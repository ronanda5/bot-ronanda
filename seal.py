from enum import Enum


class Seal(Enum):

    CITY_OF_LS = "https://cdn.discordapp.com/attachments/818119814240665640/818122275818963004/Seal_of_Los_Santos.png"
    LSPD = "https://i.servimg.com/u/f62/15/10/04/98/14094910.png"
    SA = "https://cdn.discordapp.com/attachments/689355937466548237/700726187135205506/ZiYDsGM.png"
    CORONER = "https://cdn.discordapp.com/attachments/820941310961778689/823233484230230036/DepartmentOfCoronerLosSantosCounty-GTAV-Seal.png"
    INTERNAL_AFFAIRS = "https://cdn.discordapp.com/attachments/820941310961778689/823244543981256724/LYetGYu.png"

    def __str__(self):
        return str(self.value)
