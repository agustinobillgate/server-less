#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
#------------------------------------------

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

import time

def rmcat_segment_create_output_webbl():
    doneflag = False
    rmcat_segm_list_data = []
    counter:int = 0
    queasy = None

    rmcat_segm_list = bqueasy = pqueasy = tqueasy = None

    rmcat_segm_list_data, Rmcat_segm_list = create_model("Rmcat_segm_list", {"flag":int, "segment":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string, "rmnite1":string, "rmrev1":string, "rmnite":string, "rmrev":string, "rmcat":string, "segm_code":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, rmcat_segm_list_data, counter, queasy
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal rmcat_segm_list, bqueasy, pqueasy, tqueasy
        nonlocal rmcat_segm_list_data

        return {"doneflag": doneflag, "rmcat-segm-list": rmcat_segm_list_data}

    count = retry = tmp_count = 0
    while True:
        count = db_session.query(Queasy).filter(
            (Queasy.key == 280) &
            (Queasy.char1 == ("Guest Segment By Room Type").lower())
        ).count()

        if count >= 1000:
            break

        if tmp_count == 0 and retry > 60:
            break

        if tmp_count > 0 and tmp_count == count:
            break

        tmp_count = count
        retry += 1

        time.sleep(0.3)

    for queasy in db_session.query(Queasy).filter((Queasy.key == 280) & (Queasy.char1 == ("Guest Segment By Room Type").lower())).order_by(Queasy.number1).all():
        
        counter = counter + 1

        if counter > 1000:
            break

        rmcat_segm_list = Rmcat_segm_list()
        rmcat_segm_list_data.append(rmcat_segm_list)

        rmcat_segm_list.flag = to_int(entry(0, queasy.char2 , "|"))
        rmcat_segm_list.segment = entry(1, queasy.char2 , "|")
        rmcat_segm_list.room = entry(2, queasy.char2 , "|")
        rmcat_segm_list.pax = entry(3, queasy.char2 , "|")
        rmcat_segm_list.logis = entry(4, queasy.char2 , "|")
        rmcat_segm_list.proz = entry(5, queasy.char2 , "|")
        rmcat_segm_list.avrgrate = entry(6, queasy.char2 , "|")
        rmcat_segm_list.m_room = entry(7, queasy.char2 , "|")
        rmcat_segm_list.m_pax = entry(8, queasy.char2 , "|")
        rmcat_segm_list.m_logis = entry(9, queasy.char2 , "|")
        rmcat_segm_list.m_proz = entry(10, queasy.char2 , "|")
        rmcat_segm_list.m_avrgrate = entry(11, queasy.char2 , "|")
        rmcat_segm_list.y_room = entry(12, queasy.char2 , "|")
        rmcat_segm_list.y_pax = entry(13, queasy.char2 , "|")
        rmcat_segm_list.y_logis = entry(14, queasy.char2 , "|")
        rmcat_segm_list.y_proz = entry(15, queasy.char2 , "|")
        rmcat_segm_list.y_avrgrate = entry(16, queasy.char2 , "|")
        rmcat_segm_list.rmnite1 = entry(17, queasy.char2 , "|")
        rmcat_segm_list.rmrev1 = entry(18, queasy.char2 , "|")
        rmcat_segm_list.rmnite = entry(19, queasy.char2 , "|")
        rmcat_segm_list.rmrev = entry(20, queasy.char2 , "|")
        rmcat_segm_list.rmcat = entry(21, queasy.char2 , "|")
        rmcat_segm_list.segm_code = to_int(entry(22, queasy.char2 , "|"))

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).with_for_update().first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Guest Segment By Room Type").lower()) & (Pqueasy.char3 == ("PROCESS").lower())).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Segment By Room Type").lower()) & (Tqueasy.number1 == 1)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    return generate_output()