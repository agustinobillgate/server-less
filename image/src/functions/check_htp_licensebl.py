from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Paramtext

def check_htp_licensebl():
    lstopped = False
    htparam = paramtext = None

    htp = None

    Htp = Htparam

    db_session = local_storage.db_session
    # print("DBSession3:", db_session)


    def generate_output():
        nonlocal lstopped, htparam, paramtext
        nonlocal htp


        nonlocal htp
        return {"lstopped": lstopped}

    def check_htp_license():

        nonlocal lstopped, htparam, paramtext
        nonlocal htp

        nonlocal htp

        lstopped = False
        lic_nr:str = ""
        lic_nr1:str = ""
        nr1:int = 0
        flogic1:bool = False
        fint1:int = 0
        fdate1:date = None
        str:str = ""
        s:str = ""

        def generate_inner_output():
            return lstopped
        Htp = Htparam

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 976)).first()
        # print("Masuk HTP1")
        if not htparam or (htparam and htparam.fdate == None):
            lstopped = True

            return generate_inner_output()

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 976)).first()
        # print("Masuk HTP2")
        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 976
            paramtext.ptexte = to_string(htparam.fdate, "99/99/9999")
            paramtext.notes = htparam.fchar
            # print("Masuk HTP21")
        else:
            # print("Masuk HTP31")
            if paramtext.notes != htparam.fchar:
                lstopped = True

                return generate_inner_output()
        # print("Masuk HTP91")
        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 243)).first()
        
        if paramtext and paramtext.ptexte != "":
            # print("Masuk HTP91a: txtnr: ")
            lic_nr = decode_string(paramtext.ptexte)
            # print("LicNr:", lic_nr)
        else:
            # print("Masuk HTP91b: txtnr: ")
            lstopped = True

            return generate_inner_output()
        # print("Masuk HTP201")
        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 99) &  ((Htparam.feldtyp == 1) |  (Htparam.feldtyp == 3) |  (Htparam.feldtyp == 4))).all():
            str = decode_string(htparam.fchar)
            str = str.lower()
            # local_storage.debugging = local_storage.debugging + "," + htparam.bezeichnung + ":" + str

            if htparam.feldtyp == 1:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                fint1 = to_int(substring(str, 8, 4))

                if fint1 != htparam.finteger:

                    htp = db_session.query(Htp).filter(
                            (Htp.paramnr == htparam.paramnr)).first()
                    htp.finteger = fint1

                    htp = db_session.query(Htp).first()

            elif htparam.feldtyp == 3:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                s = substring(str, 8, 8)
                fdate1 = date_mdy(to_int(substring(s, 0, 2)) , to_int(substring(s, 2, 2)) , to_int(substring(s, 4, 4)))

                if fdate1 != htparam.fdate:

                    htp = db_session.query(Htp).filter(
                            (Htp.paramnr == htparam.paramnr)).first()

                    if fdate1 == None:
                        htp.fdate = None
                    else:
                        htp.fdate = fdate1

                    htp = db_session.query(Htp).first()

            elif htparam.feldtyp == 4:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                flogic1 = (substring(str, 8, 3).lower() == ("YES").lower())

                if flogic1 != htparam.flogical and flogic1 == False:

                    htp = db_session.query(Htp).filter(
                            (Htp.paramnr == htparam.paramnr)).first()
                    htp.flogical = flogic1
                    local_storage.debugging = local_storage.debugging + "," + htparam.bezeichnung + ":"

                    htp = db_session.query(Htp).first()

            if (to_int(lic_nr1) != to_int(lic_nr)) or (nr1 != htparam.paramnr):

                if htparam.feldtyp == 4 and htparam.flogical :
                    lstopped = True

                elif htparam.feldtyp != 4:
                    lstopped = True


        return generate_inner_output()

    def decode_string(in_str:str):

        nonlocal lstopped, htparam, paramtext
        nonlocal htp


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

    lstopped = check_htp_license()

    return generate_output()