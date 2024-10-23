from functions.additional_functions import *
import decimal
from models import Res_line

def guest_locatorbl(resno:int, reslino:int, curr_s:str):
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line
        nonlocal resno, reslino, curr_s


        return {}


    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.reslinnr == reslino)).first()

    if res_line:
        res_line.voucher_nr = curr_s

    return generate_output()