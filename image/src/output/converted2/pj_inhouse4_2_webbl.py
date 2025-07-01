#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.pj_inhouse4_btn_go_5_cldbl import pj_inhouse4_btn_go_5_cldbl
from models import Queasy, Zimkateg, Paramtext

def pj_inhouse4_2_webbl(sorttype:int, from_date:date, to_date:date, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, disp_accompany:bool, idflag:string, exc_compli:bool):

    prepare_cache ([Queasy, Zimkateg, Paramtext])

    curr_date:date = None
    curr_gastnr:int = 0
    str:string = ""
    htl_no:string = ""
    tdate:string = ""
    crdate:string = ""
    cgdate:string = ""
    counter:int = 0
    company:string = ""
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    inactive:int = 0
    tot_keycard:int = 0
    bemerk:string = ""
    bemerk1:string = ""
    bezeich:string = ""
    tot_qty:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    ct:int = 0
    tmp_rmcat:string = ""
    tmp_nat:string = ""
    tmp_adult:string = ""
    tmp_proz:string = ""
    tmp_child:string = ""
    tmp_flag:string = ""
    tmp_vip:string = ""
    tmp_firstname:string = ""
    tmp_lastname:string = ""
    tmp_birthdate:string = ""
    tmp_groupname:string = ""
    tmp_rmno:string = ""
    tmp_qty:string = ""
    tmp_arrive:string = ""
    tmp_depart:string = ""
    tmp_rmcat_que:string = ""
    tmp_ratecode:string = ""
    tmp_kurzbez:string = ""
    tmp_pax:string = ""
    tmp_nat_que:string = ""
    tmp_nation:string = ""
    tmp_argt:string = ""
    tmp_company:string = ""
    tmp_flight:string = ""
    tmp_etd:string = ""
    tmp_segm:string = ""
    tmp_telefon:string = ""
    tmp_mobil_tel:string = ""
    tmp_created:string = ""
    tmp_createid:string = ""
    tmp_ci_time:string = ""
    tmp_curr:string = ""
    tmp_sob:string = ""
    tmp_memberno:string = ""
    tmp_membertype:string = ""
    tmp_email:string = ""
    tmp_localreg:string = ""
    tmp_c_zipreis:string = ""
    tmp_c_lodging:string = ""
    tmp_c_breakfast:string = ""
    tmp_c_lunch:string = ""
    tmp_c_dinner:string = ""
    tmp_c_otherev:string = ""
    tmp_c_a:string = ""
    tmp_c_c:string = ""
    tmp_c_co:string = ""
    tmp_c_rechnr:string = ""
    tmp_c_resnr:string = ""
    tmp_night:string = ""
    tmp_city:string = ""
    tmp_keycard:string = ""
    tmp_co_time:string = ""
    tmp_pay_art:string = ""
    tmp_zinr_bez:string = ""
    tmp_bezeich:string = ""
    tmp_currency:string = ""
    tmp_segment:string = ""
    tmp_sum_curr:string = ""
    curr_time:int = 0
    queasy = zimkateg = paramtext = None

    inhouse_guest_list = output_list = s_list = zikat_list = t_buff_queasy = summary_roomtype = summary_nation = summary_revenue = summary_segment = summary_list4 = sum_list = tmplist = bqueasy = tqueasy = bufflist = None

    inhouse_guest_list_list, Inhouse_guest_list = create_model("Inhouse_guest_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    output_list_list, Output_list = create_model("Output_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    s_list_list, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})
    t_buff_queasy_list, T_buff_queasy = create_model_like(Queasy)
    summary_roomtype_list, Summary_roomtype = create_model("Summary_roomtype", {"rmcat":string, "bezeich":string, "anz":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_nation_list, Summary_nation = create_model("Summary_nation", {"nat":string, "adult":string, "proz":string, "child":string})
    summary_revenue_list, Summary_revenue = create_model("Summary_revenue", {"currency":string, "room_rate":Decimal, "lodging":Decimal, "b_amount":Decimal, "l_amount":Decimal, "d_amount":Decimal, "o_amount":Decimal})
    summary_segment_list, Summary_segment = create_model("Summary_segment", {"segmcode":int, "segment":string, "anzahl":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    summary_list4_list, Summary_list4 = create_model("Summary_list4", {"argt":string, "rm_qty":int, "pax":int})
    sum_list_list, Sum_list = create_model("Sum_list", {"curr":string, "zipreis":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "other":Decimal})
    tmplist_list, Tmplist = create_model("Tmplist", {"resnr":int, "qty":int, "rmcat":string, "rmno":string, "nation":string, "arrive":date, "depart":date, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "nat":string, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "curr":string, "paym":int, "segm":string, "argt":string})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)
    Bufflist = Output_list
    bufflist_list = output_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, tot_qty, tot_rev, ct, tmp_rmcat, tmp_nat, tmp_adult, tmp_proz, tmp_child, tmp_flag, tmp_vip, tmp_firstname, tmp_lastname, tmp_birthdate, tmp_groupname, tmp_rmno, tmp_qty, tmp_arrive, tmp_depart, tmp_rmcat_que, tmp_ratecode, tmp_kurzbez, tmp_pax, tmp_nat_que, tmp_nation, tmp_argt, tmp_company, tmp_flight, tmp_etd, tmp_segm, tmp_telefon, tmp_mobil_tel, tmp_created, tmp_createid, tmp_ci_time, tmp_curr, tmp_sob, tmp_memberno, tmp_membertype, tmp_email, tmp_localreg, tmp_c_zipreis, tmp_c_lodging, tmp_c_breakfast, tmp_c_lunch, tmp_c_dinner, tmp_c_otherev, tmp_c_a, tmp_c_c, tmp_c_co, tmp_c_rechnr, tmp_c_resnr, tmp_night, tmp_city, tmp_keycard, tmp_co_time, tmp_pay_art, tmp_zinr_bez, tmp_bezeich, tmp_currency, tmp_segment, tmp_sum_curr, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag, exc_compli
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, summary_roomtype, summary_nation, summary_revenue, summary_segment, summary_list4, sum_list, tmplist, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_list, output_list_list, s_list_list, zikat_list_list, t_buff_queasy_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, summary_list4_list, sum_list_list, tmplist_list

        return {}

    def decode_string(in_str:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, tot_qty, tot_rev, ct, tmp_rmcat, tmp_nat, tmp_adult, tmp_proz, tmp_child, tmp_flag, tmp_vip, tmp_firstname, tmp_lastname, tmp_birthdate, tmp_groupname, tmp_rmno, tmp_qty, tmp_arrive, tmp_depart, tmp_rmcat_que, tmp_ratecode, tmp_kurzbez, tmp_pax, tmp_nat_que, tmp_nation, tmp_argt, tmp_company, tmp_flight, tmp_etd, tmp_segm, tmp_telefon, tmp_mobil_tel, tmp_created, tmp_createid, tmp_ci_time, tmp_curr, tmp_sob, tmp_memberno, tmp_membertype, tmp_email, tmp_localreg, tmp_c_zipreis, tmp_c_lodging, tmp_c_breakfast, tmp_c_lunch, tmp_c_dinner, tmp_c_otherev, tmp_c_a, tmp_c_c, tmp_c_co, tmp_c_rechnr, tmp_c_resnr, tmp_night, tmp_city, tmp_keycard, tmp_co_time, tmp_pay_art, tmp_zinr_bez, tmp_bezeich, tmp_currency, tmp_segment, tmp_sum_curr, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag, exc_compli
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, summary_roomtype, summary_nation, summary_revenue, summary_segment, summary_list4, sum_list, tmplist, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_list, output_list_list, s_list_list, zikat_list_list, t_buff_queasy_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, summary_list4_list, sum_list_list, tmplist_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def add_html(pcstring:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, tot_qty, tot_rev, ct, tmp_rmcat, tmp_nat, tmp_adult, tmp_proz, tmp_child, tmp_flag, tmp_vip, tmp_firstname, tmp_lastname, tmp_birthdate, tmp_groupname, tmp_rmno, tmp_qty, tmp_arrive, tmp_depart, tmp_rmcat_que, tmp_ratecode, tmp_kurzbez, tmp_pax, tmp_nat_que, tmp_nation, tmp_argt, tmp_company, tmp_flight, tmp_etd, tmp_segm, tmp_telefon, tmp_mobil_tel, tmp_created, tmp_createid, tmp_ci_time, tmp_curr, tmp_sob, tmp_memberno, tmp_membertype, tmp_email, tmp_localreg, tmp_c_zipreis, tmp_c_lodging, tmp_c_breakfast, tmp_c_lunch, tmp_c_dinner, tmp_c_otherev, tmp_c_a, tmp_c_c, tmp_c_co, tmp_c_rechnr, tmp_c_resnr, tmp_night, tmp_city, tmp_keycard, tmp_co_time, tmp_pay_art, tmp_zinr_bez, tmp_bezeich, tmp_currency, tmp_segment, tmp_sum_curr, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag, exc_compli
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, summary_roomtype, summary_nation, summary_revenue, summary_segment, summary_list4, sum_list, tmplist, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_list, output_list_list, s_list_list, zikat_list_list, t_buff_queasy_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, summary_list4_list, sum_list_list, tmplist_list

        pccleaned = ""
        ihtmltagbegins:int = 0
        ihtmltagends:int = 0
        lhtmltagactive:bool = False
        i:int = 0

        def generate_inner_output():
            return (pccleaned)

        for i in range(1,length(pcstring)  + 1) :

            if lhtmltagactive == False and substring(pcstring, i - 1, 1) == ">":
                ihtmltagbegins = i
                lhtmltagactive = True

            if lhtmltagactive and substring(pcstring, i - 1, 1) == "<":
                ihtmltagends = i
                lhtmltagactive = True
                pcstring = replace_substring(pcstring, i - 1, 1, " " + replace_substring(pcstring, i - 1, 1))
        pccleaned = pcstring

        return generate_inner_output()


    def clean_html(pcstring:string):

        nonlocal curr_date, curr_gastnr, str, htl_no, tdate, crdate, cgdate, counter, company, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, bemerk, bemerk1, bezeich, tot_qty, tot_rev, ct, tmp_rmcat, tmp_nat, tmp_adult, tmp_proz, tmp_child, tmp_flag, tmp_vip, tmp_firstname, tmp_lastname, tmp_birthdate, tmp_groupname, tmp_rmno, tmp_qty, tmp_arrive, tmp_depart, tmp_rmcat_que, tmp_ratecode, tmp_kurzbez, tmp_pax, tmp_nat_que, tmp_nation, tmp_argt, tmp_company, tmp_flight, tmp_etd, tmp_segm, tmp_telefon, tmp_mobil_tel, tmp_created, tmp_createid, tmp_ci_time, tmp_curr, tmp_sob, tmp_memberno, tmp_membertype, tmp_email, tmp_localreg, tmp_c_zipreis, tmp_c_lodging, tmp_c_breakfast, tmp_c_lunch, tmp_c_dinner, tmp_c_otherev, tmp_c_a, tmp_c_c, tmp_c_co, tmp_c_rechnr, tmp_c_resnr, tmp_night, tmp_city, tmp_keycard, tmp_co_time, tmp_pay_art, tmp_zinr_bez, tmp_bezeich, tmp_currency, tmp_segment, tmp_sum_curr, curr_time, queasy, zimkateg, paramtext
        nonlocal sorttype, from_date, to_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, idflag, exc_compli
        nonlocal bqueasy, tqueasy, bufflist


        nonlocal inhouse_guest_list, output_list, s_list, zikat_list, t_buff_queasy, summary_roomtype, summary_nation, summary_revenue, summary_segment, summary_list4, sum_list, tmplist, bqueasy, tqueasy, bufflist
        nonlocal inhouse_guest_list_list, output_list_list, s_list_list, zikat_list_list, t_buff_queasy_list, summary_roomtype_list, summary_nation_list, summary_revenue_list, summary_segment_list, summary_list4_list, sum_list_list, tmplist_list

        pccleaned = ""
        ihtmltagbegins:int = 0
        ihtmltagends:int = 0
        lhtmltagactive:bool = False
        i:int = 0

        def generate_inner_output():
            return (pccleaned)

        for i in range(1,length(pcstring)  + 1) :

            if lhtmltagactive == False and substring(pcstring, i - 1, 1) == "<":
                ihtmltagbegins = i
                lhtmltagactive = True

            if lhtmltagactive and substring(pcstring, i - 1, 1) == ">":
                ihtmltagends = i
                lhtmltagactive = True
                pcstring = replace_substring(pcstring, ihtmltagbegins - 1, ihtmltagends - ihtmltagbegins + 1, fill("|", ihtmltagends - ihtmltagbegins))
        pccleaned = replace_str(pcstring, "|", "")

        return generate_inner_output()


    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Inhouse List"
    queasy.number1 = 1
    queasy.number2 = to_int(idflag)


    pass
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Inhouse List Sum"
    queasy.number1 = 1
    queasy.number2 = to_int(idflag)


    pass
    curr_time = get_current_time_in_seconds()


    curr_date = get_output(htpdate(87))

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg.kurzbez).all():
        zikat_list = Zikat_list()
        zikat_list_list.append(zikat_list)

        zikat_list.zikatnr = zimkateg.zikatnr
        zikat_list.kurzbez = zimkateg.kurzbez
        zikat_list.bezeich = zimkateg.bezeichnung

    for zikat_list in query(zikat_list_list):
        zikat_list.selected = True

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, output_list_list, s_list_list, t_buff_queasy_list = get_output(pj_inhouse4_btn_go_5_cldbl(1, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, "PJ-inhouse2", disp_accompany, exc_compli, zikat_list_list))

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

    sum_list_list.clear()
    summary_roomtype_list.clear()
    summary_nation_list.clear()
    summary_revenue_list.clear()
    summary_segment_list.clear()
    summary_list4_list.clear()

    for output_list in query(output_list_list):

        tmplist = query(tmplist_list, filters=(lambda tmplist: tmplist.resnr == output_list.resnr and tmplist.rmno == output_list.rmno), first=True)

        if not tmplist:
            tmplist = Tmplist()
            tmplist_list.append(tmplist)

            buffer_copy(output_list, tmplist)

    for tmplist in query(tmplist_list, filters=(lambda tmplist: tmplist.rmno.lower()  >= (froom).lower()  and tmplist.rmno.lower()  <= (troom).lower())):

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

        summary_list4 = query(summary_list4_list, filters=(lambda summary_list4: summary_list4.argt == tmplist.argt), first=True)

        if not summary_list4:
            summary_list4 = Summary_list4()
            summary_list4_list.append(summary_list4)

            summary_list4.argt = tmplist.argt


        summary_list4.rm_qty = summary_list4.rm_qty + tmplist.qty
        summary_list4.pax = summary_list4.pax + tmplist.a + tmplist.co

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

    for inhouse_guest_list in query(inhouse_guest_list_list):

        if inhouse_guest_list.bezeich == None:
            bezeich = ""
        else:
            bezeich = inhouse_guest_list.bezeich

        if inhouse_guest_list.bemerk == None:
            bemerk = ""
        else:
            bemerk = inhouse_guest_list.bemerk

        if inhouse_guest_list.bemerk1 == None:
            bemerk1 = ""
        else:
            bemerk1 = inhouse_guest_list.bemerk1
        bezeich = replace_str(bezeich, chr_unicode(10) , "")
        bezeich = replace_str(bezeich, chr_unicode(13) , "")
        bemerk = replace_str(bemerk, chr_unicode(10) , "")
        bemerk = replace_str(bemerk, chr_unicode(13) , "")
        bemerk = replace_str(bemerk, "|", "")
        counter = counter + 1


        bezeich = add_html(bezeich)
        bezeich = clean_html(bezeich)
        bemerk = add_html(bemerk)
        bemerk = clean_html(bemerk)
        bemerk1 = add_html(bemerk1)
        bemerk1 = clean_html(bemerk1)

        if inhouse_guest_list.flag != None:
            tmp_flag = to_string(inhouse_guest_list.flag)
        else:
            tmp_flag = ""

        if inhouse_guest_list.vip != None:
            tmp_vip = inhouse_guest_list.vip
        else:
            tmp_vip = ""

        if inhouse_guest_list.firstname != None:
            tmp_firstname = inhouse_guest_list.firstname
        else:
            tmp_firstname = ""

        if inhouse_guest_list.lastname != None:
            tmp_lastname = inhouse_guest_list.lastname
        else:
            tmp_lastname = ""

        if inhouse_guest_list.birthdate != None:
            tmp_birthdate = inhouse_guest_list.birthdate
        else:
            tmp_birthdate = ""

        if inhouse_guest_list.groupname != None:
            tmp_groupname = inhouse_guest_list.groupname
        else:
            tmp_groupname = ""

        if inhouse_guest_list.rmno != None:
            tmp_rmno = inhouse_guest_list.rmno
        else:
            tmp_rmno = ""

        if inhouse_guest_list.qty != None:
            tmp_qty = to_string(inhouse_guest_list.qty)
        else:
            tmp_qty = ""

        if inhouse_guest_list.arrive != None:
            tmp_arrive = to_string(inhouse_guest_list.arrive)
        else:
            tmp_arrive = ""

        if inhouse_guest_list.depart != None:
            tmp_depart = to_string(inhouse_guest_list.depart)
        else:
            tmp_depart = ""

        if inhouse_guest_list.rmcat != None:
            tmp_rmcat_que = inhouse_guest_list.rmcat
        else:
            tmp_rmcat_que = ""

        if inhouse_guest_list.ratecode != None:
            tmp_ratecode = inhouse_guest_list.ratecode
        else:
            tmp_ratecode = ""

        if inhouse_guest_list.kurzbez != None:
            tmp_kurzbez = inhouse_guest_list.kurzbez
        else:
            tmp_kurzbez = ""

        if inhouse_guest_list.pax != None:
            tmp_pax = inhouse_guest_list.pax
        else:
            tmp_pax = ""

        if inhouse_guest_list.nat != None:
            tmp_nat_que = inhouse_guest_list.nat
        else:
            tmp_nat_que = ""

        if inhouse_guest_list.nation != None:
            tmp_nation = inhouse_guest_list.nation
        else:
            tmp_nation = ""

        if inhouse_guest_list.argt != None:
            tmp_argt = inhouse_guest_list.argt
        else:
            tmp_argt = ""

        if inhouse_guest_list.company != None:
            tmp_company = inhouse_guest_list.company
        else:
            tmp_company = ""

        if inhouse_guest_list.flight != None:
            tmp_flight = inhouse_guest_list.flight
        else:
            tmp_flight = ""

        if inhouse_guest_list.etd != None:
            tmp_etd = inhouse_guest_list.etd
        else:
            tmp_etd = ""

        if inhouse_guest_list.segm != None:
            tmp_segm = inhouse_guest_list.segm
        else:
            tmp_segm = ""

        if inhouse_guest_list.telefon != None:
            tmp_telefon = inhouse_guest_list.telefon
        else:
            tmp_telefon = ""

        if inhouse_guest_list.mobil_tel != None:
            tmp_mobil_tel = inhouse_guest_list.mobil_tel
        else:
            tmp_mobil_tel = ""

        if inhouse_guest_list.created != None:
            tmp_created = to_string(inhouse_guest_list.created)
        else:
            tmp_created = ""

        if inhouse_guest_list.createid != None:
            tmp_createid = inhouse_guest_list.createid
        else:
            tmp_createid = ""

        if inhouse_guest_list.ci_time != None:
            tmp_ci_time = inhouse_guest_list.ci_time
        else:
            tmp_ci_time = ""

        if inhouse_guest_list.curr != None:
            tmp_curr = inhouse_guest_list.curr
        else:
            tmp_curr = ""

        if inhouse_guest_list.sob != None:
            tmp_sob = inhouse_guest_list.sob
        else:
            tmp_sob = ""

        if inhouse_guest_list.memberno != None:
            tmp_memberno = inhouse_guest_list.memberno
        else:
            tmp_memberno = ""

        if inhouse_guest_list.membertype != None:
            tmp_membertype = inhouse_guest_list.membertype
        else:
            tmp_membertype = ""

        if inhouse_guest_list.email != None:
            tmp_email = inhouse_guest_list.email
        else:
            tmp_email = ""

        if inhouse_guest_list.localreg != None:
            tmp_localreg = inhouse_guest_list.localreg
        else:
            tmp_localreg = ""

        if inhouse_guest_list.c_zipreis != None:
            tmp_c_zipreis = inhouse_guest_list.c_zipreis
        else:
            tmp_c_zipreis = ""

        if inhouse_guest_list.c_lodging != None:
            tmp_c_lodging = inhouse_guest_list.c_lodging
        else:
            tmp_c_lodging = ""

        if inhouse_guest_list.c_breakfast != None:
            tmp_c_breakfast = inhouse_guest_list.c_breakfast
        else:
            tmp_c_breakfast = ""

        if inhouse_guest_list.c_lunch != None:
            tmp_c_lunch = inhouse_guest_list.c_lunch
        else:
            tmp_c_lunch = ""

        if inhouse_guest_list.c_dinner != None:
            tmp_c_dinner = inhouse_guest_list.c_dinner
        else:
            tmp_c_dinner = ""

        if inhouse_guest_list.c_otherev != None:
            tmp_c_otherev = inhouse_guest_list.c_otherev
        else:
            tmp_c_otherev = ""

        if inhouse_guest_list.c_a != None:
            tmp_c_a = inhouse_guest_list.c_a
        else:
            tmp_c_a = ""

        if inhouse_guest_list.c_c != None:
            tmp_c_c = inhouse_guest_list.c_c
        else:
            tmp_c_c = ""

        if inhouse_guest_list.c_co != None:
            tmp_c_co = inhouse_guest_list.c_co
        else:
            tmp_c_co = ""

        if inhouse_guest_list.c_rechnr != None:
            tmp_c_rechnr = inhouse_guest_list.c_rechnr
        else:
            tmp_c_rechnr = ""

        if inhouse_guest_list.c_resnr != None:
            tmp_c_resnr = inhouse_guest_list.c_resnr
        else:
            tmp_c_resnr = ""

        if inhouse_guest_list.night != None:
            tmp_night = inhouse_guest_list.night
        else:
            tmp_night = ""

        if inhouse_guest_list.city != None:
            tmp_city = inhouse_guest_list.city
        else:
            tmp_city = ""

        if inhouse_guest_list.keycard != None:
            tmp_keycard = inhouse_guest_list.keycard
        else:
            tmp_keycard = ""

        if inhouse_guest_list.co_time != None:
            tmp_co_time = inhouse_guest_list.co_time
        else:
            tmp_co_time = ""

        if inhouse_guest_list.pay_art != None:
            tmp_pay_art = inhouse_guest_list.pay_art
        else:
            tmp_pay_art = ""

        if inhouse_guest_list.zinr_bez != None:
            tmp_zinr_bez = inhouse_guest_list.zinr_bez
        else:
            tmp_zinr_bez = ""

        if matches(tmp_vip,r"*|*"):
            tmp_vip = replace_str(tmp_vip, "|", "&")
        else:
            tmp_vip = tmp_vip

        if matches(tmp_firstname,r"*|*"):
            tmp_firstname = replace_str(tmp_firstname, "|", "&")
        else:
            tmp_firstname = tmp_firstname

        if matches(tmp_lastname,r"*|*"):
            tmp_lastname = replace_str(tmp_lastname, "|", "&")
        else:
            tmp_lastname = tmp_lastname

        if matches(tmp_groupname,r"*|*"):
            tmp_groupname = replace_str(tmp_groupname, "|", " ")
        else:
            tmp_groupname = tmp_groupname

        if matches(tmp_birthdate,r"*|*"):
            tmp_birthdate = replace_str(tmp_birthdate, "|", " ")
        else:
            tmp_birthdate = tmp_birthdate

        if matches(tmp_rmno,r"*|*"):
            tmp_rmno = replace_str(tmp_rmno, "|", " ")
        else:
            tmp_rmno = tmp_rmno

        if matches(tmp_rmcat_que,r"*|*"):
            tmp_rmcat_que = replace_str(tmp_rmcat_que, "|", " ")
        else:
            tmp_rmcat_que = tmp_rmcat_que

        if matches(tmp_ratecode,r"*|*"):
            tmp_ratecode = replace_str(tmp_ratecode, "|", " ")
        else:
            tmp_ratecode = tmp_ratecode

        if matches(tmp_kurzbez,r"*|*"):
            tmp_kurzbez = replace_str(tmp_kurzbez, "|", " ")
        else:
            tmp_kurzbez = tmp_kurzbez

        if matches(tmp_pax,r"*|*"):
            tmp_pax = replace_str(tmp_pax , "|", " ")
        else:
            tmp_pax = tmp_pax

        if matches(tmp_nat_que,r"*|*"):
            tmp_nat_que = replace_str(tmp_nat_que , "|", " ")
        else:
            tmp_nat_que = tmp_nat_que

        if matches(tmp_nation,r"*|*"):
            tmp_nation = replace_str(tmp_nation , "|", " ")
        else:
            tmp_nation = tmp_nation

        if matches(tmp_argt,r"*|*"):
            tmp_argt = replace_str(tmp_argt , "|", " ")
        else:
            tmp_argt = tmp_argt

        if matches(tmp_company,r"*|*"):
            tmp_company = replace_str(tmp_company , "|", " ")
        else:
            tmp_company = tmp_company

        if matches(tmp_flight,r"*|*"):
            tmp_flight = replace_str(tmp_flight , "|", " ")
        else:
            tmp_flight = tmp_flight

        if matches(tmp_etd,r"*|*"):
            tmp_etd = replace_str(tmp_etd , "|", " ")
        else:
            tmp_etd = tmp_etd

        if matches(tmp_segm,r"*|*"):
            tmp_segm = replace_str(tmp_segm , "|", " ")
        else:
            tmp_segm = tmp_segm

        if matches(tmp_telefon,r"*|*"):
            tmp_telefon = replace_str(tmp_telefon , "|", " ")
        else:
            tmp_telefon = tmp_telefon

        if matches(tmp_mobil_tel,r"*|*"):
            tmp_mobil_tel = replace_str(tmp_mobil_tel , "|", " ")
        else:
            tmp_mobil_tel = tmp_mobil_tel

        if matches(tmp_createid,r"*|*"):
            tmp_createid = replace_str(tmp_createid , "|", " ")
        else:
            tmp_createid = tmp_createid

        if matches(tmp_ci_time,r"*|*"):
            tmp_ci_time = replace_str(tmp_ci_time , "|", " ")
        else:
            tmp_ci_time = tmp_ci_time

        if matches(tmp_curr,r"*|*"):
            tmp_curr = replace_str(tmp_curr , "|", " ")
        else:
            tmp_curr = tmp_curr

        if matches(tmp_sob,r"*|*"):
            tmp_sob = replace_str(tmp_sob , "|", " ")
        else:
            tmp_sob = tmp_sob

        if matches(tmp_memberno,r"*|*"):
            tmp_memberno = replace_str(tmp_memberno , "|", " ")
        else:
            tmp_memberno = tmp_memberno

        if matches(tmp_membertype,r"*|*"):
            tmp_membertype = replace_str(tmp_membertype, "|", " ")
        else:
            tmp_membertype = tmp_membertype

        if matches(tmp_email,r"*|*"):
            tmp_email = replace_str(tmp_email, "|", " ")
        else:
            tmp_email = tmp_email

        if matches(tmp_localreg,r"*|*"):
            tmp_localreg = replace_str(tmp_localreg, "|", " ")
        else:
            tmp_localreg = tmp_localreg

        if matches(tmp_c_zipreis,r"*|*"):
            tmp_c_zipreis = replace_str(tmp_c_zipreis, "|", " ")
        else:
            tmp_c_zipreis = tmp_c_zipreis

        if matches(tmp_c_lodging,r"*|*"):
            tmp_c_lodging = replace_str(tmp_c_lodging, "|", " ")
        else:
            tmp_c_lodging = tmp_c_lodging

        if matches(tmp_c_breakfast,r"*|*"):
            tmp_c_breakfast = replace_str(tmp_c_breakfast, "|", " ")
        else:
            tmp_c_breakfast = tmp_c_breakfast

        if matches(tmp_c_lunch,r"*|*"):
            tmp_c_lunch = replace_str(tmp_c_lunch, "|", " ")
        else:
            tmp_c_lunch = tmp_c_lunch

        if matches(tmp_c_dinner,r"*|*"):
            tmp_c_dinner = replace_str(tmp_c_dinner, "|", " ")
        else:
            tmp_c_dinner = tmp_c_dinner

        if matches(tmp_c_otherev,r"*|*"):
            tmp_c_otherev = replace_str(tmp_c_otherev, "|", " ")
        else:
            tmp_c_otherev = tmp_c_otherev

        if matches(tmp_c_a,r"*|*"):
            tmp_c_a = replace_str(tmp_c_a, "|", " ")
        else:
            tmp_c_a = tmp_c_a

        if matches(tmp_c_c,r"*|*"):
            tmp_c_c = replace_str(tmp_c_c, "|", " ")
        else:
            tmp_c_c = tmp_c_c

        if matches(tmp_c_co,r"*|*"):
            tmp_c_co = replace_str(tmp_c_co, "|", " ")
        else:
            tmp_c_co = tmp_c_co

        if matches(tmp_c_rechnr,r"*|*"):
            tmp_c_rechnr = replace_str(tmp_c_rechnr, "|", " ")
        else:
            tmp_c_rechnr = tmp_c_rechnr

        if matches(tmp_c_resnr,r"*|*"):
            tmp_c_resnr = replace_str(tmp_c_resnr, "|", " ")
        else:
            tmp_c_resnr = tmp_c_resnr

        if matches(tmp_night,r"*|*"):
            tmp_night = replace_str(tmp_night, "|", " ")
        else:
            tmp_night = tmp_night

        if matches(tmp_city,r"*|*"):
            tmp_city = replace_str(tmp_city, "|", " ")
        else:
            tmp_city = tmp_city

        if matches(tmp_keycard,r"*|*"):
            tmp_keycard = replace_str(tmp_keycard, "|", " ")
        else:
            tmp_keycard = tmp_keycard

        if matches(tmp_co_time,r"*|*"):
            tmp_co_time = replace_str(tmp_co_time, "|", " ")
        else:
            tmp_co_time = tmp_co_time

        if matches(tmp_pay_art,r"*|*"):
            tmp_pay_art = replace_str(tmp_pay_art, "|", " ")
        else:
            tmp_pay_art = tmp_pay_art

        if matches(tmp_zinr_bez,r"*|*"):
            tmp_zinr_bez = replace_str(tmp_zinr_bez , "|", " ")
        else:
            tmp_zinr_bez = tmp_zinr_bez

        if matches(tmp_zinr_bez,r"*|*"):
            tmp_zinr_bez = replace_str(tmp_zinr_bez , "|", " ")
        else:
            tmp_zinr_bez = tmp_zinr_bez
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "Inhouse List"
        queasy.number2 = to_int(idflag)
        queasy.char3 = to_string(bezeich) + "|" +\
                to_string(bemerk) + "|" +\
                to_string(bemerk1)
        queasy.char2 = tmp_flag + "|" +\
                to_string(inhouse_guest_list.karteityp) + "|" +\
                to_string(inhouse_guest_list.nr) + "|" +\
                tmp_vip + "|" +\
                to_string(inhouse_guest_list.resnr) + "|" +\
                tmp_firstname + "|" +\
                tmp_lastname + "|" +\
                tmp_birthdate + "|" +\
                tmp_groupname + "|" +\
                tmp_rmno + "|" +\
                tmp_qty + "|" +\
                tmp_arrive + "|" +\
                tmp_depart + "|" +\
                tmp_rmcat_que + "|" +\
                tmp_ratecode + "|" +\
                to_string(inhouse_guest_list.zipreis) + "|" +\
                tmp_kurzbez + "|" +\
                to_string(inhouse_guest_list.a) + "|" +\
                to_string(inhouse_guest_list.c) + "|" +\
                to_string(inhouse_guest_list.co) + "|" +\
                tmp_pax + "|" +\
                tmp_nat_que + "|" +\
                tmp_nation + "|" +\
                tmp_argt + "|" +\
                tmp_company + "|" +\
                tmp_flight + "|" +\
                tmp_etd + "|" +\
                to_string(inhouse_guest_list.paym) + "|" +\
                tmp_segm + "|" +\
                tmp_telefon + "|" +\
                tmp_mobil_tel + "|" +\
                tmp_created + "|" +\
                tmp_createid + "|" +\
                tmp_ci_time + "|" +\
                tmp_curr + "|" +\
                to_string(inhouse_guest_list.inhousedate) + "|" +\
                tmp_sob + "|" +\
                to_string(inhouse_guest_list.gastnr) + "|" +\
                to_string(inhouse_guest_list.lodging) + "|" +\
                to_string(inhouse_guest_list.breakfast) + "|" +\
                to_string(inhouse_guest_list.lunch) + "|" +\
                to_string(inhouse_guest_list.dinner) + "|" +\
                to_string(inhouse_guest_list.otherev) + "|" +\
                to_string(inhouse_guest_list.rechnr) + "|" +\
                tmp_memberno + "|" +\
                tmp_membertype + "|" +\
                tmp_email + "|" +\
                tmp_localreg + "|" +\
                tmp_c_zipreis + "|" +\
                tmp_c_lodging + "|" +\
                tmp_c_breakfast + "|" +\
                tmp_c_lunch + "|" +\
                tmp_c_dinner + "|" +\
                tmp_c_otherev + "|" +\
                tmp_c_a + "|" +\
                tmp_c_c + "|" +\
                tmp_c_co + "|" +\
                tmp_c_rechnr + "|" +\
                tmp_c_resnr + "|" +\
                tmp_night + "|" +\
                tmp_city + "|" +\
                tmp_keycard + "|" +\
                tmp_co_time + "|" +\
                tmp_pay_art + "|" +\
                to_string(inhouse_guest_list.etage) + "|" +\
                tmp_zinr_bez + "|" +\
                to_string(inhouse_guest_list.flag_guest)
        queasy.number1 = counter


        pass

    queasy = get_cache (Queasy, {"key": [(eq, 280)],"char1": [(eq, "inhouse list sum")],"number2": [(eq, to_int(idflag))]})

    if not queasy:

        for summary_roomtype in query(summary_roomtype_list):

            if summary_roomtype.rmcat != None:
                tmp_rmcat = summary_roomtype.rmcat
            else:
                tmp_rmcat = ""

            if summary_roomtype.bezeich != None:
                tmp_bezeich = summary_roomtype.bezeich
            else:
                tmp_bezeich = ""

            if matches(tmp_rmcat,r"*|*"):
                tmp_rmcat = replace_str(tmp_rmcat , "|", " ")
            else:
                tmp_rmcat = tmp_rmcat

            if matches(tmp_bezeich,r"*|*"):
                tmp_bezeich = replace_str(tmp_bezeich, "|", " ")
            else:
                tmp_bezeich = tmp_bezeich
            ct = ct + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "roomtype"
            queasy.char2 = tmp_rmcat + "|" +\
                    tmp_bezeich + "|" +\
                    to_string(summary_roomtype.anz) + "|" +\
                    to_string(summary_roomtype.proz_qty) + "|" +\
                    to_string(summary_roomtype.rev) + "|" +\
                    to_string(summary_roomtype.proz_rev) + "|" +\
                    to_string(summary_roomtype.arr)


        ct = 0

        for summary_nation in query(summary_nation_list):

            if summary_nation.nat != None:
                tmp_nat = summary_nation.nat
            else:
                tmp_nat = ""

            if summary_nation.adult != None:
                tmp_adult = summary_nation.adult
            else:
                tmp_adult = ""

            if summary_nation.proz != None:
                tmp_proz = summary_nation.proz
            else:
                tmp_proz = ""

            if summary_nation.child != None:
                tmp_child = summary_nation.child
            else:
                tmp_child = ""

            if matches(tmp_nat,r"*|*"):
                tmp_nat = replace_str(tmp_nat, "|", "&")
            else:
                tmp_nat = tmp_nat

            if matches(tmp_adult,r"*|*"):
                tmp_adult = replace_str(tmp_adult, "|", "&")
            else:
                tmp_adult = tmp_adult

            if matches(tmp_proz,r"*|*"):
                tmp_proz = replace_str(tmp_proz, "|", "&")
            else:
                tmp_proz = tmp_proz

            if matches(tmp_child,r"*|*"):
                tmp_child = replace_str(tmp_child, "|", "&")
            else:
                tmp_child = tmp_child
            ct = ct + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "nation"
            queasy.char2 = tmp_nat + "|" +\
                    tmp_adult + "|" +\
                    tmp_proz + "|" +\
                    tmp_child


        ct = 0

        for summary_revenue in query(summary_revenue_list):
            ct = ct + 1

            if matches(summary_revenue.currency,r"*|*"):
                tmp_currency = replace_str(summary_revenue.currency, "|", " ")
            else:
                tmp_currency = summary_revenue.currency
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "revenue"
            queasy.char2 = summary_revenue.currency + "|" +\
                    to_string(summary_revenue.room_rate) + "|" +\
                    to_string(summary_revenue.lodging) + "|" +\
                    to_string(summary_revenue.b_amount) + "|" +\
                    to_string(summary_revenue.l_amount) + "|" +\
                    to_string(summary_revenue.d_amount) + "|" +\
                    to_string(summary_revenue.o_amount)


        ct = 0

        for summary_segment in query(summary_segment_list):
            ct = ct + 1

            if matches(summary_segment.segment,r"*|*"):
                tmp_segment = replace_str(summary_segment.segment, "|", " ")
            else:
                tmp_segment = summary_segment.segment
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "segment"
            queasy.char2 = to_string(summary_segment.segmcode) + "|" +\
                    summary_segment.segment + "|" +\
                    to_string(summary_segment.anzahl) + "|" +\
                    to_string(summary_segment.proz_qty) + "|" +\
                    to_string(summary_segment.rev) + "|" +\
                    to_string(summary_segment.proz_rev) + "|" +\
                    to_string(summary_segment.arr)


        ct = 0

        for summary_list4 in query(summary_list4_list):
            ct = ct + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "summary-list4"
            queasy.char2 = summary_list4.argt + "|" +\
                    to_string(summary_list4.rm_qty) + "|" +\
                    to_string(summary_list4.pax)


        ct = 0

        for sum_list in query(sum_list_list):
            ct = ct + 1

            if matches(sum_list.curr,r"*|*"):
                tmp_sum_curr = replace_str(sum_list.curr, "|", " ")
            else:
                tmp_sum_curr = sum_list.curr
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 280
            queasy.char1 = "Inhouse List Sum"
            queasy.number1 = ct
            queasy.number2 = to_int(idflag)
            queasy.char3 = "summary"
            queasy.char2 = sum_list.curr + "|" +\
                    to_string(sum_list.zipreis) + "|" +\
                    to_string(sum_list.lodging) + "|" +\
                    to_string(sum_list.bfast) + "|" +\
                    to_string(sum_list.lunch) + "|" +\
                    to_string(sum_list.dinner) + "|" +\
                    to_string(sum_list.other)

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "inhouse list")],"number2": [(eq, to_int(idflag))]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "inhouse list sum")],"number2": [(eq, to_int(idflag))]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()