#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/8/2025
# pembagi nol
# beda sorting, 
# 1/9/22025 kolom kosong
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.pj_inhouse2_btn_go_4_cldbl import pj_inhouse2_btn_go_4_cldbl
from models import Queasy

def safe_divide(numerator, denominator):
    numerator, denominator = to_decimal(numerator), to_decimal(denominator)
    return (numerator / denominator) if denominator not in (0, None) else to_decimal("0")

def pj_inhouse2_btn_go_4_webbl(sorttype:int, datum:date, curr_date:date, curr_gastnr:int, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, prog_name:string, disp_accompany:bool, disp_exclinact:bool, split_rsv_print:bool, exc_compli:bool):
    output_list_data = []
    summary_list1_data = []
    summary_list2_data = []
    summary_list3_data = []
    summary_list4_data = []
    lnl_sum_data = []
    t_buff_queasy_data = []
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    tot_rmqty:int = 0
    inactive:int = 0
    curr_company:string = ""
    outnr:int = 0
    query_string:string = ""
    queasy = None

    froom = froom.strip()

    cl_list = s_list = segm_list = argt_list = sum_list = t_buff_queasy = output_list = lnl_sum = summary_list1 = summary_list2 = summary_list3 = summary_list4 = c_list = None

    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "bemerk1":string, "ci_time":string, "curr":string, "spreq":string, "tot_bfast":int, "local_reg":string, "rsv_comment":string, "other_comment":string, "g_comment":string, "zinr_bez":string, "flag_guest":int, "etage":int, "birthdate":date})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "rmqty":int})
    segm_list_data, Segm_list = create_model("Segm_list", {"segmcode":int, "segment":string, "anzahl":int})
    argt_list_data, Argt_list = create_model("Argt_list", {"argt":string, "tot_room":int, "tot_pax":int, "tot_breakfast":int})
    sum_list_data, Sum_list = create_model("Sum_list", {"curr":string, "zipreis":Decimal})
    t_buff_queasy_data, T_buff_queasy = create_model_like(Queasy)
    output_list_data, Output_list = create_model("Output_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "bemerk1":string, "ci_time":string, "curr":string, "spreq":string, "tot_bfast":int, "local_reg":string, "memberno":string, "membertype":string, "email":string, "ac":string, "stay":int, "rsv_comment":string, "other_comment":string, "g_comment":string, "zinr_bez":string, "flag_guest":int, "etage":int, "birthdate":date})
    lnl_sum_data, Lnl_sum = create_model("Lnl_sum", {"counter":int, "summ":string, "rm_type":string, "qty":string, "nation":string, "rm_qty":string, "adult":string, "percent":string, "child":string})
    summary_list1_data, Summary_list1 = create_model("Summary_list1", {"summ":string, "room_type":string, "qty":string, "nation":string, "rm_qty":string, "adult":string, "percent":string, "child":string})
    summary_list2_data, Summary_list2 = create_model("Summary_list2", {"summ":string, "curr":string, "room_rate":string})
    summary_list3_data, Summary_list3 = create_model("Summary_list3", {"summ":string, "segm_code":string, "rm_qty":string})
    summary_list4_data, Summary_list4 = create_model("Summary_list4", {"summ":string, "argt":string, "rm_qty":string, "pax":string, "bfast":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data, lnl_sum_data, t_buff_queasy_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, curr_company, outnr, query_string, queasy
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal cl_list, s_list, segm_list, argt_list, sum_list, t_buff_queasy, output_list, lnl_sum, summary_list1, summary_list2, summary_list3, summary_list4, c_list
        nonlocal cl_list_data, s_list_data, segm_list_data, argt_list_data, sum_list_data, t_buff_queasy_data, output_list_data, lnl_sum_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data
        # print("Sorttype:", sorttype)
        # for rec in output_list_data:
        #     print(rec.rmno)
        return {"output-list": output_list_data, "summary-list1": summary_list1_data, "summary-list2": summary_list2_data, "summary-list3": summary_list3_data, "summary-list4": summary_list4_data, "lnl-sum": lnl_sum_data, "t-buff-queasy": t_buff_queasy_data}

    def create_inhouse_v2():

        nonlocal output_list_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data, lnl_sum_data, t_buff_queasy_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, curr_company, outnr, query_string, queasy
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal cl_list, s_list, segm_list, argt_list, sum_list, t_buff_queasy, output_list, lnl_sum, summary_list1, summary_list2, summary_list3, summary_list4, c_list
        nonlocal cl_list_data, s_list_data, segm_list_data, argt_list_data, sum_list_data, t_buff_queasy_data, output_list_data, lnl_sum_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data

        prog_name:string = ""
        prog_name = "PJ-inhouse2"
        tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data = get_output(pj_inhouse2_btn_go_4_cldbl(sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli))
        C_list = Cl_list
        c_list_data = cl_list_data
        output_list_data.clear()
        sum_list_data.clear()
        segm_list_data.clear()
        argt_list_data.clear()
        summary_list1_data.clear()
        summary_list2_data.clear()
        summary_list3_data.clear()
        summary_list4_data.clear()
        lnl_sum_data.clear()

        if sorttype == 1 or sorttype == 3:
            outnr = 0

            if sorttype == 1:

                for cl_list in query(cl_list_data):
                    create_outlist()


            elif sorttype == 3:

                for cl_list in query(cl_list_data, sort_by=[("etage",False),("rmno",False)]):
                    create_outlist()

        else:
            for cl_list in query(cl_list_data, sort_by=[("company",False)]):

                if curr_company != cl_list.company:
                    curr_company = cl_list.company
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.rmno = ""
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.rmno = ""
                    output_list.name = cl_list.company.upper()


                    outnr = 0

                    for c_list in query(c_list_data, filters=(lambda c_list: c_list.company  == curr_company)):
                        outnr = outnr + 1
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        buffer_copy(c_list, output_list)
                        output_list.nr = outnr

                        if num_entries(c_list.telefon, ";") > 1:
                            output_list.memberno = trim(to_string(entry(1, c_list.telefon, ";") , "x(25)"))
                            output_list.telefon = trim(entry(0, c_list.telefon, ";"))

                        if num_entries(c_list.mobil_tel, ";") > 1:
                            output_list.membertype = trim(to_string(entry(1, c_list.mobil_tel, ";") , "x(26)"))
                            output_list.mobil_tel = trim(entry(0, c_list.mobil_tel, ";"))

                        if num_entries(c_list.curr, ";") > 1:
                            # print("c_list.curr:", c_list.curr)
                            output_list.email = to_string(entry(1, c_list.curr, ";") , "x(40)")
                        output_list.ac = to_string(c_list.a) + "/" + to_string(c_list.c)

                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.curr == entry(0, cl_list.curr, ";")), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.curr = entry(0, cl_list.curr, ";")


                sum_list.zipreis =  to_decimal(sum_list.zipreis) + to_decimal(cl_list.zipreis)

                segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segmcode == cl_list.paym), first=True)

                if not segm_list:
                    segm_list = Segm_list()
                    segm_list_data.append(segm_list)

                    segm_list.segmcode = cl_list.paym
                    segm_list.segment = cl_list.segm


                segm_list.anzahl = segm_list.anzahl + cl_list.qty

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == cl_list.argt), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_data.append(argt_list)

                    argt_list.argt = cl_list.argt


                argt_list.tot_room = argt_list.tot_room + 1
                argt_list.tot_pax = argt_list.tot_pax + cl_list.a + cl_list.co
                argt_list.tot_breakfast = argt_list.tot_breakfast + cl_list.tot_bfast


                output_list.stay = (cl_list.depart - cl_list.arrive).days


        for s_list in query(s_list_data):
            summary_list1 = Summary_list1()
            summary_list1_data.append(summary_list1)

            summary_list1.summ = ""
            summary_list1.room_type = s_list.bezeich
            summary_list1.qty = to_string(s_list.anz, ">>>>>")
            summary_list1.nation = trim(s_list.nat)
            summary_list1.rm_qty = to_string(s_list.rmqty, ">>>>9")
            summary_list1.adult = to_string(s_list.adult, ">>>>9")
            summary_list1.percent = to_string(s_list.proz, ">>9.99")
            summary_list1.child = to_string(s_list.child, ">>>>9")


        summary_list1 = Summary_list1()
        summary_list1_data.append(summary_list1)

        summary_list1 = Summary_list1()
        summary_list1_data.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "ROOM AVAILABLE"
        summary_list1.qty = to_string(tot_avail, ">>>>9")

        if inactive != 0:
            summary_list1 = Summary_list1()
            summary_list1_data.append(summary_list1)

            summary_list1.summ = ""
            summary_list1.room_type = "OCCUPIED/inactive"
            summary_list1.qty = to_string(tot_rm, ">>>>9") + "/" + to_string(inactive)
            summary_list1.nation = ""
            summary_list1.rm_qty = to_string(tot_rmqty, ">>>>9")
            summary_list1.adult = to_string(tot_a + tot_co, ">>>>9")
            summary_list1.percent = "100.00"
            summary_list1.child = to_string(tot_c, ">>>>9")
        else:
            summary_list1 = Summary_list1()
            summary_list1_data.append(summary_list1)

            summary_list1.summ = ""
            summary_list1.room_type = "TOTAL OCCUPIED"
            summary_list1.qty = to_string(tot_rm, ">>>>9")
            summary_list1.nation = ""
            summary_list1.rm_qty = to_string(tot_rmqty, ">>>>9")
            summary_list1.adult = to_string(tot_a + tot_co, ">>>>9")
            summary_list1.percent = "100.00"
            summary_list1.child = to_string(tot_c, ">>>>9")


        summary_list1 = Summary_list1()
        summary_list1_data.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "TOTAL OCCUPIED (%)"

        # Rd 20/8/2025
        # summary_list1.qty = to_string(tot_rm / tot_avail * 100, "->>9.99")
        summary_list1.qty = to_string(safe_divide(tot_rm , tot_avail) * 100, "->>9.99")
        summary_list1.nation = "AVRG GUEST/ROOM"
        # Rd 20/8/2025
        # summary_list1.rm_qty = to_string((tot_a + tot_co) / tot_rm, ">>9.99")
        summary_list1.rm_qty = to_string(safe_divide((tot_a + tot_co) , tot_rm), ">>9.99")


        summary_list1 = Summary_list1()
        summary_list1_data.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "OCC. PAYING ROOMS"
        summary_list1.qty = to_string(tot_payrm)


        summary_list1 = Summary_list1()
        summary_list1_data.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "OCC. PAYING ROOMS (%)"
        # summary_list1.qty = to_string(tot_payrm / tot_avail * 100, "->>9.99")
        summary_list1.qty = to_string(safe_divide(tot_payrm , tot_avail) * 100, "->>9.99")

        for sum_list in query(sum_list_data):
            summary_list2 = Summary_list2()
            summary_list2_data.append(summary_list2)

            summary_list2.summ = ""
            summary_list2.curr = to_string(sum_list.curr, "x(15)")
            summary_list2.room_rate = to_string(sum_list.zipreis, "->,>>>,>>>,>>9.99")

        for segm_list in query(segm_list_data):
            summary_list3 = Summary_list3()
            summary_list3_data.append(summary_list3)

            summary_list3.summ = ""
            summary_list3.segm_code = segm_list.segment
            summary_list3.rm_qty = to_string(segm_list.anzahl, ">>>>9")

        for argt_list in query(argt_list_data):
            summary_list4 = Summary_list4()
            summary_list4_data.append(summary_list4)

            summary_list4.summ = ""
            summary_list4.argt = to_string(argt_list.argt, "x(15)")
            summary_list4.rm_qty = to_string(argt_list.tot_room, ">>>>>9")
            summary_list4.pax = to_string(argt_list.tot_pax, ">>>>>9")
            summary_list4.bfast = to_string(argt_list.tot_breakfast, ">>>>9")


    def create_outlist():

        nonlocal output_list_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data, lnl_sum_data, t_buff_queasy_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, curr_company, outnr, query_string, queasy
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal cl_list, s_list, segm_list, argt_list, sum_list, t_buff_queasy, output_list, lnl_sum, summary_list1, summary_list2, summary_list3, summary_list4, c_list
        nonlocal cl_list_data, s_list_data, segm_list_data, argt_list_data, sum_list_data, t_buff_queasy_data, output_list_data, lnl_sum_data, summary_list1_data, summary_list2_data, summary_list3_data, summary_list4_data


        outnr = outnr + 1
        output_list = Output_list()
        output_list_data.append(output_list)

        buffer_copy(cl_list, output_list)
        output_list.nr = outnr

        if num_entries(cl_list.telefon, ";") > 1:
            output_list.memberno = trim(to_string(entry(1, cl_list.telefon, ";") , "x(25)"))
            output_list.telefon = trim(entry(0, cl_list.telefon, ";"))

        if num_entries(cl_list.mobil_tel, ";") > 1:
            output_list.membertype = trim(to_string(entry(1, cl_list.mobil_tel, ";") , "x(26)"))
            output_list.mobil_tel = trim(entry(0, cl_list.mobil_tel, ";"))

        if num_entries(cl_list.curr, ";") > 1:
            # print("c_list.curr:", c_list.curr)
            output_list.email = to_string(entry(1, cl_list.curr, ";") , "x(40)")
        output_list.ac = to_string(cl_list.a) + "/" + to_string(cl_list.c)

        sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.curr == entry(0, cl_list.curr, ";")), first=True)

        if not sum_list:
            sum_list = Sum_list()
            sum_list_data.append(sum_list)

            sum_list.curr = entry(0, cl_list.curr, ";")


        sum_list.zipreis =  to_decimal(sum_list.zipreis) + to_decimal(cl_list.zipreis)

        segm_list = query(segm_list_data, filters=(lambda segm_list: segm_list.segmcode == cl_list.paym), first=True)

        if not segm_list:
            segm_list = Segm_list()
            segm_list_data.append(segm_list)

            segm_list.segmcode = cl_list.paym
            segm_list.segment = cl_list.segm


        segm_list.anzahl = segm_list.anzahl + cl_list.qty

        argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == cl_list.argt), first=True)

        if not argt_list:
            argt_list = Argt_list()
            argt_list_data.append(argt_list)

            argt_list.argt = cl_list.argt


        argt_list.tot_room = argt_list.tot_room + 1
        argt_list.tot_pax = argt_list.tot_pax + cl_list.a + cl_list.co
        argt_list.tot_breakfast = argt_list.tot_breakfast + cl_list.tot_bfast
        output_list.stay = (cl_list.depart - cl_list.arrive).days

    if datum is None or curr_date is None:
        return generate_output()
    
    create_inhouse_v2()

    return generate_output()