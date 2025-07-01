#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_maintain

def eg_maincalendar_fill_s1bl(awal:date, akhir:date):
    flag = False
    eg_maintain = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, eg_maintain
        nonlocal awal, akhir

        return {"flag": flag}


    eg_maintain = db_session.query(Eg_maintain).filter(
             (Eg_maintain.estworkdate >= awal) & (Eg_maintain.estworkdate <= akhir) & (Eg_maintain.delete_flag == False) | (Eg_maintain.workdate >= awal) & (Eg_maintain.workdate <= akhir) & (Eg_maintain.delete_flag == False)).first()

    if eg_maintain:
        flag = True

    return generate_output()