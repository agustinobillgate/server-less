#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# 
# yusufwijasena, 13/01/2026
# fix cannot create new fix asset item
# cast value fa_art.anz_depn to integer
# fix mathis.nr value with counters.counter
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Fa_artikel, Counters, Queasy, Mhis_line

m_list_data, M_list = create_model_like(Mathis)
fa_art_data, Fa_art = create_model_like(Fa_artikel, {"start_date":date})

def fa_artlist_btn_exit_webbl(flag:int, mathis_nr:int, spec:string, locate:string, picture_file:string, upgrade_part:bool, fibukonto:string, credit_fibu:string, debit_fibu:string, user_init:string, curr_location:string, m_list_data:[M_list], fa_art_data:[Fa_art]):

    prepare_cache ([Mathis, Fa_artikel, Counters, Queasy, Mhis_line])

    curr_mathisnr = 0
    created:bool = False
    mathis = fa_artikel = counters = queasy = mhis_line = None

    m_list = fa_art = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, queasy, mhis_line
        nonlocal flag, mathis_nr, spec, locate, picture_file, upgrade_part, fibukonto, credit_fibu, debit_fibu, user_init, curr_location
        nonlocal m_list, fa_art

        return {"curr_mathisnr": curr_mathisnr}

    def new_mathis():
        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, queasy, mhis_line
        nonlocal flag, mathis_nr, spec, locate, picture_file, upgrade_part, fibukonto, credit_fibu, debit_fibu, user_init, curr_location
        nonlocal m_list, fa_art

        avail_counter:bool = False
        last_counter:int = 0

        # counters = get_cache (Counters, {"counter_no": [(eq, 17)]})
        counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 17)).with_for_update().first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 17

        if counters.counter == 0:
            counters.counter_bez = "Material / Fixed Asset"
        last_counter = counters.counter + 1
        while avail_counter == False:

            # mathis = get_cache (Mathis, {"nr": [(eq, last_counter)]})
            mathis = db_session.query(Mathis).filter((Mathis.nr == last_counter)).with_for_update().first()

            if mathis:
                last_counter = last_counter + 1
            else:
                avail_counter = True
                
        counters.counter = last_counter
        mathis = Mathis()

        mathis.nr = counters.counter
        mathis.datum = m_list.datum
        mathis.name = m_list.name
        mathis.supplier = m_list.supplier
        mathis.model = m_list.model
        mathis.mark = m_list.mark
        mathis.asset = m_list.asset
        mathis.price =  to_decimal(m_list.price)
        mathis.spec = spec
        mathis.location = locate
        mathis.remark = m_list.remark
        mathis.fname = picture_file
        curr_mathisnr = mathis.nr
        
        db_session.add(mathis)

        if upgrade_part:
            mathis.flag = 2
        else:
            mathis.flag = 1
            
        fa_artikel = Fa_artikel()

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
        fa_artikel.warenwert =  to_decimal(fa_art.warenwert)
        fa_artikel.depn_wert =  to_decimal(fa_art.depn_wert)
        fa_artikel.book_wert =  to_decimal(fa_art.book_wert)
        fa_artikel.anz_depn = to_int(fa_art.anz_depn)
        fa_artikel.next_depn = fa_art.next_depn
        fa_artikel.first_depn = fa_art.first_depn
        fa_artikel.last_depn = fa_art.last_depn
        fa_artikel.id = user_init
        created = True
        
        db_session.add(fa_artikel)

        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 314
        queasy.number1 = counters.counter
        queasy.date1 = fa_art.start_date
        

        db_session.commit()
        
    def chg_mathis():
        nonlocal curr_mathisnr, created, mathis, fa_artikel, counters, queasy, mhis_line
        nonlocal flag, mathis_nr, spec, locate, picture_file, upgrade_part, fibukonto, credit_fibu, debit_fibu, user_init, curr_location
        nonlocal m_list, fa_art

        next_date:date = None
        next_mon:int = 0
        next_yr:int = 0

        # mathis = get_cache (Mathis, {"nr": [(eq, mathis_nr)]})
        mathis = db_session.query(Mathis).filter(
                 (Mathis.nr == mathis_nr)).with_for_update().first()
        

        if mathis:
            mathis.datum = m_list.datum
            mathis.name = m_list.name
            mathis.supplier = m_list.supplier
            mathis.model = m_list.model
            mathis.mark = m_list.mark
            mathis.spec = spec
            mathis.asset = m_list.asset
            mathis.location = locate
            mathis.price =  to_decimal(m_list.price)
            mathis.remark = m_list.remark
            mathis.fname = picture_file
            
            if upgrade_part:
                mathis.flag = 2
            else:
                mathis.flag = 1
                
            # print(f"[LOG] updating: {mathis.nr}")
            # pass
            # db_session.refresh(mathis,with_for_update=True)

            # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis_nr)]})
            fa_artikel = db_session.query(Fa_artikel).filter(
                     (Fa_artikel.nr == mathis_nr)).with_for_update().first()

            if fa_artikel:
                fa_artikel.lief_nr = fa_art.lief_nr
                fa_artikel.gnr = fa_art.gnr
                fa_artikel.subgrp = fa_art.subgrp
                fa_artikel.katnr = fa_art.katnr
                fa_artikel.fibukonto = fibukonto
                fa_artikel.credit_fibu = credit_fibu
                fa_artikel.debit_fibu = debit_fibu
                fa_artikel.anzahl = fa_art.anzahl
                fa_artikel.anz100 = fa_art.anzahl
                fa_artikel.warenwert =  to_decimal(fa_art.warenwert)
                fa_artikel.depn_wert =  to_decimal(fa_art.depn_wert)
                fa_artikel.book_wert =  to_decimal(fa_art.book_wert)
                fa_artikel.anz_depn = to_int(fa_art.anz_depn)
                fa_artikel.next_depn = fa_art.next_depn
                fa_artikel.first_depn = fa_art.first_depn
                fa_artikel.last_depn = fa_art.last_depn
                fa_artikel.cid = user_init
                fa_artikel.changed = get_current_date()
                
                # print(f"[LOG] Updating fa_artikel: {fa_artikel.lief_nr}")

                queasy = get_cache (Queasy, {"key": [(eq, 314)],"number1": [(eq, mathis_nr)]})

                if queasy:
                    queasy.date1 = fa_art.start_date

                    if fa_artikel.posted  and fa_artikel.next_depn != None and fa_artikel.first_depn == None:
                        next_mon = get_month(queasy.date1) + 1
                        next_yr = get_year(queasy.date1)

                        if next_mon == 13:
                            next_mon = 1
                            next_yr = next_yr + 1
                        next_date = date_mdy(next_mon, 1, next_yr) - timedelta(days=1)
                        fa_artikel.next_depn = next_date


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 314
                    queasy.number1 = mathis_nr
                    queasy.date1 = fa_art.start_date
                    
                # pass
                # db_session.refresh(fa_artikel,with_for_update=True)

                if curr_location != mathis.location:
                    mhis_line = Mhis_line()

                    mhis_line.nr = mathis_nr
                    mhis_line.datum = get_current_date()
                    mhis_line.remark = "Change Location From: " + curr_location +\
                            " To: " + mathis.location

                    db_session.add(mhis_line)

    m_list = query(m_list_data, first=True)

    fa_art = query(fa_art_data, first=True)

    if flag == 1:
        new_mathis()

    elif flag == 2:
        chg_mathis()

    return generate_output()