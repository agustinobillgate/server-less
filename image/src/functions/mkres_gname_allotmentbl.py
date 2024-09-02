from functions.additional_functions import *
import decimal
from datetime import date
from models import Kontline, Zimkateg

def mkres_gname_allotmentbl(pvilanguage:int, inp_gastnr:int, ci_date:date, co_date:date):
    allot_bemerk = ""
    rmtype:str = ""
    lvcarea:str = "mkres_gname"
    kontline = zimkateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal allot_bemerk, rmtype, lvcarea, kontline, zimkateg


        return {"allot_bemerk": allot_bemerk}


    for kontline in db_session.query(Kontline).filter(
            (Kontline.gastnr == inp_gastnr) &  (Kontline.kontignr > 0) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1) &  (Kontline.ankunft <= ci_date) &  (Kontline.abreise >= (co_date - 1))).all():

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == kontline.zikatnr)).first()
        rmtype = ""

        if zimkateg:
            rmtype = zimkateg.kurzbez

        if allot_bemerk == "":
            allot_bemerk = translateExtended ("Allotment:", lvcarea, "") + chr(10)
        allot_bemerk = allot_bemerk + to_string(kontline.kontcode, "x(10)  ") + to_string(kontline.ankunft) + " - " + to_string(kontline.abreise) + "  " + to_string(rmtype, "x(6)  ") + translateExtended ("QTY:", lvcarea, "") + to_string(kontline.zimmeranz, ">>9  ") + translateExtended ("A:", lvcarea, "") + to_string(kontline.erwachs, "9  ") + to_string(kontline.ruecktage, ">9 ") + translateExtended ("days", lvcarea, "") + chr(10)

    return generate_output()