from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Htparam, Res_line, Reservation, Segment, Waehrung

def walkin_glistbl(pvilanguage:int, arrival_flag:bool, walkin_flag:bool, sameday_flag:bool, from_date:date, to_date:date, ci_date:date, walk_in:int, wi_grp:int):
    walkin_glist_list = []
    wi_int:int = 0
    long_digit:bool = False
    htparam = res_line = reservation = segment = waehrung = None

    cl_list = walkin_glist = None

    cl_list_list, Cl_list = create_model("Cl_list", {"segm":int, "bezeich":str, "zimmeranz":int, "pax":int})
    walkin_glist_list, Walkin_glist = create_model("Walkin_glist", {"datum":date, "zinr":str, "name":str, "rsv_name":str, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "segm":str, "zipreis":str, "curr":str, "rstatus":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal walkin_glist_list, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_list, walkin_glist_list
        return {"walkin-glist": walkin_glist_list}

    def create_list():

        nonlocal walkin_glist_list, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_list, walkin_glist_list

        datum:date = None
        t_anz:int = 0
        t_pax:int = 0
        tot_anz:int = 0
        tot_pax:int = 0
        gtot_pax:int = 0
        gtot_anz:int = 0
        gtot_smday_pax:int = 0
        gtot_smday_anz:int = 0
        walkin_glist_list.clear()
        cl_list_list.clear()
        for datum in range(from_date,to_date + 1) :
            t_anz = 0
            t_pax = 0

            if datum >= ci_date:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr == wi_int)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rstatus = "In_House"
                        walkin_glist.rec_id = res_line._recid

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz = t_anz + 1
                        t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segmentcode == walk_in or res_line.gastnr == wi_int and segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rstatus = "In_House"
                            walkin_glist.rec_id = res_line._recid

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag(datum)
            else:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == Res_line.abreise) &  (Res_line.ankunft == datum))) &  ((Res_line.gratis + Res_line.erwachs) > 0))).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if res_line.gastnr == wi_int:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

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
                                walkin_glist.rstatus = "In_House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                            ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == Res_line.abreise) &  (Res_line.ankunft == datum))) &  ((Res_line.gratis + Res_line.erwachs) > 0))).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segmentcode == walk_in or res_line.gastnr == wi_int and segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

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
                                walkin_glist.rstatus = "In_House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag(datum)

        for walkin_glist in query(walkin_glist_list, filters=(lambda walkin_glist :re.match("Total",walkin_glist.name) or re.match("Total Same day Rsv",walkin_glist.name))):

            if re.match("Total",walkin_glist.name):
                gtot_pax = gtot_pax + walkin_glist.pax
                gtot_anz = gtot_anz + walkin_glist.zimmeranz

            elif re.match("Total Same day Rsv",walkin_glist.name):
                gtot_smday_pax = gtot_smday_pax + walkin_glist.pax
                gtot_smday_anz = gtot_smday_anz + walkin_glist.zimmeranz


        walkin_glist = Walkin_glist()
        walkin_glist_list.append(walkin_glist)

        walkin_glist.name = "Grand Total"
        walkin_glist.zimmeranz = gtot_anz
        walkin_glist.pax = gtot_pax

        if sameday_flag:
            walkin_glist = Walkin_glist()
            walkin_glist_list.append(walkin_glist)

            walkin_glist.name = "Grand Total Same Day Rsv"
            walkin_glist.zimmeranz = gtot_smday_anz
            walkin_glist.pax = gtot_smday_pax
        walkin_glist = Walkin_glist()
        walkin_glist_list.append(walkin_glist)

        walkin_glist.zinr = ""

    def create_list1():

        nonlocal walkin_glist_list, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_list, walkin_glist_list

        datum:date = None
        t_anz:int = 0
        t_pax:int = 0
        tot_anz:int = 0
        tot_pax:int = 0
        walkin_glist_list.clear()
        cl_list_list.clear()
        for datum in range(from_date,to_date + 1) :
            t_anz = 0
            t_pax = 0

            if datum >= ci_date:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr == wi_int) &  (Res_line.ankunft == datum)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.datum = datum
                        walkin_glist.zinr = res_line.zinr
                        walkin_glist.name = res_line.name
                        walkin_glist.rsv_name = reservation.name
                        walkin_glist.zimmeranz = res_line.zimmeranz
                        walkin_glist.pax = res_line.erwachs + res_line.gratis
                        walkin_glist.ankunft = res_line.ankunft
                        walkin_glist.abreise = res_line.abreise
                        walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                        walkin_glist.rstatus = "In_House"
                        walkin_glist.rec_id = res_line._recid

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz = t_anz + 1
                        t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft == datum)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segmentcode == walk_in or res_line.gastnr == wi_int and segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

                            walkin_glist.datum = datum
                            walkin_glist.zinr = res_line.zinr
                            walkin_glist.name = res_line.name
                            walkin_glist.rsv_name = reservation.name
                            walkin_glist.zimmeranz = res_line.zimmeranz
                            walkin_glist.pax = res_line.erwachs + res_line.gratis
                            walkin_glist.ankunft = res_line.ankunft
                            walkin_glist.abreise = res_line.abreise
                            walkin_glist.segm = entry(0, segment.bezeich, "$$0")
                            walkin_glist.rstatus = "In_House"
                            walkin_glist.rec_id = res_line._recid

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag_show_arr(datum)
            else:

                if not walkin_flag:

                    for res_line in db_session.query(Res_line).filter(
                            (((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == Res_line.abreise) &  (Res_line.ankunft == datum))) &  ((Res_line.gratis + Res_line.erwachs) > 0))) &  (Res_line.ankunft == datum)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if res_line.gastnr == wi_int:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

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
                                walkin_glist.rstatus = "In_House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""
                else:

                    for res_line in db_session.query(Res_line).filter(
                            (((Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == Res_line.abreise) &  (Res_line.ankunft == datum))) &  ((Res_line.gratis + Res_line.erwachs) > 0))) &  (Res_line.ankunft == datum)).all():

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segmentcode == walk_in or res_line.gastnr == wi_int and segmentgrup != 0:
                            walkin_glist = Walkin_glist()
                            walkin_glist_list.append(walkin_glist)

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
                                walkin_glist.rstatus = "In_House"
                            else:
                                walkin_glist.rstatus = "Departed"

                            if long_digit:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                            else:
                                walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                            waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                            if waehrung:
                                walkin_glist.curr = waehrung.wabkurz
                            t_anz = t_anz + 1
                            t_pax = t_pax + res_line.erwachs + res_line.gratis

                    if t_anz != 0:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.name = "Total"
                        walkin_glist.zimmeranz = t_anz
                        walkin_glist.pax = t_pax
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

                        walkin_glist.zinr = ""

                if sameday_flag:
                    proc_sameday_flag_show_arr(datum)

    def proc_sameday_flag(datum:date):

        nonlocal walkin_glist_list, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_list, walkin_glist_list

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
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr != wi_int) &  (Res_line.ankunft == datum)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                a = res_line._recid

                walkin_glist = query(walkin_glist_list, filters=(lambda walkin_glist :walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

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
                            walkin_glist.rstatus = "In_House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis

        else:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr != wi_int) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                a = res_line._recid

                walkin_glist = query(walkin_glist_list, filters=(lambda walkin_glist :walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

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
                            walkin_glist.rstatus = "In_House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis


        if t_anz_sameday != 0:
            walkin_glist = Walkin_glist()
            walkin_glist_list.append(walkin_glist)

            walkin_glist.name = "Total Same day Rsv"
            walkin_glist.zimmeranz = t_anz_sameday
            walkin_glist.pax = t_pax_sameday
            walkin_glist = Walkin_glist()
            walkin_glist_list.append(walkin_glist)

            walkin_glist.zinr = ""

    def proc_sameday_flag_show_arr(datum:date):

        nonlocal walkin_glist_list, wi_int, long_digit, htparam, res_line, reservation, segment, waehrung


        nonlocal cl_list, walkin_glist
        nonlocal cl_list_list, walkin_glist_list

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
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr != wi_int) &  (Res_line.ankunft == datum)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                a = res_line._recid

                walkin_glist = query(walkin_glist_list, filters=(lambda walkin_glist :walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

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
                            walkin_glist.rstatus = "In_House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis

        else:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.gastnr != wi_int) &  (Res_line.ankunft == datum)).all():

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                a = res_line._recid

                walkin_glist = query(walkin_glist_list, filters=(lambda walkin_glist :walkin_glist.rec_id == a), first=True)

                if not walkin_glist:
                    create_date = reservation.resdat

                    if create_date == res_line.ankunft:
                        walkin_glist = Walkin_glist()
                        walkin_glist_list.append(walkin_glist)

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
                            walkin_glist.rstatus = "In_House"
                        else:
                            walkin_glist.rstatus = "Departed"

                        if long_digit:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">,>>>,>>>,>>9")
                        else:
                            walkin_glist.zipreis = to_string(res_line.zipreis, ">>,>>>,>>9.99")

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            walkin_glist.curr = waehrung.wabkurz
                        t_anz_sameday = t_anz_sameday + 1
                        t_pax_sameday = t_pax_sameday + res_line.erwachs + res_line.gratis


        if t_anz_sameday != 0:
            walkin_glist = Walkin_glist()
            walkin_glist_list.append(walkin_glist)

            walkin_glist.name = "Total Same day Rsv"
            walkin_glist.zimmeranz = t_anz_sameday
            walkin_glist.pax = t_pax_sameday
            walkin_glist = Walkin_glist()
            walkin_glist_list.append(walkin_glist)

            walkin_glist.zinr = ""


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 109) &  (Htparam.paramgruppe == 7)).first()
    wi_int = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if not arrival_flag:
        create_list()
    else:
        create_list1()

    return generate_output()