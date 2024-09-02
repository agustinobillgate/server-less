from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import L_bestand, L_op, L_ophdr, L_pprice, L_kredit, Ap_journal, L_artikel, L_besthis, L_hauptgrp, L_lager, L_lieferant, L_liefumsatz, L_ophhis, L_ophis, L_order, L_orderhdr, L_quote, L_segment, L_umsatz, L_untergrup, L_verbrauch, L_zahlbed, H_rezept, H_rezlin, Htparam, Paramtext

def prepare_close_inventory1_1bl(inv_type:int, user_init:str, port:str):
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    m_datum = None
    fb_datum = None
    billdate = None
    closedate = None
    begindate = None
    todate = None
    tlist_list = []
    curr_folder:str = ""
    lic_nr:str = " "
    type_inv:str = " "
    period:date = None
    doit:bool = False
    fb_close_date:date = None
    mat_close_date:date = None
    last_journ_transgl:date = None
    l_bestand = l_op = l_ophdr = l_pprice = l_kredit = ap_journal = l_artikel = l_besthis = l_hauptgrp = l_lager = l_lieferant = l_liefumsatz = l_ophhis = l_ophis = l_order = l_orderhdr = l_quote = l_segment = l_umsatz = l_untergrup = l_verbrauch = l_zahlbed = h_rezept = h_rezlin = htparam = paramtext = None

    t_l_bestand = t_l_op = t_l_ophdr = t_l_pprice = t_l_kredit = t_ap_journal = t_l_artikel = t_l_besthis = t_l_hauptgrp = t_l_lager = t_l_lieferant = t_l_liefumsatz = t_l_ophhis = t_l_ophis = t_l_order = t_l_orderhdr = t_l_quote = t_l_segment = t_l_umsatz = t_l_untergrup = t_l_verbrauch = t_l_zahlbed = t_h_rezept = t_h_rezlin = tlist = ophis_fnb = ophis_mat = None

    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)
    t_l_op_list, T_l_op = create_model_like(L_op)
    t_l_ophdr_list, T_l_ophdr = create_model_like(L_ophdr)
    t_l_pprice_list, T_l_pprice = create_model_like(L_pprice)
    t_l_kredit_list, T_l_kredit = create_model_like(L_kredit)
    t_ap_journal_list, T_ap_journal = create_model_like(Ap_journal)
    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)
    t_l_besthis_list, T_l_besthis = create_model_like(L_besthis)
    t_l_hauptgrp_list, T_l_hauptgrp = create_model_like(L_hauptgrp)
    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)
    t_l_liefumsatz_list, T_l_liefumsatz = create_model_like(L_liefumsatz)
    t_l_ophhis_list, T_l_ophhis = create_model_like(L_ophhis)
    t_l_ophis_list, T_l_ophis = create_model_like(L_ophis)
    t_l_order_list, T_l_order = create_model_like(L_order)
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr)
    t_l_quote_list, T_l_quote = create_model_like(L_quote)
    t_l_segment_list, T_l_segment = create_model_like(L_segment)
    t_l_umsatz_list, T_l_umsatz = create_model_like(L_umsatz)
    t_l_untergrup_list, T_l_untergrup = create_model_like(L_untergrup)
    t_l_verbrauch_list, T_l_verbrauch = create_model_like(L_verbrauch)
    t_l_zahlbed_list, T_l_zahlbed = create_model_like(L_zahlbed)
    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept)
    t_h_rezlin_list, T_h_rezlin = create_model_like(H_rezlin)
    tlist_list, Tlist = create_model("Tlist", {"table_name":str, "objfile":bytes})

    Ophis_fnb = L_ophis
    Ophis_mat = L_ophis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_list, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_list, t_l_op_list, t_l_ophdr_list, t_l_pprice_list, t_l_kredit_list, t_ap_journal_list, t_l_artikel_list, t_l_besthis_list, t_l_hauptgrp_list, t_l_lager_list, t_l_lieferant_list, t_l_liefumsatz_list, t_l_ophhis_list, t_l_ophis_list, t_l_order_list, t_l_orderhdr_list, t_l_quote_list, t_l_segment_list, t_l_umsatz_list, t_l_untergrup_list, t_l_verbrauch_list, t_l_zahlbed_list, t_h_rezept_list, t_h_rezlin_list, tlist_list
        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "m_datum": m_datum, "fb_datum": fb_datum, "billdate": billdate, "closedate": closedate, "begindate": begindate, "todate": todate, "tlist": tlist_list}

    def dump_files():

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_list, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_list, t_l_op_list, t_l_ophdr_list, t_l_pprice_list, t_l_kredit_list, t_ap_journal_list, t_l_artikel_list, t_l_besthis_list, t_l_hauptgrp_list, t_l_lager_list, t_l_lieferant_list, t_l_liefumsatz_list, t_l_ophhis_list, t_l_ophis_list, t_l_order_list, t_l_orderhdr_list, t_l_quote_list, t_l_segment_list, t_l_umsatz_list, t_l_untergrup_list, t_l_verbrauch_list, t_l_zahlbed_list, t_h_rezept_list, t_h_rezlin_list, tlist_list


        OS_DELETE VALUE (curr_folder + "/l_bestan.d")
        OS_DELETE VALUE (curr_folder + "/l_op.d")
        OS_DELETE VALUE (curr_folder + "/l_ophdr.d")
        OS_DELETE VALUE (curr_folder + "/l_pprice.d")
        OS_DELETE VALUE (curr_folder + "/l_kredit.d")
        OS_DELETE VALUE (curr_folder + "/ap_journ.d")
        OS_DELETE VALUE (curr_folder + "/l_artike.d")
        OS_DELETE VALUE (curr_folder + "/l_besta1.d")
        OS_DELETE VALUE (curr_folder + "/l_hauptg.d")
        OS_DELETE VALUE (curr_folder + "/l_lager.d")
        OS_DELETE VALUE (curr_folder + "/l_liefer.d")
        OS_DELETE VALUE (curr_folder + "/l_liefum.d")
        OS_DELETE VALUE (curr_folder + "/l_ophhis.d")
        OS_DELETE VALUE (curr_folder + "/l_ophis.d")
        OS_DELETE VALUE (curr_folder + "/l_order.d")
        OS_DELETE VALUE (curr_folder + "/l_orderh.d")
        OS_DELETE VALUE (curr_folder + "/l_quote.d")
        OS_DELETE VALUE (curr_folder + "/l_segmen.d")
        OS_DELETE VALUE (curr_folder + "/l_umsatz.d")
        OS_DELETE VALUE (curr_folder + "/l_unterg.d")
        OS_DELETE VALUE (curr_folder + "/l_verbra.d")
        OS_DELETE VALUE (curr_folder + "/l_zahlbe.d")

        for l_bestand in db_session.query(L_bestand).all():
            t_l_bestand = T_l_bestand()
            t_l_bestand_list.append(t_l_bestand)

            buffer_copy(l_bestand, t_l_bestand)

        for l_op in db_session.query(L_op).all():
            t_l_op = T_l_op()
            t_l_op_list.append(t_l_op)

            buffer_copy(l_op, t_l_op)

        for l_ophdr in db_session.query(L_ophdr).all():
            t_l_ophdr = T_l_ophdr()
            t_l_ophdr_list.append(t_l_ophdr)

            buffer_copy(l_ophdr, t_l_ophdr)

        for l_pprice in db_session.query(L_pprice).all():
            t_l_pprice = T_l_pprice()
            t_l_pprice_list.append(t_l_pprice)

            buffer_copy(l_pprice, t_l_pprice)

        for l_kredit in db_session.query(L_kredit).all():
            t_l_kredit = T_l_kredit()
            t_l_kredit_list.append(t_l_kredit)

            buffer_copy(l_kredit, t_l_kredit)

        for ap_journal in db_session.query(Ap_journal).all():
            t_ap_journal = T_ap_journal()
            t_ap_journal_list.append(t_ap_journal)

            buffer_copy(ap_journal, t_ap_journal)

        for l_artikel in db_session.query(L_artikel).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            buffer_copy(l_artikel, t_l_artikel)

        for l_besthis in db_session.query(L_besthis).all():
            t_l_besthis = T_l_besthis()
            t_l_besthis_list.append(t_l_besthis)

            buffer_copy(l_besthis, t_l_besthis)

        for l_hauptgrp in db_session.query(L_hauptgrp).all():
            t_l_hauptgrp = T_l_hauptgrp()
            t_l_hauptgrp_list.append(t_l_hauptgrp)

            buffer_copy(l_hauptgrp, t_l_hauptgrp)

        for l_lager in db_session.query(L_lager).all():
            t_l_lager = T_l_lager()
            t_l_lager_list.append(t_l_lager)

            buffer_copy(l_lager, t_l_lager)

        for l_lieferant in db_session.query(L_lieferant).all():
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_list.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)

        for l_liefumsatz in db_session.query(L_liefumsatz).all():
            t_l_liefumsatz = T_l_liefumsatz()
            t_l_liefumsatz_list.append(t_l_liefumsatz)

            buffer_copy(l_liefumsatz, t_l_liefumsatz)

        for l_ophhis in db_session.query(L_ophhis).all():
            t_l_ophhis = T_l_ophhis()
            t_l_ophhis_list.append(t_l_ophhis)

            buffer_copy(l_ophhis, t_l_ophhis)

        for l_ophis in db_session.query(L_ophis).all():
            t_l_ophis = T_l_ophis()
            t_l_ophis_list.append(t_l_ophis)

            buffer_copy(l_ophis, t_l_ophis)

        for l_order in db_session.query(L_order).all():
            t_l_order = T_l_order()
            t_l_order_list.append(t_l_order)

            buffer_copy(l_order, t_l_order)

        for l_orderhdr in db_session.query(L_orderhdr).all():
            t_l_orderhdr = T_l_orderhdr()
            t_l_orderhdr_list.append(t_l_orderhdr)

            buffer_copy(l_orderhdr, t_l_orderhdr)

        for l_quote in db_session.query(L_quote).all():
            t_l_quote = T_l_quote()
            t_l_quote_list.append(t_l_quote)

            buffer_copy(l_quote, t_l_quote)

        for l_segment in db_session.query(L_segment).all():
            t_l_segment = T_l_segment()
            t_l_segment_list.append(t_l_segment)

            buffer_copy(l_segment, t_l_segment)

        for l_umsatz in db_session.query(L_umsatz).all():
            t_l_umsatz = T_l_umsatz()
            t_l_umsatz_list.append(t_l_umsatz)

            buffer_copy(l_umsatz, t_l_umsatz)

        for l_untergrup in db_session.query(L_untergrup).all():
            t_l_untergrup = T_l_untergrup()
            t_l_untergrup_list.append(t_l_untergrup)

            buffer_copy(l_untergrup, t_l_untergrup)

        for l_verbrauch in db_session.query(L_verbrauch).all():
            t_l_verbrauch = T_l_verbrauch()
            t_l_verbrauch_list.append(t_l_verbrauch)

            buffer_copy(l_verbrauch, t_l_verbrauch)

        for l_zahlbed in db_session.query(L_zahlbed).all():
            t_l_zahlbed = T_l_zahlbed()
            t_l_zahlbed_list.append(t_l_zahlbed)

            buffer_copy(l_zahlbed, t_l_zahlbed)

        for h_rezept in db_session.query(H_rezept).all():
            t_h_rezept = T_h_rezept()
            t_h_rezept_list.append(t_h_rezept)

            buffer_copy(h_rezept, t_h_rezept)

        for h_rezlin in db_session.query(H_rezlin).all():
            t_h_rezlin = T_h_rezlin()
            t_h_rezlin_list.append(t_h_rezlin)

            buffer_copy(h_rezlin, t_h_rezlin)

    def create_file():

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_list, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_list, t_l_op_list, t_l_ophdr_list, t_l_pprice_list, t_l_kredit_list, t_ap_journal_list, t_l_artikel_list, t_l_besthis_list, t_l_hauptgrp_list, t_l_lager_list, t_l_lieferant_list, t_l_liefumsatz_list, t_l_ophhis_list, t_l_ophis_list, t_l_order_list, t_l_orderhdr_list, t_l_quote_list, t_l_segment_list, t_l_umsatz_list, t_l_untergrup_list, t_l_verbrauch_list, t_l_zahlbed_list, t_h_rezept_list, t_h_rezlin_list, tlist_list


        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_bestan.d")

        for t_l_bestand in query(t_l_bestand_list):
            EXPORT STREAM s1 t_l_bestand
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_bestan.d"


        COPY_LOB FROM FILE curr_folder + "/l_bestan.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_op.d")

        for t_l_op in query(t_l_op_list):
            EXPORT STREAM s1 t_l_op
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_op.d"


        COPY_LOB FROM FILE curr_folder + "/l_op.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_ophdr.d")

        for t_l_ophdr in query(t_l_ophdr_list):
            EXPORT STREAM s1 t_l_ophdr
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_ophdr.d"


        COPY_LOB FROM FILE curr_folder + "/l_ophdr.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_pprice.d")

        for t_l_pprice in query(t_l_pprice_list):
            EXPORT STREAM s1 t_l_pprice
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_pprice.d"


        COPY_LOB FROM FILE curr_folder + "/l_pprice.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_kredit.d")

        for t_l_kredit in query(t_l_kredit_list):
            EXPORT STREAM s1 t_l_kredit
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_kredit.d"


        COPY_LOB FROM FILE curr_folder + "/l_kredit.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/ap_journ.d")

        for t_ap_journal in query(t_ap_journal_list):
            EXPORT STREAM s1 t_ap_journal
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "ap_journ.d"


        COPY_LOB FROM FILE curr_folder + "/ap_journ.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_artike.d")

        for t_l_artikel in query(t_l_artikel_list):
            EXPORT STREAM s1 t_l_artikel
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_artike.d"


        COPY_LOB FROM FILE curr_folder + "/l_artike.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_besta1.d")

        for t_l_besthis in query(t_l_besthis_list):
            EXPORT STREAM s1 t_l_besthis
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_besta1.d"


        COPY_LOB FROM FILE curr_folder + "/l_besta1.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_hauptg.d")

        for t_l_hauptgrp in query(t_l_hauptgrp_list):
            EXPORT STREAM s1 t_l_hauptgrp
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_hauptg.d"


        COPY_LOB FROM FILE curr_folder + "/l_hauptg.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_lager.d")

        for t_l_lager in query(t_l_lager_list):
            EXPORT STREAM s1 t_l_lager
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_lager.d"


        COPY_LOB FROM FILE curr_folder + "/l_lager.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_liefer.d")

        for t_l_lieferant in query(t_l_lieferant_list):
            EXPORT STREAM s1 t_l_lieferant
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_liefer.d"


        COPY_LOB FROM FILE curr_folder + "/l_liefer.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_liefum.d")

        for t_l_liefumsatz in query(t_l_liefumsatz_list):
            EXPORT STREAM s1 t_l_liefumsatz
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_liefum.d"


        COPY_LOB FROM FILE curr_folder + "/l_liefum.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_ophhis.d")

        for t_l_ophhis in query(t_l_ophhis_list):
            EXPORT STREAM s1 t_l_ophhis
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_ophhis.d"


        COPY_LOB FROM FILE curr_folder + "/l_ophhis.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_ophis.d")

        for t_l_ophis in query(t_l_ophis_list):
            EXPORT STREAM s1 t_l_ophis
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_ophis.d"


        COPY_LOB FROM FILE curr_folder + "/l_ophis.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_order.d")

        for t_l_order in query(t_l_order_list):
            EXPORT STREAM s1 t_l_order
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_order.d"


        COPY_LOB FROM FILE curr_folder + "/l_order.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_orderh.d")

        for t_l_orderhdr in query(t_l_orderhdr_list):
            EXPORT STREAM s1 t_l_orderhdr
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_orderh.d"


        COPY_LOB FROM FILE curr_folder + "/l_orderh.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_quote.d")

        for t_l_quote in query(t_l_quote_list):
            EXPORT STREAM s1 t_l_quote
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_quote.d"


        COPY_LOB FROM FILE curr_folder + "/l_quote.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_segmen.d")

        for t_l_segment in query(t_l_segment_list):
            EXPORT STREAM s1 t_l_segment
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_segmen.d"


        COPY_LOB FROM FILE curr_folder + "/l_segmen.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_umsatz.d")

        for t_l_umsatz in query(t_l_umsatz_list):
            EXPORT STREAM s1 t_l_umsatz
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_umsatz.d"


        COPY_LOB FROM FILE curr_folder + "/l_umsatz.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_unterg.d")

        for t_l_untergrup in query(t_l_untergrup_list):
            EXPORT STREAM s1 t_l_untergrup
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_unterg.d"


        COPY_LOB FROM FILE curr_folder + "/l_unterg.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_verbra.d")

        for t_l_verbrauch in query(t_l_verbrauch_list):
            EXPORT STREAM s1 t_l_verbrauch
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_verbra.d"


        COPY_LOB FROM FILE curr_folder + "/l_verbra.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/l_zahlbe.d")

        for t_l_zahlbed in query(t_l_zahlbed_list):
            EXPORT STREAM s1 t_l_zahlbed
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "l_zahlbe.d"


        COPY_LOB FROM FILE curr_folder + "/l_zahlbe.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/h_rezept.d")

        for t_h_rezept in query(t_h_rezept_list):
            EXPORT STREAM s1 t_h_rezept
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "h_rezept.d"


        COPY_LOB FROM FILE curr_folder + "/h_rezept.d" TO tlist.objfile
        OUTPUT STREAM s1 TO VALUE (curr_folder + "/h_rezlin.d")

        for t_h_rezlin in query(t_h_rezlin_list):
            EXPORT STREAM s1 h_rezlin
        OUTPUT STREAM s1 CLOSE
        tlist = Tlist()
        tlist_list.append(tlist)

        tlist.table_name = "h_rezlin.d"


        COPY_LOB FROM FILE curr_folder + "/h_rezlin.d" TO tlist.objfile

    def decode_string(in_str:str):

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_list, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_list, t_l_op_list, t_l_ophdr_list, t_l_pprice_list, t_l_kredit_list, t_ap_journal_list, t_l_artikel_list, t_l_besthis_list, t_l_hauptgrp_list, t_l_lager_list, t_l_lieferant_list, t_l_liefumsatz_list, t_l_ophhis_list, t_l_ophis_list, t_l_order_list, t_l_orderhdr_list, t_l_quote_list, t_l_segment_list, t_l_umsatz_list, t_l_untergrup_list, t_l_verbrauch_list, t_l_zahlbed_list, t_h_rezept_list, t_h_rezlin_list, tlist_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    f_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    b_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 268)).first()
    m_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_datum = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_datum = htparam.fdate

    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
    billdate = htparam.fdate

    if get_month(billdate) == 1:
        closedate = billdate + 28
    else:
        closedate = billdate + 30
    closedate = date_mdy(get_month(closedate) , 1, get_year(closedate)) - 1
    begindate = date_mdy(get_month(closedate) , 1, get_year(closedate))
    todate = closedate + 32
    todate = date_mdy(get_month(todate) , 1, get_year(todate)) - 1

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 232)).first()
    htparam.flogical = True

    htparam = db_session.query(Htparam).first()


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        lic_nr = decode_string(paramtext.ptexte)

    if inv_type == 1:
        type_inv = "FnB"
        period = fb_datum

    elif inv_type == 2:
        type_inv = "MAT"
        period = m_datum

    elif inv_type == 3:
        type_inv = "ALL"
        period = fb_datum


    doit = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1035)).first()
    last_journ_transgl = htparam.fdate

    if inv_type == 1:
        mat_close_date = get_output(htpdate(221))

        if mat_close_date == last_journ_transgl:

            ophis_mat = db_session.query(Ophis_mat).filter(
                    (Ophis_mat.op_art == 3) &  (get_month(Ophis_mat.datum) == get_month(mat_close_date)) &  (get_year(Ophis_mat.datum) == get_year(mat_close_date))).first()

            if ophis_mat:
                doit = False

            elif not ophis_mat:
                doit = True
        else:
            doit = False

    elif inv_type == 2:
        fb_close_date = get_output(htpdate(224))

        if fb_close_date == last_journ_transgl:

            ophis_fnb = db_session.query(Ophis_fnb).filter(
                    (Ophis_fnb.op_art == 1) &  (get_month(Ophis_fnb.datum) == get_month(fb_close_date)) &  (get_year(Ophis_fnb.datum) == get_year(fb_close_date))).first()

            if ophis_fnb:
                doit = False

            elif not ophis_fnb:
                doit = True
        else:
            doit = False

    if doit:

        if OPSYS.lower()  == "WIN32":
            curr_folder = "c:\\backupinv\\bkpinv-" + port + "-" + lic_nr + "-ALL-" +\
                to_string(get_month(period) , "99") + to_string(get_year(period) , "9999")


        else:
            curr_folder = "/usr1/vhp/backupinv/bkpinv-" + port + "-" + lic_nr + "-ALL-" +\
                to_string(get_month(period) , "99") + to_string(get_year(period) , "9999")


        OS_COMMAND SILENT VALUE ("mkdir -p " + curr_folder)
        dump_files()
        create_file()

    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).first()

    return generate_output()