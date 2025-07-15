#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.view_staycostbl import view_staycostbl
from models import Htparam, Zimkateg, Res_line, Guest, Reservation, Segment, Sourccod, Reslin_queasy, Guestseg

def res_list_2_webbl(case_type:int, from_date:date, to_date:date, resnr:int, gastnr:int, search_resno:int, search_voucher:string, search_prcode:string):

    prepare_cache ([Htparam, Zimkateg, Res_line, Guest, Reservation, Segment, Sourccod, Reslin_queasy, Guestseg])

    curr_select:string = ""
    res_listmain_data = []
    res_listmember_data = []
    vip_nr:List[int] = create_empty_list(10,0)
    res_bemerk:string = ""
    loopk:int = 0
    prcode:string = ""
    i:int = 0
    htparam = zimkateg = res_line = guest = reservation = segment = sourccod = reslin_queasy = guestseg = None

    res_listmain = res_listmember = revenue_list = None

    res_listmain_data, Res_listmain = create_model("Res_listmain", {"resdat":date, "resnr":int, "name":string, "groupname":string, "depositgef":Decimal, "limitdate":date, "depositbez":Decimal, "zahldatum":date, "depositbez2":Decimal, "zahldatum2":date, "useridanlage":string, "mutdat":date, "useridmutat":string, "gastnr":int, "bemerk":string, "grpflag":bool, "activeflag":int, "resname":string, "address":string, "city":string, "sob":string, "segment":string, "tot_revenue_resv":Decimal, "prcode":string})
    res_listmember_data, Res_listmember = create_model("Res_listmember", {"name":string, "ankunft":date, "abreise":date, "zinr":string, "kurzbez":string, "zipreis":Decimal, "arrangement":string, "erwachs":int, "gratis":int, "zimmeranz":int, "anztage":int, "changed_id":string, "changed":date, "gastnr":int, "resstatus":int, "zikatnr":int, "resnr":int, "bemerk":string, "active_flag":int, "l_zuordnung":[int,5], "reslinnr":int, "res_recid":int, "vip":string, "nat":string, "rate_code":string, "segment":string, "sp_req":string, "usr_id":string, "ratecode":string, "voucher_no":string, "child":int, "email":string, "phone_no":string, "sob":string})
    revenue_list_data, Revenue_list = create_model("Revenue_list", {"flag":int, "str":string, "str1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_select, res_listmain_data, res_listmember_data, vip_nr, res_bemerk, loopk, prcode, i, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno, search_voucher, search_prcode


        nonlocal res_listmain, res_listmember, revenue_list
        nonlocal res_listmain_data, res_listmember_data, revenue_list_data

        return {"res-listmain": res_listmain_data, "res-listmember": res_listmember_data}

    def calc_br1():

        nonlocal curr_select, res_listmain_data, res_listmember_data, vip_nr, res_bemerk, loopk, prcode, i, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno, search_voucher, search_prcode


        nonlocal res_listmain, res_listmember, revenue_list
        nonlocal res_listmain_data, res_listmember_data, revenue_list_data

        loopi:int = 0
        str:string = ""
        res_listmain_data.clear()
        res_listmember_data.clear()
        curr_select = ""

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        for res_line.name, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zipreis, res_line.arrangement, res_line.erwachs, res_line.gratis, res_line.zimmeranz, res_line.anztage, res_line.changed_id, res_line.changed, res_line.gastnr, res_line.resstatus, res_line.l_zuordnung, res_line.zikatnr, res_line.resnr, res_line.bemerk, res_line.active_flag, res_line.reslinnr, res_line._recid, res_line.kind1, res_line.gastnrmember, res_line.zimmer_wunsch, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zipreis, Res_line.arrangement, Res_line.erwachs, Res_line.gratis, Res_line.zimmeranz, Res_line.anztage, Res_line.changed_id, Res_line.changed, Res_line.gastnr, Res_line.resstatus, Res_line.l_zuordnung, Res_line.zikatnr, Res_line.resnr, Res_line.bemerk, Res_line.active_flag, Res_line.reslinnr, Res_line._recid, Res_line.kind1, Res_line.gastnrmember, Res_line.zimmer_wunsch, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.resnr == resnr) & (Res_line.resstatus != 12)).order_by(Res_line.resnr, Res_line.reslinnr, Res_line.zinr, Res_line.ankunft, Res_line.resstatus, func.substring(Res_line.name, 0, 32)).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            res_listmember = Res_listmember()
            res_listmember_data.append(res_listmember)

            res_listmember.name = res_line.name
            res_listmember.ankunft = res_line.ankunft
            res_listmember.abreise = res_line.abreise
            res_listmember.zinr = res_line.zinr
            res_listmember.kurzbez = zimkateg.kurzbez
            res_listmember.zipreis =  to_decimal(res_line.zipreis)
            res_listmember.arrangement = res_line.arrangement
            res_listmember.erwachs = res_line.erwachs
            res_listmember.gratis = res_line.gratis
            res_listmember.zimmeranz = res_line.zimmeranz
            res_listmember.anztage = res_line.anztage
            res_listmember.changed_id = res_line.changed_id
            res_listmember.changed = res_line.changed
            res_listmember.gastnr = res_line.gastnr
            res_listmember.resstatus = res_line.resstatus + res_line.l_zuordnung[2]
            res_listmember.zikatnr = res_line.zikatnr
            res_listmember.resnr = res_line.resnr
            res_listmember.bemerk = res_line.bemerk
            res_listmember.active_flag = res_line.active_flag
            res_listmember.l_zuordnung[2] = res_line.l_zuordnung[2]
            res_listmember.reslinnr = res_line.reslinnr
            res_listmember.res_recid = res_line._recid
            res_listmember.child = res_line.kind1


            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr_unicode(10) , "")


            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr_unicode(13) , "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "\\n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~r", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, "~r~n", "")
            res_listmember.bemerk = replace_str(res_listmember.bemerk, chr_unicode(10) + chr_unicode(13) , "")
            res_bemerk = ""
            for loopk in range(1,length(res_listmember.bemerk)  + 1) :

                if asc(substring(res_listmember.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(res_listmember.bemerk, loopk - 1, 1)
            res_listmember.bemerk = res_bemerk

            if length(res_listmember.bemerk) < 3:
                res_listmember.bemerk = replace_str(res_listmember.bemerk, chr_unicode(32) , "")

            if length(res_listmember.bemerk) == None:
                res_listmember.bemerk = ""

            if reslin_queasy:
                res_listmember.ratecode = reslin_queasy.char2


            else:
                res_listmember.ratecode = "Undefined"

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                if guest.mobil_telefon != "":
                    res_listmember.phone_no = guest.mobil_telefon

                if guest.mobil_telefon == "" and guest.telefon != "":
                    res_listmember.phone_no = guest.telefon

                if guest.email_adr != "":
                    res_listmember.email = guest.email_adr


            else:
                res_listmember.email = ""
                res_listmember.phone_no = ""

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation:

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    res_listmember.segment = entry(0, segment.bezeich, "$$0")
                res_listmember.usr_id = reservation.useridanlage
                res_listmember.voucher_no = reservation.vesrdepot

                sourccod = get_cache (Sourccod, {"betriebsnr": [(eq, reservation.betriebsnr)]})

                if sourccod:
                    res_listmember.sob = sourccod.bezeich


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == ("$CODE$").lower() :
                    res_listmember.rate_code = substring(str, 6)
                    break

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if reslin_queasy:
                res_listmember.sp_req = reslin_queasy.char3 + "," + res_listmember.sp_req
                res_listmember.ratecode = reslin_queasy.char2


            else:
                res_listmember.ratecode = "Undefined"

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment:
                        res_listmember.vip = segment.bezeich


                res_listmember.nat = guest.nation1


    def update_browse_b2():

        nonlocal curr_select, res_listmain_data, res_listmember_data, vip_nr, res_bemerk, loopk, prcode, i, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg
        nonlocal case_type, from_date, to_date, resnr, gastnr, search_resno, search_voucher, search_prcode


        nonlocal res_listmain, res_listmember, revenue_list
        nonlocal res_listmain_data, res_listmember_data, revenue_list_data


        res_listmain_data.clear()
        res_listmember_data.clear()

        if search_resno == 0 and search_voucher == "" and search_prcode == "":
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.resdat >= from_date) & (Reservation.resdat <= to_date) & (Reservation.activeflag <= 1)).order_by(Reservation.resnr, Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 12)]})

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        res_listmain.segment = entry(0, segment.bezeich, "$$0")

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        res_listmain.sob = sourccod.bezeich

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) + chr_unicode(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,length(res_listmain.bemerk)  + 1) :

                        if asc(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if length(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(32) , "")

                    if length(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""
                    res_listmain.tot_revenue_resv = count_total_reservation(reservation.resnr)

            reservation = get_cache (Reservation, {"resdat": [(ge, from_date),(le, to_date)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"

        elif search_resno != 0:
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.resnr == search_resno) & (Reservation.activeflag <= 1)).order_by(Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 12)]})

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        res_listmain.segment = entry(0, segment.bezeich, "$$0")

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        res_listmain.sob = sourccod.bezeich

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) + chr_unicode(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,length(res_listmain.bemerk)  + 1) :

                        if asc(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if length(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(32) , "")

                    if length(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""
                    res_listmain.tot_revenue_resv = count_total_reservation(reservation.resnr)

            reservation = get_cache (Reservation, {"resnr": [(eq, search_resno)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"

        elif search_voucher != "":
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.vesrdepot == (search_voucher).lower()) & (Reservation.activeflag <= 1)).order_by(Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 12)]})

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        res_listmain.sob = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        res_listmain.segment = entry(0, segment.bezeich, "$$0")

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) + chr_unicode(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,length(res_listmain.bemerk)  + 1) :

                        if asc(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if length(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(32) , "")

                    if length(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""
                    res_listmain.tot_revenue_resv = count_total_reservation(reservation.resnr)

            reservation = get_cache (Reservation, {"resnr": [(eq, search_resno)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"

        elif search_prcode != "":
            curr_select = ""

            for reservation in db_session.query(Reservation).filter(
                     (Reservation.activeflag <= 1)).order_by(Reservation.resdat, func.substring(Reservation.name, 0, 32)).all():

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 12) & (matches(Res_line.zimmer_wunsch,"*PromotionCode*"))).first()

                if res_line:
                    res_listmain = Res_listmain()
                    res_listmain_data.append(res_listmain)

                    res_listmain.resdat = reservation.resdat
                    res_listmain.resnr = reservation.resnr
                    res_listmain.name = reservation.name
                    res_listmain.groupname = reservation.groupname
                    res_listmain.depositgef =  to_decimal(reservation.depositgef)
                    res_listmain.limitdate = reservation.limitdate
                    res_listmain.depositbez =  to_decimal(reservation.depositbez)
                    res_listmain.zahldatum = reservation.zahldatum
                    res_listmain.depositbez2 =  to_decimal(reservation.depositbez2)
                    res_listmain.zahldatum2 = reservation.zahldatum2
                    res_listmain.useridanlage = reservation.useridanlage
                    res_listmain.mutdat = reservation.mutdat
                    res_listmain.useridmutat = reservation.useridmutat
                    res_listmain.gastnr = reservation.gastnr
                    res_listmain.bemerk = reservation.bemerk
                    res_listmain.grpflag = reservation.grpflag
                    res_listmain.activeflag = reservation.activeflag

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        res_listmain.segment = entry(0, segment.bezeich, "$$0")

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        res_listmain.sob = sourccod.bezeich

                    guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                    if guest:
                        res_listmain.resname = guest.name + ", " + guest.vorname1 +\
                                guest.anredefirma + " " + guest.anrede1
                        res_listmain.address = guest.adresse1 + " " + guest.adresse2
                        res_listmain.city = guest.land + " " + guest.wohnort + " " +\
                                guest.plz


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) , "")


                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(13) , "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "\\n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, "~r~n", "")
                    res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(10) + chr_unicode(13) , "")
                    res_bemerk = ""
                    for loopk in range(1,length(res_listmain.bemerk)  + 1) :

                        if asc(substring(res_listmain.bemerk, loopk - 1, 1)) == 0:
                            pass
                        else:
                            res_bemerk = res_bemerk + substring(res_listmain.bemerk, loopk - 1, 1)
                    res_listmain.bemerk = res_bemerk

                    if length(res_listmain.bemerk) < 3:
                        res_listmain.bemerk = replace_str(res_listmain.bemerk, chr_unicode(32) , "")

                    if length(res_listmain.bemerk) == None:
                        res_listmain.bemerk = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        prcode = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if matches(prcode,r"*$prcode$*"):
                            res_listmain.prcode = trim (substring(prcode, 8))


                    res_listmain.tot_revenue_resv = count_total_reservation(reservation.resnr)

            reservation = get_cache (Reservation, {"resnr": [(eq, search_resno)],"activeflag": [(le, 1)]})

            if reservation:
                curr_select = "mainres"


    def count_total_reservation(resnr:int):

        nonlocal curr_select, res_listmain_data, res_listmember_data, vip_nr, res_bemerk, loopk, prcode, i, htparam, zimkateg, res_line, guest, reservation, segment, sourccod, reslin_queasy, guestseg
        nonlocal case_type, from_date, to_date, gastnr, search_resno, search_voucher, search_prcode


        nonlocal res_listmain, res_listmember, revenue_list
        nonlocal res_listmain_data, res_listmember_data, revenue_list_data

        tot_revenue_resv = to_decimal("0.0")
        excp_rev:string = ""

        def generate_inner_output():
            return (tot_revenue_resv)


        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr)).order_by(Res_line._recid).all():
            revenue_list_data = get_output(view_staycostbl(0, resnr, res_line.reslinnr, ""))

            revenue_list = query(revenue_list_data, last=True)

            if revenue_list:
                excp_rev = to_string(trim(entry(1, revenue_list.str, "=")))
                tot_revenue_resv =  to_decimal(tot_revenue_resv) + to_decimal(to_decimal(excp_rev)) * to_decimal(res_line.zimmeranz)

        return generate_inner_output()


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
    res_listmain_data.clear()
    res_listmember_data.clear()

    if case_type == 1:
        update_browse_b2()
    else:
        calc_br1()

    return generate_output()