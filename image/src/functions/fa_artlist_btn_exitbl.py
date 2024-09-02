from functions.additional_functions import *
import decimal
from models import Mathis, Fa_artikel, Counters, Mhis_line

def fa_artlist_btn_exitbl(flag:int, mathis_nr:int, spec:str, locate:str, picture_file:str, upgrade_part:bool, fibukonto:str, credit_fibu:str, debit_fibu:str, user_init:str, curr_location:str, m_list:[M_list], fa_art:[Fa_art]):
    curr_mathisnr = 0
    created:bool = False
    mathis = fa_artikel = counters = mhis_line = None

    m_list = fa_art = None

    m_list_list, M_list = create_model_like(Mathis)
    fa_art_list, Fa_art = create_model_like(Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, mhis_line


        nonlocal m_list, fa_art
        nonlocal m_list_list, fa_art_list
        return {"curr_mathisnr": curr_mathisnr}

    def new_mathis():

        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, mhis_line


        nonlocal m_list, fa_art
        nonlocal m_list_list, fa_art_list

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 17)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 17

        if counters.counter == 0:
            counters.counter_bez = "Material / Fixed Asset"
        counters.counter = counters.counter + 1
        mathis = Mathis()
        db_session.add(mathis)

        mathis.nr = counters.counter
        mathis.datum = m_list.datum
        mathis.name = m_list.name
        mathis.supplier = m_list.supplier
        mathis.model = m_list.model
        mathis.mark = m_list.mark
        mathis.asset = m_list.asset
        mathis.price = m_list.price
        mathis.spec = spec
        mathis.location = locate
        mathis.remark = m_list.remark
        mathis.fname = picture_file
        curr_mathisnr = mathis.nr

        if upgrade_part:
            mathis.flag = 2
        else:
            mathis.flag = 1
        fa_artikel = Fa_artikel()
        db_session.add(fa_artikel)

        fa_artikel.nr = counters.counter
        fa_artikel.lief_nr = fa_art.lief_nr
        fa_artikel.gnr = fa_art.gnr
        fa_artikel.subgrp = fa_art.subgrp
        fa_artikel.katnr = fa_art.katnr
        fa_artikel.fibukonto = fibukonto
        fa_artikel.credit_fibu = credit_fibu
        fa_artikel.debit_fibu = debit_fibu
        fa_artikel.anzahl = fa_art.anzahl
        fa_artikel.anz100 = fa_art.anzahl
        fa_artikel.warenwert = fa_art.warenwert
        fa_artikel.depn_wert = fa_art.depn_wert
        fa_artikel.book_wert = fa_art.book_wert
        fa_artikel.anz_depn = fa_art.anz_depn
        fa_artikel.next_depn = fa_art.next_depn
        fa_artikel.first_depn = fa_art.first_depn
        fa_artikel.last_depn = fa_art.last_depn
        fa_artikel.id = user_init
        created = True

        mathis = db_session.query(Mathis).first()

        counters = db_session.query(Counters).first()

        fa_artikel = db_session.query(Fa_artikel).first()

    def chg_mathis():

        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, mhis_line


        nonlocal m_list, fa_art
        nonlocal m_list_list, fa_art_list

        mathis = db_session.query(Mathis).filter(
                (Mathis.nr == mathis_nr)).first()
        mathis.datum = m_list.datum
        mathis.name = m_list.name
        mathis.supplier = m_list.supplier
        mathis.model = m_list.model
        mathis.mark = m_list.mark
        mathis.spec = spec
        mathis.asset = m_list.asset
        mathis.location = locate
        mathis.price = m_list.price
        mathis.remark = m_list.remark
        mathis.fname = picture_file

        if upgrade_part:
            mathis.flag = 2
        else:
            mathis.flag = 1

        mathis = db_session.query(Mathis).first()

        fa_artikel = db_session.query(Fa_artikel).filter(
                (Fa_artikel.nr == mathis_nr)).first()
        fa_artikel.lief_nr = fa_art.lief_nr
        fa_artikel.gnr = fa_art.gnr
        fa_artikel.subgrp = fa_art.subgrp
        fa_artikel.katnr = fa_art.katnr
        fa_artikel.fibukonto = fibukonto
        fa_artikel.credit_fibu = credit_fibu
        fa_artikel.debit_fibu = debit_fibu
        fa_artikel.anzahl = fa_art.anzahl
        fa_artikel.anz100 = fa_art.anzahl
        fa_artikel.warenwert = fa_art.warenwert
        fa_artikel.depn_wert = fa_art.depn_wert
        fa_artikel.book_wert = fa_art.book_wert
        fa_artikel.anz_depn = fa_art.anz_depn
        fa_artikel.next_depn = fa_art.next_depn
        fa_artikel.first_depn = fa_art.first_depn
        fa_artikel.last_depn = fa_art.last_depn
        fa_artikel.cid = user_init
        fa_artikel.changed = get_current_date()

        fa_artikel = db_session.query(Fa_artikel).first()

        if curr_location != mathis.location:
            mhis_line = Mhis_line()
            db_session.add(mhis_line)

            mhis_line.nr = mathis_nr
            mhis_line.datum = get_current_date()
            mhis_line.remark = "Change Location      From: " + curr_location +\
                    "   To: " + mathis.location

            mhis_line = db_session.query(Mhis_line).first()


    m_list = query(m_list_list, first=True)

    fa_art = query(fa_art_list, first=True)

    if flag == 1:
        new_mathis()

    elif flag == 2:
        chg_mathis()

    return generate_output()