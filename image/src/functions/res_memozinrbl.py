from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line

def res_memozinrbl(memo_zinr:str):
    t_memozinr_list = []
    res_line = None

    t_memozinr = None

    t_memozinr_list, T_memozinr = create_model("T_memozinr", {"gastnr":int, "memozinr":str, "memodatum":date, "name":str, "ankunft":date, "abreise":date, "anztage":int, "arrangement":str, "zipreis":decimal, "erwachs":int, "kind1":int, "resstatus":int, "resnr":int, "gastnrmember":int, "zinr":str, "active_flag":int, "reslinnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_memozinr_list, res_line


        nonlocal t_memozinr
        nonlocal t_memozinr_list
        return {"t-memozinr": t_memozinr_list}

    def create_t_memozinr():

        nonlocal t_memozinr_list, res_line


        nonlocal t_memozinr
        nonlocal t_memozinr_list


        t_memozinr = T_memozinr()
        t_memozinr_list.append(t_memozinr)

        t_memozinr.gastnr = res_line.gastnr
        t_memozinr.memozinr = res_line.memozinr
        t_memozinr.memodatum = res_line.memodatum
        t_memozinr.name = res_line.name
        t_memozinr.ankunft = res_line.ankunft
        t_memozinr.abreise = res_line.abreise
        t_memozinr.anztage = res_line.anztage
        t_memozinr.arrangement = res_line.arrangement
        t_memozinr.zipreis = res_line.zipreis
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
                (Res_line.active_flag <= 1) &  (Res_line.memozinr.op("~")(".*;.*")) &  (trim(entry(1, Res_line.memozinr, ";")) != "")).all():
            create_t_memozinr()
    else:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (func.lower(Res_line.memozinr) >= (";" + memo_zinr))).all():
            create_t_memozinr()

    return generate_output()