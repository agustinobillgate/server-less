#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "outstand":Decimal, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "email":string, "email_adr":string, "tot_night":int, "ratecode":string, "full_name":string, "address":string, "memberno":string, "membertype":string})
s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})

def pj_depart_create_browse_webbl(tot_rm:int, tot_a:int, tot_c:int, tot_co:int, cl_list_data:[Cl_list], s_list_data:[S_list]):
    t_cl_list_data = []

    s_list = cl_list = t_cl_list = None

    t_cl_list_data, T_cl_list = create_model("T_cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "outstand":Decimal, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "email":string, "email_adr":string, "tot_night":int, "ratecode":string, "full_name":string, "address":string, "memberno":string, "membertype":string, "phonenum":string, "str_outstand":string, "night":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cl_list_data
        nonlocal tot_rm, tot_a, tot_c, tot_co


        nonlocal s_list, cl_list, t_cl_list
        nonlocal t_cl_list_data

        return {"t-cl-list": t_cl_list_data}


    t_cl_list_data.clear()

    for cl_list in query(cl_list_data):
        t_cl_list = T_cl_list()
        t_cl_list_data.append(t_cl_list)

        buffer_copy(cl_list, t_cl_list)

        if num_entries(cl_list.company, ";") > 1:
            t_cl_list.company = entry(0, cl_list.company, ";")
            t_cl_list.phonenum = entry(1, cl_list.company, ";")


        else:
            t_cl_list.company = cl_list.company
        t_cl_list.str_outstand = to_string(cl_list.outstand, "->>>,>>>,>>9.99")
        t_cl_list.night = date_mdy(cl_list.depart) - date_mdy(cl_list.arrive)
    t_cl_list = T_cl_list()
    t_cl_list_data.append(t_cl_list)

    t_cl_list = T_cl_list()
    t_cl_list_data.append(t_cl_list)

    t_cl_list.name = "SUMMARY"
    t_cl_list.memberno = "Room Type"
    t_cl_list.membertype = "Nation"
    t_cl_list.vip = " Qty"
    t_cl_list.rmcat = " Adult"
    t_cl_list.ratecode = " (%)"
    t_cl_list.pax = " Child"

    for s_list in query(s_list_data):
        t_cl_list = T_cl_list()
        t_cl_list_data.append(t_cl_list)

        t_cl_list.memberno = s_list.bezeich
        t_cl_list.membertype = s_list.nat
        t_cl_list.vip = to_string(s_list.anz, ">>>9")
        t_cl_list.rmcat = to_string(s_list.adult, ">>,>>9")
        t_cl_list.ratecode = to_string(s_list.proz, " >>9.99")
        t_cl_list.pax = to_string(s_list.child, ">>,>>9")


    t_cl_list = T_cl_list()
    t_cl_list_data.append(t_cl_list)

    t_cl_list = T_cl_list()
    t_cl_list_data.append(t_cl_list)

    t_cl_list.memberno = "T O T A L"
    t_cl_list.membertype = ""
    t_cl_list.vip = to_string(tot_rm, ">>>9")
    t_cl_list.rmcat = to_string(tot_a + tot_co, ">>,>>9")
    t_cl_list.ratecode = " 100.00"
    t_cl_list.pax = to_string(tot_c, ">>,>>9")

    return generate_output()