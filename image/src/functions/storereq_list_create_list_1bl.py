from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_lager, L_artikel, L_op, L_ophdr, Parameters, Gl_acct, Bediener

def storereq_list_create_list_1bl(from_date:date, to_date:date, from_dept:int, to_dept:int, curr_lschein:str, show_price:bool):
    it_exist = False
    t_list_list = []
    appflag:bool = False
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_op = l_ophdr = parameters = gl_acct = bediener = None

    t_list = l_store = usr = None

    t_list_list, T_list = create_model("T_list", {"s_recid":int, "t_status":int, "datum":date, "deptno":int, "lager_nr":int, "to_stock":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "deptname":str, "lscheinnr":str, "f_bezeich":str, "t_bezeich":str, "artnr":str, "bezeich":str, "einheit":str, "content":decimal, "price":str, "qty":decimal, "qty1":decimal, "val":decimal, "fibukonto":str, "id":str, "appstr":str, "appflag":bool, "stornogrund":str, "gl_bezeich":str, "art_bezeich":str, "art_lief_einheit":int, "art_traubensort":str, "zwkum":int, "endkum":int, "centername":str})

    L_store = L_lager
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_list, appflag, long_digit, htparam, l_lager, l_artikel, l_op, l_ophdr, parameters, gl_acct, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list
        return {"it_exist": it_exist, "t-list": t_list_list}

    def create_list():

        nonlocal it_exist, t_list_list, appflag, long_digit, htparam, l_lager, l_artikel, l_op, l_ophdr, parameters, gl_acct, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        lscheinnr:str = ""
        qty:decimal = 0
        qty1:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_qty1:decimal = 0
        t_val:decimal = 0
        do_it:bool = False
        deptno:int = 0
        deptname:str = ""
        appflag:bool = False
        curr_centername:str = ""
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        qty1 = 0
        lscheinnr = ""

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.reorgflag >= from_dept) &  (L_op.reorgflag <= to_dept) &  (L_op.op_art >= 13) &  (L_op.op_art <= 14) &  (L_op.herkunftflag <= 2) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            appflag = False

            l_ophdr = db_session.query(L_ophdr).filter(
                    (func.lower(L_ophdr.op_typ) == "REQ") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.docu_nr == l_op.lscheinnr)).first()

            if l_ophdr:
                appflag = l_ophdr.betriebsnr != 0
            do_it = True

            if curr_lschein != "":
                do_it = l_op.lscheinnr == curr_lschein

            if do_it:
                it_exist = True


                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                if l_op.op_art == 14:

                    l_store = db_session.query(L_store).filter(
                            (L_store.lager_nr == l_op.pos)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    t_list.qty1 = qty1
                    qty = 0
                    val = 0
                    qty1 = 0
                lscheinnr = l_op.lscheinnr

                if l_op.reorgflag != deptno:
                    deptno = l_op.reorgflag

                    parameters = db_session.query(Parameters).filter(
                            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()
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
                t_list.anzahl = l_op.anzahl
                t_list.qty1 = l_op.deci1[0]
                t_list.einzelpreis = l_op.einzelpreis
                t_list.warenwert = l_op.warenwert
                t_list.lscheinnr = lscheinnr
                t_list.f_bezeich = l_lager.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content = l_artikel.inhalt
                t_list.appflag = appflag
                t_list.stornogrund = l_op.stornogrund
                t_list.art_bezeich = l_artikel.bezeich
                t_list.art_lief_einheit = l_artikel.lief_einheit
                t_list.art_traubensort = l_artikel.traubensort
                t_list.zwkum = l_artikel.zwkum
                t_list.endkum = l_artikel.endkum
                t_list.centername = curr_centername


                t_list.deptname = l_lager.bezeich

                if l_op.op_art == 14:
                    t_list.deptname = l_store.bezeich

                if appflag:
                    t_list.appStr = "Y"

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.op_art == 13:
                    t_list.to_stock = 0

                if l_op.op_art == 13 and trim(l_op.stornogrund) != "":

                    gl_acct = db_session.query(Gl_acct).filter(
                            (Gl_acct.fibukonto == l_op.stornogrund)).first()

                    if not gl_acct:

                        gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.bezeich == l_op.stornogrund)).first()

                    if gl_acct:
                        t_list.fibukonto = gl_acct.fibukonto
                        t_list.gl_bezeich = gl_acct.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not long_digit:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>,>>>,>>9.99")
                    else:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">,>>>,>>>,>>9")
                qty = qty + l_op.anzahl
                qty1 = qty1 + l_op.deci1[0]
                t_list.qty = l_op.anzahl
                t_list.qty1 = l_op.deci1[0]
                t_qty = t_qty + l_op.anzahl
                t_qty1 = t_qty1 + l_op.deci1[0]

                if show_price:
                    t_list.val = l_op.warenwert
                    val = val + l_op.warenwert
                    t_val = t_val + l_op.warenwert

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.qty1 = qty1
            t_list.val = val

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.qty1 = t_qty1
            t_list.val = t_val


    def add_id():

        nonlocal it_exist, t_list_list, appflag, long_digit, htparam, l_lager, l_artikel, l_op, l_ophdr, parameters, gl_acct, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list


        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (Usr.nr == l_op.fuellflag)).first()

        if usr:
            t_list.id = usr.userinit
        else:
            t_list.id = "??"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    create_list()

    return generate_output()