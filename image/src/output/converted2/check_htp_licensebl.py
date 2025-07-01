#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext

def check_htp_licensebl():

    prepare_cache ([Htparam, Paramtext])

    lstopped = False
    htparam = paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lstopped, htparam, paramtext

        return {"lstopped": lstopped}

    def check_htp_license():

        nonlocal lstopped, htparam, paramtext

        lstopped = False
        lic_nr:string = ""
        lic_nr1:string = ""
        nr1:int = 0
        flogic1:bool = False
        fint1:int = 0
        fdate1:date = None
        str:string = ""
        s:string = ""
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
            str = decode_string(htparam.fchar)

            if htparam.feldtyp == 1:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                fint1 = to_int(substring(str, 8, 4))

                if fint1 != htparam.finteger:

                    htp = get_cache (Htparam, {"paramnr": [(eq, htparam.paramnr)]})
                    htp.finteger = fint1
                    pass

            elif htparam.feldtyp == 3:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                s = substring(str, 8, 8)
                fdate1 = date_mdy(to_int(substring(s, 0, 2)) , to_int(substring(s, 2, 2)) , to_int(substring(s, 4, 4)))

                if fdate1 != htparam.fdate:

                    htp = get_cache (Htparam, {"paramnr": [(eq, htparam.paramnr)]})

                    if fdate1 == None:
                        htp.fdate = None
                    else:
                        htp.fdate = fdate1
                    pass

            elif htparam.feldtyp == 4:
                lic_nr1 = substring(str, 0, 4)
                nr1 = to_int(substring(str, 4, 4))
                flogic1 = (substring(str, 8, 3) == "YES")

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

        nonlocal lstopped, htparam, paramtext

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


    lstopped = check_htp_license()

    return generate_output()