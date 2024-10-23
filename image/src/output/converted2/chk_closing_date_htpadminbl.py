from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import random
from models import Htparam, Bediener, Res_history, Paramtext

def chk_closing_date_htpadminbl(htp_number:int, user_init:str, intval:int, decval:decimal, dateval:date, logval:bool, charval:str, htl_name:str):
    htp_wert = ""
    htp_logv = False
    htp_note = ""
    zahl = ""
    t_htparam_list = []
    htparam = bediener = res_history = paramtext = None

    t_htparam = None

    t_htparam_list, T_htparam = create_model_like(Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list
        return {"htp_wert": htp_wert, "htp_logv": htp_logv, "htp_note": htp_note, "zahl": zahl, "t-htparam": t_htparam_list}

    def update_htparam():

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        htpchar:str = ""
        lic_nr:str = ""

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == htp_number)).first()

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Change ParamNo " + to_string(htparam.paramnr) +\
                ": "
        res_history.action = "htparam"

        if htparam.feldtyp == 1:
            res_history.aenderung = res_history.aenderung + to_string(htparam.finteger) + " TO: " + to_string(intval)
            htparam.finteger = intval
            htp_wert = to_string(htparam.finteger)

        elif htparam.feldtyp == 2:
            res_history.aenderung = res_history.aenderung + to_string(htparam.fdecimal) + " TO: " + to_string(decval)
            htparam.fdecimal =  to_decimal(decval)
            htp_wert = to_string(htparam.fdecimal)

        elif htparam.feldtyp == 3:
            res_history.aenderung = res_history.aenderung + to_string(htparam.fdate) + " TO: " + to_string(dateval)
            htparam.fdate = dateval
            htp_wert = to_string(htparam.fdate)

        elif htparam.feldtyp == 4:
            res_history.aenderung = res_history.aenderung + to_string(htparam.flogical) + " TO: " + to_string(logval)
            htparam.flogical = logval
            htp_wert = to_string(htparam.flogical)
            htp_logv = htparam.flogical

        elif htparam.feldtyp == 5:
            res_history.aenderung = res_history.aenderung + to_string(htparam.fchar) + " TO: " + to_string(charval)
            htparam.fchar = charval
            htp_wert = to_string(htparam.fchar)
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(time, "HH:MM:SS")
        htparam.lupdate = htparam.lupdate
        htp_note = htparam.fdefault
        pass

        if htparam.paramgruppe == 99 or htparam.paramgruppe == 100:

            paramtext = db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == 243)).first()

            if paramtext and paramtext.ptexte != "":
                lic_nr = decode_string(paramtext.ptexte)
                htpchar = ""

                if htparam.feldtyp == 1:
                    htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(finteger, "9999")

                if htparam.feldtyp == 3:
                    htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(get_month(htparam.fdate) , "99") + to_string(get_day(htparam.fdate) , "99") + to_string(get_year(htparam.fdate) , "9999")

                elif htparam.feldtyp == 4:
                    htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(htparam.flogical)
                htpchar = encode_string(htpchar)
                htparam.fchar = htpchar

        if htparam.paramnr == 976:

            paramtext = db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == 976)).first()

            if paramtext:
                paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
                paramtext.notes = htparam.fchar

            if substring(proversion(), 0, 1) == ("1").lower() :
                encode_serial(lic_nr, htparam.fdate, htl_name)


    def decode_string(in_str:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def encode_string(in_str:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0
        ch:str = ""

        def generate_inner_output():
            return (out_str)

        j = random.randint(1, 9)
        ch = chr(asc(to_string(j)) + 23)
        out_str = ch
        j = asc(ch) - 70
        for len_ in range(1,len(in_str)  + 1) :
            out_str = out_str + chr (asc(substring(in_str, len_ - 1, 1)) + j)

        return generate_inner_output()


    def encode_serial(license:str, curr_date:date, hotel:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        datum:str = ""
        str1:str = ""
        str2:str = ""
        license_enc:str = ""
        datum_1_enc:str = ""
        datum_2_enc:str = ""
        schluessel:str = ""
        nama1:str = ""
        nama2:str = ""
        nama3:str = ""
        nama4:str = ""
        datum = to_string(get_month(curr_date) , "99") +\
                to_string(get_day(curr_date) , "99") +\
                to_string(get_year(curr_date) , "9999")


        datum_1_enc, license_enc, datum_2_enc, schluessel = encode_all(license, datum)
        nama1, nama2, nama3, nama4 = encode_hotel(datum_2_enc, schluessel, datum_1_enc, license_enc, hotel)
        str1 = datum_1_enc + " " + license_enc + " " + datum_2_enc + " " + schluessel
        str2 = nama1 + " " + nama2 + " " + nama3 + " " + nama4

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 200)).first()

        if paramtext:
            paramtext.passwort = str1

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 203)).first()

        if paramtext:
            paramtext.passwort = str2


    def encode_all(license:str, datum:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        license3 = ""
        datum1_teil1 = ""
        datum1_teil2 = ""
        schluessel = ""
        datum2:str = ""
        license2:str = ""
        datum_teil1:str = ""
        datum_teil2:str = ""
        flag:bool = True
        accept:bool = False
        accept1:bool = False

        def generate_inner_output():
            return (license3, datum1_teil1, datum1_teil2, schluessel)

        while (flag) :
            zahl = ""


            license2 = encode_serial_str(license, False)
            datum2 = encode_serial_str(datum, False)
            datum_teil1, datum_teil2 = cutword(datum2)
            zahl = encode_serial_str(zahl, True)
            zahl = encode_serial_str(zahl, True)
            schluessel = zahl


            accept1 = modulo_check(schluessel)

            if accept1:
                datum1_teil2 = encode_next(datum_teil2, schluessel)
                license3 = encode_next(license2, datum1_teil2)
                datum1_teil1 = encode_next(datum_teil1, license3)
                accept = serial_check(license3, datum1_teil1, datum1_teil2, schluessel)

                if accept:
                    flag = True

        return generate_inner_output()


    def encode_hotel(datum2:str, schluessel:str, datum1:str, license:str, hotel:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        name1 = ""
        name2 = ""
        name3 = ""
        name4 = ""

        def generate_inner_output():
            return (name1, name2, name3, name4)

        name1 = encode_name(datum2, hotel, 1)
        name2 = encode_name(schluessel, hotel, 2)
        name3 = encode_name(datum1, hotel, 3)
        name4 = encode_name(license, hotel, 4)

        return generate_inner_output()


    def encode_serial_str(in_str:str, prefix:bool):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_str = ""
        j:int = 0
        len_:int = 0
        len1:int = 0
        ch:str = ""

        def generate_inner_output():
            return (out_str)

        j = random.randint(1, 12)
        ch = chr(asc(to_string(j)) + 27)
        zahl = zahl + ch

        if prefix:
            out_str = ch
            j = asc(ch) - 70


        else:
            j = asc(ch) - 49


        for len_ in range(1,len(in_str)  + 1) :
            len1 = (13 * len_) % 5 + 6
            out_str = out_str + chr (asc(substring(in_str, len_ - 1, 1)) + j - len1)

        return generate_inner_output()


    def cutword(word:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        teil1 = ""
        teil2 = ""
        len_:int = 0
        halb:int = 0

        def generate_inner_output():
            return (teil1, teil2)

        len_ = len(word)
        halb = len_ / 2
        teil1 = substring(word, 0, halb)
        teil2 = substring(word, halb + 1 - 1, halb)

        return generate_inner_output()


    def modulo_check(wort:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        accept_key = False
        i:int = 0
        summe:int = 0

        def generate_inner_output():
            return (accept_key)

        for i in range(1,len(wort)  + 1) :
            summe = summe + (asc(substring(wort, i - 1, 1)) - 64) + i

        if (summe % 13) == 0:
            accept_key = True

        return generate_inner_output()


    def encode_next(in_str:str, schluessel:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_str = ""
        schluessel1:int = 0
        len_:int = 0
        reverse:int = 0
        len1:int = 0

        def generate_inner_output():
            return (out_str)

        for len_ in range(1,len(in_str)  + 1) :
            reverse = len(in_str) - len_ + 1
            schluessel1 = asc(substring(schluessel, reverse - 1, 1)) % 7 - 1
            out_str = out_str + chr (asc(substring(in_str, len_ - 1, 1)) - schluessel1 + len_ + 5)

        return generate_inner_output()


    def serial_check(wort1:str, wort2:str, wort3:str, wort4:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        accept = True
        i:int = 0
        j:int = 0
        alpha:int = 0
        wort:List[str] = create_empty_list(4,"")

        def generate_inner_output():
            return (accept)

        wort[0] = wort1
        wort[1] = wort2
        wort[2] = wort3
        wort[3] = wort4


        for i in range(1,4 + 1) :
            for j in range(1,4 + 1) :
                alpha = asc(substring(wort[i - 1], j - 1, 1))

                if alpha < 65 or alpha > 90:
                    accept = False

        return generate_inner_output()


    def encode_name(in_string:str, hotel:str, pos:int):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_string = ""
        i:int = 0
        hotel_int:int = 0
        string_int:int = 0
        summe:str = ""
        len_:int = 0

        def generate_inner_output():
            return (out_string)

        len_ = len(in_string)
        for i in range(1,len + 1) :
            hotel_int = char_number(substring(hotel, i + (pos - 1) * 4  - 1, 1))
            string_int = char_number(substring(in_string, i - 1, 1))
            summe = number_char(hotel_int + (2 * string_int % 10) + 1)
            out_string = out_string + summe

        return generate_inner_output()


    def char_number(in_char:str):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_int = 0

        def generate_inner_output():
            return (out_int)


        if asc(substring(in_char, 0, 1)) > 64 and asc(substring(in_char, 0, 1)) < 91:
            out_int = asc(substring(in_char, 0, 1)) - 64

        elif asc(substring(in_char, 0, 1)) > 48 and asc(substring(in_char, 0, 1)) < 58:
            out_int = asc(substring(in_char, 0, 1)) - 22

        elif asc(substring(in_char, 0, 1)) == 32:
            out_int = 0

        return generate_inner_output()


    def number_char(in_int:int):

        nonlocal htp_wert, htp_logv, htp_note, zahl, t_htparam_list, htparam, bediener, res_history, paramtext
        nonlocal htp_number, user_init, intval, decval, dateval, logval, charval, htl_name


        nonlocal t_htparam
        nonlocal t_htparam_list

        out_char = ""

        def generate_inner_output():
            return (out_char)


        if in_int > 0 and in_int < 27:
            out_char = chr(in_int + 64)

        elif in_int > 26 and in_int < 37:
            out_char = chr(in_int + 22)

        elif in_int == 0:
            out_char = " "

        return generate_inner_output()

    update_htparam()

    for htparam in db_session.query(Htparam).filter(
             (Htparam.paramgruppe == 40)).order_by(Htparam._recid).all():
        t_htparam = T_htparam()
        t_htparam_list.append(t_htparam)

        buffer_copy(htparam, t_htparam)

    return generate_output()