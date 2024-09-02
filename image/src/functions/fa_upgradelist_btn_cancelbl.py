from functions.additional_functions import *
import decimal
from datetime import date
from models import Fa_artikel, Htparam, Fa_op

def fa_upgradelist_btn_cancelbl(mat_buff_nr:int, recid_fa_artikel:int, user_init:str):
    err_no = 0
    last_depn:date = None
    fa_artikel = htparam = fa_op = None

    fa_buff = None

    Fa_buff = Fa_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, last_depn, fa_artikel, htparam, fa_op
        nonlocal fa_buff


        nonlocal fa_buff
        return {"err_no": err_no}

    def cancel_upgrade():

        nonlocal err_no, last_depn, fa_artikel, htparam, fa_op
        nonlocal fa_buff


        nonlocal fa_buff

        fa_op = db_session.query(Fa_op).first()
        fa_op.loeschflag = 1

        fa_op = db_session.query(Fa_op).first()

        fa_buff = db_session.query(Fa_buff).filter(
                    (Fa_buff.nr == fa_artikel.p_nr)).first()
        fa_buff.warenwert = fa_buff.warenwert - fa_artikel.warenwert
        fa_buff.book_wert = fa_buff.book_wert - fa_artikel.warenwert

        fa_buff = db_session.query(Fa_buff).first()

        fa_artikel = db_session.query(Fa_artikel).first()
        fa_artikel.loeschflag = 0
        fa_artikel.deleted = None
        fa_artikel.DID = user_init
        fa_art.p_nr = 0

        fa_artikel = db_session.query(Fa_artikel).first()
        err_no = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 881)).first()
    last_depn = htparam.fdate

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel._recid == recid_fa_artikel)).first()

    fa_op = db_session.query(Fa_op).filter(
            (Fa_op.opart == 4) &  (Fa_op.nr == mat_buff_nr) &  (Fa_op.datum == fa_artikel.deleted)).first()

    if fa_op.datum < last_depn:
        err_no = 1

        return generate_output()
    cancel_upgrade()

    return generate_output()