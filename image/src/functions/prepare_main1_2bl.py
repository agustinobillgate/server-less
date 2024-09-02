from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htplogic import htplogic
from functions.htpchar import htpchar
from functions.htpint import htpint
from models import Paramtext, Queasy, Htparam, Akt_line, Bediener

def prepare_main1_2bl(user_init:str):
    telop_sensitive = False
    setting_sensitive = False
    condotel_sensitive = False
    club_sensitive = False
    eng_sensitive = False
    repgen_sensitive = False
    wo_sensitive = False
    new_contrate = False
    ci_date = None
    hpname_training = ""
    aktlist_flag = False
    dynarate_flag = False
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
    golf_license:bool = False
    paramtext = queasy = htparam = akt_line = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal telop_sensitive, setting_sensitive, condotel_sensitive, club_sensitive, eng_sensitive, repgen_sensitive, wo_sensitive, new_contrate, ci_date, hpname_training, aktlist_flag, dynarate_flag, htl_city, curr_htl_city, p_1072, p_244, p_975, p_996, p_1002, p_997, p_988, p_992, p_1016, p_868, p_990, p_1015, p_169, p_991, p_2000, p_329, p_985, p_473, new_setup, golf_license, paramtext, queasy, htparam, akt_line, bediener


        return {"telop_sensitive": telop_sensitive, "setting_sensitive": setting_sensitive, "condotel_sensitive": condotel_sensitive, "club_sensitive": club_sensitive, "eng_sensitive": eng_sensitive, "repgen_sensitive": repgen_sensitive, "wo_sensitive": wo_sensitive, "new_contrate": new_contrate, "ci_date": ci_date, "hpname_training": hpname_training, "aktlist_flag": aktlist_flag, "dynarate_flag": dynarate_flag, "htl_city": htl_city, "curr_htl_city": curr_htl_city, "p_1072": p_1072, "p_244": p_244, "p_975": p_975, "p_996": p_996, "p_1002": p_1002, "p_997": p_997, "p_988": p_988, "p_992": p_992, "p_1016": p_1016, "p_868": p_868, "p_990": p_990, "p_1015": p_1015, "p_169": p_169, "p_991": p_991, "p_2000": p_2000, "p_329": p_329, "p_985": p_985, "p_473": p_473, "new_setup": new_setup}


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 204)).first()
    curr_htl_city = paramtext.ptexte

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (Queasy.logi2)).first()
    dynarate_flag = None != queasy

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 6001)).first()

    if htparam and not htparam.flogical:
        telop_sensitive = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 169)).first()
    hpname_training = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 999)).first()

    if htparam.flogical:
        setting_sensitive = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 981)).first()

    if not htparam.flogical:
        condotel_sensitive = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1114)).first()

    if not htparam.flogical:
        club_sensitive = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 319)).first()

    if not htparam.flogical or htparam.paramgruppe != 99:
        eng_sensitive = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1072)).first()

    if not htparam.flogical or htparam.paramgruppe != 99:
        repgen_sensitive = False

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 28)).first()

    if not queasy:
        wo_sensitive = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1002)).first()

    if htparam.flogical:

        akt_line = db_session.query(Akt_line).filter(
                (func.lower(Akt_line.userinit) == user_init.lower()) and  (Akt_line.datum >= (ci_date - 1)) and  (Akt_line.datum <= ci_date)).first()
        aktlist_flag = None != akt_line

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 203)).first()
    htl_city = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 473)).first()


    if htparam:
        p_473 = htparam.flogical

    
    p_1072 = get_output(htplogic(1072))
    p_244 = get_output(htpchar(244))

    local_storage.debugging = local_storage.debugging + ",1072:" + str(p_1072)
    local_storage.debugging = local_storage.debugging + ",244:" + str(p_244)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 299)).first()

    if htparam.paramgruppe == 99 and htparam.flogical:
        p_244 = p_244 + chr(2) + "yes"
    else:
        p_244 = p_244 + chr(2) + "no"


    p_975 = get_output(htpint(975))
#     local_storage.debugging = local_storage.debugging + ",975:" + str(p_975)
    p_996 = get_output(htplogic(996))
#     local_storage.debugging = local_storage.debugging + ",996:" + str(996)

    p_1002 = get_output(htplogic(1002))
#     local_storage.debugging = local_storage.debugging + ",1002:" + str(p_1002)

    p_997 = get_output(htplogic(997))
#     local_storage.debugging = local_storage.debugging + ",997:" + str(p_997)

    p_988 = get_output(htplogic(988))
#     local_storage.debugging = local_storage.debugging + ",988:" + str(p_988)

    p_992 = get_output(htplogic(992))
#     local_storage.debugging = local_storage.debugging + ",992:" + str(p_992)

    p_1016 = get_output(htplogic(1016))
#     local_storage.debugging = local_storage.debugging + ",1016:" + str(p_1016)

    p_868 = get_output(htpchar(868))
#     local_storage.debugging = local_storage.debugging + ",868:" + str(p_868)

    p_990 = get_output(htplogic(990))
#     local_storage.debugging = local_storage.debugging + ",990:" + str(p_990)

    p_1015 = get_output(htplogic(1015))
#     local_storage.debugging = local_storage.debugging + "1015:" + str(p_1015)

    p_169 = get_output(htpchar(169))
#     local_storage.debugging = local_storage.debugging + ",169:" + str(p_169)

    p_991 = get_output(htplogic(991))
#     local_storage.debugging = local_storage.debugging + ",991:" + str(p_991)

    p_2000 = get_output(htplogic(2000))
#     local_storage.debugging = local_storage.debugging + ",2000:" + str(p_2000)

    p_329 = get_output(htplogic(329))
#     local_storage.debugging = local_storage.debugging + ",329:" + str(p_329)

    p_985 = get_output(htplogic(985))
#     local_storage.debugging = local_storage.debugging + ",985:" + str(p_985)

    bediener = db_session.query(Bediener).filter(
            (Bediener.username.op("~")(".*" + chr(2) + ".*"))).first()

    if bediener:
        new_setup = True


    else:
        new_setup = False

    return generate_output()