DEFINE INPUT PARAMETER vKey             AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER case-type        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER image-number     AS INTEGER.
DEFINE INPUT PARAMETER location         AS INTEGER.
DEFINE INPUT PARAMETER floor            AS INTEGER.
DEFINE INPUT PARAMETER char1            AS CHAR NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER base64image AS LONGCHAR NO-UNDO.
DEFINE OUTPUT PARAMETER result-message  AS CHAR.

DEFINE VARIABLE pointer     AS MEMPTR NO-UNDO.
DEFINE VARIABLE info-str    AS CHAR NO-UNDO.
DEFINE VARIABLE pic-number  AS INT.
DEFINE VARIABLE aend-str    AS CHAR NO-UNDO.
DEFINE VARIABLE img-str     AS CHAR NO-UNDO.
DEFINE VARIABLE img-num1    AS INTEGER NO-UNDO.
DEFINE VARIABLE img-num2    AS INTEGER NO-UNDO.

IF case-type EQ 2 THEN
DO:
    image-number = INTEGER(STRING(location) + STRING(floor)).
END.

IF vKey EQ "upload" THEN RUN upload-image.
ELSE IF vKey EQ "load" THEN RUN load-dataimage.
ELSE IF vKey EQ "delete" THEN RUN delete-image.

/***********************************************************************************************/
PROCEDURE upload-image:
    IF base64image EQ ? OR base64image EQ "" THEN
    DO:
        result-message = "1 - Imagedata Can't be Null!".
        RETURN.
    END.
    IF image-number EQ ? THEN
    DO:
        result-message = "1 - Image Number Can't be Null!".
        RETURN.
    END.
    IF user-init EQ ? OR user-init EQ "" THEN
    DO:
        result-message = "2 - Userinit Can't be Null!".
        RETURN.
    END.
    ELSE
    DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bediener THEN
        DO:
            result-message = "2 - Userinit Not Found!".
            RETURN.
        END.
    END.
    
    IF case-type EQ 1 THEN ASSIGN
        info-str   = "ROOMPLAN IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-7" + STRING(image-number,"99") + "00000").
    ELSE IF case-type EQ 2 THEN ASSIGN 
        info-str   = "FLOORPLAN IMAGE-" + "L" + STRING(location) + "F" + STRING(floor)
        pic-number = INTEGER("-6" + STRING(location,"99") + STRING(floor, "99") + "000").
    ELSE IF case-type EQ 3 THEN ASSIGN 
        info-str   = "TABLEPLAN IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-3" + STRING(image-number,"99") + "00000").
    ELSE IF case-type = 4 THEN ASSIGN
        info-str   = "WORKORDER IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-8" + STRING(image-number)).
    ELSE IF case-type = 5 THEN ASSIGN
        info-str   = "SCROOM IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-12" + STRING(image-number)).
    ELSE IF case-type = 6 THEN ASSIGN
        info-str   = "SCROOM&TABLE IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-10" + STRING(image-number)).
    ELSE IF case-type = 7 THEN ASSIGN
        info-str   = "SCTASKLIST FILE-" + STRING(image-number)
        pic-number = INTEGER("-13" + STRING(image-number)).
    ELSE IF case-type = 8 THEN ASSIGN
        info-str   = "SCNOTES FILE-" + STRING(image-number)
        pic-number = INTEGER("-14" + STRING(image-number)).
    ELSE IF case-type = 9 THEN ASSIGN
        info-str   = "HOTEL IMAGE-" + STRING(image-number)
        pic-number = INTEGER("-15" + STRING(image-number)).
    ELSE IF case-type = 10 THEN ASSIGN
        info-str   = "BQT ATTCH-" + STRING(image-number)
        pic-number = INTEGER("-16" + STRING(image-number)).
    ELSE IF case-type = 11 THEN ASSIGN
        info-str   = "OUTLET LOGO-" + STRING(image-number)
        pic-number = INTEGER("-17" + STRING(image-number)).
    ELSE
    DO:
        result-message = "3 - Unknown CaseType".
        RETURN.
    END.
    
    FIND FIRST guestbook WHERE guestbook.gastnr EQ pic-number 
        AND guestbook.reserve-int[1] EQ image-number EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE guestbook THEN
    DO: 
        CREATE guestbook.
        ASSIGN 
        guestbook.gastnr      = pic-number
        guestbook.zeit        = TIME
        guestbook.userinit    = user-init
        guestbook.reserve-int[1] = image-number
        .
    
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
        CREATE res-history. 
        ASSIGN 
              res-history.nr          = bediener.nr 
              res-history.resnr       = 0
              res-history.reslinnr    = 0
              res-history.datum       = TODAY 
              res-history.zeit        = TIME 
              res-history.aenderung   = "Upload Image For: " + info-str
              res-history.action      = "Image Setup". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history. 
    END.
    ELSE
    DO:
        ASSIGN 
        guestbook.cid       = user-init
        guestbook.changed   = TODAY
        guestbook.zeit      = TIME
        .
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
        CREATE res-history. 
        ASSIGN 
              res-history.nr          = bediener.nr 
              res-history.resnr       = 0
              res-history.reslinnr    = 0
              res-history.datum       = TODAY 
              res-history.zeit        = TIME 
              res-history.aenderung   = "Change Image For: " + info-str
              res-history.action      = "Image Setup". 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history.
    END.
    
    ASSIGN guestbook.reserve-char[1] = STRING(TIME,"99999")
        + STRING(YEAR(TODAY))
        + STRING(MONTH(TODAY),"99") 
        + STRING(DAY(TODAY),"99")
            
        guestbook.infostr = info-str.
    
    pointer = BASE64-DECODE(base64image).
    COPY-LOB pointer TO guestbook.imagefile.
    
    FIND CURRENT guestbook.
    RELEASE guestbook.
    result-message = "0 - Save Image Success".
END PROCEDURE.

PROCEDURE load-dataimage:
    IF case-type EQ 1 THEN pic-number = INTEGER("-7" + STRING(image-number,"99") + "00000").
    ELSE IF case-type EQ 2 THEN pic-number = INTEGER("-6" + STRING(location,"99") + STRING(floor,"99") + "000").
    ELSE IF case-type EQ 3 THEN pic-number = INTEGER("-3" + STRING(image-number,"99") + "00000").
    ELSE IF case-type EQ 4 THEN pic-number = INTEGER("-8" + STRING(image-number)).
    ELSE IF case-type EQ 5 THEN pic-number = INTEGER("-12" + STRING(image-number)).
    ELSE IF case-type EQ 6 THEN pic-number = INTEGER("-10" + STRING(image-number)).
    ELSE IF case-type EQ 7 THEN pic-number = INTEGER("-13" + STRING(image-number)).
    ELSE IF case-type EQ 8 THEN pic-number = INTEGER("-14" + STRING(image-number)).
    ELSE IF case-type EQ 9 THEN pic-number = INTEGER("-15" + STRING(image-number)).
    ELSE IF case-type EQ 10 THEN pic-number = INTEGER("-16" + STRING(image-number)).
    ELSE IF case-type EQ 11 THEN pic-number = INTEGER("-17" + STRING(image-number)).
    ELSE
    DO:
        result-message = "1 - Unknown CaseType".
        RETURN.
    END.
    
    FIND FIRST guestbook WHERE guestbook.gastnr EQ pic-number 
        AND guestbook.reserve-int[1] EQ image-number NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guestbook THEN
    DO: 
        result-message = "2 - Image Not exist!".
        RETURN.
    END.
    ELSE
    DO:
        COPY-LOB guestbook.imagefile TO pointer.
        base64image = BASE64-ENCODE(pointer).
        result-message = "0 - Load Image Success".
    END.
END PROCEDURE.

PROCEDURE delete-image:
    IF case-type EQ 1 THEN pic-number = INTEGER("-7" + STRING(image-number,"99") + "00000").
    ELSE IF case-type EQ 2 THEN pic-number = INTEGER("-6" + STRING(location,"99") + STRING(floor,"99") + "000").
    ELSE IF case-type EQ 3 THEN pic-number = INTEGER("-3" + STRING(image-number,"99") + "00000").
    ELSE IF case-type EQ 4 THEN pic-number = INTEGER("-8" + STRING(image-number)).
    ELSE IF case-type EQ 5 THEN pic-number = INTEGER("-12" + STRING(image-number)).
    ELSE IF case-type EQ 6 THEN pic-number = INTEGER("-10" + STRING(image-number)).
    ELSE IF case-type EQ 7 THEN pic-number = INTEGER("-13" + STRING(image-number)).
    ELSE IF case-type EQ 8 THEN pic-number = INTEGER("-14" + STRING(image-number)).
    ELSE IF case-type EQ 9 THEN pic-number = INTEGER("-15" + STRING(image-number)).
    ELSE IF case-type EQ 10 THEN pic-number = INTEGER("-16" + STRING(image-number)).
    ELSE IF case-type EQ 11 THEN pic-number = INTEGER("-17" + STRING(image-number)).
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
END PROCEDURE.

