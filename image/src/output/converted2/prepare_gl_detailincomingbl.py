from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Htparam, L_orderhdr, L_artikel, L_untergrup, L_op, L_lieferant, L_ophis

def prepare_gl_detailincomingbl(fibu:str, from_date:date, bemerk:str):
    close_date = None
    s_list_list = []
    t_gl_acct_list = []
    gl_acct = htparam = l_orderhdr = l_artikel = l_untergrup = l_op = l_lieferant = l_ophis = None

    s_list = t_gl_acct = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":str, "einzelpreis":decimal, "anzahl":decimal, "warenwert":decimal, "firma":str, "docu_nr":str, "lscheinnr":str, "fibu":str, "lief_nr":int, "lflag":bool, "avail_l_ord":bool})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, s_list_list, t_gl_acct_list, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        return {"close_date": close_date, "s-list": s_list_list, "t-gl-acct": t_gl_acct_list}

    def disp_it():

        nonlocal close_date, s_list_list, t_gl_acct_list, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        lager_nr:int = 0
        lief_nr:int = 0
        docu_nr:str = ""
        lscheinnr:str = ""
        bezeich:str = ""

        if gl_acct.acc_type == 3:

            if bemerk != "":
                lager_nr = to_int(entry(3, bemerk, ";"))
                lief_nr = to_int(entry(4, bemerk, ";"))
                docu_nr = entry(5, bemerk, ";")
                lscheinnr = entry(6, bemerk, ";")
                bezeich = substring(entry(0, bemerk, ";") , len(lscheinnr) + 2 - 1, len(bemerk))


        else:

            if bemerk != " ":
                lager_nr = to_int(entry(2, bemerk, ";"))
                lief_nr = to_int(entry(3, bemerk, ";"))
                docu_nr = entry(4, bemerk, ";")
                lscheinnr = entry(5, bemerk, ";")

        l_op_obj_list = []
        for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.op_art == 1) & (L_op.loeschflag < 2) & (L_op.datum == from_date) & (L_op.lager_nr == lager_nr) & (L_op.lief_nr == lief_nr) & (func.lower(L_op.lscheinnr) == (lscheinnr).lower())).order_by(L_op.artnr).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_op, s_list)

            l_lieferant = db_session.query(L_lieferant).filter(
                     (L_lieferant.lief_nr == l_op.lief_nr)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            if not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

            if gl_acct:
                s_list.fibu = gl_acct.fibukonto


            s_list.firma = l_lieferant.firma
            s_list.bezeich = l_artikel.bezeich
            s_list.lflag = (bezeich == l_artikel.bezeich)


    def disp_hist():

        nonlocal close_date, s_list_list, t_gl_acct_list, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        lager_nr:int = 0
        lief_nr:int = 0
        docu_nr:str = ""
        lscheinnr:str = ""
        bezeich:str = ""

        if gl_acct.acc_type == 3:
            lager_nr = to_int(entry(3, bemerk, ";"))
            lief_nr = to_int(entry(4, bemerk, ";"))
            docu_nr = entry(5, bemerk, ";")
            lscheinnr = entry(6, bemerk, ";")
            bezeich = substring(entry(0, bemerk, ";") , len(lscheinnr) + 2 - 1, len(bemerk))
        else:
            lager_nr = to_int(entry(2, bemerk, ";"))
            lief_nr = to_int(entry(3, bemerk, ";"))
            docu_nr = entry(4, bemerk, ";")
            lscheinnr = entry(5, bemerk, ";")

        l_ophis_obj_list = []
        for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (func.lower(L_ophis.lscheinnr) == (lscheinnr).lower()) & (L_ophis.op_art == 1) & (L_ophis.datum == from_date) & (L_ophis.lief_nr == lief_nr)).order_by(L_ophis.artnr).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)


            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_ophis, s_list)

            l_lieferant = db_session.query(L_lieferant).filter(
                     (L_lieferant.lief_nr == l_ophis.lief_nr)).first()

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == l_untergrup.fibukonto)).first()

            if not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == l_artikel.fibukonto)).first()

            if gl_acct:
                s_list.fibu = gl_acct.fibukonto


            s_list.firma = l_lieferant.firma
            s_list.bezeich = l_artikel.bezeich
            s_list.docu_nr = l_ophis.docu_nr
            s_list.lflag = (bezeich == l_artikel.bezeich)

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

    for s_list in query(s_list_list):

        l_orderhdr = db_session.query(L_orderhdr).filter(
                 (L_orderhdr.lief_nr == s_list.lief_nr) & (L_orderhdr.docu_nr == s_list.docu_nr) & (L_orderhdr.betriebsnr <= 1)).first()

        if l_orderhdr:
            s_list.avail_l_ord = True

    return generate_output()