from functions.additional_functions import *
import decimal
from models import Bediener, Kellner

def ts_helpusr_check_passwdbl(passwd:str, knr:int, dept:int):
    anzahl_falsch = 0
    its_ok = False
    bediener = kellner = None

    vhpusr = None

    Vhpusr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal vhpusr


        nonlocal vhpusr
        return {"anzahl_falsch": anzahl_falsch, "its_ok": its_ok}

    def check_passwd():

        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal vhpusr


        nonlocal vhpusr

        passwd1:str = ""
        Vhpusr = Bediener

        kellner = db_session.query(Kellner).filter(
                (Kellner_nr == knr) &  (Kellner.departement == dept)).first()

        vhpusr = db_session.query(Vhpusr).filter(
                (Vhpusr.userinit == trim(to_string(kellner_nr, ">>99")))).first()
        passwd1 = decode_string1(vhpusr.usercode)
        its_ok = (passwd == passwd1)

        if not its_ok:
            anzahl_falsch = anzahl_falsch + 1

    def decode_string1(in_str:str):

        nonlocal anzahl_falsch, its_ok, bediener, kellner
        nonlocal vhpusr


        nonlocal vhpusr

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr(ord(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))


        return generate_inner_output()

    check_passwd()

    return generate_output()