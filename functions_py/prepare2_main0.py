#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.nt_bahistory import nt_bahistory
from functions.nt_bapostbill import nt_bapostbill
from models import Htparam

def prepare2_main0(pvilanguage:int):

    prepare_cache ([Htparam])

    stop_it = False
    quit_it = False
    dummy_str = ""
    msg_str = ""
    notice_day:int = 14
    lvcarea:string = "e1-main0"
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stop_it, quit_it, dummy_str, msg_str, notice_day, lvcarea, htparam
        nonlocal pvilanguage

        return {"stop_it": stop_it, "quit_it": quit_it, "dummy_str": dummy_str, "msg_str": msg_str}

    def check_license_date():

        nonlocal stop_it, quit_it, dummy_str, msg_str, notice_day, lvcarea, htparam
        nonlocal pvilanguage

        billdate:date = None
        condo_flag:bool = False
        htp1 = None
        htp2 = None
        Htp1 =  create_buffer("Htp1",Htparam)
        Htp2 =  create_buffer("Htp2",Htparam)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 981)]})

        if htparam.flogical:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 724)]})
            condo_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if (htparam.finteger == 1) or condo_flag:

            htp1 = get_cache (Htparam, {"paramnr": [(eq, 985)]})

            htp2 = get_cache (Htparam, {"paramnr": [(eq, 724)]})

            # htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            htparam = db_session.query(Htparam).filter(Htparam.paramnr == 110).with_for_update().first()

            if htparam.fdate != get_current_date():
                pass
                htparam.fdate = get_current_date()
                pass

            # htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
            htparam = db_session.query(Htparam).filter(Htparam.paramnr == 87).with_for_update().first()

            if htparam.fdate != get_current_date():
                pass
                htparam.fdate = get_current_date()
                pass

                if htp1.flogical:
                    get_output(nt_bahistory())

            if htp1.flogical and htp2.flogical:
                get_output(nt_bapostbill())

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate

        if billdate == None or billdate > get_current_date():
            billdate = get_current_date()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 976)]})

        if htparam.fdate != None:

            if htparam.fdate < get_current_date() or htparam.fdate < billdate:
                stop_it = True
                msg_str = translateExtended ("Your License was valid until : ", lvcarea, "") + to_string(htparam.fdate, "99/99/9999") + chr_unicode(10) + translateExtended ("Please contact your next Our Technical Support for further information.", lvcarea, "") + chr_unicode(2)

            elif (htparam.fdate - notice_day) <= get_current_date():

                # htp1 = get_cache (Htparam, {"paramnr": [(eq, 1072)]})
                htp1 = db_session.query(Htparam).filter(Htparam.paramnr == 1072).with_for_update().first()
                htp1.finteger = 1072


                pass
                msg_str = translateExtended ("Your License is valid until :", lvcarea, "") + to_string(htparam.fdate, "99/99/9999") + chr_unicode(10) + translateExtended ("Please contact your next Our Technical Support for further information", lvcarea, "") + chr_unicode(2)

                return
        else:
            stop_it = True

        htp1 = get_cache (Htparam, {"paramnr": [(eq, 1072)]})

        if htp1.finteger == 1027:
            stop_it = True
            quit_it = True

        if stop_it:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})

            if htparam.flogical or (htp1.finteger == 1072):

                # htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})
                htparam = db_session.query(Htparam).filter(Htparam.paramnr == 996).with_for_update().first()
                htparam.fchar = ""
                
                htp1.finteger = 1027


                pass


    dummy_str = "MyLord"


    check_license_date()

    return generate_output()