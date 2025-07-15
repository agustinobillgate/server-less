#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimmer, Res_line, Outorder, Zimkateg

na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":string, "anz":int})

def update_rmstatusbl(na_list_data:[Na_list], ci_date:date):

    prepare_cache ([Htparam, Res_line, Zimkateg])

    i = 0
    htparam = zimmer = res_line = outorder = zimkateg = None

    na_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, zimmer, res_line, outorder, zimkateg
        nonlocal ci_date


        nonlocal na_list

        return {"na-list": na_list_data, "i": i}

    def update_rmstatus():

        nonlocal i, htparam, zimmer, res_line, outorder, zimkateg
        nonlocal ci_date


        nonlocal na_list

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 3), first=True)

        zimmer = db_session.query(Zimmer).first()
        while None != zimmer:

            if zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 2:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

            elif zimmer.zistatus == 3:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line and res_line.abreise > ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0
                    pass

            elif zimmer.zistatus == 4 or zimmer.zistatus == 5:

                res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(eq, 6)]})

                if res_line and res_line.abreise == ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 3
                    zimmer.bediener_nr_stat = 0
                    pass

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0
                    pass

            if zimmer.zistatus == 6:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.zinr == zimmer.zinr) & (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1
                    pass

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0
                    pass

                    outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(lt, res_line.abreise)]})

                    if outorder:
                        db_session.delete(outorder)
                else:

                    outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})

                    if not outorder:
                        pass
                        zimmer.bediener_nr_stat = 0
                        zimmer.zistatus = 2


                        pass

            curr_recid = zimmer._recid
            zimmer = db_session.query(Zimmer).filter(Zimmer._recid > curr_recid).first()

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 0

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
                i = i + 1
            zimkateg.maxzimanz = i

    update_rmstatus()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 592)]})
    htparam.flogical = False


    pass

    return generate_output()