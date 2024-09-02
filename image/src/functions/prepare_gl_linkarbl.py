from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Guest, Artikel

def prepare_gl_linkarbl(combo_pf_file1:str, combo_pf_file2:str, combo_gastnr:int, combo_ledger:int, combo_gl_link:bool):
    f_int = 0
    last_acctdate = None
    from_date = None
    acct_date = None
    close_year = None
    htparam = guest = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, last_acctdate, from_date, acct_date, close_year, htparam, guest, artikel


        return {"f_int": f_int, "last_acctdate": last_acctdate, "from_date": from_date, "acct_date": acct_date, "close_year": close_year}


    if combo_gastnr == None:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 155)).first()
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == combo_gastnr)).first()

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == combo_ledger) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).first()

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 339)).first()
        combo_pf_file1 = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 340)).first()
        combo_pf_file2 = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 343)).first()
        combo_gl_link = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1014)).first()
    last_acctdate = htparam.fdate
    from_date = last_acctdate + 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    return generate_output()