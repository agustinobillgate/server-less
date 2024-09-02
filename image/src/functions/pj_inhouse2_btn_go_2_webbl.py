from functions.additional_functions import *
import decimal
from datetime import date
from functions.pj_inhouse2_btn_go_2bl import pj_inhouse2_btn_go_2bl
from models import Queasy

def pj_inhouse2_btn_go_2_webbl(sorttype:int, datum:date, curr_date:date, curr_gastnr:int, froom:str, troom:str, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, prog_name:str, disp_accompany:bool, disp_exclinact:bool):
    output_list_list = []
    summary_list1_list = []
    summary_list2_list = []
    summary_list3_list = []
    summary_list4_list = []
    lnl_sum_list = []
    t_buff_queasy_list = []
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    tot_rmqty:int = 0
    inactive:int = 0
    curr_company:str = ""
    outnr:int = 0
    queasy = None

    cl_list = s_list = segm_list = argt_list = sum_list = t_buff_queasy = output_list = lnl_sum = summary_list1 = summary_list2 = summary_list3 = summary_list4 = c_list = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "karteityp":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":date, "depart":date, "rmcat":str, "ratecode":str, "zipreis":decimal, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "paym":int, "segm":str, "telefon":str, "mobil_tel":str, "created":date, "createid":str, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "bemerk1":str, "ci_time":str, "curr":str, "spreq":str, "tot_bfast":int, "local_reg":str})
    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int, "rmqty":int})
    segm_list_list, Segm_list = create_model("Segm_list", {"segmcode":int, "segment":str, "anzahl":int})
    argt_list_list, Argt_list = create_model("Argt_list", {"argt":str, "tot_room":int, "tot_pax":int, "tot_breakfast":int})
    sum_list_list, Sum_list = create_model("Sum_list", {"curr":str, "zipreis":decimal})
    t_buff_queasy_list, T_buff_queasy = create_model_like(Queasy)
    output_list_list, Output_list = create_model("Output_list", {"flag":int, "karteityp":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":date, "depart":date, "rmcat":str, "ratecode":str, "zipreis":decimal, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "paym":int, "segm":str, "telefon":str, "mobil_tel":str, "created":date, "createid":str, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "bemerk1":str, "ci_time":str, "curr":str, "spreq":str, "tot_bfast":int, "local_reg":str, "memberno":str, "membertype":str, "email":str, "ac":str, "stay":int})
    lnl_sum_list, Lnl_sum = create_model("Lnl_sum", {"counter":int, "summ":str, "rm_type":str, "qty":str, "nation":str, "rm_qty":str, "adult":str, "percent":str, "child":str})
    summary_list1_list, Summary_list1 = create_model("Summary_list1", {"summ":str, "room_type":str, "qty":str, "nation":str, "rm_qty":str, "adult":str, "percent":str, "child":str})
    summary_list2_list, Summary_list2 = create_model("Summary_list2", {"summ":str, "curr":str, "room_rate":str})
    summary_list3_list, Summary_list3 = create_model("Summary_list3", {"summ":str, "segm_code":str, "rm_qty":str})
    summary_list4_list, Summary_list4 = create_model("Summary_list4", {"summ":str, "argt":str, "rm_qty":str, "pax":str, "bfast":str})

    C_list = Cl_list
    c_list_list = cl_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, summary_list1_list, summary_list2_list, summary_list3_list, summary_list4_list, lnl_sum_list, t_buff_queasy_list, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, curr_company, outnr, queasy
        nonlocal c_list


        nonlocal cl_list, s_list, segm_list, argt_list, sum_list, t_buff_queasy, output_list, lnl_sum, summary_list1, summary_list2, summary_list3, summary_list4, c_list
        nonlocal cl_list_list, s_list_list, segm_list_list, argt_list_list, sum_list_list, t_buff_queasy_list, output_list_list, lnl_sum_list, summary_list1_list, summary_list2_list, summary_list3_list, summary_list4_list
        return {"output-list": output_list_list, "summary-list1": summary_list1_list, "summary-list2": summary_list2_list, "summary-list3": summary_list3_list, "summary-list4": summary_list4_list, "lnl-sum": lnl_sum_list, "t-buff-queasy": t_buff_queasy_list}

    def create_inhouse_v2():

        nonlocal output_list_list, summary_list1_list, summary_list2_list, summary_list3_list, summary_list4_list, lnl_sum_list, t_buff_queasy_list, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, curr_company, outnr, queasy
        nonlocal c_list


        nonlocal cl_list, s_list, segm_list, argt_list, sum_list, t_buff_queasy, output_list, lnl_sum, summary_list1, summary_list2, summary_list3, summary_list4, c_list
        nonlocal cl_list_list, s_list_list, segm_list_list, argt_list_list, sum_list_list, t_buff_queasy_list, output_list_list, lnl_sum_list, summary_list1_list, summary_list2_list, summary_list3_list, summary_list4_list


        tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list = get_output(pj_inhouse2_btn_go_2bl(sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, "PJ_inhouse2", disp_accompany, disp_exclinact))
        C_list = Cl_list
        output_list_list.clear()
        sum_list_list.clear()
        segm_list_list.clear()
        argt_list_list.clear()
        summary_list1_list.clear()
        summary_list2_list.clear()
        summary_list3_list.clear()
        summary_list4_list.clear()
        lnl_sum_list.clear()

        if sorttype == 1:

            for cl_list in query(cl_list_list):
                output_list = Output_list()
                output_list_list.append(output_list)

                buffer_copy(cl_list, output_list)

                if num_entries(cl_list.telefon, ";") > 1:
                    output_list.memberno = trim(to_string(entry(1, cl_list.telefon, ";") , "x(25)"))
                    output_list.telefon = trim(entry(0, cl_list.telefon, ";"))

                if num_entries(cl_list.mobil_tel, ";") > 1:
                    output_list.membertype = trim(to_string(entry(1, cl_list.mobil_tel, ";") , "x(26)"))
                    output_list.mobil_tel = trim(entry(0, cl_list.mobil_tel, ";"))

                if num_entries(cl_list.curr, ";") > 1:
                    output_list.email = to_string(entry(1, cl_list.curr, ";") , "x(40)")
                output_list.ac = to_string(cl_list.a) + "/" + to_string(cl_list.c)

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.curr == entry(0, cl_list.curr, ";")), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.curr = entry(0, cl_list.curr, ";")


                sum_list.zipreis = sum_list.zipreis + cl_list.zipreis

                segm_list = query(segm_list_list, filters=(lambda segm_list :segm_list.segmcode == cl_list.paym), first=True)

                if not segm_list:
                    segm_list = Segm_list()
                    segm_list_list.append(segm_list)

                    segm_list.segmcode = cl_list.paym
                    segm_list.segment = cl_list.segm


                segm_list.anzahl = segm_list.anzahl + cl_list.qty

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argt == cl_list.argt), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_list.append(argt_list)

                    argt_list.argt = cl_list.argt


                argt_list.tot_room = argt_list.tot_room + 1
                argt_list.tot_pax = argt_list.tot_pax + cl_list.a
                argt_list.tot_breakfast = argt_list.tot_breakfast + cl_list.tot_bfast


                output_list.stay = cl_list.depart - cl_list.arrive
        else:

            for cl_list in query(cl_list_list):

                if curr_company != cl_list.company:
                    curr_company = cl_list.company
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.rmno = ""
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.rmno = ""
                    output_list.name = cl_list.company.upper()


                    outnr = 0

                    for c_list in query(c_list_list, filters=(lambda c_list :c_list.company.lower()  == (curr_company).lower())):
                        outnr = outnr + 1
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        buffer_copy(c_list, output_list)
                        output_list.nr = outnr

                        if num_entries(c_list.telefon, ";") > 1:
                            output_list.memberno = trim(to_string(entry(1, c_list.telefon, ";") , "x(25)"))
                            output_list.telefon = trim(entry(0, c_list.telefon, ";"))

                        if num_entries(c_list.mobil_tel, ";") > 1:
                            output_list.membertype = trim(to_string(entry(1, c_list.mobil_tel, ";") , "x(26)"))
                            output_list.mobil_tel = trim(entry(0, c_list.mobil_tel, ";"))

                        if num_entries(c_list.curr, ";") > 1:
                            output_list.email = to_string(entry(1, c_list.curr, ";") , "x(40)")
                        output_list.ac = to_string(c_list.a) + "/" + to_string(c_list.c)

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.curr == entry(0, cl_list.curr, ";")), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.curr = entry(0, cl_list.curr, ";")


                sum_list.zipreis = sum_list.zipreis + cl_list.zipreis

                segm_list = query(segm_list_list, filters=(lambda segm_list :segm_list.segmcode == cl_list.paym), first=True)

                if not segm_list:
                    segm_list = Segm_list()
                    segm_list_list.append(segm_list)

                    segm_list.segmcode = cl_list.paym
                    segm_list.segment = cl_list.segm


                segm_list.anzahl = segm_list.anzahl + cl_list.qty

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argt == cl_list.argt), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_list.append(argt_list)

                    argt_list.argt = cl_list.argt


                argt_list.tot_room = argt_list.tot_room + 1
                argt_list.tot_pax = argt_list.tot_pax + cl_list.a
                argt_list.tot_breakfast = argt_list.tot_breakfast + cl_list.tot_bfast


                output_list.stay = cl_list.depart - cl_list.arrive

        for s_list in query(s_list_list):
            summary_list1 = Summary_list1()
            summary_list1_list.append(summary_list1)

            summary_list1.summ = ""
            summary_list1.room_type = s_list.bezeich
            summary_list1.qty = to_string(s_list.anz, ">>>>>")
            summary_list1.nation = trim(s_list.nat)
            summary_list1.rm_qty = to_string(s_list.rmqty, ">>>>9")
            summary_list1.adult = to_string(s_list.adult, ">>>>9")
            summary_list1.percent = to_string(s_list.proz, ">>9.99")
            summary_list1.child = to_string(s_list.child, ">>>>9")


        summary_list1 = Summary_list1()
        summary_list1_list.append(summary_list1)

        summary_list1 = Summary_list1()
        summary_list1_list.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "ROOM AVAILABLE"
        summary_list1.qty = to_string(tot_avail, ">>>>9")

        if inactive != 0:
            summary_list1 = Summary_list1()
            summary_list1_list.append(summary_list1)

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
            summary_list1_list.append(summary_list1)

            summary_list1.summ = ""
            summary_list1.room_type = "T O T A L  OCCUPIED"
            summary_list1.qty = to_string(tot_rm, ">>>>9")
            summary_list1.nation = ""
            summary_list1.rm_qty = to_string(tot_rmqty, ">>>>9")
            summary_list1.adult = to_string(tot_a + tot_co, ">>>>9")
            summary_list1.percent = "100.00"
            summary_list1.child = to_string(tot_c, ">>>>9")


        summary_list1 = Summary_list1()
        summary_list1_list.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "IN PERCENTAGE (%)"
        summary_list1.qty = to_string(tot_rm / tot_avail * 100, ">>9.99")
        summary_list1.nation = "AVRG GUEST/ROOM"
        summary_list1.rm_qty = to_string((tot_a + tot_co) / tot_rm, ">>9.99")


        summary_list1 = Summary_list1()
        summary_list1_list.append(summary_list1)

        summary_list1.summ = ""
        summary_list1.room_type = "OCC. PAYING ROOMS"
        summary_list1.qty = to_string(tot_payrm / tot_avail * 100, ">>9.99") + " %"

        for sum_list in query(sum_list_list):
            summary_list2 = Summary_list2()
            summary_list2_list.append(summary_list2)

            summary_list2.summ = ""
            summary_list2.curr = to_string(sum_list.curr, "x(15)")
            summary_list2.room_rate = to_string(sum_list.zipreis, "->,>>>,>>>,>>9.99")

        for segm_list in query(segm_list_list):
            summary_list3 = Summary_list3()
            summary_list3_list.append(summary_list3)

            summary_list3.summ = ""
            summary_list3.segm_code = segm_list.segment
            summary_list3.rm_qty = to_string(segm_list.anzahl, ">>>>9")

        for argt_list in query(argt_list_list):
            summary_list4 = Summary_list4()
            summary_list4_list.append(summary_list4)

            summary_list4.summ = ""
            summary_list4.argt = to_string(argt_list.argt, "x(15)")
            summary_list4.rm_qty = to_string(argt_list.tot_room, ">>>>>9")
            summary_list4.pax = to_string(argt_list.tot_pax, ">>>>>9")
            summary_list4.bfast = to_string(argt_list.tot_breakfast, ">>>>9")

    create_inhouse_v2()

    return generate_output()