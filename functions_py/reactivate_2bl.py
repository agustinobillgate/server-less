#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Reservation, Zimkateg, Res_line, Guest, Reslin_queasy

from functions import log_program

def reactivate_2bl(fresnr:int, fdate:date, fname:string, comments:string):

    prepare_cache ([Reservation, Zimkateg, Res_line, Guest])

    resname = ""
    address = ""
    city = ""
    stat_avail = False
    t_reactivate_data = []
    tname:string = ""
    loopi:int = 0
    str:string = ""
    reservation = zimkateg = res_line = guest = reslin_queasy = None

    t_reactivate = None

    t_reactivate_data, T_reactivate = create_model("T_reactivate", {"resnr":int, "reslinnr":int, "gastnr":int, "rsvname":string, "rsname":string, "ankunft":date, "abreise":date, "resstatus":int, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "arrangement":string, "zipreis":Decimal, "zinr":string, "cancelled":date, "cancelled_id":string, "bemerk":string, "bemerk1":string, "rsv_gastnr":int, "anztage":int, "active_flag":int, "activeflag":int, "betrieb_gastpay":int, "kind1":int, "kind2":int, "changed":date, "changed_id":string, "address":string, "city":string, "deposit":bool, "reactivated":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, stat_avail, t_reactivate_data, tname, loopi, str, reservation, zimkateg, res_line, guest, reslin_queasy
        nonlocal fresnr, fdate, fname, comments


        nonlocal t_reactivate
        nonlocal t_reactivate_data

        return {"comments": comments, "resname": resname, "address": address, "city": city, "stat_avail": stat_avail, "t-reactivate": t_reactivate_data}

    def create_t_reactive():

        nonlocal resname, address, city, stat_avail, t_reactivate_data, tname, loopi, str, reservation, zimkateg, res_line, guest, reslin_queasy
        nonlocal fresnr, fdate, fname, comments


        nonlocal t_reactivate
        nonlocal t_reactivate_data

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
        t_reactivate = T_reactivate()
        t_reactivate_data.append(t_reactivate)

        t_reactivate.resnr = res_line.resnr
        t_reactivate.reslinnr = res_line.reslinnr
        t_reactivate.rsvname = reservation.name
        t_reactivate.rsname = res_line.name
        t_reactivate.ankunft = res_line.ankunft
        t_reactivate.abreise = res_line.abreise
        t_reactivate.resstatus = res_line.resstatus
        t_reactivate.zimmeranz = res_line.zimmeranz
        t_reactivate.kurzbez = zimkateg.kurzbez
        t_reactivate.erwachs = res_line.erwachs
        t_reactivate.gratis = res_line.gratis
        t_reactivate.arrangement = res_line.arrangement
        t_reactivate.zipreis =  to_decimal(res_line.zipreis)
        t_reactivate.zinr = res_line.zinr
        t_reactivate.cancelled = res_line.cancelled
        t_reactivate.cancelled_id = res_line.cancelled_id
        t_reactivate.bemerk = res_line.bemerk
        t_reactivate.bemerk1 = reservation.bemerk
        t_reactivate.rsv_gastnr = reservation.gastnr
        t_reactivate.anztage = res_line.anztage
        t_reactivate.gastnr = res_line.gastnr
        t_reactivate.active_flag = res_line.active_flag
        t_reactivate.activeflag = reservation.activeflag
        t_reactivate.betrieb_gastpay = res_line.betrieb_gastpay
        t_reactivate.kind1 = res_line.kind1
        t_reactivate.kind2 = res_line.kind2
        t_reactivate.changed = res_line.changed
        t_reactivate.changed_id = res_line.changed_id
        t_reactivate.address = guest.adresse1


        t_reactivate.city = guest.wohnort + " " + guest.plz

        if reservation.depositgef != 0:
            t_reactivate.deposit = True
        else:
            t_reactivate.deposit = False

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.char3.collate("C").ilike("%RE-ACTIVATE RSV%"))).first()

        if reslin_queasy:
            t_reactivate.reactivated = True
        else:
            t_reactivate.reactivated = False

    stat_avail = False

    if fresnr == 0 and fdate == None:
        tname = chr_unicode(asc(substring(fname, 0, 1)) + 1)

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        zimkateg = Zimkateg()
        for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag == 2) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.resname >= (fname).lower()) & (Res_line.resname < (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            create_t_reactive()

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        zimkateg = Zimkateg()
        for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.zimmer_wunsch,"*cancel*")) & (Res_line.resname >= (fname).lower()) & (Res_line.resname < (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Reservation.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            create_t_reactive()
    else:

        if fresnr == 0:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & (Res_line.l_zuordnung[inc_value(2)] == 0) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft == fdate)).order_by(Reservation.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_reactive()

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.zimmer_wunsch,"*cancel*"))).order_by(Reservation.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if matches(str,r"*$arrival$*"):

                        if date_mdy(to_int(substring(str, 12, 2)) , to_int(substring(str, 9, 2)) , to_int(substring(str, 15, 4))) == fdate:
                            create_t_reactive()
                            break
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 2) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.resnr >= fresnr) & (Res_line.resnr <= (fresnr + 100)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_reactive()

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            for res_line.gastnr, res_line.resnr, res_line.reslinnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.arrangement, res_line.zipreis, res_line.zinr, res_line.cancelled, res_line.cancelled_id, res_line.bemerk, res_line.anztage, res_line.active_flag, res_line.betrieb_gastpay, res_line.kind1, res_line.kind2, res_line.changed, res_line.changed_id, res_line.zimmer_wunsch, res_line._recid, reservation.name, reservation.bemerk, reservation.gastnr, reservation.activeflag, reservation.depositgef, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.arrangement, Res_line.zipreis, Res_line.zinr, Res_line.cancelled, Res_line.cancelled_id, Res_line.bemerk, Res_line.anztage, Res_line.active_flag, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.kind2, Res_line.changed, Res_line.changed_id, Res_line.zimmer_wunsch, Res_line._recid, Reservation.name, Reservation.bemerk, Reservation.gastnr, Reservation.activeflag, Reservation.depositgef, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (fname).lower())).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag == 0) & ((Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.zimmer_wunsch,"*cancel*")) & (Res_line.resnr >= fresnr) & (Res_line.resnr <= (fresnr + 100)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_reactive()

    t_reactivate = query(t_reactivate_data, first=True)

    if t_reactivate:
        stat_avail = True
        resname = t_reactivate.rsvname

        guest = get_cache (Guest, {"gastnr": [(eq, t_reactivate.rsv_gastnr)]})
        address = guest.adresse1
        city = guest.wohnort + " " + guest.plz
        comments = t_reactivate.bemerk1 + chr_unicode(10) + t_reactivate.bemerk

    return generate_output()