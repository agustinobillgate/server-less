#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Guestbook, Res_history

def operation_image_webbl(vkey:string, case_type:int, user_init:string, image_number:int, location:int, floor:int, char1:string, base64image:string):

    prepare_cache ([Bediener, Res_history])

    result_message = ""
    pointer:bytes = None
    info_str:string = ""
    pic_number:int = 0
    aend_str:string = ""
    img_str:string = ""
    img_num1:int = 0
    img_num2:int = 0
    bediener = guestbook = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, pointer, info_str, pic_number, aend_str, img_str, img_num1, img_num2, bediener, guestbook, res_history
        nonlocal vkey, case_type, user_init, image_number, location, floor, char1, base64image

        return {"base64image": base64image, "result_message": result_message}

    def upload_image():

        nonlocal result_message, pointer, info_str, pic_number, aend_str, img_str, img_num1, img_num2, bediener, guestbook, res_history
        nonlocal vkey, case_type, user_init, image_number, location, floor, char1, base64image

        if base64image == None or base64image == "":
            result_message = "1 - Imagedata Can't be Null!"

            return

        if image_number == None:
            result_message = "1 - Image Number Can't be Null!"

            return

        if user_init == None or user_init == "":
            result_message = "2 - Userinit Can't be Null!"

            return
        else:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if not bediener:
                result_message = "2 - Userinit Not Found!"

                return

        if case_type == 1:
            info_str = "ROOMPLAN IMAGE-" + to_string(image_number)
            pic_number = to_int("-7" + to_string(image_number, "99") + "00000")

        elif case_type == 2:
            info_str = "FLOORPLAN IMAGE-" + "L" + to_string(location) + "F" + to_string(floor)
            pic_number = to_int("-6" + to_string(location, "99") + to_string(floor, "99") + "000")

        elif case_type == 3:
            info_str = "TABLEPLAN IMAGE-" + to_string(image_number)
            pic_number = to_int("-3" + to_string(image_number, "99") + "00000")

        elif case_type == 4:
            info_str = "WORKORDER IMAGE-" + to_string(image_number)
            pic_number = to_int("-8" + to_string(image_number))

        elif case_type == 5:
            info_str = "SCROOM IMAGE-" + to_string(image_number)
            pic_number = to_int("-12" + to_string(image_number))

        elif case_type == 6:
            info_str = "SCROOM&TABLE IMAGE-" + to_string(image_number)
            pic_number = to_int("-10" + to_string(image_number))

        elif case_type == 7:
            info_str = "SCTASKLIST FILE-" + to_string(image_number)
            pic_number = to_int("-13" + to_string(image_number))

        elif case_type == 8:
            info_str = "SCNOTES FILE-" + to_string(image_number)
            pic_number = to_int("-14" + to_string(image_number))

        elif case_type == 9:
            info_str = "HOTEL IMAGE-" + to_string(image_number)
            pic_number = to_int("-15" + to_string(image_number))

        elif case_type == 10:
            info_str = "BQT ATTCH-" + to_string(image_number)
            pic_number = to_int("-16" + to_string(image_number))

        elif case_type == 11:
            info_str = "OUTLET LOGO-" + to_string(image_number)
            pic_number = to_int("-17" + to_string(image_number))


        else:
            result_message = "3 - Unknown CaseType"

            return

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, pic_number)],"reserve_int[0]": [(eq, image_number)]})

        if not guestbook:
            guestbook = Guestbook()
            db_session.add(guestbook)

            guestbook.gastnr = pic_number
            guestbook.zeit = get_current_time_in_seconds()
            guestbook.userinit = user_init
            guestbook.reserve_int[0] = image_number

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = 0
            res_history.reslinnr = 0
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Upload Image For: " + info_str
            res_history.action = "Image Setup"


            pass
            pass
        else:
            guestbook.cid = user_init
            guestbook.changed = get_current_date()
            guestbook.zeit = get_current_time_in_seconds()

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = 0
            res_history.reslinnr = 0
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Change Image For: " + info_str
            res_history.action = "Image Setup"


            pass
            pass
        guestbook.reserve_char[0] = to_string(get_current_time_in_seconds(), "99999") +\
                to_string(get_year(get_current_date())) +\
                to_string(get_month(get_current_date()) , "99") +\
                to_string(get_day(get_current_date()) , "99")
        guestbook.infostr = info_str


        pointer = base64_decode(base64image)
        guestbook.imagefile = pointer
        pass
        pass
        result_message = "0 - Save Image Success"


    def load_dataimage():

        nonlocal result_message, pointer, info_str, pic_number, aend_str, img_str, img_num1, img_num2, bediener, guestbook, res_history
        nonlocal vkey, case_type, user_init, image_number, location, floor, char1, base64image

        if case_type == 1:
            pic_number = to_int("-7" + to_string(image_number, "99") + "00000")

        elif case_type == 2:
            pic_number = to_int("-6" + to_string(location, "99") + to_string(floor, "99") + "000")

        elif case_type == 3:
            pic_number = to_int("-3" + to_string(image_number, "99") + "00000")

        elif case_type == 4:
            pic_number = to_int("-8" + to_string(image_number))

        elif case_type == 5:
            pic_number = to_int("-12" + to_string(image_number))

        elif case_type == 6:
            pic_number = to_int("-10" + to_string(image_number))

        elif case_type == 7:
            pic_number = to_int("-13" + to_string(image_number))

        elif case_type == 8:
            pic_number = to_int("-14" + to_string(image_number))

        elif case_type == 9:
            pic_number = to_int("-15" + to_string(image_number))

        elif case_type == 10:
            pic_number = to_int("-16" + to_string(image_number))

        elif case_type == 11:
            pic_number = to_int("-17" + to_string(image_number))
        else:
            result_message = "1 - Unknown CaseType"

            return

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, pic_number)],"reserve_int[0]": [(eq, image_number)]})

        if not guestbook:
            result_message = "2 - Image Not exist!"

            return
        else:
            pointer = guestbook.imagefile
            base64image = base64_encode(pointer)
            result_message = "0 - Load Image Success"


    def delete_image():

        nonlocal result_message, pointer, info_str, pic_number, aend_str, img_str, img_num1, img_num2, bediener, guestbook, res_history
        nonlocal vkey, case_type, user_init, image_number, location, floor, char1, base64image

        if case_type == 1:
            pic_number = to_int("-7" + to_string(image_number, "99") + "00000")

        elif case_type == 2:
            pic_number = to_int("-6" + to_string(location, "99") + to_string(floor, "99") + "000")

        elif case_type == 3:
            pic_number = to_int("-3" + to_string(image_number, "99") + "00000")

        elif case_type == 4:
            pic_number = to_int("-8" + to_string(image_number))

        elif case_type == 5:
            pic_number = to_int("-12" + to_string(image_number))

        elif case_type == 6:
            pic_number = to_int("-10" + to_string(image_number))

        elif case_type == 7:
            pic_number = to_int("-13" + to_string(image_number))

        elif case_type == 8:
            pic_number = to_int("-14" + to_string(image_number))

        elif case_type == 9:
            pic_number = to_int("-15" + to_string(image_number))

        elif case_type == 10:
            pic_number = to_int("-16" + to_string(image_number))

        elif case_type == 11:
            pic_number = to_int("-17" + to_string(image_number))
        else:
            result_message = "1 - Unknown CaseType"

            return

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, pic_number)],"reserve_int[0]": [(eq, image_number)]})

        if not guestbook:
            result_message = "2 - Image Not exist!"

            return
        else:
            db_session.delete(guestbook)
            pass
            result_message = "0 - Delete Image Success"

    if case_type == 2:
        image_number = to_int(to_string(location) + to_string(floor))

    if vkey.lower()  == ("upload").lower() :
        upload_image()

    elif vkey.lower()  == ("load").lower() :
        load_dataimage()

    elif vkey.lower()  == ("delete").lower() :
        delete_image()

    return generate_output()