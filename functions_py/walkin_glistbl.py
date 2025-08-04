#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# gitlab: 811
# UI baru, payload: ci-date sblmnya blm ada.
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Reservation, Segment, Waehrung

def walkin_glistbl(pvilanguage:int, arrival_flag:bool, walkin_flag:bool, sameday_flag:bool, from_date:date, to_date:date, ci_date:date, walk_in:int, wi_grp:int):

    prepare_cache ([Htparam, Res_line, Reservation, Segment, Waehrung])

    walkin_glist_data = []
    wi_int:int = 0
    long_digit:bool = False
    htparam = res_line = reservation = segment = waehrung = None

    cl_list = walkin_glist = None

    cl_list_data, Cl_list = create_model("Cl_list", {"segm":int, "bezeich":string, "zimmeranz":int, "pax":int})
    walkin_glist_data, Walkin_glist = create_model("Walkin_glist", {"datum":date, "zinr":string, "name":string, "rsv_name":string, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "segm":string, "zipreis":string, "curr":string, "rstatus":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal walkin_glist_data, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung
        nonlocal pvilanguage, arrival_flag, walkin_flag, sameday_flag, from_date, to_date, ci_date, walk_in, wi_grp


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_data, walkin_glist_data

        return {"walkin-glist": walkin_glist_data}

    def create_list():

        nonlocal walkin_glist_data, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung
        nonlocal pvilanguage, arrival_flag, walkin_flag, sameday_flag, from_date, to_date, ci_date, walk_in, wi_grp


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_data, walkin_glist_data

        datum:date = None
        t_anz:int = 0
        t_pax:int = 0
        tot_anz:int = 0
        tot_pax:int = 0
        gtot_pax:int = 0
        gtot_anz:int = 0
        gtot_smday_pax:int = 0
        gtot_smday_anz:int = 0
        walkin_glist_data.clear()
        cl_list_data.clear()
        for datum in date_range(from_date,to_date) :
            t_anz = 0
            t_pax = 0

            if datum >= ci_date:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr == wi_int)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rstatus = "In-House"
                        walkin_glist.rec_id = res_line._recid

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz = t_anz + 1
                        t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment.segmentcode == walk_in or res_line.gastnr == wi_int and segment.segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rstatus = "In-House"
                            walkin_glist.rec_id = res_line._recid

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag(datum)
            else:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == Res_line.abreise) & (Res_line.ankunft == datum))) & ((Res_line.gratis + Res_line.erwachs) > 0))).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if res_line.gastnr == wi_int:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rec_id = res_line._recid

                            if res_line.active_flag == 1:
                                walkin_glist.rstatus = "In-House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == Res_line.abreise) & (Res_line.ankunft == datum))) & ((Res_line.gratis + Res_line.erwachs) > 0))).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment.segmentcode == walk_in or res_line.gastnr == wi_int and segment.segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rec_id = res_line._recid

                            if res_line.active_flag == 1:
                                walkin_glist.rstatus = "In-House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag(datum)

        for walkin_glist in query(walkin_glist_data, filters=(lambda walkin_glist: matches(walkin_glist.name,r"Total") or matches(walkin_glist.name,r"Total Same day Rsv"))):

            if matches(walkin_glist.name,r"Total"):
                gtot_pax = gtot_pax + walkin_glist.pax
                gtot_anz = gtot_anz + walkin_glist.zimmeranz

            elif matches(walkin_glist.name,r"Total Same day Rsv"):
                gtot_smday_pax = gtot_smday_pax + walkin_glist.pax
                gtot_smday_anz = gtot_smday_anz + walkin_glist.zimmeranz


        walkin_glist = Walkin_glist()
        walkin_glist_data.append(walkin_glist)

        walkin_glist.name = "Grand Total"
        walkin_glist.zimmeranz = gtot_anz
        walkin_glist.pax = gtot_pax

        if sameday_flag:
            walkin_glist = Walkin_glist()
            walkin_glist_data.append(walkin_glist)

            walkin_glist.name = "Grand Total Same Day Rsv"
            walkin_glist.zimmeranz = gtot_smday_anz
            walkin_glist.pax = gtot_smday_pax
        walkin_glist = Walkin_glist()
        walkin_glist_data.append(walkin_glist)

        walkin_glist.zinr = ""


    def create_list1():

        nonlocal walkin_glist_data, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung
        nonlocal pvilanguage, arrival_flag, walkin_flag, sameday_flag, from_date, to_date, ci_date, walk_in, wi_grp


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_data, walkin_glist_data

        datum:date = None
        t_anz:int = 0
        t_pax:int = 0
        tot_anz:int = 0
        tot_pax:int = 0
        walkin_glist_data.clear()
        cl_list_data.clear()
        for datum in date_range(from_date,to_date) :
            t_anz = 0
            t_pax = 0

            if datum >= ci_date:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr == wi_int) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rstatus = "In-House"
                        walkin_glist.rec_id = res_line._recid

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz = t_anz + 1
                        t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment.segmentcode == walk_in or res_line.gastnr == wi_int and segment.segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rstatus = "In-House"
                            walkin_glist.rec_id = res_line._recid

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag_show_arr(datum)
            else:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                             (((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == Res_line.abreise) & (Res_line.ankunft == datum))) & ((Res_line.gratis + Res_line.erwachs) > 0))) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if res_line.gastnr == wi_int:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rec_id = res_line._recid

                            if res_line.active_flag == 1:
                                walkin_glist.rstatus = "In-House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                             (((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == Res_line.abreise) & (Res_line.ankunft == datum))) & ((Res_line.gratis + Res_line.erwachs) > 0))) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment.segmentcode == walk_in or res_line.gastnr == wi_int and segment.segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_data.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rec_id = res_line._recid

                            if res_line.active_flag == 1:
                                walkin_glist.rstatus = "In-House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag_show_arr(datum)


    def proc_sameday_flag(datum:date):

        nonlocal walkin_glist_data, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung
        nonlocal pvilanguage, arrival_flag, walkin_flag, sameday_flag, from_date, to_date, ci_date, walk_in, wi_grp


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_data, walkin_glist_data

        t_anz_sameday:int = 0
        t_pax_sameday:int = 0
        tot_anz_sameday:int = 0
        tot_pax_sameday:int = 0
        create_date:date = None
        a:int = 0
        t_anz_sameday = 0
        t_pax_sameday = 0

        if datum > ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr != wi_int) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                a = res_line._recid

                walkin_glist = query(walkin_glist_data, filters=(lambda walkin_glist: walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = from_date
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rec_id = res_line._recid

                        if res_line.active_flag == 1:
                            walkin_glist.rstatus = "In-House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis

        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr != wi_int) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum)).order_by(Res_line.zinr).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                a = res_line._recid

                walkin_glist = query(walkin_glist_data, filters=(lambda walkin_glist: walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rec_id = res_line._recid

                        if res_line.active_flag == 1:
                            walkin_glist.rstatus = "In-House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis


        if t_anz_sameday != 0:
            walkin_glist = Walkin_glist()
            walkin_glist_data.append(walkin_glist)

            walkin_glist.name = "Total Same day Rsv"
            walkin_glist.zimmeranz = t_anz_sameday
            walkin_glist.pax = t_pax_sameday
            walkin_glist = Walkin_glist()
            walkin_glist_data.append(walkin_glist)

            walkin_glist.zinr = ""


    def proc_sameday_flag_show_arr(datum:date):

        nonlocal walkin_glist_data, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung
        nonlocal pvilanguage, arrival_flag, walkin_flag, sameday_flag, from_date, to_date, ci_date, walk_in, wi_grp


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_data, walkin_glist_data

        t_anz_sameday:int = 0
        t_pax_sameday:int = 0
        tot_anz_sameday:int = 0
        tot_pax_sameday:int = 0
        create_date:date = None
        a:int = 0
        t_anz_sameday = 0
        t_pax_sameday = 0

        if datum > ci_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr != wi_int) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                a = res_line._recid

                walkin_glist = query(walkin_glist_data, filters=(lambda walkin_glist: walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = from_date
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rec_id = res_line._recid

                        if res_line.active_flag == 1:
                            walkin_glist.rstatus = "In-House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis

        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.gastnr != wi_int) & (Res_line.ankunft == datum)).order_by(Res_line.zinr).all():

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                a = res_line._recid

                walkin_glist = query(walkin_glist_data, filters=(lambda walkin_glist: walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_data.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rec_id = res_line._recid

                        if res_line.active_flag == 1:
                            walkin_glist.rstatus = "In-House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis


        if t_anz_sameday != 0:
            walkin_glist = Walkin_glist()
            walkin_glist_data.append(walkin_glist)

            walkin_glist.name = "Total Same day Rsv"
            walkin_glist.zimmeranz = t_anz_sameday
            walkin_glist.pax = t_pax_sameday
            walkin_glist = Walkin_glist()
            walkin_glist_data.append(walkin_glist)

            walkin_glist.zinr = ""

    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)],"paramgruppe": [(eq, 7)]})
    wi_int = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if not arrival_flag:
        create_list()
    else:
        create_list1()

    return generate_output()