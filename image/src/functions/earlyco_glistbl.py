from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Htparam, Reservation, Res_line, Guest, Waehrung

def earlyco_glistbl(from_date:date, to_date:date):
    earlycog_list_list = []
    datum:date = None
    t_anz:int = 0
    t_pax:int = 0
    tot_anz:int = 0
    tot_pax:int = 0
    n:int = 0
    st:str = ""
    long_digit:bool = False
    htparam = reservation = res_line = guest = waehrung = None

    earlycog_list = cl_list = None

    earlycog_list_list, Earlycog_list = create_model("Earlycog_list", {"datum":date, "zinr":str, "resname":str, "name":str, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "origdate":date, "zipreis":str, "curr":str, "reason":str, "country":str, "sex":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"bezeich":str, "zimmeranz":int, "pax":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal earlycog_list_list, datum, t_anz, t_pax, tot_anz, tot_pax, n, st, long_digit, htparam, reservation, res_line, guest, waehrung


        nonlocal earlycog_list, cl_list
        nonlocal earlycog_list_list, cl_list_list
        return {"earlycog-list": earlycog_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    earlycog_list_list.clear()
    cl_list_list.clear()
    for datum in range(from_date,to_date + 1) :
        t_anz = 0
        t_pax = 0

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise >= datum) &  (Res_line.abreise <= datum) &  ((Res_line.abreise - Res_line.ankunft) < Res_line.anztage)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()
            earlycog_list = Earlycog_list()
            earlycog_list_list.append(earlycog_list)

            earlycog_list.datum = datum
            earlycog_list.zinr = res_line.zinr
            earlycog_list.name = res_line.name
            earlycog_list.resname = reservation.name
            earlycog_list.zimmeranz = res_line.zimmeranz
            earlycog_list.pax = res_line.erwachs + res_line.gratis
            earlycog_list.ankunft = res_line.ankunft
            earlycog_list.abreise = res_line.abreise
            earlycog_list.origdate = res_line.ankunft + res_line.anztage

            if guest:
                earlycog_list.sex = guest.geschlecht
                earlycog_list.country = guest.land

            if re.match(".*earlyCO.*",res_line.zimmer_wunsch):
                for n in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    st = entry(n - 1, res_line.zimmer_wunsch, ";")

                    if substring(st, 0, 8) == "earlyCO,":
                        earlycog_list.reason = earlycog_list.reason + substring(st, 8) + ";"

            if long_digit:
                earlycog_list.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
            else:
                earlycog_list.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

            waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                earlycog_list.curr = waehrung.wabkurz
            t_anz = t_anz + 1
            t_pax = t_pax + res_line.erwachs + res_line.gratis

        if t_anz != 0:
            earlycog_list = Earlycog_list()
            earlycog_list_list.append(earlycog_list)

            earlycog_list.name = "T O T A L"
            earlycog_list.zimmeranz = t_anz
            earlycog_list.pax = t_pax

    return generate_output()