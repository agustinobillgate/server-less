#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Reservation, Genstat, Res_line, Queasy, Guest, Nation

payload_list_data, Payload_list = create_model("Payload_list", {"sorttype":int, "from_month":string})

def res_groupsummary_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, Reservation, Genstat, Res_line, Queasy, Guest, Nation])

    res_grplist_data = []
    output_list_data = []
    grp_name:string = ""
    room:string = ""
    str:string = ""
    purpose_no:int = 0
    mm:int = 0
    yy:int = 0
    i:int = 0
    res_no:int = 0
    night_stay:int = 0
    tot_pax:int = 0
    tot_room:int = 0
    tot_rmnight:int = 0
    ci_date:date = None
    month_int:int = 0
    year_int:int = 0
    htparam = reservation = genstat = res_line = queasy = guest = nation = None

    res_grplist = payload_list = output_list = None

    res_grplist_data, Res_grplist = create_model("Res_grplist", {"res_month":string, "res_no":int, "resline_no":int, "group_name":string, "arrival_date":string, "depart_date":string, "night":int, "pax":int, "room_stay":int, "room_night":int, "ta_company":string, "purpose_stay":string, "nationality":string})
    output_list_data, Output_list = create_model("Output_list", {"month_report":int, "year_report":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_grplist_data, output_list_data, grp_name, room, str, purpose_no, mm, yy, i, res_no, night_stay, tot_pax, tot_room, tot_rmnight, ci_date, month_int, year_int, htparam, reservation, genstat, res_line, queasy, guest, nation


        nonlocal res_grplist, payload_list, output_list
        nonlocal res_grplist_data, output_list_data

        return {"res-grplist": res_grplist_data, "output-list": output_list_data}

    payload_list = query(payload_list_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate
    month_int = to_int(get_month(ci_date))
    year_int = to_int(get_year(ci_date))
    output_list.month_report = month_int
    output_list.year_report = year_int


    mm = to_int(substring(payload_list.from_month, 0, 2))
    yy = to_int(substring(payload_list.from_month, 2, 4))
    res_grplist_data.clear()

    if payload_list.sorttype == 1:

        genstat_obj_list = {}
        genstat = Genstat()
        reservation = Reservation()
        for genstat.res_char, genstat.res_date, genstat.erwachs, genstat.gratis, genstat.kind1, genstat.kind2, genstat.resnr, genstat.gastnr, genstat.zinr, genstat._recid, reservation.name, reservation.groupname, reservation._recid in db_session.query(Genstat.res_char, Genstat.res_date, Genstat.erwachs, Genstat.gratis, Genstat.kind1, Genstat.kind2, Genstat.resnr, Genstat.gastnr, Genstat.zinr, Genstat._recid, Reservation.name, Reservation.groupname, Reservation._recid).join(Reservation,(Reservation.resnr == Genstat.resnr)).filter(
                 (get_month(Genstat.datum) == mm) & (get_year(Genstat.datum) == yy) & (Genstat.res_char[inc_value(2)] != "")).order_by(Genstat.resnr, Genstat.res_char[inc_value(2)]).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if grp_name != genstat.res_char[2]:
                res_grplist = Res_grplist()
                res_grplist_data.append(res_grplist)

                res_grplist.group_name = genstat.res_char[2]
                res_grplist.arrival_date = to_string(genstat.res_date[0])
                res_grplist.depart_date = to_string(genstat.res_date[1])
                res_grplist.night = (genstat.res_date[1] - genstat.res_date[0]).days
                res_grplist.pax = genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2
                res_grplist.ta_company = reservation.name
                res_grplist.room_stay = 1


                night_stay = (genstat.res_date[1] - genstat.res_date[0]).days

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == genstat.resnr) & (matches(Res_line.zimmer_wunsch,"*SEGM_PUR*"))).first()

                if res_line:
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                            purpose_no = to_int(substring(str, 8))

                            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, purpose_no)]})

                            if queasy:
                                res_grplist.purpose_stay = queasy.char3

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                if guest:

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:
                        res_grplist.nationality = nation.bezeich
                room = genstat.zinr
                grp_name = genstat.res_char[2]
            res_grplist.pax = res_grplist.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2

            if room != genstat.zinr:
                res_grplist.room_stay = res_grplist.room_stay + 1
                room = genstat.zinr
    else:

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.zimmer_wunsch, res_line.ankunft, res_line.abreise, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.gastnr, res_line.zinr, res_line._recid, reservation.name, reservation.groupname, reservation._recid in db_session.query(Res_line.zimmer_wunsch, Res_line.ankunft, Res_line.abreise, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.gastnr, Res_line.zinr, Res_line._recid, Reservation.name, Reservation.groupname, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.groupname != "")).filter(
                 (get_month(Res_line.ankunft) == mm) & (get_year(Res_line.ankunft) == yy) & (get_month(Res_line.abreise) == mm) & (get_year(Res_line.abreise) == yy)).order_by(Reservation.resnr, Reservation.groupname).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if grp_name != reservation.groupname:
                res_grplist = Res_grplist()
                res_grplist_data.append(res_grplist)

                res_grplist.group_name = reservation.groupname
                res_grplist.arrival_date = to_string(res_line.ankunft)
                res_grplist.depart_date = to_string(res_line.abreise)
                res_grplist.night = (res_line.abreise - res_line.ankunft).days
                res_grplist.pax = res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                res_grplist.ta_company = reservation.name
                res_grplist.room_stay = 1

                if matches(res_line.zimmer_wunsch,r"*SEGM_PUR*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                            purpose_no = to_int(substring(str, 8))

                            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, purpose_no)]})

                            if queasy:
                                res_grplist.purpose_stay = queasy.char3

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if guest:

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:
                        res_grplist.nationality = nation.bezeich
                room = res_line.zinr
                grp_name = reservation.groupname
            res_grplist.pax = res_grplist.pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

            if room != res_line.zinr:
                res_grplist.room_stay = res_grplist.room_stay + 1
                room = res_line.zinr
    tot_pax = 0
    tot_room = 0
    tot_rmnight = 0

    for res_grplist in query(res_grplist_data):
        res_grplist.room_night = res_grplist.night * res_grplist.room_stay
        tot_pax = tot_pax + res_grplist.pax
        tot_room = tot_room + res_grplist.room_stay
        tot_rmnight = tot_rmnight + res_grplist.room_night

    res_grplist = query(res_grplist_data, first=True)

    if res_grplist:
        res_grplist = Res_grplist()
        res_grplist_data.append(res_grplist)

        res_grplist.group_name = "T O T A L"
        res_grplist.pax = tot_pax
        res_grplist.room_stay = tot_room
        res_grplist.room_night = tot_rmnight

    return generate_output()