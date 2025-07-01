#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, L_order, L_lieferant, L_artikel, Parameters

def po_list_btn_print_webbl(case_type:int, all_supp:bool, stattype:int, deptno:int, from_date:date, to_date:date, billdate:date, disp_comm:bool, l_orderhdr_docu_nr:string, str4:string, l_supp_lief_nr:int):

    prepare_cache ([L_orderhdr, L_order, L_lieferant, L_artikel, Parameters])

    output_list_list = []
    po_list_list = []
    detail_po_list_list = []
    ind:int = 0
    l_order1_lieferdatum:string = ""
    l_order1_lieferdatum_eff:string = ""
    l_odrhdr_lieferdatum:string = ""
    l_order1_rechnungswert:string = ""
    l_orderhdr = l_order = l_lieferant = l_artikel = parameters = None

    cost_list = output_list = po_list = detail_po_list = l_odrhdr = l_order1 = l_order2 = l_supplier = l_art = l_art2 = None

    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    output_list_list, Output_list = create_model("Output_list", {"str":string, "pos":int})
    po_list_list, Po_list = create_model("Po_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "odrhdr_lieferdatum":date, "bestellart":string, "besteller":string, "lief_fax2":string, "order1_lieferdatum":date, "lief_fax3":string, "lieferdatum_eff":date, "rechnungswert":Decimal, "pr_number":string})
    detail_po_list_list, Detail_po_list = create_model("Detail_po_list", {"bestelldatum":date, "artnr":string, "bezeich":string, "lief_fax3":string, "txtnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "geliefert":Decimal, "angebot_lief1":int})

    L_odrhdr = create_buffer("L_odrhdr",L_orderhdr)
    L_order1 = create_buffer("L_order1",L_order)
    L_order2 = create_buffer("L_order2",L_order)
    L_supplier = create_buffer("L_supplier",L_lieferant)
    L_art = create_buffer("L_art",L_artikel)
    L_art2 = create_buffer("L_art2",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        return {"output-list": output_list_list, "po-list": po_list_list, "detail-po-list": detail_po_list_list}

    def create_costlist():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    def print_polist1():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str + to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        order_instruction_detail()

                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str + to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, l_orderhdr_docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        tes:string = ""
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)

        po_list = Po_list()
        po_list_list.append(po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        l_supp = None
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        L_supp =  create_buffer("L_supp",L_lieferant)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)

        po_list = Po_list()
        po_list_list.append(po_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.bestelldatum, L_odrhdr.docu_nr, L_supplier.firma).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        order_instruction_detail()

                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_supplier.firma, L_odrhdr.bestelldatum, L_odrhdr.docu_nr).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 1) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True


                    output_list.pos = 9
                    output_list.str = output_list.str + to_string(l_odrhdr.bestelldatum)
                    output_list.str = output_list.str + to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + " " + " "
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str + to_string(l_supplier.firma, "x(16)")
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    detail_po_list.bezeich = detail_po_list.bezeich + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
                    detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


                    detail_po_list = Detail_po_list()
                    detail_po_list_list.append(detail_po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        detail_po_list.bezeich = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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


                    l_order2_obj_list = {}
                    l_order2 = L_order()
                    l_art2 = L_artikel()
                    for l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2.rechnungswert, l_order2.lief_fax, l_order2._recid, l_order2.artnr, l_order2.txtnr, l_order2.anzahl, l_order2.einzelpreis, l_order2.warenwert, l_order2.geliefert, l_order2.angebot_lief, l_art2.bezeich, l_art2._recid in db_session.query(L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2.rechnungswert, L_order2.lief_fax, L_order2._recid, L_order2.artnr, L_order2.txtnr, L_order2.anzahl, L_order2.einzelpreis, L_order2.warenwert, L_order2.geliefert, L_order2.angebot_lief, L_art2.bezeich, L_art2._recid).join(L_art2,(L_art2.artnr == L_order2.artnr)).filter(
                             (L_order2.docu_nr == l_odrhdr.docu_nr) & (L_order2.loeschflag == 2) & (L_order2.pos > 0)).order_by(L_art2.bezeich).all():
                        if l_order2_obj_list.get(l_order2._recid):
                            continue
                        else:
                            l_order2_obj_list[l_order2._recid] = True


                        output_list.str = output_list.str +\
                                to_string(l_order2.artnr, "9999999 ") +\
                                to_string(l_art2.bezeich, "x(24) ") +\
                                to_string(l_order2.lief_fax[2], "x(12) ") +\
                                to_string(l_order2.txtnr, " >>9 ") +\
                                to_string(l_order2.anzahl, "->>>,>>9.99 ") +\
                                to_string(l_order2.einzelpreis, " >,>>>,>>>,>>9 ") +\
                                to_string(l_order2.warenwert, "->>,>>>,>>>,>>9 ") +\
                                to_string(l_order2.geliefert, "->,>>>,>>9.99 ") +\
                                to_string(l_order2.angebot_lief[0], " >>9")


                        output_list = Output_list()
                        output_list_list.append(output_list)

                        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
                        detail_po_list.bezeich = l_art2.bezeich
                        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
                        detail_po_list.txtnr = l_order2.txtnr
                        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
                        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
                        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
                        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list

        l_odrhdr = None
        l_order1 = None
        l_order2 = None
        l_supplier = None
        l_art = None
        l_art2 = None
        statflag:int = 0
        L_odrhdr =  create_buffer("L_odrhdr",L_orderhdr)
        L_order1 =  create_buffer("L_order1",L_order)
        L_order2 =  create_buffer("L_order2",L_order)
        L_supplier =  create_buffer("L_supplier",L_lieferant)
        L_art =  create_buffer("L_art",L_artikel)
        L_art2 =  create_buffer("L_art2",L_artikel)
        output_list = Output_list()
        output_list_list.append(output_list)


        if stattype == 0:

            if deptno <= 0:

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum >= billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lieferdatum < billdate) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

                l_odrhdr_obj_list = {}
                l_odrhdr = L_orderhdr()
                l_supplier = L_lieferant()
                l_order1 = L_order()
                for l_odrhdr.bestelldatum, l_odrhdr.angebot_lief, l_odrhdr.docu_nr, l_odrhdr.lief_fax, l_odrhdr.lieferdatum, l_odrhdr.bestellart, l_odrhdr.besteller, l_odrhdr._recid, l_supplier.firma, l_supplier._recid, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1.rechnungswert, l_order1.lief_fax, l_order1._recid, l_order1.artnr, l_order1.txtnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.geliefert, l_order1.angebot_lief in db_session.query(L_odrhdr.bestelldatum, L_odrhdr.angebot_lief, L_odrhdr.docu_nr, L_odrhdr.lief_fax, L_odrhdr.lieferdatum, L_odrhdr.bestellart, L_odrhdr.besteller, L_odrhdr._recid, L_supplier.firma, L_supplier._recid, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1.rechnungswert, L_order1.lief_fax, L_order1._recid, L_order1.artnr, L_order1.txtnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.geliefert, L_order1.angebot_lief).join(L_supplier,(L_supplier.lief_nr == L_odrhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_odrhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_odrhdr.bestelldatum >= from_date) & (L_odrhdr.bestelldatum <= to_date) & (L_odrhdr.lief_nr == l_supp_lief_nr) & (L_odrhdr.betriebsnr <= 1) & (L_odrhdr.angebot_lief[inc_value(0)] == deptno)).order_by(L_odrhdr.docu_nr, L_supplier.firma, L_odrhdr.bestelldatum).all():
                    if l_odrhdr_obj_list.get(l_odrhdr._recid):
                        continue
                    else:
                        l_odrhdr_obj_list[l_odrhdr._recid] = True

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
                            to_string(" ")

                    cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.nr == l_odrhdr.angebot_lief[0]), first=True)

                    if cost_list:
                        output_list.str = output_list.str + cost_list.bezeich
                        po_list.bezeich = cost_list.bezeich
                    else:
                        output_list.str = output_list.str + " "
                        po_list.bezeich = ""
                    output_list.str = output_list.str + to_string(" ")
                    output_list.str = output_list.str +\
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
                    po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
                    po_list.pr_number = l_order1.lief_fax[0]


                    po_list = Po_list()
                    po_list_list.append(po_list)


                    if disp_comm and l_odrhdr.lief_fax[2] != "":
                        output_list.str = output_list.str + to_string(" Order Instruction: ")
                        po_list.firma = to_string(" Order Instruction: ")


                        for ind in range(1,80 + 1) :

                            if ind <= length(l_odrhdr.lief_fax[2]):

                                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


        output_list.str = output_list.str + to_string(" Order Instruction: ")
        detail_po_list.bezeich = to_string(" Order Instruction: ")


        for ind in range(1,80 + 1) :

            if ind <= length(l_odrhdr.lief_fax[2]):

                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


        output_list.str = output_list.str + to_string(" Order Instruction: ")
        po_list.firma = to_string(" Order Instruction: ")


        for ind in range(1,80 + 1) :

            if ind <= length(l_odrhdr.lief_fax[2]):

                if substring(l_odrhdr.lief_fax[2], ind - 1, 1) == chr_unicode(10):
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

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


        detail_po_list.bezeich = to_string(l_odrhdr.bestelldatum) + to_string(" ") + to_string(l_supplier.firma, "x(16)" + to_string(" "))
        detail_po_list.lief_fax3 = l_odrhdr.docu_nr + to_string(" ")


        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)

    def detail_po_list2():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


        detail_po_list.artnr = to_string(l_order2.artnr, "9999999 ")
        detail_po_list.bezeich = l_art2.bezeich
        detail_po_list.lief_fax3 = l_order2.lief_fax[2]
        detail_po_list.txtnr = l_order2.txtnr
        detail_po_list.anzahl =  to_decimal(l_order2.anzahl)
        detail_po_list.einzelpreis =  to_decimal(l_order2.einzelpreis)
        detail_po_list.warenwert =  to_decimal(l_order2.warenwert)
        detail_po_list.geliefert =  to_decimal(l_order2.geliefert)
        detail_po_list.angebot_lief1 = l_order2.angebot_lief[0]


        detail_po_list = Detail_po_list()
        detail_po_list_list.append(detail_po_list)

    def create_po_list():

        nonlocal output_list_list, po_list_list, detail_po_list_list, ind, l_order1_lieferdatum, l_order1_lieferdatum_eff, l_odrhdr_lieferdatum, l_order1_rechnungswert, l_orderhdr, l_order, l_lieferant, l_artikel, parameters
        nonlocal case_type, all_supp, stattype, deptno, from_date, to_date, billdate, disp_comm, l_orderhdr_docu_nr, str4, l_supp_lief_nr
        nonlocal l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2


        nonlocal cost_list, output_list, po_list, detail_po_list, l_odrhdr, l_order1, l_order2, l_supplier, l_art, l_art2
        nonlocal cost_list_list, output_list_list, po_list_list, detail_po_list_list


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
        po_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
        po_list.pr_number = l_order1.lief_fax[0]


        po_list = Po_list()
        po_list_list.append(po_list)

    create_costlist()

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