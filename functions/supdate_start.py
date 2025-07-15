from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Billjournal, Artikel, H_journal, H_artikel, L_artikel, L_op, L_ophdr, H_rezept, H_rezlin, L_bestand, L_verbrauch

def supdate_start():
    bill_date:date = None
    wait_time:int = 0
    lscheinnr:str = ""
    last_date:date = None
    anzahl:decimal = to_decimal("0.0")
    wert:decimal = to_decimal("0.0")
    curr_lager:int = 0
    htparam = billjournal = artikel = h_journal = h_artikel = l_artikel = l_op = l_ophdr = h_rezept = h_rezlin = l_bestand = l_verbrauch = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        return {}

    def update_stock(anz:int, lagernr:int, artnrlager:int, artnrrezept:int):

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        curr_pos:int = 0
        curr_lager = lagernr

        if curr_lager != 0 and artnrlager != 0:

            if last_date != bill_date:
                create_ophdr()

            l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.artnr == artnrlager)).first()

            l_op = db_session.query(L_op).filter(
                     (L_op.op_art == 7) & (L_op.datum == bill_date) & (L_op.lager_nr == curr_lager) & (L_op.artnr == artnrlager)).first()

            if not l_op:
                curr_pos = l_op_pos()
                l_op = L_op()
                db_session.add(l_op)

                l_op.datum = bill_date
                l_op.lager_nr = curr_lager
                l_op.artnr = artnrlager
                l_op.zeit = get_current_time_in_seconds()
                l_op.op_art = 7
                l_op.herkunftflag = 1
                l_op.pos = curr_pos
                l_op.lscheinnr = lscheinnr
                l_op.einzelpreis =  to_decimal(l_artikel.vk_preis)
            anzahl =  to_decimal(anz)
            l_op.anzahl =  to_decimal(l_op.anzahl) + to_decimal(anzahl)
            wert =  to_decimal(l_artikel.vk_preis) * to_decimal(anzahl)
            l_op.warenwert =  to_decimal(l_op.warenwert) + to_decimal(wert)
            update_soh(artnrlager)
            update_verbrauch(artnrlager)

        elif curr_lager != 0 and artnrrezept != 0:
            deduct_recipe(artnrrezept, anz)


    def l_op_pos():

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)

        for l_op1 in db_session.query(L_op1).filter(
                 (func.lower(L_op1.lscheinnr) == (lscheinnr).lower()) & (L_op1.loeschflag >= 0) & (L_op1.pos > 0)).order_by(L_op1._recid).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1

        return generate_inner_output()


    def create_ophdr():

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        s:str = ""
        i:int = 1
        s = "pos" + substring(to_string(get_year(get_current_date())) , 2, 2) + to_string(get_month(get_current_date()) , "99") + to_string(get_day(get_current_date()) , "99")
        lscheinnr = s + to_string(i, "999")
        l_ophdr = L_ophdr()
        db_session.add(l_ophdr)

        l_ophdr.datum = bill_date
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "pos"
        last_date = bill_date


    def deduct_recipe(rezeptnr:int, anz:int):

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        lart = None
        curr_pos:int = 0
        Lart =  create_buffer("Lart",L_artikel)

        h_rezept = db_session.query(H_rezept).filter(
                 (H_rezept.artnrrezept == rezeptnr)).first()

        if h_rezept:

            for h_rezlin in db_session.query(H_rezlin).filter(
                     (H_rezlin.artnrrezept == rezeptnr)).order_by(H_rezlin._recid).all():

                lart = db_session.query(Lart).filter(
                         (Lart.artnr == h_rezlin.artnrlager)).first()
                anzahl =  to_decimal(h_rezlin.menge) * to_decimal(anz)
                wert =  to_decimal(anzahl) * to_decimal(lart.vk_preis)

                if last_date != bill_date:
                    create_ophdr()

                l_op = db_session.query(L_op).filter(
                         (L_op.op_art == 7) & (L_op.datum == bill_date) & (L_op.lager_nr == curr_lager) & (L_op.artnr == lart.artnr)).first()

                if not l_op:
                    curr_pos = l_op_pos()
                    l_op = L_op()
                    db_session.add(l_op)

                    l_op.datum = bill_date
                    l_op.lager_nr = curr_lager
                    l_op.artnr = lart.artnr
                    l_op.zeit = get_current_time_in_seconds()
                    l_op.op_art = 7
                    l_op.herkunftflag = 1
                    l_op.pos = curr_pos
                    l_op.lscheinnr = lscheinnr
                    l_op.einzelpreis =  to_decimal(lart.vk_preis)
                l_op.anzahl =  to_decimal(l_op.anzahl) + to_decimal(anzahl)
                l_op.warenwert =  to_decimal(l_op.warenwert) + to_decimal(wert)
                update_soh(lart.artnr)
                update_verbrauch(lart.artnr)


    def update_soh(artnr:int):

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & (L_bestand.artnr == artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.artnr = artnr
            l_bestand.anf_best_dat = bill_date
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(wert)

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == l_artikel.artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = artnr
            l_bestand.anf_best_dat = bill_date
        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(wert)


    def update_verbrauch(artnr:int):

        nonlocal bill_date, wait_time, lscheinnr, last_date, anzahl, wert, curr_lager, htparam, billjournal, artikel, h_journal, h_artikel, l_artikel, l_op, l_ophdr, h_rezept, h_rezlin, l_bestand, l_verbrauch

        l_verbrauch = db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == artnr) & (L_verbrauch.datum == bill_date)).first()

        if not l_verbrauch:
            l_verbrauch = L_verbrauch()
            db_session.add(l_verbrauch)

            l_verbrauch.artnr = artnr
            l_verbrauch.datum = bill_date
        l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) + to_decimal(anzahl)
        l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(wert)


    while True:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 222)).first()
        wait_time = htparam.finteger * 60

        if wait_time == 0:
            wait_time = 30 * 60

        billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.nachbuchen == False) & (Billjournal.bill_datum == bill_date)).first()
        while None != billjournal:

            artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()

            if artikel.artart == 0 and artikel.lagernr != 0 and (artikel.artnrlager != 0 or artikel.artnrrezept != 0):
                update_stock(billjournal.anzahl, artikel.lagernr, artikel.artnrlager, artikel.artnrrezept)
            billjournal.nachbuchen = True

        curr_recid = billjournal._recid
        billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.nachbuchen == False) & (Billjournal.bill_datum == bill_date) & (Billjournal._recid > curr_recid)).first()

        h_journal = db_session.query(H_journal).filter(
                 (H_journal.nachbuchen == False) & (H_journal.bill_datum == bill_date) & (H_journal.artart == 0)).first()
        while None != h_journal:

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == h_journal.departement)).first()

            if h_artikel.lagernr != 0 and (h_artikel.artnrlager != 0 or artikel.artnrrezept != 0):
                update_stock(h_journal.anzahl, h_artikel.lagernr, h_artikel.artnrlager, h_artikel.artnrrezept)
            h_journal.nachbuchen = True

        curr_recid = h_journal._recid
        h_journal = db_session.query(H_journal).filter(
                 (H_journal.nachbuchen == False) & (H_journal.bill_datum == bill_date) & (H_journal.artart == 0) & (H_journal._recid > curr_recid)).first()

    return generate_output()