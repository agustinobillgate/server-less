from functions.additional_functions import *
import decimal
from datetime import date
from functions.e1_serial_decodebl import e1_serial_decodebl
from models import Paramtext, Htparam

def e1_serialbl(inp_serial:str):
    i_case = 0
    i_number = 0
    d_datum = None
    error_flag = True
    license_nr:int = 0
    lic_nr:str = ""
    htl_name:str = ""
    max_ext_date:date = None
    zahl:str = ""
    valid_flag:bool = False
    paramtext = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial


        return {"i_case": i_case, "i_number": i_number, "d_datum": d_datum, "error_flag": error_flag}

    def activate_license(lic_string:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        htpchar:str = ""
        htpchar1:str = ""
        vhp_lite:bool = False
        maxroom:int = 0
        curr_i:int = 0
        ct:str = ""
        for curr_i in range(1,num_entries(lic_string, ",")  + 1) :
            ct = trim(entry(curr_i - 1, lic_string, ","))

            if ct != "":

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == to_int(ct))).first()
                htparam.flogical = True
                htpchar = to_string(lic_nr) + to_string(paramnr, "9999") +\
                        to_string(htparam.flogical)


                htpchar1 = encode_string(htpchar)
                htparam.fchar = htpchar1


    def extent_vhp_license_date():

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        if get_month(get_current_date()) == 2 and get_day(get_current_date()) >= 28:
            max_ext_date = date_mdy(2, 28, get_year(get_current_date()) + timedelta(days=3))


        else:
            max_ext_date = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()) + timedelta(days=3))

        if d_datum < get_current_date():
            error_flag = True

            return
        extent_lic_date()
        htl_name = ""

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 240)).first()

        if paramtext and paramtext.ptexte != "":
            htl_name = decode_string(paramtext.ptexte)
            htl_name = htl_name.upper()
            encode_serial(lic_nr, d_datum, htl_name)


    def vhp_rooms_pos(i_param:int):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        htpchar:str = ""
        htpchar1:str = ""

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == i_param)).first()
        htparam.finteger = i_number
        htpchar = to_string(lic_nr) + to_string(paramnr, "9999") + to_string(htparam.finteger)
        htpchar1 = encode_string(htpchar)
        htparam.fchar = htpchar1


    def decode_string(in_str:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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
            out_str = out_str + chr(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def encode_string(in_str:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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
            out_str = out_str + chr(asc(substring(in_str, len_ - 1, 1)) + j)

        return generate_inner_output()


    def extent_lic_date():

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        htpchar:str = ""
        htpchar1:str = ""
        vhp_lite:bool = False
        maxroom:int = 0

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 976)).first()
        htparam.fdate = d_datum
        htpchar = to_string(lic_nr) + to_string(paramnr, "9999") + to_string(get_month(htparam.fdate) , "99") + to_string(get_day(htparam.fdate) , "99") + to_string(get_year(htparam.fdate) , "9999")
        htpchar1 = encode_string(htpchar)
        htparam.fchar = htpchar1

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 976)).first()

        if paramtext:
            paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
            paramtext.notes = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1072)).first()
        htparam.finteger = 0

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 996)).first()

        if htparam.fchar == "":

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 1015)).first()
            vhp_lite = htparam.flogical

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 975)).first()
            maxroom = htparam.finteger

            if not vhp_lite and maxroom != 1:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 996)).first()
                htparam.flogical = True
                htpchar = to_string(lic_nr) + to_string(htparam.paramnr, "9999") + to_string(htparam.flogical)
                htpchar1 = encode_string(htpchar)
                htparam.fchar = htpchar1


    def encode_serial(license:str, curr_date:date, hotel:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def encode_hotel(datum2:str, schluessel:str, datum1:str, license:str, hotel:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def encode_name(in_string:str, hotel:str, pos:int):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def encode_all(license:str, datum:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def encode_serial_str(in_str:str, prefix:bool):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def combineword(teil1:str, teil2:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        word = ""

        def generate_inner_output():
            return (word)

        word = teil1 + teil2

        return generate_inner_output()


    def encode_next(in_str:str, schluessel:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def modulo_check(wort:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

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


    def char_number(in_char:str):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        out_int = 0

        def generate_inner_output():
            return (out_int)


        if asc(substring(in_char, 0, 1)) > 96 and asc(substring(in_char, 0, 1)) < 123:
            out_int = asc(substring(in_char, 0, 1)) - 60

        elif asc(substring(in_char, 0, 1)) > 64 and asc(substring(in_char, 0, 1)) < 91:
            out_int = asc(substring(in_char, 0, 1)) - 64

        elif asc(substring(in_char, 0, 1)) > 48 and asc(substring(in_char, 0, 1)) < 58:
            out_int = asc(substring(in_char, 0, 1)) - 21

        elif asc(substring(in_char, 0, 1)) == 32:
            out_int = 0

        return generate_inner_output()


    def number_char(in_int:int):

        nonlocal i_case, i_number, d_datum, error_flag, license_nr, lic_nr, htl_name, max_ext_date, zahl, valid_flag, paramtext, htparam
        nonlocal inp_serial

        out_char = ""

        def generate_inner_output():
            return (out_char)


        if in_int > 0 and in_int < 27:
            out_char = chr(in_int + 64)

        elif in_int > 26 and in_int < 37:
            out_char = chr(in_int + 21)

        elif in_int > 36 and in_int < 63:
            out_char = chr(in_int + 60)

        elif in_int == 0:
            out_char = " "

        return generate_inner_output()

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if not paramtext:

        return generate_output()

    if paramtext.ptexte == "":

        return generate_output()
    license_nr, d_datum, i_case, i_number, valid_flag = get_output(e1_serial_decodebl(inp_serial))
    error_flag = not valid_flag

    if error_flag:

        return generate_output()
    lic_nr = decode_string(paramtext.ptexte)

    if get_month(get_current_date()) == 2 and get_day(get_current_date()) >= 28:
        max_ext_date = date_mdy(2, 28, get_year(get_current_date()) + timedelta(days=3))


    else:
        max_ext_date = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()) + timedelta(days=3))

    if to_int(lic_nr) != license_nr:
        error_flag = True

    elif (i_case == 2 or i_case == 3) and i_number == 0:
        error_flag = True

    elif (i_case == 1 or i_case > 3) and i_number != 0:
        error_flag = True

    elif i_number < 0:
        error_flag = True

    elif d_datum == None:
        error_flag = True

    elif d_datum > max_ext_date:
        error_flag = True

    elif i_case != 1 and d_datum > (get_current_date() + 1):
        error_flag = True

    if error_flag:

        return generate_output()

    if i_case == 1:
        extent_vhp_license_date()
    elif i_case == 2:
        vhp_rooms_pos(975)
    elif i_case == 3:
        vhp_rooms_pos(989)
    elif i_case == 4:
        activate_license("1002")
    elif i_case == 5:
        activate_license("985")
    elif i_case == 6:
        activate_license("1114")
    elif i_case == 7:
        activate_license("988")
    elif i_case == 8:
        activate_license("992,1016")
    elif i_case == 9:
        activate_license("991")
    elif i_case == 10:
        activate_license("2000")
    elif i_case == 11:
        activate_license("319")
    elif i_case == 12:
        activate_license("329")
    elif i_case == 13:
        activate_license("997")
    elif i_case == 14:
        activate_license("1016")
    elif i_case == 15:
        activate_license("1112")
    elif i_case == 16:
        activate_license("223")
    elif i_case == 17:
        activate_license("1072")
    elif i_case == 18:
        activate_license("1102")
    elif i_case == 19:
        activate_license("981")
    elif i_case == 20:
        activate_license("996")
    elif i_case == 21:
        activate_license("990,254")
    elif i_case == 22:
        activate_license("982")
    elif i_case == 23:
        activate_license("1111")
    elif i_case == 24:
        activate_license("306")
    elif i_case == 25:
        activate_license("307,308,309,310,311,348")
    elif i_case == 26:
        activate_license("358")
    elif i_case == 27:
        activate_license("359")
    elif i_case == 28:
        activate_license("472")
    elif i_case == 29:
        activate_license("299")
    elif i_case == 30:
        activate_license("1074")
    elif i_case == 31:
        activate_license("1075")
    elif i_case == 32:
        activate_license("1073")
    elif i_case == 33:
        activate_license("1055")
    elif i_case == 34:
        activate_license("1357")
    elif i_case == 35:
        activate_license("1358")
    elif i_case == 36:
        activate_license("1359")
    elif i_case == 37:
        activate_license("1022")
    elif i_case == 38:
        activate_license("1023")
    elif i_case == 39:
        activate_license("282")
    elif i_case == 40:
        activate_license("280")
    else:
        pass

    return generate_output()