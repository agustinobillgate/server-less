#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reservation, Zimkateg, Res_line

def rm_revenue_fcast_detail_webbl(t_date:date, f_date:date, room:string):

    prepare_cache ([Reservation, Zimkateg, Res_line])

    res_detail_list = []
    reservation = zimkateg = res_line = None

    res_detail = None

    res_detail_list, Res_detail = create_model("Res_detail", {"guest_name":string, "arrival":date, "departure":date, "arr_time":string, "room_type":string, "room_number":string, "room_rate":Decimal, "room_qty":int, "argt_code":string, "res_number":int, "turnover":Decimal, "art_number":int, "segment_code":int, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_detail_list, reservation, zimkateg, res_line
        nonlocal t_date, f_date, room


        nonlocal res_detail
        nonlocal res_detail_list

        return {"res-detail": res_detail_list}

    res_line_obj_list = {}
    res_line = Res_line()
    reservation = Reservation()
    zimkateg = Zimkateg()
    for res_line.name, res_line.ankunft, res_line.abreise, res_line.ankzeit, res_line.zinr, res_line.zipreis, res_line.zimmeranz, res_line.arrangement, res_line.resnr, res_line.bemerk, res_line._recid, reservation.segmentcode, reservation._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.ankzeit, Res_line.zinr, Res_line.zipreis, Res_line.zimmeranz, Res_line.arrangement, Res_line.resnr, Res_line.bemerk, Res_line._recid, Reservation.segmentcode, Reservation._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
             ((Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr == (room).lower()) & (Res_line.zipreis != 0)).order_by(Res_line.name).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        res_detail = Res_detail()
        res_detail_list.append(res_detail)

        res_detail.guest_name = res_line.name
        res_detail.arrival = res_line.ankunft
        res_detail.departure = res_line.abreise
        res_detail.arr_time = to_string(res_line.ankzeit, "HH:MM")
        res_detail.room_type = zimkateg.kurzbez
        res_detail.room_number = res_line.zinr
        res_detail.room_rate =  to_decimal(res_line.zipreis)
        res_detail.room_qty = res_line.zimmeranz
        res_detail.argt_code = res_line.arrangement
        res_detail.res_number = res_line.resnr
        res_detail.segment_code = reservation.segmentcode
        res_detail.remark = res_line.bemerk


        res_detail.remark = replace_str(res_detail.remark, chr_unicode(10) , "")
        res_detail.remark = replace_str(res_detail.remark, chr_unicode(13) , "")
        res_detail.remark = replace_str(res_detail.remark, "~n", "")
        res_detail.remark = replace_str(res_detail.remark, "\\n", "")
        res_detail.remark = replace_str(res_detail.remark, "~r", "")
        res_detail.remark = replace_str(res_detail.remark, "~r~n", "")
        res_detail.remark = replace_str(res_detail.remark, "&nbsp;", " ")
        res_detail.remark = replace_str(res_detail.remark, "</p>", "</p></p>")
        res_detail.remark = replace_str(res_detail.remark, "</p>", chr_unicode(13))
        res_detail.remark = replace_str(res_detail.remark, "<BR>", chr_unicode(13))
        res_detail.remark = replace_str(res_detail.remark, chr_unicode(10) + chr_unicode(13) , "")
        res_detail.remark = replace_str(res_detail.remark, chr_unicode(2) , "")
        res_detail.remark = replace_str(res_detail.remark, chr_unicode(3) , "")
        res_detail.remark = replace_str(res_detail.remark, chr_unicode(4) , "")

        if length(res_detail.remark) < 3:
            res_detail.remark = replace_str(res_detail.remark, chr_unicode(32) , "")

        if length(res_detail.remark) < 3:
            res_detail.remark = ""

        if length(res_detail.remark) == None:
            res_detail.remark = ""

    return generate_output()