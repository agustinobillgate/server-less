from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Hoteldpt, L_bestand, Dml_artdep, Reslin_queasy, Dml_art, L_artikel, L_untergrup, Queasy, L_lieferant

def web_interface_dml_listbl(curr_dept:int, selected_date:date, dml_no:str):
    supply_list_list = []
    c_list_list = []
    t_hoteldpt_list = []
    t_l_bestand_list = []
    hoteldpt = l_bestand = dml_artdep = reslin_queasy = dml_art = l_artikel = l_untergrup = queasy = l_lieferant = None

    supply_list = c_list = dml_list = t_hoteldpt = t_l_bestand = None

    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":str, "telefon":str, "fax":str, "namekontakt":str})
    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal, "dml_nr":str, "qty2":decimal})
    dml_list_list, Dml_list = create_model("Dml_list", {"varname":str, "vstring":str})
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal supply_list_list, c_list_list, t_hoteldpt_list, t_l_bestand_list, hoteldpt, l_bestand, dml_artdep, reslin_queasy, dml_art, l_artikel, l_untergrup, queasy, l_lieferant
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list, dml_list, t_hoteldpt, t_l_bestand
        nonlocal supply_list_list, c_list_list, dml_list_list, t_hoteldpt_list, t_l_bestand_list
        return {"supply-list": supply_list_list, "c-list": c_list_list, "t-hoteldpt": t_hoteldpt_list, "t-l-bestand": t_l_bestand_list}

    def create_it():

        nonlocal supply_list_list, c_list_list, t_hoteldpt_list, t_l_bestand_list, hoteldpt, l_bestand, dml_artdep, reslin_queasy, dml_art, l_artikel, l_untergrup, queasy, l_lieferant
        nonlocal curr_dept, selected_date, dml_no


        nonlocal supply_list, c_list, dml_list, t_hoteldpt, t_l_bestand
        nonlocal supply_list_list, c_list_list, dml_list_list, t_hoteldpt_list, t_l_bestand_list

        dept:int = 0
        liefno:int = 0
        chginit:str = ""
        b_artdep = None
        breslin = None
        B_artdep =  create_buffer("B_artdep",Dml_artdep)
        Breslin =  create_buffer("Breslin",Reslin_queasy)

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            t_hoteldpt = T_hoteldpt()
            t_hoteldpt_list.append(t_hoteldpt)

            buffer_copy(hoteldpt, t_hoteldpt)

        for l_bestand in db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0)).order_by(L_bestand._recid).all():
            t_l_bestand = T_l_bestand()
            t_l_bestand_list.append(t_l_bestand)

            buffer_copy(l_bestand, t_l_bestand)
        c_list_list.clear()
        supply_list_list.clear()
        supply_list = Supply_list()
        supply_list_list.append(supply_list)


        if curr_dept == 0:

            dml_art = db_session.query(Dml_art).filter(
                     (Dml_art.datum == selected_date)).first()
            while None != dml_art:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == dml_art.artnr)).first()

                if l_artikel:

                    l_untergrup = db_session.query(L_untergrup).filter(
                             (L_untergrup.zwkum == l_artikel.zwkum)).first()

                    if l_untergrup:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.grp = l_untergrup.bezeich
                        c_list.zwkum = l_untergrup.zwkum
                        c_list.bezeich = l_artikel.bezeich
                        c_list.qty =  to_decimal(dml_art.anzahl)
                        c_list.price =  to_decimal(dml_art.einzelpreis)
                        c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                        c_list.unit = l_artikel.traubensorte
                        c_list.content =  to_decimal(l_artikel.inhalt)
                        c_list.deliver =  to_decimal(dml_art.geliefert)
                        c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                        c_list.qty1 =  to_decimal(c_list.qty)
                        c_list.price1 =  to_decimal(c_list.price)
                        c_list.id = entry(0, dml_art.userinit, ";")
                        c_list.cid = replace_str(entry(0, dml_art.chginit, ";") , "!", "")
                        c_list.dept = curr_dept

                        if num_entries(dml_art.chginit, ";") > 1:
                            c_list.dml_nr = entry(1, dml_art.chginit, ";")

                        if num_entries(dml_artdep.chginit, ";") > 2:
                            c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_artdep.chginit , ";")))

                        if num_entries(dml_art.chginit, ";") > 1 and entry(0, dml_art.chginit, ";") != "" and substring(entry(0, dml_art.chginit, ";") , len(entry(0, dml_art.chginit, ";")) - 1) == ("!").lower() :
                            c_list.approved = True

                        elif dml_artdep.chginit != "" and substring(dml_artdep.chginit, len(dml_artdep.chginit) - 1) == ("!").lower() :
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_art.userinit, ";"))

                        l_bestand = db_session.query(L_bestand).filter(
                                 (L_bestand.artnr == dml_art.artnr) & (L_bestand.lager_nr == 0)).first()

                        if l_bestand:
                            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 202) & (Queasy.number1 == 0) & (Queasy.number2 == dml_art.artnr) & (Queasy.date1 == dml_art.datum)).first()

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = db_session.query(L_lieferant).filter(
                                     (L_lieferant.lief_nr == liefno)).first()

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                                supply_list = query(supply_list_list, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_list.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                curr_recid = dml_art._recid
                dml_art = db_session.query(Dml_art).filter(
                         (Dml_art.datum == selected_date) & (substring(Dml_art.chginit, len(Dml_art.chginit) - 1) != ("*").lower())).filter(Dml_art._recid > curr_recid).first()
        else:

            breslin = db_session.query(Breslin).filter(
                     (func.lower(Breslin.key) == ("DML").lower()) & (Breslin.date1 == selected_date) & (to_int(entry(1, Breslin.char1, ";")) == curr_dept) & (entry(1, Breslin.char3, ";") == (dml_no).lower())).first()

            if breslin:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())).first()
                while None != reslin_queasy:

                    l_artikel = db_session.query(L_artikel).filter(
                             (L_artikel.artnr == to_int(entry(0, reslin_queasy.char1, ";")))).first()

                    if l_artikel:

                        l_untergrup = db_session.query(L_untergrup).filter(
                                 (L_untergrup.zwkum == l_artikel.zwkum)).first()

                        if l_untergrup:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = l_artikel.artnr
                            c_list.grp = l_untergrup.bezeich
                            c_list.zwkum = l_untergrup.zwkum
                            c_list.bezeich = l_artikel.bezeich
                            c_list.qty =  to_decimal(reslin_queasy.deci2)
                            c_list.price =  to_decimal(reslin_queasy.deci1)
                            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                            c_list.unit = l_artikel.traubensorte
                            c_list.content =  to_decimal(l_artikel.inhalt)
                            c_list.deliver =  to_decimal(reslin_queasy.deci3)
                            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                            c_list.qty1 =  to_decimal(c_list.qty)
                            c_list.price1 =  to_decimal(c_list.price)
                            c_list.id = entry(0, reslin_queasy.char2, ";")
                            c_list.cid = entry(0, reslin_queasy.char3, ";")
                            c_list.dept = curr_dept
                            c_list.dml_nr = entry(1, reslin_queasy.char3, ";")

                            if num_entries(reslin_queasy.char3, ";") > 2:
                                c_list.qty2 =  to_decimal(to_decimal(entry(2 , reslin_queasy.char3 , ";")))

                            if entry(0, reslin_queasy.char3, ";") != "" and substring(entry(0, reslin_queasy.char3, ";") , len(entry(0, reslin_queasy.char3, ";")) - 1) == ("!").lower() :
                                c_list.approved = True
                            liefno = 0
                            liefno = to_int(entry(1, reslin_queasy.char2, ";"))

                            l_bestand = db_session.query(L_bestand).filter(
                                     (L_bestand.artnr == to_int(entry(0, reslin_queasy.char1, ";"))) & (L_bestand.lager_nr == 0)).first()

                            if l_bestand:
                                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 202) & (Queasy.number1 == to_int(entry(1, reslin_queasy.char1, ";"))) & (Queasy.number2 == to_int(entry(0, reslin_queasy.char1, ";"))) & (Queasy.date1 == reslin_queasy.date1)).first()

                            if queasy:
                                c_list.remark = queasy.char1

                            if liefno != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                         (L_lieferant.lief_nr == liefno)).first()

                                if l_lieferant:
                                    c_list.supplier = l_lieferant.firma
                                    c_list.lief_nr = liefno

                                supply_list = query(supply_list_list, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_list.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                    curr_recid = reslin_queasy._recid
                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("DML").lower()) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())).filter(Reslin_queasy._recid > curr_recid).first()
            else:

                dml_artdep = db_session.query(Dml_artdep).filter(
                         (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept)).first()
                while None != dml_artdep:

                    l_artikel = db_session.query(L_artikel).filter(
                             (L_artikel.artnr == dml_artdep.artnr)).first()

                    if l_artikel:

                        l_untergrup = db_session.query(L_untergrup).filter(
                                 (L_untergrup.zwkum == l_artikel.zwkum)).first()

                        if l_untergrup:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = l_artikel.artnr
                            c_list.grp = l_untergrup.bezeich
                            c_list.zwkum = l_untergrup.zwkum
                            c_list.bezeich = l_artikel.bezeich
                            c_list.qty =  to_decimal(dml_artdep.anzahl)
                            c_list.price =  to_decimal(dml_artdep.einzelpreis)
                            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
                            c_list.unit = l_artikel.traubensorte
                            c_list.content =  to_decimal(l_artikel.inhalt)
                            c_list.deliver =  to_decimal(dml_artdep.geliefert)
                            c_list.amount =  to_decimal(c_list.qty) * to_decimal(c_list.price)
                            c_list.qty1 =  to_decimal(c_list.qty)
                            c_list.price1 =  to_decimal(c_list.price)
                            c_list.id = entry(0, dml_artdep.userinit, ";")
                            c_list.dept = curr_dept

                            if num_entries(dml_artdep.chginit, ";") > 1:
                                c_list.cid = entry(0, dml_artdep.chginit, ";")
                                c_list.dml_nr = entry(1, dml_artdep.chginit, ";")


                            else:
                                c_list.cid = dml_artdep.chginit

                            if num_entries(dml_artdep.chginit, ";") > 2:
                                c_list.qty2 =  to_decimal(to_decimal(entry(2 , dml_artdep.chginit , ";")))

                            if num_entries(dml_artdep.chginit, ";") > 1 and entry(0, dml_artdep.chginit, ";") != "" and substring(entry(0, dml_artdep.chginit, ";") , len(entry(0, dml_artdep.chginit, ";")) - 1) == ("!").lower() :
                                c_list.approved = True

                            elif dml_artdep.chginit != "" and substring(dml_artdep.chginit, len(dml_artdep.chginit) - 1) == ("!").lower() :
                                c_list.approved = True
                            liefno = 0
                            liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                            l_bestand = db_session.query(L_bestand).filter(
                                     (L_bestand.artnr == dml_artdep.artnr) & (L_bestand.lager_nr == 0)).first()

                            if l_bestand:
                                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 202) & (Queasy.number1 == dml_artdep.departement) & (Queasy.number2 == dml_artdep.artnr) & (Queasy.date1 == dml_artdep.datum)).first()

                            if queasy:
                                c_list.remark = queasy.char1

                            if liefno != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                         (L_lieferant.lief_nr == liefno)).first()

                                if l_lieferant:
                                    c_list.supplier = l_lieferant.firma
                                    c_list.lief_nr = liefno

                                supply_list = query(supply_list_list, filters=(lambda supply_list: supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_list.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                    curr_recid = dml_artdep._recid
                    dml_artdep = db_session.query(Dml_artdep).filter(
                             (Dml_artdep.datum == selected_date) & (Dml_artdep.departement == curr_dept)).filter(Dml_artdep._recid > curr_recid).first()

    create_it()

    return generate_output()