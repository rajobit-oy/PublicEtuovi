from dataclasses import dataclass


mappings={
    "Firma":"muualta sivulta",
    "Myyjänimi":"muaalta sivulta",
    "Nimi":"Sijainti",
    "Tyyppi":"Tyyppi",  #Tähän lisätään myös Huoneistoselitelmä
    "Hinta":"Velaton hinta",
    "Koko":"Kokonaispinta-ala",
    "Vuosi":"Rakennusvuosi",
    "KansioPolku":"Osoite google driveen",
    "Kuvat":"=HYPERLINK(H{index})",
    "PVM":"Now",
    "KohdeNumero":"Kohdenumero",
    "VanhaHinta":"Velaton hinta",
    "PVM_Vanhahinta":"Now", 
    "Linkki":"laitetaan"
}

@dataclass
class EtuoviData:
    Firma:str
    Myyjänimi:str
    Nimi:str
    Tyyppi:str
    Hinta:str
    Koko:str
    Vuosi:str
    KansioPolku:str
    Kuvat:str
    PVM:str
    KohdeNumero:str
    VanhaHinta:str
    PVM_Vanhahinta:str

if __name__ == "__main__":
    print("")
    import os
    full_path = os.path.realpath(__file__)
    print("in __main__:"+full_path + "\n")
    
    dt=EtuoviData()