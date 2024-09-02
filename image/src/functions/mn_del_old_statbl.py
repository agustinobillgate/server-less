from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bill, Res_line, Bill_line, Zimmer, Zinrstat, Zimkateg, Zkstat, Sourccod, Sources, Segment, Segmentstat, Guest_queasy, Nation, Nationstat, Artikel, Umsatz, Kontplan, Budget, Uebertrag, H_artikel, H_umsatz, H_cost, Exrate, Dml_art, Queasy, Dml_artdep

def mn_del_old_statbl(case_type:int):
    i = 0
    j = 0
    anz:int = 762
    ci_date:date = None
    htparam = bill = res_line = bill_line = zimmer = zinrstat = zimkateg = zkstat = sourccod = sources = segment = segmentstat = guest_queasy = nation = nationstat = artikel = umsatz = kontplan = budget = uebertrag = h_artikel = h_umsatz = h_cost = exrate = dml_art = queasy = dml_artdep = None

    bbuff = None

    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff
        return {"i": i, "j": j}

    def check_co_guestbill():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        bl_saldo:decimal = 0
        bl_saldo2:decimal = 0
        Bbuff = Bill

        bill = db_session.query(Bill).filter(
                (Bill.resnr > 0) &  (Bill.reslinnr > 0) &  (Bill.flag == 0) &  (Bill.saldo == 0)).first()
        while None != bill:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

            if not res_line:

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1

                bbuff = db_session.query(Bbuff).first()


            elif res_line.active_flag == 2:

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1

                bbuff = db_session.query(Bbuff).first()


            bill = db_session.query(Bill).filter(
                    (Bill.resnr > 0) &  (Bill.reslinnr > 0) &  (Bill.flag == 0) &  (Bill.saldo == 0)).first()

        bill = db_session.query(Bill).filter(
                (Bill.flag == 0) &  (Bill.rechnr > 0)).first()
        while None != bill:
            bl_saldo = 0

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr)).all():
                bl_saldo = bl_saldo + bill_line.betrag

            if bl_saldo != bill.saldo:

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.saldo = bl_saldo

                bbuff = db_session.query(Bbuff).first()


            bill = db_session.query(Bill).filter(
                    (Bill.flag == 0) &  (Bill.rechnr > 0)).first()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).first()
            while None != bill:
                bl_saldo2 = 0

                for bill_line in db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr)).all():
                    bl_saldo2 = bl_saldo2 + bill_line.betrag

                if bill.zinr != res_line.zinr:

                    bbuff = db_session.query(Bbuff).filter(
                            (Bbuff._recid == bill._recid)).first()
                    bbuff.zinr = res_line.zinr

                    bbuff = db_session.query(Bbuff).first()


                if bl_saldo2 != bill.saldo:

                    bbuff = db_session.query(Bbuff).filter(
                            (Bbuff._recid == bill._recid)).first()
                    bbuff.saldo = bl_saldo2

                    bbuff = db_session.query(Bbuff).first()


                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).first()

    def del_old_stat1():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for zimmer in db_session.query(Zimmer).all():

            zinrstat = db_session.query(Zinrstat).filter(
                        (Zinrstat.datum <= curr_date) &  (Zinrstat.zinr == zimmer.zinr)).first()
            while None != zinrstat:
                i = i + 1

                zinrstat = db_session.query(Zinrstat).first()
                db_session.delete(zinrstat)

                zinrstat = db_session.query(Zinrstat).filter(
                            (Zinrstat.datum <= curr_date) &  (Zinrstat.zinr == zimmer.zinr)).first()

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ooo") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "SegArr") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ArgArr") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "CatArr") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "SegDep") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ArgDep") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "CatDep") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "SegInh") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "ArgInh") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)

        for zinrstat in db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "CatInh") &  (Zinrstat.datum <= (ci_date - anz))).all():
            db_session.delete(zinrstat)


    def del_old_stat2():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for zimkateg in db_session.query(Zimkateg).all():

            zkstat = db_session.query(Zkstat).filter(
                    (Zkstat.datum <= curr_date) &  (Zkstat.zikatnr == zimkateg.zikatnr)).first()
            while None != zkstat:
                i = i + 1

                zkstat = db_session.query(Zkstat).first()
                db_session.delete(zkstat)


                zkstat = db_session.query(Zkstat).filter(
                        (Zkstat.datum <= curr_date) &  (Zkstat.zikatnr == zimkateg.zikatnr)).first()

    def del_old_stat3():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for sourccod in db_session.query(Sourccod).all():

            sources = db_session.query(Sources).filter(
                    (Sources.datum <= curr_date) &  (Sources.source_code == sourccod.source_code)).first()
            while None != sources:
                i = i + 1

                sources = db_session.query(Sources).first()
                db_session.delete(sources)


                sources = db_session.query(Sources).filter(
                        (Sources.datum <= curr_date) &  (Sources.source_code == sourccod.source_code)).first()

    def del_old_stat4():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for segment in db_session.query(Segment).all():

            segmentstat = db_session.query(Segmentstat).filter(
                    (Segmentstat.datum <= curr_date) &  (Segmentstat.segmentcode == segmentcode)).first()
            while None != segmentstat:
                i = i + 1

                segmentstat = db_session.query(Segmentstat).first()
                db_session.delete(segmentstat)


                segmentstat = db_session.query(Segmentstat).filter(
                        (Segmentstat.datum <= curr_date) &  (Segmentstat.segmentcode == segmentcode)).first()

    def del_old_stat41():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for guest_queasy in db_session.query(Guest_queasy).filter(
                (Guest_queasy.betriebsnr == 0) &  (func.lower(Guest_queasy.key) == "msegm") &  (Guest_queasy.date1 <= curr_date)).all():
            i = i + 1
            db_session.delete(guest_queasy)

    def del_old_stat5():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for nation in db_session.query(Nation).all():

            nationstat = db_session.query(Nationstat).filter(
                    (Nationstat.datum <= curr_date) &  (Nationstat.nationnr == nationnr)).first()
            while None != nationstat:
                i = i + 1

                nationstat = db_session.query(Nationstat).first()
                db_session.delete(nationstat)


                nationstat = db_session.query(Nationstat).filter(
                        (Nationstat.datum <= curr_date) &  (Nationstat.nationnr == nationnr)).first()

    def del_old_stat6():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        j = 0
        curr_date = ci_date - anz

        for artikel in db_session.query(Artikel).all():

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.datum <= curr_date) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement)).first()
            while None != umsatz:
                i = i + 1

                kontplan = db_session.query(Kontplan).filter(
                            (Kontplan.betriebsnr == umsatz.departement) &  (Kontplan.kontignr == umsatz.artnr) &  (Kontplan.datum == umsatz.datum)).first()

                if kontplan:
                    db_session.delete(kontplan)

                umsatz = db_session.query(Umsatz).first()
                db_session.delete(umsatz)


                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.datum <= curr_date) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement)).first()

            budget = db_session.query(Budget).filter(
                    (Budget.datum <= curr_date) &  (Budget.artnr == artikel.artnr) &  (Budget.departement == artikel.departement)).first()
            while None != budget:
                j = j + 1

                budget = db_session.query(Budget).first()
                db_session.delete(budget)


                budget = db_session.query(Budget).filter(
                        (Budget.datum <= curr_date) &  (Budget.artnr == artikel.artnr) &  (Budget.departement == artikel.departement)).first()

        for uebertrag in db_session.query(Uebertrag).filter(
                (Uebertrag.datum < curr_date)).all():
            db_session.delete(uebertrag)

    def del_old_stat7():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        for h_artikel in db_session.query(H_artikel).all():

            h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.datum <= curr_date) &  (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.departement == h_artikel.departement)).first()
            while None != h_umsatz:
                i = i + 1

                h_umsatz = db_session.query(H_umsatz).first()
                db_session.delete(h_umsatz)


                h_umsatz = db_session.query(H_umsatz).filter(
                        (H_umsatz.datum <= curr_date) &  (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.departement == h_artikel.departement)).first()

    def del_old_stat8():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        h_cost = db_session.query(H_cost).filter(
                (H_cost.datum <= curr_date)).first()
        while None != h_cost:
            i = i + 1

            h_cost = db_session.query(H_cost).first()
            db_session.delete(h_cost)


            h_cost = db_session.query(H_cost).filter(
                    (H_cost.datum <= curr_date)).first()

    def del_old_stat9():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        i = 0
        curr_date = ci_date - anz

        exrate = db_session.query(Exrate).filter(
                (Exrate.datum <= curr_date)).first()
        while None != exrate:
            i = i + 1

            exrate = db_session.query(Exrate).first()
            db_session.delete(exrate)


            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum <= curr_date)).first()

    def del_dml():

        nonlocal i, j, anz, ci_date, htparam, bill, res_line, bill_line, zimmer, zinrstat, zimkateg, zkstat, sourccod, sources, segment, segmentstat, guest_queasy, nation, nationstat, artikel, umsatz, kontplan, budget, uebertrag, h_artikel, h_umsatz, h_cost, exrate, dml_art, queasy, dml_artdep
        nonlocal bbuff


        nonlocal bbuff

        for dml_art in db_session.query(Dml_art).filter(
                (Dml_art.datum <= (ci_date - 60))).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 202) &  (Queasy.number1 == 0) &  (Queasy.number2 == dml_art.artnr) &  (Queasy.date1 == dml_art.datum)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                db_session.delete(queasy)

            db_session.delete(dml_art)

        for dml_artdep in db_session.query(Dml_artdep).filter(
                (Dml_artdep.datum <= (ci_date - 60))).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 202) &  (Queasy.number1 == dml_artdep.departement) &  (Queasy.number2 == dml_artdep.artnr) &  (Queasy.date1 == dml_artdep.datum)).first()

            if queasy:

                queasy = db_session.query(Queasy).first()
                db_session.delete(queasy)

            db_session.delete(dml_artdep)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 277)).first()

    if htparam.paramgruppe == 9 and htparam.finteger != 0:
        anz = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
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