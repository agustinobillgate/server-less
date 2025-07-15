#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_lieferant, L_order, L_orderhdr, Parameters, L_artikel, L_pprice, Gl_acct

def pr_list_disp_list_2bl(char1:string, billdate:date, from_date:date, to_date:date, outstand_flag:bool, expired_flag:bool, approve_flag:bool, reject_flag:bool, sorttype:int, sort_app:string):

    prepare_cache ([Bediener, L_lieferant, L_orderhdr, Parameters, L_artikel, L_pprice, Gl_acct])

    s_list_data = []
    estimated:int = 0
    testimated:int = 0
    bediener = l_lieferant = l_order = l_orderhdr = parameters = l_artikel = l_pprice = gl_acct = None

    s_list = usrbuff = t_lieferant = b_lorder = b_lorderhdr = sbuff = tbuff = None

    s_list_data, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

    Usrbuff = create_buffer("Usrbuff",Bediener)
    T_lieferant = create_buffer("T_lieferant",L_lieferant)
    B_lorder = create_buffer("B_lorder",L_order)
    B_lorderhdr = create_buffer("B_lorderhdr",L_orderhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, estimated, testimated, bediener, l_lieferant, l_order, l_orderhdr, parameters, l_artikel, l_pprice, gl_acct
        nonlocal char1, billdate, from_date, to_date, outstand_flag, expired_flag, approve_flag, reject_flag, sorttype, sort_app
        nonlocal usrbuff, t_lieferant, b_lorder, b_lorderhdr


        nonlocal s_list, usrbuff, t_lieferant, b_lorder, b_lorderhdr, sbuff, tbuff
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def disp_list(pr_nr:string):

        nonlocal s_list_data, estimated, testimated, bediener, l_lieferant, l_order, l_orderhdr, parameters, l_artikel, l_pprice, gl_acct
        nonlocal char1, billdate, from_date, to_date, outstand_flag, expired_flag, approve_flag, reject_flag, sorttype, sort_app
        nonlocal usrbuff, t_lieferant, b_lorder, b_lorderhdr


        nonlocal s_list, usrbuff, t_lieferant, b_lorder, b_lorderhdr, sbuff, tbuff
        nonlocal s_list_data

        app_flag:bool = False
        rej_flag:bool = False
        rej_reason:string = ""
        do_it:bool = False
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        Sbuff = S_list
        sbuff_data = s_list_data
        Tbuff = S_list
        tbuff_data = s_list_data

        if pr_nr != "":
            estimated = get_current_time_in_seconds()

            l_orderhdr = get_cache (L_orderhdr, {"betriebsnr": [(ge, 9)],"docu_nr": [(eq, pr_nr)],"bestelldatum": [(eq, billdate)],"lief_nr": [(eq, 0)]})

            if l_orderhdr:
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                         (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                s_list = S_list()
                s_list_data.append(s_list)


                if parameters:
                    s_list.bezeich = parameters.vstring
                s_list.pos = 0
                s_list.s_recid = l_orderhdr._recid
                s_list.docu_nr = l_orderhdr.docu_nr
                s_list.str0 = l_orderhdr.docu_nr
                s_list.deptnr = l_orderhdr.angebot_lief[0]
                s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                s_list.approved = app_flag
                s_list.rejected = rej_flag

                if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                    s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                    s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                else:
                    s_list.instruct = l_orderhdr.lief_fax[2]

                if l_orderhdr.betriebsnr == 10:
                    s_list.flag = True

                if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                    if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                        s_list.app_rej = ""


                    else:
                        s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                    s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                    s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                        entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                        " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                if l_order:
                    s_list.loeschflag = l_order.loeschflag

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                while None != l_order:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                    if l_artikel:

                        usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.s_recid = l_order._recid
                        s_list.deptnr = l_orderhdr.angebot_lief[0]
                        s_list.docu_nr = l_order.docu_nr
                        s_list.po_nr = l_order.lief_fax[1]
                        s_list.pos = l_order.pos
                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.qty =  to_decimal(l_order.anzahl)
                        s_list.dunit = l_artikel.traubensorte
                        s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                        s_list.approved = app_flag
                        s_list.rejected = rej_flag
                        s_list.loeschflag = l_order.loeschflag
                        s_list.userinit = usr.userinit
                        s_list.pchase_nr = l_order.lief_fax[1]
                        s_list.konto = l_order.stornogrund
                        s_list.pchase_date = l_order.bestelldatum
                        s_list.cdate = l_order.lieferdatum_eff
                        s_list.instruct = l_order.besteller
                        s_list.supno = l_order.angebot_lief[1]
                        s_list.currno = l_order.angebot_lief[2]
                        s_list.duprice =  to_decimal(l_order.einzelpreis)
                        s_list.amount =  to_decimal(l_order.warenwert)
                        s_list.anzahl = l_order.anzahl
                        s_list.txtnr = l_order.txtnr
                        s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                        s_list.zeit = l_order.zeit
                        s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                        s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                        s_list.masseinheit = l_artikel.masseinheit
                        s_list.lief_fax2 = l_order.lief_fax[1]
                        s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                        s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                        l_pprice_obj_list = {}
                        l_pprice = L_pprice()
                        t_lieferant = L_lieferant()
                        for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                 (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                            if l_pprice_obj_list.get(l_pprice._recid):
                                continue
                            else:
                                l_pprice_obj_list[l_pprice._recid] = True


                            s_list.last_pdate = l_pprice.bestelldatum
                            s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                            s_list.a_firma = t_lieferant.firma


                            break

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                        if gl_acct:
                            s_list.desc_coa = gl_acct.bezeich

                        if l_order.bestellart != "":
                            s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                            s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                            s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                            s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                            s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                            s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                        if l_lieferant:
                            s_list.suppn1 = l_lieferant.firma

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                        if l_lieferant:
                            s_list.suppn2 = l_lieferant.firma

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                        if l_lieferant:
                            s_list.suppn3 = l_lieferant.firma

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                        if l_lieferant:
                            s_list.supps = l_lieferant.firma

                        if l_order.angebot_lief[2] != 0:

                            usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                            if usrbuff:
                                s_list.cid = usrbuff.userinit

                        if l_order.anzahl != 0:
                            s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                        if l_artikel.lief_einheit != 0:
                            s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                        if l_order.lieferdatum != None:
                            s_list.lieferdatum = to_string(l_order.lieferdatum)

                    curr_recid = l_order._recid
                    l_order = db_session.query(L_order).filter(
                             (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

            return
        s_list_data.clear()
        estimated = get_current_time_in_seconds()

        if sort_app.lower()  == ("ALL").lower()  or sort_app.lower()  == "":

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag
                    else:
                        s_list.loeschflag = 999

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                    while None != l_order:

                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                        if l_artikel:

                            usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                            tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                            if not tbuff:
                                tbuff = Tbuff()
                                tbuff_data.append(tbuff)

                                buffer_copy(sbuff, tbuff)
                                tbuff.loeschflag = l_order.loeschflag


                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.s_recid = l_order._recid
                            s_list.deptnr = l_orderhdr.angebot_lief[0]
                            s_list.docu_nr = l_order.docu_nr
                            s_list.po_nr = l_order.lief_fax[1]
                            s_list.pos = l_order.pos
                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.qty =  to_decimal(l_order.anzahl)
                            s_list.dunit = l_artikel.traubensorte
                            s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                            s_list.approved = app_flag
                            s_list.rejected = rej_flag
                            s_list.pchase_date = l_order.bestelldatum
                            s_list.loeschflag = l_order.loeschflag
                            s_list.konto = l_order.stornogrund
                            s_list.userinit = usr.userinit
                            s_list.pchase_nr = l_order.lief_fax[1]
                            s_list.cdate = l_order.lieferdatum_eff
                            s_list.instruct = l_order.besteller
                            s_list.supno = l_order.angebot_lief[1]
                            s_list.currno = l_order.angebot_lief[2]
                            s_list.duprice =  to_decimal(l_order.einzelpreis)
                            s_list.amount =  to_decimal(l_order.warenwert)
                            s_list.anzahl = l_order.anzahl
                            s_list.txtnr = l_order.txtnr
                            s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                            s_list.zeit = l_order.zeit
                            s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                            s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                            s_list.masseinheit = l_artikel.masseinheit
                            s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                            l_pprice_obj_list = {}
                            l_pprice = L_pprice()
                            t_lieferant = L_lieferant()
                            for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                         (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                if l_pprice_obj_list.get(l_pprice._recid):
                                    continue
                                else:
                                    l_pprice_obj_list[l_pprice._recid] = True


                                s_list.last_pdate = l_pprice.bestelldatum
                                s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                s_list.a_firma = t_lieferant.firma


                                break

                            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                            if gl_acct:
                                s_list.desc_coa = gl_acct.bezeich

                            if l_order.bestellart != "":
                                s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                            if l_lieferant:
                                s_list.suppn1 = l_lieferant.firma

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                            if l_lieferant:
                                s_list.suppn2 = l_lieferant.firma

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                            if l_lieferant:
                                s_list.suppn3 = l_lieferant.firma

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                            if l_lieferant:
                                s_list.supps = l_lieferant.firma

                            if not sbuff:
                                s_list.str0 = l_order.docu_nr
                                s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                            if l_order.angebot_lief[2] != 0:

                                usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                if usrbuff:
                                    s_list.cid = usrbuff.userinit

                            if l_order.lieferdatum != None:
                                s_list.lieferdatum = to_string(l_order.lieferdatum)

                            if l_order.anzahl != 0:
                                s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                            if l_artikel.lief_einheit != 0:
                                s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                        curr_recid = l_order._recid
                        l_order = db_session.query(L_order).filter(
                                     (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

        elif sort_app.lower()  == ("No Approve").lower() :

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9) & (entry(0, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(1, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(2, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(3, L_orderhdr.lief_fax[inc_value(1)], ";") == " ")).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":

                        l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                        while None != l_order:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                            if l_artikel:

                                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                                tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                                if not tbuff:
                                    tbuff = Tbuff()
                                    tbuff_data.append(tbuff)

                                    buffer_copy(sbuff, tbuff)
                                    tbuff.loeschflag = l_order.loeschflag


                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.s_recid = l_order._recid
                                s_list.deptnr = l_orderhdr.angebot_lief[0]
                                s_list.docu_nr = l_order.docu_nr
                                s_list.po_nr = l_order.lief_fax[1]
                                s_list.pos = l_order.pos
                                s_list.artnr = l_artikel.artnr
                                s_list.bezeich = l_artikel.bezeich
                                s_list.qty =  to_decimal(l_order.anzahl)
                                s_list.dunit = l_artikel.traubensorte
                                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                                s_list.approved = app_flag
                                s_list.rejected = rej_flag
                                s_list.pchase_date = l_order.bestelldatum
                                s_list.loeschflag = l_order.loeschflag
                                s_list.konto = l_order.stornogrund
                                s_list.userinit = usr.userinit
                                s_list.pchase_nr = l_order.lief_fax[1]
                                s_list.cdate = l_order.lieferdatum_eff
                                s_list.instruct = l_order.besteller
                                s_list.supno = l_order.angebot_lief[1]
                                s_list.currno = l_order.angebot_lief[2]
                                s_list.duprice =  to_decimal(l_order.einzelpreis)
                                s_list.amount =  to_decimal(l_order.warenwert)
                                s_list.anzahl = l_order.anzahl
                                s_list.txtnr = l_order.txtnr
                                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                                s_list.zeit = l_order.zeit
                                s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                                s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                                s_list.masseinheit = l_artikel.masseinheit
                                s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                                l_pprice_obj_list = {}
                                l_pprice = L_pprice()
                                t_lieferant = L_lieferant()
                                for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                             (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                    if l_pprice_obj_list.get(l_pprice._recid):
                                        continue
                                    else:
                                        l_pprice_obj_list[l_pprice._recid] = True


                                    s_list.last_pdate = l_pprice.bestelldatum
                                    s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                    s_list.a_firma = t_lieferant.firma


                                    break

                                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                                if gl_acct:
                                    s_list.desc_coa = gl_acct.bezeich

                                if l_order.bestellart != "":
                                    s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                                if l_lieferant:
                                    s_list.suppn1 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                                if l_lieferant:
                                    s_list.suppn2 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                                if l_lieferant:
                                    s_list.suppn3 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                                if l_lieferant:
                                    s_list.supps = l_lieferant.firma

                                if not sbuff:
                                    s_list.str0 = l_order.docu_nr
                                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                                if l_order.angebot_lief[2] != 0:

                                    usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                    if usrbuff:
                                        s_list.cid = usrbuff.userinit

                                if l_order.lieferdatum != None:
                                    s_list.lieferdatum = to_string(l_order.lieferdatum)

                                if l_order.anzahl != 0:
                                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                                if l_artikel.lief_einheit != 0:
                                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                            curr_recid = l_order._recid
                            l_order = db_session.query(L_order).filter(
                                         (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

        elif sort_app.lower()  == ("Approve 1").lower() :

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9) & (entry(0, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(1, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(2, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(3, L_orderhdr.lief_fax[inc_value(1)], ";") == " ")).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":

                        l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                        while None != l_order:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                            if l_artikel:

                                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                                tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                                if not tbuff:
                                    tbuff = Tbuff()
                                    tbuff_data.append(tbuff)

                                    buffer_copy(sbuff, tbuff)
                                    tbuff.loeschflag = l_order.loeschflag


                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.s_recid = l_order._recid
                                s_list.deptnr = l_orderhdr.angebot_lief[0]
                                s_list.docu_nr = l_order.docu_nr
                                s_list.po_nr = l_order.lief_fax[1]
                                s_list.pos = l_order.pos
                                s_list.artnr = l_artikel.artnr
                                s_list.bezeich = l_artikel.bezeich
                                s_list.qty =  to_decimal(l_order.anzahl)
                                s_list.dunit = l_artikel.traubensorte
                                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                                s_list.approved = app_flag
                                s_list.rejected = rej_flag
                                s_list.pchase_date = l_order.bestelldatum
                                s_list.loeschflag = l_order.loeschflag
                                s_list.konto = l_order.stornogrund
                                s_list.userinit = usr.userinit
                                s_list.pchase_nr = l_order.lief_fax[1]
                                s_list.cdate = l_order.lieferdatum_eff
                                s_list.instruct = l_order.besteller
                                s_list.supno = l_order.angebot_lief[1]
                                s_list.currno = l_order.angebot_lief[2]
                                s_list.duprice =  to_decimal(l_order.einzelpreis)
                                s_list.amount =  to_decimal(l_order.warenwert)
                                s_list.anzahl = l_order.anzahl
                                s_list.txtnr = l_order.txtnr
                                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                                s_list.zeit = l_order.zeit
                                s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                                s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                                s_list.masseinheit = l_artikel.masseinheit
                                s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                                l_pprice_obj_list = {}
                                l_pprice = L_pprice()
                                t_lieferant = L_lieferant()
                                for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                             (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                    if l_pprice_obj_list.get(l_pprice._recid):
                                        continue
                                    else:
                                        l_pprice_obj_list[l_pprice._recid] = True


                                    s_list.last_pdate = l_pprice.bestelldatum
                                    s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                    s_list.a_firma = t_lieferant.firma


                                    break

                                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                                if gl_acct:
                                    s_list.desc_coa = gl_acct.bezeich

                                if l_order.bestellart != "":
                                    s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                                if l_lieferant:
                                    s_list.suppn1 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                                if l_lieferant:
                                    s_list.suppn2 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                                if l_lieferant:
                                    s_list.suppn3 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                                if l_lieferant:
                                    s_list.supps = l_lieferant.firma

                                if not sbuff:
                                    s_list.str0 = l_order.docu_nr
                                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                                if l_order.angebot_lief[2] != 0:

                                    usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                    if usrbuff:
                                        s_list.cid = usrbuff.userinit

                                if l_order.lieferdatum != None:
                                    s_list.lieferdatum = to_string(l_order.lieferdatum)

                                if l_order.anzahl != 0:
                                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                                if l_artikel.lief_einheit != 0:
                                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                            curr_recid = l_order._recid
                            l_order = db_session.query(L_order).filter(
                                         (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

        elif sort_app.lower()  == ("Approve 2").lower() :

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9) & (entry(0, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(1, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(2, L_orderhdr.lief_fax[inc_value(1)], ";") == " ") & (entry(3, L_orderhdr.lief_fax[inc_value(1)], ";") == " ")).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":

                        l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                        while None != l_order:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                            if l_artikel:

                                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                                tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                                if not tbuff:
                                    tbuff = Tbuff()
                                    tbuff_data.append(tbuff)

                                    buffer_copy(sbuff, tbuff)
                                    tbuff.loeschflag = l_order.loeschflag


                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.s_recid = l_order._recid
                                s_list.deptnr = l_orderhdr.angebot_lief[0]
                                s_list.docu_nr = l_order.docu_nr
                                s_list.po_nr = l_order.lief_fax[1]
                                s_list.pos = l_order.pos
                                s_list.artnr = l_artikel.artnr
                                s_list.bezeich = l_artikel.bezeich
                                s_list.qty =  to_decimal(l_order.anzahl)
                                s_list.dunit = l_artikel.traubensorte
                                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                                s_list.approved = app_flag
                                s_list.rejected = rej_flag
                                s_list.pchase_date = l_order.bestelldatum
                                s_list.loeschflag = l_order.loeschflag
                                s_list.konto = l_order.stornogrund
                                s_list.userinit = usr.userinit
                                s_list.pchase_nr = l_order.lief_fax[1]
                                s_list.cdate = l_order.lieferdatum_eff
                                s_list.instruct = l_order.besteller
                                s_list.supno = l_order.angebot_lief[1]
                                s_list.currno = l_order.angebot_lief[2]
                                s_list.duprice =  to_decimal(l_order.einzelpreis)
                                s_list.amount =  to_decimal(l_order.warenwert)
                                s_list.anzahl = l_order.anzahl
                                s_list.txtnr = l_order.txtnr
                                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                                s_list.zeit = l_order.zeit
                                s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                                s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                                s_list.masseinheit = l_artikel.masseinheit
                                s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                                l_pprice_obj_list = {}
                                l_pprice = L_pprice()
                                t_lieferant = L_lieferant()
                                for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                             (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                    if l_pprice_obj_list.get(l_pprice._recid):
                                        continue
                                    else:
                                        l_pprice_obj_list[l_pprice._recid] = True


                                    s_list.last_pdate = l_pprice.bestelldatum
                                    s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                    s_list.a_firma = t_lieferant.firma


                                    break

                                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                                if gl_acct:
                                    s_list.desc_coa = gl_acct.bezeich

                                if l_order.bestellart != "":
                                    s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                                if l_lieferant:
                                    s_list.suppn1 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                                if l_lieferant:
                                    s_list.suppn2 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                                if l_lieferant:
                                    s_list.suppn3 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                                if l_lieferant:
                                    s_list.supps = l_lieferant.firma

                                if not sbuff:
                                    s_list.str0 = l_order.docu_nr
                                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                                if l_order.angebot_lief[2] != 0:

                                    usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                    if usrbuff:
                                        s_list.cid = usrbuff.userinit

                                if l_order.lieferdatum != None:
                                    s_list.lieferdatum = to_string(l_order.lieferdatum)

                                if l_order.anzahl != 0:
                                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                                if l_artikel.lief_einheit != 0:
                                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                            curr_recid = l_order._recid
                            l_order = db_session.query(L_order).filter(
                                         (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

        elif sort_app.lower()  == ("Approve 3").lower() :

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9) & (entry(0, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(1, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(2, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(3, L_orderhdr.lief_fax[inc_value(1)], ";") == " ")).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":

                        l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                        while None != l_order:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                            if l_artikel:

                                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                                tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                                if not tbuff:
                                    tbuff = Tbuff()
                                    tbuff_data.append(tbuff)

                                    buffer_copy(sbuff, tbuff)
                                    tbuff.loeschflag = l_order.loeschflag


                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.s_recid = l_order._recid
                                s_list.deptnr = l_orderhdr.angebot_lief[0]
                                s_list.docu_nr = l_order.docu_nr
                                s_list.po_nr = l_order.lief_fax[1]
                                s_list.pos = l_order.pos
                                s_list.artnr = l_artikel.artnr
                                s_list.bezeich = l_artikel.bezeich
                                s_list.qty =  to_decimal(l_order.anzahl)
                                s_list.dunit = l_artikel.traubensorte
                                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                                s_list.approved = app_flag
                                s_list.rejected = rej_flag
                                s_list.pchase_date = l_order.bestelldatum
                                s_list.loeschflag = l_order.loeschflag
                                s_list.konto = l_order.stornogrund
                                s_list.userinit = usr.userinit
                                s_list.pchase_nr = l_order.lief_fax[1]
                                s_list.cdate = l_order.lieferdatum_eff
                                s_list.instruct = l_order.besteller
                                s_list.supno = l_order.angebot_lief[1]
                                s_list.currno = l_order.angebot_lief[2]
                                s_list.duprice =  to_decimal(l_order.einzelpreis)
                                s_list.amount =  to_decimal(l_order.warenwert)
                                s_list.anzahl = l_order.anzahl
                                s_list.txtnr = l_order.txtnr
                                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                                s_list.zeit = l_order.zeit
                                s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                                s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                                s_list.masseinheit = l_artikel.masseinheit
                                s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                                l_pprice_obj_list = {}
                                l_pprice = L_pprice()
                                t_lieferant = L_lieferant()
                                for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                             (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                    if l_pprice_obj_list.get(l_pprice._recid):
                                        continue
                                    else:
                                        l_pprice_obj_list[l_pprice._recid] = True


                                    s_list.last_pdate = l_pprice.bestelldatum
                                    s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                    s_list.a_firma = t_lieferant.firma


                                    break

                                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                                if gl_acct:
                                    s_list.desc_coa = gl_acct.bezeich

                                if l_order.bestellart != "":
                                    s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                                if l_lieferant:
                                    s_list.suppn1 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                                if l_lieferant:
                                    s_list.suppn2 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                                if l_lieferant:
                                    s_list.suppn3 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                                if l_lieferant:
                                    s_list.supps = l_lieferant.firma

                                if not sbuff:
                                    s_list.str0 = l_order.docu_nr
                                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                                if l_order.angebot_lief[2] != 0:

                                    usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                    if usrbuff:
                                        s_list.cid = usrbuff.userinit

                                if l_order.lieferdatum != None:
                                    s_list.lieferdatum = to_string(l_order.lieferdatum)

                                if l_order.anzahl != 0:
                                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                                if l_artikel.lief_einheit != 0:
                                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                            curr_recid = l_order._recid
                            l_order = db_session.query(L_order).filter(
                                         (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

        elif sort_app.lower()  == ("Approve 4").lower() :

            for l_orderhdr in db_session.query(L_orderhdr).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr >= 9) & (entry(0, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(1, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(2, L_orderhdr.lief_fax[inc_value(1)], ";") != " ") & (entry(3, L_orderhdr.lief_fax[inc_value(1)], ";") != " ")).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                app_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
                rej_flag = (l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0)

                parameters = db_session.query(Parameters).filter(
                             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, 0)]})
                do_it = True

                if outstand_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum >= billdate:
                    do_it = False

                if do_it and expired_flag and not app_flag and not rej_flag and l_orderhdr.lieferdatum < billdate:
                    do_it = False

                if do_it and approve_flag and app_flag:
                    do_it = False

                if do_it and reject_flag and rej_flag:
                    do_it = False

                if do_it:
                    s_list = S_list()
                    s_list_data.append(s_list)


                    if parameters:
                        s_list.bezeich = parameters.vstring
                    s_list.pos = 0
                    s_list.s_recid = l_orderhdr._recid
                    s_list.docu_nr = l_orderhdr.docu_nr
                    s_list.str0 = l_orderhdr.docu_nr
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag

                    if l_orderhdr.betriebsnr == 10:
                        s_list.flag = True

                    if num_entries(l_orderhdr.lief_fax[2], "-") > 1:
                        s_list.del_reason = entry(1, l_orderhdr.lief_fax[2], "-")
                        s_list.instruct = entry(0, l_orderhdr.lief_fax[2], "-")


                    else:
                        s_list.instruct = l_orderhdr.lief_fax[2]

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                            s_list.app_rej = ""


                        else:
                            s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")

                    if get_index(l_orderhdr.lief_fax[1], "|") > 0:
                        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                        s_list.app_rej = entry(0, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") + " " +\
                            entry(1, trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";")) , " ") +\
                            " " + trim(entry(1, l_orderhdr.lief_fax[1], "|"))

                    if l_order:
                        s_list.loeschflag = l_order.loeschflag

                    sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff._recid == s_list._recid), first=True)

                    if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " ":

                        l_order = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"lief_nr": [(eq, 0)],"loeschflag": [(eq, sorttype)]})
                        while None != l_order:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                            if l_artikel:

                                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})

                                tbuff = query(tbuff_data, filters=(lambda tbuff: tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                                if not tbuff:
                                    tbuff = Tbuff()
                                    tbuff_data.append(tbuff)

                                    buffer_copy(sbuff, tbuff)
                                    tbuff.loeschflag = l_order.loeschflag


                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.s_recid = l_order._recid
                                s_list.deptnr = l_orderhdr.angebot_lief[0]
                                s_list.docu_nr = l_order.docu_nr
                                s_list.po_nr = l_order.lief_fax[1]
                                s_list.pos = l_order.pos
                                s_list.artnr = l_artikel.artnr
                                s_list.bezeich = l_artikel.bezeich
                                s_list.qty =  to_decimal(l_order.anzahl)
                                s_list.dunit = l_artikel.traubensorte
                                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                                s_list.approved = app_flag
                                s_list.rejected = rej_flag
                                s_list.pchase_date = l_order.bestelldatum
                                s_list.loeschflag = l_order.loeschflag
                                s_list.konto = l_order.stornogrund
                                s_list.userinit = usr.userinit
                                s_list.pchase_nr = l_order.lief_fax[1]
                                s_list.cdate = l_order.lieferdatum_eff
                                s_list.instruct = l_order.besteller
                                s_list.supno = l_order.angebot_lief[1]
                                s_list.currno = l_order.angebot_lief[2]
                                s_list.duprice =  to_decimal(l_order.einzelpreis)
                                s_list.amount =  to_decimal(l_order.warenwert)
                                s_list.anzahl = l_order.anzahl
                                s_list.txtnr = l_order.txtnr
                                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                                s_list.zeit = l_order.zeit
                                s_list.min_bestand =  to_decimal(l_artikel.min_bestand)
                                s_list.max_bestand =  to_decimal(l_artikel.anzverbrauch)
                                s_list.masseinheit = l_artikel.masseinheit
                                s_list.last_pprice =  to_decimal(l_artikel.ek_letzter)

                                l_pprice_obj_list = {}
                                l_pprice = L_pprice()
                                t_lieferant = L_lieferant()
                                for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, t_lieferant.firma, t_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, T_lieferant.firma, T_lieferant._recid).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                             (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                                    if l_pprice_obj_list.get(l_pprice._recid):
                                        continue
                                    else:
                                        l_pprice_obj_list[l_pprice._recid] = True


                                    s_list.last_pdate = l_pprice.bestelldatum
                                    s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                                    s_list.a_firma = t_lieferant.firma


                                    break

                                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

                                if gl_acct:
                                    s_list.desc_coa = gl_acct.bezeich

                                if l_order.bestellart != "":
                                    s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                                if l_lieferant:
                                    s_list.suppn1 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                                if l_lieferant:
                                    s_list.suppn2 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                                if l_lieferant:
                                    s_list.suppn3 = l_lieferant.firma

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                                if l_lieferant:
                                    s_list.supps = l_lieferant.firma

                                if not sbuff:
                                    s_list.str0 = l_order.docu_nr
                                    s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                                    s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                                if l_order.angebot_lief[2] != 0:

                                    usrbuff = get_cache (Bediener, {"nr": [(eq, l_order.angebot_lief[2])]})

                                    if usrbuff:
                                        s_list.cid = usrbuff.userinit

                                if l_order.lieferdatum != None:
                                    s_list.lieferdatum = to_string(l_order.lieferdatum)

                                if l_order.anzahl != 0:
                                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                                if l_artikel.lief_einheit != 0:
                                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                            curr_recid = l_order._recid
                            l_order = db_session.query(L_order).filter(
                                         (L_order.docu_nr == l_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag == sorttype) & (L_order._recid > curr_recid)).first()

    disp_list(char1)
    estimated = get_current_time_in_seconds()

    for s_list in query(s_list_data):

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, s_list.docu_nr)]})

        if l_orderhdr:
            s_list.lief_fax2 = l_orderhdr.lief_fax[1]

    return generate_output()