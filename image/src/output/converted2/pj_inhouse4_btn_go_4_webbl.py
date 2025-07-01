#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.pj_inhouse4_btn_go_4_cldbl import pj_inhouse4_btn_go_4_cldbl
from models import Queasy, Zimkateg

def pj_inhouse4_btn_go_4_webbl(sorttype:int, from_date:date, to_date:date, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, disp_accompany:bool):

    prepare_cache ([Zimkateg])

    tot_payrm = 0
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    inactive = 0
    tot_keycard = 0
    inhouse_guest_list_list = []
    summary_roomtype_list = []
    summary_nation_list = []
    summary_revenue_list = []
    summary_segment_list = []
    curr_date:date = None
    curr_gastnr:int = 0
    prog_name:string = "PJ-inhouse2"
    tot_qty:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    company:string = ""
    counter:int = 0
    queasy = zimkateg = None

    inhouse_guest_list = output_list = tmplist = company_list = zikat_list = s_list = summary_roomtype = summary_nation = summary_revenue = summary_segment = t_buff_queasy = sum_list = bufflist = None

    inhouse_guest_list_list, Inhouse_guest_list = create_model("Inhouse_guest_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    output_list_list, Output_list = create_model("Output_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    tmplist_list, Tmplist = create_model("Tmplist", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    company_list_list, Company_list = create_model("Company_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})
    s_list_list, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_roomtype_list, Summary_roomtype = create_model("Summary_roomtype", {"rmcat":string, "bezeich":string, "anz":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_nation_list, Summary_nation = create_model("Summary_nation", {"nat":string, "adult":string, "proz":string, "child":string})
    summary_revenue_list, Summary_revenue = create_model("Summary_revenue", {"currency":string, "room_rate":Decimal, "lodging":Decimal, "b_amount":Decimal, "l_amount":Decimal, "d_amount":Decimal, "o_amount":Decimal})
    summary_segment_list, Summary_segment = create_model("Summary_segment", {"segmcode":int, "segment":string, "anzahl":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    t_buff_queasy_list, T_buff_queasy = create_model_like(Queasy)
    sum_list_list, Sum_list = create_model("Sum_list", {"curr":string, "zipreis":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "other":Decimal})

    Bufflist = Output_list
    bufflist_list = output_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, inhouse_guest_list_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, curr_date, curr_gastnr, prog_name, tot_qty, tot_rev, company, counter, queasy, zimkateg
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany
        nonlocal bufflist


        nonlocal inhouse_guest_list, output_list, tmplist, company_list, zikat_list, s_list, summary_roomtype, summary_nation, summary_revenue, summary_segment, t_buff_queasy, sum_list, bufflist
        nonlocal inhouse_guest_list_list, output_list_list, tmplist_list, company_list_list, zikat_list_list, s_list_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, t_buff_queasy_list, sum_list_list

        return {"tot_payrm": tot_payrm, "tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "inactive": inactive, "tot_keycard": tot_keycard, "inhouse-guest-list": inhouse_guest_list_list, "summary-roomtype": summary_roomtype_list, "summary-nation": summary_nation_list, "summary-revenue": summary_revenue_list, "summary-segment": summary_segment_list}

    curr_date = get_output(htpdate(87))

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_list.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    for zikat_list in query(zikat_list_list):
        zikat_list.selected = True
    tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, output_list_list, s_list_list, t_buff_queasy_list = get_output(pj_inhouse4_btn_go_4_cldbl(1, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, "PJ-inhouse2", disp_accompany, zikat_list_list))
    company_list_list.clear()
    sum_list_list.clear()
    inhouse_guest_list_list.clear()
    summary_roomtype_list.clear()
    summary_nation_list.clear()
    summary_revenue_list.clear()
    summary_segment_list.clear()

    for output_list in query(output_list_list, sort_by=[("inhousedate",False)]):

        tmplist = query(tmplist_list, filters=(lambda tmplist: tmplist.resnr == output_list.resnr and tmplist.rmno == output_list.rmno), first=True)

        if not tmplist:
            tmplist = Tmplist()
            tmplist_list.append(tmplist)

            buffer_copy(output_list, tmplist)

    for tmplist in query(tmplist_list, filters=(lambda tmplist: tmplist.rmno.lower()  >= (froom).lower()  and tmplist.rmno.lower()  <= (troom).lower()), sort_by=[("inhousedate",False)]):

        sum_list = query(sum_list_list, filters=(lambda sum_list: sum_list.curr == entry(0, tmplist.curr, ";")), first=True)

        if not sum_list:
            sum_list = Sum_list()
            sum_list_list.append(sum_list)

            sum_list.curr = entry(0, tmplist.curr, ";")


        sum_list.zipreis =  to_decimal(sum_list.zipreis) + to_decimal(tmplist.zipreis)
        sum_list.lodging =  to_decimal(sum_list.lodging) + to_decimal(tmplist.lodging)
        sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(tmplist.breakfast)
        sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(tmplist.lunch)
        sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(tmplist.dinner)
        sum_list.other =  to_decimal(sum_list.other) + to_decimal(tmplist.otherev)

        summary_segment = query(summary_segment_list, filters=(lambda summary_segment: summary_segment.segmcode == tmplist.paym), first=True)

        if not summary_segment:
            summary_segment = Summary_segment()
            summary_segment_list.append(summary_segment)

            summary_segment.segmcode = tmplist.paym
            summary_segment.segment = tmplist.segm


        summary_segment.anzahl = summary_segment.anzahl + tmplist.qty
        summary_segment.rev =  to_decimal(summary_segment.rev) + to_decimal(tmplist.zipreis)
        tot_qty = tot_qty + tmplist.qty
        tot_rev =  to_decimal(tot_rev) + to_decimal(tmplist.zipreis)

    if sorttype == 1 or sorttype == 3:

        if sorttype == 1:

            for output_list in query(output_list_list, sort_by=[("nr",False)]):
                counter = counter + 1
                output_list.nr = counter


                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_list.append(inhouse_guest_list)

                buffer_copy(output_list, inhouse_guest_list)
        else:

            for output_list in query(output_list_list, sort_by=[("etage",False),("rmno",False)]):
                counter = counter + 1
                output_list.nr = counter


                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_list.append(inhouse_guest_list)

                buffer_copy(output_list, inhouse_guest_list)
    else:

        for output_list in query(output_list_list, sort_by=[("company",False)]):

            if company != output_list.company:
                company = output_list.company
                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_list.append(inhouse_guest_list)

                inhouse_guest_list.rmcat = output_list.company

                for bufflist in query(bufflist_list, filters=(lambda bufflist: bufflist.company.lower()  == (company).lower())):
                    counter = counter + 1
                    inhouse_guest_list = Inhouse_guest_list()
                    inhouse_guest_list_list.append(inhouse_guest_list)

                    buffer_copy(bufflist, inhouse_guest_list)
                    inhouse_guest_list.nr = counter
                inhouse_guest_list = Inhouse_guest_list()
                inhouse_guest_list_list.append(inhouse_guest_list)


    for s_list in query(s_list_list, filters=(lambda s_list: s_list.rmcat != "")):
        summary_roomtype = Summary_roomtype()
        summary_roomtype_list.append(summary_roomtype)

        summary_roomtype.bezeich = s_list.bezeich
        summary_roomtype.anz = s_list.anz
        summary_roomtype.proz_qty =  to_decimal(s_list.proz_qty)
        summary_roomtype.rev =  to_decimal(s_list.rev)
        summary_roomtype.proz_rev =  to_decimal(s_list.proz_rev)
        summary_roomtype.arr =  to_decimal(s_list.arr)

    for s_list in query(s_list_list, filters=(lambda s_list: s_list.nat != "")):
        summary_nation = Summary_nation()
        summary_nation_list.append(summary_nation)


        if num_entries(s_list.nat, ";") > 1:
            summary_nation.nat = entry(0, s_list.nat, ";")
        else:
            summary_nation.nat = s_list.nat
        summary_nation.adult = to_string(s_list.adult, ">>>>9")
        summary_nation.proz = to_string(s_list.proz, ">>9.99")
        summary_nation.child = to_string(s_list.child, ">>>>9")


    summary_nation = Summary_nation()
    summary_nation_list.append(summary_nation)

    summary_nation.nat = "T O T A L"
    summary_nation.adult = to_string(tot_a + tot_co, ">>>>9")
    summary_nation.proz = "100.00"
    summary_nation.child = to_string(tot_c, ">>>>9")


    summary_nation = Summary_nation()
    summary_nation_list.append(summary_nation)

    summary_nation = Summary_nation()
    summary_nation_list.append(summary_nation)

    summary_nation.nat = "ROOM AVAILABLE"
    summary_nation.adult = to_string(tot_avail, ">>,>>9")

    if inactive != 0:
        summary_nation = Summary_nation()
        summary_nation_list.append(summary_nation)

        summary_nation.nat = "OCCUPIED/inactive"
        summary_nation.adult = to_string(tot_rm, ">>,>>9") + "/" + to_string(inactive)


    else:
        summary_nation = Summary_nation()
        summary_nation_list.append(summary_nation)

        summary_nation.nat = "T O T A L OCCUPIED"
        summary_nation.adult = to_string(tot_rm, ">>,>>9")


    summary_nation = Summary_nation()
    summary_nation_list.append(summary_nation)

    summary_nation.nat = "AVRG GUEST/ROOM"
    summary_nation.adult = to_string((tot_a + tot_co) / tot_rm, ">>,>>9.99")


    summary_nation = Summary_nation()
    summary_nation_list.append(summary_nation)

    summary_nation.nat = "KEYCARD"
    summary_nation.adult = to_string(tot_keycard, ">>,>>9")

    for sum_list in query(sum_list_list):
        summary_revenue = Summary_revenue()
        summary_revenue_list.append(summary_revenue)

        summary_revenue.currency = sum_list.curr
        summary_revenue.room_rate =  to_decimal(sum_list.zipreis)
        summary_revenue.lodging =  to_decimal(sum_list.lodging)
        summary_revenue.b_amount =  to_decimal(sum_list.bfast)
        summary_revenue.l_amount =  to_decimal(sum_list.lunch)
        summary_revenue.d_amount =  to_decimal(sum_list.dinner)
        summary_revenue.o_amount =  to_decimal(sum_list.other)

    for summary_segment in query(summary_segment_list):
        summary_segment.proz_qty = ( to_decimal(summary_segment.anzahl) / to_decimal(tot_qty)) * to_decimal("100")
        summary_segment.proz_rev = ( to_decimal(summary_segment.rev) / to_decimal(tot_rev)) * to_decimal("100")
        summary_segment.arr = ( to_decimal(summary_segment.rev) / to_decimal(summary_segment.anzahl) )

    return generate_output()