from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Bediener, Akt_line, Guest

def akt_calendar_fill_act_webbl(user_init:str, all_flag:bool, curr_month:int, curr_year:int):
    act_list = []
    lname:str = ""
    akt_code = bediener = akt_line = guest = None

    act = None

    act_list, Act = create_model("Act", {"linenr":int, "datum":date, "ftime":int, "ttime":int, "aktion":str, "lname":str, "kontakt":str, "regard":str, "sales":str, "priority":int, "flag":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal act_list, lname, akt_code, bediener, akt_line, guest


        nonlocal act
        nonlocal act_list
        return {"act": act_list}


    act_list.clear()

    if all_flag:

        akt_line_obj_list = []
        for akt_line, akt_code, bediener in db_session.query(Akt_line, Akt_code, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                (Akt_line.flag == 0) &  (get_month(Akt_line.datum) == curr_month) &  (get_year(Akt_line.datum) == curr_year)).all():
            if akt_line._recid in akt_line_obj_list:
                continue
            else:
                akt_line_obj_list.append(akt_line._recid)

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == akt_line.gastnr)).first()

            if guest:
                lname = guest.name + ", " + guest.anredefirma
            act = Act()
            act_list.append(act)

            act.linenr = akt_line.linenr
            act.datum = akt_line.datum
            act.ftime = akt_line.zeit
            act.ttime = akt_line.dauer
            act.aktion = akt_code.bezeich
            act.kontakt = akt_line.kontakt
            act.lname = lname
            act.regard = akt_line.regard
            act.sales = bediener.userinit
            act.priority = akt_line.prioritaet
            act.flag = akt_line.flag


    else:

        akt_line_obj_list = []
        for akt_line, akt_code, bediener in db_session.query(Akt_line, Akt_code, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                (Akt_line.flag == 0) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (get_month(Akt_line.datum) == curr_month) &  (get_year(Akt_line.datum) == curr_year)).all():
            if akt_line._recid in akt_line_obj_list:
                continue
            else:
                akt_line_obj_list.append(akt_line._recid)

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == akt_line.gastnr)).first()

            if guest:
                lname = guest.name + ", " + guest.anredefirma
            act = Act()
            act_list.append(act)

            act.linenr = akt_line.linenr
            act.datum = akt_line.datum
            act.ftime = akt_line.zeit
            act.ttime = akt_line.dauer
            act.aktion = akt_code.bezeich
            act.kontakt = akt_line.kontakt
            act.lname = lname
            act.regard = akt_line.regard
            act.sales = bediener.userinit
            act.priority = akt_line.prioritaet
            act.flag = akt_line.flag

    return generate_output()