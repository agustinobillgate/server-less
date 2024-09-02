from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Hoteldpt, Kellner

def prepare_rest_daymercurebl():
    exchg_rate = 0
    curr_local = ""
    curr_foreign = ""
    from_date = None
    h_art_coupon = 0
    t_hoteldpt_list = []
    t_kellner_list = []
    htparam = waehrung = hoteldpt = kellner = None

    t_kellner = t_hoteldpt = None

    t_kellner_list, T_kellner = create_model("T_kellner", {"kellnername":str, "kellner_nr":int, "departement":int, "rec_id":int})
    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, curr_local, curr_foreign, from_date, h_art_coupon, t_hoteldpt_list, t_kellner_list, htparam, waehrung, hoteldpt, kellner


        nonlocal t_kellner, t_hoteldpt
        nonlocal t_kellner_list, t_hoteldpt_list
        return {"exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "from_date": from_date, "h_art_coupon": h_art_coupon, "t-hoteldpt": t_hoteldpt_list, "t-kellner": t_kellner_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    h_art_coupon = htparam.fINTEGER

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    for kellner in db_session.query(Kellner).all():
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        t_kellnername = kellnername
        t_kellner_nr = kellner_nr
        t_kellner.departement = kellner.departement
        t_kellner.rec_id = kellner._recid

    return generate_output()