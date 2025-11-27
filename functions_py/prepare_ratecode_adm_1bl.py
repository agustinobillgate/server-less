#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 27/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Waehrung, Ratecode, Prmarket, Prtable, Zimkateg, Arrangement
from sqlalchemy.orm import flag_modified

def prepare_ratecode_adm_1bl(pvilanguage:int):

    prepare_cache ([Queasy, Htparam, Prmarket, Zimkateg, Arrangement])

    msg_str = ""
    f_ratecode_data = []
    tb1_data = []
    lvcarea:string = "ratecode-admin"
    cidate:date = None
    queasy = htparam = waehrung = ratecode = prmarket = prtable = zimkateg = arrangement = None

    f_ratecode = tb1 = bqueasy = None

    f_ratecode_data, F_ratecode = create_model("F_ratecode", {"foreign_rate":bool, "double_currency":bool, "local_nr":int, "foreign_nr":int})
    tb1_data, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":string, "active_flag":bool})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, f_ratecode_data, tb1_data, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal pvilanguage
        nonlocal bqueasy


        nonlocal f_ratecode, tb1, bqueasy
        nonlocal f_ratecode_data, tb1_data

        return {"msg_str": msg_str, "f-ratecode": f_ratecode_data, "tb1": tb1_data}

    def update_queasy():

        nonlocal msg_str, f_ratecode_data, tb1_data, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal pvilanguage
        nonlocal bqueasy


        nonlocal f_ratecode, tb1, bqueasy
        nonlocal f_ratecode_data, tb1_data

        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        qsy = get_cache (Queasy, {"key": [(eq, 18)]})

        if not qsy:

            for prmarket in db_session.query(Prmarket).order_by(Prmarket.bezeich).all():
                qsy = Queasy()
                db_session.add(qsy)

                qsy.key = 18
                qsy.number1 = prmarket.nr


                pass

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"number1": [(eq, 0)]})

        if not queasy:

            return

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy.number1 == 0)).order_by(Queasy._recid).with_for_update().all():

            if (not f_ratecode.foreign_rate) or queasy.logi1:
                queasy.number1 = f_ratecode.local_nr
            else:
                queasy.number1 = f_ratecode.foreign_nr


    def update_prtable():

        nonlocal msg_str, f_ratecode_data, tb1_data, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal pvilanguage
        nonlocal bqueasy


        nonlocal f_ratecode, tb1, bqueasy
        nonlocal f_ratecode_data, tb1_data

        prbuff = None
        curr_i:int = 0
        Prbuff =  create_buffer("Prbuff",Prtable)

        prbuff = db_session.query(Prbuff).first()
        while None != prbuff:

            # prtable = get_cache (Prtable, {"_recid": [(eq, prbuff._recid)]})
            prtable = db_session.query(Prtable).filter(Prtable._recid == prbuff._recid).with_for_update().first()
            for curr_i in range(1,99 + 1) :
                prtable.zikatnr[curr_i - 1] = 0
                prtable.argtnr[curr_i - 1] = 0


            curr_i = 0

            for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.zikatnr).all():
                curr_i = curr_i + 1
                prtable.zikatnr[curr_i - 1] = zimkateg.zikatnr


            curr_i = 0

            for arrangement in db_session.query(Arrangement).filter(
                         not_ (Arrangement.weeksplit) & (Arrangement.segmentcode == 0)).order_by(Arrangement.argtnr).all():
                curr_i = curr_i + 1
                prtable.argtnr[curr_i - 1] = arrangement.argtnr


            pass

            curr_recid = prbuff._recid
            prbuff = db_session.query(Prbuff).filter(Prbuff._recid > curr_recid).with_for_update().first()
        flag_modified(prtable, "zikatnr")
        flag_modified(prtable, "argtnr")
        
    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    cidate = htparam.fdate
    f_ratecode = F_ratecode()
    f_ratecode_data.append(f_ratecode)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    f_ratecode.foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    f_ratecode.double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        msg_str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    f_ratecode.local_nr = waehrung.waehrungsnr

    if f_ratecode.foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if not waehrung:
            msg_str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

            return generate_output()
        f_ratecode.foreign_nr = waehrung.waehrungsnr
    update_queasy()

    queasy_obj_list = {}
    for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Queasy.number1)).filter(
             (Queasy.key == 2)).order_by(Queasy.logi2.desc(), Queasy.char2).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True


        tb1 = Tb1()
        tb1_data.append(tb1)

        buffer_copy(waehrung, tb1)
        buffer_copy(queasy, tb1)

        if queasy.logi2 == False:

            ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)]})

            if ratecode:

                ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"endperiode": [(ge, cidate)]})

                if ratecode:
                    tb1.logi3 = True
            else:
                tb1.logi3 = True

        if queasy.date2 < cidate:
            tb1.logi3 = False

        bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, queasy.char1)]})

        if bqueasy:
            tb1.active_flag = bqueasy.logi1

    return generate_output()