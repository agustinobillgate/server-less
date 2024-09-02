from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpdate import htpdate
from models import Bediener, Htparam, Paramtext, Zimmer, Hoteldpt

def prepare_main01bl():
    error_code = 0
    lic_nr = ""
    htl_name = ""
    htl_city = ""
    htl_adr = ""
    htl_tel = ""
    price_decimal = 0
    coa_format = ""
    vhp_licensedate = None
    vhp_newdb = False
    i_param297:int = 0
    foreign_currency:bool = False
    lstopped:bool = False
    h_name:str = ""
    h_city:str = ""
    lic_room:int = 0
    lic_pos:int = 0
    msg_str:str = ""
    p_787:str = ""
    p_223:bool = False
    loyalty_flag:bool = False
    bediener = htparam = paramtext = zimmer = hoteldpt = None

    htp = None
    Htp = Htparam

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        return {"error_code": error_code, 
                "lic_nr": lic_nr, 
                "htl_name": htl_name, 
                "htl_city": htl_city, 
                "htl_adr": htl_adr, 
                "htl_tel": htl_tel, 
                "price_decimal": price_decimal, 
                "coa_format": coa_format, 
                "vhp_licensedate": vhp_licensedate, 
                "vhp_newdb": vhp_newdb}

    def check_htp():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        lstopped = False
        flogic1:bool = False
        lic_nr:str = ""
        lic_nr1:str = ""
        str1:str = ""
        s:str = ""
        nr1:int = 0
        fint1:int = 0
        fdate1:date = None

        def generate_inner_output():
            return lstopped
        Htp = Htparam

        htparam = db_session.query(Htparam).filter((Htparam.paramnr == 976)).first()
        if not htparam or (htparam and htparam.fdate == None):
            lstopped = True
            return generate_inner_output()

        paramtext = db_session.query(Paramtext).filter((Paramtext.txtnr == 976)).first()
        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 976
            paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
            paramtext.notes = htparam.fchar
        else:
            if paramtext.notes != htparam.fchar:
                lstopped = True
                return generate_inner_output()

        paramtext = db_session.query(Paramtext).filter((Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        else:
            lstopped = True
            return generate_inner_output()

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 99) &  ((Htparam.feldtyp == 1) |  (Htparam.feldtyp == 3) |  (Htparam.feldtyp == 4))).all():
            str1 = decode_string(htparam.fchar)
            str1 = str1.lower()
            print("99:", htparam.fchar, str1)
            # local_storage.debugging = local_storage.debugging + "," + htparam.bezeichnung + ":" + str1
            if htparam.feldtyp == 1:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                fint1 = to_int(substring(str1, 8, 4))

                if fint1 != htparam.finteger:
                    htp = db_session.query(Htp).filter((Htp.paramnr == htparam.paramnr)).first()
                    htp.finteger = fint1
                    htp = db_session.query(Htp).first()

            elif htparam.feldtyp == 3:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                s = substring(str1, 8, 8)
                fdate1 = date_mdy(to_int(substring(s, 0, 2)) , to_int(substring(s, 2, 2)) , to_int(substring(s, 4, 4)))

                if fdate1 != htparam.fdate:
                    htp = db_session.query(Htp).filter((Htp.paramnr == htparam.paramnr)).first()

                    if fdate1 == None:
                        htp.fdate = None
                    else:
                        htp.fdate = fdate1

                    htp = db_session.query(Htp).first()

            elif htparam.feldtyp == 4:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                flogic1 = (substring(str1, 8, 3).lower() == ("YES").lower())

                if flogic1 != htparam.flogical and flogic1 == False:

                    htp = db_session.query(Htp).filter((Htp.paramnr == htparam.paramnr)).first()
                    htp.flogical = flogic1

                    htp = db_session.query(Htp).first()

            if (to_int(lic_nr1) != to_int(lic_nr)) or (nr1 != htparam.paramnr):
                if htparam.feldtyp == 4 and htparam.flogical :
                    lstopped = True

                elif htparam.feldtyp != 4:
                    lstopped = True

        return generate_inner_output()

    def decode_string(in_str:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

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

    def decode_strings():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        lstopped = False
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return lstopped
        htl_name = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 240)).first()

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            htl_name = decode_string(paramtext.ptexte)
        htl_city = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 242)).first()

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            htl_city = decode_string(paramtext.ptexte)
        htl_adr = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 201)).first()

        if paramtext:
            htl_adr = paramtext.ptexte
        htl_tel = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 204)).first()

        if paramtext:
            htl_tel = paramtext.ptexte
        lic_nr = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 243)).first()

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        lic_nr = "license NO: " + lic_nr

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 200)).first()

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext:
            h_name = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 203)).first()

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext:
            h_city = paramtext.ptexte

        if htl_name.lower()  != (h_name).lower()  or htl_city.lower()  != (h_city).lower() :

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 200)).first()

            if paramtext:
                paramtext.ptexte = htl_name

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 203)).first()

            if paramtext:
                paramtext.ptexte = htl_city

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 11000) &  (Paramtext.number == 1)).first()

        if paramtext and paramtext.ptexte != "":
            h_name = h_name + chr(2) + paramtext.ptexte


        return generate_inner_output()

    def decode_serial():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        do_it:bool = True
        str11:str = ""
        str12:str = ""
        str13:str = ""
        str14:str = ""
        str21:str = ""
        str22:str = ""
        str23:str = ""
        str24:str = ""
        license_dec:str = ""
        datum_dec:str = ""
        hotel_dec:str = ""
        next_expired:str = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 200)).first()
        do_it = (len(paramtext.passwort) == 19)

        if do_it:
            str11 = entry(0, paramtext.passwort, " ")
            str12 = entry(1, paramtext.passwort, " ")
            str13 = entry(2, paramtext.passwort, " ")
            str14 = entry(3, paramtext.passwort, " ")

        if do_it:

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == 203)).first()
            do_it = (len(paramtext.passwort) == 19)

            if do_it:
                str21 = entry(0, paramtext.passwort, " ")
                str22 = entry(1, paramtext.passwort, " ")
                str23 = entry(2, paramtext.passwort, " ")
                str24 = entry(3, paramtext.passwort, " ")

        if do_it:
            license_dec, datum_dec, hotel_dec = decode_serial1(str11, str12, str13, str14, str21, str22, str23, str24)

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 976)).first()
        next_expired = to_string(get_month(htparam.fdate) , "99") +\
                to_string(get_day(htparam.fdate) , "99") +\
                to_string(get_year(htparam.fdate))

        if (license_dec != substring(lic_nr, len(lic_nr) - 3 - 1)) or (datum_dec != next_expired):
            error_code = 1006

            return

    def decode_serial1(datum_1_enc:str, license_enc:str, datum_2_enc:str, schluessel:str, nama1:str, nama2:str, nama3:str, nama4:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        license_dec = ""
        datum_dec = ""
        hotel_dec = ""
        datum_1_enc_2:str = ""
        license_enc_2:str = ""
        datum_2_enc_2:str = ""
        schluessel_2:str = ""

        def generate_inner_output():
            return license_dec, datum_dec, hotel_dec
        license_dec, datum_dec = decode_all(datum_1_enc, license_enc, datum_2_enc, schluessel)
        hotel_dec = decode_hotel(nama1, nama2, nama3, nama4, datum_2_enc, schluessel, datum_1_enc, license_enc)


        return generate_inner_output()

    def decode_hotel(name1:str, name2:str, name3:str, name4:str, datum2:str, schluessel:str, datum1:str, license:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        hotel = ""
        temp1:str = ""
        temp2:str = ""
        temp3:str = ""
        temp4:str = ""

        def generate_inner_output():
            return hotel
        temp1 = decode_name(name1, datum2)
        temp2 = decode_name(name2, schluessel)
        temp3 = decode_name(name3, datum1)
        temp4 = decode_name(name4, license)
        hotel = temp1 + temp2 + temp3 + temp4
        return generate_inner_output()

    def decode_name(hotel_enc:str, in_string:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        out_string = ""
        i:int = 0
        string_int:int = 0
        hotel_int:int = 0
        name_dec:str = ""
        len_:int = 0

        def generate_inner_output():
            return out_string
        len_ = len(in_string)
        for i in range(1,len + 1) :
            hotel_int = char_number(substring (hotel_enc, i, 1))
            string_int = char_number(substring(in_string, i - 1, 1))
            name_dec = number_char(hotel_int - (2 * string_int % 10) - 1)
            out_string = out_string + name_dec

        return generate_inner_output()

    def decode_all(license_enc:str, datum_teil1:str, datum_teil2:str, schluessel:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        license3 = ""
        datum3 = ""
        datum_combined:str = ""
        license2:str = ""
        zahl2:str = ""
        zahl3:str = ""
        license_next:str = ""
        datum_teil1_next:str = ""
        datum_teil2_next:str = ""
        summe:int = 0
        i:int = 0

        def generate_inner_output():
            return license3, datum3
        datum_teil1_next = decode_next(datum_teil1, license_enc)
        license_next = decode_next(license_enc, datum_teil2)
        datum_teil2_next = decode_next(datum_teil2, schluessel)
        zahl2 = decode_serial_str(schluessel, "", 0)
        zahl3 = decode_serial_str(zahl2, "", 0)
        license3 = decode_serial_str(license_next, zahl3, 1)
        datum_combined = combineword(datum_teil1_next, datum_teil2_next)
        datum3 = decode_serial_str(datum_combined, zahl3, 2)


        return generate_inner_output()

    def decode_serial_str(in_str:str, schluessel:str, keychar:int):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0
        len1:int = 0

        def generate_inner_output():
            return out_str
        s = in_str

        if keychar == 0:
            j = ord(substring(s, 0, 1)) - 70
            len_ = len(in_str) - 1
            s = substring(in_str, 1, len_)
        else:
            j = ord(substring(schluessel, keychar - 1, 1)) - 49
            len_ = len(in_str)
            s = substring(in_str, 0, len_)

        for len_ in range(1,len(s)  + 1) :
            len1 = 13 * len_ % 5 + 6
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j + len1)

        return generate_inner_output()

    def cutword(word:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        teil1 = ""
        teil2 = ""
        len_:int = 0
        halb:int = 0

        def generate_inner_output():
            return teil1, teil2
        len_ = len(word)
        halb = len_ / 2
        teil1 = substring(word, 0, halb)
        teil2 = substring(word, halb + 1 - 1, halb)

        return generate_inner_output()

    def combineword(teil1:str, teil2:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        word = ""

        def generate_inner_output():
            return word
        word = teil1 + teil2
        return generate_inner_output()

    def decode_next(in_str:str, schluessel:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp
        out_str = ""
        schluessel1:int = 0
        len_:int = 0
        reverse:int = 0
        len1:int = 0

        def generate_inner_output():
            return out_str
        for len_ in range(1,len(in_str)  + 1) :
            reverse = len(in_str) - len_ + 1
            schluessel1 = ord(substring(schluessel, reverse - 1, 1)) % 7 - 1
            out_str = out_str + chr (ord(substring(in_str, len_ - 1, 1)) + schluessel1 - len_ - 5)

        return generate_inner_output()

    def serial_check(wort1:str, wort2:str, wort3:str, wort4:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        accept = False
        i:int = 0
        j:int = 0
        alpha:int = 0
        wort:[str] = ["", "", "", "", ""]

        def generate_inner_output():
            return accept
        wort[0] = wort1
        wort[1] = wort2
        wort[2] = wort3
        wort[3] = wort4

        for i in range(1,4 + 1) :
            for j in range(1,4 + 1) :
                alpha = ord(substring(wort[i - 1], j - 1, 1))

                if alpha < 65 or alpha > 90:
                    accept = False


        return generate_inner_output()

    def modulo_check(wort:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        accept_key = False
        i:int = 0
        summe:int = 0

        def generate_inner_output():
            return accept_key
        for i in range(1,len(wort)  + 1) :
            summe = summe + (ord(substring(wort, i - 1, 1)) - 64) + i

        if (summe % 13) == 0:
            accept_key = True

        return generate_inner_output()

    def char_number(in_char:str):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp
        out_int = 0

        def generate_inner_output():
            return out_int

        if ord(substring(in_char, 0, 1)) > 64 and ord(substring(in_char, 0, 1)) < 91:
            out_int = ord(substring(in_char, 0, 1)) - 64

        elif ord(substring(in_char, 0, 1)) > 48 and ord(substring(in_char, 0, 1)) < 58:
            out_int = ord(substring(in_char, 0, 1)) - 22

        elif ord(substring(in_char, 0, 1)) == 32:
            out_int = 0

        return generate_inner_output()

    def number_char(in_int:int):
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        out_char = ""

        def generate_inner_output():
            return out_char

        if in_int > 0 and in_int < 27:
            out_char = chr(in_int + 64)

        elif in_int > 26 and in_int < 37:
            out_char = chr(in_int + 22)

        elif in_int == 0:
            out_char = " "

        return generate_inner_output()

    def check_room_pos_license():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt
        nonlocal htp

        lstopped = False
        lic_room:int = 0
        lic_pos:int = 0
        max_room:int = 0
        max_pos:int = 0

        def generate_inner_output():
            return lstopped
        
        lic_room = get_output(htpint(975))
        lic_pos = get_output(htpint(989))

        if lic_room == 0:
            lstopped = True
            error_code = 1003
            return generate_inner_output()

        for zimmer in db_session.query(Zimmer).all():
            max_room = max_room + 1

        if max_room > lic_room:
            error_code = 1004
            lstopped = True
            return generate_inner_output()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num > 0)).all():
            max_pos = max_pos + 1

        if max_pos > lic_pos:
            error_code = 1005
            lstopped = True
            return generate_inner_output()

        return generate_inner_output()


    bediener = db_session.query(Bediener).filter(
            (substring(Bediener.username, len(Bediener.username) - 1, 1) == chr(2))).first()
    vhp_newdb = None != bediener
    lstopped = check_htp()

    if lstopped:
        error_code = 1001
        return generate_output()
    
    lstopped = decode_strings()

    if lstopped:
        error_code = 1002
        return generate_output()

    # PROVERSION = "111"
    # if substring(PROVERSION, 0, 1) == "1":
    #   pass
    decode_serial()

    lstopped = check_room_pos_license()

    if lstopped:
        return generate_output()
    
    coa_format = get_output(htpchar(977))
    foreign_currency = get_output(htplogic(240))
    i_param297 = get_output(htpint(297))
    price_decimal = get_output(htpint(491))
    vhp_licensedate = get_output(htpdate(976))
    lic_room = get_output(htpint(975))
    lic_pos = get_output(htpint(989))

    return generate_output()