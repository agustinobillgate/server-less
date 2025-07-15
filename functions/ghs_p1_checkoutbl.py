#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from models import Guest, Zimkateg, Reservation, Sourccod, Segment, Queasy, Res_line

def ghs_p1_checkoutbl(datum:date, propid:string):

    prepare_cache ([Guest, Zimkateg, Sourccod, Segment, Queasy, Res_line])

    p_list_data = []
    birthdate:string = ""
    str_rsv:string = ""
    contcode:string = ""
    loop_i:int = 0
    curr_i:int = 0
    rsv_date:date = None
    to_date:date = None
    datum1:date = None
    flodging:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    breakfast:Decimal = to_decimal("0.0")
    lunch:Decimal = to_decimal("0.0")
    dinner:Decimal = to_decimal("0.0")
    others:Decimal = to_decimal("0.0")
    rmrate:Decimal = to_decimal("0.0")
    net_vat:Decimal = to_decimal("0.0")
    net_service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    t_rmrev:Decimal = to_decimal("0.0")
    t_fbrev:Decimal = to_decimal("0.0")
    t_others:Decimal = to_decimal("0.0")
    ci_date:string = ""
    co_date:string = ""
    guest = zimkateg = reservation = sourccod = segment = queasy = res_line = None

    p_list = gmember = gcomp = None

    p_list_data, P_list = create_model("P_list", {"confno":string, "arrdate":string, "depdate":string, "roomtype":string, "roomno":string, "roomrate":Decimal, "gname":string, "comp":string, "sourcename":string, "memberno":string, "totrev":Decimal, "rmrev":Decimal, "fbrev":Decimal, "others":Decimal, "propid":string, "reward":string, "bookdate":string, "market":string, "note":string, "profile":string, "exportdate":string, "ratecode":string})

    Gmember = create_buffer("Gmember",Guest)
    Gcomp = create_buffer("Gcomp",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_list_data, birthdate, str_rsv, contcode, loop_i, curr_i, rsv_date, to_date, datum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, ci_date, co_date, guest, zimkateg, reservation, sourccod, segment, queasy, res_line
        nonlocal datum, propid
        nonlocal gmember, gcomp


        nonlocal p_list, gmember, gcomp
        nonlocal p_list_data

        return {"p-list": p_list_data}

    res_line_obj_list = {}
    for res_line, gmember, zimkateg, reservation, sourccod, segment, queasy in db_session.query(Res_line, Gmember, Zimkateg, Reservation, Sourccod, Segment, Queasy).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Queasy,(Queasy.key == 152) & (Queasy.number1 == Zimkateg.typ)).filter(
             (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.abreise == datum)).order_by(Res_line._recid).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        t_rmrev =  to_decimal("0")
        t_fbrev =  to_decimal("0")
        t_others =  to_decimal("0")
        curr_i = 0

        if gmember:
            p_list = P_list()
            p_list_data.append(p_list)

            p_list.confno = propid + "-" + to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
            p_list.roomno = res_line.zinr
            p_list.roomrate =  to_decimal(res_line.zipreis)
            p_list.sourcename = sourccod.bezeich
            p_list.market = segment.bezeich
            p_list.note = res_line.bemerk
            p_list.memberno = ""
            p_list.reward = ""
            p_list.profile = propid + "-" + to_string(gmember.gastnr)
            p_list.propid = propid
            p_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1

            if matches(propid,r"*SSRS*"):
                p_list.roomtype = queasy.char1
            else:
                p_list.roomtype = zimkateg.kurzbez
            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                    contcode = substring(str_rsv, 6)
            p_list.ratecode = contcode

            if session_date_format() == ("dmy").lower() :
                rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

            elif session_date_format() == ("mdy").lower() :
                rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
            else:
                rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

            if rsv_date != None:
                p_list.bookdate = to_string(get_year(rsv_date) , "9999") + "-" + to_string(get_month(rsv_date) , "99") + "-" + to_string(get_day(rsv_date) , "99")
            else:
                p_list.bookdate = ""
            p_list.exportdate = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" + to_string(get_day(get_current_date()) , "99")

            if res_line.ankunft == res_line.abreise:
                to_date = res_line.abreise
            else:
                to_date = res_line.abreise - timedelta(days=1)
            for datum1 in date_range(res_line.ankunft,to_date) :
                curr_i = curr_i + 1
                flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, curr_i, datum))
                t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)
                t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                t_others =  to_decimal(t_others) + to_decimal(others)


            p_list.rmrev = to_decimal(round(t_rmrev , 2))
            p_list.fbrev = to_decimal(round(t_fbrev , 2))
            p_list.others = to_decimal(round(t_others , 2))
            p_list.totrev =  to_decimal(p_list.rmrev) + to_decimal(p_list.fbrev) + to_decimal(p_list.others)

            if res_line.ankunft != None:
                ci_date = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
            else:
                ci_date = ""

            if res_line.abreise != None:
                co_date = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
            p_list.arrdate = ci_date
            p_list.depdate = co_date

            gcomp = get_cache (Guest, {"gastnr": [(eq, gmember.master_gastnr)]})

            if gcomp:
                p_list.comp = gcomp.name + ", " + gcomp.anredefirma

    return generate_output()