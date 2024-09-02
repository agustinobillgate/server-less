from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Htparam, L_ophdr, L_artikel, L_untergrup, L_op, L_ophis

def prepare_gl_detailoutgoingbl(fibu:str, from_date:date, bemerk:str):
    close_date = None
    t_gl_acct_list = []
    s_list_list = []
    gl_acct = htparam = l_ophdr = l_artikel = l_untergrup = l_op = l_ophis = None

    s_list = t_gl_acct = gl_acc1 = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":str, "einzelpreis":decimal, "anzahl":decimal, "warenwert":decimal, "stornogrund":str, "lscheinnr":str, "lflag":bool})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)

    Gl_acc1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal gl_acc1


        nonlocal s_list, t_gl_acct, gl_acc1
        nonlocal s_list_list, t_gl_acct_list
        return {"close_date": close_date, "t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal gl_acc1


        nonlocal s_list, t_gl_acct, gl_acc1
        nonlocal s_list_list, t_gl_acct_list

        lscheinnr:str = ""
        lbezeich:str = ""
        delta:decimal = 0
        Gl_acc1 = Gl_acct
        lscheinnr = entry(3, bemerk, ";")
        lbezeich = substring(entry(0, bemerk, ";") , len(lscheinnr) + 5 - 1, len(bemerk))

        l_op_obj_list = []
        for l_op, l_ophdr, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, L_artikel, L_untergrup).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_op.pos > 0) &  (L_op.op_art == 3) &  (L_op.loeschflag < 2) &  (L_op.datum == from_date) &  (L_op.lager_nr > 0) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower())).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            delta = l_op.warenwert - warenwert

            if delta < 0:
                delta = - delta
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_op, s_list)

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == l_op.stornogrund)).first()

                if not gl_acc1:

                    gl_acc1 = db_session.query(Gl_acc1).filter(
                            (Gl_acc1.fibukonto == l_ophdr.fibukonto)).first()
            else:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acc1:

                    gl_acc1 = db_session.query(Gl_acc1).filter(
                            (Gl_acc1.fibukonto == l_artikel.fibukonto)).first()

            if gl_acc1:
                s_list.stornogrund = gl_acc1.fibukonto


            s_list.bezeich = l_artikel.bezeich

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                s_list.lflag = (fibu == gl_acc1.fibukonto)
            else:
                s_list.lflag = ((lbezeich == l_artikel.bezeich) and delta <= 0.01)

    def disp_hist():

        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal gl_acc1


        nonlocal s_list, t_gl_acct, gl_acc1
        nonlocal s_list_list, t_gl_acct_list

        lscheinnr:str = ""
        lbezeich:str = ""
        delta:decimal = 0
        Gl_acc1 = Gl_acct
        lscheinnr = entry(3, bemerk, ";")
        lbezeich = substring(entry(0, bemerk, ";") , len(lscheinnr) + 5 - 1, len(bemerk))

        l_ophis_obj_list = []
        for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (func.lower(L_ophis.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_ophis.op_art == 3) &  (L_ophis.datum == from_date)).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)


            delta = l_ophis.warenwert - warenwert

            if delta < 0:
                delta = - delta
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_ophis, s_list)

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == l_ophis.fibukonto)).first()

                if not gl_acc1:

                    gl_acc1 = db_session.query(Gl_acc1).filter(
                            (Gl_acc1.fibukonto == l_ophhis.fibukonto)).first()
            else:

                gl_acc1 = db_session.query(Gl_acc1).filter(
                        (Gl_acc1.fibukonto == l_untergrup.fibukonto)).first()

                if not gl_acc1:

                    gl_acc1 = db_session.query(Gl_acc1).filter(
                            (Gl_acc1.fibukonto == l_artikel.fibukonto)).first()

            if gl_acc1:
                s_list.stornogrund = gl_acc1.fibukonto


            s_list.bezeich = l_artikel.bezeich

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                s_list.lflag = (fibu == gl_acc1.fibukonto)
            else:
                s_list.lflag = ((lbezeich == l_artikel.bezeich) and delta <= 0.01)


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    close_date = htparam.fdate

    if from_date >= date_mdy(get_month(close_date) , 1, get_year(close_date)):
        disp_it()
    else:
        disp_hist()

    return generate_output()