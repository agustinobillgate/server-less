DEFINE INPUT PARAMETER resNr        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER failReadFlag AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER roomNr       AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER consumeUse   AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER mealTime     AS CHARACTER NO-UNDO.
DEFINE INPUT PARAMETER ciDate       AS DATE NO-UNDO.
DEFINE INPUT PARAMETER coDate       AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER resultStr   AS CHARACTER NO-UNDO.

DEFINE VARIABLE p-87                AS DATE NO-UNDO.
DEFINE VARIABLE num-of-day          AS INTEGER NO-UNDO.
DEFINE VARIABLE diffCiDate          AS INTEGER NO-UNDO.  
DEFINE VARIABLE i                   AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-87 = htparam.fdate.

diffCiDate = p-87 - ciDate.
IF diffCiDate GT 32 THEN do:
    num-of-day = diffCiDate - 32.
    /*Simpan data ke queasy jika Long Stay lebih dari 32 hari*/
END.
ELSE num-of-day = diffCiDate.

IF num-of-day GE 0 THEN DO TRANSACTION:
    FIND FIRST mealcoup WHERE mealcoup.resnr = resnr AND
        mealcoup.zinr = roomNr AND
        mealcoup.NAME = mealTime NO-LOCK NO-ERROR.
    IF AVAILABLE mealcoup THEN DO: 
        FIND CURRENT mealcoup EXCLUSIVE-LOCK NO-ERROR.
        ASSIGN 
            mealcoup.verbrauch[num-of-day] = mealcoup.verbrauch[num-of-day] + consumeUse.
        IF diffCiDate GT 32 AND (diffCiDate - 32 = 1) THEN DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY = 176
                queasy.number1 = RECID(mealcoup) /*Disimpan berdasarkan RECID Mealcoupon*/
                queasy.number2 = mealcoup.resnr
                queasy.number3 = (diffCiDate - (diffCiDate MOD 32)) / 32 /*Urutan data berdasarkan sudah berapa banyak data yang di buat queasy*/.
            DO i = 1 TO EXTENT(mealcoup.verbrauch):
                ASSIGN
                    queasy.char1 = STRING(mealcoup.verbrauch[i]) + ";" NO-ERROR.
            END.
        END.
        FIND CURRENT mealcoup NO-LOCK NO-ERROR.
        RELEASE mealcoup.
    END.
    ELSE DO:
        CREATE mealcoup.
        ASSIGN
            mealcoup.resnr = resNr
            mealcoup.zinr  = roomNr
            mealcoup.NAME  = mealTime
            mealcoup.verbrauch[num-of-day] = consumeUse
            mealcoup.ankunft = ciDate
            mealcoup.abreise = coDate
            .
    END.
    resultStr = "Success".
    IF failReadFlag THEN DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        CREATE res-history. 
        ASSIGN 
          res-history.nr = bediener.nr 
          res-history.datum = TODAY 
          res-history.zeit = TIME 
          res-history.aenderung = "ReadCard:Failure read from encoder, user " + 
            bediener.username + " trying to querying room number manually".
          res-history.action = "BreakfastKey"
         NO-ERROR. 
        FIND CURRENT res-history NO-LOCK. 
        RELEASE res-history. 
    END.
    RETURN.
END.

resultStr = "Failed".
