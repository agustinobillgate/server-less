#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpchar import htpchar
from functions.htpint import htpint
from sqlalchemy import func
from models import Queasy, Paramtext, Htparam, Akt_line, Bediener

def prepare_main1_5bl(user_init:string):

    prepare_cache ([Paramtext, Htparam])

    telop_sensitive = True
    setting_sensitive = True
    condotel_sensitive = True
    club_sensitive = True
    eng_sensitive = True
    repgen_sensitive = True
    wo_sensitive = True
    new_contrate = True
    ci_date = None
    hpname_training = ""
    aktlist_flag = False
    dynarate_flag = True
    htl_city = ""
    curr_htl_city = ""
    p_1072 = False
    p_244 = ""
    p_975 = 0
    p_996 = False
    p_1002 = False
    p_997 = False
    p_988 = False
    p_992 = False
    p_1016 = False
    p_868 = ""
    p_990 = False
    p_1015 = False
    p_169 = ""
    p_991 = False
    p_2000 = False
    p_329 = False
    p_985 = False
    p_473 = False
    new_setup = False
    lic_nr = ""
    p_282 = False
    p_1371 = False
    golf_license:bool = False
    queasy = paramtext = htparam = akt_line = bediener = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal telop_sensitive, setting_sensitive, condotel_sensitive, club_sensitive, eng_sensitive, repgen_sensitive, wo_sensitive, new_contrate, ci_date, hpname_training, aktlist_flag, dynarate_flag, htl_city, curr_htl_city, p_1072, p_244, p_975, p_996, p_1002, p_997, p_988, p_992, p_1016, p_868, p_990, p_1015, p_169, p_991, p_2000, p_329, p_985, p_473, new_setup, lic_nr, p_282, p_1371, golf_license, queasy, paramtext, htparam, akt_line, bediener
        nonlocal user_init
        nonlocal bqueasy


        nonlocal bqueasy

        return {"telop_sensitive": telop_sensitive, "setting_sensitive": setting_sensitive, "condotel_sensitive": condotel_sensitive, "club_sensitive": club_sensitive, "eng_sensitive": eng_sensitive, "repgen_sensitive": repgen_sensitive, "wo_sensitive": wo_sensitive, "new_contrate": new_contrate, "ci_date": ci_date, "hpname_training": hpname_training, "aktlist_flag": aktlist_flag, "dynarate_flag": dynarate_flag, "htl_city": htl_city, "curr_htl_city": curr_htl_city, "p_1072": p_1072, "p_244": p_244, "p_975": p_975, "p_996": p_996, "p_1002": p_1002, "p_997": p_997, "p_988": p_988, "p_992": p_992, "p_1016": p_1016, "p_868": p_868, "p_990": p_990, "p_1015": p_1015, "p_169": p_169, "p_991": p_991, "p_2000": p_2000, "p_329": p_329, "p_985": p_985, "p_473": p_473, "new_setup": new_setup, "lic_nr": lic_nr, "p_282": p_282, "p_1371": p_1371}

    def decode_string(in_str:string):

        nonlocal telop_sensitive, setting_sensitive, condotel_sensitive, club_sensitive, eng_sensitive, repgen_sensitive, wo_sensitive, new_contrate, ci_date, hpname_training, aktlist_flag, dynarate_flag, htl_city, curr_htl_city, p_1072, p_244, p_975, p_996, p_1002, p_997, p_988, p_992, p_1016, p_868, p_990, p_1015, p_169, p_991, p_2000, p_329, p_985, p_473, new_setup, lic_nr, p_282, p_1371, golf_license, queasy, paramtext, htparam, akt_line, bediener
        nonlocal user_init
        nonlocal bqueasy


        nonlocal bqueasy

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

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    curr_htl_city = paramtext.ptexte

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.logi2)).first()
    dynarate_flag = None != queasy

    htparam = get_cache (Htparam, {"paramnr": [(eq, 6001)]})

    if htparam and not htparam.flogical:
        telop_sensitive = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 169)]})
    hpname_training = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})

    if htparam.flogical:
        setting_sensitive = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 981)]})

    if not htparam.flogical:
        condotel_sensitive = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1114)]})

    if not htparam.flogical:
        club_sensitive = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 319)]})

    if not htparam.flogical or htparam.paramgruppe != 99:
        eng_sensitive = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1072)]})

    if not htparam.flogical or htparam.paramgruppe != 99:
        repgen_sensitive = False

    queasy = get_cache (Queasy, {"key": [(eq, 28)]})

    if not queasy:
        wo_sensitive = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

    if htparam.flogical:

        akt_line = get_cache (Akt_line, {"userinit": [(eq, user_init)],"datum": [(ge, ci_date - timedelta(days=1)),(le, ci_date)]})
        aktlist_flag = None != akt_line

    paramtext = get_cache (Paramtext, {"txtnr": [(ge, 203)]})
    htl_city = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 473)]})

    if htparam:
        p_473 = htparam.flogical
    p_1072 = get_output(htplogic(1072))
    p_244 = get_output(htpchar(244))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 299)]})

    if htparam.paramgruppe == 99 and htparam.flogical:
        p_244 = p_244 + chr_unicode(2) + "YES"
    else:
        p_244 = p_244 + chr_unicode(2) + "NO"
    p_975 = get_output(htpint(975))
    p_996 = get_output(htplogic(996))
    p_1002 = get_output(htplogic(1002))
    p_997 = get_output(htplogic(997))
    p_988 = get_output(htplogic(988))
    p_992 = get_output(htplogic(992))
    p_1016 = get_output(htplogic(1016))
    p_868 = get_output(htpchar(868))
    p_990 = get_output(htplogic(990))
    p_1015 = get_output(htplogic(1015))
    p_169 = get_output(htpchar(169))
    p_991 = get_output(htplogic(991))
    p_2000 = get_output(htplogic(2000))
    p_329 = get_output(htplogic(329))
    p_985 = get_output(htplogic(985))
    p_1371 = get_output(htplogic(1371))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1371)],"bezeichnung": [(ne, "not used")]})

    if htparam:
        p_1371 = htparam.flogical


    else:
        p_1371 = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 282)],"bezeichnung": [(ne, "not used")]})

    if htparam:
        p_282 = htparam.flogical

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 159) & (matches(Queasy.char1,"*E1-BOOKING*")) & (Queasy.number2 != 0)).first()

        if queasy:
            p_282 = True


        else:

            bqueasy = db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 159)).first()

            if not bqueasy:
                p_282 = True


            else:
                p_282 = False


    else:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 159) & (matches(Queasy.char1,"*E1-BOOKING*")) & (Queasy.number2 != 0)).first()

        if queasy:
            p_282 = True


        else:

            bqueasy = db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 159)).first()

            if not bqueasy:
                p_282 = True


            else:
                p_282 = False

    bediener = db_session.query(Bediener).filter(
             (matches(Bediener.username,"*" + chr_unicode(2) + "*"))).first()

    if bediener:
        new_setup = True


    else:
        new_setup = False

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        lic_nr = decode_string(paramtext.ptexte)

    return generate_output()