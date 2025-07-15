#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Waehrung, Reservation, Zimkateg, Res_line, Zkstat, Reslin_queasy, Messages

def telop_webbl(sorttype:int, room:string, fdate1:date, fdate2:date, ci_date:date, lname:string, last_sort:int, lnat:string, lresnr:int):

    prepare_cache ([Guest, Waehrung, Reservation, Zimkateg, Res_line, Reslin_queasy])

    troom = ""
    tpax = ""
    telop_list_data = []
    rmlen:int = 0
    temp_total:int = 0
    temp_total2:int = 0
    guest = waehrung = reservation = zimkateg = res_line = zkstat = reslin_queasy = messages = None

    gmember = telop_list = None

    telop_list_data, Telop_list = create_model("Telop_list", {"resli_wabkurz":string, "voucher_nr":string, "grpflag":bool, "reser_name":string, "zinr":string, "resli_name":string, "segmentcode":int, "nation1":string, "resstatus":int, "l_zuordnung":int, "ankunft":date, "abreise":date, "ankzeit":int, "abreisezeit":int, "flight_nr":string, "zimmeranz":int, "kurzbez":string, "erwachs":int, "kind1":int, "gratis":int, "waeh_wabkurz":string, "resnr":int, "reslinnr":int, "betrieb_gast":int, "groupname":string, "cancelled_id":string, "changed_id":string, "bemerk":string, "active_flag":int, "gastnrmember":int, "gastnr":int, "betrieb_gastmem":int, "pseudofix":bool, "zikatnr":int, "arrangement":string, "zipreis":Decimal, "resname":string, "address":string, "city":string, "b_comments":string, "message_flag":bool, "flag_color":int, "flight1":string, "eta":string, "flight2":string, "etd":string})

    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        return {"troom": troom, "tpax": tpax, "telop-list": telop_list_data}

    def disp_arl1():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rmlen = length(room)

        if fdate1 == None:

            if fdate2 != None:
                fdate1 = fdate2
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if fdate2 == None:

            if fdate1 != None:
                fdate2 = fdate1
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (matches(Res_line.name,(lname)))).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2)).order_by(Reservation.name, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower()) & (Reservation.name <= (to_name).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2)).order_by(Reservation.name, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (matches(Res_line.resname,(lname)))).order_by(Res_line.resname, Res_line.ankunft, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower())).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2) & (matches(Res_line.name,(lname)))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower())).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == fdate2) & (matches(Res_line.name,(lname)))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


            else:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 0) & (Res_line.resnr == lresnr)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


    def disp_arl2():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.name,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    if ci_date != None:

                        res_line_obj_list = {}
                        res_line = Res_line()
                        waehrung = Waehrung()
                        reservation = Reservation()
                        zimkateg = Zimkateg()
                        gmember = Guest()
                        for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            assign_it()

                            if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                                temp_total2 = temp_total2 + res_line.zimmeranz
                            temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                        troom = to_string(temp_total2)
                        tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.name,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, Res_line.resname, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


            else:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resnr == lresnr)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


    def disp_arl4():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "" and room == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date)).order_by(Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.name, Res_line.zinr).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "":

                if room == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif room != "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.resname,(lname))) & (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.abreise == ci_date)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


            else:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resnr == lresnr) & (Res_line.abreise == ci_date)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


    def disp_arl5():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = "zzz"
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if fdate2 == None:
            fdate2 = ci_date

        if last_sort == 1 and room != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.name,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 1 and room == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.name,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 2 and room != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 2 and room == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Res_line.resname, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower()) & (Reservation.name <= (to_name).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Reservation.name, Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.resstatus == 8) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         (Res_line.resstatus == 8) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise >= fdate1) & (Res_line.abreise <= fdate2)).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


            else:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.resnr == lresnr)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


    def disp_arl6():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.name,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.name,(lname))) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.name,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (matches(Res_line.name,(lname))) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (matches(Res_line.name,(lname))) & (Res_line.abreise == ci_date))).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    res_line = Res_line()
                    waehrung = Waehrung()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    gmember = Guest()
                    for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                             ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                        if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + res_line.zimmeranz
                        temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                    troom = to_string(temp_total2)
                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Res_line.resname,(lname))) & (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise == ci_date))).order_by(Res_line.resname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (matches(Res_line.resname,(lname))) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (matches(Res_line.resname,(lname))) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember) & (Gmember.nation1 == (lnat).lower())).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)) | ((Res_line.active_flag == 0) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.resname >= (lname).lower()) & (Res_line.resname <= (to_name).lower()) & (Res_line.abreise == ci_date))).order_by(Gmember.nation1, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 0) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))).order_by(Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


            else:

                res_line_obj_list = {}
                res_line = Res_line()
                waehrung = Waehrung()
                reservation = Reservation()
                zimkateg = Zimkateg()
                gmember = Guest()
                for res_line.resstatus, res_line.l_zuordnung, res_line.zimmeranz, res_line.erwachs, res_line.wabkurz, res_line.voucher_nr, res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.abreisezeit, res_line.flight_nr, res_line.kind1, res_line.gratis, res_line.resnr, res_line.reslinnr, res_line.betrieb_gast, res_line.cancelled_id, res_line.changed_id, res_line.bemerk, res_line.active_flag, res_line.gastnrmember, res_line.gastnr, res_line.betrieb_gastmem, res_line.pseudofix, res_line.zikatnr, res_line.arrangement, res_line.zipreis, res_line._recid, waehrung.wabkurz, waehrung._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zimkateg.kurzbez, zimkateg._recid, gmember.adresse1, gmember.wohnort, gmember.plz, gmember._recid, gmember.nation1 in db_session.query(Res_line.resstatus, Res_line.l_zuordnung, Res_line.zimmeranz, Res_line.erwachs, Res_line.wabkurz, Res_line.voucher_nr, Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.abreisezeit, Res_line.flight_nr, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.reslinnr, Res_line.betrieb_gast, Res_line.cancelled_id, Res_line.changed_id, Res_line.bemerk, Res_line.active_flag, Res_line.gastnrmember, Res_line.gastnr, Res_line.betrieb_gastmem, Res_line.pseudofix, Res_line.zikatnr, Res_line.arrangement, Res_line.zipreis, Res_line._recid, Waehrung.wabkurz, Waehrung._recid, Reservation.gastnr, Reservation.grpflag, Reservation.name, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Gmember.adresse1, Gmember.wohnort, Gmember.plz, Gmember._recid, Gmember.nation1).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                         ((Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resnr == lresnr)) | ((Res_line.active_flag == 0) & (Res_line.resnr == lresnr) & (Res_line.ankunft == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.resnr == lresnr) & (Res_line.abreise == ci_date))).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

                    if res_line.resstatus != 13 and res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + res_line.zimmeranz
                    temp_total = to_int(temp_total) + to_int(res_line.erwachs)


                troom = to_string(temp_total2)
                tpax = to_string(temp_total)


    def count_al1():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rline = None
        whrg = None
        reservation = None
        gme = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if fdate1 == None:

            if fdate2 != None:
                fdate1 = fdate2
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if fdate2 == None:

            if fdate1 != None:
                fdate2 = fdate1
            else:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=30)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower())).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2) & (matches(Rline.name,(lname)))).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2)).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower())).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft >= fdate1) & (Rline.ankunft <= fdate2) & (matches(Rline.resname,(lname)))).order_by(Rline.resname, Rline.ankunft, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower())).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2) & (matches(Rline.name,(lname)))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower())).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == fdate2) & (matches(Rline.name,(lname)))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.ankunft == ci_date)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 0) & (Rline.resnr == lresnr)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


    def count_all2():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rline = None
        whrg = None
        reservation = None
        gme = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.name,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    if ci_date != None:

                        rline_obj_list = {}
                        for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                                 (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                            if rline_obj_list.get(rline._recid):
                                continue
                            else:
                                rline_obj_list[rline._recid] = True

                            if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                                temp_total2 = temp_total2 + rline.zimmeranz
                            temp_total = to_int(temp_total) + to_int(rline.erwachs)
                        troom = to_string(temp_total2)


                        tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.name,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.zinr, Rline.resname, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resnr == lresnr)).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


    def count_all4():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rline = None
        whrg = None
        reservation = None
        gme = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "" and room == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date)).order_by(Rline.name, Rline.zinr).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date)).order_by(Rline.name, Rline.zinr).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "":

                if room == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif room != "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date)).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.resname,(lname))) & (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == ci_date)).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.abreise == ci_date)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resnr == lresnr) & (Rline.abreise == ci_date)).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


    def count_all5():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rline = None
        whrg = None
        reservation = None
        gme = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zimkateg)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1 and room != "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (matches(Rline.name,(lname))) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 1 and room == "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (matches(Rline.name,(lname))) & (Rline.abreise == fdate2)).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == fdate2)).order_by(Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 2 and room != "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.zinr, Reserv.name, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.zinr, Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == fdate2) & (Rline.zinr >= (room).lower())).order_by(Rline.zinr, Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 2 and room == "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by(Reserv.name, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == fdate2)).order_by(Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr) & (Reserv.name >= (lname).lower()) & (Reserv.name <= (to_name).lower())).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by(Rline.resname, Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.resstatus == 8) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         (Rline.resstatus == 8) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == fdate2)).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == fdate2)).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = {}
                rline = Res_line()
                whrg = Waehrung()
                reservation = Reservation()
                zkstat = Zimkateg()
                gme = Guest()
                for rline.resstatus, rline.l_zuordnung, rline.zimmeranz, rline.erwachs, rline.wabkurz, rline.voucher_nr, rline.zinr, rline.name, rline.ankunft, rline.abreise, rline.ankzeit, rline.abreisezeit, rline.flight_nr, rline.kind1, rline.gratis, rline.resnr, rline.reslinnr, rline.betrieb_gast, rline.cancelled_id, rline.changed_id, rline.bemerk, rline.active_flag, rline.gastnrmember, rline.gastnr, rline.betrieb_gastmem, rline.pseudofix, rline.zikatnr, rline.arrangement, rline.zipreis, rline._recid, whrg.wabkurz, whrg._recid, reservation.gastnr, reservation.grpflag, reservation.name, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation._recid, zkstat.kurzbez, zkstat._recid, gme.adresse1, gme.wohnort, gme.plz, gme._recid, gme.nation1 in db_session.query(Rline.resstatus, Rline.l_zuordnung, Rline.zimmeranz, Rline.erwachs, Rline.wabkurz, Rline.voucher_nr, Rline.zinr, Rline.name, Rline.ankunft, Rline.abreise, Rline.ankzeit, Rline.abreisezeit, Rline.flight_nr, Rline.kind1, Rline.gratis, Rline.resnr, Rline.reslinnr, Rline.betrieb_gast, Rline.cancelled_id, Rline.changed_id, Rline.bemerk, Rline.active_flag, Rline.gastnrmember, Rline.gastnr, Rline.betrieb_gastmem, Rline.pseudofix, Rline.zikatnr, Rline.arrangement, Rline.zipreis, Rline._recid, Whrg.wabkurz, Whrg._recid, Reserv.gastnr, Reserv.grpflag, Reserv.name, Reserv.segmentcode, Reserv.groupname, Reserv.bemerk, Reserv._recid, Zk.kurzbez, Zk._recid, Gme.adresse1, Gme.wohnort, Gme.plz, Gme._recid, Gme.nation1).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         (Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.resnr == lresnr)).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


    def count_all6():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        to_name:string = ""
        rline = None
        whrg = None
        reservation = None
        gme = None
        zkstat = None
        Rline =  create_buffer("Rline",Res_line)
        Whrg =  create_buffer("Whrg",Waehrung)
        Reserv =  create_buffer("Reserv",Reservation)
        Gme =  create_buffer("Gme",Guest)
        Zk =  create_buffer("Zk",Zkstat)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if last_sort == 1:

            if room != "":

                if lname == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.name,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.name,(lname))) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

            elif room == "":

                if lname == "":

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == ci_date))).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.name,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (matches(Rline.name,(lname))) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (matches(Rline.name,(lname))) & (Rline.abreise == ci_date))).order_by(Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    rline_obj_list = {}
                    for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                             ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.name >= (lname).lower()) & (Rline.name <= (to_name).lower()) & (Rline.abreise == ci_date))).order_by(Rline.name).all():
                        if rline_obj_list.get(rline._recid):
                            continue
                        else:
                            rline_obj_list[rline._recid] = True

                        if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                            temp_total2 = temp_total2 + rline.zimmeranz
                        temp_total = to_int(temp_total) + to_int(rline.erwachs)
                    troom = to_string(temp_total2)


                    tpax = to_string(temp_total)

        elif last_sort == 2:

            if lname == "" and room == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.resnr, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname == "" and room != "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.abreise == ci_date))).order_by(Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.resname,(lname))) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (matches(Rline.resname,(lname))) & (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & ((substring(Rline.zinr, 0, to_int(rmlen))) >= (room).lower()) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == ci_date))).order_by(Rline.resname, Rline.zinr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat == "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (matches(Rline.resname,(lname))) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 3 and lnat != "":

            if lname == "":

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (matches(Rline.resname,(lname))) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (matches(Rline.resname,(lname))) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (matches(Rline.resname,(lname))) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember) & (Gme.nation1 == (lnat).lower())).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft <= ci_date) & (Rline.abreise >= ci_date)) | ((Rline.active_flag == 0) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.resname >= (lname).lower()) & (Rline.resname <= (to_name).lower()) & (Rline.abreise == ci_date))).order_by(Gme.nation1, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)

        elif last_sort == 4:

            if lresnr == 0:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12)) | ((Rline.active_flag == 0) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.abreise == ci_date))).order_by(Rline.resnr, (Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


            else:

                rline_obj_list = {}
                for rline, whrg, reservation, zkstat, gme in db_session.query(Rline, Whrg, Reserv, Zk, Gme).join(Whrg,(Whrg.waehrungsnr == Rline.betriebsnr)).join(Reserv,(Reserv.resnr == Rline.resnr)).join(Zk,(Zk.zikatnr == Rline.zikatnr)).join(Gme,(Gme.gastnr == Rline.gastnrmember)).filter(
                         ((Rline.active_flag == 1) & (Rline.resstatus != 12) & (Rline.resnr == lresnr)) | ((Rline.active_flag == 0) & (Rline.resnr == lresnr) & (Rline.ankunft == ci_date)) | ((Rline.active_flag == 2) & (Rline.resstatus == 8) & (Rline.resnr == lresnr) & (Rline.abreise == ci_date))).order_by((Rline.kontakt_nr * Rline.resnr), Rline.resstatus, Rline.name).all():
                    if rline_obj_list.get(rline._recid):
                        continue
                    else:
                        rline_obj_list[rline._recid] = True

                    if rline.resstatus != 13 and rline.resstatus != 11 and rline.l_zuordnung[2] != 1:
                        temp_total2 = temp_total2 + rline.zimmeranz
                    temp_total = to_int(temp_total) + to_int(rline.erwachs)
                troom = to_string(temp_total2)


                tpax = to_string(temp_total)


    def assign_it():

        nonlocal troom, tpax, telop_list_data, rmlen, temp_total, temp_total2, guest, waehrung, reservation, zimkateg, res_line, zkstat, reslin_queasy, messages
        nonlocal sorttype, room, fdate1, fdate2, ci_date, lname, last_sort, lnat, lresnr
        nonlocal gmember


        nonlocal gmember, telop_list
        nonlocal telop_list_data

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
        telop_list = Telop_list()
        telop_list_data.append(telop_list)

        telop_list.resli_wabkurz = res_line.wabkurz
        telop_list.voucher_nr = res_line.voucher_nr
        telop_list.grpflag = reservation.grpflag
        telop_list.reser_name = reservation.name
        telop_list.zinr = res_line.zinr
        telop_list.resli_name = res_line.name
        telop_list.segmentcode = reservation.segmentcode
        telop_list.nation1 = gmember.nation1
        telop_list.resstatus = res_line.resstatus
        telop_list.l_zuordnung = res_line.l_zuordnung[2]
        telop_list.ankunft = res_line.ankunft
        telop_list.abreise = res_line.abreise
        telop_list.ankzeit = res_line.ankzeit
        telop_list.abreisezeit = res_line.abreisezeit
        telop_list.flight_nr = res_line.flight_nr
        telop_list.flight1 = substring(res_line.flight_nr, 0, 6)
        telop_list.eta = to_string(substring(res_line.flight_nr, 6, 5) , "99:99")
        telop_list.flight2 = substring(res_line.flight_nr, 11, 6)
        telop_list.etd = to_string(substring(res_line.flight_nr, 17, 5) , "99:99")
        telop_list.zimmeranz = res_line.zimmeranz
        telop_list.kurzbez = zimkateg.kurzbez
        telop_list.erwachs = res_line.erwachs
        telop_list.kind1 = res_line.kind1
        telop_list.gratis = res_line.gratis
        telop_list.waeh_wabkurz = waehrung.wabkurz
        telop_list.resnr = res_line.resnr
        telop_list.reslinnr = res_line.reslinnr
        telop_list.betrieb_gast = res_line.betrieb_gast
        telop_list.groupname = reservation.groupname
        telop_list.cancelled_id = res_line.cancelled_id
        telop_list.changed_id = res_line.changed_id
        telop_list.bemerk = res_line.bemerk
        telop_list.active_flag = res_line.active_flag
        telop_list.gastnrmember = res_line.gastnrmember
        telop_list.gastnr = res_line.gastnr
        telop_list.betrieb_gastmem = res_line.betrieb_gastmem
        telop_list.pseudofix = res_line.pseudofix
        telop_list.zikatnr = res_line.zikatnr
        telop_list.arrangement = res_line.arrangement
        telop_list.zipreis =  to_decimal(res_line.zipreis)
        telop_list.resname = reservation.name
        telop_list.address = guest.adresse1
        telop_list.city = guest.wohnort + " " + guest.plz
        telop_list.b_comments = reservation.bemerk

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"betriebsnr": [(eq, 0)]})

        if reslin_queasy:

            if (reslin_queasy.char1 != "" and reslin_queasy.deci1 == 0) or (reslin_queasy.char2 != "" and reslin_queasy.deci2 == 0) or (reslin_queasy.char3 != "" and reslin_queasy.deci3 == 0):
                telop_list.flag_color = 1


            else:
                telop_list.flag_color = 9

        messages = get_cache (Messages, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
        telop_list.message_flag = None != messages


    if sorttype == 1:
        disp_arl1()

    elif sorttype == 2:
        disp_arl2()

    elif sorttype == 4:
        disp_arl4()

    elif sorttype == 5:
        disp_arl5()

    elif sorttype == 6:
        disp_arl6()

    return generate_output()