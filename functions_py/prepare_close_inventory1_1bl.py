#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import MetaData
from models import L_bestand, L_op, L_ophdr, L_pprice, L_kredit, Ap_journal, L_artikel, L_besthis, L_hauptgrp, L_lager, L_lieferant, L_liefumsatz, L_ophhis, L_ophis, L_order, L_orderhdr, L_quote, L_segment, L_umsatz, L_untergrup, L_verbrauch, L_zahlbed, H_rezept, H_rezlin, Htparam, Paramtext

import os
import platform

def prepare_close_inventory1_1bl(inv_type:int, user_init:string, port:string):

    prepare_cache ([Htparam, Paramtext])

    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    m_datum = None
    fb_datum = None
    billdate = None
    closedate = None
    begindate = None
    todate = None
    tlist_data = []
    curr_folder:string = ""
    lic_nr:string = " "
    type_inv:string = " "
    period:date = None
    doit:bool = False
    fb_close_date:date = None
    mat_close_date:date = None
    last_journ_transgl:date = None
    l_bestand = l_op = l_ophdr = l_pprice = l_kredit = ap_journal = l_artikel = l_besthis = l_hauptgrp = l_lager = l_lieferant = l_liefumsatz = l_ophhis = l_ophis = l_order = l_orderhdr = l_quote = l_segment = l_umsatz = l_untergrup = l_verbrauch = l_zahlbed = h_rezept = h_rezlin = htparam = paramtext = None

    t_l_bestand = t_l_op = t_l_ophdr = t_l_pprice = t_l_kredit = t_ap_journal = t_l_artikel = t_l_besthis = t_l_hauptgrp = t_l_lager = t_l_lieferant = t_l_liefumsatz = t_l_ophhis = t_l_ophis = t_l_order = t_l_orderhdr = t_l_quote = t_l_segment = t_l_umsatz = t_l_untergrup = t_l_verbrauch = t_l_zahlbed = t_h_rezept = t_h_rezlin = tlist = ophis_fnb = ophis_mat = None

    t_l_bestand_data, T_l_bestand = create_model_like(L_bestand)
    t_l_op_data, T_l_op = create_model_like(L_op)
    t_l_ophdr_data, T_l_ophdr = create_model_like(L_ophdr)
    t_l_pprice_data, T_l_pprice = create_model_like(L_pprice)
    t_l_kredit_data, T_l_kredit = create_model_like(L_kredit)
    t_ap_journal_data, T_ap_journal = create_model_like(Ap_journal)
    t_l_artikel_data, T_l_artikel = create_model_like(L_artikel)
    t_l_besthis_data, T_l_besthis = create_model_like(L_besthis)
    t_l_hauptgrp_data, T_l_hauptgrp = create_model_like(L_hauptgrp)
    t_l_lager_data, T_l_lager = create_model_like(L_lager)
    t_l_lieferant_data, T_l_lieferant = create_model_like(L_lieferant)
    t_l_liefumsatz_data, T_l_liefumsatz = create_model_like(L_liefumsatz)
    t_l_ophhis_data, T_l_ophhis = create_model_like(L_ophhis)
    t_l_ophis_data, T_l_ophis = create_model_like(L_ophis)
    t_l_order_data, T_l_order = create_model_like(L_order)
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr)
    t_l_quote_data, T_l_quote = create_model_like(L_quote)
    t_l_segment_data, T_l_segment = create_model_like(L_segment)
    t_l_umsatz_data, T_l_umsatz = create_model_like(L_umsatz)
    t_l_untergrup_data, T_l_untergrup = create_model_like(L_untergrup)
    t_l_verbrauch_data, T_l_verbrauch = create_model_like(L_verbrauch)
    t_l_zahlbed_data, T_l_zahlbed = create_model_like(L_zahlbed)
    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept)
    t_h_rezlin_data, T_h_rezlin = create_model_like(H_rezlin)
    tlist_data, Tlist = create_model("Tlist", {"table_name":string, "objfile":bytes})

    Ophis_fnb = create_buffer("Ophis_fnb",L_ophis)
    Ophis_mat = create_buffer("Ophis_mat",L_ophis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_data, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal inv_type, user_init, port
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_data, t_l_op_data, t_l_ophdr_data, t_l_pprice_data, t_l_kredit_data, t_ap_journal_data, t_l_artikel_data, t_l_besthis_data, t_l_hauptgrp_data, t_l_lager_data, t_l_lieferant_data, t_l_liefumsatz_data, t_l_ophhis_data, t_l_ophis_data, t_l_order_data, t_l_orderhdr_data, t_l_quote_data, t_l_segment_data, t_l_umsatz_data, t_l_untergrup_data, t_l_verbrauch_data, t_l_zahlbed_data, t_h_rezept_data, t_h_rezlin_data, tlist_data

        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "m_datum": m_datum, "fb_datum": fb_datum, "billdate": billdate, "closedate": closedate, "begindate": begindate, "todate": todate, "tlist": tlist_data}

    def dump_data_to_sql(tableName):
        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_data, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal inv_type, user_init, port
        nonlocal ophis_fnb, ophis_mat

        db_session = local_storage.db_session

        engine = db_session.get_bind()
        metadata = MetaData()
        metadata.reflect(engine)

        lines = []

        table = metadata.tables[tableName] 
        
        with engine.connect() as conn:
            rows = conn.execute(table.select()).fetchall()

        for row in rows:
            values = dict(row._mapping) if hasattr(row, "_mapping") else dict(row)
            insert_sql = table.insert().values(**values).compile(
                engine,
                compile_kwargs={"literal_binds": True}
            )
            lines.append(str(insert_sql) + ";")

        output_path = os.path.join(curr_folder, f"{tableName}.sql")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        
    def dump_files():

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_data, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal inv_type, user_init, port
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_data, t_l_op_data, t_l_ophdr_data, t_l_pprice_data, t_l_kredit_data, t_ap_journal_data, t_l_artikel_data, t_l_besthis_data, t_l_hauptgrp_data, t_l_lager_data, t_l_lieferant_data, t_l_liefumsatz_data, t_l_ophhis_data, t_l_ophis_data, t_l_order_data, t_l_orderhdr_data, t_l_quote_data, t_l_segment_data, t_l_umsatz_data, t_l_untergrup_data, t_l_verbrauch_data, t_l_zahlbed_data, t_h_rezept_data, t_h_rezlin_data, tlist_data

        list_d = [ "l_bestand", 
                    "l_op", 
                    "l_ophdr", 
                    "l_pprice", 
                    "l_kredit", 
                    "ap_journal",
                    "l_artikel",
                    "l_besthis",
                    "l_hauptgrp",
                    "l_lager",
                    "l_lieferant",
                    "l_liefumsatz",
                    "l_ophhis",
                    "l_ophis",
                    "l_order",
                    "l_orderh",
                    "l_quote",
                    "l_segment",
                    "l_umsatz",
                    "l_untergrup",
                    "l_verbrauch",
                    "l_zahlbed"
                ]
        
        for file_d in list_d:
            file_path = os.path.join(curr_folder, f"{file_d}.sql")
            if os.path.exists(file_path):
                os.remove(file_path)

        for file_d in list_d:
            dump_data_to_sql(file_d)

    def create_file():

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_data, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal inv_type, user_init, port
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_data, t_l_op_data, t_l_ophdr_data, t_l_pprice_data, t_l_kredit_data, t_ap_journal_data, t_l_artikel_data, t_l_besthis_data, t_l_hauptgrp_data, t_l_lager_data, t_l_lieferant_data, t_l_liefumsatz_data, t_l_ophhis_data, t_l_ophis_data, t_l_order_data, t_l_orderhdr_data, t_l_quote_data, t_l_segment_data, t_l_umsatz_data, t_l_untergrup_data, t_l_verbrauch_data, t_l_zahlbed_data, t_h_rezept_data, t_h_rezlin_data, tlist_data


        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-bestan.d")

        # for t_l_bestand in query(t_l_bestand_data):
        #     EXPORT STREAM s1 t_l_bestand
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-bestan.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-op.d")

        # for t_l_op in query(t_l_op_data):
        #     EXPORT STREAM s1 t_l_op
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-op.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-ophdr.d")

        # for t_l_ophdr in query(t_l_ophdr_data):
        #     EXPORT STREAM s1 t_l_ophdr
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-ophdr.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-pprice.d")

        # for t_l_pprice in query(t_l_pprice_data):
        #     EXPORT STREAM s1 t_l_pprice
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-pprice.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-kredit.d")

        # for t_l_kredit in query(t_l_kredit_data):
        #     EXPORT STREAM s1 t_l_kredit
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-kredit.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/ap-journ.d")

        # for t_ap_journal in query(t_ap_journal_data):
        #     EXPORT STREAM s1 t_ap_journal
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "ap-journ.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-artike.d")

        # for t_l_artikel in query(t_l_artikel_data):
        #     EXPORT STREAM s1 t_l_artikel
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-artike.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-besta1.d")

        # for t_l_besthis in query(t_l_besthis_data):
        #     EXPORT STREAM s1 t_l_besthis
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-besta1.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-hauptg.d")

        # for t_l_hauptgrp in query(t_l_hauptgrp_data):
        #     EXPORT STREAM s1 t_l_hauptgrp
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-hauptg.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-lager.d")

        # for t_l_lager in query(t_l_lager_data):
        #     EXPORT STREAM s1 t_l_lager
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-lager.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-liefer.d")

        # for t_l_lieferant in query(t_l_lieferant_data):
        #     EXPORT STREAM s1 t_l_lieferant
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-liefer.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-liefum.d")

        # for t_l_liefumsatz in query(t_l_liefumsatz_data):
        #     EXPORT STREAM s1 t_l_liefumsatz
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-liefum.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-ophhis.d")

        # for t_l_ophhis in query(t_l_ophhis_data):
        #     EXPORT STREAM s1 t_l_ophhis
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-ophhis.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-ophis.d")

        # for t_l_ophis in query(t_l_ophis_data):
        #     EXPORT STREAM s1 t_l_ophis
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-ophis.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-order.d")

        # for t_l_order in query(t_l_order_data):
        #     EXPORT STREAM s1 t_l_order
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-order.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-orderh.d")

        # for t_l_orderhdr in query(t_l_orderhdr_data):
        #     EXPORT STREAM s1 t_l_orderhdr
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-orderh.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-quote.d")

        # for t_l_quote in query(t_l_quote_data):
        #     EXPORT STREAM s1 t_l_quote
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-quote.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-segmen.d")

        # for t_l_segment in query(t_l_segment_data):
        #     EXPORT STREAM s1 t_l_segment
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-segmen.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-umsatz.d")

        # for t_l_umsatz in query(t_l_umsatz_data):
        #     EXPORT STREAM s1 t_l_umsatz
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-umsatz.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-unterg.d")

        # for t_l_untergrup in query(t_l_untergrup_data):
        #     EXPORT STREAM s1 t_l_untergrup
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-unterg.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-verbra.d")

        # for t_l_verbrauch in query(t_l_verbrauch_data):
        #     EXPORT STREAM s1 t_l_verbrauch
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-verbra.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/l-zahlbe.d")

        # for t_l_zahlbed in query(t_l_zahlbed_data):
        #     EXPORT STREAM s1 t_l_zahlbed
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "l-zahlbe.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/h-rezept.d")

        # for t_h_rezept in query(t_h_rezept_data):
        #     EXPORT STREAM s1 t_h_rezept
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "h-rezept.d"

        # OUTPUT STREAM s1 TO VALUE (curr_folder + "/h-rezlin.d")

        # for t_h_rezlin in query(t_h_rezlin_data):
        #     EXPORT STREAM s1 h_rezlin
        # OUTPUT STREAM s1 CLOSE
        # tlist = Tlist()
        # tlist_data.append(tlist)

        # tlist.table_name = "h-rezlin.d"

    def decode_string(in_str:string):

        nonlocal f_endkum, b_endkum, m_endkum, m_datum, fb_datum, billdate, closedate, begindate, todate, tlist_data, curr_folder, lic_nr, type_inv, period, doit, fb_close_date, mat_close_date, last_journ_transgl, l_bestand, l_op, l_ophdr, l_pprice, l_kredit, ap_journal, l_artikel, l_besthis, l_hauptgrp, l_lager, l_lieferant, l_liefumsatz, l_ophhis, l_ophis, l_order, l_orderhdr, l_quote, l_segment, l_umsatz, l_untergrup, l_verbrauch, l_zahlbed, h_rezept, h_rezlin, htparam, paramtext
        nonlocal inv_type, user_init, port
        nonlocal ophis_fnb, ophis_mat


        nonlocal t_l_bestand, t_l_op, t_l_ophdr, t_l_pprice, t_l_kredit, t_ap_journal, t_l_artikel, t_l_besthis, t_l_hauptgrp, t_l_lager, t_l_lieferant, t_l_liefumsatz, t_l_ophhis, t_l_ophis, t_l_order, t_l_orderhdr, t_l_quote, t_l_segment, t_l_umsatz, t_l_untergrup, t_l_verbrauch, t_l_zahlbed, t_h_rezept, t_h_rezlin, tlist, ophis_fnb, ophis_mat
        nonlocal t_l_bestand_data, t_l_op_data, t_l_ophdr_data, t_l_pprice_data, t_l_kredit_data, t_ap_journal_data, t_l_artikel_data, t_l_besthis_data, t_l_hauptgrp_data, t_l_lager_data, t_l_lieferant_data, t_l_liefumsatz_data, t_l_ophhis_data, t_l_ophis_data, t_l_order_data, t_l_orderhdr_data, t_l_quote_data, t_l_segment_data, t_l_umsatz_data, t_l_untergrup_data, t_l_verbrauch_data, t_l_zahlbed_data, t_h_rezept_data, t_h_rezlin_data, tlist_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_datum = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_datum = htparam.fdate

    if inv_type == 1:
        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    else:
        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

    billdate = htparam.fdate

    if get_month(billdate) == 1:
        closedate = billdate + timedelta(days=28)
    else:
        closedate = billdate + timedelta(days=30)

    closedate = date_mdy(get_month(closedate), 1, get_year(closedate)) - timedelta(days=1)
    begindate = date_mdy(get_month(closedate), 1, get_year(closedate))
    todate = closedate + timedelta(days=32)
    todate = date_mdy(get_month(todate), 1, get_year(todate)) - timedelta(days=1)

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 232).with_for_update().first()
    htparam.flogical = True
    pass

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1035)]})
    last_journ_transgl = htparam.fdate

    if inv_type == 1:
        mat_close_date = get_output(htpdate(221))

        if mat_close_date == last_journ_transgl:

            ophis_mat = db_session.query(Ophis_mat).filter(
                     (Ophis_mat.op_art == 3) & (get_month(Ophis_mat.datum) == get_month(mat_close_date)) & (get_year(Ophis_mat.datum) == get_year(mat_close_date))).first()

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
                     (Ophis_fnb.op_art == 1) & (get_month(Ophis_fnb.datum) == get_month(fb_close_date)) & (get_year(Ophis_fnb.datum) == get_year(fb_close_date))).first()

            if ophis_fnb:
                doit = False

            elif not ophis_fnb:
                doit = True
        else:
            doit = False

    if doit:

        if platform.system().lower()  == ("Windows").lower() :
            curr_folder = "c:\\backupinv\\bkpinv-" + port + "-" + lic_nr + "-ALL-" +\
                to_string(get_month(period) , "99") + to_string(get_year(period) , "9999")
        else:
            curr_folder = "/usr1/vhp/backupinv/bkpinv-" + port + "-" + lic_nr + "-ALL-" +\
                to_string(get_month(period) , "99") + to_string(get_year(period) , "9999")

        os.makedirs(curr_folder, exist_ok=True)
        dump_files()
        # create_file()

    if inv_type == 1:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 2:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    elif inv_type == 3:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 221).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 224).with_for_update().first()
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    return generate_output()

