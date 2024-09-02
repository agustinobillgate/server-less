from functions.additional_functions import *
import decimal
from datetime import date
from models import L_orderhdr, L_order, L_lieferant, L_artikel

def po_list_btn_print_webbl(case_type:int, all_supp:bool, stattype:int, deptno:int, from_date:date, to_date:date, billdate:date, disp_comm:bool, l_orderhdr_docu_nr:str, str4:str, l_supp_lief_nr:int):
    output_list_list = []
    po_list_list = []
    detail_po_list_list = []
    ind:int = 0
    l_order1_lieferdatum:str = ""
    l_order1_lieferdatum_eff:str = ""
    l_odrhdr_lieferdatum:str = ""
    l_order1_rechnungswert:str = ""
    l_orderhdr = l_order = l_lieferant = l_artikel = None

    output_list = po_list = detail_po_list = l_odrhdr = l_order1 = l_order2 = l_supplier = l_art = l_art2 = l_supp = None

    output_list_list, Output_list = create_model("Output_list", {"str":str, "pos":int})
    po_list_list, Po_list = create_model("Po_list", {"bestelldatum":date, "firma":str, "docu_nr":str, "odrhdr_lieferdatum":date, "bestellart":str, "besteller":str, "lief_fax2":str, "order1_lieferdatum":date, "lief_fax3":str, "lieferdatum_eff":date, "rechnungswert":decimal})
    detail_po_list_list, Detail_po_list = create_model("Detail_po_list", {"bestelldatum":date, "artnr":str, "bezeich":str, "lief_fax3":str, "txtnr":int, "anzahl":decimal, "einzelpreis":decimal, "warenwert":decimal, "geliefert":decimal, "angebot_lief1":int})

    L_odrhdr = L_orderhdr
    L_order1 = L_order
    L_order2 = L_order
    L_supplier = L_lieferant
    L_art = L_artikel
    L_art2 = L_artikel
    L_supp = L_lieferant

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list
        return {"output-list": output_list_list, "po-list": po_list_list, "detail-po-list": detail_po_list_list}

    def print_polist1():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str + to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        order_instruction_detail()

                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str + to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist2():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        tes:str = ""
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)

        po_list = Po_list()
        po_list_list.append(po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def print_polist11():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        L_supp = L_lieferant
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist22():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)

        po_list = Po_list()
        po_list_list.append(po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def print_polist1a():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            order_instruction_detail()

                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist2a():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def print_polist11a():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist22a():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def print_polist1b():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist2b():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def print_polist11b():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string("  Order Instruction: ")
                        detail_po_list.bezeich = to_string("  Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= len(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                    output_list.str = output_list.str + to_string(" ")
                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                else:
                                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                        output_list.str = output_list.str + to_string("")
                        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 1) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)


                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.pos = 9
                    output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            detail_po_list.bezeich = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            detail_po_list = Detail_po_list()
                            detail_po_list_list.append(detail_po_list)


                    l_order2_obj_list = []
                    for l_order2, l_art2 in db_session.query(L_order2, L_art2).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                            (L_order2.docu_nr == l_odrhdr.docu_nr) &  (L_order2.loeschflag == 2) &  (L_order2.pos > 0)).all():
                        if l_order2._recid in l_order2_obj_list:
                            continue
                        else:
                            l_order2_obj_list.append(l_order2._recid)


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], "   >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl = l_order2.anzahl
                        detail_po_list.einzelpreis = l_order2.einzelpreis
                        detail_po_list.warenwert = l_order2.warenwert
                        detail_po_list.geliefert = l_order2.geliefert
                        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


                        detail_po_list = Detail_po_list()
                        detail_po_list_list.append(detail_po_list)

                    output_list.str = output_list.str + str4


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)


    def print_polist22b():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list

        statflag:int = 0
        L_odrhdr = L_orderhdr
        L_order1 = L_order
        L_order2 = L_order
        L_supplier = L_lieferant
        L_art = L_artikel
        L_art2 = L_artikel
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum >= billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 1:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 1) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 2:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lieferdatum < billdate) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


        elif stattype == 3:

            if deptno <= 0:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)

            else:

                l_odrhdr_obj_list = []
                for l_odrhdr, l_supplier, l_order1 in db_session.query(L_odrhdr, L_supplier, L_order1).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) &  (L_order1.loeschflag == 2) &  (L_order1.pos == 0)).filter(
                        (L_odrhdr.bestelldatum >= from_date) &  (L_odrhdr.bestelldatum <= to_date) &  (L_odrhdr.lief_nr == l_supp_lief_nr) &  (L_odrhdr.betriebsnr <= 1) &  (L_odrhdr.angebot_lief[0] == deptno)).all():
                    if l_odrhdr._recid in l_odrhdr_obj_list:
                        continue
                    else:
                        l_odrhdr_obj_list.append(l_odrhdr._recid)

                    if l_order1.lieferdatum == None:
                        l_order1_lieferdatum = ""
                    else:
                        l_order1_lieferdatum = to_string(l_order1.lieferdatum)

                    if l_order1.lieferdatum_eff == None:
                        l_order1_lieferdatum_eff = ""
                    else:
                        l_order1_lieferdatum_eff = to_string(l_order1.lieferdatum_eff)
                    l_odrhdr_lieferdatum = to_string(l_odrhdr.lieferdatum)
                    l_order1_rechnungswert = to_string(l_order1.rechnungswert, " ->>,>>>,>>9.99")
                    output_list.str = output_list.str +\
                            to_string(l_odrhdr.bestelldatum) +\
                            to_string(" ") +\
                            to_string(l_supplier.firma, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.docu_nr, "x(16)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.bestellart, "x(10)") +\
                            to_string(" ") +\
                            to_string(l_odrhdr.besteller, "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[1], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1.lief_fax[2], "x(12)") +\
                            to_string(" ") +\
                            to_string(l_order1_lieferdatum_eff, "x(8)") +\
                            to_string(" ") +\
                            to_string(l_order1_rechnungswert)


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    po_list.bestelldatum = l_odrhdr.bestelldatum
                    po_list.firma = l_supplier.firma
                    po_list.docu_nr = l_odrhdr.docu_nr
                    po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
                    po_list.bestellart = l_odrhdr.bestellart
                    po_list.besteller = l_odrhdr.besteller
                    po_list.lief_fax2 = l_order1.lief_fax[1]
                    po_list.order1_lieferdatum = l_order1.lieferdatum
                    po_list.lief_fax3 = l_order1.lief_fax[2]
                    po_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    po_list.rechnungswert = l_order1.rechnungswert


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":

                        if disp_comm and l_odrhdr.lief_fax[2] != "":
                            output_list.str = output_list.str + to_string("  Order Instruction: ")
                            po_list.firma = to_string("  Order Instruction: ")


                            for ind in range(1,80 + 1) :

                                if ind <= len(l_odrhdr.lief_fax[2]):

                                    if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                                        output_list.str = output_list.str + to_string(" ")
                                        po_list.firma = po_list.firma + to_string(" ")


                                    else:
                                        output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                                        po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                            output_list.str = output_list.str + to_string("")
                            po_list.firma = po_list.firma + to_string("")


                            output_list = Output_list()
                            output_list_list.append(output_list)

                            po_list = Po_list()
                            po_list_list.append(po_list)


    def order_instruction_detail():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        output_list.str = output_list.str + to_string("  Order Instruction: ")
        detail_po_list.bezeich = to_string("  Order Instruction: ")


        for ind in range(1,80 + 1) :

            if ind <= len(l_odrhdr.lief_fax[2]):

                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ")
                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ")


                else:
                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


        output_list.str = output_list.str + to_string("")
        detail_po_list.bezeich = detail_po_list.bezeich + to_string("")


        output_list = Output_list()
        output_list_list.append(output_list)

        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)


    def order_instruction_po():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        output_list.str = output_list.str + to_string("  Order Instruction: ")
        po_list.firma = to_string("  Order Instruction: ")


        for ind in range(1,80 + 1) :

            if ind <= len(l_odrhdr.lief_fax[2]):

                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ")
                    po_list.firma = po_list.firma + to_string(" ")


                else:
                    output_list.str = output_list.str + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


                    po_list.firma = po_list.firma + to_string(substring(l_odrhdr.lief_fax[2], ind - 1, 1) , "x(1)")


        output_list.str = output_list.str + to_string("")
        po_list.firma = po_list.firma + to_string("")


        output_list = Output_list()
        output_list_list.append(output_list)

        po_list = Po_list()
        po_list_list.append(po_list)


    def detail_po_list1():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
        detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)


    def detail_po_list2():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
        detail_po_list.bezeich = l_art2.bezeich
        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
        detail_po_list.txtnr = l_order2.txtnr
        detail_po_list.anzahl = l_order2.anzahl
        detail_po_list.einzelpreis = l_order2.einzelpreis
        detail_po_list.warenwert = l_order2.warenwert
        detail_po_list.geliefert = l_order2.geliefert
        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)


    def create_po_list():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp


        nonlocal output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2, l_supp
        nonlocal output_list_list, po_list_list, detail_po_list_list


        po_list.bestelldatum = l_odrhdr.bestelldatum
        po_list.firma = l_supplier.firma
        po_list.docu_nr = l_odrhdr.docu_nr
        po_list.odrhdr_lieferdatum = l_odrhdr.lieferdatum
        po_list.bestellart = l_odrhdr.bestellart
        po_list.besteller = l_odrhdr.besteller
        po_list.lief_fax2 = l_order1.lief_fax[1]
        po_list.order1_lieferdatum = l_order1.lieferdatum
        po_list.lief_fax3 = l_order1.lief_fax[2]
        po_list.lieferdatum_eff = l_order1.lieferdatum_eff
        po_list.rechnungswert = l_order1.rechnungswert


        po_list = Po_list()
        po_list_list.append(po_list)


    if case_type == 1:
        print_polist1()

    elif case_type == 2:
        print_polist2()

    elif case_type == 3:
        print_polist11()

    elif case_type == 4:
        print_polist22()

    elif case_type == 5:
        print_polist1a()

    elif case_type == 6:
        print_polist2a()

    elif case_type == 7:
        print_polist11a()

    elif case_type == 8:
        print_polist22a()

    elif case_type == 9:
        print_polist1b()

    elif case_type == 10:
        print_polist2b()

    elif case_type == 11:
        print_polist11b()

    elif case_type == 12:
        print_polist22b()

    return generate_output()