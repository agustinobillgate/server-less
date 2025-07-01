#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bill, Res_line, Bill_line, Zimmer, Zinrstat, Zimkateg, Zkstat, Sourccod, Sources, Segment, Segmentstat, Guest_queasy, Nation, Nationstat, Artikel, Umsatz, Kontplan, Budget, Uebertrag, H_artikel, H_umsatz, H_cost, Exrate, Dml_art, Queasy, Dml_artdep

def mn_del_old_statbl(case_type:int):

    prepare_cache ([Htparam, Res_line, Bill_line, Zimmer, Zimkateg, Sourccod, Artikel, H_artikel])

    i = 0
    j = 0
    anz:int = 762
    ci_date:date = None
    htparam = bill = res_line = bill_line = zimmer = zinrstat = zimkateg = zkstat = sourccod = sources = segment = segmentstat = guest_queasy = nation = nationstat = artikel = umsatz = kontplan = budget = uebertrag = h_artikel = h_umsatz = h_cost = exrate = dml_art = queasy = dml_artdep = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        return {"i": i, "j": j}

    def check_co_guestbill():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        bbuff = None
        bl_saldo:Decimal = to_decimal("0.0")
        bl_saldo2:Decimal = to_decimal("0.0")
        Bbuff =  create_buffer("Bbuff",Bill)

        bill = get_cache (Bill, {"resnr": [(gt, 0)],"reslinnr": [(gt, 0)],"flag": [(eq, 0)],"saldo": [(eq, 0)]})
        while None != bill:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

            if not res_line:

                bbuff = db_session.query(Bbuff).filter(
                         (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1
                pass
                pass

            elif res_line.active_flag == 2:

                bbuff = db_session.query(Bbuff).filter(
                         (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1
                pass
                pass

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.resnr > 0) & (Bill.reslinnr > 0) & (Bill.flag == 0) & (Bill.saldo == 0) & (Bill._recid > curr_recid)).first()

        bill = get_cache (Bill, {"flag": [(eq, 0)],"rechnr": [(gt, 0)]})
        while None != bill:
            bl_saldo =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                bl_saldo =  to_decimal(bl_saldo) + to_decimal(bill_line.betrag)

            if bl_saldo != bill.saldo:

                bbuff = db_session.query(Bbuff).filter(
                         (Bbuff._recid == bill._recid)).first()
                bbuff.saldo =  to_decimal(bl_saldo)
                pass
                pass

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.flag == 0) & (Bill.rechnr > 0) & (Bill._recid > curr_recid)).first()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"parent_nr": [(eq, res_line.reslinnr)]})
            while None != bill:
                bl_saldo2 =  to_decimal("0")

                for bill_line in db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                    bl_saldo2 =  to_decimal(bl_saldo2) + to_decimal(bill_line.betrag)

                if bill.zinr != res_line.zinr:

                    bbuff = db_session.query(Bbuff).filter(
                             (Bbuff._recid == bill._recid)).first()
                    bbuff.zinr = res_line.zinr
                    pass
                    pass

                if bl_saldo2 != bill.saldo:

                    bbuff = db_session.query(Bbuff).filter(
                             (Bbuff._recid == bill._recid)).first()
                    bbuff.saldo =  to_decimal(bl_saldo2)
                    pass
                    pass

                curr_recid = bill._recid
                bill = db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill._recid > curr_recid)).first()


    def del_old_stat1():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

            zinrstat = get_cache (Zinrstat, {"datum": [(le, curr_date)],"zinr": [(eq, zimmer.zinr)]})
            while None != zinrstat:
                i = i + 1
                pass
                db_session.delete(zinrstat)

                curr_recid = zinrstat._recid
                zinrstat = db_session.query(Zinrstat).filter(
                             (Zinrstat.datum <= curr_date) & (Zinrstat.zinr == zimmer.zinr) & (Zinrstat._recid > curr_recid)).first()

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ooo").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("SegArr").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ArgArr").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("CatArr").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("SegDep").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ArgDep").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("CatDep").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("SegInh").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("ArgInh").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.zinr == ("CatInh").lower()) & (Zinrstat.datum <= (ci_date - timedelta(days=anz)))).order_by(Zinrstat._recid).all():
            db_session.delete(zinrstat)


    def del_old_stat2():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            zkstat = get_cache (Zkstat, {"datum": [(le, curr_date)],"zikatnr": [(eq, zimkateg.zikatnr)]})
            while None != zkstat:
                i = i + 1
                pass
                db_session.delete(zkstat)

                curr_recid = zkstat._recid
                zkstat = db_session.query(Zkstat).filter(
                         (Zkstat.datum <= curr_date) & (Zkstat.zikatnr == zimkateg.zikatnr) & (Zkstat._recid > curr_recid)).first()


    def del_old_stat3():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for sourccod in db_session.query(Sourccod).order_by(Sourccod._recid).all():

            sources = get_cache (Sources, {"datum": [(le, curr_date)],"source_code": [(eq, sourccod.source_code)]})
            while None != sources:
                i = i + 1
                pass
                db_session.delete(sources)

                curr_recid = sources._recid
                sources = db_session.query(Sources).filter(
                         (Sources.datum <= curr_date) & (Sources.source_code == sourccod.source_code) & (Sources._recid > curr_recid)).first()


    def del_old_stat4():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            segmentstat = get_cache (Segmentstat, {"datum": [(le, curr_date)],"segmentcode": [(eq, segment.segmentcode)]})
            while None != segmentstat:
                i = i + 1
                pass
                db_session.delete(segmentstat)

                curr_recid = segmentstat._recid
                segmentstat = db_session.query(Segmentstat).filter(
                         (Segmentstat.datum <= curr_date) & (Segmentstat.segmentcode == segment.segmentcode) & (Segmentstat._recid > curr_recid)).first()


    def del_old_stat41():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for guest_queasy in db_session.query(Guest_queasy).filter(
                 (Guest_queasy.betriebsnr == 0) & (Guest_queasy.key == ("msegm").lower()) & (Guest_queasy.date1 <= curr_date)).order_by(Guest_queasy._recid).all():
            i = i + 1
            db_session.delete(guest_queasy)


    def del_old_stat5():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for nation in db_session.query(Nation).order_by(Nation._recid).all():

            nationstat = get_cache (Nationstat, {"datum": [(le, curr_date)],"nationnr": [(eq, nation.nationnr)]})
            while None != nationstat:
                i = i + 1
                pass
                db_session.delete(nationstat)

                curr_recid = nationstat._recid
                nationstat = db_session.query(Nationstat).filter(
                         (Nationstat.datum <= curr_date) & (Nationstat.nationnr == nation.nationnr) & (Nationstat._recid > curr_recid)).first()


    def del_old_stat6():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        j = 0
        curr_date = ci_date - timedelta(days=anz)

        for artikel in db_session.query(Artikel).order_by(Artikel.departement, Artikel.artnr).all():

            umsatz = get_cache (Umsatz, {"datum": [(le, curr_date)],"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})
            while None != umsatz:
                i = i + 1

                kontplan = get_cache (Kontplan, {"betriebsnr": [(eq, umsatz.departement)],"kontignr": [(eq, umsatz.artnr)],"datum": [(eq, umsatz.datum)]})

                if kontplan:
                    db_session.delete(kontplan)
                pass
                db_session.delete(umsatz)

                curr_recid = umsatz._recid
                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.datum <= curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz._recid > curr_recid)).first()

            budget = get_cache (Budget, {"datum": [(le, curr_date)],"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)]})
            while None != budget:
                j = j + 1
                pass
                db_session.delete(budget)

                curr_recid = budget._recid
                budget = db_session.query(Budget).filter(
                         (Budget.datum <= curr_date) & (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget._recid > curr_recid)).first()

        for uebertrag in db_session.query(Uebertrag).filter(
                 (Uebertrag.datum < curr_date)).order_by(Uebertrag._recid).all():
            db_session.delete(uebertrag)


    def del_old_stat7():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        for h_artikel in db_session.query(H_artikel).order_by(H_artikel.departement, H_artikel.artnr).all():

            h_umsatz = get_cache (H_umsatz, {"datum": [(le, curr_date)],"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)]})
            while None != h_umsatz:
                i = i + 1
                pass
                db_session.delete(h_umsatz)

                curr_recid = h_umsatz._recid
                h_umsatz = db_session.query(H_umsatz).filter(
                         (H_umsatz.datum <= curr_date) & (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz._recid > curr_recid)).first()


    def del_old_stat8():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        h_cost = get_cache (H_cost, {"datum": [(le, curr_date)]})
        while None != h_cost:
            i = i + 1
            pass
            db_session.delete(h_cost)

            curr_recid = h_cost._recid
            h_cost = db_session.query(H_cost).filter(
                     (H_cost.datum <= curr_date) & (H_cost._recid > curr_recid)).first()


    def del_old_stat9():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        curr_date:date = None
        i = 0
        curr_date = ci_date - timedelta(days=anz)

        exrate = get_cache (Exrate, {"datum": [(le, curr_date)]})
        while None != exrate:
            i = i + 1
            pass
            db_session.delete(exrate)

            curr_recid = exrate._recid
            exrate = db_session.query(Exrate).filter(
                     (Exrate.datum <= curr_date) & (Exrate._recid > curr_recid)).first()


    def del_dml():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal case_type

        for dml_art in db_session.query(Dml_art).filter(
                 (Dml_art.datum <= (ci_date - timedelta(days=60)))).order_by(Dml_art._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, dml_art.artnr)],"date1": [(eq, dml_art.datum)]})

            if queasy:
                pass
                db_session.delete(queasy)
                pass
            db_session.delete(dml_art)

        for dml_artdep in db_session.query(Dml_artdep).filter(
                 (Dml_artdep.datum <= (ci_date - timedelta(days=60)))).order_by(Dml_artdep._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, dml_artdep.departement)],"number2": [(eq, dml_artdep.artnr)],"date1": [(eq, dml_artdep.datum)]})

            if queasy:
                pass
                db_session.delete(queasy)
                pass
            db_session.delete(dml_artdep)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 277)]})

    if htparam.paramgruppe == 9 and htparam.finteger != 0:
        anz = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    check_co_guestbill()

    if case_type == 1:
        del_old_stat1()

    elif case_type == 2:
        del_old_stat2()

    elif case_type == 3:
        del_old_stat3()

    elif case_type == 4:
        del_old_stat4()

    elif case_type == 41:
        del_old_stat41()

    elif case_type == 5:
        del_old_stat5()

    elif case_type == 6:
        del_old_stat6()

    elif case_type == 7:
        del_old_stat7()

    elif case_type == 8:
        del_old_stat8()

    elif case_type == 9:
        del_old_stat9()

    elif case_type == 999:
        del_dml()

    return generate_output()