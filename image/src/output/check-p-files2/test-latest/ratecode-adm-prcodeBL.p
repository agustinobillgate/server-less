DEFINE TEMP-TABLE tb1 LIKE queasy
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr
    FIELD wabkurz       LIKE waehrung.wabkurz
.
/*
    FIELD KEY           LIKE queasy.KEY
    FIELD number1       LIKE queasy.number1
    FIELD number2       LIKE queasy.number2
    FIELD char1         LIKE queasy.char1
    FIELD char2         LIKE queasy.char2
    FIELD char3         LIKE queasy.char3
    FIELD logi1         LIKE queasy.logi1
    FIELD logi2         LIKE queasy.logi2
    FIELD deci1         LIKE queasy.deci1
    FIELD date1         LIKE queasy.date1
    FIELD betriebsnr    LIKE queasy.betriebsnr
    FIELD waehrungsnr   LIKE waehrung.waehrungsnr
    FIELD wabkurz       LIKE waehrung.wabkurz
.
*/
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
DEF OUTPUT PARAMETER TABLE FOR tb1.

IF curr-select = "add" THEN 
DO: 
  CREATE queasy. 
  ASSIGN 
    queasy.key     = 2 
    queasy.char1   = prcode 
    queasy.char2   = bezeich 
    queasy.char3   = segmentcode + ";"
    queasy.number2 = minstay
    queasy.deci2   = maxstay
    queasy.number3 = minadvance
    queasy.deci3   = maxadvance
    queasy.date1   = frdate
    queasy.date2   = todate
    queasy.logi1   = local-flag
    queasy.logi2   = drate-flag
/*  queasy.number3 = gastnr     /* added april 12, 2007 */ */
  . 
  IF (NOT foreign-rate) OR queasy.logi1 THEN 
    queasy.number1 = local-nr. 
  ELSE queasy.number1 = foreign-nr. 
  FIND CURRENT queasy NO-LOCK. 

  IF gastnr = 0 THEN
  DO:
    FIND LAST guest NO-LOCK NO-ERROR.
    IF AVAILABLE guest AND guest.gastnr GT 0 THEN gastnr = guest.gastnr + 1.
    ELSE gastnr = 1.
    CREATE guest.
    ASSIGN
      guest.gastnr       = gastnr
      guest.NAME         = prcode
      guest.karteityp    = 9
      guest.anlage-datum = TODAY
      guest.char1        = user-init
    .
    FIND CURRENT guest NO-LOCK.
  END.

  CREATE guest-pr. 
  ASSIGN
    guest-pr.gastnr = gastnr 
    guest-pr.code   = prcode
  . 

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
DEF VAR ct AS CHAR NO-UNDO.
  FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prcode EXCLUSIVE-LOCK.
  ASSIGN
    queasy.char2   = bezeich 
    queasy.logi1   = local-flag
    queasy.number2 = minstay
    queasy.deci2   = maxstay
    queasy.number3 = minadvance
    queasy.deci3   = maxadvance
    queasy.date1   = frdate
    queasy.date2   = todate
  .
  IF NOT queasy.char3 MATCHES("*;*") THEN 
      queasy.char3 = segmentcode + ";".
  ELSE
  ASSIGN
      ct           = ENTRY(1, queasy.char3, ";") + ";"
      queasy.char3 = segmentcode + ";" 
                   + SUBSTR(queasy.char3, LENGTH(ct) + 1)
  .
  

  FIND CURRENT queasy NO-LOCK. 

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
FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 
  NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN
ASSIGN
    tb1.waehrungsnr = waehrung.waehrungsnr
    tb1.wabkurz     = waehrung.wabkurz
.
