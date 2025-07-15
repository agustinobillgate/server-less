#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line

def res_checkin_assignbl(case_type:int, resnr:int, reslinnr:int, nat_bez:string, purno:int):

    prepare_cache ([Guest, Res_line])

    guest = res_line = None

    gast = res_line1 = rline = res_sharer = None

    Gast = create_buffer("Gast",Guest)
    Res_line1 = create_buffer("Res_line1",Res_line)
    Rline = create_buffer("Rline",Res_line)
    Res_sharer = create_buffer("Res_sharer",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest, res_line
        nonlocal case_type, resnr, reslinnr, nat_bez, purno
        nonlocal gast, res_line1, rline, res_sharer


        nonlocal gast, res_line1, rline, res_sharer

        return {}


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if case_type == 1:

        gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        pass
        gast.land = nat_bez
        pass

    elif case_type == 2:

        gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        pass
        gast.nation1 = nat_bez
        pass

    elif case_type == 3:
        pass
        res_line.zimmer_wunsch = res_line.zimmer_wunsch +\
                "SEGM_PUR" + to_string(purno) + ";"


        pass

        res_line1 = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"l_zuordnung[2]": [(eq, 0)]})
        while None != res_line1:

            if not matches(res_line1.zimmer_wunsch,r"*SEGM_PUR*"):

                rline = get_cache (Res_line, {"_recid": [(eq, res_line1._recid)]})

                if rline:
                    rline.zimmer_wunsch = rline.zimmer_wunsch +\
                            "SEGM_PUR" + to_string(purno) + ";"


                    pass

            curr_recid = res_line1._recid
            res_line1 = db_session.query(Res_line1).filter(
                         (Res_line1.resnr == res_line.resnr) & (Res_line1.reslinnr != res_line.reslinnr) & (Res_line1.active_flag <= 1) & (Res_line1.resstatus != 12) & (Res_line1.l_zuordnung[inc_value(2)] == 0) & (Res_line1._recid > curr_recid)).first()

    elif case_type == 4:
        pass

        for res_sharer in db_session.query(Res_sharer).filter(
                 (Res_sharer.resnr == resnr) & (Res_sharer.kontakt_nr == reslinnr) & (Res_sharer.l_zuordnung[inc_value(2)] == 1)).order_by(Res_sharer._recid).all():
            res_sharer.zinr = res_line.zinr
            res_sharer.zikatnr = res_line.zikatnr
            res_sharer.setup = res_line.setup

    return generate_output()