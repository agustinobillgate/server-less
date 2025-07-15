#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpdate import htpdate
from models import Bediener, Htparam, Paramtext, Zimmer, Hoteldpt

def prepare_main01bl():

    prepare_cache ([Htparam, Paramtext])

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
    h_name:string = ""
    h_city:string = ""
    lic_room:int = 0
    lic_pos:int = 0
    msg_str:string = ""
    p_787:string = ""
    p_223:bool = False
    loyalty_flag:bool = False
    bediener = htparam = paramtext = zimmer = hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        return {"error_code": error_code, "lic_nr": lic_nr, "htl_name": htl_name, "htl_city": htl_city, "htl_adr": htl_adr, "htl_tel": htl_tel, "price_decimal": price_decimal, "coa_format": coa_format, "vhp_licensedate": vhp_licensedate, "vhp_newdb": vhp_newdb}

    def check_htp():

        nonlocal error_code, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        lstopped = False
        flogic1:bool = False
        lic_nr:string = ""
        lic_nr1:string = ""
        str1:string = ""
        s:string = ""
        nr1:int = 0
        fint1:int = 0
        fdate1:date = None
        htp = None

        def generate_inner_output():
            return (lstopped)

        Htp =  create_buffer("Htp",Htparam)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 976)]})

        if not htparam or (htparam and htparam.fdate == None):
            lstopped = True

            return generate_inner_output()

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 976)]})

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 976
            paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
            paramtext.notes = htparam.fchar


            pass
        else:

            if paramtext.notes != htparam.fchar:
                lstopped = True

                return generate_inner_output()

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        else:
            lstopped = True

            return generate_inner_output()

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 99) & ((Htparam.feldtyp == 1) | (Htparam.feldtyp == 3) | (Htparam.feldtyp == 4))).order_by(Htparam._recid).all():
            str1 = decode_string(htparam.fchar)

            if htparam.feldtyp == 1:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                fint1 = to_int(substring(str1, 8, 4))

                if fint1 != htparam.finteger:

                    htp = get_cache (Htparam, {"paramnr": [(eq, htparam.paramnr)]})
                    htp.finteger = fint1
                    pass

            elif htparam.feldtyp == 3:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                s = substring(str1, 8, 8)
                fdate1 = date_mdy(to_int(substring(s, 0, 2)) , to_int(substring(s, 2, 2)) , to_int(substring(s, 4, 4)))

                if fdate1 != htparam.fdate:

                    htp = get_cache (Htparam, {"paramnr": [(eq, htparam.paramnr)]})

                    if fdate1 == None:
                        htp.fdate = None
                    else:
                        htp.fdate = fdate1
                    pass

            elif htparam.feldtyp == 4:
                lic_nr1 = substring(str1, 0, 4)
                nr1 = to_int(substring(str1, 4, 4))
                flogic1 = (substring(str1, 8, 3) == "YES")

                if flogic1 != htparam.flogical and flogic1 == False:

                    htp = get_cache (Htparam, {"paramnr": [(eq, htparam.paramnr)]})
                    htp.flogical = flogic1
                    pass

            if (to_int(lic_nr1) != to_int(lic_nr)) or (nr1 != htparam.paramnr):

                if htparam.feldtyp == 4 and htparam.flogical :
                    lstopped = True

                elif htparam.feldtyp != 4:
                    lstopped = True

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

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


    def decode_strings():

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        lstopped = False
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (lstopped)

        htl_name = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            htl_name = decode_string(paramtext.ptexte)
        htl_city = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 242)]})

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            htl_city = decode_string(paramtext.ptexte)
        htl_adr = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})

        if paramtext:
            htl_adr = paramtext.ptexte
        htl_tel = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})

        if paramtext:
            htl_tel = paramtext.ptexte
        lic_nr = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        lic_nr = "license NO: " + lic_nr

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext:
            h_name = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})

        if not paramtext:
            lstopped = True

        if paramtext.ptexte == "":
            lstopped = True

        if paramtext:
            h_city = paramtext.ptexte

        if htl_name.lower()  != (h_name).lower()  or htl_city.lower()  != (h_city).lower() :

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

            if paramtext:
                paramtext.ptexte = htl_name

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})

            if paramtext:
                paramtext.ptexte = htl_city

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 11000)],"number": [(eq, 1)]})

        if paramtext and paramtext.ptexte != "":
            h_name = h_name + chr_unicode(2) + paramtext.ptexte

        return generate_inner_output()


    def decode_serial():

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        do_it:bool = True
        str11:string = ""
        str12:string = ""
        str13:string = ""
        str14:string = ""
        str21:string = ""
        str22:string = ""
        str23:string = ""
        str24:string = ""
        license_dec:string = ""
        datum_dec:string = ""
        hotel_dec:string = ""
        next_expired:string = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
        do_it = (length(paramtext.passwort) == 19)

        if do_it:
            str11 = entry(0, paramtext.passwort, " ")
            str12 = entry(1, paramtext.passwort, " ")
            str13 = entry(2, paramtext.passwort, " ")
            str14 = entry(3, paramtext.passwort, " ")

        if do_it:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
            do_it = (length(paramtext.passwort) == 19)

            if do_it:
                str21 = entry(0, paramtext.passwort, " ")
                str22 = entry(1, paramtext.passwort, " ")
                str23 = entry(2, paramtext.passwort, " ")
                str24 = entry(3, paramtext.passwort, " ")

        if do_it:
            license_dec, datum_dec, hotel_dec = decode_serial1(str11, str12, str13, str14, str21, str22, str23, str24)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 976)]})
        next_expired = to_string(get_month(htparam.fdate) , "99") +\
                to_string(get_day(htparam.fdate) , "99") +\
                to_string(get_year(htparam.fdate))

        if (license_dec != substring(lic_nr, length(lic_nr) - 3 - 1)) or (datum_dec.lower()  != (next_expired).lower()):
            error_code = 1006

            return


    def decode_serial1(datum_1_enc:string, license_enc:string, datum_2_enc:string, schluessel:string, nama1:string, nama2:string, nama3:string, nama4:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        license_dec = ""
        datum_dec = ""
        hotel_dec = ""
        datum_1_enc_2:string = ""
        license_enc_2:string = ""
        datum_2_enc_2:string = ""
        schluessel_2:string = ""

        def generate_inner_output():
            return (license_dec, datum_dec, hotel_dec)

        license_dec, datum_dec = decode_all(datum_1_enc, license_enc, datum_2_enc, schluessel)
        hotel_dec = decode_hotel(nama1, nama2, nama3, nama4, datum_2_enc, schluessel, datum_1_enc, license_enc)

        return generate_inner_output()


    def decode_hotel(name1:string, name2:string, name3:string, name4:string, datum2:string, schluessel:string, datum1:string, license:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        hotel = ""
        temp1:string = ""
        temp2:string = ""
        temp3:string = ""
        temp4:string = ""

        def generate_inner_output():
            return (hotel)

        temp1 = decode_name(name1, datum2)
        temp2 = decode_name(name2, schluessel)
        temp3 = decode_name(name3, datum1)
        temp4 = decode_name(name4, license)
        hotel = temp1 + temp2 + temp3 + temp4

        return generate_inner_output()


    def decode_name(hotel_enc:string, in_string:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        out_string = ""
        i:int = 0
        string_int:int = 0
        hotel_int:int = 0
        name_dec:string = ""
        len_:int = 0

        def generate_inner_output():
            return (out_string)

        len_ = length(in_string)
        for i in range(1,len + 1) :
            hotel_int = char_number(substring(hotel_enc, i - 1, 1))
            string_int = char_number(substring(in_string, i - 1, 1))
            name_dec = number_char(hotel_int - (2 * string_int % 10) - 1)
            out_string = out_string + name_dec

        return generate_inner_output()


    def decode_all(license_enc:string, datum_teil1:string, datum_teil2:string, schluessel:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        license3 = ""
        datum3 = ""
        datum_combined:string = ""
        license2:string = ""
        zahl2:string = ""
        zahl3:string = ""
        license_next:string = ""
        datum_teil1_next:string = ""
        datum_teil2_next:string = ""
        summe:int = 0
        i:int = 0

        def generate_inner_output():
            return (license3, datum3)

        datum_teil1_next = decode_next(datum_teil1, license_enc)
        license_next = decode_next(license_enc, datum_teil2)
        datum_teil2_next = decode_next(datum_teil2, schluessel)
        zahl2 = decode_serial_str(schluessel, "", 0)
        zahl3 = decode_serial_str(zahl2, "", 0)
        license3 = decode_serial_str(license_next, zahl3, 1)
        datum_combined = combineword(datum_teil1_next, datum_teil2_next)
        datum3 = decode_serial_str(datum_combined, zahl3, 2)

        return generate_inner_output()


    def decode_serial_str(in_str:string, schluessel:string, keychar:int):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0
        len1:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str

        if keychar == 0:
            j = asc(substring(s, 0, 1)) - 70
            len_ = length(in_str) - 1
            s = substring(in_str, 1, len_)


        else:
            j = asc(substring(schluessel, keychar - 1, 1)) - 49
            len_ = length(in_str)
            s = substring(in_str, 0, len_)


        for len_ in range(1,length(s)  + 1) :
            len1 = 13 * len_ % 5 + 6
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j + len1)

        return generate_inner_output()


    def cutword(word:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        teil1 = ""
        teil2 = ""
        len_:int = 0
        halb:int = 0

        def generate_inner_output():
            return (teil1, teil2)

        len_ = length(word)
        halb = len_ / 2
        teil1 = substring(word, 0, halb)
        teil2 = substring(word, halb + 1 - 1, halb)

        return generate_inner_output()


    def combineword(teil1:string, teil2:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        word = ""

        def generate_inner_output():
            return (word)

        word = teil1 + teil2

        return generate_inner_output()


    def decode_next(in_str:string, schluessel:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        out_str = ""
        schluessel1:int = 0
        len_:int = 0
        reverse:int = 0
        len1:int = 0

        def generate_inner_output():
            return (out_str)

        for len_ in range(1,length(in_str)  + 1) :
            reverse = length(in_str) - len_ + 1
            schluessel1 = asc(substring(schluessel, reverse - 1, 1)) % 7 - 1
            out_str = out_str + chr_unicode(asc(substring(in_str, len_ - 1, 1)) + schluessel1 - len_ - 5)

        return generate_inner_output()


    def serial_check(wort1:string, wort2:string, wort3:string, wort4:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        accept = True
        i:int = 0
        j:int = 0
        alpha:int = 0
        wort:List[string] = create_empty_list(4,"")

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


    def modulo_check(wort:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        accept_key = False
        i:int = 0
        summe:int = 0

        def generate_inner_output():
            return (accept_key)

        for i in range(1,length(wort)  + 1) :
            summe = summe + (asc(substring(wort, i - 1, 1)) - 64) + i

        if (summe % 13) == 0:
            accept_key = True

        return generate_inner_output()


    def char_number(in_char:string):

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

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

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, lic_room, lic_pos, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        out_char = ""

        def generate_inner_output():
            return (out_char)


        if in_int > 0 and in_int < 27:
            out_char = chr_unicode(in_int + 64)

        elif in_int > 26 and in_int < 37:
            out_char = chr_unicode(in_int + 22)

        elif in_int == 0:
            out_char = " "

        return generate_inner_output()


    def check_room_pos_license():

        nonlocal error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, i_param297, foreign_currency, lstopped, h_name, h_city, msg_str, p_787, p_223, loyalty_flag, bediener, htparam, paramtext, zimmer, hoteldpt

        lstopped = False
        lic_room:int = 0
        lic_pos:int = 0
        max_room:int = 0
        max_pos:int = 0

        def generate_inner_output():
            return (lstopped)

        lic_room = get_output(htpint(975))
        lic_pos = get_output(htpint(989))

        if lic_room == 0:
            lstopped = True
            error_code = 1003

            return generate_inner_output()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            max_room = max_room + 1

        if max_room > lic_room:
            error_code = 1004
            lstopped = True

            return generate_inner_output()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
            max_pos = max_pos + 1

        if max_pos > lic_pos:
            error_code = 1005
            lstopped = True

            return generate_inner_output()

        return generate_inner_output()

    bediener = db_session.query(Bediener).filter(
             (substring(Bediener.username, length(Bediener.username) - 1, 1) == chr_unicode(2))).first()
    vhp_newdb = None != bediener
    lstopped = check_htp()

    if lstopped:
        error_code = 1001

        return generate_output()
    lstopped = decode_strings()

    if lstopped:
        error_code = 1002

        return generate_output()

    if substring(proversion(), 0, 1) == ("1").lower() :
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