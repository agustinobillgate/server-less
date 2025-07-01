#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Htparam, Res_line

def select_allotmentbl(main_gastnr:int, gastnr:int, ktype:int, zikatnr:int, argt:string, erwachs:int, ankunft:date, abreise:date, qty:int, resno:int, reslinno:int):

    prepare_cache ([Htparam, Res_line])

    kcode = ""
    remark = ""
    t_kontline_list = []
    ci_date:date = None
    delta:int = 0
    do_it:bool = False
    overbook_flag:bool = False
    found_kontcode:string = ""
    kontline = htparam = res_line = None

    t_kontline = allot_list = overbook_list = s_list = kline = None

    t_kontline_list, T_kontline = create_model_like(Kontline)
    allot_list_list, Allot_list = create_model("Allot_list", {"kontcode":string, "ruecktage":int})
    overbook_list_list, Overbook_list = create_model("Overbook_list", {"kontcode":string, "overbook":int})
    s_list_list, S_list = create_model("S_list", {"datum":date, "zimmeranz":int})

    Kline = create_buffer("Kline",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kcode, remark, t_kontline_list, ci_date, delta, do_it, overbook_flag, found_kontcode, kontline, htparam, res_line
        nonlocal main_gastnr, gastnr, ktype, zikatnr, argt, erwachs, ankunft, abreise, qty, resno, reslinno
        nonlocal kline


        nonlocal t_kontline, allot_list, overbook_list, s_list, kline
        nonlocal t_kontline_list, allot_list_list, overbook_list_list, s_list_list

        return {"kcode": kcode, "remark": remark, "t-kontline": t_kontline_list}

    def check_allot_overbook():

        nonlocal kcode, remark, t_kontline_list, ci_date, delta, do_it, overbook_flag, found_kontcode, kontline, htparam, res_line
        nonlocal main_gastnr, gastnr, ktype, zikatnr, argt, erwachs, ankunft, abreise, qty, resno, reslinno
        nonlocal kline


        nonlocal t_kontline, allot_list, overbook_list, s_list, kline
        nonlocal t_kontline_list, allot_list_list, overbook_list_list, s_list_list

        overbook_flag = False
        datum:date = None
        beg_date:date = None
        end_date:date = None
        kline = None
        kbuff = None

        def generate_inner_output():
            return (overbook_flag)

        Kline =  create_buffer("Kline",Kontline)
        Kbuff =  create_buffer("Kbuff",Kontline)

        for kline in db_session.query(Kline).filter(
                 (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1) & not_ (Kline.ankunft >= abreise) & not_ (Kline.abreise < ankunft)).order_by(Kline._recid).all():
            s_list_list.clear()
            beg_date = kontline.ankunft

            if ankunft > beg_date:
                beg_date = ankunft
            end_date = kontline.abreise

            if (abreise - 1) < end_date:
                end_date = abreise - timedelta(days=1)
            for datum in date_range(beg_date,end_date) :
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.datum = datum
                s_list.zimmeranz = kontline.zimmeranz - qty

            res_line_obj_list = {}
            for res_line, kbuff in db_session.query(Res_line, Kbuff).join(Kbuff,(Kbuff.kontignr == Res_line.kontignr) & (Kbuff.kontstat == 1) & (Kbuff.kontcode == kontline.kontcode)).filter(
                     (Res_line.kontignr > 0) & (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & not_ (Res_line.ankunft > beg_date) & (not_ (Res_line.abreise - 1) < end_date)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True

                if res_line.resnr == resno and res_line.reslinnr == reslinno:
                    pass
                else:
                    for datum in date_range(beg_date,end_date) :

                        if datum >= res_line.ankunft and datum < res_line.abreise:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.datum == datum), first=True)
                            s_list.zimmeranz = s_list.zimmeranz - res_line.zimmeranz

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.zimmeranz < 0), sort_by=[("zimmeranz",False)]):

                overbook_list = query(overbook_list_list, filters=(lambda overbook_list: overbook_list.kontcode == kontline.kontcode), first=True)

                if not overbook_list:
                    overbook_list = Overbook_list()
                    overbook_list_list.append(overbook_list)

                    overbook_list.kontcode = kontline.kontcode


                overbook_flag = True

                if overbook_list.overbook > s_list.zimmeranz:
                    overbook_list.overbook = s_list.zimmeranz
                break

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if ankunft < ci_date:
        delta = 9999
    else:
        delta = (ankunft - ci_date).days

    kline = db_session.query(Kline).filter(
                 (Kline.gastnr == gastnr) & (Kline.betriebsnr == ktype)).first()

    if kline:

        for kontline in db_session.query(Kontline).filter(
                     (Kontline.gastnr == gastnr) & (Kontline.betriebsnr == ktype)).order_by(Kontline.ruecktage.desc()).all():
            do_it = True

            if main_gastnr != gastnr:
                do_it = (kontline.pr_code != "")

            if do_it:

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.kontcode == kontline.kontcode and allot_list.ruecktage == kontline.ruecktage), first=True)

                if not allot_list:
                    allot_list = Allot_list()
                    allot_list_list.append(allot_list)

                    allot_list.kontcode = kontline.kontcode
                    allot_list.ruecktage = kontline.ruecktage

        for allot_list in query(allot_list_list, sort_by=[("ruecktage",True)]):

            kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, argt)],"erwachs": [(eq, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, "")],"erwachs": [(eq, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, argt)],"erwachs": [(ge, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, "")],"erwachs": [(ge, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, argt)],"erwachs": [(eq, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, "")],"erwachs": [(eq, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"kontstatus": [(eq, 1)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, argt)],"erwachs": [(ge, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, "")],"erwachs": [(ge, erwachs)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"kontstatus": [(eq, 1)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, argt)],"erwachs": [(eq, 0)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, zikatnr)],"arrangement": [(eq, "")],"erwachs": [(eq, 0)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, argt)],"erwachs": [(eq, 0)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"ruecktage": [(le, delta)]})

            if not kontline:

                kontline = get_cache (Kontline, {"gastnr": [(eq, gastnr)],"kontcode": [(eq, allot_list.kontcode)],"betriebsnr": [(eq, ktype)],"zikatnr": [(eq, 0)],"arrangement": [(eq, "")],"erwachs": [(eq, 0)],"ankunft ": [(le, ankunft)],"abreise ": [(ge, ankunft)],"kontstatus": [(eq, 1)],"ruecktage": [(le, delta)]})

            if kontline:
                overbook_flag = check_allot_overbook()

                if not overbook_flag:
                    found_kontcode = kontline.kontcode
                    break

    if found_kontcode == "":

        for overbook_list in query(overbook_list_list, sort_by=[("overbook",True)]):
            found_kontcode = overbook_list.kontcode
            break


    if found_kontcode != "":

        kontline = get_cache (Kontline, {"kontcode": [(eq, found_kontcode)],"kontstatus": [(eq, 1)]})
        kcode = kontline.kontcode
        remark = kontline.bemerk


        t_kontline = T_kontline()
        t_kontline_list.append(t_kontline)

        buffer_copy(kontline, t_kontline)

    return generate_output()