#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, L_op, L_artikel, L_ophhis, L_ophis, Queasy

def close_inventory1_step2bl(inv_type:int, m_endkum:int, closedate:date):

    prepare_cache ([L_artikel, L_ophhis, L_ophis, Queasy])

    l_lager = l_op = l_artikel = l_ophhis = l_ophis = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis, queasy
        nonlocal inv_type, m_endkum, closedate

        return {}

    def close_op(lager_nr:int):

        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis, queasy
        nonlocal inv_type, m_endkum, closedate

        l_op = db_session.query(L_op).filter(
                 (L_op.lager_nr == lager_nr) & (L_op.datum <= closedate) & (L_op.op_art <= 5)).order_by(L_op._recid).first()
        
        while None != l_op:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

            if not l_artikel:
                db_session.refresh(l_op, with_for_update=True)
                db_session.delete(l_op)
                db_session.flush()

            elif l_artikel and ((inv_type == 1 and l_artikel.endkum < m_endkum) or (inv_type == 2 and l_artikel.endkum >= m_endkum) or inv_type == 3):
                db_session.refresh(l_op, with_for_update=True)

                if (l_op.op_art >= 1 and l_op.op_art <= 4) and l_op.lager_nr != 0:
                    create_ophis()

                db_session.delete(l_op)

                db_session.flush()

            curr_recid = l_op._recid
            l_op = db_session.query(L_op).filter(
                     (L_op.lager_nr == lager_nr) & (L_op.datum <= closedate) & (L_op.op_art <= 5) & (L_op._recid > curr_recid)).first()


# Rulita, 17-10-2025
# Dont used in progress program 
    # def create_ophhis():

    #     nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis, queasy
    #     nonlocal inv_type, m_endkum, closedate

    #     l_ophhis = L_ophhis()
    #     db_session.add(l_ophhis)

    #     l_ophhis.datum = l_ophdr.datum
    #     l_ophhis.op_typ = l_ophdr.op_typ
    #     l_ophhis.docu_nr = l_ophdr.docu_nr
    #     l_ophhis.lscheinnr = l_ophdr.lscheinnr
    #     l_ophhis.fibukonto = l_ophdr.fibukonto

    #     pass


    def create_ophis():

        nonlocal l_lager, l_op, l_artikel, l_ophhis, l_ophis, queasy
        nonlocal inv_type, m_endkum, closedate


        l_ophis = L_ophis()
        db_session.add(l_ophis)

        l_ophis.lief_nr = l_op.lief_nr
        l_ophis.lager_nr = l_op.lager_nr
        l_ophis.artnr = l_op.artnr
        l_ophis.op_art = l_op.op_art
        l_ophis.datum = l_op.datum
        l_ophis.docu_nr = l_op.docu_nr
        l_ophis.lscheinnr = l_op.lscheinnr
        l_ophis.anzahl =  to_decimal(l_op.anzahl)
        l_ophis.einzelpreis =  to_decimal(l_op.einzelpreis)
        l_ophis.warenwert =  to_decimal(l_op.warenwert)

        if l_op.op_art == 3 and l_op.stornogrund != "":
            l_ophis.fibukonto = l_op.stornogrund

        if (l_op.op_art == 2 or l_op.op_art == 4):
            l_ophis.lief_nr = l_op.pos

        if l_op.loeschflag == 2:
            l_ophis.fibukonto = l_op.stornogrund + ";CANCELLED"


        pass

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 363) & (Queasy.char1 == l_op.docu_nr) & (Queasy.char2 == l_op.lscheinnr) & (Queasy.number1 == l_op.artnr)).with_for_update().first()

        if queasy:
            queasy.deci1 =  to_decimal(l_op.deci1[0])
            queasy.number2 = l_op.fuellflag
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 363
            queasy.char1 = l_op.docu_nr
            queasy.char2 = l_op.lscheinnr
            queasy.number1 = l_op.artnr
            queasy.number2 = l_op.fuellflag
            queasy.deci1 =  to_decimal(l_op.deci1[0])

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        close_op(l_lager.lager_nr)
        
    close_op(0)

    return generate_output()