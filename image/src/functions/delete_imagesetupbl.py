from functions.additional_functions import *
import decimal
from models import Guestbook

def delete_imagesetupbl(case_type:int, image_number:int):
    result_message = ""
    base64image = ""
    pic_number:int = 0
    pointer:bytes = None
    img_str:str = ""
    img_num1:int = 0
    img_num2:int = 0
    guestbook = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, base64image, pic_number, pointer, img_str, img_num1, img_num2, guestbook


        return {"result_message": result_message, "base64image": base64image}


    if case_type == 2:
        img_str = to_string(image_number)

        if len(img_str) > 1:
            img_num1 = to_int(substring(img_str, 0, 1))
            img_num2 = to_int(substring(img_str, 1, 1))

    if case_type == 1:
        pic_number = to_int("-7" + to_string(image_number, "99") + "00000")

    elif case_type == 2:
        pic_number = to_int("-6" + to_string(img_num1, "99") + to_string(img_num2, "99") + "000")

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

        return generate_output()

    guestbook = db_session.query(Guestbook).filter(
            (Guestbook.gastnr == pic_number) &  (Guestbook.reserve_int[0] == image_number)).first()

    if not guestbook:
        result_message = "2 - Image Not exist!"

        return generate_output()
    else:
        db_session.delete(guestbook)

        result_message = "0 - Delete Image Success"

    return generate_output()