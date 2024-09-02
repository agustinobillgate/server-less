from functions.additional_functions import *
import decimal

def pj_depart_create_browse_webbl(tot_rm:int, tot_a:int, tot_c:int, tot_co:int, cl_list:[Cl_list], s_list:[S_list]):
    t_cl_list_list = []

    s_list = cl_list = t_cl_list = None

    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":str, "depart":str, "rmcat":str, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "outstand":decimal, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "email":str, "email_adr":str, "tot_night":int, "ratecode":str, "full_name":str, "address":str, "memberno":str, "membertype":str})
    t_cl_list_list, T_cl_list = create_model("T_cl_list", {"flag":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":str, "depart":str, "rmcat":str, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "outstand":decimal, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "email":str, "email_adr":str, "tot_night":int, "ratecode":str, "full_name":str, "address":str, "memberno":str, "membertype":str, "phonenum":str, "str_outstand":str, "night":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cl_list_list


        nonlocal s_list, cl_list, t_cl_list
        nonlocal s_list_list, cl_list_list, t_cl_list_list
        return {"t-cl-list": t_cl_list_list}


    t_cl_list_list.clear()

    for cl_list in query(cl_list_list):
        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        buffer_copy(cl_list, t_cl_list)

        if num_entries(cl_list.company, ";") > 1:
            t_cl_list.company = entry(0, cl_list.company, ";")
            t_cl_list.phonenum = entry(1, cl_list.company, ";")


        else:
            t_cl_list.company = cl_list.company
        t_cl_list.str_outstand = to_string(cl_list.outstand, "->>>,>>>,>>9.99")
        t_cl_list.night = date_mdy(cl_list.depart) - date_mdy(cl_list.arrive)
    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list.name = "SUMMARY"
    t_cl_list.memberno = "Room Type"
    t_cl_list.membertype = "Nation"
    t_cl_list.vip = " Qty"
    t_cl_list.rmcat = " Adult"
    t_cl_list.ratecode = "       (%)"
    t_cl_list.pax = " Child"

    for s_list in query(s_list_list):
        t_cl_list = T_cl_list()
        t_cl_list_list.append(t_cl_list)

        t_cl_list.memberno = s_list.bezeich
        t_cl_list.membertype = s_list.nat
        t_cl_list.vip = to_string(s_list.anz, ">>>9")
        t_cl_list.rmcat = to_string(s_list.adult, ">>,>>9")
        t_cl_list.ratecode = to_string(s_list.proz, "    >>9.99")
        t_cl_list.pax = to_string(s_list.child, ">>,>>9")


    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list = T_cl_list()
    t_cl_list_list.append(t_cl_list)

    t_cl_list.memberno = "T O T A L"
    t_cl_list.membertype = ""
    t_cl_list.vip = to_string(tot_rm, ">>>9")
    t_cl_list.rmcat = to_string(tot_a + tot_co, ">>,>>9")
    t_cl_list.ratecode = "    100.00"
    t_cl_list.pax = to_string(tot_c, ">>,>>9")

    return generate_output()