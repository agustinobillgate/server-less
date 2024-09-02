from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Waehrung, Ratecode, Prmarket, Prtable, Zimkateg, Arrangement

def prepare_ratecode_admbl(pvilanguage:int):
    msg_str = ""
    f_ratecode_list = []
    tb1_list = []
    lvcarea:str = "ratecode_admin"
    cidate:date = None
    queasy = htparam = waehrung = ratecode = prmarket = prtable = zimkateg = arrangement = None

    f_ratecode = tb1 = qsy = prbuff = None

    f_ratecode_list, F_ratecode = create_model("F_ratecode", {"foreign_rate":bool, "double_currency":bool, "local_nr":int, "foreign_nr":int})
    tb1_list, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":str})

    Qsy = Queasy
    Prbuff = Prtable

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, f_ratecode_list, tb1_list, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal qsy, prbuff


        nonlocal f_ratecode, tb1, qsy, prbuff
        nonlocal f_ratecode_list, tb1_list
        return {"msg_str": msg_str, "f-ratecode": f_ratecode_list, "tb1": tb1_list}

    def update_queasy():

        nonlocal msg_str, f_ratecode_list, tb1_list, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal qsy, prbuff


        nonlocal f_ratecode, tb1, qsy, prbuff
        nonlocal f_ratecode_list, tb1_list


        Qsy = Queasy

        qsy = db_session.query(Qsy).filter(
                (Qsy.key == 18)).first()

        if not qsy:

            for prmarket in db_session.query(Prmarket).all():
                qsy = Qsy()
                db_session.add(qsy)

                qsy.key = 18
                qsy.number1 = prmarket.nr


        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.number1 == 0)).first()

        if not queasy:

            return

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.number1 == 0)).all():

            if (not f_ratecode.foreign_rate) or queasy.logi1:
                queasy.number1 = f_ratecode.local_nr
            else:
                queasy.number1 = f_ratecode.foreign_nr

    def update_prtable():

        nonlocal msg_str, f_ratecode_list, tb1_list, lvcarea, cidate, queasy, htparam, waehrung, ratecode, prmarket, prtable, zimkateg, arrangement
        nonlocal qsy, prbuff


        nonlocal f_ratecode, tb1, qsy, prbuff
        nonlocal f_ratecode_list, tb1_list

        curr_i:int = 0
        Prbuff = Prtable

        prbuff = db_session.query(Prbuff).first()
        while None != prbuff:

            prtable = db_session.query(Prtable).filter(
                        (Prtable._recid == prbuff._recid)).first()
            for curr_i in range(1,99 + 1) :
                prtable.zikatnr[curr_i - 1] = 0
                prtable.argtnr[curr_i - 1] = 0


            curr_i = 0

            for zimkateg in db_session.query(Zimkateg).all():
                curr_i = curr_i + 1
                prtable.zikatnr[curr_i - 1] = zimkateg.zikatnr


            curr_i = 0

            for arrangement in db_session.query(Arrangement).filter(
                        (not Arrangement.weeksplit) &  (Arrangement.segmentcode == 0)).all():
                curr_i = curr_i + 1
                prtable.argtnr[curr_i - 1] = arrangement.argtnr

            prtable = db_session.query(Prtable).first()


            prbuff = db_session.query(Prbuff).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    cidate = htparam.fdate
    f_ratecode = F_ratecode()
    f_ratecode_list.append(f_ratecode)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    f_ratecode.foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    f_ratecode.double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        msg_str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    f_ratecode.local_nr = waehrung.waehrungsnr

    if f_ratecode.foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if not waehrung:
            msg_str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "")

            return generate_output()
        f_ratecode.foreign_nr = waehrung.waehrungsnr
    update_queasy()

    queasy_obj_list = []
    for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Queasy.number1)).filter(
            (Queasy.key == 2)).all():
        if queasy._recid in queasy_obj_list:
            continue
        else:
            queasy_obj_list.append(queasy._recid)


        tb1 = Tb1()
        tb1_list.append(tb1)

        buffer_copy(waehrung, tb1)
        buffer_copy(queasy, tb1)

        if queasy.logi2 == False:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.code == queasy.char1)).first()

            if ratecode:

                ratecode = db_session.query(Ratecode).filter(
                        (Ratecode.code == queasy.char1) &  (Ratecode.endperiode >= cidate)).first()

                if ratecode:
                    tb1.logi3 = True
            else:
                tb1.logi3 = True

        # if queasy.date2 < cidate:
        # if queasy.date2 is not None and queasy.date2 < cidate: 
        if queasy.date2 and queasy.date2 < cidate:  
            tb1.logi3 = False

    return generate_output()