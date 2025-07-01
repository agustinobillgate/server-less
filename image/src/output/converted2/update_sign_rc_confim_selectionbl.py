#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line

def update_sign_rc_confim_selectionbl(resno:int, reslino:int, gastno:int, gdpr_flag:bool, mark_flag:bool, news_flag:bool):

    prepare_cache ([Res_line])

    tempzwunsch1:string = ""
    tempzwunsch2:string = ""
    res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tempzwunsch1, tempzwunsch2, res_line
        nonlocal resno, reslino, gastno, gdpr_flag, mark_flag, news_flag

        return {}


    if gdpr_flag == None:
        gdpr_flag = False

    if mark_flag == None:
        mark_flag = False

    if news_flag == None:
        news_flag = False

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslino)],"gastnrmember": [(eq, gastno)]})

    if res_line:

        if not matches(res_line.zimmer_wunsch,r"*GDPR*"):
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "GDPRyes;"

        elif matches(res_line.zimmer_wunsch,r"*GDPR*"):
            tempzwunsch1 = res_line.zimmer_wunsch

            if matches(tempzwunsch1,r"*GDPRyes*"):
                tempzwunsch2 = replace_str(tempzwunsch1, "GDPRyes", "")

            elif matches(tempzwunsch1,r"*GDPRno*"):
                tempzwunsch2 = replace_str(tempzwunsch1, "GDPRno", "")
            res_line.zimmer_wunsch = tempzwunsch2 + "GDPR" + to_string(gdpr_flag) + ";"

        if mark_flag :

            if not matches(res_line.zimmer_wunsch,r"*MARKETING*"):
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "MARKETINGyes;"

            elif matches(res_line.zimmer_wunsch,r"*MARKETING*"):
                tempzwunsch1 = res_line.zimmer_wunsch

                if matches(tempzwunsch1,r"*MARKETINGyes*"):
                    tempzwunsch2 = replace_str(tempzwunsch1, "MARKETINGyes", "")

                elif matches(tempzwunsch1,r"*MARKETINGno*"):
                    tempzwunsch2 = replace_str(tempzwunsch1, "MARKETINGno", "")
                res_line.zimmer_wunsch = tempzwunsch2 + "MARKETING" + to_string(mark_flag) + ";"


        else:
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "MARKETINGno;"

        if news_flag :

            if not matches(res_line.zimmer_wunsch,r"*NEWSLETTER*"):
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "NEWSLETTERyes;"

            elif matches(res_line.zimmer_wunsch,r"*NEWSLETTER*"):
                tempzwunsch1 = res_line.zimmer_wunsch

                if matches(tempzwunsch1,r"*NEWSLETTERyes*"):
                    tempzwunsch2 = replace_str(tempzwunsch1, "NEWSLETTERyes", "")

                elif matches(tempzwunsch1,r"*NEWSLETTERno*"):
                    tempzwunsch2 = replace_str(tempzwunsch1, "NEWSLETTERno", "")
                res_line.zimmer_wunsch = tempzwunsch2 + "NEWSLETTER" + to_string(news_flag) + ";"


        else:
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "NEWSLETTERno;"

    return generate_output()