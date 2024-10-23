from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline, Res_line

def allotment_check_reslinebl(kontcode:str, kontignr:int):
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

        res_line_obj_list = []
        for res_line, kline in db_session.query(Res_line, Kline).join(Kline,(Kline.kontignr == Res_line.kontignr) & (Kline.kontcode == kontline.kontcode) & (Kline.kontstat == 1)).filter(
                 (Res_line.kontignr > 0) & (Res_line.active_flag < 2) & (Res_line.resstatus < 11)).order_by(Res_line._recid).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if res_line.abreise <= kontline.ankunft or res_line.ankunft > kontline.abreise:
                pass
            else:
                res_line_resnr = res_line.resnr
                res_line_name = res_line.name
                res_line_ankunft = res_line.ankunft
                res_line_abreise = res_line.abreise
                it_exist = True

                return

    kontline = db_session.query(Kontline).filter(
             (Kontline.kontignr == kontignr) & (func.lower(Kontline.kontcode) == (kontcode).lower())).first()
    check_resline()

    return generate_output()