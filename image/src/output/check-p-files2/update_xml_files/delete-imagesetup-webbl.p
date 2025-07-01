DEFINE INPUT PARAMETER case-type       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER image-number    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER image-number2   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER result-message AS CHAR.
DEFINE OUTPUT PARAMETER base64image    AS LONGCHAR NO-UNDO.

DEFINE VARIABLE pic-number  AS INT.
DEFINE VARIABLE pointer     AS MEMPTR NO-UNDO.
DEFINE VARIABLE img-str     AS CHAR NO-UNDO.
DEFINE VARIABLE img-num1    AS INTEGER NO-UNDO.
DEFINE VARIABLE img-num2    AS INTEGER NO-UNDO.

IF case-type EQ 2 THEN
DO:
    img-str = STRING(image-number).
    IF LENGTH(img-str) GT 1 THEN
    DO:
        img-num1 = INTEGER(SUBSTRING(img-str,1,1)).
        img-num2 = INTEGER(SUBSTRING(img-str,2)).
    END.
END.

IF case-type EQ 1 THEN pic-number = INTEGER("-7" + STRING(image-number,"99") + "00000").
ELSE IF case-type EQ 2 THEN pic-number = INTEGER("-6" + STRING(img-num1,"99") + STRING(img-num2,"99") + "000").
ELSE IF case-type EQ 3 THEN pic-number = INTEGER("-3" + STRING(image-number,"99") + STRING(image-number2,"99999")).
ELSE IF case-type EQ 4 THEN pic-number = INTEGER("-8" + STRING(image-number)).
ELSE IF case-type EQ 5 THEN pic-number = INTEGER("-12" + STRING(image-number)).
ELSE IF case-type EQ 6 THEN pic-number = INTEGER("-10" + STRING(image-number)).
ELSE IF case-type EQ 7 THEN pic-number = INTEGER("-13" + STRING(image-number)).
ELSE IF case-type EQ 8 THEN pic-number = INTEGER("-14" + STRING(image-number)).
ELSE IF case-type EQ 9 THEN pic-number = INTEGER("-15" + STRING(image-number)).
ELSE IF case-type EQ 10 THEN pic-number = INTEGER("-16" + STRING(image-number)).
ELSE IF case-type EQ 11 THEN pic-number = INTEGER("-17" + STRING(image-number)).
ELSE IF case-type EQ 12 THEN pic-number = INTEGER("-18" + STRING(image-number)).
ELSE
DO:
    result-message = "1 - Unknown CaseType".
    RETURN.
END.

FIND FIRST guestbook WHERE guestbook.gastnr EQ pic-number 
    AND guestbook.reserve-int[1] EQ image-number EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE guestbook THEN
DO: 
    result-message = "2 - Image Not exist!".
    RETURN.
END.
ELSE
DO:
    DELETE guestbook.
    RELEASE guestbook.
    result-message = "0 - Delete Image Success".
END.

