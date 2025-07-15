from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Res_line, Interface

def nt_custom_emailtrigger():
    datum:date = None
    ci_days:int = 0
    co_days:int = 0
    ci_flag:str = ""
    co_flag:str = ""
    res_line = interface = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, ci_days, co_days, ci_flag, co_flag, res_line, interface
        nonlocal resline


        nonlocal resline

        return {}

    def readsession():

        nonlocal datum, ci_days, co_days, ci_flag, co_flag, res_line, interface
        nonlocal resline


        nonlocal resline

        str_param:str = ""
        param1:str = ""
        param_file:str = ""
        fpath:str = ""
        fpath = SEARCH ("C:\\e1-vhp\\greetmail.cfg")

        if fpath != None:
            INPUT STREAM s1 FROM VALUE (fpath)
            while True:
                IMPORT STREAM s1 UNFORMATTED str_param

                if not re.match(r".*#.*",str_param, re.IGNORECASE):

                    if num_entries(str_param, "=") == 2:
                        param1 = entry(0, str_param, "=")

                        if re.match(r".*checkin-flag.*",param1, re.IGNORECASE):
                            ci_flag = trim(entry(1, str_param, "="))

                        if re.match(r".*checkout-flag.*",param1, re.IGNORECASE):
                            co_flag = trim(entry(1, str_param, "="))

                        if re.match(r".*days-before-checkin.*",param1, re.IGNORECASE):
                            ci_days = to_int(trim(entry(1, str_param, "=")))

                        if re.match(r".*days-after-checkout.*",param1, re.IGNORECASE):
                            co_days = to_int(trim(entry(1, str_param, "=")))
            INPUT STREAM s1 CLOSE

            if re.match(r".*e.*",co_flag, re.IGNORECASE) and co_days > 0:
                co_days = co_days - 1
        else:
            ci_days = 7
            co_days = 2
            ci_flag = "yes"
            co_flag = "yes"


    readsession()
    datum = get_output(htpdate(87))
    datum = datum - timedelta(days=1)

    if re.match(r".*e.*",ci_flag, re.IGNORECASE):

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.resstatus < 6) & (Res_line.ankunft - datum == ci_days) & (func.lower(not Res_line.zimmer_wunsch).op("~")(("*$CI7DAYSMAIL$*".lower().replace("*",".*"))))).first()
        while None != res_line:

            interface = db_session.query(Interface).filter(
                     (Interface.key == 7) & (Interface.resnr == res_line.resnr) & (Interface.reslinnr == res_line.reslinnr) & (func.lower(not Interface.nebenstelle).op("~")(("*$CI7DAYSMAIL$*".lower().replace("*",".*"))))).first()

            if not interface:
                interface = Interface()
                db_session.add(interface)

                interface.key = 7
                interface.zinr = res_line.zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield =  to_decimal("1")
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = "My Checkin!"
                interface.resnr = res_line.resnr
                interface.reslinnr = res_line.reslinnr


                pass
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$CI7DAYSMAIL$;"

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus < 6) & (Res_line.ankunft - datum <= 7) & (func.lower(not Res_line.zimmer_wunsch).op("~")(("*$CI7DAYSMAIL$*".lower().replace("*",".*")))) & (Res_line._recid > curr_recid)).first()

    if re.match(r".*e.*",co_flag, re.IGNORECASE):

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (datum - Res_line.abreise == co_days) & (func.lower(not Res_line.zimmer_wunsch).op("~")(("*$CO3DAYSMAIL$*".lower().replace("*",".*"))))).first()
        while None != res_line:

            interface = db_session.query(Interface).filter(
                     (Interface.key == 7) & (Interface.resnr == res_line.resnr) & (Interface.reslinnr == res_line.reslinnr) & (func.lower(not Interface.nebenstelle).op("~")(("*$CO3DAYSMAIL$*".lower().replace("*",".*"))))).first()

            if not interface:
                interface = Interface()
                db_session.add(interface)

                interface.key = 7
                interface.zinr = res_line.zinr
                interface.nebenstelle = ""
                interface.intfield = 0
                interface.decfield =  to_decimal("2")
                interface.int_time = get_current_time_in_seconds()
                interface.intdate = get_current_date()
                interface.parameters = "My Checkout!"
                interface.resnr = res_line.resnr
                interface.reslinnr = res_line.reslinnr


                pass
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$CO3DAYSMAIL$;"

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (datum - Res_line.abreise == 2) & (func.lower(not Res_line.zimmer_wunsch).op("~")(("*$CO3DAYSMAIL$*".lower().replace("*",".*")))) & (Res_line._recid > curr_recid)).first()

    return generate_output()