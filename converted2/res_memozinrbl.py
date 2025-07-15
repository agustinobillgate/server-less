#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Res_line

def res_memozinrbl(memo_zinr:string):

    prepare_cache ([Res_line])

    t_memozinr_data = []
    res_line = None

    t_memozinr = None

    t_memozinr_data, T_memozinr = create_model("T_memozinr", {"gastnr":int, "memozinr":string, "memodatum":date, "name":string, "ankunft":date, "abreise":date, "anztage":int, "arrangement":string, "zipreis":Decimal, "erwachs":int, "kind1":int, "resstatus":int, "resnr":int, "gastnrmember":int, "zinr":string, "active_flag":int, "reslinnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_memozinr_data, res_line
        nonlocal memo_zinr


        nonlocal t_memozinr
        nonlocal t_memozinr_data

        return {"t-memozinr": t_memozinr_data}

    def create_t_memozinr():

        nonlocal t_memozinr_data, res_line
        nonlocal memo_zinr


        nonlocal t_memozinr
        nonlocal t_memozinr_data


        t_memozinr = T_memozinr()
        t_memozinr_data.append(t_memozinr)

        t_memozinr.gastnr = res_line.gastnr
        t_memozinr.memozinr = res_line.memozinr
        t_memozinr.memodatum = res_line.memodatum
        t_memozinr.name = res_line.name
        t_memozinr.ankunft = res_line.ankunft
        t_memozinr.abreise = res_line.abreise
        t_memozinr.anztage = res_line.anztage
        t_memozinr.arrangement = res_line.arrangement
        t_memozinr.zipreis =  to_decimal(res_line.zipreis)
        t_memozinr.erwachs = res_line.erwachs
        t_memozinr.kind1 = res_line.kind1
        t_memozinr.resstatus = res_line.resstatus
        t_memozinr.resnr = res_line.resnr
        t_memozinr.gastnrmember = res_line.gastnrmember
        t_memozinr.zinr = res_line.zinr
        t_memozinr.active_flag = res_line.active_flag
        t_memozinr.reslinnr = res_line.reslinnr


    if memo_zinr == "":

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (matches(Res_line.memozinr,("*;*"))) & (trim(entry(1, Res_line.memozinr, ";")) != "")).order_by(Res_line.memozinr, Res_line.memodatum, Res_line.resnr).all():
            create_t_memozinr()
    else:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.memozinr >= ((";" + memo_zinr).lower()))).order_by(Res_line.memozinr, Res_line.memodatum, Res_line.resnr, Res_line.ankunft).all():
            create_t_memozinr()

    return generate_output()