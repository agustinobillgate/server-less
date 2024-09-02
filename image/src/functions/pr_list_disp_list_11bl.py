from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, L_lieferant, L_orderhdr, Parameters, L_order, L_artikel, L_pprice, Gl_acct

def pr_list_disp_list_11bl(char1:str, billdate:date, from_date:date, to_date:date, outstand_flag:bool, expired_flag:bool, approve_flag:bool, reject_flag:bool, artnumber:int):
    s_list_list = []
    bediener = l_lieferant = l_orderhdr = parameters = l_order = l_artikel = l_pprice = gl_acct = None

    s_list = usrbuff = t_lieferant = usr = sbuff = tbuff = None

    s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str, "last_pdate":date, "last_pprice":decimal, "zeit":int, "min_bestand":decimal, "max_bestand":decimal, "del_reason":str, "desc_coa":str, "lief_fax3":str, "masseinheit":str, "lief_fax_2":str, "ek_letzter":decimal, "supplier":str, "vk_preis":decimal, "a_firma":str, "last_pbook":decimal}, {"pos": 999999})

    Usrbuff = Bediener
    T_lieferant = L_lieferant
    Usr = Bediener
    Sbuff = S_list
    sbuff_list = s_list_list

    Tbuff = S_list
    tbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, bediener, l_lieferant, l_orderhdr, parameters, l_order, l_artikel, l_pprice, gl_acct
        nonlocal usrbuff, t_lieferant, usr, sbuff, tbuff


        nonlocal s_list, usrbuff, t_lieferant, usr, sbuff, tbuff
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def disp_list(pr_nr:str):

        nonlocal s_list_list, bediener, l_lieferant, l_orderhdr, parameters, l_order, l_artikel, l_pprice, gl_acct
        nonlocal usrbuff, t_lieferant, usr, sbuff, tbuff


        nonlocal s_list, usrbuff, t_lieferant, usr, sbuff, tbuff
        nonlocal s_list_list

        app_flag:bool = False
        rej_flag:bool = False
        rej_reason:str = ""
        do_it:bool = False
        Usr = Bediener
        Sbuff = S_list
        Tbuff = S_list

        if pr_nr != "":

            l_orderhdr = db_session.query(L_orderhdr).filter(
                    (L_orderhdr.betriebsnr >= 9) &  (func.lower(L_orderhdr.docu_nr) == (pr_nr).lower()) &  (L_orderhdr.bestelldatum == billdate) &  (L_orderhdr.lief_nr == 0)).first()
            app_flag = (l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
            rej_flag = (l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") > 0)

            parameters = db_session.query(Parameters).filter(
                    (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

            l_order = db_session.query(L_order).filter(
                    (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.pos == 0) &  (L_order.lief_nr == 0)).first()
            s_list = S_list()
            s_list_list.append(s_list)


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
            IF1 + get_index(l_orderhdr.lief_fax[1], "|") = 0 THEN

            if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                s_list.app_rej = ""


            else:
                s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")
            IF1 + get_index(l_orderhdr.lief_fax[1], "|") > 0 THEN
            s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
            s_list.app_rej = trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";"))

            if l_order:
                s_list.loeschflag = l_order.loeschflag

            l_order = db_session.query(L_order).filter(
                    (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.loeschflag <= 1) &  (L_order.pos > 0) &  (L_order.lief_nr == 0)).first()
            while None != l_order:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == l_order.artnr)).first()

                if l_artikel:

                    usr = db_session.query(Usr).filter(
                            (Usr.username == l_order.lief_fax[0])).first()
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.s_recid = l_order._recid
                    s_list.deptnr = l_orderhdr.angebot_lief[0]
                    s_list.docu_nr = l_order.docu_nr
                    s_list.po_nr = l_order.lief_fax[1]
                    s_list.pos = l_order.pos
                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.qty = l_order.anzahl
                    s_list.dunit = l_artikel.traubensort
                    s_list.lief_einheit = l_artikel.lief_einheit
                    s_list.approved = app_flag
                    s_list.rejected = rej_flag
                    s_list.loeschflag = l_order.loeschflag
                    s_list.userinit = usr.userinit
                    s_list.pchase_nr = l_order.lief_fax[1]
                    s_list.konto = l_order.stornogrund
                    s_list.pchase_date = l_order.bestelldatum
                    s_list.cdate = l_order.lieferdatum_eff
                    s_list.instruct = l_order.besteller
                    s_list.supNo = l_order.angebot_lief[1]
                    s_list.currNo = l_order.angebot_lief[2]
                    s_list.duprice = l_order.einzelpreis
                    s_list.amount = l_order.warenwert
                    s_list.anzahl = l_order.anzahl
                    s_list.txtnr = l_order.txtnr
                    s_list.einzelpreis = l_order.einzelpreis
                    s_list.zeit = l_order.zeit
                    s_list.min_bestand = l_artikel.min_bestand
                    s_list.max_bestand = l_artikel.anzverbrauch
                    s_list.masseinheit = l_artikel.masseinheit
                    s_list.lief_fax2 = l_order.lief_fax[1]
                    s_list.last_pprice = l_artikel.ek_letzter

                    l_pprice_obj_list = []
                    for l_pprice, t_lieferant in db_session.query(L_pprice, T_lieferant).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                            (L_pprice.artnr == l_artikel.artnr)).all():
                        if l_pprice._recid in l_pprice_obj_list:
                            continue
                        else:
                            l_pprice_obj_list.append(l_pprice._recid)


                        s_list.last_pdate = l_pprice.bestelldatum
                        s_list.last_pbook = l_pprice.einzelpreis
                        s_list.a_firma = t_lieferant.firma


                        break

                    gl_acct = db_session.query(Gl_acct).filter(
                            (Gl_acct.fibukonto == l_order.stornogrund)).first()

                    if gl_acct:
                        s_list.konto = l_order.stornogrund + ";" + gl_acct.bezeich
                        s_list.desc_coa = gl_acct.bezeich

                    if l_order.bestellart != "":
                        s_list.du_price1 = decimal.Decimal(entry(1, entry(0, l_order.bestellart , "-") , ";")) / 100
                        s_list.du_price2 = decimal.Decimal(entry(1, entry(1, l_order.bestellart , "-") , ";")) / 100
                        s_list.du_price3 = decimal.Decimal(entry(1, entry(2, l_order.bestellart , "-") , ";")) / 100
                        s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                        s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                        s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == s_list.supp1)).first()

                    if l_lieferant:
                        s_list.suppn1 = l_lieferant.firma

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == s_list.supp2)).first()

                    if l_lieferant:
                        s_list.suppn2 = l_lieferant.firma

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == s_list.supp3)).first()

                    if l_lieferant:
                        s_list.suppn3 = l_lieferant.firma

                    l_lieferant = db_session.query(L_lieferant).filter(
                            (L_lieferant.lief_nr == s_list.supNo)).first()

                    if l_lieferant:
                        s_list.supps = l_lieferant.firma

                    if l_order.angebot_lief[2] != 0:

                        usrbuff = db_session.query(Usrbuff).filter(
                                (Usrbuff.nr == l_order.angebot_lief[2])).first()

                        if usrbuff:
                            s_list.cid = usrbuff.userinit

                    if l_order.anzahl != 0:
                        s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                    if l_artikel.lief_einheit != 0:
                        s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                    if l_order.lieferdatum != None:
                        s_list.lieferdatum = to_string(l_order.lieferdatum)

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.loeschflag <= 1) &  (L_order.pos > 0) &  (L_order.lief_nr == 0)).first()

            return
        s_list_list.clear()

        for l_orderhdr in db_session.query(L_orderhdr).filter(
                    (L_orderhdr.bestelldatum >= from_date) &  (L_orderhdr.bestelldatum <= to_date) &  (L_orderhdr.betriebsnr >= 9)).all():
            app_flag = (l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") == 0) and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
            rej_flag = (l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") > 0)

            parameters = db_session.query(Parameters).filter(
                        (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

            l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.pos == 0) &  (L_order.lief_nr == 0) &  (L_order.artnr == artnumber)).first()
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
                s_list_list.append(s_list)


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
                IF1 + get_index(l_orderhdr.lief_fax[1], "|") = 0 THEN

                if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                    s_list.app_rej = ""


                else:
                    s_list.app_rej = entry(0, entry(0, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(1, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(2, l_orderhdr.lief_fax[1], ";") , " ") + ";" + entry(0, entry(3, l_orderhdr.lief_fax[1], ";") , " ")
                IF1 + get_index(l_orderhdr.lief_fax[1], "|") > 0 THEN
                s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
                s_list.app_rej = trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";"))

                if l_order:
                    s_list.loeschflag = l_order.loeschflag

                sbuff = query(sbuff_list, filters=(lambda sbuff :sbuff._recid == s_list._recid), first=True)

                l_order = db_session.query(L_order).filter(
                            (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.artnr == artnumber)).first()
                while None != l_order:

                    l_artikel = db_session.query(L_artikel).filter(
                                (L_artikel.artnr == l_order.artnr)).first()

                    if l_artikel:

                        usr = db_session.query(Usr).filter(
                                    (Usr.username == l_order.lief_fax[0])).first()

                        tbuff = query(tbuff_list, filters=(lambda tbuff :tbuff.docu_nr == l_order.docu_nr and tbuff.pos == 0 and tbuff.loeschflag == l_order.loeschflag), first=True)

                        if not tbuff:
                            tbuff = Tbuff()
                            tbuff_list.append(tbuff)

                            buffer_copy(sbuff, tbuff)
                            tbuff.loeschflag = l_order.loeschflag


                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.s_recid = l_order._recid
                        s_list.deptnr = l_orderhdr.angebot_lief[0]
                        s_list.docu_nr = l_order.docu_nr
                        s_list.po_nr = l_order.lief_fax[1]
                        s_list.pos = l_order.pos
                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.qty = l_order.anzahl
                        s_list.dunit = l_artikel.traubensort
                        s_list.lief_einheit = l_artikel.lief_einheit
                        s_list.approved = app_flag
                        s_list.rejected = rej_flag
                        s_list.pchase_date = l_order.bestelldatum
                        s_list.loeschflag = l_order.loeschflag
                        s_list.konto = l_order.stornogrund
                        s_list.userinit = usr.userinit
                        s_list.pchase_nr = l_order.lief_fax[1]
                        s_list.cdate = l_order.lieferdatum_eff
                        s_list.instruct = l_order.besteller
                        s_list.supNo = l_order.angebot_lief[1]
                        s_list.currNo = l_order.angebot_lief[2]
                        s_list.duprice = l_order.einzelpreis
                        s_list.amount = l_order.warenwert
                        s_list.anzahl = l_order.anzahl
                        s_list.txtnr = l_order.txtnr
                        s_list.einzelpreis = l_order.einzelpreis
                        s_list.zeit = l_order.zeit
                        s_list.min_bestand = l_artikel.min_bestand
                        s_list.max_bestand = l_artikel.anzverbrauch
                        s_list.masseinheit = l_artikel.masseinheit
                        s_list.last_pprice = l_artikel.ek_letzter

                        l_pprice_obj_list = []
                        for l_pprice, t_lieferant in db_session.query(L_pprice, T_lieferant).join(T_lieferant,(T_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                                    (L_pprice.artnr == l_artikel.artnr)).all():
                            if l_pprice._recid in l_pprice_obj_list:
                                continue
                            else:
                                l_pprice_obj_list.append(l_pprice._recid)


                            s_list.last_pdate = l_pprice.bestelldatum
                            s_list.last_pbook = l_pprice.einzelpreis
                            s_list.a_firma = t_lieferant.firma


                            break

                        gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == l_order.stornogrund)).first()

                        if gl_acct:
                            s_list.konto = l_order.stornogrund + ";" + gl_acct.bezeich
                            s_list.desc_coa = gl_acct.bezeich

                        if l_order.bestellart != "":
                            s_list.du_price1 = decimal.Decimal(entry(1, entry(0, l_order.bestellart , "-") , ";")) / 100
                            s_list.du_price2 = decimal.Decimal(entry(1, entry(1, l_order.bestellart , "-") , ";")) / 100
                            s_list.du_price3 = decimal.Decimal(entry(1, entry(2, l_order.bestellart , "-") , ";")) / 100
                            s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                            s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                            s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                        l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == s_list.supp1)).first()

                        if l_lieferant:
                            s_list.suppn1 = l_lieferant.firma

                        l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == s_list.supp2)).first()

                        if l_lieferant:
                            s_list.suppn2 = l_lieferant.firma

                        l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == s_list.supp3)).first()

                        if l_lieferant:
                            s_list.suppn3 = l_lieferant.firma

                        l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == s_list.supNo)).first()

                        if l_lieferant:
                            s_list.supps = l_lieferant.firma

                        if not sbuff:
                            s_list.str0 = l_order.docu_nr
                            s_list.bestelldatum = to_string(l_orderhdr.bestelldatum)
                            s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)

                        if l_order.angebot_lief[2] != 0:

                            usrbuff = db_session.query(Usrbuff).filter(
                                        (Usrbuff.nr == l_order.angebot_lief[2])).first()

                            if usrbuff:
                                s_list.cid = usrbuff.userinit

                        if l_order.lieferdatum != None:
                            s_list.lieferdatum = to_string(l_order.lieferdatum)

                        if l_order.anzahl != 0:
                            s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                        if l_artikel.lief_einheit != 0:
                            s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                    l_order = db_session.query(L_order).filter(
                                (L_order.docu_nr == l_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.artnr == artnumber)).first()


    disp_list(char1)

    for s_list in query(s_list_list):

        l_orderhdr = db_session.query(L_orderhdr).filter(
                (L_orderhdr.docu_nr == s_list.docu_nr)).first()

        if l_orderhdr:
            s_list.lief_fax2 = l_orderhdr.lief_fax[1]
            s_list.lief_fax3 = l_orderhdr.lief_fax[2]

    return generate_output()