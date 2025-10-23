#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_lager, L_op, Fa_op

def mn_del_old_l_opbl():

    prepare_cache ([L_lager])

    i = 0
    j = 0
    l_lager = l_op = fa_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, l_lager, l_op, fa_op

        return {"i": i, "j": j}

    def del_old_l_op():

        nonlocal i, j, l_lager, l_op, fa_op

        anz:int = 0
        lscheinnr:string = ""

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            # l_op = get_cache (L_op, {"loeschflag": [(eq, 0)],"pos": [(ge, 0)],"lager_nr": [(eq, l_lager.lager_nr)],"op_art": [(eq, 1)],"lscheinnr": [(eq, l_op.docu_nr)]})
            l_op = db_session.query(L_op).filter(
                        (L_op.loeschflag == 0) & (L_op.pos >= 0) & (L_op.lager_nr == l_lager.lager_nr) & (L_op.op_art == 1) & (L_op.lscheinnr == L_op.docu_nr)).order_by(L_op._recid).first()
            while None != l_op:
                pass
                l_op.loeschflag = 1
                pass
                i = i + 1

                curr_recid = l_op._recid
                l_op = db_session.query(L_op).filter(
                         (L_op.loeschflag == 0) & (L_op.pos >= 0) & (L_op.lager_nr == l_lager.lager_nr) & (L_op.op_art == 1) & (L_op.lscheinnr == L_op.docu_nr) & (L_op._recid > curr_recid)).first()
        j = 0

        # fa_op = get_cache (Fa_op, {"loeschflag": [(eq, 0)],"lscheinnr": [(eq, fa_op.docu_nr)]})
        fa_op = db_session.query(Fa_op).filter(
                     (Fa_op.loeschflag == 0) & (Fa_op.lscheinnr == Fa_op.docu_nr)).order_by(Fa_op._recid).first()
        while None != fa_op:
            pass
            fa_op.loeschflag = 1
            pass
            j = j + 1

            curr_recid = fa_op._recid
            fa_op = db_session.query(Fa_op).filter(
                         (Fa_op.loeschflag == 0) & (Fa_op.lscheinnr == Fa_op.docu_nr) & (Fa_op._recid > curr_recid)).first()


    del_old_l_op()

    return generate_output()