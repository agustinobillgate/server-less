#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.pj_inhouse4_summary_cldbl import pj_inhouse4_summary_cldbl
from models import Queasy, Zimkateg

def pj_inhouse4_summary_webbl(sorttype:int, from_date:date, to_date:date, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, disp_accompany:bool):

    prepare_cache ([Zimkateg])

    tot_payrm = 0
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    inactive = 0
    tot_keycard = 0
    summary_roomtype_data = []
    summary_nation_data = []
    summary_revenue_data = []
    summary_segment_data = []
    curr_date:date = None
    curr_gastnr:int = 0
    prog_name:string = "PJ-inhouse4-summary"
    tot_qty:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    company:string = ""
    counter:int = 0
    queasy = zimkateg = None

    inhouse_guest_list = output_list = tmplist = s_list = summary_roomtype = summary_nation = summary_revenue = summary_segment = t_buff_queasy = sum_list = zikat_list = None

    inhouse_guest_list_data, Inhouse_guest_list = create_model("Inhouse_guest_list", {"resnr":int, "qty":int, "rmcat":string, "rmno":string, "nation":string, "arrive":date, "depart":date, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "nat":string, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "curr":string, "paym":int, "segm":string})
    output_list_data, Output_list = create_model("Output_list", {"resnr":int, "qty":int, "rmcat":string, "rmno":string, "nation":string, "arrive":date, "depart":date, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "nat":string, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "curr":string, "paym":int, "segm":string})
    tmplist_data, Tmplist = create_model("Tmplist", {"resnr":int, "qty":int, "rmcat":string, "rmno":string, "nation":string, "arrive":date, "depart":date, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "nat":string, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "curr":string, "paym":int, "segm":string})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_roomtype_data, Summary_roomtype = create_model("Summary_roomtype", {"rmcat":string, "bezeich":string, "anz":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_nation_data, Summary_nation = create_model("Summary_nation", {"nat":string, "adult":string, "proz":string, "child":string})
    summary_revenue_data, Summary_revenue = create_model("Summary_revenue", {"currency":string, "room_rate":Decimal, "lodging":Decimal, "b_amount":Decimal, "l_amount":Decimal, "d_amount":Decimal, "o_amount":Decimal})
    summary_segment_data, Summary_segment = create_model("Summary_segment", {"segmcode":int, "segment":string, "anzahl":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    t_buff_queasy_data, T_buff_queasy = create_model_like(Queasy)
    sum_list_data, Sum_list = create_model("Sum_list", {"curr":string, "zipreis":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "other":Decimal})
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, curr_date, curr_gastnr, prog_name, tot_qty, tot_rev, company, counter, queasy, zimkateg
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany


        nonlocal inhouse_guest_list, output_list, tmplist, s_list, summary_roomtype, summary_nation, summary_revenue, summary_segment, t_buff_queasy, sum_list, zikat_list
        nonlocal inhouse_guest_list_data, output_list_data, tmplist_data, s_list_data, summary_roomtype_data, summary_nation_data, summary_revenue_data, summary_segment_data, t_buff_queasy_data, sum_list_data, zikat_list_data

        return {"tot_payrm": tot_payrm, "tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "inactive": inactive, "tot_keycard": tot_keycard, "summary-roomtype": summary_roomtype_data, "summary-nation": summary_nation_data, "summary-revenue": summary_revenue_data, "summary-segment": summary_segment_data}


    curr_date = get_output(htpdate(87))

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_data.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    for zikat_list in query(zikat_list_data):
        zikat_list.selected = True
    tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, output_list_data, s_list_data, t_buff_queasy_data = get_output(pj_inhouse4_summary_cldbl(1, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, "PJ-inhouse2", disp_accompany, zikat_list_data))
    sum_list_data.clear()
    inhouse_guest_list_data.clear()
    summary_roomtype_data.clear()
    summary_nation_data.clear()
    summary_revenue_data.clear()
    summary_segment_data.clear()

    for output_list in query(output_list_data):

        tmplist = query(tmplist_data, filters=(lambda tmplist: tmplist.resnr == output_list.resnr and tmplist.rmno == output_list.rmno), first=True)

        if not tmplist:
            tmplist = Tmplist()
            tmplist_data.append(tmplist)

            buffer_copy(output_list, tmplist)

    for tmplist in query(tmplist_data, filters=(lambda tmplist: tmplist.rmno.lower()  >= (froom).lower()  and tmplist.rmno.lower()  <= (troom).lower())):

        sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.curr == entry(0, tmplist.curr, ";")), first=True)

        if not sum_list:
            sum_list = Sum_list()
            sum_list_data.append(sum_list)

            sum_list.curr = entry(0, tmplist.curr, ";")


        sum_list.zipreis =  to_decimal(sum_list.zipreis) + to_decimal(tmplist.zipreis)
        sum_list.lodging =  to_decimal(sum_list.lodging) + to_decimal(tmplist.lodging)
        sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(tmplist.breakfast)
        sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(tmplist.lunch)
        sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(tmplist.dinner)
        sum_list.other =  to_decimal(sum_list.other) + to_decimal(tmplist.otherev)

        summary_segment = query(summary_segment_data, filters=(lambda summary_segment: summary_segment.segmcode == tmplist.paym), first=True)

        if not summary_segment:
            summary_segment = Summary_segment()
            summary_segment_data.append(summary_segment)

            summary_segment.segmcode = tmplist.paym
            summary_segment.segment = tmplist.segm


        summary_segment.anzahl = summary_segment.anzahl + tmplist.qty
        summary_segment.rev =  to_decimal(summary_segment.rev) + to_decimal(tmplist.zipreis)
        tot_qty = tot_qty + tmplist.qty
        tot_rev =  to_decimal(tot_rev) + to_decimal(tmplist.zipreis)

    for s_list in query(s_list_data, filters=(lambda s_list: s_list.rmcat != "")):
        summary_roomtype = Summary_roomtype()
        summary_roomtype_data.append(summary_roomtype)

        summary_roomtype.bezeich = s_list.bezeich
        summary_roomtype.anz = s_list.anz
        summary_roomtype.proz_qty =  to_decimal(s_list.proz_qty)
        summary_roomtype.rev =  to_decimal(s_list.rev)
        summary_roomtype.proz_rev =  to_decimal(s_list.proz_rev)
        summary_roomtype.arr =  to_decimal(s_list.arr)

    for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):
        summary_nation = Summary_nation()
        summary_nation_data.append(summary_nation)


        if num_entries(s_list.nat, ";") > 1:
            summary_nation.nat = entry(0, s_list.nat, ";")
        else:
            summary_nation.nat = s_list.nat
        summary_nation.adult = to_string(s_list.adult, ">>>>9")
        summary_nation.proz = to_string(s_list.proz, ">>9.99")
        summary_nation.child = to_string(s_list.child, ">>>>9")


    summary_nation = Summary_nation()
    summary_nation_data.append(summary_nation)

    summary_nation.nat = "T O T A L"
    summary_nation.adult = to_string(tot_a + tot_co, ">>>>9")
    summary_nation.proz = "100.00"
    summary_nation.child = to_string(tot_c, ">>>>9")


    summary_nation = Summary_nation()
    summary_nation_data.append(summary_nation)

    summary_nation = Summary_nation()
    summary_nation_data.append(summary_nation)

    summary_nation.nat = "ROOM AVAILABLE"
    summary_nation.adult = to_string(tot_avail, ">>,>>9")

    if inactive != 0:
        summary_nation = Summary_nation()
        summary_nation_data.append(summary_nation)

        summary_nation.nat = "OCCUPIED/inactive"
        summary_nation.adult = to_string(tot_rm, ">>,>>9") + "/" + to_string(inactive)


    else:
        summary_nation = Summary_nation()
        summary_nation_data.append(summary_nation)

        summary_nation.nat = "T O T A L OCCUPIED"
        summary_nation.adult = to_string(tot_rm, ">>,>>9")


    summary_nation = Summary_nation()
    summary_nation_data.append(summary_nation)

    summary_nation.nat = "AVRG GUEST/ROOM"
    summary_nation.adult = to_string((tot_a + tot_co) / tot_rm, ">>,>>9.99")


    summary_nation = Summary_nation()
    summary_nation_data.append(summary_nation)

    summary_nation.nat = "KEYCARD"
    summary_nation.adult = to_string(tot_keycard, ">>,>>9")

    for sum_list in query(sum_list_data):
        summary_revenue = Summary_revenue()
        summary_revenue_data.append(summary_revenue)

        summary_revenue.currency = sum_list.curr
        summary_revenue.room_rate =  to_decimal(sum_list.zipreis)
        summary_revenue.lodging =  to_decimal(sum_list.lodging)
        summary_revenue.b_amount =  to_decimal(sum_list.bfast)
        summary_revenue.l_amount =  to_decimal(sum_list.lunch)
        summary_revenue.d_amount =  to_decimal(sum_list.dinner)
        summary_revenue.o_amount =  to_decimal(sum_list.other)

    for summary_segment in query(summary_segment_data):
        summary_segment.proz_qty = ( to_decimal(summary_segment.anzahl) / to_decimal(tot_qty)) * to_decimal("100")
        summary_segment.proz_rev = ( to_decimal(summary_segment.rev) / to_decimal(tot_rev)) * to_decimal("100")
        summary_segment.arr = ( to_decimal(summary_segment.rev) / to_decimal(summary_segment.anzahl) )

    return generate_output()