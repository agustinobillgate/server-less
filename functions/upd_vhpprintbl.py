#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

t_printer_data, T_printer = create_model_like(Printer)

def upd_vhpprintbl(t_printer_data:[T_printer]):
    content:string = ""
    newcontent:string = None
    ni:int = 0
    maxrowperpage:int = 0
    newmaxrowperpage:int = 0
    filesettings:string = ""
    printer = None

    t_printer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal content, newcontent, ni, maxrowperpage, newmaxrowperpage, filesettings, printer


        nonlocal t_printer

        return {}