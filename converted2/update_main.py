from functions.additional_functions import *
import decimal
import random
from models import Paramtext, Htparam

def update_main(passwd:str):
    str:str = ""
    lic_nr:str = ""
    lic_date:str = ""
    htpchar:str = ""
    found:bool = False
    paramtext = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, lic_nr, lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

        return {}

    def update_records():

        nonlocal lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

        htl_name:str = ""
        htl_city:str = ""
        lic_nr:str = ""
        str:str = ""
        htl_name = ""

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 240)).first()

        if not paramtext:
            quit

        if paramtext.ptexte == "":
            quit
        htl_name = decode71_string(paramtext.ptexte)
        str = encode70_string(htl_name)
        paramtext.ptexte = str
        htl_city = ""

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 242)).first()

        if not paramtext:
            quit

        if paramtext.ptexte == "":
            quit
        htl_city = decode71_string(paramtext.ptexte)
        str = encode70_string(htl_city)
        paramtext.ptexte = str
        lic_nr = ""

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 243)).first()

        if not paramtext:
            quit

        if paramtext.ptexte == "":
            quit
        lic_nr = decode71_string(paramtext.ptexte)
        str = encode70_string(lic_nr)
        paramtext.ptexte = str

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgr == 99)).order_by(Htparam._recid).all():
            htparam.fchar = ""
        encode70_htp()


    def encode70_htp():

        nonlocal str, lic_date, found, paramtext, htparam
        nonlocal passwd

        lic_nr:str = ""
        s:str = ""
        j:int = 0
        len_:int = 0
        htpchar:str = ""
        htpchar1:str = ""

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode70_string(paramtext.ptexte)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 99) & ((Htparam.feldtyp == 1) | (Htparam.feldtyp == 3) | (Htparam.feldtyp == 4)) & (Htparam.fchar == "")).first()
        while None != htparam:
            htpchar = ""

            if htparam.feldtyp == 1:
                htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(finteger, "9999")

            elif htparam.feldtyp == 3:
                htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(get_month(htparam.fdate) , "99") + to_string(get_day(htparam.fdate) , "99") + to_string(get_year(htparam.fdate) , "9999")

            elif htparam.feldtyp == 4:
                htpchar = to_string(lic_nr, "x(4)") + to_string(paramnr, "9999") + to_string(htparam.flogical)
            htpchar1 = encode70_string(htpchar)
            htparam.fchar = htpchar1

            curr_recid = htparam._recid
            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramgruppe == 99) & ((Htparam.feldtyp == 1) | (Htparam.feldtyp == 3) | (Htparam.feldtyp == 4)) & (Htparam.fchar == "") & (Htparam._recid > curr_recid)).first()

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 976)).first()

        if not htparam:
            quit

        paramtext = db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == 976)).first()

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 976
            paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
        paramtext.notes = htparam.fchar

    def decode70_string(in_str:str):

        nonlocal str, lic_nr, lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

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


    def decode71_string(in_str:str):

        nonlocal str, lic_nr, lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def encode70_string(in_str:str):

        nonlocal str, lic_nr, lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

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


    def encode71_string(in_str:str):

        nonlocal str, lic_nr, lic_date, htpchar, found, paramtext, htparam
        nonlocal passwd

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
        j = asc(ch) - 71
        for len_ in range(1,len(in_str)  + 1) :
            out_str = out_str + chr (asc(substring(in_str, len_ - 1, 1)) + j)

        return generate_inner_output()

    if passwd.lower()  != ("Lord is watching you.").lower() :
        quit

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if not paramtext or paramtext.ptexte == "":
        quit
    lic_nr = decode71_string(paramtext.ptexte)

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 976)).first()

    if not paramtext or paramtext.ptexte == "":
        quit

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 976)).first()

    if htparam.fdate == None:
        quit
    htpchar = decode70_string(paramtext.notes)
    htpchar = substring(htpchar, 8, len(htpchar))
    str = to_string(htparam.fdate, "99/99/9999")
    lic_date = substring(str, 0, 2) + substring(str, 3, 2) + substring(str, 6, 4)

    if lic_date.lower()  == (htpchar).lower() :

        return generate_output()
    lic_date = substring(str, 3, 2) + substring(str, 0, 2) + substring(str, 6, 4)

    if lic_date.lower()  == (htpchar).lower() :

        return generate_output()
    lic_date = substring(str, 5, 2) + substring(str, 8, 2) + substring(str, 0, 4)

    if lic_date.lower()  == (htpchar).lower() :

        return generate_output()
    lic_date = substring(str, 8, 2) + substring(str, 5, 2) + substring(str, 0, 4)

    if lic_date.lower()  == (htpchar).lower() :

        return generate_output()
    lic_date = substring(str, 0, 4) + substring(str, 5, 2) + substring(str, 8, 2)

    if lic_date.lower()  == (htpchar).lower() :

        return generate_output()
    htpchar = decode71_string(paramtext.notes)
    htpchar = substring(htpchar, 8, len(htpchar))
    str = to_string(htparam.fdate, "99/99/9999")
    lic_date = substring(str, 0, 2) + substring(str, 3, 2) + substring(str, 6, 4)

    if lic_date.lower()  == (htpchar).lower() :
        found = True

    if not found:
        lic_date = substring(str, 3, 2) + substring(str, 0, 2) + substring(str, 6, 4)

        if lic_date.lower()  == (htpchar).lower() :
            found = True

    if not found:
        quit
    update_records()

    return generate_output()