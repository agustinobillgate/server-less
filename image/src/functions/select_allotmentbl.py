from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline, Htparam, Res_line

def select_allotmentbl(main_gastnr:int, gastnr:int, ktype:int, zikatnr:int, argt:str, erwachs:int, ankunft:date, abreise:date, qty:int, resno:int, reslinno:int):
    kcode = ""
    remark = ""
    t_kontline_list = []
    ci_date:date = None
    delta:int = 0
    do_it:bool = False
    overbook_flag:bool = False
    found_kontcode:str = ""
    kontline = htparam = res_line = None

    t_kontline = allot_list = overbook_list = s_list = kline = kbuff = None

    t_kontline_list, T_kontline = create_model_like(Kontline)
    allot_list_list, Allot_list = create_model("Allot_list", {"kontcode":str, "ruecktage":int})
    overbook_list_list, Overbook_list = create_model("Overbook_list", {"kontcode":str, "overbook":int})
    s_list_list, S_list = create_model("S_list", {"datum":date, "zimmeranz":int})

    Kline = Kontline
    Kbuff = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kcode, remark, t_kontline_list, ci_date, delta, do_it, overbook_flag, found_kontcode, kontline, htparam, res_line
        nonlocal kline, kbuff


        nonlocal t_kontline, allot_list, overbook_list, s_list, kline, kbuff
        nonlocal t_kontline_list, allot_list_list, overbook_list_list, s_list_list
        return {"kcode": kcode, "remark": remark, "t-kontline": t_kontline_list}

    def check_allot_overbook():

        nonlocal kcode, remark, t_kontline_list, ci_date, delta, do_it, overbook_flag, found_kontcode, kontline, htparam, res_line
        nonlocal kline, kbuff


        nonlocal t_kontline, allot_list, overbook_list, s_list, kline, kbuff
        nonlocal t_kontline_list, allot_list_list, overbook_list_list, s_list_list

        overbook_flag = False
        datum:date = None
        beg_date:date = None
        end_date:date = None

        def generate_inner_output():
            return overbook_flag
        Kline = Kontline
        Kbuff = Kontline

        for kline in db_session.query(Kline).filter(
                (Kline.kontcode == kontline.kontcode) &  (Kline.kontstatus == 1) &  (not Kline.ankunft >= abreise) &  (not Kline.abreise < ankunft)).all():
            s_list_list.clear()
            beg_date = kontline.ankunft

            if ankunft > beg_date:
                beg_date = ankunft
            end_date = kontline.abreise

            if (abreise - 1) < end_date:
                end_date = abreise - 1
            for datum in range(beg_date,end_date + 1) :
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.datum = datum
                s_list.zimmeranz = kontline.zimmeranz - qty

            res_line_obj_list = []
            for res_line, kbuff in db_session.query(Res_line, Kbuff).join(Kbuff,(Kbuff.kontignr == Res_line.kontignr) &  (Kbuff.kontstat == 1) &  (Kbuff.kontcode == kontline.kontcode)).filter(
                    (Res_line.kontignr > 0) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (not Res_line.ankunft > beg_date) &  (not (Res_line.abreise - 1) < end_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                if res_line.resnr == resno and res_line.reslinnr == reslinno:
                    1
                else:
                    for datum in range(beg_date,end_date + 1) :

                        if datum >= res_line.ankunft and datum < res_line.abreise:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.datum == datum), first=True)
                            s_list.zimmeranz = s_list.zimmeranz - res_line.zimmeranz

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.zimmeranz < 0)):

                overbook_list = query(overbook_list_list, filters=(lambda overbook_list :overbook_list.kontcode == kontline.kontcode), first=True)

                if not overbook_list:
                    overbook_list = Overbook_list()
                    overbook_list_list.append(overbook_list)

                    overbook_list.kontcode = kontline.kontcode


                overbook_flag = True

                if overbook_list.overbook > s_list.zimmeranz:
                    overbook_list.overbook = s_list.zimmeranz
                break


        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if ankunft < ci_date:
        delta = 9999
    else:
        delta = ankunft - ci_date

    kline = db_session.query(Kline).filter(
                (Kline.gastnr == gastnr) &  (Kline.betriebsnr == ktype)).first()

    if kline:

        for kontline in db_session.query(Kontline).filter(
                    (Kontline.gastnr == gastnr) &  (Kontline.betriebsnr == ktype)).all():
            do_it = True

            if main_gastnr != gastnr:
                do_it = (kontline.pr_code != "")

            if do_it:

                allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.kontcode == kontline.kontcode and allot_list.ruecktage == kontline.ruecktage), first=True)

                if not allot_list:
                    allot_list = Allot_list()
                    allot_list_list.append(allot_list)

                    allot_list.kontcode = kontline.kontcode
                    allot_list.ruecktage = kontline.ruecktage

        for allot_list in query(allot_list_list):

            kontline = db_session.query(Kontline).filter(
                        (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs == erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (Kontline.arrangement == "") &  (Kontline.erwachs == erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs >= erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (Kontline.arrangement == "") &  (Kontline.erwachs >= erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs == erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (Kontline.arrangement == "") &  (Kontline.erwachs == erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.kontstat == 1) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs >= erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (Kontline.arrangement == "") &  (Kontline.erwachs >= erwachs) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.kontstat == 1) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs == 0) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == zikatnr) &  (Kontline.arrangement == "") &  (Kontline.erwachs == 0) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (func.lower(Kontline.arrangement) == (argt).lower()) &  (Kontline.erwachs == 0) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if not kontline:

                kontline = db_session.query(Kontline).filter(
                            (Kontline.gastnr == gastnr) &  (Kontline.kontcode == allot_list.kontcode) &  (Kontline.betriebsnr == ktype) &  (Kontline.zikatnr == 0) &  (Kontline.arrangement == "") &  (Kontline.erwachs == 0) &  ((Kontline.ankunft >= Kontline.ankunft)) &  ((Kontline.ankunft <= Kontline.abreise)) &  (Kontline.kontstat == 1) &  (Kontline.delta >= Kontline.ruecktage)).first()

            if kontline:
                overbook_flag = check_allot_overbook()

                if not overbook_flag:
                    found_kontcode = kontline.kontcode
                    break

    if found_kontcode == "":

        for overbook_list in query(overbook_list_list):
            found_kontcode = overbook_list.kontcode
            break


    if found_kontcode != "":

        kontline = db_session.query(Kontline).filter(
                    (func.lower(Kontline.kontcode) == (found_kontcode).lower()) &  (Kontline.kontstat == 1)).first()
        kcode = kontline.kontcode
        remark = kontline.bemerk


        t_kontline = T_kontline()
        t_kontline_list.append(t_kontline)

        buffer_copy(kontline, t_kontline)

    return generate_output()