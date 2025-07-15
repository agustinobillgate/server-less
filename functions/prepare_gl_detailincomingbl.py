#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Htparam, L_orderhdr, L_artikel, L_untergrup, L_op, L_lieferant, L_ophis

def prepare_gl_detailincomingbl(fibu:string, from_date:date, bemerk:string):

    prepare_cache ([Htparam, L_artikel, L_untergrup, L_lieferant])

    close_date = None
    s_list_data = []
    t_gl_acct_data = []
    gl_acct = htparam = l_orderhdr = l_artikel = l_untergrup = l_op = l_lieferant = l_ophis = None

    s_list = t_gl_acct = None

    s_list_data, S_list = create_model("S_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "anzahl":Decimal, "warenwert":Decimal, "firma":string, "docu_nr":string, "lscheinnr":string, "fibu":string, "lief_nr":int, "lflag":bool, "avail_l_ord":bool})
    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, s_list_data, t_gl_acct_data, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_data, t_gl_acct_data

        return {"close_date": close_date, "s-list": s_list_data, "t-gl-acct": t_gl_acct_data}

    def disp_it():

        nonlocal close_date, s_list_data, t_gl_acct_data, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_data, t_gl_acct_data

        lager_nr:int = 0
        lief_nr:int = 0
        docu_nr:string = ""
        lscheinnr:string = ""
        bezeich:string = ""

        if gl_acct.acc_type == 3:

            if bemerk != "":
                lager_nr = to_int(entry(3, bemerk, ";"))
                lief_nr = to_int(entry(4, bemerk, ";"))
                docu_nr = entry(5, bemerk, ";")
                lscheinnr = entry(6, bemerk, ";")
                bezeich = substring(entry(0, bemerk, ";") , length(lscheinnr) + 2 - 1, length(bemerk))


        else:

            if bemerk != " ":
                lager_nr = to_int(entry(2, bemerk, ";"))
                lief_nr = to_int(entry(3, bemerk, ";"))
                docu_nr = entry(4, bemerk, ";")
                lscheinnr = entry(5, bemerk, ";")

        l_op_obj_list = {}
        for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.op_art == 1) & (L_op.loeschflag < 2) & (L_op.datum == from_date) & (L_op.lager_nr == lager_nr) & (L_op.lief_nr == lief_nr) & (L_op.lscheinnr == (lscheinnr).lower())).order_by(L_op.artnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            s_list = S_list()
            s_list_data.append(s_list)

            buffer_copy(l_op, s_list)

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            if not gl_acct:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct:
                s_list.fibu = gl_acct.fibukonto


            s_list.firma = l_lieferant.firma
            s_list.bezeich = l_artikel.bezeich
            s_list.lflag = (bezeich == l_artikel.bezeich)


    def disp_hist():

        nonlocal close_date, s_list_data, t_gl_acct_data, gl_acct, htparam, l_orderhdr, l_artikel, l_untergrup, l_op, l_lieferant, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_data, t_gl_acct_data

        lager_nr:int = 0
        lief_nr:int = 0
        docu_nr:string = ""
        lscheinnr:string = ""
        bezeich:string = ""

        if gl_acct.acc_type == 3:
            lager_nr = to_int(entry(3, bemerk, ";"))
            lief_nr = to_int(entry(4, bemerk, ";"))
            docu_nr = entry(5, bemerk, ";")
            lscheinnr = entry(6, bemerk, ";")
            bezeich = substring(entry(0, bemerk, ";") , length(lscheinnr) + 2 - 1, length(bemerk))
        else:
            lager_nr = to_int(entry(2, bemerk, ";"))
            lief_nr = to_int(entry(3, bemerk, ";"))
            docu_nr = entry(4, bemerk, ";")
            lscheinnr = entry(5, bemerk, ";")

        l_ophis_obj_list = {}
        for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_ophis.lscheinnr == (lscheinnr).lower()) & (L_ophis.op_art == 1) & (L_ophis.datum == from_date) & (L_ophis.lief_nr == lief_nr)).order_by(L_ophis.artnr).all():
            if l_ophis_obj_list.get(l_ophis._recid):
                continue
            else:
                l_ophis_obj_list[l_ophis._recid] = True


            s_list = S_list()
            s_list_data.append(s_list)

            buffer_copy(l_ophis, s_list)

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

            if not gl_acct:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acct:
                s_list.fibu = gl_acct.fibukonto


            s_list.firma = l_lieferant.firma
            s_list.bezeich = l_artikel.bezeich
            s_list.docu_nr = l_ophis.docu_nr
            s_list.lflag = (bezeich == l_artikel.bezeich)

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_data.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    close_date = htparam.fdate

    if from_date >= date_mdy(get_month(close_date) , 1, get_year(close_date)):
        disp_it()
    else:
        disp_hist()

    for s_list in query(s_list_data):

        l_orderhdr = get_cache (L_orderhdr, {"lief_nr": [(eq, s_list.lief_nr)],"docu_nr": [(eq, s_list.docu_nr)],"betriebsnr": [(le, 1)]})

        if l_orderhdr:
            s_list.avail_l_ord = True

    return generate_output()