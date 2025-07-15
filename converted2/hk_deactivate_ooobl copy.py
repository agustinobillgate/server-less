from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.deactivate_ooo2_cldbl import deactivate_ooo2_cldbl
from models import Bediener, Outorder, Queasy, Guestbook

def hk_deactivate_ooobl(userinit:str, rec_id:int):
    ci_date:date = None
    oos_flag:bool = False
    user_nr:int = 0
    bediener = outorder = queasy = guestbook = None

    om_list = ooo_list2 = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int})
    ooo_list2_list, Ooo_list2 = create_model("Ooo_list2", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, oos_flag, user_nr, bediener, outorder, queasy, guestbook
        nonlocal userinit, rec_id


        nonlocal om_list, ooo_list2
        nonlocal om_list_list, ooo_list2_list
        return {}


    if not bediener or not(bediener.userinit.lower()  == (userinit).lower()):
        bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (userinit).lower())).first()

    if not outorder or not(outorder._recid == rec_id):
        outorder = db_session.query(Outorder).filter(
            (Outorder._recid == rec_id)).first()

    if bediener and outorder:
        user_nr = bediener.nr
        oos_flag = (outorder.betriebsnr == 3 or outorder.betriebsnr == 4)

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 195) &  (func.lower(Queasy.char1) == ("ooo;room=" + outorder.zinr + ";from=" + to_string(get_day(outorder.gespstart) , "99") + "/" + to_string(get_month(outorder.gespstart) , "99") + "/" + to_string(get_year(outorder.gespstart) , "9999") + ";to=" + to_string(get_day(outorder.gespende) , "99") + "/" + to_string(get_month(outorder.gespende) , "99") + "/" + to_string(get_year(outorder.gespende) , "9999").lower()))).order_by(Queasy._recid).all():

            if not guestbook or not(guestbook.gastnr == queasy.number1):
                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number1)).first()

            if guestbook:
                db_session.delete(guestbook)
            db_session.delete(queasy)
        ooo_list2 = Ooo_list2()
        ooo_list2_list.append(ooo_list2)

        ooo_list2.zinr = outorder.zinr
        ooo_list2.betriebsnr = outorder.betriebsnr
        ooo_list2.gespstart = outorder.gespstart
        ooo_list2.gespende = outorder.gespende
        ci_date = get_output(htpdate(87))
        get_output(deactivate_ooo2_cldbl(user_nr, oos_flag, ci_date, ooo_list2_list))

    return generate_output()