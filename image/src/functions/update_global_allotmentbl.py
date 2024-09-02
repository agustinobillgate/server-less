from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline, Counters

def update_global_allotmentbl(user_init:str, currcode:str, allot_list:[Allot_list]):
    kontline = counters = None

    allot_list = kline = kbuff = None

    allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "w_day":str, "tot_rm":int, "ooo":int, "occ":int, "avl_rm":int, "stat1":int, "stat2":int, "stat5":int, "glres":int, "avail1":int, "ovb1":int, "allot1":int, "gl_allot":int, "gl_used":int, "gl_remain":int, "allot2":int, "blank_str":str, "avail2":int, "ovb2":int, "s_avail2":int, "expired":bool})

    Kline = Kontline
    Kbuff = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kontline, counters
        nonlocal kline, kbuff


        nonlocal allot_list, kline, kbuff
        nonlocal allot_list_list
        return {}

    def update_allotment():

        nonlocal kontline, counters
        nonlocal kline, kbuff


        nonlocal allot_list, kline, kbuff
        nonlocal allot_list_list


        Kline = Kontline
        Kbuff = Kontline

        for allot_list in query(allot_list_list, filters=(lambda allot_list :allot_list.expired == False and allot_list.allot1 != allot_list.gl_allot)):

            kontline = db_session.query(Kontline).filter(
                    (func.lower(Kontline.kontcode) == (currcode).lower()) &  (Kontline.ankunft <= allot_list.datum) &  (Kontline.abreise >= allot_list.datum)).first()

            if kontline and kontline.zimmeranz != allot_list.gl_allot:

                if kontline.ankunft == kontline.abreise:
                    kontline.zimmeranz = allot_list.gl_allot

                    kontline = db_session.query(Kontline).first()
                else:

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 10)).first()
                    counters = counters + 1

                    counters = db_session.query(Counters).first()
                    kline = Kline()
                    db_session.add(kline)

                    buffer_copy(kontline, kline,except_fields=["kontignr"])
                    kline.abreise = allot_list.datum - 1
                    kline.kontignr = counters

                    kline = db_session.query(Kline).first()

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 10)).first()
                    counters = counters + 1

                    counters = db_session.query(Counters).first()
                    kline = Kline()
                    db_session.add(kline)

                    buffer_copy(kontline, kline,except_fields=["kontignr"])
                    kline.ankunft = allot_list.datum + 1
                    kline.kontignr = counters

                    kline = db_session.query(Kline).first()
                    kontline.ankunft = allot_list.datum
                    kontline.abreise = allot_list.datum
                    kontline.zimmeranz = allot_list.gl_allot
                    kontline.useridanlage = user_init

                    kontline = db_session.query(Kontline).first()

        for kontline in db_session.query(Kontline).filter(
                (func.lower(Kontline.kontcode) == (currcode).lower())).all():

            kline = db_session.query(Kline).filter(
                    (func.lower(Kline.kontcode) == (currcode).lower()) &  (Kline.ankunft == kontline.abreise + 1) &  (Kline.zimmeranz == kontline.zimmeranz)).first()

            if kline:

                kbuff = db_session.query(Kbuff).filter(
                        (Kbuff._recid == kontline._recid)).first()
                kbuff.abreise = kline.abreise

                kbuff = db_session.query(Kbuff).first()

                kline = db_session.query(Kline).first()
                db_session.delete(kline)

    update_allotment()

    return generate_output()