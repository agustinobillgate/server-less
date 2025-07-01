#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Artikel

def prepare_select_article_drr_2bl(case_type:int, nr:int):

    prepare_cache ([Queasy, Artikel])

    str2:string = ""
    str3:string = ""
    st1:string = ""
    st2:string = ""
    st3:string = ""
    st4:string = ""
    n:int = 0
    n1:int = 0
    n2:int = 0
    n3:int = 0
    n4:int = 0
    str_list_list = []
    zwkum:int = 0
    queasy = artikel = None

    str_list = stat_list = None

    str_list_list, Str_list = create_model("Str_list", {"nr":int, "bezeich":string, "used":bool, "descr":string})
    stat_list_list, Stat_list = create_model("Stat_list", {"artnr":int, "used":bool, "descr":string, "zwkum":int, "flag":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str2, str3, st1, st2, st3, st4, n, n1, n2, n3, n4, str_list_list, zwkum, queasy, artikel
        nonlocal case_type, nr


        nonlocal str_list, stat_list
        nonlocal str_list_list, stat_list_list

        return {"str-list": str_list_list}


    queasy = get_cache (Queasy, {"key": [(eq, 265)]})

    if queasy:
        str2 = queasy.char2
        str3 = queasy.char3


    for n1 in range(1,num_entries(str2, ";")  + 1) :
        st1 = entry(n1 - 1, str2, ";")

        if substring(st1, 0, 11) == ("$statistic$").lower()  and substring(st1, 11, 3) == ("YES").lower() :
            st2 = substring(st1, 15)


            for n2 in range(1,num_entries(st2, "/")  + 1) :
                st3 = entry(n2 - 1, st2, "/")

                if n2 == 1 and st3 != "":
                    zwkum = to_int(st3)

                elif st3 != "" and n2 > 1:
                    for n3 in range(1,num_entries(st3, ",")  + 1) :
                        st4 = entry(n3 - 1, st3, ",")
                        stat_list = Stat_list()
                        stat_list_list.append(stat_list)

                        stat_list.zwkum = zwkum
                        stat_list.used = True
                        stat_list.artnr = to_int(entry(0, st4, "-"))
                        stat_list.descr = entry(1, st4, "-")
                        stat_list.flag = "Statistic"

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr >= 4000) & (Artikel.zwkum == nr) & (Artikel.departement == 0)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.artnr == artikel.artnr), first=True)

            if stat_list:
                str_list.used = True
                str_list.descr = stat_list.descr

    return generate_output()