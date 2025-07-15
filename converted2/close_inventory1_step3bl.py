#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr, L_ophhis

def close_inventory1_step3bl(closedate:date):

    prepare_cache ([L_ophhis])

    l_ophdr = l_ophhis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr, l_ophhis
        nonlocal closedate

        return {}

    def create_ophhis():

        nonlocal l_ophdr, l_ophhis
        nonlocal closedate


        l_ophhis = L_ophhis()
        db_session.add(l_ophhis)

        l_ophhis.datum = l_ophdr.datum
        l_ophhis.op_typ = l_ophdr.op_typ
        l_ophhis.docu_nr = l_ophdr.docu_nr
        l_ophhis.lscheinnr = l_ophdr.lscheinnr
        l_ophhis.fibukonto = l_ophdr.fibukonto


        pass

    l_ophdr = db_session.query(L_ophdr).filter(
             ((L_ophdr.op_typ == ("STI").lower()) | (L_ophdr.op_typ == ("STT").lower()) | (L_ophdr.op_typ == ("WIP").lower())) & (L_ophdr.datum <= closedate)).first()
    while None != l_ophdr:
        pass
        create_ophhis()
        db_session.delete(l_ophdr)

        curr_recid = l_ophdr._recid
        l_ophdr = db_session.query(L_ophdr).filter(
                 ((L_ophdr.op_typ == ("STI").lower()) | (L_ophdr.op_typ == ("STT").lower()) | (L_ophdr.op_typ == ("WIP").lower())) & (L_ophdr.datum <= closedate) & (L_ophdr._recid > curr_recid)).first()

    return generate_output()