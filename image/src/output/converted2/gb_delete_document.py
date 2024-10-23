from functions.additional_functions import *
import decimal

def gb_delete_document(gastno:int):

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastno


        return {}


    vhpgb.guestbook = db_session.query(Vhpgb.guestbook).filter(
             (Vhpgb.guestbook.guestbook.gastnr == gastno)).first()

    if vhpgb.guestbook:
        vhpgb.guestbook_list.remove(vhpgb.guestbook)
        pass

    return generate_output()