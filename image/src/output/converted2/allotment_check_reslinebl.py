#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Res_line

def allotment_check_reslinebl(kontcode:string, kontignr:int):

    prepare_cache ([Kontline, Res_line])

    it_exist = False
    res_line_resnr = 0
    res_line_name = ""
    res_line_ankunft = None
    res_line_abreise = None
    kontline = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, res_line_resnr, res_line_name, res_line_ankunft, res_line_abreise, kontline, res_line
        nonlocal kontcode, kontignr

        return {"it_exist": it_exist, "res_line_resnr": res_line_resnr, "res_line_name": res_line_name, "res_line_ankunft": res_line_ankunft, "res_line_abreise": res_line_abreise}

    def check_resline():

        nonlocal it_exist, res_line_resnr, res_line_name, res_line_ankunft, res_line_abreise, kontline, res_line
        nonlocal kontcode, kontignr

        d:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)

        res_line_obj_list = {}
        res_line = Res_line()
        kline = Kontline()
        for res_line.ankunft, res_line.resnr, res_line.name, res_line.abreise, res_line._recid, kline.kontcode, kline.ankunft, kline.abreise, kline._recid in db_session.query(Res_line.ankunft, Res_line.resnr, Res_line.name, Res_line.abreise, Res_line._recid, Kline.kontcode, Kline.ankunft, Kline.abreise, Kline._recid).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstatus == 1)).filter(
                 (Res_line.kontignr > 0) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.abreise <= kontline.ankunft or res_line.ankunft > kontline.abreise:
                pass
            else:
                res_line_resnr = res_line.resnr
                res_line_name = res_line.name
                res_line_ankunft = res_line.ankunft
                res_line_abreise = res_line.abreise
                it_exist = True

                return

    kontline = get_cache (Kontline, {"kontignr": [(eq, kontignr)],"kontcode": [(eq, kontcode)]})
    check_resline()

    return generate_output()