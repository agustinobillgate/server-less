from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Reslin_queasy, Bediener

def prepare_flag_reportbl(resnr:int, reslinnr:int, user_init:str):
    perm_bediener = False
    s_list_list = []
    t_res_line_list = []
    n:int = 0
    res_line = reslin_queasy = bediener = None

    s_list = t_res_line = None

    s_list_list, S_list = create_model("S_list", {"newflag":bool, "id":str, "frdate":date, "datum":date, "note":str, "urgent":bool, "done":bool, "dept":str, "ciflag":bool, "coflag":bool}, {"newflag": True})
    t_res_line_list, T_res_line = create_model_like(Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal perm_bediener, s_list_list, t_res_line_list, n, res_line, reslin_queasy, bediener


        nonlocal s_list, t_res_line
        nonlocal s_list_list, t_res_line_list
        return {"perm_bediener": perm_bediener, "s-list": s_list_list, "t-res-line": t_res_line_list}

    def fill_additionals(inp_char:str):

        nonlocal perm_bediener, s_list_list, t_res_line_list, n, res_line, reslin_queasy, bediener


        nonlocal s_list, t_res_line
        nonlocal s_list_list, t_res_line_list

        curr_i:int = 0
        mesvalue:str = ""
        s_list.frdate = s_list.datum

        if num_entries(inp_char, chr(2)) < 2:

            return
        for curr_i in range(2,num_entries(inp_char, chr(2))  + 1) :

            if curr_i == 2:
                s_list.id = entry(1, inp_char, chr(2))
            elif curr_i == 3:
                mesvalue = entry(2, inp_char, chr(2))
                s_list.frdate = date_mdy(to_int(substring(mesvalue, 0, 2)) , to_int(substring(mesvalue, 2, 2)) , to_int(substring(mesvalue, 4)))


            elif curr_i == 4:
                s_list.dept = entry(3, inp_char, chr(2))
            elif curr_i == 5:
                mesvalue = entry(4, inp_char, chr(2))
                s_list.ciflag = logical(to_int(mesvalue))


            elif curr_i == 6:
                mesvalue = entry(5, inp_char, chr(2))

                if mesvalue.lower()  == "SP":
                    s_list.id = s_list.id + chr(2) + "SP"

    forPEAT n in range(0,2 + 1) :

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "flag") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.betriebsnr == n)).first()
        s_list = S_list()
        s_list_list.append(s_list)


        if reslin_queasy:
            s_list.datum = reslin_queasy.date1
            s_list.coflag = reslin_queasy.logi1

            if s_list.datum != None:
                s_list.newflag = False
                s_list.note = entry(0, reslin_queasy.char1, chr(2))

            if reslin_queasy.number1 == 1:
                s_list.urgent = True
            else:
                s_list.urgent = False

            if reslin_queasy.deci1 == 1:
                s_list.done = True
            else:
                s_list.done = False
            fill_additionals(reslin_queasy.char1)
        s_list = S_list()
        s_list_list.append(s_list)


        if reslin_queasy:
            s_list.datum = reslin_queasy.date2
            s_list.coflag = reslin_queasy.logi2

            if s_list.datum != None:
                s_list.newflag = False
                s_list.note = entry(0, reslin_queasy.char2, chr(2))

            if reslin_queasy.number2 == 1:
                s_list.urgent = True
            else:
                s_list.urgent = False

            if reslin_queasy.deci2 == 1:
                s_list.done = True
            else:
                s_list.done = False
            fill_additionals(reslin_queasy.char2)
        s_list = S_list()
        s_list_list.append(s_list)


        if reslin_queasy:
            s_list.datum = reslin_queasy.date3
            s_list.coflag = reslin_queasy.logi3

            if s_list.datum != None:
                s_list.newflag = False
                s_list.note = entry(0, reslin_queasy.char3, chr(2))

            if reslin_queasy.number3 == 1:
                s_list.urgent = True
            else:
                s_list.urgent = False

            if reslin_queasy.deci3 == 1:
                s_list.done = True
            else:
                s_list.done = False
            fill_additionals(reslin_queasy.char3)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line:
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        buffer_copy(res_line, t_res_line)

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if substring(bediener.permissions, 2, 1) >= "2":
        perm_bediener = True

    return generate_output()