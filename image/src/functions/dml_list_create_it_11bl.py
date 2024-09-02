from functions.additional_functions import *
import decimal
from datetime import date
from models import Dml_art, L_artikel, L_untergrup, L_bestand, Queasy, L_lieferant, Dml_artdep

def dml_list_create_it_11bl(curr_dept:int, selected_date:date):
    supply_list_list = []
    c_list_list = []
    dml_art = l_artikel = l_untergrup = l_bestand = queasy = l_lieferant = dml_artdep = None

    supply_list = c_list = None

    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":str, "telefon":str, "fax":str, "namekontakt":str})
    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal supply_list_list, c_list_list, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant, dml_artdep


        nonlocal supply_list, c_list
        nonlocal supply_list_list, c_list_list
        return {"supply-list": supply_list_list, "c-list": c_list_list}

    def create_it():

        nonlocal supply_list_list, c_list_list, dml_art, l_artikel, l_untergrup, l_bestand, queasy, l_lieferant, dml_artdep


        nonlocal supply_list, c_list
        nonlocal supply_list_list, c_list_list

        dept:int = 0
        liefno:int = 0
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
                        c_list.qty = dml_art.anzahl
                        c_list.price = dml_art.einzelpreis
                        c_list.l_price = l_artikel.ek_letzter
                        c_list.unit = l_artikel.traubensorte
                        c_list.content = l_artikel.inhalt
                        c_list.deliver = dml_art.geliefert
                        c_list.amount = c_list.qty * c_list.price
                        c_list.qty1 = c_list.qty
                        c_list.price1 = c_list.price
                        c_list.id = entry(0, dml_art.userinit, ";")
                        c_list.cid = replace_str(dml_art.chginit, "!", "")
                        c_list.dept = curr_dept

                        if dml_art.chginit != "" and substring(dml_art.chginit, len(dml_art.chginit) - 1) == "!":
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_art.userinit, ";"))

                        l_bestand = db_session.query(L_bestand).filter(
                                (L_bestand.artnr == dml_art.artnr) &  (L_bestand.lager_nr == 0)).first()

                        if l_bestand:
                            c_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 202) &  (Queasy.number1 == 0) &  (Queasy.number2 == dml_art.artnr) &  (Queasy.date1 == dml_art.datum)).first()

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == liefno)).first()

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                                supply_list = query(supply_list_list, filters=(lambda supply_list :supply_list.lief_nr == liefno), first=True)

                                if not supply_list:
                                    supply_list = Supply_list()
                                    supply_list_list.append(supply_list)

                                    supply_list.lief_nr = l_lieferant.lief_nr
                                    supply_list.supplier = l_lieferant.firma
                                    supply_list.telefon = l_lieferant.telefon
                                    supply_list.fax = l_lieferant.fax
                                    supply_list.namekontakt = l_lieferant.namekontakt

                dml_art = db_session.query(Dml_art).filter(
                        (Dml_art.datum == selected_date)).first()
        else:

            dml_artdep = db_session.query(Dml_artdep).filter(
                    (Dml_artdep.datum == selected_date) &  (Dml_artdep.departement == curr_dept)).first()
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
                        c_list.qty = dml_artdep.anzahl
                        c_list.price = dml_artdep.einzelpreis
                        c_list.l_price = l_artikel.ek_letzter
                        c_list.unit = l_artikel.traubensorte
                        c_list.content = l_artikel.inhalt
                        c_list.deliver = dml_artdep.geliefert
                        c_list.amount = c_list.qty * c_list.price
                        c_list.qty1 = c_list.qty
                        c_list.price1 = c_list.price
                        c_list.id = entry(0, dml_artdep.userinit, ";")
                        c_list.cid = dml_artdep.chginit
                        c_list.dept = curr_dept

                        if dml_artdep.chginit != "" and substring(dml_artdep.chginit, len(dml_artdep.chginit) - 1) == "!":
                            c_list.approved = True
                        liefno = 0
                        liefno = to_int(entry(1, dml_artdep.userinit, ";"))

                        l_bestand = db_session.query(L_bestand).filter(
                                (L_bestand.artnr == dml_artdep.artnr) &  (L_bestand.lager_nr == 0)).first()

                        if l_bestand:
                            c_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 202) &  (Queasy.number1 == dml_artdep.departement) &  (Queasy.number2 == dml_artdep.artnr) &  (Queasy.date1 == dml_artdep.datum)).first()

                        if queasy:
                            c_list.remark = queasy.char1

                        if liefno != 0:

                            l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == liefno)).first()

                            if l_lieferant:
                                c_list.supplier = l_lieferant.firma
                                c_list.lief_nr = liefno

                            supply_list = query(supply_list_list, filters=(lambda supply_list :supply_list.lief_nr == liefno), first=True)

                            if not supply_list:
                                supply_list = Supply_list()
                                supply_list_list.append(supply_list)

                                supply_list.lief_nr = l_lieferant.lief_nr
                                supply_list.supplier = l_lieferant.firma
                                supply_list.telefon = l_lieferant.telefon
                                supply_list.fax = l_lieferant.fax
                                supply_list.namekontakt = l_lieferant.namekontakt

                dml_artdep = db_session.query(Dml_artdep).filter(
                        (Dml_artdep.datum == selected_date) &  (Dml_artdep.departement == curr_dept)).first()

    create_it()

    return generate_output()