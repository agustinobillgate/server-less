#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Zwkum, Artikel, Kellne1, Kellner, Hoteldpt

def rwaiter_admin_copy_waiterbl(r_kellner:int, dept2:int, dept:int, crart2:int):

    prepare_cache ([Artikel, Kellne1, Kellner, Hoteldpt])

    to_deptname:string = ""
    from_deptname:string = ""
    str_desc:string = ""
    subgrp_number:int = 0
    zwkum = artikel = kellne1 = kellner = hoteldpt = None

    t_zwkum = toart1 = toart2 = waiter1 = waiter2 = b_zwkum = None

    t_zwkum_data, T_zwkum = create_model_like(Zwkum)

    Toart1 = create_buffer("Toart1",Artikel)
    Toart2 = create_buffer("Toart2",Artikel)
    Waiter1 = create_buffer("Waiter1",Kellne1)
    Waiter2 = create_buffer("Waiter2",Kellner)
    B_zwkum = create_buffer("B_zwkum",Zwkum)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_deptname, from_deptname, str_desc, subgrp_number, zwkum, artikel, kellne1, kellner, hoteldpt
        nonlocal r_kellner, dept2, dept, crart2
        nonlocal toart1, toart2, waiter1, waiter2, b_zwkum


        nonlocal t_zwkum, toart1, toart2, waiter1, waiter2, b_zwkum
        nonlocal t_zwkum_data

        return {}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept2)]})

    if hoteldpt:
        to_deptname = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if hoteldpt:
        from_deptname = hoteldpt.depart

    kellner = get_cache (Kellner, {"_recid": [(eq, r_kellner)]})

    if kellner:

        toart2 = get_cache (Artikel, {"artnr": [(eq, kellner.kumsatz_nr)],"departement": [(eq, dept2)]})

        if not toart2:

            toart1 = get_cache (Artikel, {"artnr": [(eq, kellner.kumsatz_nr)],"departement": [(eq, dept)]})

            if toart1:
                toart2 = Artikel()
                db_session.add(toart2)

                buffer_copy(toart1, toart2,except_fields=["departement"])
                toart2.departement = dept2

                if num_entries(toart1.bezeich, " ") > 2:

                    if entry(0, toart1.bezeich, " ") == ("T/O").lower() :

                        if entry(2, toart1.bezeich, " ") != "":
                            str_desc = "T/O " + to_deptname + " " + entry(2, toart1.bezeich, " ")
                        else:
                            str_desc = "T/O " + to_deptname + " 1"
                        toart2.bezeich = str_desc

                zwkum = get_cache (Zwkum, {"zknr": [(eq, toart1.zwkum)],"departement": [(eq, dept2)]})

                if not zwkum:

                    for b_zwkum in db_session.query(B_zwkum).filter(
                             (B_zwkum.departement == dept2)).order_by(B_zwkum.zknr.desc()).yield_per(100):
                        t_zwkum = T_zwkum()
                        t_zwkum_data.append(t_zwkum)

                        buffer_copy(b_zwkum, t_zwkum,except_fields=["b_zwkum.zknr"])
                        t_zwkum.zknr = toart1.zwkum
                        t_zwkum.bezeich = str_desc
                        break
                    zwkum = Zwkum()
                    db_session.add(zwkum)

                    buffer_copy(t_zwkum, zwkum)
                str_desc = ""

        toart2 = get_cache (Artikel, {"artnr": [(eq, kellner.kzahl_nr)],"departement": [(eq, dept2)]})

        if not toart2:

            toart1 = get_cache (Artikel, {"artnr": [(eq, kellner.kzahl_nr)],"departement": [(eq, dept)]})

            if toart1:
                toart2 = Artikel()
                db_session.add(toart2)

                buffer_copy(toart1, toart2,except_fields=["departement"])
                toart2.departement = dept2

                if num_entries(toart1.bezeich, " ") > 2:

                    if entry(0, toart1.bezeich, " ") == ("T/O").lower() :

                        if entry(2, toart1.bezeich, " ") != "":
                            str_desc = "T/O " + to_deptname + " " + entry(2, toart1.bezeich, " ")
                        else:
                            str_desc = "T/O " + to_deptname + " 1"
                        toart2.bezeich = str_desc

                zwkum = get_cache (Zwkum, {"zknr": [(eq, toart1.zwkum)],"departement": [(eq, dept2)]})

                if not zwkum:

                    for b_zwkum in db_session.query(B_zwkum).filter(
                             (B_zwkum.departement == dept2)).order_by(B_zwkum.zknr.desc()).yield_per(100):
                        t_zwkum = T_zwkum()
                        t_zwkum_data.append(t_zwkum)

                        buffer_copy(b_zwkum, t_zwkum,except_fields=["b_zwkum.zknr"])
                        t_zwkum.zknr = toart1.zwkum
                        t_zwkum.bezeich = str_desc
                        break
                    zwkum = Zwkum()
                    db_session.add(zwkum)

                    buffer_copy(t_zwkum, zwkum)
                str_desc = ""

        # waiter2 = get_cache (Kellner, {"departement": [(eq, dept2)],"kumsatz_nr": [(eq, kellner.kumsatz_nr)]})
        waiter2 = db_session.query(Waiter2).filter(
                 (Waiter2.departement == dept2) &
                 (Waiter2.kumsatz_nr == kellner.kumsatz_nr)).with_for_update().first()

        if waiter2:
            pass
            buffer_copy(kellner, waiter2,except_fields=["kcredit_nr","departement"])
            waiter2.kcredit_nr = crart2
            waiter2.departement = dept2


        else:

            kellner = get_cache (Kellner, {"_recid": [(eq, r_kellner)]})

            if kellner:
                waiter2 = Kellner()
                db_session.add(waiter2)

                buffer_copy(kellner, waiter2,except_fields=["kcredit_nr","departement"])
                waiter2.kcredit_nr = crart2
                waiter2.departement = dept2


        pass
        pass

        waiter1 = get_cache (Kellne1, {"kellner_nr": [(eq, kellner.kellner_nr)],"departement": [(eq, dept2)]})

        if not waiter1:
            waiter1 = Kellne1()
            db_session.add(waiter1)

            buffer_copy(kellner, waiter1,except_fields=["departement"])
            waiter1.departement = dept2


            pass

    return generate_output()