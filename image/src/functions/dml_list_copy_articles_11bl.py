from functions.additional_functions import *
import decimal
from datetime import date
from models import Dml_art, Dml_artdep, L_artikel, L_untergrup, L_bestand, Queasy

def dml_list_copy_articles_11bl(user_init:str, curr_dept:int, selected_date:date):
    approve_flag = False
    c_list_list = []
    supply_list_list = []
    dml_art = dml_artdep = l_artikel = l_untergrup = l_bestand = queasy = None

    c_list = supply_list = d_art = d_art1 = None

    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal})
    supply_list_list, Supply_list = create_model("Supply_list", {"lief_nr":int, "supplier":str, "telefon":str, "fax":str, "namekontakt":str})

    D_art = Dml_art
    D_art1 = Dml_artdep

    db_session = local_storage.db_session

    def generate_output():
        nonlocal approve_flag, c_list_list, supply_list_list, dml_art, dml_artdep, l_artikel, l_untergrup, l_bestand, queasy
        nonlocal d_art, d_art1


        nonlocal c_list, supply_list, d_art, d_art1
        nonlocal c_list_list, supply_list_list
        return {"approve_flag": approve_flag, "c-list": c_list_list, "supply-list": supply_list_list}

    def copy_articles():

        nonlocal approve_flag, c_list_list, supply_list_list, dml_art, dml_artdep, l_artikel, l_untergrup, l_bestand, queasy
        nonlocal d_art, d_art1


        nonlocal c_list, supply_list, d_art, d_art1
        nonlocal c_list_list, supply_list_list

        liefno:int = 0
        D_art = Dml_art
        D_art1 = Dml_artdep
        c_list_list.clear()
        supply_list_list.clear()

        if curr_dept == 0:

            dml_art_obj_list = []
            for dml_art, l_artikel, l_untergrup in db_session.query(Dml_art, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (Dml_art.datum == (selected_date - 1))).all():
                if dml_art._recid in dml_art_obj_list:
                    continue
                else:
                    dml_art_obj_list.append(dml_art._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.grp = l_untergrup.bezeich
                c_list.zwkum = l_untergrup.zwkum
                c_list.bezeich = l_artikel.bezeich
                c_list.qty = dml_art.anzahl
                c_list.price = dml_art.einzelpreis
                c_list.unit = l_artikel.masseinheit
                c_list.content = l_artikel.inhalt
                c_list.amount = c_list.qty * c_list.price
                c_list.qty1 = c_list.qty
                c_list.price1 = c_list.price
                c_list.id = entry(0, dml_art.userinit, ";")

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == dml_art.artnr) &  (L_bestand.lager_nr == 0)).first()

                if l_bestand:
                    c_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 202) &  (Queasy.number1 == 0) &  (Queasy.number2 == dml_art.artnr) &  (Queasy.date1 == dml_art.datum)).first()

                if queasy:
                    c_list.remark = queasy.char1


                d_art = D_art()
                db_session.add(d_art)

                d_art.artnr = dml_art.artnr
                d_art.datum = selected_date
                d_art.userinit = user_init
                d_art.anzahl = dml_art.anzahl
                d_art.einzelpreis = dml_art.einzelpreis

        else:

            dml_artdep_obj_list = []
            for dml_artdep, l_artikel, l_untergrup in db_session.query(Dml_artdep, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == Dml_artdep.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (Dml_artdep.datum == (selected_date - 1)) &  (Dml_artdep.departement == curr_dept)).all():
                if dml_artdep._recid in dml_artdep_obj_list:
                    continue
                else:
                    dml_artdep_obj_list.append(dml_artdep._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.grp = l_untergrup.bezeich
                c_list.zwkum = l_untergrup.zwkum
                c_list.bezeich = l_artikel.bezeich
                c_list.qty = dml_artdep.anzahl
                c_list.price = dml_artdep.einzelpreis
                c_list.unit = l_artikel.masseinheit
                c_list.content = l_artikel.inhalt
                c_list.deliver = dml_artdep.geliefert
                c_list.amount = c_list.qty * c_list.price
                c_list.qty1 = c_list.qty
                c_list.price1 = c_list.price
                c_list.id = entry(0, dml_artdep.userinit, ";")
                c_list.dept = curr_dept

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == dml_artdep.artnr) &  (L_bestand.lager_nr == 0)).first()

                if l_bestand:
                    c_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 202) &  (Queasy.number1 == dml_artdep.departement) &  (Queasy.number2 == dml_artdep.artnr) &  (Queasy.date1 == dml_artdep.datum)).first()

                if queasy:
                    c_list.remark = queasy.char1


                d_art1 = D_art1()
                db_session.add(d_art1)

                d_art1.artnr = dml_artdep.artnr
                d_art1.datum = selected_date
                d_art1.userinit = user_init
                d_art1.anzahl = dml_artdep.anzahl
                d_art1.einzelpreis = dml_artdep.einzelpreis
                d_art1.departement = curr_dept

        approve_flag = False

    copy_articles()

    return generate_output()