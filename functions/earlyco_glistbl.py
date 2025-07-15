#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Reservation, Res_line, Guest, Waehrung

def earlyco_glistbl(from_date:date, to_date:date):

    prepare_cache ([Htparam, Reservation, Res_line, Guest, Waehrung])

    earlycog_list_data = []
    datum:date = None
    t_anz:int = 0
    t_pax:int = 0
    tot_anz:int = 0
    tot_pax:int = 0
    n:int = 0
    st:string = ""
    long_digit:bool = False
    htparam = reservation = res_line = guest = waehrung = None

    earlycog_list = cl_list = None

    earlycog_list_data, Earlycog_list = create_model("Earlycog_list", {"datum":date, "zinr":string, "resname":string, "name":string, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "origdate":date, "zipreis":string, "curr":string, "reason":string, "country":string, "sex":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"bezeich":string, "zimmeranz":int, "pax":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal earlycog_list_data, datum, t_anz, t_pax, tot_anz, tot_pax, n, st, long_digit, htparam, reservation, res_line, guest, waehrung
        nonlocal from_date, to_date


        nonlocal earlycog_list, cl_list
        nonlocal earlycog_list_data, cl_list_data

        return {"earlycog-list": earlycog_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    earlycog_list_data.clear()
    cl_list_data.clear()
    for datum in date_range(from_date,to_date) :
        t_anz = 0
        t_pax = 0

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.gastnrmember, res_line.zinr, res_line.name, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.ankunft, res_line.abreise, res_line.anztage, res_line.zimmer_wunsch, res_line.zipreis, res_line.betriebsnr, res_line._recid, reservation.name, reservation._recid in db_session.query(Res_line.gastnrmember, Res_line.zinr, Res_line.name, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.ankunft, Res_line.abreise, Res_line.anztage, Res_line.zimmer_wunsch, Res_line.zipreis, Res_line.betriebsnr, Res_line._recid, Reservation.name, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise >= datum) & (Res_line.abreise <= datum) & ((Res_line.abreise - Res_line.ankunft) < Res_line.anztage)).order_by(Res_line.abreise, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            earlycog_list = Earlycog_list()
            earlycog_list_data.append(earlycog_list)

            earlycog_list.datum = datum
            earlycog_list.zinr = res_line.zinr
            earlycog_list.name = res_line.name
            earlycog_list.resname = reservation.name
            earlycog_list.zimmeranz = res_line.zimmeranz
            earlycog_list.pax = res_line.erwachs + res_line.gratis
            earlycog_list.ankunft = res_line.ankunft
            earlycog_list.abreise = res_line.abreise
            earlycog_list.origdate = res_line.ankunft + timedelta(days=res_line.anztage)

            if guest:
                earlycog_list.sex = guest.geschlecht
                earlycog_list.country = guest.land

            if matches(res_line.zimmer_wunsch,r"*earlyCO*"):
                for n in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    st = entry(n - 1, res_line.zimmer_wunsch, ";")

                    if substring(st, 0, 8) == ("earlyCO,").lower() :
                        earlycog_list.reason = earlycog_list.reason + substring(st, 8) + ";"

            if long_digit:
                earlycog_list.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
            else:
                earlycog_list.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                earlycog_list.curr = waehrung.wabkurz
            t_anz = t_anz + 1
            t_pax = t_pax + res_line.erwachs + res_line.gratis

        if t_anz != 0:
            earlycog_list = Earlycog_list()
            earlycog_list_data.append(earlycog_list)

            earlycog_list.name = "T O T A L"
            earlycog_list.zimmeranz = t_anz
            earlycog_list.pax = t_pax

    return generate_output()