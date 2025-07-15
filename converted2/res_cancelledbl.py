#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Reservation, Zimkateg, Guest, Res_line, History

def res_cancelledbl(case_type:int, show_rate:bool, curr_rmtype:string, do_it:bool, gname:string, tname:string, res_status:int, fdate:date, tdate:date, kart:int):

    prepare_cache ([Reservation, Zimkateg, Guest, Res_line, History])

    tot_rm = 0
    tot_pax = 0
    tot_ch1 = 0
    tot_com = 0
    tot_nite = 0
    tot_rm_reactive = 0
    tot_pax_reactive = 0
    tot_ch1_reactive = 0
    tot_com_reactive = 0
    tot_nite_reactive = 0
    res_cancelled_list_data = []
    reservation = zimkateg = guest = res_line = history = None

    res_cancelled_list = None

    res_cancelled_list_data, Res_cancelled_list = create_model("Res_cancelled_list", {"resnr":int, "columnr":int, "reslinnr":int, "gastnr":int, "rsv_gastnr":int, "zinr":string, "name":string, "rsv_name":string, "ankunft":date, "bemerk":string, "rsv_bemerk":string, "anztage":int, "abreise":date, "zimmeranz":int, "kurzbez":string, "erwachs":int, "kind1":int, "gratis":int, "arrangement":string, "zipreis":Decimal, "betrieb_gastpay":int, "cancelled":date, "cancelled_id":string, "resdat":date, "vesrdepot2":string, "address":string, "city":string, "res_resnr":int, "groupname":string, "flag":int, "depositpay":Decimal, "deposit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        return {"tot_rm": tot_rm, "tot_pax": tot_pax, "tot_ch1": tot_ch1, "tot_com": tot_com, "tot_nite": tot_nite, "tot_rm_reactive": tot_rm_reactive, "tot_pax_reactive": tot_pax_reactive, "tot_ch1_reactive": tot_ch1_reactive, "tot_com_reactive": tot_com_reactive, "tot_nite_reactive": tot_nite_reactive, "res-cancelled-list": res_cancelled_list_data}

    def disp_noshow():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if show_rate:
            disp_noshow1()
        else:
            disp_noshow2()


    def disp_noshowc():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if show_rate:
            disp_noshowc1()
        else:
            disp_noshowc2()


    def disp_noshow1():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if do_it:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshow1_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshow1_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()


    def disp_noshow2():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if do_it:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshow2_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshow2_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()


    def disp_noshowc1():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if do_it:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshowc1_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.active_flag == 2) & (Res_line.betrieb_gastpay != 3) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshowc1_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.active_flag == 2) & (Res_line.betrieb_gastpay != 3) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()


    def disp_noshowc2():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if do_it:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshowc2_a()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
        else:

            if matches(curr_rmtype,r"*-ALL-*"):
                disp_noshowc2_b()
            else:

                if fdate != None and tdate != None:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                else:

                    if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                    else:

                        if res_status == 1:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()
                        else:

                            res_line_obj_list = {}
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                                if res_line_obj_list.get(res_line._recid):
                                    continue
                                else:
                                    res_line_obj_list[res_line._recid] = True


                                assign_it()

                            history_obj_list = {}
                            history = History()
                            res_line = Res_line()
                            reservation = Reservation()
                            zimkateg = Zimkateg()
                            guest = Guest()
                            for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.kurzbez == curr_rmtype)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                                if history_obj_list.get(history._recid):
                                    continue
                                else:
                                    history_obj_list[history._recid] = True

                                res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                                if not res_cancelled_list:
                                    assign_it_reactive()


    def disp_noshow1_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshow1_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*"))).order_by(History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshow2_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshow2_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshowc1_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.active_flag == 2) & (Res_line.betrieb_gastpay != 3) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshowc1_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.active_flag == 2) & (Res_line.betrieb_gastpay != 3) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshowc2_a():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == kart)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def disp_noshowc2_b():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if fdate != None and tdate != None:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.cancelled, Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
        else:

            if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
            else:

                if res_status == 1:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay != 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()
                else:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.resstatus == 9) & (Res_line.betrieb_gastpay == 3) & (Res_line.active_flag == 2) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        assign_it()

                    history_obj_list = {}
                    history = History()
                    res_line = Res_line()
                    reservation = Reservation()
                    zimkateg = Zimkateg()
                    guest = Guest()
                    for history.resnr, history.reslinnr, history._recid, res_line.betrieb_gastpay, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.abreise, res_line.ankunft, res_line.erwachs, res_line.kind1, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.zinr, res_line.name, res_line.bemerk, res_line.anztage, res_line.arrangement, res_line.zipreis, res_line.cancelled, res_line.cancelled_id, res_line.storno_nr, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.gastnr, reservation.name, reservation.bemerk, reservation.resdat, reservation.vesrdepot2, reservation.resnr, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.betrieb_gastpay, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.abreise, Res_line.ankunft, Res_line.erwachs, Res_line.kind1, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.zinr, Res_line.name, Res_line.bemerk, Res_line.anztage, Res_line.arrangement, Res_line.zipreis, Res_line.cancelled, Res_line.cancelled_id, Res_line.storno_nr, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.gastnr, Reservation.name, Reservation.bemerk, Reservation.resdat, Reservation.vesrdepot2, Reservation.resnr, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.name <= (tname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                        if history_obj_list.get(history._recid):
                            continue
                        else:
                            history_obj_list[history._recid] = True

                        res_cancelled_list = query(res_cancelled_list_data, filters=(lambda res_cancelled_list: res_cancelled_list.resnr == history.resnr and res_cancelled_list.reslinnr == history.reslinnr), first=True)

                        if not res_cancelled_list:
                            assign_it_reactive()


    def assign_it():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or res_line.betrieb_gastpay == 11 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
            pass
        else:
            tot_rm = tot_rm + res_line.zimmeranz
            tot_nite = tot_nite + (res_line.abreise - res_line.ankunft) *\
                res_line.zimmeranz


        tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
        tot_ch1 = tot_ch1 + res_line.kind1 * res_line.zimmeranz
        tot_com = tot_com + res_line.gratis * res_line.zimmeranz


        res_cancelled_list = Res_cancelled_list()
        res_cancelled_list_data.append(res_cancelled_list)

        res_cancelled_list.resnr = res_line.resnr
        res_cancelled_list.reslinnr = res_line.reslinnr
        res_cancelled_list.gastnr = res_line.gastnr
        res_cancelled_list.rsv_gastnr = reservation.gastnr
        res_cancelled_list.zinr = res_line.zinr
        res_cancelled_list.name = res_line.name
        res_cancelled_list.rsv_name = reservation.name
        res_cancelled_list.ankunft = res_line.ankunft
        res_cancelled_list.bemerk = res_line.bemerk
        res_cancelled_list.rsv_bemerk = reservation.bemerk
        res_cancelled_list.anztage = res_line.anztage
        res_cancelled_list.abreise = res_line.abreise
        res_cancelled_list.zimmeranz = res_line.zimmeranz
        res_cancelled_list.kurzbez = zimkateg.kurzbez
        res_cancelled_list.erwachs = res_line.erwachs
        res_cancelled_list.kind1 = res_line.kind1
        res_cancelled_list.gratis = res_line.gratis
        res_cancelled_list.arrangement = res_line.arrangement
        res_cancelled_list.zipreis =  to_decimal(res_line.zipreis)
        res_cancelled_list.betrieb_gastpay = res_line.betrieb_gastpay
        res_cancelled_list.cancelled = res_line.cancelled
        res_cancelled_list.cancelled_id = res_line.cancelled_id
        res_cancelled_list.resdat = reservation.resdat
        res_cancelled_list.vesrdepot2 = reservation.vesrdepot2
        res_cancelled_list.address = guest.adresse1
        res_cancelled_list.city = guest.wohnort + " " + guest.plz
        res_cancelled_list.res_resnr = reservation.resnr
        res_cancelled_list.groupname = reservation.groupname
        res_cancelled_list.deposit =  to_decimal(reservation.depositgef)
        res_cancelled_list.depositpay =  to_decimal(reservation.depositbez)


    def assign_it_reactive():

        nonlocal tot_rm, tot_pax, tot_ch1, tot_com, tot_nite, tot_rm_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, tot_nite_reactive, res_cancelled_list_data, reservation, zimkateg, guest, res_line, history
        nonlocal case_type, show_rate, curr_rmtype, do_it, gname, tname, res_status, fdate, tdate, kart


        nonlocal res_cancelled_list
        nonlocal res_cancelled_list_data

        night:int = 0

        if res_line.abreise == res_line.ankunft:
            night = 1
        else:
            night = (res_line.abreise - res_line.ankunft).days

        if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or res_line.betrieb_gastpay == 11 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
            pass
        else:
            tot_rm_reactive = tot_rm_reactive + res_line.zimmeranz
            tot_nite_reactive = tot_nite_reactive + night * res_line.zimmeranz


        tot_pax_reactive = tot_pax_reactive + res_line.erwachs * res_line.zimmeranz
        tot_ch1_reactive = tot_ch1_reactive + res_line.kind1 * res_line.zimmeranz
        tot_com_reactive = tot_com_reactive + res_line.gratis * res_line.zimmeranz


        res_cancelled_list = Res_cancelled_list()
        res_cancelled_list_data.append(res_cancelled_list)

        res_cancelled_list.resnr = res_line.resnr
        res_cancelled_list.columnr = res_line.storno_nr
        res_cancelled_list.reslinnr = res_line.reslinnr
        res_cancelled_list.gastnr = res_line.gastnr
        res_cancelled_list.rsv_gastnr = reservation.gastnr
        res_cancelled_list.zinr = res_line.zinr
        res_cancelled_list.name = res_line.name
        res_cancelled_list.rsv_name = reservation.name
        res_cancelled_list.ankunft = res_line.ankunft
        res_cancelled_list.bemerk = res_line.bemerk
        res_cancelled_list.rsv_bemerk = reservation.bemerk
        res_cancelled_list.anztage = res_line.anztage
        res_cancelled_list.abreise = res_line.abreise
        res_cancelled_list.zimmeranz = res_line.zimmeranz
        res_cancelled_list.kurzbez = zimkateg.kurzbez
        res_cancelled_list.erwachs = res_line.erwachs
        res_cancelled_list.kind1 = res_line.kind1
        res_cancelled_list.gratis = res_line.gratis
        res_cancelled_list.arrangement = res_line.arrangement
        res_cancelled_list.zipreis =  to_decimal(res_line.zipreis)
        res_cancelled_list.betrieb_gastpay = res_line.betrieb_gastpay
        res_cancelled_list.cancelled = res_line.cancelled
        res_cancelled_list.cancelled_id = res_line.cancelled_id
        res_cancelled_list.resdat = reservation.resdat
        res_cancelled_list.vesrdepot2 = reservation.vesrdepot2
        res_cancelled_list.address = guest.adresse1
        res_cancelled_list.city = guest.wohnort + " " + guest.plz
        res_cancelled_list.res_resnr = reservation.resnr
        res_cancelled_list.groupname = reservation.groupname
        res_cancelled_list.flag = 1
        res_cancelled_list.deposit =  to_decimal(reservation.depositgef)
        res_cancelled_list.depositpay =  to_decimal(reservation.depositbez)


    if case_type == 1:
        disp_noshow()

    elif case_type == 2:
        disp_noshowc()

    return generate_output()