#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Bediener, Akt_line, Guest

def akt_calendar_fill_act_webbl(user_init:string, all_flag:bool, curr_month:int, curr_year:int):

    prepare_cache ([Akt_code, Bediener, Akt_line, Guest])

    act_data = []
    lname:string = ""
    akt_code = bediener = akt_line = guest = None

    act = None

    act_data, Act = create_model("Act", {"linenr":int, "datum":date, "ftime":int, "ttime":int, "aktion":string, "lname":string, "kontakt":string, "regard":string, "sales":string, "priority":int, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal act_data, lname, akt_code, bediener, akt_line, guest
        nonlocal user_init, all_flag, curr_month, curr_year


        nonlocal act
        nonlocal act_data

        return {"act": act_data}


    act_data.clear()

    if all_flag:

        akt_line_obj_list = {}
        akt_line = Akt_line()
        akt_code = Akt_code()
        bediener = Bediener()
        for akt_line.gastnr, akt_line.linenr, akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.kontakt, akt_line.regard, akt_line.prioritaet, akt_line.flag, akt_line._recid, akt_code.bezeich, akt_code._recid, bediener.userinit, bediener._recid in db_session.query(Akt_line.gastnr, Akt_line.linenr, Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.kontakt, Akt_line.regard, Akt_line.prioritaet, Akt_line.flag, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Bediener.userinit, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                 (Akt_line.flag == 0) & (get_month(Akt_line.datum) == curr_month) & (get_year(Akt_line.datum) == curr_year)).order_by(Akt_line._recid).all():
            if akt_line_obj_list.get(akt_line._recid):
                continue
            else:
                akt_line_obj_list[akt_line._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, akt_line.gastnr)]})

            if guest:
                lname = guest.name + ", " + guest.anredefirma
            act = Act()
            act_data.append(act)

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

        akt_line_obj_list = {}
        akt_line = Akt_line()
        akt_code = Akt_code()
        bediener = Bediener()
        for akt_line.gastnr, akt_line.linenr, akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.kontakt, akt_line.regard, akt_line.prioritaet, akt_line.flag, akt_line._recid, akt_code.bezeich, akt_code._recid, bediener.userinit, bediener._recid in db_session.query(Akt_line.gastnr, Akt_line.linenr, Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.kontakt, Akt_line.regard, Akt_line.prioritaet, Akt_line.flag, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Bediener.userinit, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                 (Akt_line.flag == 0) & (Akt_line.userinit == (user_init).lower()) & (get_month(Akt_line.datum) == curr_month) & (get_year(Akt_line.datum) == curr_year)).order_by(Akt_line._recid).all():
            if akt_line_obj_list.get(akt_line._recid):
                continue
            else:
                akt_line_obj_list[akt_line._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, akt_line.gastnr)]})

            if guest:
                lname = guest.name + ", " + guest.anredefirma
            act = Act()
            act_data.append(act)

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