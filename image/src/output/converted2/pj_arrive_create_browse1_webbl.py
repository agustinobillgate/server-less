#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

cl_list_list, Cl_list = create_model("Cl_list", {"ci_id":string, "stat_flag":string, "datum":date, "flag":int, "nr":int, "vip":string, "gastnr":int, "resnr":int, "name":string, "groupname":string, "zimmeranz":int, "rmno":string, "qty":int, "zipreis":string, "arrival":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "stay":int, "segment":string, "rate_code":string, "eta":string, "email":string, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "spreq":string, "memberno":string, "resdate":string, "sob":string, "created_by":string, "ci_time":string, "city":string, "res_stat":int, "res_stat_str":string, "nation2":string, "birthdate":date, "rsv_comment":string, "other_comment":string, "g_comment":string})
s_list_list, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})

def pj_arrive_create_browse1_webbl(tot_rm:int, tot_a:int, tot_c:int, tot_co:int, total_flag:bool, cl_list_list:[Cl_list], s_list_list:[S_list]):
    t_cl_list_list = []
    found:bool = False
    loopi:int = 0
    counter_str:string = ""
    tot_troom:int = 0
    tot_trsv:int = 0
    tot_tadult:int = 0
    tot_tkind:int = 0

    s_list = t_list = cl_list = t_cl_list = None

    t_list_list, T_list = create_model("T_list", {"gastnr":int, "company":string, "counter":string, "int_counter":int, "anzahl":int, "erwachs":int, "kind":int})
    t_cl_list_list, T_cl_list = create_model("T_cl_list", {"ci_id":string, "stat_flag":string, "datum":date, "flag":int, "nr":int, "vip":string, "gastnr":int, "resnr":int, "name":string, "groupname":string, "zimmeranz":int, "rmno":string, "qty":int, "zipreis":string, "arrival":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "stay":int, "segment":string, "rate_code":string, "eta":string, "email":string, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "spreq":string, "memberno":string, "resdate":string, "sob":string, "created_by":string, "ci_time":string, "phonenum":string, "member_typ":string, "repeat_guest":string, "night":int, "city":string, "res_stat":int, "res_stat_str":string, "nation2":string, "birthdate":date, "rsv_comment":string, "other_comment":string, "g_comment":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cl_list_list, found, loopi, counter_str, tot_troom, tot_trsv, tot_tadult, tot_tkind
        nonlocal tot_rm, tot_a, tot_c, tot_co, total_flag


        nonlocal s_list, t_list, cl_list, t_cl_list
        nonlocal t_list_list, t_cl_list_list

        return {"t-cl-list": t_cl_list_list}

    t_cl_list_list.clear()
    t_list_list.clear()

    for cl_list in query(cl_list_list):
        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        buffer_copy(cl_list, t_cl_list)

        if num_entries(cl_list.company, ";") > 1:
            t_cl_list.company = entry(0, cl_list.company, ";")
            t_cl_list.phonenum = entry(1, cl_list.company, ";")


        else:
            t_cl_list.company = cl_list.company

        if num_entries(cl_list.memberno, ";") > 1:
            t_cl_list.member_typ = entry(1, cl_list.memberno, ";")
            t_cl_list.memberno = entry(0, cl_list.memberno, ";")


        else:
            t_cl_list.memberno = cl_list.memberno

        if t_cl_list.stay > 1:
            t_cl_list.repeat_guest = "*"
        t_cl_list.night = date_mdy(cl_list.depart) - date_mdy(cl_list.arrival)


    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list.name = "SUMMARY"
    t_cl_list.memberno = "Room Type"
    t_cl_list.member_typ = "Nation"
    t_cl_list.vip = " Qty"
    t_cl_list.argt = " Adult"
    t_cl_list.rmcat = " (%)"
    t_cl_list.rate_code = " Child"

    for s_list in query(s_list_list):
        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        t_cl_list.memberno = s_list.bezeich
        t_cl_list.member_typ = s_list.nat
        t_cl_list.vip = to_string(s_list.anz, ">>>9")
        t_cl_list.argt = to_string(s_list.adult, " >>>>9")
        t_cl_list.rmcat = to_string(s_list.proz, ">>9.99")
        t_cl_list.rate_code = to_string(s_list.child, " >>>>9")


    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list.memberno = "T O T A L"
    t_cl_list.member_typ = ""
    t_cl_list.vip = to_string(tot_rm, ">>>9")
    t_cl_list.argt = to_string(tot_a + tot_co, " >>>>9")
    t_cl_list.rmcat = "100.00"
    t_cl_list.rate_code = to_string(tot_c, " >>>>9")

    for t_cl_list in query(t_cl_list_list, sort_by=[("datum",False),("nr",False)]):

        if total_flag and t_cl_list.gastnr > 0:

            t_list = query(t_list_list, filters=(lambda t_list: t_list.gastnr == t_cl_list.gastnr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.gastnr = t_cl_list.gastnr
                t_list.company = t_cl_list.company


            t_list.anzahl = t_list.anzahl + t_cl_list.zimmeranz
            t_list.erwachs = t_list.erwachs + t_cl_list.zimmeranz * t_cl_list.a
            t_list.kind = t_list.kind + t_cl_list.zimmeranz * t_cl_list.c


            found = False
            for loopi in range(1,num_entries(t_list.counter, ";")  + 1) :
                counter_str = entry(loopi - 1, t_list.counter, ";")

                if to_int(counter_str) == t_cl_list.resnr:
                    found = True

            if not found:
                t_list.counter = t_list.counter + to_string(t_cl_list.resnr) + ";"

    if total_flag:
        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        t_cl_list.memberno = "Reserve Name"
        t_cl_list.member_typ = " Rooms"
        t_cl_list.argt = " TotRsv"
        t_cl_list.rmcat = " Adult"
        t_cl_list.rate_code = " Child"

        for t_list in query(t_list_list):

            if num_entries(t_list.counter, ";") >= 2:
                t_list.int_counter = num_entries(t_list.counter, ";") - 1
            else:
                t_list.int_counter = 0

        for t_list in query(t_list_list):
            t_cl_list = T_cl_list()
            t_cl_list_list.append(t_cl_list)

            t_cl_list.rmno = "#"
            t_cl_list.memberno = t_list.company
            t_cl_list.member_typ = to_string(t_list.anzahl, " >>>9")
            t_cl_list.argt = to_string(t_list.int_counter, " >>9")
            t_cl_list.rmcat = to_string(t_list.erwachs, " >>9")
            t_cl_list.rate_code = to_string(t_list.kind, " >>9")

        for t_list in query(t_list_list):
            tot_troom = tot_troom + t_list.anzahl
            tot_trsv = tot_trsv + t_list.int_counter
            tot_tadult = tot_tadult + t_list.erwachs
            tot_tkind = tot_tkind + t_list.kind


        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        t_cl_list.rmno = "#"
        t_cl_list.memberno = "T O T A L"
        t_cl_list.member_typ = to_string(tot_troom, " >>>9")
        t_cl_list.argt = to_string(tot_trsv, " >>9")
        t_cl_list.rmcat = to_string(tot_tadult, " >>9")
        t_cl_list.rate_code = to_string(tot_tkind, " >>9")

    return generate_output()