#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Htparam, L_ophdr, L_artikel, L_untergrup, L_op, L_ophis

def prepare_gl_detailoutgoingbl(fibu:string, from_date:date, bemerk:string):

    prepare_cache ([Gl_acct, Htparam, L_ophdr, L_artikel, L_untergrup])

    close_date = None
    t_gl_acct_list = []
    s_list_list = []
    gl_acct = htparam = l_ophdr = l_artikel = l_untergrup = l_op = l_ophis = None

    s_list = t_gl_acct = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "anzahl":Decimal, "warenwert":Decimal, "stornogrund":string, "lscheinnr":string, "lflag":bool})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        return {"close_date": close_date, "t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        lscheinnr:string = ""
        lbezeich:string = ""
        delta:Decimal = to_decimal("0.0")
        gl_acc1 = None
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        lscheinnr = entry(3, bemerk, ";")
        lbezeich = substring(entry(0, bemerk, ";") , length(lscheinnr) + 5 - 1, length(bemerk))

        l_op_obj_list = {}
        for l_op, l_ophdr, l_artikel, l_untergrup in db_session.query(L_op, L_ophdr, L_artikel, L_untergrup).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_op.pos > 0) & (L_op.op_art == 3) & (L_op.loeschflag < 2) & (L_op.datum == from_date) & (L_op.lager_nr > 0) & (L_op.lscheinnr == (lscheinnr).lower())).order_by(L_op.stornogrund, L_op.artnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            delta =  to_decimal(l_op.warenwert) - to_decimal(warenwert)

            if delta < 0:
                delta =  - to_decimal(delta)
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_op, s_list)

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if not gl_acc1:

                    gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)]})
            else:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

                if not gl_acc1:

                    gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acc1:
                s_list.stornogrund = gl_acc1.fibukonto


            s_list.bezeich = l_artikel.bezeich

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                s_list.lflag = (fibu == gl_acc1.fibukonto)
            else:
                s_list.lflag = ((lbezeich == l_artikel.bezeich) and delta <= 0.01)


    def disp_hist():

        nonlocal close_date, t_gl_acct_list, s_list_list, gl_acct, htparam, l_ophdr, l_artikel, l_untergrup, l_op, l_ophis
        nonlocal fibu, from_date, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        lscheinnr:string = ""
        lbezeich:string = ""
        delta:Decimal = to_decimal("0.0")
        gl_acc1 = None
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)
        lscheinnr = entry(3, bemerk, ";")
        lbezeich = substring(entry(0, bemerk, ";") , length(lscheinnr) + 5 - 1, length(bemerk))

        l_ophis_obj_list = {}
        for l_ophis, l_artikel, l_untergrup in db_session.query(L_ophis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_ophis.lscheinnr == (lscheinnr).lower()) & (L_ophis.op_art == 3) & (L_ophis.datum == from_date)).order_by(L_ophis.fibukonto, L_ophis.artnr).all():
            if l_ophis_obj_list.get(l_ophis._recid):
                continue
            else:
                l_ophis_obj_list[l_ophis._recid] = True


            delta =  to_decimal(l_ophis.warenwert) - to_decimal(warenwert)

            if delta < 0:
                delta =  - to_decimal(delta)
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_ophis, s_list)

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                if not gl_acc1:

                    gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophhis.fibukonto)]})
            else:

                gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_untergrup.fibukonto)]})

                if not gl_acc1:

                    gl_acc1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

            if gl_acc1:
                s_list.stornogrund = gl_acc1.fibukonto


            s_list.bezeich = l_artikel.bezeich

            if gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                s_list.lflag = (fibu == gl_acc1.fibukonto)
            else:
                s_list.lflag = ((lbezeich == l_artikel.bezeich) and delta <= 0.01)

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    close_date = htparam.fdate

    if from_date >= date_mdy(get_month(close_date) , 1, get_year(close_date)):
        disp_it()
    else:
        disp_hist()

    return generate_output()