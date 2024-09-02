from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_ophdr, L_ophhis

def close_inventory1_step3bl(closedate:date):
    l_ophdr = l_ophhis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr, l_ophhis


        return {}

    def create_ophhis():

        nonlocal l_ophdr, l_ophhis


        l_ophhis = L_ophhis()
        db_session.add(l_ophhis)

        l_ophhis.datum = l_ophdr.datum
        l_ophhis.op_typ = l_ophdr.op_typ
        l_ophhis.docu_nr = l_ophdr.docu_nr
        l_ophhis.lscheinnr = l_ophdr.lscheinnr
        l_ophhis.fibukonto = l_ophdr.fibukonto

        l_ophhis = db_session.query(L_ophhis).first()


    l_ophdr = db_session.query(L_ophdr).filter(
            ((func.lower(L_ophdr.op_typ) == "STI") |  (func.lower(L_ophdr.op_typ) == "STT") |  (func.lower(L_ophdr.op_typ) == "WIP")) &  (L_ophdr.datum <= closedate)).first()
    while None != l_ophdr:

        l_ophdr = db_session.query(L_ophdr).first()
        create_ophhis()
        db_session.delete(l_ophdr)

        l_ophdr = db_session.query(L_ophdr).filter(
                ((func.lower(L_ophdr.op_typ) == "STI") |  (func.lower(L_ophdr.op_typ) == "STT") |  (func.lower(L_ophdr.op_typ) == "WIP")) &  (L_ophdr.datum <= closedate)).first()

    return generate_output()