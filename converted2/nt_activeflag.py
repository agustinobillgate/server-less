from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Artikel, H_artikel

def nt_activeflag():
    lvcarea:str = "nt-activeflag"
    bill_date:date = None
    htparam = hoteldpt = artikel = h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, bill_date, htparam, hoteldpt, artikel, h_artikel

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

        artikel = db_session.query(Artikel).filter(
                 (Artikel.departement == hoteldpt.num)).first()
        while None != artikel:

            if artikel.activeflag:

                if artikel.s_gueltig != None and artikel.e_gueltig != None:

                    if bill_date < artikel.s_gueltig or bill_date > artikel.e_gueltig:
                        artikel.activeflag = False

            elif not artikel.activeflag:

                if artikel.s_gueltig != None and artikel.e_gueltig != None:

                    if bill_date >= artikel.s_gueltig and bill_date <= artikel.e_gueltig:
                        artikel.activeflag = True

            curr_recid = artikel._recid
            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == hoteldpt.num) & (Artikel._recid > curr_recid)).first()

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.departement == hoteldpt.num)).first()
        while None != h_artikel:

            if h_artikel.activeflag:

                if h_artikel.s_gueltig != None and h_artikel.e_gueltig != None:

                    if bill_date < h_artikel.s_gueltig or bill_date > h_artikel.e_gueltig:
                        h_artikel.activeflag = False

            elif not h_artikel.activeflag:

                if h_artikel.s_gueltig != None and h_artikel.e_gueltig != None:

                    if bill_date >= h_artikel.s_gueltig and bill_date <= h_artikel.e_gueltig:
                        h_artikel.activeflag = True

            curr_recid = h_artikel._recid
            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num) & (H_artikel._recid > curr_recid)).first()

    return generate_output()