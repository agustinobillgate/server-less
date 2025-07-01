#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Htparam, Reservation, Zimkateg, Res_line, History, Segment, Guestseg

def no_show_1_webbl(case_type:int, gname:string, fdate:date, tdate:date, resno:int, gastno:int, comments:string):

    prepare_cache ([Guest, Htparam, Reservation, Zimkateg, Res_line, History, Segment, Guestseg])

    resname = ""
    address = ""
    city = ""
    stat_avail = False
    tot_rm = 0
    tot_pax = 0
    tot_com = 0
    t_noshow_list = []
    tot_rm_reactive = 0
    tot_nite_reactive = 0
    tot_pax_reactive = 0
    tot_ch1_reactive = 0
    tot_com_reactive = 0
    vip_nr:List[int] = create_empty_list(10,0)
    guest = htparam = reservation = zimkateg = res_line = history = segment = guestseg = None

    t_noshow = r_guest = None

    t_noshow_list, T_noshow = create_model("T_noshow", {"resnr":int, "gastnr":int, "rsname":string, "gsname":string, "ankunft":date, "abreise":date, "zimmeranz":int, "kurzbez":string, "erwachs":int, "gratis":int, "arrangement":string, "zinr":string, "zipreis":Decimal, "vesrdepot2":string, "bemerk":string, "bemerk1":string, "rsvname":string, "rsv_gastnr":int, "vip":string, "nat":string, "rate_code":string, "segment":string, "bill_detail":string, "usr_id":string, "reslinnr":int, "flag":int})

    R_guest = create_buffer("R_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list

        return {"comments": comments, "resname": resname, "address": address, "city": city, "stat_avail": stat_avail, "tot_rm": tot_rm, "tot_pax": tot_pax, "tot_com": tot_com, "t-noshow": t_noshow_list, "tot_rm_reactive": tot_rm_reactive, "tot_nite_reactive": tot_nite_reactive, "tot_pax_reactive": tot_pax_reactive, "tot_ch1_reactive": tot_ch1_reactive, "tot_com_reactive": tot_com_reactive}

    def disp_noshow1():

        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list


        tot_rm = 0
        tot_pax = 0
        tot_com = 0

        if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            r_guest = Guest()
            zimkateg = Zimkateg()
            for res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, r_guest.adresse1, r_guest.wohnort, r_guest.plz, r_guest.gastnr, r_guest.nation1, r_guest.name, r_guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, R_guest.adresse1, R_guest.wohnort, R_guest.plz, R_guest.gastnr, R_guest.nation1, R_guest.name, R_guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(R_guest,(R_guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resstatus == 10) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_noshow()

                if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                    pass
                else:
                    tot_rm = tot_rm + res_line.zimmeranz
                tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
                tot_com = tot_com + res_line.gratis * res_line.zimmeranz

            history_obj_list = {}
            history = History()
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for history.resnr, history.reslinnr, history._recid, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest.gastnr, guest.nation1, guest.name, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest.gastnr, Guest.nation1, Guest.name, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.betrieb_gastpay == 10)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                if history_obj_list.get(history._recid):
                    continue
                else:
                    history_obj_list[history._recid] = True

                t_noshow = query(t_noshow_list, filters=(lambda t_noshow: t_noshow.resnr == history.resnr and t_noshow.reslinnr == history.reslinnr), first=True)

                if not t_noshow:
                    assign_it_reactive()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            r_guest = Guest()
            zimkateg = Zimkateg()
            for res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, r_guest.adresse1, r_guest.wohnort, r_guest.plz, r_guest.gastnr, r_guest.nation1, r_guest.name, r_guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, R_guest.adresse1, R_guest.wohnort, R_guest.plz, R_guest.gastnr, R_guest.nation1, R_guest.name, R_guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(R_guest,(R_guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resstatus == 10) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_noshow()

                if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                    pass
                else:
                    tot_rm = tot_rm + res_line.zimmeranz
                tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
                tot_com = tot_com + res_line.gratis * res_line.zimmeranz

            history_obj_list = {}
            history = History()
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for history.resnr, history.reslinnr, history._recid, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest.gastnr, guest.nation1, guest.name, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest.gastnr, Guest.nation1, Guest.name, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.betrieb_gastpay == 10)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                if history_obj_list.get(history._recid):
                    continue
                else:
                    history_obj_list[history._recid] = True

                t_noshow = query(t_noshow_list, filters=(lambda t_noshow: t_noshow.resnr == history.resnr and t_noshow.reslinnr == history.reslinnr), first=True)

                if not t_noshow:
                    assign_it_reactive()
        view_resline()


    def disp_noshow2():

        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list

        res_buff = None
        tot_rm = 0
        tot_pax = 0
        tot_com = 0


        Res_buff =  create_buffer("Res_buff",Res_line)

        if substring(gname, 0, 1) == ("*").lower()  and substring(gname, length(gname) - 1, 1) == ("*").lower() :

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            r_guest = Guest()
            zimkateg = Zimkateg()
            for res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, r_guest.adresse1, r_guest.wohnort, r_guest.plz, r_guest.gastnr, r_guest.nation1, r_guest.name, r_guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, R_guest.adresse1, R_guest.wohnort, R_guest.plz, R_guest.gastnr, R_guest.nation1, R_guest.name, R_guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(R_guest,(R_guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resstatus == 10) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_noshow()

                if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                    pass
                else:
                    tot_rm = tot_rm + res_line.zimmeranz
                tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
                tot_com = tot_com + res_line.gratis * res_line.zimmeranz

            history_obj_list = {}
            history = History()
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for history.resnr, history.reslinnr, history._recid, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest.gastnr, guest.nation1, guest.name, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest.gastnr, Guest.nation1, Guest.name, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (matches(Res_line.name,(gname))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.betrieb_gastpay == 10)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                if history_obj_list.get(history._recid):
                    continue
                else:
                    history_obj_list[history._recid] = True

                t_noshow = query(t_noshow_list, filters=(lambda t_noshow: t_noshow.resnr == history.resnr and t_noshow.reslinnr == history.reslinnr), first=True)

                if not t_noshow:
                    assign_it_reactive()
        else:

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            r_guest = Guest()
            zimkateg = Zimkateg()
            for res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, r_guest.adresse1, r_guest.wohnort, r_guest.plz, r_guest.gastnr, r_guest.nation1, r_guest.name, r_guest._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, R_guest.adresse1, R_guest.wohnort, R_guest.plz, R_guest.gastnr, R_guest.nation1, R_guest.name, R_guest._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(R_guest,(R_guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.resstatus == 10) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.name >= (gname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.ankunft).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_t_noshow()

                if res_line.zimmerfix or res_line.l_zuordnung[2] == 1 or (res_line.kontakt_nr != 0 and (res_line.kontakt_nr != res_line.reslinnr)):
                    pass
                else:
                    tot_rm = tot_rm + res_line.zimmeranz
                tot_pax = tot_pax + res_line.erwachs * res_line.zimmeranz
                tot_com = tot_com + res_line.gratis * res_line.zimmeranz

            history_obj_list = {}
            history = History()
            res_line = Res_line()
            reservation = Reservation()
            zimkateg = Zimkateg()
            guest = Guest()
            for history.resnr, history.reslinnr, history._recid, res_line.kontakt_nr, res_line.reslinnr, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.resnr, res_line.gastnr, res_line.name, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.zinr, res_line.zipreis, res_line.bemerk, res_line.cancelled_id, res_line.zimmer_wunsch, res_line.gastnrmember, res_line.betrieb_gastpay, res_line.kind1, res_line.zimmerfix, res_line.l_zuordnung, res_line._recid, reservation.vesrdepot2, reservation.bemerk, reservation.name, reservation.gastnr, reservation.segmentcode, reservation.useridanlage, reservation._recid, zimkateg.kurzbez, zimkateg._recid, guest.adresse1, guest.wohnort, guest.plz, guest.gastnr, guest.nation1, guest.name, guest._recid in db_session.query(History.resnr, History.reslinnr, History._recid, Res_line.kontakt_nr, Res_line.reslinnr, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.resnr, Res_line.gastnr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.zinr, Res_line.zipreis, Res_line.bemerk, Res_line.cancelled_id, Res_line.zimmer_wunsch, Res_line.gastnrmember, Res_line.betrieb_gastpay, Res_line.kind1, Res_line.zimmerfix, Res_line.l_zuordnung, Res_line._recid, Reservation.vesrdepot2, Reservation.bemerk, Reservation.name, Reservation.gastnr, Reservation.segmentcode, Reservation.useridanlage, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.adresse1, Guest.wohnort, Guest.plz, Guest.gastnr, Guest.nation1, Guest.name, Guest._recid).join(Res_line,(Res_line.resnr == History.resnr) & (Res_line.reslinnr == History.reslinnr) & (Res_line.name >= (gname).lower()) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.betrieb_gastpay == 10)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                     (matches(History.bemerk,"*reactive by*")) & (History.ankunft >= fdate) & (History.ankunft <= tdate)).order_by(History.ankunft, History.gastinfo).all():
                if history_obj_list.get(history._recid):
                    continue
                else:
                    history_obj_list[history._recid] = True

                t_noshow = query(t_noshow_list, filters=(lambda t_noshow: t_noshow.resnr == history.resnr and t_noshow.reslinnr == history.reslinnr), first=True)

                if not t_noshow:
                    assign_it_reactive()
        view_resline()


    def view_resline():

        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list

        t_noshow = query(t_noshow_list, first=True)

        if t_noshow:
            stat_avail = True
            resname = t_noshow.rsvname

            guest = get_cache (Guest, {"gastnr": [(eq, t_noshow.rsv_gastnr)]})
            address = guest.adresse1
            city = guest.wohnort + " " + guest.plz

            if t_noshow.vesrdepot2 != "":
                comments = t_noshow.vesrdepot2 + chr_unicode(10)
            comments = t_noshow.bemerk1 + chr_unicode(10) + t_noshow.bemerk


    def create_t_noshow():

        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list

        loopi:int = 0
        str:string = ""
        t_noshow = T_noshow()
        t_noshow_list.append(t_noshow)

        t_noshow.resnr = res_line.resnr
        t_noshow.gastnr = res_line.gastnr
        t_noshow.rsname = res_line.name
        t_noshow.gsname = r_guest.name
        t_noshow.ankunft = res_line.ankunft
        t_noshow.abreise = res_line.abreise
        t_noshow.zimmeranz = res_line.zimmeranz
        t_noshow.kurzbez = zimkateg.kurzbez
        t_noshow.erwachs = res_line.erwachs
        t_noshow.gratis = res_line.gratis
        t_noshow.arrangement = res_line.arrangement
        t_noshow.zinr = res_line.zinr
        t_noshow.zipreis =  to_decimal(res_line.zipreis)
        t_noshow.vesrdepot2 = reservation.vesrdepot2
        t_noshow.bemerk = res_line.bemerk
        t_noshow.bemerk1 = reservation.bemerk
        t_noshow.rsvname = reservation.name
        t_noshow.rsv_gastnr = reservation.gastnr
        t_noshow.reslinnr = res_line.reslinnr

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

        if segment:
            t_noshow.segment = entry(0, segment.bezeich, "$$0")
        t_noshow.usr_id = entry(0, res_line.cancelled_id, ";")


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                t_noshow.rate_code = substring(str, 6)
                return

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

            if guestseg:

                segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                if segment:
                    t_noshow.vip = segment.bezeich


            t_noshow.nat = guest.nation1


    def assign_it_reactive():

        nonlocal resname, address, city, stat_avail, tot_rm, tot_pax, tot_com, t_noshow_list, tot_rm_reactive, tot_nite_reactive, tot_pax_reactive, tot_ch1_reactive, tot_com_reactive, vip_nr, guest, htparam, reservation, zimkateg, res_line, history, segment, guestseg
        nonlocal case_type, gname, fdate, tdate, resno, gastno, comments
        nonlocal r_guest


        nonlocal t_noshow, r_guest
        nonlocal t_noshow_list

        night:int = 0
        loopi:int = 0
        str:string = ""

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


        t_noshow = T_noshow()
        t_noshow_list.append(t_noshow)

        t_noshow.resnr = res_line.resnr
        t_noshow.gastnr = res_line.gastnr
        t_noshow.gsname = guest.name
        t_noshow.rsname = res_line.name
        t_noshow.ankunft = res_line.ankunft
        t_noshow.abreise = res_line.abreise
        t_noshow.zimmeranz = res_line.zimmeranz
        t_noshow.kurzbez = zimkateg.kurzbez
        t_noshow.erwachs = res_line.erwachs
        t_noshow.gratis = res_line.gratis
        t_noshow.arrangement = res_line.arrangement
        t_noshow.zinr = res_line.zinr
        t_noshow.zipreis =  to_decimal(res_line.zipreis)
        t_noshow.vesrdepot2 = reservation.vesrdepot2
        t_noshow.bemerk = res_line.bemerk
        t_noshow.bemerk1 = reservation.bemerk
        t_noshow.rsvname = reservation.name
        t_noshow.rsv_gastnr = reservation.gastnr
        t_noshow.flag = 1

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

        if segment:
            t_noshow.segment = entry(0, segment.bezeich, "$$0")
        t_noshow.usr_id = reservation.useridanlage


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                t_noshow.rate_code = substring(str, 6)
                return

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

            if segment:
                t_noshow.vip = segment.bezeich


        t_noshow.nat = guest.nation1


    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
    vip_nr[0] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
    vip_nr[1] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
    vip_nr[2] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
    vip_nr[3] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
    vip_nr[4] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
    vip_nr[5] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
    vip_nr[6] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
    vip_nr[7] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
    vip_nr[8] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
    vip_nr[9] = htparam.finteger

    if case_type == 1:
        disp_noshow1()
    elif case_type == 2:
        disp_noshow2()

    return generate_output()