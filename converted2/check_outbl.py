#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Zimkateg, Guest, Reservation, Res_line

def check_outbl(sorttype:int, input_resnr:int, lzinr:string, lname:string, gname:string):

    prepare_cache ([Zimkateg, Guest, Reservation, Res_line])

    ci_date = None
    check_out_list_data = []
    zimkateg = guest = reservation = res_line = None

    check_out_list = None

    check_out_list_data, Check_out_list = create_model("Check_out_list", {"zinr":string, "reser_name":string, "resli_name":string, "g_name":string, "ankunft":date, "abreise":date, "kurzbez":string, "erwachs":int, "gratis":int, "resstatus":int, "arrangement":string, "zipreis":Decimal, "groupname":string, "resnr":int, "gastnr":int, "bemerk":string, "gastnrmember":int, "reslinnr":int, "zimmeranz":int, "res_address":string, "res_city":string, "res_bemerk":string, "recid_resline":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, check_out_list_data, zimkateg, guest, reservation, res_line
        nonlocal sorttype, input_resnr, lzinr, lname, gname


        nonlocal check_out_list
        nonlocal check_out_list_data

        return {"ci_date": ci_date, "check-out-list": check_out_list_data}

    def disp_arlist():

        nonlocal ci_date, check_out_list_data, zimkateg, guest, reservation, res_line
        nonlocal sorttype, input_resnr, lzinr, lname, gname


        nonlocal check_out_list
        nonlocal check_out_list_data

        if sorttype == 1:

            if input_resnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr >= (lzinr).lower()) & (Res_line.abreise == ci_date)).order_by((Res_line.zinr + Res_line.name)).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

            else:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr >= (lzinr).lower()) & (Res_line.resnr == input_resnr)).order_by((Res_line.zinr + Res_line.name)).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()


        elif sorttype == 2:

            if input_resnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.name >= (lname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr >= (lzinr).lower()) & (Res_line.abreise == ci_date)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

            else:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (Guest.name >= (lname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr >= (lzinr).lower()) & (Res_line.resnr == input_resnr)).order_by(Res_line.name).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()


        elif sorttype == 3:

            if input_resnr == 0:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.name >= (gname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.grpflag)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == ci_date)).order_by((Guest.name + to_string(Res_line.resnr))).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

            else:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                guest = Guest()
                reservation = Reservation()
                for res_line.zinr, res_line.name, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.resstatus, res_line.arrangement, res_line.zipreis, res_line.resnr, res_line.gastnr, res_line.bemerk, res_line.gastnrmember, res_line.reslinnr, res_line.zimmeranz, res_line._recid, zimkateg.kurzbez, zimkateg._recid, guest.name, guest.adresse1, guest.wohnort, guest.plz, guest._recid, reservation.name, reservation.groupname, reservation.bemerk, reservation._recid in db_session.query(Res_line.zinr, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.resstatus, Res_line.arrangement, Res_line.zipreis, Res_line.resnr, Res_line.gastnr, Res_line.bemerk, Res_line.gastnrmember, Res_line.reslinnr, Res_line.zimmeranz, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Guest.name, Guest.adresse1, Guest.wohnort, Guest.plz, Guest._recid, Reservation.name, Reservation.groupname, Reservation.bemerk, Reservation._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.name >= (gname).lower())).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.grpflag)).filter(
                         ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.resnr == input_resnr)).order_by((Guest.name + to_string(Res_line.resnr))).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    assign_it()

    def assign_it():

        nonlocal ci_date, check_out_list_data, zimkateg, guest, reservation, res_line
        nonlocal sorttype, input_resnr, lzinr, lname, gname


        nonlocal check_out_list
        nonlocal check_out_list_data


        check_out_list = Check_out_list()
        check_out_list_data.append(check_out_list)

        check_out_list.zinr = res_line.zinr
        check_out_list.reser_name = reservation.name
        check_out_list.resli_name = res_line.name
        check_out_list.g_name = guest.name
        check_out_list.ankunft = res_line.ankunft
        check_out_list.abreise = res_line.abreise
        check_out_list.kurzbez = zimkateg.kurzbez
        check_out_list.erwachs = res_line.erwachs
        check_out_list.gratis = res_line.gratis
        check_out_list.resstatus = res_line.resstatus
        check_out_list.arrangement = res_line.arrangement
        check_out_list.zipreis =  to_decimal(res_line.zipreis)
        check_out_list.groupname = reservation.groupname
        check_out_list.resnr = res_line.resnr
        check_out_list.gastnr = res_line.gastnr
        check_out_list.bemerk = res_line.bemerk
        check_out_list.gastnrmember = res_line.gastnrmember
        check_out_list.reslinnr = res_line.reslinnr
        check_out_list.zimmeranz = res_line.zimmeranz
        check_out_list.res_address = guest.adresse1
        check_out_list.res_city = guest.wohnort + " " + guest.plz
        check_out_list.res_bemerk = reservation.bemerk
        check_out_list.recid_resline = res_line._recid

    ci_date = get_output(htpdate(87))
    disp_arlist()

    return generate_output()