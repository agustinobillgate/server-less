from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htplogic import htplogic
from functions.htpchar import htpchar
from functions.htpint import htpint
from models import Queasy, Paramtext, Htparam, Akt_line, Bediener

def prepare_main1_4bl(user_init:str):
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
    golf_license:bool = False
    queasy = paramtext = htparam = akt_line = bediener = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal telop_sensitive, setting_sensitive, condotel_sensitive, club_sensitive, eng_sensitive, repgen_sensitive, wo_sensitive, new_contrate, ci_date, hpname_training, aktlist_flag, dynarate_flag, htl_city, curr_htl_city, p_1072, p_244, p_975, p_996, p_1002, p_997, p_988, p_992, p_1016, p_868, p_990, p_1015, p_169, p_991, p_2000, p_329, p_985, p_473, new_setup, lic_nr, p_282, golf_license, queasy, paramtext, htparam, akt_line, bediener
        nonlocal user_init
        nonlocal bqueasy


        nonlocal bqueasy
        return {"telop_sensitive": telop_sensitive, 
                "setting_sensitive": setting_sensitive, 
                "condotel_sensitive": condotel_sensitive, 
                "club_sensitive": club_sensitive, 
                "eng_sensitive": eng_sensitive, 
                "repgen_sensitive": repgen_sensitive, 
                "wo_sensitive": wo_sensitive, 
                "new_contrate": new_contrate, 
                "ci_date": ci_date, 
                "hpname_training": hpname_training, 
                "aktlist_flag": aktlist_flag, 
                "dynarate_flag": dynarate_flag, 
                "htl_city": htl_city, 
                "curr_htl_city": curr_htl_city, 
                "p_1072": p_1072, "p_244": p_244, "p_975": p_975, "p_996": p_996, "p_1002": p_1002, "p_997": p_997, "p_988": p_988, "p_992": p_992, "p_1016": p_1016, "p_868": p_868, "p_990": p_990, "p_1015": p_1015, "p_169": p_169, "p_991": p_991, "p_2000": p_2000, "p_329": p_329, "p_985": p_985, "p_473": p_473, "new_setup": new_setup, "lic_nr": lic_nr, "p_282": p_282}

    def decode_string(in_str:str):

        nonlocal telop_sensitive, setting_sensitive, condotel_sensitive, club_sensitive, eng_sensitive, repgen_sensitive, wo_sensitive, new_contrate, ci_date, hpname_training, aktlist_flag, dynarate_flag, htl_city, curr_htl_city, p_1072, p_244, p_975, p_996, p_1002, p_997, p_988, p_992, p_1016, p_868, p_990, p_1015, p_169, p_991, p_2000, p_329, p_985, p_473, new_setup, lic_nr, p_282, golf_license, queasy, paramtext, htparam, akt_line, bediener
        nonlocal user_init
        nonlocal bqueasy


        nonlocal bqueasy

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    if not paramtext or not(paramtext.txtnr == 204):
        paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 204)).first()
    curr_htl_city = paramtext.ptexte

    if not queasy or not(queasy.key == 2 and queasy.logi2):
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (Queasy.logi2)).first()
    dynarate_flag = None != queasy

    if not htparam or not(htparam.paramnr == 6001):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 6001)).first()

    if htparam and not htparam.flogical:
        telop_sensitive = False

    if not htparam or not(htparam.paramnr == 110):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    if not htparam or not(htparam.paramnr == 550):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    if not htparam or not(htparam.paramnr == 169):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 169)).first()
    hpname_training = htparam.fchar

    if not htparam or not(htparam.paramnr == 999):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 999)).first()

    if htparam.flogical:
        setting_sensitive = False

    if not htparam or not(htparam.paramnr == 981):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 981)).first()

    if not htparam.flogical:
        condotel_sensitive = False

    if not htparam or not(htparam.paramnr == 1114):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1114)).first()

    if not htparam.flogical:
        club_sensitive = False

    if not htparam or not(htparam.paramnr == 319):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 319)).first()

    if not htparam.flogical or htparam.paramgruppe != 99:
        eng_sensitive = False

    if not htparam or not(htparam.paramnr == 1072):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1072)).first()

    if not htparam.flogical or htparam.paramgruppe != 99:
        repgen_sensitive = False

    if not queasy or not(queasy.key == 28):
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 28)).first()

    if not queasy:
        wo_sensitive = True

    if not htparam or not(htparam.paramnr == 1002):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1002)).first()

    if htparam.flogical:

        if not akt_line or not(akt_line.userinit.lower()  == (user_init).lower()  and akt_line.datum >= (ci_date - 1) and akt_line.datum <= ci_date):
            akt_line = db_session.query(Akt_line).filter(
                (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= (ci_date - 1)) &  (Akt_line.datum <= ci_date)).first()
        aktlist_flag = None != akt_line

    if not paramtext or not(paramtext.txtnr >= 203):
        paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 203)).first()
    htl_city = paramtext.ptexte

    if not htparam or not(htparam.paramnr == 473):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 473)).first()

    if htparam:
        p_473 = htparam.flogical
    p_1072 = get_output(htplogic(1072))
    p_244 = get_output(htpchar(244))

    if not htparam or not(htparam.paramnr == 299):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 299)).first()

    if htparam.paramgruppe == 99 and htparam.flogical:
        p_244 = p_244 + chr(2) + "yes"
    else:
        p_244 = p_244 + chr(2) + "no"
    p_975 = get_output(htpint(975))
    # local_storage.debugging = local_storage.debugging + ",975:" + str(p_975)

    p_996 = get_output(htplogic(996))
    # local_storage.debugging = local_storage.debugging + ",996:" + str(p_996)

    p_1002 = get_output(htplogic(1002))
    # local_storage.debugging = local_storage.debugging + ",1002:" + str(p_1002)

    p_997 = get_output(htplogic(997))
    # local_storage.debugging = local_storage.debugging + ",997:" + str(p_997)

    p_988 = get_output(htplogic(988))
    # local_storage.debugging = local_storage.debugging + ",988:" + str(p_988)

    p_992 = get_output(htplogic(992))
    # local_storage.debugging = local_storage.debugging + ",992:" + str(p_992)

    p_1016 = get_output(htplogic(1016))
    # local_storage.debugging = local_storage.debugging + ",1016:" + str(p_1016)

    p_868 = get_output(htpchar(868))
    # local_storage.debugging = local_storage.debugging + ",868:" + str(p_868)

    p_990 = get_output(htplogic(990))
    # local_storage.debugging = local_storage.debugging + ",990:" + str(p_990)

    p_1015 = get_output(htplogic(1015))
    # local_storage.debugging = local_storage.debugging + "1015:" + str(p_1015)

    p_169 = get_output(htpchar(169))
    # local_storage.debugging = local_storage.debugging + ",169:" + str(p_169)

    p_991 = get_output(htplogic(991))
    # local_storage.debugging = local_storage.debugging + ",991:" + str(p_991)

    p_2000 = get_output(htplogic(2000))
    # local_storage.debugging = local_storage.debugging + ",2000:" + str(p_2000)

    p_329 = get_output(htplogic(329))
    # local_storage.debugging = local_storage.debugging + ",329:" + str(p_329)

    p_985 = get_output(htplogic(985))
    # local_storage.debugging = local_storage.debugging + ",985:" + str(p_985)


    if not htparam or not(htparam.paramnr == 282 and htparam.bezeichnung.lower()  != "not used"):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 282) &  (func.lower(Htparam.bezeichnung) != "not used")).first()

    if htparam:
        p_282 = htparam.flogical

        if not queasy or not(queasy.key == 159 and re.match(".*E1-BOOKING.*",queasy.char1, re.IGNORECASE) and queasy.number2 != 0):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 159) &  (func.lower(Queasy.char1).op("~")(("*E1-BOOKING*").lower().replace("*",".*"))) &  (Queasy.number2 != 0)).first()

        if queasy:
            p_282 = True


        else:

            if not bqueasy or not(bqueasy.key == 159):
                bqueasy = db_session.query(Bqueasy).filter(
                    (Bqueasy.key == 159)).first()

            if not bqueasy:
                p_282 = True


            else:
                p_282 = False


    else:

        if not queasy or not(queasy.key == 159 and re.match(".*E1-BOOKING.*",queasy.char1, re.IGNORECASE) and queasy.number2 != 0):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 159) &  (func.lower(Queasy.char1).op("~")(("*E1-BOOKING*").lower().replace("*",".*"))) &  (Queasy.number2 != 0)).first()

        if queasy:
            p_282 = True


        else:

            if not bqueasy or not(bqueasy.key == 159):
                bqueasy = db_session.query(Bqueasy).filter(
                    (Bqueasy.key == 159)).first()

            if not bqueasy:
                p_282 = True


            else:
                p_282 = False

    if not bediener or not(re.match((".*" + chr(2) + ".*"),bediener.username, re.IGNORECASE)):
        bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username).op("~")(("*" + chr(2) + "*").lower().replace("*",".*")))).first()

    if bediener:
        new_setup = True
    else:
        new_setup = False

    if not paramtext or not(paramtext.txtnr == 243):
        paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        lic_nr = decode_string(paramtext.ptexte)

    return generate_output()