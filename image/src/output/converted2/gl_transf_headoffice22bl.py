#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_accthis, Queasy, Gl_acctgrp, Gl_acctgrphis, Htparam

t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)
t_gl_accthis_list, T_gl_accthis = create_model_like(Gl_accthis)

def gl_transf_headoffice22bl(htl_code:string, close_month:date, close_year:date, t_gl_acct_list:[T_gl_acct], t_gl_accthis_list:[T_gl_accthis]):

    prepare_cache ([Queasy, Gl_acctgrp, Gl_acctgrphis, Htparam])

    success_flag = False
    curr_i:int = 0
    curr_ct:string = ""
    ct:string = ""
    c_code:string = ""
    i_year:int = 0
    gl_acct = gl_accthis = queasy = gl_acctgrp = gl_acctgrphis = htparam = None

    t_gl_acct = t_gl_accthis = hotel_list = qbuff = gbuff = ghbuff = None

    hotel_list_list, Hotel_list = create_model("Hotel_list", {"selectflag":bool, "htl_code":string, "i_hotel":int, "c_hotel":string, "i_brand":int, "i_country":int, "i_region":int, "i_area":int, "i_city":int, "dispflag":bool, "c_users":string}, {"dispflag": True})

    Qbuff = create_buffer("Qbuff",Queasy)
    Gbuff = create_buffer("Gbuff",Gl_acctgrp)
    Ghbuff = create_buffer("Ghbuff",Gl_acctgrphis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_i, curr_ct, ct, c_code, i_year, gl_acct, gl_accthis, queasy, gl_acctgrp, gl_acctgrphis, htparam
        nonlocal htl_code, close_month, close_year
        nonlocal qbuff, gbuff, ghbuff


        nonlocal t_gl_acct, t_gl_accthis, hotel_list, qbuff, gbuff, ghbuff
        nonlocal hotel_list_list

        return {"success_flag": success_flag}

    queasy = get_cache (Queasy, {"key": [(eq, 185)],"char1": [(eq, htl_code)]})

    if not queasy:

        return generate_output()
    success_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})

    if htparam:
        pass
        htparam.fdate = close_month


        pass
        pass
    hotel_list = Hotel_list()
    hotel_list_list.append(hotel_list)

    hotel_list.i_hotel = queasy.number1
    hotel_list.htl_code = queasy.char1
    hotel_list.c_hotel = queasy.char2
    ct = queasy.char3


    for curr_i in range(1,num_entries(ct, ";")  + 1) :
        curr_ct = entry(curr_i - 1, ct, ";")

        if curr_ct != "":

            if substring(curr_ct, 0, 6) == ("$brand").lower() :
                c_code = substring(curr_ct, 6)

                qbuff = get_cache (Queasy, {"key": [(eq, 180)],"char1": [(eq, c_code)]})
                hotel_list.i_brand = qbuff.number1

            elif substring(curr_ct, 0, 3) == ("$CN").lower() :
                c_code = substring(curr_ct, 3)

                qbuff = get_cache (Queasy, {"key": [(eq, 183)],"char1": [(eq, c_code)]})
                hotel_list.i_country = qbuff.number1

            elif substring(curr_ct, 0, 3) == ("$RG").lower() :
                c_code = substring(curr_ct, 3)

                qbuff = get_cache (Queasy, {"key": [(eq, 182)],"char1": [(eq, c_code)]})
                hotel_list.i_region = qbuff.number1

            elif substring(curr_ct, 0, 5) == ("$AREA").lower() :
                c_code = substring(curr_ct, 5)

                qbuff = get_cache (Queasy, {"key": [(eq, 184)],"char1": [(eq, c_code)]})
                hotel_list.i_area = qbuff.number1

            elif substring(curr_ct, 0, 3) == ("$ct").lower() :
                c_code = substring(curr_ct, 3)

                qbuff = get_cache (Queasy, {"key": [(eq, 181)],"char1": [(eq, c_code)]})

                if qbuff:
                    hotel_list.i_city = qbuff.number1

            elif substring(curr_ct, 0, 5) == ("$USER").lower() :
                hotel_list.c_users = substring(curr_ct, 5)

    t_gl_acct = query(t_gl_acct_list, first=True)
    while None != t_gl_acct:

        gl_acctgrp = get_cache (Gl_acctgrp, {"fibukonto": [(eq, t_gl_acct.fibukonto)],"htlcode": [(eq, htl_code)]})

        if not gl_acctgrp:
            gl_acctgrp = Gl_acctgrp()
            db_session.add(gl_acctgrp)

            gl_acctgrp.htlcode = htl_code


            pass

        gbuff = get_cache (Gl_acctgrp, {"_recid": [(eq, gl_acctgrp._recid)]})
        buffer_copy(t_gl_acct, gbuff)
        gbuff.brand = hotel_list.i_brand
        gbuff.country = hotel_list.i_country
        gbuff.region = hotel_list.i_region
        gbuff.area = hotel_list.i_area
        gbuff.city = hotel_list.i_city


        pass
        pass
        pass

        t_gl_acct = query(t_gl_acct_list, next=True)

    if close_year != None:
        i_year = get_year(close_year)

    t_gl_accthis = query(t_gl_accthis_list, first=True)
    while None != t_gl_accthis:

        gl_acctgrphis = get_cache (Gl_acctgrphis, {"fibukonto": [(eq, t_gl_acct.fibukonto)],"htlcode": [(eq, htl_code)],"year": [(eq, i_year)]})

        if not gl_acctgrphis:
            gl_acctgrphis = Gl_acctgrphis()
            db_session.add(gl_acctgrphis)

            gl_acctgrphis.htlcode = htl_code


            pass

        ghbuff = get_cache (Gl_acctgrphis, {"_recid": [(eq, gl_acctgrphis._recid)]})
        buffer_copy(t_gl_accthis, ghbuff)
        ghbuff.brand = hotel_list.i_brand
        ghbuff.country = hotel_list.i_country
        ghbuff.region = hotel_list.i_region
        ghbuff.area = hotel_list.i_area
        ghbuff.city = hotel_list.i_city


        pass
        pass
        pass

        t_gl_accthis = query(t_gl_accthis_list, next=True)

    queasy = get_cache (Queasy, {"key": [(eq, 188)],"char1": [(eq, htl_code)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 188
        queasy.char1 = htl_code


        pass

    qbuff = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
    qbuff.date1 = close_month

    if close_year != None:
        qbuff.date2 = close_year
    pass
    pass

    return generate_output()