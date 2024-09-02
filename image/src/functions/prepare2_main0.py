from functions.additional_functions import *
import decimal
from datetime import date
from functions.nt_bahistory import nt_bahistory
from functions.nt_bapostbill import nt_bapostbill
from models import Htparam

def prepare2_main0(pvilanguage:int):
    stop_it = False
    quit_it = False
    dummy_str = ""
    msg_str = ""
    notice_day:int = 14
    lvcarea:str = "e1_main0"
    htparam = None

    htp1 = htp2 = None

    Htp1 = Htparam
    Htp2 = Htparam

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stop_it, quit_it, dummy_str, msg_str, notice_day, lvcarea, htparam
        nonlocal htp1, htp2


        nonlocal htp1, htp2
        return {"stop_it": stop_it, "quit_it": quit_it, "dummy_str": dummy_str, "msg_str": msg_str}

    def check_license_date():

        nonlocal stop_it, quit_it, dummy_str, msg_str, notice_day, lvcarea, htparam
        nonlocal htp1, htp2


        nonlocal htp1, htp2

        billdate:date = None
        condo_flag:bool = False
        Htp1 = Htparam
        Htp2 = Htparam

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 981)).first()

        if htparam.flogical:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 724)).first()
            condo_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 975)).first()

        if (htparam.finteger == 1) or condo_flag:

            htp1 = db_session.query(Htp1).filter(
                    (Htp1.paramnr == 985)).first()

            htp2 = db_session.query(Htp2).filter(
                    (Htp2.paramnr == 724)).first()

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()

            if htparam.fdate != get_current_date():

                htparam = db_session.query(Htparam).first()
                htparam.fdate = get_current_date()

                htparam = db_session.query(Htparam).first()

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 87)).first()

            if htparam.fdate != get_current_date():

                htparam = db_session.query(Htparam).first()
                htparam.fdate = get_current_date()

                htparam = db_session.query(Htparam).first()

                if htp1.flogical:
                    get_output(nt_bahistory())

            if htp1.flogical and htp2.flogical:
                get_output(nt_bapostbill())

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate

        if billdate == None or billdate > get_current_date():
            billdate = get_current_date()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 976)).first()

        if htparam.fdate != None:

            if htparam.fdate < get_current_date() or htparam.fdate < billdate:
                stop_it = True
                msg_str = translateExtended ("Your License was valid until : ", lvcarea, "") + to_string(htparam.fdate, "99/99/9999") + chr(10) + translateExtended ("Please contact your next Our Technical Support for further information.", lvcarea, "") + chr(2)

            elif (htparam.fdate - notice_day) <= get_current_date():

                htp1 = db_session.query(Htp1).filter(
                        (Htp1.paramnr == 1072)).first()
                htp1.finteger = 1072

                htp1 = db_session.query(Htp1).first()
                msg_str = translateExtended ("Your License is valid until :", lvcarea, "") + to_string(htparam.fdate, "99/99/9999") + chr(10) + translateExtended ("Please contact your next Our Technical Support for further information", lvcarea, "") + chr(2)

                return
        else:
            stop_it = True

        htp1 = db_session.query(Htp1).filter(
                (Htp1.paramnr == 1072)).first()

        if htp1.finteger == 1027:
            stop_it = True
            quit_it = True

        if stop_it:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 999)).first()

            if htparam.flogical or (htp1.finteger == 1072):

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 996)).first()
                htparam.fchar = ""

                htparam = db_session.query(Htparam).first()

                htp1 = db_session.query(Htp1).first()
                htp1.finteger = 1027

                htp1 = db_session.query(Htp1).first()

    dummy_str = "MyLord"


    check_license_date()

    return generate_output()