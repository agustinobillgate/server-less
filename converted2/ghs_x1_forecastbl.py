#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from models import Guest, Reservation, Segment, Sourccod, Zimkateg, Queasy, Res_line

def ghs_x1_forecastbl(datum:date, propid:string):

    prepare_cache ([Guest, Segment, Sourccod, Zimkateg, Queasy, Res_line])

    x_list_data = []
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
    guest = reservation = segment = sourccod = zimkateg = queasy = res_line = None

    x_list = gmember = gcomp = None

    x_list_data, X_list = create_model("X_list", {"confno":string, "arrdate":string, "depdate":string, "roomtype":string, "roomrate":Decimal, "gname":string, "comp":string, "sourcename":string, "memberno":string, "profile":string, "email":string, "totrev":Decimal, "rmrev":Decimal, "fbrev":Decimal, "others":Decimal, "propid":string, "bookdate":string, "market":string, "bookstatus":string, "adult":int, "child":int, "note":string})

    Gmember = create_buffer("Gmember",Guest)
    Gcomp = create_buffer("Gcomp",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal x_list_data, birthdate, str_rsv, contcode, loop_i, curr_i, rsv_date, to_date, datum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, ci_date, co_date, guest, reservation, segment, sourccod, zimkateg, queasy, res_line
        nonlocal datum, propid
        nonlocal gmember, gcomp


        nonlocal x_list, gmember, gcomp
        nonlocal x_list_data

        return {"x-list": x_list_data}

    res_line_obj_list = {}
    for res_line, gmember, reservation, segment, sourccod, zimkateg, queasy in db_session.query(Res_line, Gmember, Reservation, Segment, Sourccod, Zimkateg, Queasy).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Queasy,(Queasy.key == 152) & (Queasy.number1 == Zimkateg.typ)).filter(
             ((Res_line.ankunft <= datum) & (Res_line.abreise >= datum)) | (((Res_line.resstatus == 1) | (Res_line.resstatus == 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 11)) & (Res_line.active_flag == 0))).order_by(Res_line._recid).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        t_rmrev =  to_decimal("0")
        t_fbrev =  to_decimal("0")
        t_others =  to_decimal("0")
        curr_i = 0


        x_list = X_list()
        x_list_data.append(x_list)

        x_list.confno = propid + "-" + to_string(res_line.resnr) + to_string(res_line.reslinnr, "999")
        x_list.roomrate =  to_decimal(res_line.zipreis)
        x_list.sourcename = sourccod.bezeich
        x_list.market = segment.bezeich
        x_list.note = res_line.bemerk
        x_list.memberno = ""
        x_list.profile = propid + "-" + to_string(gmember.gastnr)
        x_list.propid = propid
        x_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1
        x_list.adult = res_line.erwachs
        x_list.child = res_line.kind1 + res_line.kind2

        if matches(propid,r"*SSRS*"):
            x_list.roomtype = queasy.char1
        else:
            x_list.roomtype = zimkateg.kurzbez

        if res_line.resstatus != 9:
            x_list.bookstatus = "BOOKING"

        elif res_line.resstatus == 9 or res_line.resstatus == 10:
            x_list.bookstatus = "CANCEL"

        if session_date_format() == ("dmy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

        elif session_date_format() == ("mdy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
        else:
            rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

        if rsv_date != None:
            x_list.bookdate = to_string(get_year(rsv_date) , "9999") + "-" + to_string(get_month(rsv_date) , "99") + "-" + to_string(get_day(rsv_date) , "99")
        else:
            x_list.bookdate = ""

        if res_line.ankunft == res_line.abreise:
            to_date = res_line.abreise
        else:
            to_date = res_line.abreise - timedelta(days=1)
        for datum1 in date_range(res_line.ankunft,to_date) :
            curr_i = curr_i + 1
            flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, curr_i, datum))
            t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)
            t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch)
            t_others =  to_decimal(t_others) + to_decimal(others)


        x_list.rmrev = to_decimal(round(t_rmrev , 2))
        x_list.fbrev = to_decimal(round(t_fbrev , 2))
        x_list.others = to_decimal(round(t_others , 2))
        x_list.totrev =  to_decimal(x_list.rmrev) + to_decimal(x_list.fbrev) + to_decimal(x_list.others)

        if res_line.ankunft != None:
            ci_date = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" + to_string(get_day(res_line.ankunft) , "99")
        else:
            ci_date = ""

        if res_line.abreise != None:
            co_date = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
        x_list.arrdate = ci_date
        x_list.depdate = co_date

        gcomp = get_cache (Guest, {"gastnr": [(eq, gmember.master_gastnr)]})

        if gcomp:
            x_list.comp = gcomp.name + ", " + gcomp.anredefirma

    return generate_output()