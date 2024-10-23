from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_ophdr, Htparam, L_artikel, L_ophis, L_ophhis

def close_inventory_step2bl(inv_type:int, m_endkum:int, closedate:date):
    firstdate:date = None
    delete_oph:bool = False
    m_datum:date = None
    fb_datum:date = None
    l_op = l_ophdr = htparam = l_artikel = l_ophis = l_ophhis = None

    l_opbuff = l_ophbuff = None

    L_opbuff = create_buffer("L_opbuff",L_op)
    L_ophbuff = create_buffer("L_ophbuff",L_ophdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal firstdate, delete_oph, m_datum, fb_datum, l_op, l_ophdr, htparam, l_artikel, l_ophis, l_ophhis
        nonlocal inv_type, m_endkum, closedate
        nonlocal l_opbuff, l_ophbuff


        nonlocal l_opbuff, l_ophbuff
        return {}

    firstdate = date_mdy(get_month(closedate) , 1, get_year(closedate))

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 221)).first()
    m_datum = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 224)).first()
    fb_datum = htparam.fdate

    l_op = db_session.query(L_op).filter(
             (L_op.datum >= firstdate) & (L_op.datum <= closedate) & (L_op.op_art <= 4)).first()
    while None != l_op:

        l_artikel = db_session.query(L_artikel).filter(
                     (L_artikel.artnr == l_op.artnr)).first()

        if l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or (inv_type == 3)):

            if l_op.loeschflag <= 2:
                l_ophis = L_ophis()
                db_session.add(l_ophis)

                buffer_copy(l_op, l_ophis)

                if l_op.op_art == 3 and l_op.stornogrund != "":
                    l_ophis.fibukonto = l_op.stornogrund

                if l_op.loeschflag == 2:
                    l_ophis.fibukonto = l_op.stornogrund + ";CANCELLED"

                if (l_op.op_art == 2 or l_op.op_art == 4):
                    l_ophis.lief_nr = l_op.pos

            l_opbuff = db_session.query(L_opbuff).filter(
                         (L_opbuff._recid == l_op._recid)).first()
            l_opbuff_list.remove(l_opbuff)
            pass

        elif not l_artikel:

            l_opbuff = db_session.query(L_opbuff).filter(
                         (L_opbuff._recid == l_op._recid)).first()
            l_opbuff_list.remove(l_opbuff)
            pass


        curr_recid = l_op._recid
        l_op = db_session.query(L_op).filter(
                 (L_op.datum >= firstdate) & (L_op.datum <= closedate) & (L_op.op_art <= 4)).filter(L_op._recid > curr_recid).first()

    if inv_type == 1 and fb_datum < m_datum:
        delete_oph = True

    elif inv_type == 2 and m_datum < fb_datum:
        delete_oph = True

    elif inv_type == 3:
        delete_oph = True

    if not delete_oph:

        return generate_output()

    l_ophdr = db_session.query(L_ophdr).filter(
             ((func.lower(L_ophdr.op_typ) == ("STI").lower()) | (func.lower(L_ophdr.op_typ) == ("STT").lower()) | (func.lower(L_ophdr.op_typ) == ("WIP").lower())) & (L_ophdr.datum >= firstdate) & (L_ophdr.datum <= closedate)).first()
    while None != l_ophdr:
        l_ophhis = L_ophhis()
        db_session.add(l_ophhis)

        buffer_copy(l_ophdr, l_ophhis)

        l_ophbuff = db_session.query(L_ophbuff).filter(
                     (L_ophbuff._recid == l_ophdr._recid)).first()
        l_ophbuff_list.remove(l_ophbuff)
        pass


        curr_recid = l_ophdr._recid
        l_ophdr = db_session.query(L_ophdr).filter(
                 ((func.lower(L_ophdr.op_typ) == ("STI").lower()) | (func.lower(L_ophdr.op_typ) == ("STT").lower()) | (func.lower(L_ophdr.op_typ) == ("WIP").lower())) & (L_ophdr.datum >= firstdate) & (L_ophdr.datum <= closedate)).filter(L_ophdr._recid > curr_recid).first()

    return generate_output()