from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi, Gc_pitype

def mk_gcpi_go1abl(pbuff:[Pbuff], pi_type:str, pay_type:str, pay_acctno:str, rcvname:str, bemerk:str, pi_number:str):
    gc_pi = gc_pitype = None

    pbuff = None

    pbuff_list, Pbuff = create_model_like(Gc_pi)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi, gc_pitype


        nonlocal pbuff
        nonlocal pbuff_list
        return {}

    pbuff = query(pbuff_list, first=True)

    gc_pitype = db_session.query(Gc_pitype).filter(
            (func.lower(Gc_pitype.bezeich) == (pi_type).lower())).first()

    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.docu_nr) == (pi_number).lower())).first()

    gc_pi = db_session.query(Gc_pi).first()
    buffer_copy(pbuff, gc_pi)
    gc_PI.rcvname = rcvname
    gc_PI.bemerk = bemerk
    gc_PI.pay_type = to_int(substring(pay_type, 0, 1))
    gc_PI.credit_fibu = pay_acctno
    gc_pi.pi_type = gc_pitype.nr

    return generate_output()