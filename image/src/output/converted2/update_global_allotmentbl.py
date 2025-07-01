#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline, Counters

allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "w_day":string, "tot_rm":int, "ooo":int, "occ":int, "avl_rm":int, "stat1":int, "stat2":int, "stat5":int, "glres":int, "avail1":int, "ovb1":int, "allot1":int, "gl_allot":int, "gl_used":int, "gl_remain":int, "allot2":int, "blank_str":string, "avail2":int, "ovb2":int, "s_avail2":int, "expired":bool})

def update_global_allotmentbl(user_init:string, currcode:string, allot_list_list:[Allot_list]):

    prepare_cache ([Kontline, Counters])

    kontline = counters = None

    allot_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kontline, counters
        nonlocal user_init, currcode


        nonlocal allot_list

        return {}

    def update_allotment():

        nonlocal kontline, counters
        nonlocal user_init, currcode


        nonlocal allot_list

        kline = None
        kbuff = None
        tmp_date:date = None
        Kline =  create_buffer("Kline",Kontline)
        Kbuff =  create_buffer("Kbuff",Kontline)

        for allot_list in query(allot_list_list, filters=(lambda allot_list: allot_list.expired == False and allot_list.allot1 != allot_list.gl_allot), sort_by=[("datum",False)]):

            kontline = get_cache (Kontline, {"kontcode": [(eq, currcode)],"ankunft": [(le, allot_list.datum)],"abreise": [(ge, allot_list.datum)]})

            if kontline and kontline.zimmeranz != allot_list.gl_allot:

                if kontline.ankunft == kontline.abreise:
                    kontline.zimmeranz = allot_list.gl_allot


                    pass
                else:

                    counters = get_cache (Counters, {"counter_no": [(eq, 10)]})
                    counters.counter = counters.counter + 1
                    pass
                    kline = Kontline()
                    db_session.add(kline)

                    buffer_copy(kontline, kline,except_fields=["kontignr"])
                    kline.abreise = allot_list.datum - timedelta(days=1)
                    kline.kontignr = counters.counter


                    pass

                    counters = get_cache (Counters, {"counter_no": [(eq, 10)]})
                    counters.counter = counters.counter + 1
                    pass
                    kline = Kontline()
                    db_session.add(kline)

                    buffer_copy(kontline, kline,except_fields=["kontignr"])
                    kline.ankunft = allot_list.datum + timedelta(days=1)
                    kline.kontignr = counters.counter


                    pass
                    kontline.ankunft = allot_list.datum
                    kontline.abreise = allot_list.datum
                    kontline.zimmeranz = allot_list.gl_allot
                    kontline.useridanlage = user_init


                    pass

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontcode == (currcode).lower())).order_by(Kontline.ankunft).all():
            tmp_date = kontline.abreise + timedelta(days=1)

            kline = get_cache (Kontline, {"kontcode": [(eq, currcode)],"ankunft": [(eq, tmp_date)],"zimmeranz": [(eq, kontline.zimmeranz)]})

            if kline:

                kbuff = get_cache (Kontline, {"_recid": [(eq, kontline._recid)]})

                if kbuff:
                    pass
                    kbuff.abreise = kline.abreise


                    pass
                    pass
                    db_session.delete(kline)
                    pass

    update_allotment()

    return generate_output()