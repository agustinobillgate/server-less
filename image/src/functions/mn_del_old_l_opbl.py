from functions.additional_functions import *
import decimal
from models import L_lager, L_op, Fa_op

def mn_del_old_l_opbl():
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
        lscheinnr:str = ""

        for l_lager in db_session.query(L_lager).all():

            l_op = db_session.query(L_op).filter(
                    (L_op.loeschflag == 0) &  (L_op.pos >= 0) &  (L_op.lager_nr == l_lager.lager_nr) &  (L_op.op_art == 1) &  (L_op.lscheinnr == L_op.docu_nr)).first()
            while None != l_op:

                l_op = db_session.query(L_op).first()
                l_op.loeschflag = 1

                l_op = db_session.query(L_op).first()
                i = i + 1


                l_op = db_session.query(L_op).filter(
                        (L_op.loeschflag == 0) &  (L_op.pos >= 0) &  (L_op.lager_nr == l_lager.lager_nr) &  (L_op.op_art == 1) &  (L_op.lscheinnr == L_op.docu_nr)).first()
        j = 0

        fa_op = db_session.query(Fa_op).filter(
                (Fa_op.loeschflag == 0) &  (Fa_op.lscheinnr == Fa_op.docu_nr)).first()
        while None != fa_op:

            fa_op = db_session.query(Fa_op).first()
            fa_op.loeschflag = 1

            fa_op = db_session.query(Fa_op).first()
            j = j + 1

            fa_op = db_session.query(Fa_op).filter(
                        (Fa_op.loeschflag == 0) &  (Fa_op.lscheinnr == Fa_op.docu_nr)).first()


    del_old_l_op()

    return generate_output()