from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Htparam, Nightaudit

def na_startbl(case_type:int, user_init:str, htparam_recid:int):
    mnstart_flag = False
    store_flag = False
    printer_nr = 0
    t_nightaudit_list = []
    na_date = None
    na_time = 0
    na_name = ""
    ci_date:date = None
    bediener = htparam = nightaudit = None

    t_nightaudit = None

    t_nightaudit_list, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":str, "hogarest":int, "reihenfolge":int, "programm":str, "abschlussart":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit


        nonlocal t_nightaudit
        nonlocal t_nightaudit_list
        return {"mnstart_flag": mnstart_flag, "store_flag": store_flag, "printer_nr": printer_nr, "t-nightaudit": t_nightaudit_list, "na_date": na_date, "na_time": na_time, "na_name": na_name}

    def na_prog():

        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit


        nonlocal t_nightaudit
        nonlocal t_nightaudit_list

        night_type:int = 0
        mn_stopped:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        for nightaudit in db_session.query(Nightaudit).filter(
                (Nightaudit.selektion)).all():
            t_nightaudit = T_nightaudit()
            t_nightaudit_list.append(t_nightaudit)

            t_nightaudit.bezeichnung = nightaudit.bezeichnung
            t_nightaudit.hogarest = nightaudit.hogarest
            t_nightaudit.reihenfolge = nightaudit.reihenfolge
            t_nightaudit.programm = nightaudit.programm
            t_nightaudit.abschlussart = nightaudit.abschlussart

    def check_mn_start():

        nonlocal mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date, na_time, na_name, ci_date, bediener, htparam, nightaudit


        nonlocal t_nightaudit
        nonlocal t_nightaudit_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 105)).first()

        if htparam.fdate < get_current_date():
            mnstart_flag = True

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 230)).first()

    if htparam.feldtyp == 4 and htparam.flogical:
        store_flag = True

    if case_type == 1:

        htparam = db_session.query(Htparam).filter(
                    (Htparam._recid == htparam_recid)).first()
        htparam.flogical = True
        check_mn_start()

        if mnstart_flag:

            return generate_output()
        na_prog()


    if case_type == 2:
        na_prog()

    if case_type == 3:

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()
        htparam.fchar = bediener.username
        htparam.fdate = get_current_date()
        htparam.finteger = get_current_time_in_seconds()
        htparam.flogical = False

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 102)).first()
        htparam.fdate = get_current_date()

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 103)).first()
        htparam.finteger = get_current_time_in_seconds()

        htparam = db_session.query(Htparam).first()


        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 99)).first()
        printer_nr = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 102)).first()
        na_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 103)).first()
        na_time = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 253)).first()
        na_name = htparam.fchar

    return generate_output()