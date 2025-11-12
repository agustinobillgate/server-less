#using conversion tools version: 1.0.0.117
#---------------------------------------------
# Rd, 17-July-25
# replace TRUE -> True

# Rulita, 12-11-2025 | 2A3C8E
# - Update release program  
#---------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Htparam, Fa_artikel

def fa_artlist_find_new_artnr_webbl(endkum:int, zwkum:int):

    prepare_cache ([Mathis, Fa_artikel])

    new_artnr = ""
    l_end:int = 0
    l_zw:int = 0
    ct:int = 0
    counter:int = 0
    counter2:int = 0
    mathis = htparam = fa_artikel = None

    buff_mathis = b_mathis = None

    Buff_mathis = create_buffer("Buff_mathis",Mathis)
    B_mathis = create_buffer("B_mathis",Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_artnr, l_end, l_zw, ct, counter, counter2, mathis, htparam, fa_artikel
        nonlocal endkum, zwkum
        nonlocal buff_mathis, b_mathis


        nonlocal buff_mathis, b_mathis

        return {"new_artnr": new_artnr}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 293)]})

    if htparam:

        if htparam.flogical:

            for fa_artikel in db_session.query(Fa_artikel).filter(
                     (Fa_artikel.subgrp == zwkum) & (Fa_artikel.gnr == endkum)).order_by(Fa_artikel._recid).all():

                mathis = get_cache (Mathis, {"nr": [(eq, fa_artikel.nr)]})

                if mathis:

                    if length(trim(mathis.asset)) == 9:
                        new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 5)) + 1 , "9999")
                        while True:
                            counter2 = counter2 + 1

                            if counter2 > 100:
                                break

                            buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                            if buff_mathis:
                                new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 5)) + 1 , "9999")
                            else:
                                new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(new_artnr, 5)) , "999999")
                                while True:
                                    counter = counter + 1

                                    if counter > 100:
                                        break

                                    b_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                                    if b_mathis:
                                        new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(b_mathis.asset, 6)) + 1 , "999999")
                                    else:
                                        break
                                break

                        return generate_output()
                    else:
                        new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 6)) + 1 , "9999")

                        if length(trim(new_artnr)) != length(trim(mathis.asset)) or matches(new_artnr,r"*?*"):
                            new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 6)) + 1 , "999999")
                        while True:
                            counter2 = counter2 + 1

                            if counter2 > 100:
                                break

                            buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                            if buff_mathis:

                                if length(trim(new_artnr)) == 12:
                                    new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 6)) + 1 , "999999")
                                else:
                                    new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 6)) + 1 , "9999")
                            else:
                                new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(new_artnr, 6)) , "999999")
                                while True:
                                    counter = counter + 1

                                    if counter > 100:
                                        break

                                    b_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                                    if b_mathis:
                                        new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(b_mathis.asset, 6)) + 1 , "999999")
                                    else:
                                        break
                                break

                        return generate_output()
            new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(ct + 1, "999999")
        else:

            for fa_artikel in db_session.query(Fa_artikel).filter(
                     (Fa_artikel.subgrp == zwkum) & (Fa_artikel.gnr == endkum)).order_by(Fa_artikel._recid).all():

                mathis = get_cache (Mathis, {"nr": [(eq, fa_artikel.nr)]})

                if mathis:

                    if length(trim(mathis.asset)) == 9:
                        new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 5)) + 1 , "9999")
                        while True:
                            counter = counter + 1

                            if counter > 100:
                                break

                            buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                            if buff_mathis:
                                new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 5)) + 1 , "9999")
                            else:
                                new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(new_artnr, 5)) , "9999")
                                break

                        return generate_output()
                    else:
                        new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 6)) + 1 , "9999")
                        while True:
                            counter = counter + 1

                            if counter > 100:
                                break

                            buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                            if buff_mathis:
                                new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 6)) + 1 , "9999")
                            else:
                                break

                        return generate_output()
            new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(ct + 1, "9999")
    else:

        for fa_artikel in db_session.query(Fa_artikel).filter(
                 (Fa_artikel.subgrp == zwkum) & (Fa_artikel.gnr == endkum)).order_by(Fa_artikel._recid).all():

            mathis = get_cache (Mathis, {"nr": [(eq, fa_artikel.nr)]})

            if mathis:

                if length(trim(mathis.asset)) == 9:
                    new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 5)) + 1 , "9999")
                    while True:

                        buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                        if buff_mathis:
                            new_artnr = to_string(endkum, "99") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 5)) + 1 , "9999")
                        else:
                            new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(new_artnr, 5)) , "9999")
                            break

                    return generate_output()
                else:
                    new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(mathis.asset, 6)) + 1 , "9999")
                    while True:

                        buff_mathis = get_cache (Mathis, {"asset": [(eq, trim(new_artnr))]})

                        if buff_mathis:
                            new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(to_int(substring(buff_mathis.asset, 6)) + 1 , "9999")
                        else:
                            break

                    return generate_output()
        new_artnr = to_string(endkum, "999") + to_string(zwkum, "999") + to_string(ct + 1, "9999")

    return generate_output()