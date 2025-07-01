DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr
    FIELD wabkurz       LIKE waehrung.wabkurz
    FIELD active-flag   AS LOGICAL
.
DEF INPUT PARAMETER curr-select  AS CHAR     NO-UNDO.
DEF INPUT PARAMETER prcode       AS CHAR     NO-UNDO.
DEF INPUT PARAMETER bezeich      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER segmentcode  AS CHAR     NO-UNDO.
/*
DEF INPUT PARAMETER rate-prog    AS CHAR     NO-UNDO.
*/
DEF INPUT PARAMETER minstay      AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER maxstay      AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER minadvance   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER maxadvance   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER frdate       AS DATE     NO-UNDO.
DEF INPUT PARAMETER todate       AS DATE     NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEF INPUT PARAMETER foreign-rate AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER local-flag   AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER drate-flag   AS LOGICAL  NO-UNDO.
DEF INPUT PARAMETER gastnr       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER local-nr     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER foreign-nr   AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER rcode-element AS CHAR   NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR tb1.

DEFINE VARIABLE queasy-number1 AS INTEGER NO-UNDO. /*Alder - Serverless - Issue 723*/

DEFINE BUFFER bqueasy FOR queasy.

IF curr-select = "add" THEN 
DO: 
    CREATE queasy. 
    ASSIGN 
        queasy.key     = 2 
        queasy.char1   = prcode 
        queasy.char2   = bezeich 
        queasy.char3   = segmentcode
        queasy.number2 = minstay
        queasy.deci2   = maxstay
        queasy.number3 = minadvance
        queasy.deci3   = maxadvance
        queasy.date1   = frdate
        queasy.date2   = todate
        queasy.logi1   = local-flag
        queasy.logi2   = drate-flag
        /*queasy.number3 = gastnr*/. 

    IF (NOT foreign-rate) OR queasy.logi1 THEN queasy.number1 = local-nr. 
    ELSE queasy.number1 = foreign-nr. 

    ASSIGN queasy-number1 = queasy.number1. /*Alder - Serverless - Issue 723*/

    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
  
    FIND FIRST bqueasy WHERE bqueasy.KEY EQ 289 AND bqueasy.char1 EQ prcode NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bqueasy THEN
    DO:
        CREATE bqueasy.
        ASSIGN
            bqueasy.KEY    = 289
            bqueasy.char1  = prcode
            bqueasy.char2  = rcode-element.
    END.

    IF gastnr = 0 THEN
    DO:
        FIND LAST guest NO-LOCK NO-ERROR.
        IF AVAILABLE guest AND guest.gastnr GT 0 THEN
        DO:
            gastnr = guest.gastnr + 1.
        END.
        ELSE
        DO:
            gastnr = 1.
        END.
        CREATE guest.
        ASSIGN
            guest.gastnr       = gastnr
            guest.NAME         = prcode
            guest.karteityp    = 9
            guest.anlage-datum = TODAY
            guest.char1        = user-init.
        FIND CURRENT guest NO-LOCK.
    END.

    CREATE guest-pr. 
    ASSIGN
        guest-pr.gastnr = gastnr 
        guest-pr.code   = prcode. 

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
        CREATE res-history.
        ASSIGN 
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Add Contract Rate, Code: " + prcode + " SegmentCode: " + segmentcode + " Description: " + bezeich.
            res-history.action      = "RateCode".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END. 
ELSE /* curr-select = "change" */ 
DO:
    DEFINE VARIABLE ct AS CHARACTER NO-UNDO.
    
    /*Alder - Serverless - Issue 723 - Start*/
    FIND FIRST queasy WHERE queasy.KEY EQ 2 AND queasy.char1 EQ prcode NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.char2    = bezeich
            queasy.logi1    = local-flag
            queasy.number2  = minstay
            queasy.deci2    = maxstay
            queasy.number3  = minadvance
            queasy.deci3    = maxadvance
            queasy.date1    = frdate
            queasy.date2    = todate
            /*queasy.char3 = ""*/.
        
        IF NOT queasy.char3 MATCHES("*;*") THEN
        DO:
            ASSIGN queasy.char3 = segmentcode + ";".
        END.
        ELSE
        DO:
            ASSIGN
                ct = ENTRY(1, queasy.char3, ";") + ";"
                queasy.char3 = segmentcode + ";" + SUBSTR(queasy.char3, LENGTH(ct) + 1).
        END.

        IF (NOT foreign-rate) OR queasy.logi1 THEN queasy.number1 = local-nr. 
        ELSE queasy.number1 = foreign-nr.

        ASSIGN queasy-number1 = queasy.number1.

        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    /*Alder - Serverless - Issue 723 - End*/
  
    FIND FIRST bqueasy WHERE bqueasy.KEY EQ 289 AND bqueasy.char1 EQ prcode NO-LOCK NO-ERROR.
    IF AVAILABLE bqueasy THEN
    DO:
        FIND CURRENT bqueasy EXCLUSIVE-LOCK.
        bqueasy.char2 = rcode-element.
        FIND CURRENT bqueasy NO-LOCK NO-ERROR. /*Added No Error*/
        RELEASE bqueasy.
    END.
    ELSE
    DO:
        CREATE bqueasy.
        ASSIGN
            bqueasy.KEY    = 289
            bqueasy.char1  = prcode
            bqueasy.char2  = rcode-element.
    END.

    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN 
    DO:
        CREATE res-history.
        ASSIGN 
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Modify Contract Rate, Code: " + prcode + " SegmentCode: " + segmentcode + " Description: " + bezeich.
            res-history.action      = "RateCode".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
    END.
END. 

CREATE tb1.
BUFFER-COPY queasy TO tb1.

/*FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN
DO:
    ASSIGN
        tb1.waehrungsnr = waehrung.waehrungsnr
        tb1.wabkurz     = waehrung.wabkurz.
END.*/

/*Alder - Serverless - Issue 723 - Start*/
IF queasy-number1 NE ? THEN
DO:
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy-number1 NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN
    DO:
        ASSIGN
            tb1.waehrungsnr = waehrung.waehrungsnr
            tb1.wabkurz     = waehrung.wabkurz.
    END.
END.
/*Alder - Serverless - Issue 723 - End*/

