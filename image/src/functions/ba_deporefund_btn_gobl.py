from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bk_veran, Artikel, Umsatz, Billjournal, Bediener, Guest, Debitor

def ba_deporefund_btn_gobl(veran_nr:int, user_init:str, payment:decimal, artnr:int, foreign_payment:decimal, depoart:int, depobezeich:str):
    bill_date:date = None
    balance:decimal = 0
    htparam = bk_veran = artikel = umsatz = billjournal = bediener = guest = debitor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, balance, htparam, bk_veran, artikel, umsatz, billjournal, bediener, guest, debitor


        return {}

    def deposit_refund():

        nonlocal bill_date, balance, htparam, bk_veran, artikel, umsatz, billjournal, bediener, guest, debitor

        bill_date:date = None
        i:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.veran_nr == veran_nr)).first()

        if bk_veran:

            bk_veran = db_session.query(Bk_veran).first()
            bk_veran.deposit_pay[8] = bk_veran.deposit_pay[8] - payment
            bk_veran.payment_date[8] = bill_date
            bk_veran.payment_userinit[8] = user_init
            bk_veran.total_paid = 0


            for i in range(1,9 + 1) :
                bk_veran.total_paid = bk_veran.total_paid + bk_veran.deposit_payment[i - 1]

            bk_veran = db_session.query(Bk_veran).first()
            balance = bk_veran.deposit - bk_veran.total_paid


            create_journal(bill_date)

    def create_journal(bill_date:date):

        nonlocal bill_date, balance, htparam, bk_veran, artikel, umsatz, billjournal, bediener, guest, debitor

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artnr)).first()

        if artikel.artart == 2 or artikel.artart == 7:
            inv_ar(bill_date)

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + payment

        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = foreign_payment
        billjournal.bezeich = artikel.bezeich + " *BQT" + to_string(veran_nr)
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if artikel.pricetab:
            billjournal.betrag = foreign_payment
        else:
            billjournal.betrag = payment

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.departement = artikel.departement
            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.betrag = umsatz.betrag - payment
        umsatz.anzahl = umsatz.anzahl + 1
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.artnr = depoart
        billjournal.departement = artikel.departement
        billjournal.billjou_ref = artikel.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = - foreign_payment
        billjournal.betrag = - payment
        billjournal.bezeich = depobezeich + " *BQT" + to_string(veran_nr)
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

    def inv_ar(bill_date:date):

        nonlocal bill_date, balance, htparam, bk_veran, artikel, umsatz, billjournal, bediener, guest, debitor

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 997)).first()

        if not htparam.flogical:

            return

        bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()

        guest = db_session.query(Guest).filter(
                    (Guest.gastnr == bk_veran.gastnr)).first()

        artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == artnr)).first()
        debitor = Debitor()
        db_session.add(debitor)

        debitor.artnr = artikel.artnr


        debitor.gastnr = bk_veran.gastnr
        debitor.gastnrmember = bk_veran.gastnr
        debitor.saldo = - payment
        debitor.transzeit = get_current_time_in_seconds()
        debitor.rgdatum = bill_date
        debitor.bediener_nr = bediener.nr
        debitor.vesrcod = "Banquet Deposit Refund"
        debitor.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma


    deposit_refund()

    return generate_output()