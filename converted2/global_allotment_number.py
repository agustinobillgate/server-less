from functions.additional_functions import *
import decimal
from datetime import date
from models import Zimkateg, Queasy, Kontline

def global_allotment_number(sm_gastno:int, ta_gastno:int, ankunft:date, abreise:date, rmtype:str):
    allot_nr = 0
    tokcounter:int = 0
    mesvalue:str = ""
    zimkateg = queasy = kontline = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal allot_nr, tokcounter, mesvalue, zimkateg, queasy, kontline
        nonlocal sm_gastno, ta_gastno, ankunft, abreise, rmtype

        return {"allot_nr": allot_nr}


    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.kurzbez == rmtype)).first()

    if not zimkateg:

        return generate_output()

    kontline_obj_list = []
    for kontline, queasy in db_session.query(Kontline, Queasy).join(Queasy,(Queasy.key == 147) & (Queasy.number1 == sm_gastno) & (Queasy.char1 == Kontline.kontcode)).filter(
             (Kontline.gastnr == sm_gastno) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.ankunft <= ankunft) & (Kontline.abreise >= ankunft)).order_by(Kontline._recid).all():
        if kontline._recid in kontline_obj_list:
            continue
        else:
            kontline_obj_list.append(kontline._recid)


        for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
            mesvalue = entry(tokcounter - 1, queasy.char3, ",")

            if mesvalue != "" and to_int(mesvalue) == ta_gastno:
                allot_nr = kontline.kontignr

                return generate_output()

    return generate_output()