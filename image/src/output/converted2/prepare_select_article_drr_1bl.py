#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Queasy, Artikel, Segment

def prepare_select_article_drr_1bl(case_type:int, departement:int):

    prepare_cache ([Htparam, Queasy, Artikel, Segment])

    c_862:int = 0
    c_892:int = 0
    str2:string = ""
    str3:string = ""
    st1:string = ""
    st2:string = ""
    st3:string = ""
    st4:string = ""
    st5:string = ""
    st6:string = ""
    st7:string = ""
    st8:string = ""
    st9:string = ""
    st10:string = ""
    st11:string = ""
    st12:string = ""
    n:int = 0
    n1:int = 0
    n2:int = 0
    n3:int = 0
    n4:int = 0
    n5:int = 0
    n6:int = 0
    n7:int = 0
    n8:int = 0
    n9:int = 0
    n10:int = 0
    dept:int = 0
    str_list_list = []
    htparam = queasy = artikel = segment = None

    str_list = stat_list = out_list = None

    str_list_list, Str_list = create_model("Str_list", {"nr":int, "bezeich":string, "used":bool, "grup":bool, "grp_name":string})
    stat_list_list, Stat_list = create_model("Stat_list", {"artnr":int, "used":bool, "grup":bool, "grp_name":string, "flag":string})
    out_list_list, Out_list = create_model_like(Stat_list, {"deptnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_862, c_892, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, dept, str_list_list, htparam, queasy, artikel, segment
        nonlocal case_type, departement


        nonlocal str_list, stat_list, out_list
        nonlocal str_list_list, stat_list_list, out_list_list

        return {"str-list": str_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    c_862 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
    c_892 = htparam.finteger

    queasy = get_cache (Queasy, {"key": [(eq, 265)]})

    if queasy:
        str2 = queasy.char2
        str3 = queasy.char3


    for n in range(1,num_entries(str2, ";")  + 1) :
        st1 = entry(n - 1, str2, ";")

        if substring(st1, 0, 11) == ("$FOrevenue$").lower()  and substring(st1, 11, 3) == ("YES").lower() :
            st2 = substring(st1, 15)
            for n1 in range(1,num_entries(st2, ",")  + 1) :
                st3 = entry(n1 - 1, st2, ",")
                stat_list = Stat_list()
                stat_list_list.append(stat_list)

                stat_list.artnr = to_int(entry(0, st3, "-"))
                stat_list.used = True
                stat_list.grup = logical(entry(1, st3, "-"))
                stat_list.grp_name = entry(2, st3, "-")
                stat_list.flag = "FoRev"

        if substring(st1, 0, 13) == ("$otherincome$").lower()  and substring(st1, 13, 3) == ("YES").lower() :
            st4 = substring(st1, 17)
            for n2 in range(1,num_entries(st4, ",")  + 1) :
                st5 = entry(n2 - 1, st4, ",")
                stat_list = Stat_list()
                stat_list_list.append(stat_list)

                stat_list.artnr = to_int(entry(0, st5, "-"))
                stat_list.used = True
                stat_list.grup = logical(entry(1, st5, "-"))
                stat_list.grp_name = entry(2, st5, "-")
                stat_list.flag = "OtherRev"

        if substring(st1, 0, 9) == ("$segment$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
            st6 = substring(st1, 13)
            for n3 in range(1,num_entries(st6, ",")  + 1) :
                st7 = entry(n3 - 1, st6, ",")
                stat_list = Stat_list()
                stat_list_list.append(stat_list)

                stat_list.artnr = to_int(entry(0, st7, "-"))
                stat_list.used = True
                stat_list.grup = logical(entry(1, st7, "-"))
                stat_list.grp_name = entry(2, st7, "-")
                stat_list.flag = "Segment"


    for n4 =1,num_entries(str3, "*")  + 1 :
        st8 = entry(n4 - 1, str3, "*")

        if substring(st8, 0, 16) == ("$revenueOutlets$").lower()  and substring(st8, 16, 3) == ("YES").lower() :
            st9 = substring(st8, 19)
            for n5 in range(1,num_entries(st9, ";")  + 1) :
                st10 = entry(n5 - 1, st9, ";")
                for n6 in range(1,num_entries(st10, "|")  + 1) :
                    st11 = entry(n6 - 1, st10, "|")

                    if n6 == 1 and st11 != "" and entry(1, st10, "|") != "":
                        dept = to_int(st11)

                    elif st11 != "" and n6 > 1:
                        for n7 in range(1,num_entries(st11, ",")  + 1) :
                            st12 = entry(n7 - 1, st11, ",")

                            if st12 != "":
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.deptnr = dept
                                out_list.artnr = to_int(entry(0, st12, "-"))
                                out_list.used = True
                                out_list.grup = logical(entry(1, st12, "-"))
                                out_list.grp_name = entry(2, st12, "-")

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 1) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.artnr == str_list.nr and stat_list.flag.lower()  == ("FoRev").lower()), first=True)

            if stat_list:
                str_list.used = stat_list.used
                str_list.grup = stat_list.grup
                str_list.grp_name = stat_list.grp_name

    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 4) & (Artikel.zwkum != 26) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.artnr == str_list.nr and stat_list.flag.lower()  == ("OtherRev").lower()), first=True)

            if stat_list:
                str_list.used = stat_list.used
                str_list.grup = stat_list.grup
                str_list.grp_name = stat_list.grp_name

    elif case_type == 3:

        for segment in db_session.query(Segment).order_by(Segment._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = segment.segmentcode
            str_list.bezeich = segment.bezeich

            stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.artnr == str_list.nr and stat_list.flag.lower()  == ("Segment").lower()), first=True)

            if stat_list:
                str_list.used = stat_list.used
                str_list.grup = stat_list.grup
                str_list.grp_name = stat_list.grp_name

    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == departement) & (Artikel.endkum != 101)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            out_list = query(out_list_list, filters=(lambda out_list: out_list.artnr == str_list.nr and out_list.deptnr == departement), first=True)

            if out_list:
                str_list.used = out_list.used
                str_list.grup = out_list.grup
                str_list.grp_name = out_list.grp_name

    return generate_output()