#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Guest, Genstat

def nt_tauziarpt_gen_revdatabl(fdate1:date, tdate1:date):
    s_list_list = []
    w_int:int = 0
    indv:int = 0
    htparam = guest = genstat = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"gastnr":int, "datum":str, "name":str, "address":str, "city":str, "zimmeranz":int, "lodging":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, w_int, indv, htparam, guest, genstat
        nonlocal fdate1, tdate1


        nonlocal s_list
        nonlocal s_list_list

        return {"s-list": s_list_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 109)).first()

    if htparam:
        w_int = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 123)).first()

    if htparam:
        indv = htparam.finteger

    genstat_obj_list = []
    for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
             (Genstat.datum >= fdate1) & (Genstat.datum <= tdate1) & (Genstat.gastnr != w_int) & (Genstat.gastnr != indv) & (Genstat.gastnr > 0) & (Genstat.zipreis != 0) & (Genstat.resstatus != 8) & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.datum, to_int(Genstat.gastnr)).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        s_list = query(s_list_list, filters=(lambda s_list: s_list.gastnr == genstat.gastnr), first=True)

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.gastnr = guest.gastnr
            s_list.datum = to_string(get_year(genstat.datum) , "9999") +\
                    to_string(get_month(genstat.datum) , "99")
            s_list.name = trim(guest.name + " " + guest.anrede1)
            s_list.city = guest.wohnort
            s_list.lodging =  to_decimal(genstat.logis)
            s_list.zimmeranz = s_list.zimmeranz + 1

            if trim(guest.adresse1) != "" and trim(guest.adresse2) != "":
                s_list.address = trim(guest.adresse1 + " " + guest.adresse2)
        else:
            s_list.lodging =  to_decimal(s_list.lodging) + to_decimal(genstat.logis)
            s_list.zimmeranz = s_list.zimmeranz + 1

    return generate_output()