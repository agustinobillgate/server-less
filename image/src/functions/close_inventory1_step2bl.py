from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lager, L_op, L_artikel, L_ophhis, L_ophis

def close_inventory1_step2bl(inv_type:int, m_endkum:int, closedate:date):
    l_lager = l_op = l_artikel = l_ophhis = l_ophis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis


        return {}

    def close_op(lager_nr:int):

        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis

        l_op = db_session.query(L_op).filter(
                (L_op.lager_nr == lager_nr) &  (L_op.datum <= closedate) &  (L_op.op_art <= 5)).first()
        while None != l_op:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()

            if not l_artikel:

                l_op = db_session.query(L_op).first()
                db_session.delete(l_op)

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):

                l_op = db_session.query(L_op).first()

                if (l_op.op_art >= 1 and l_op.op_art <= 4) and l_op.lager_nr != 0:
                    create_ophis()
                db_session.delete(l_op)

            l_op = db_session.query(L_op).filter(
                    (L_op.lager_nr == lager_nr) &  (L_op.datum <= closedate) &  (L_op.op_art <= 5)).first()

    def create_ophhis():

        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis


        l_ophhis = L_ophhis()
        db_session.add(l_ophhis)

        l_ophhis.datum = l_ophdr.datum
        l_ophhis.op_typ = l_ophdr.op_typ
        l_ophhis.docu_nr = l_ophdr.docu_nr
        l_ophhis.lscheinnr = l_ophdr.lscheinnr
        l_ophhis.fibukonto = l_ophdr.fibukonto

        l_ophhis = db_session.query(L_ophhis).first()

    def create_ophis():

        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis


        l_ophis = L_ophis()
        db_session.add(l_ophis)

        l_ophis.lief_nr = l_op.lief_nr
        l_ophis.lager_nr = l_op.lager_nr
        l_ophis.artnr = l_op.artnr
        l_ophis.op_art = l_op.op_art
        l_ophis.datum = l_op.datum
        l_ophis.docu_nr = l_op.docu_nr
        l_ophis.lscheinnr = l_op.lscheinnr
        l_ophis.anzahl = l_op.anzahl
        l_ophis.einzelpreis = l_op.einzelpreis
        l_ophis.warenwert = l_op.warenwert

        if l_op.op_art == 3 and l_op.stornogrund != "":
            l_ophis.fibukonto = l_op.stornogrund

        if (l_op.op_art == 2 or l_op.op_art == 4):
            l_ophis.lief_nr = l_op.pos

        if l_op.loeschflag == 2:
            l_ophis.fibukonto = l_op.stornogrund + ";CANCELLED"

        l_ophis = db_session.query(L_ophis).first()


    for l_lager in db_session.query(L_lager).all():
        close_op(l_lager.lager_nr)
    close_op(0)

    return generate_output()