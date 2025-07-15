from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Calls, Bediener

str_list_list, Str_list = create_model("Str_list", {"zero_rate":bool, "c_recid":int, "destination":str, "rechnr":int, "nebenstelle":str, "datum":date, "rufnummer":str, "username":str, "guest_rate":decimal, "pabx_rate":decimal, "zeit":str, "dauer":str, "zinr":str, "impulse":int, "leitung":int, "sequence":int, "print":str})

def calls_listbl(case_type:int, last_sort:int, from_date:date, to_date:date, from_ext:str, to_ext:str, stattype:int, price_decimal:int, double_currency:bool, fr_number:str, to_number:str, dialed_nr:str):
    amount1 = to_decimal("0.0")
    amount2 = to_decimal("0.0")
    tot_pulse = 0
    str_list_list = []
    ext_amt1:decimal = to_decimal("0.0")
    ext_amt2:decimal = to_decimal("0.0")
    i:int = 0
    d:date = None
    last_ext:str = ""
    prstr:List[str] = ["False", "True"]
    calls = bediener = None

    str_list = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount1, amount2, tot_pulse, str_list_list, ext_amt1, ext_amt2, i, d, last_ext, prstr, calls, bediener
        nonlocal case_type, last_sort, from_date, to_date, from_ext, to_ext, stattype, price_decimal, double_currency, fr_number, to_number, dialed_nr

        nonlocal str_list
        nonlocal str_list_list
        return {"amount1": amount1, "amount2": amount2, "tot_pulse": tot_pulse, "str-list": str_list_list}

    def create_list():

        nonlocal amount1, amount2, tot_pulse, str_list_list, ext_amt1, ext_amt2, i, d, last_ext, prstr, calls, bediener
        nonlocal case_type, last_sort, from_date, to_date, from_ext, to_ext, stattype, price_decimal, double_currency, fr_number, to_number, dialed_nr
        nonlocal str_list
        nonlocal str_list_list

        if last_sort == 1:
            print("Masuk 1.1")
            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype)).order_by(Calls.zeit.desc()).all():
                    create_record()
            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0)).order_by(Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  
                            (Calls.buchflag == stattype) &  
                            (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  
                            (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  
                            (Calls.datum == from_date) &  
                            (Calls.zeit >= 0)
                        ).order_by(Calls.zeit.desc()).all():
                        create_record()
            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0)).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            elif (from_ext).lower()  == (to_ext).lower() :
                print("Masuk 1.1c")
                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  
                        (Calls.buchflag == stattype) &  
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  
                        (Calls.datum >= from_date) &  
                        (Calls.datum <= to_date) &  
                        (Calls.zeit >= 0)).all():
                    create_record()
            else:
                # for d in date_range(to_date,from_date BY -1):
                num_days = (to_date - from_date).days
                for dd in range(num_days):
                    d = to_date - timedelta(days=dd)
                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  
                            (Calls.buchflag == stattype) &  
                            (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  
                            (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  
                            (Calls.datum == d) &  
                            (Calls.zeit >= 0)
                        ).order_by(Calls.zeit.desc()).all():
                        create_record()
            
        elif last_sort == 2:
            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype)).order_by(Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0)).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext == "":
                            last_ext = calls.nebenstelle

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)

                else:
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0)).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)


            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0)).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:
                last_ext = ""
                ext_amt1 =  to_decimal("0")
                ext_amt2 =  to_decimal("0")

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0)).order_by(Calls.nebenstelle, Calls.datum.desc(), Calls.zeit.desc()).all():

                    if last_ext == "":
                        last_ext = calls.nebenstelle

                    if last_ext != calls.nebenstelle:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.destination = "T O T A L "

                        if price_decimal == 0:

                            if ext_amt1 <= 999999999:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)

                        if double_currency or price_decimal != 0:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:

                            if ext_amt2 <= 999999999:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                        str_list.impulse = tot_pulse
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        last_ext = calls.nebenstelle
                        ext_amt1 =  to_decimal("0")
                        ext_amt2 =  to_decimal("0")
                    ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                    ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                    create_record()
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.destination = "T O T A L "

                if price_decimal == 0:

                    if ext_amt1 <= 999999999:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                else:
                    str_list.pabx_rate =  to_decimal(ext_amt1)

                if double_currency or price_decimal != 0:
                    str_list.guest_rate =  to_decimal(ext_amt2)


                else:

                    if ext_amt2 <= 999999999:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                str_list.impulse = tot_pulse
                str_list = Str_list()
                str_list_list.append(str_list)

        elif last_sort == 3:
            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype)).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0)).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0)).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()

            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0)).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0)).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()


    def create_list1():
        nonlocal amount1, amount2, tot_pulse, str_list_list, ext_amt1, ext_amt2, i, d, last_ext, prstr, calls, bediener
        nonlocal case_type, last_sort, from_date, to_date, from_ext, to_ext, stattype, price_decimal, double_currency, fr_number, to_number, dialed_nr

        nonlocal str_list
        nonlocal str_list_list

        if last_sort == 1:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.zeit.desc()).all():
                        create_record()

            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()

        elif last_sort == 2:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext == "":
                            last_ext = calls.nebenstelle

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)

                else:
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)


            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:
                last_ext = ""
                ext_amt1 =  to_decimal("0")
                ext_amt2 =  to_decimal("0")

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.nebenstelle, Calls.datum.desc(), Calls.zeit.desc()).all():

                    if last_ext == "":
                        last_ext = calls.nebenstelle

                    if last_ext != calls.nebenstelle:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.destination = "T O T A L "

                        if price_decimal == 0:

                            if ext_amt1 <= 999999999:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)

                        if double_currency or price_decimal != 0:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:

                            if ext_amt2 <= 999999999:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                        str_list.impulse = tot_pulse
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        last_ext = calls.nebenstelle
                        ext_amt1 =  to_decimal("0")
                        ext_amt2 =  to_decimal("0")
                    ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                    ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                    create_record()
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.destination = "T O T A L "

                if price_decimal == 0:

                    if ext_amt1 <= 999999999:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                else:
                    str_list.pabx_rate =  to_decimal(ext_amt1)

                if double_currency or price_decimal != 0:
                    str_list.guest_rate =  to_decimal(ext_amt2)


                else:

                    if ext_amt2 <= 999999999:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                str_list.impulse = tot_pulse
                str_list = Str_list()
                str_list_list.append(str_list)

        elif last_sort == 3:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()

            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) >= (fr_number).lower()) &  (func.lower(Calls.rufnummer) < (to_number).lower())).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()

    def create_list2():
        nonlocal amount1, amount2, tot_pulse, str_list_list, ext_amt1, ext_amt2, i, d, last_ext, prstr, calls, bediener
        nonlocal case_type, last_sort, from_date, to_date, from_ext, to_ext, stattype, price_decimal, double_currency, fr_number, to_number, dialed_nr
        nonlocal str_list
        nonlocal str_list_list

        if last_sort == 1:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.zeit.desc()).all():
                        create_record()

            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()

        elif last_sort == 2:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext == "":
                            last_ext = calls.nebenstelle

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)

                else:
                    last_ext = ""
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.nebenstelle, Calls.zeit.desc()).all():

                        if last_ext != calls.nebenstelle:
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            str_list.destination = "T O T A L "

                            if price_decimal == 0:

                                if ext_amt1 <= 999999999:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                                else:
                                    str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)

                            if double_currency or price_decimal != 0:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:

                                if ext_amt2 <= 999999999:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                                else:
                                    str_list.guest_rate =  to_decimal(ext_amt2)


                            str_list.impulse = tot_pulse
                            str_list = Str_list()
                            str_list_list.append(str_list)

                            last_ext = calls.nebenstelle
                            ext_amt1 =  to_decimal("0")
                            ext_amt2 =  to_decimal("0")
                        ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                        ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                        create_record()
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.destination = "T O T A L "

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)

                    if double_currency or price_decimal != 0:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:

                        if ext_amt2 <= 999999999:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                    str_list.impulse = tot_pulse
                    str_list = Str_list()
                    str_list_list.append(str_list)


            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:
                last_ext = ""
                ext_amt1 =  to_decimal("0")
                ext_amt2 =  to_decimal("0")

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.nebenstelle, Calls.datum.desc(), Calls.zeit.desc()).all():

                    if last_ext == "":
                        last_ext = calls.nebenstelle

                    if last_ext != calls.nebenstelle:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.destination = "T O T A L "

                        if price_decimal == 0:

                            if ext_amt1 <= 999999999:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                            else:
                                str_list.pabx_rate =  to_decimal(ext_amt1)


                        else:
                            str_list.pabx_rate =  to_decimal(ext_amt1)

                        if double_currency or price_decimal != 0:
                            str_list.guest_rate =  to_decimal(ext_amt2)


                        else:

                            if ext_amt2 <= 999999999:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                            else:
                                str_list.guest_rate =  to_decimal(ext_amt2)


                        str_list.impulse = tot_pulse
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        last_ext = calls.nebenstelle
                        ext_amt1 =  to_decimal("0")
                        ext_amt2 =  to_decimal("0")
                    ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                    ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                    create_record()
                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.destination = "T O T A L "

                if price_decimal == 0:

                    if ext_amt1 <= 999999999:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                    else:
                        str_list.pabx_rate =  to_decimal(ext_amt1)


                else:
                    str_list.pabx_rate =  to_decimal(ext_amt1)

                if double_currency or price_decimal != 0:
                    str_list.guest_rate =  to_decimal(ext_amt2)


                else:

                    if ext_amt2 <= 999999999:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                    else:
                        str_list.guest_rate =  to_decimal(ext_amt2)


                str_list.impulse = tot_pulse
                str_list = Str_list()
                str_list_list.append(str_list)

        elif last_sort == 3:

            if from_date == to_date and from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (Calls.buchflag == stattype) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                    create_record()

            elif from_date == to_date:

                if from_ext.lower()  == ("0").lower()  and to_ext.lower()  == ("99999").lower() :

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()
                else:

                    for calls in db_session.query(Calls).filter(
                            (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum == from_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.rufnummer, Calls.zeit.desc()).all():
                        create_record()

            elif from_ext.lower()  == (to_ext).lower() :

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) == (from_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()
            else:

                for calls in db_session.query(Calls).filter(
                        (Calls.key == 1) &  (Calls.buchflag == stattype) &  (func.lower(Calls.nebenstelle) >= (from_ext).lower()) &  (func.lower(Calls.nebenstelle) <= (to_ext).lower()) &  (Calls.datum >= from_date) &  (Calls.datum <= to_date) &  (Calls.zeit >= 0) &  (func.lower(Calls.rufnummer) == (dialed_nr).lower())).order_by(Calls.rufnummer, Calls.datum.desc(), Calls.zeit.desc()).all():
                    create_record()

    def create_record():
        nonlocal amount1, amount2, tot_pulse, str_list_list, ext_amt1, ext_amt2, d, last_ext, prstr, calls, bediener
        nonlocal case_type, last_sort, from_date, to_date, from_ext, to_ext, stattype, price_decimal, double_currency, fr_number, to_number, dialed_nr
        nonlocal str_list
        nonlocal str_list_list
        print("Create:", calls)

        i:int = 0
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.zero_rate = (calls.gastbetrag == 0)
        str_list.c_recid = calls._recid
        str_list.destination = to_string(calls.satz_id, "x(16)")
        str_list.rechnr = calls.rechnr
        str_list.nebenstelle = calls.nebenstelle
        str_list.datum = calls.datum
        str_list.rufnummer = calls.rufnummer
        str_list.zeit = to_string(calls.zeit, "HH:MM")

        if calls.betriebsnr == 0:
            str_list.print = "NO"
        else:
            str_list.print = "YES"

        if calls.aufschlag != 0:

            # if not bediener or not(bediener.nr == to_int(calls.aufschlag)):
            bediener = db_session.query(Bediener).filter(
                (Bediener.nr == to_int(calls.aufschlag))).first()

            if bediener:
                str_list.username = bediener.username

        if double_currency:

            if calls.leitung >= 10000:
                str_list.dauer = to_string(calls.dauer, "HH:MM:SS")
                str_list.zinr = calls.zinr
                str_list.impulse = calls.impulse
                str_list.leitung = calls.leitung
                str_list.guest_rate =  to_decimal(calls.gastbetrag)
                str_list.pabx_rate =  to_decimal(calls.pabxbetrag)


            else:
                str_list.dauer = to_string(calls.dauer, "HH:MM:SS")
                str_list.zinr = calls.zinr
                str_list.impulse = calls.impulse
                str_list.leitung = calls.leitung
                str_list.guest_rate =  to_decimal(calls.gastbetrag)
                str_list.pabx_rate =  to_decimal(calls.pabxbetrag)

        else:

            if price_decimal == 0:
                str_list.guest_rate =  to_decimal(calls.gastbetrag)
                str_list.pabx_rate =  to_decimal(calls.pabxbetrag)


            else:
                str_list.guest_rate =  to_decimal(calls.gastbetrag)
                str_list.pabx_rate =  to_decimal(calls.pabxbetrag)

            if calls.leitung >= 10000:
                str_list.dauer = to_string(calls.dauer, "HH:MM:SS")
                str_list.zinr = calls.zinr
                str_list.impulse = calls.impulse
                str_list.leitung = calls.leitung


            else:
                str_list.dauer = to_string(calls.dauer, "HH:MM:SS")
                str_list.zinr = calls.zinr
                str_list.impulse = calls.impulse
                str_list.leitung = calls.leitung

        amount1 = amount1 + calls.pabxbetrag
        amount2 = amount2 + calls.gastbetrag
        tot_pulse = tot_pulse + calls.impulse

    if case_type == 0:
        create_list()

    elif case_type == 1:
        create_list1()

    elif case_type == 2:
        create_list2()

    return generate_output()