#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lager, L_op, L_artikel, L_ophdr, Parameters, L_bestand, Bediener, Gl_acct, Queasy

def storereq_list_create_list_2_webbl(from_date:date, to_date:date, from_dept:int, to_dept:int, curr_lschein:string, show_price:bool):

    prepare_cache ([Htparam, L_lager, L_op, L_artikel, L_ophdr, Parameters, L_bestand, Bediener, Gl_acct, Queasy])

    it_exist = False
    t_list_list = []
    sr_remark_list_list = []
    appflag:bool = False
    long_digit:bool = False
    htparam = l_lager = l_op = l_artikel = l_ophdr = parameters = l_bestand = bediener = gl_acct = queasy = None

    t_list = sr_remark_list = None

    t_list_list, T_list = create_model("T_list", {"s_recid":int, "t_status":int, "datum":date, "deptno":int, "lager_nr":int, "to_stock":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "deptname":string, "lscheinnr":string, "f_bezeich":string, "t_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "content":Decimal, "price":string, "qty":Decimal, "qty1":Decimal, "val":Decimal, "fibukonto":string, "id":string, "appstr":string, "appflag":bool, "stornogrund":string, "gl_bezeich":string, "art_bezeich":string, "art_lief_einheit":int, "art_traubensort":string, "zwkum":int, "endkum":int, "centername":string, "stock_oh":Decimal, "total":Decimal, "issue_date":date, "approved_by":string})
    sr_remark_list_list, Sr_remark_list = create_model("Sr_remark_list", {"lscheinnr":string, "sr_remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_list, sr_remark_list_list, appflag, long_digit, htparam, l_lager, l_op, l_artikel, l_ophdr, parameters, l_bestand, bediener, gl_acct, queasy
        nonlocal from_date, to_date, from_dept, to_dept, curr_lschein, show_price


        nonlocal t_list, sr_remark_list
        nonlocal t_list_list, sr_remark_list_list

        return {"it_exist": it_exist, "t-list": t_list_list, "sr-remark-list": sr_remark_list_list}

    def create_list():

        nonlocal it_exist, t_list_list, sr_remark_list_list, long_digit, htparam, l_lager, l_op, l_artikel, l_ophdr, parameters, l_bestand, bediener, gl_acct, queasy
        nonlocal from_date, to_date, from_dept, to_dept, curr_lschein, show_price


        nonlocal t_list, sr_remark_list
        nonlocal t_list_list, sr_remark_list_list

        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        qty1:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_qty1:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        do_it:bool = False
        deptno:int = 0
        deptname:string = ""
        appflag:bool = False
        curr_centername:string = ""
        amount:Decimal = to_decimal("0.0")
        t_amount:Decimal = to_decimal("0.0")
        l_store = None
        tl_op = None
        L_store =  create_buffer("L_store",L_lager)
        Tl_op =  create_buffer("Tl_op",L_op)
        it_exist = False
        t_list_list.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        qty1 =  to_decimal("0")
        amount =  to_decimal("0")
        lscheinnr = ""

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.lscheinnr, l_op.lager_nr, l_op.pos, l_op.reorgflag, l_op._recid, l_op.herkunftflag, l_op.datum, l_op.anzahl, l_op.deci1, l_op.einzelpreis, l_op.warenwert, l_op.artnr, l_op.stornogrund, l_op.op_art, l_op.loeschflag, l_op.fuellflag, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.lief_einheit, l_artikel.traubensorte, l_artikel.zwkum, l_artikel.endkum, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.lager_nr, L_op.pos, L_op.reorgflag, L_op._recid, L_op.herkunftflag, L_op.datum, L_op.anzahl, L_op.deci1, L_op.einzelpreis, L_op.warenwert, L_op.artnr, L_op.stornogrund, L_op.op_art, L_op.loeschflag, L_op.fuellflag, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.lief_einheit, L_artikel.traubensorte, L_artikel.zwkum, L_artikel.endkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.reorgflag >= from_dept) & (L_op.reorgflag <= to_dept) & (L_op.op_art >= 13) & (L_op.op_art <= 14) & (L_op.herkunftflag <= 2) & (L_op.loeschflag <= 1)).order_by(L_op.reorgflag, L_op.lscheinnr, L_op.zeit).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            appflag = False

            l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "req")],"lscheinnr": [(eq, l_op.lscheinnr)],"docu_nr": [(eq, l_op.lscheinnr)]})

            if l_ophdr:
                appflag = l_ophdr.betriebsnr != 0
            do_it = True

            if curr_lschein != "":
                do_it = l_op.lscheinnr == curr_lschein

            if do_it:
                it_exist = True
                pass

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                if l_op.op_art == 14:

                    l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    t_list.qty1 =  to_decimal(qty1)
                    t_list.total =  to_decimal(amount)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                    qty1 =  to_decimal("0")
                    amount =  to_decimal("0")
                lscheinnr = l_op.lscheinnr

                if l_op.reorgflag != deptno:
                    deptno = l_op.reorgflag

                    parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.deptno = deptno

                    if parameters:
                        t_list.bezeich = parameters.vstring
                        curr_centername = parameters.vstring


                    else:
                        t_list.bezeich = "???"
                        curr_centername = "???"


                t_list = T_list()
                t_list_list.append(t_list)

                add_id()
                t_list.s_recid = l_op._recid
                t_list.deptno = deptno
                t_list.t_status = l_op.herkunftflag
                t_list.datum = l_op.datum
                t_list.lager_nr = l_op.lager_nr
                t_list.to_stock = l_op.pos
                t_list.anzahl =  to_decimal(l_op.anzahl)
                t_list.qty1 =  to_decimal(l_op.deci1[0])
                t_list.einzelpreis =  to_decimal(l_op.einzelpreis)
                t_list.warenwert =  to_decimal(l_op.warenwert)
                t_list.lscheinnr = lscheinnr
                t_list.f_bezeich = l_lager.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content =  to_decimal(l_artikel.inhalt)
                t_list.appflag = appflag
                t_list.stornogrund = l_op.stornogrund
                t_list.art_bezeich = l_artikel.bezeich
                t_list.art_lief_einheit = l_artikel.lief_einheit
                t_list.art_traubensort = l_artikel.traubensorte
                t_list.zwkum = l_artikel.zwkum
                t_list.endkum = l_artikel.endkum
                t_list.centername = curr_centername

                tl_op = get_cache (L_op, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_art": [(eq, 3)],"loeschflag": [(le, 1)]})

                if tl_op:
                    t_list.issue_date = tl_op.datum

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})

                if l_bestand:
                    t_list.stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                t_list.deptname = l_lager.bezeich

                if l_op.op_art == 14:
                    t_list.deptname = l_store.bezeich

                if appflag:
                    t_list.appstr = "Y"

                    bediener = get_cache (Bediener, {"nr": [(eq, l_ophdr.betriebsnr)]})

                    if bediener:
                        t_list.approved_by = to_string(bediener.userinit) + ", " + bediener.username

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.op_art == 13:
                    t_list.to_stock = 0

                if l_op.op_art == 13 and trim(l_op.stornogrund) != "":

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                    if not gl_acct:

                        gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, l_op.stornogrund)]})

                    if gl_acct:
                        t_list.fibukonto = gl_acct.fibukonto
                        t_list.gl_bezeich = gl_acct.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not long_digit:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>,>>>,>>9.99")
                    else:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">,>>>,>>>,>>9")
                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                qty1 =  to_decimal(qty1) + to_decimal(l_op.deci1[0])
                t_list.qty =  to_decimal(l_op.anzahl)
                t_list.qty1 =  to_decimal(l_op.deci1[0])
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
                t_qty1 =  to_decimal(t_qty1) + to_decimal(l_op.deci1[0])
                t_list.total =  to_decimal(decimal (t_list.price)) * to_decimal(t_list.qty)
                amount =  to_decimal(amount) + to_decimal(t_list.total)
                t_amount =  to_decimal(t_amount) + to_decimal(t_list.total)

                if show_price:
                    t_list.val =  to_decimal(l_op.warenwert)
                    val =  to_decimal(val) + to_decimal(l_op.warenwert)
                    t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)

                sr_remark_list = query(sr_remark_list_list, filters=(lambda sr_remark_list: sr_remark_list.lscheinnr == l_op.lscheinnr), first=True)

                if not sr_remark_list:
                    sr_remark_list = Sr_remark_list()
                    sr_remark_list_list.append(sr_remark_list)


                    queasy = get_cache (Queasy, {"key": [(eq, 343)],"char1": [(eq, l_op.lscheinnr)]})

                    if queasy:
                        sr_remark_list.lscheinnr = l_op.lscheinnr
                        sr_remark_list.sr_remark = queasy.char2


                    else:
                        sr_remark_list.lscheinnr = l_op.lscheinnr
                        sr_remark_list.sr_remark = ""

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.qty1 =  to_decimal(qty1)
            t_list.val =  to_decimal(val)
            t_list.total =  to_decimal(amount)

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.qty1 =  to_decimal(t_qty1)
            t_list.val =  to_decimal(t_val)
            t_list.total =  to_decimal(t_amount)


        pass


    def add_id():

        nonlocal it_exist, t_list_list, sr_remark_list_list, appflag, long_digit, htparam, l_lager, l_op, l_artikel, l_ophdr, parameters, l_bestand, bediener, gl_acct, queasy
        nonlocal from_date, to_date, from_dept, to_dept, curr_lschein, show_price


        nonlocal t_list, sr_remark_list
        nonlocal t_list_list, sr_remark_list_list

        usr = None
        Usr =  create_buffer("Usr",Bediener)

        usr = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

        if usr:
            t_list.id = usr.userinit
        else:
            t_list.id = "??"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    create_list()

    return generate_output()