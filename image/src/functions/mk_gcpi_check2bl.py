from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi, Gc_piacct, Gl_acct

def mk_gcpi_check2bl(docu_nr:str, pbuff_returnamt:decimal, pbuff_datum2:date, ret_acctno:str):
    fl_err = 0
    gc_pi = gc_piacct = gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_err, gc_pi, gc_piacct, gl_acct


        return {"fl_err": fl_err}


    gc_pi = db_session.query(Gc_pi).filter(
                (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()
    gc_PI.returnAmt = pbuff_returnamt
    gc_PI.datum2 = pbuff_datum2

    gc_piacct = db_session.query(Gc_piacct).filter(
                (gc_PIacct.fibukonto == ret_acctno)).first()

    if gc_PIacct:
        gc_PI.return_fibu = ret_acctno

    gc_pi = db_session.query(Gc_pi).first()


    if pbuff_returnamt != 0:

        gc_piacct = db_session.query(Gc_piacct).filter(
                (gc_PIacct.fibukonto == ret_acctno)).first()

        if not gc_PIacct:
            fl_err = 1

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == ret_acctno)).first()

        if not gl_acct:
            fl_err = 2

            return generate_output()