
DEF TEMP-TABLE t-waehrung1 LIKE waehrung.

DEF INPUT-OUTPUT  PARAMETER reslin-list-betriebsnr AS INT.
DEF INPUT  PARAMETER marknr                 AS INT.
DEF INPUT  PARAMETER foreign-rate           AS LOGICAL.
DEF INPUT  PARAMETER t-contcode             AS CHAR.
DEF INPUT  PARAMETER reslin-list-resnr      AS INT.
DEF INPUT  PARAMETER reslin-list-reslinnr   AS INT.
DEF INPUT  PARAMETER reslin-list-adrflag    AS LOGICAL.
DEF INPUT  PARAMETER res-mode               AS CHAR.
DEF INPUT  PARAMETER gastnr                 AS INT.
DEF INPUT  PARAMETER resnr                  AS INT.
DEF INPUT  PARAMETER reslinnr               AS INT.
DEF OUTPUT PARAMETER local-nr               AS INT.
DEF OUTPUT PARAMETER foreign-nr             AS INT.
DEF OUTPUT PARAMETER guest-currency         AS INT.
DEF OUTPUT PARAMETER curr-wabnr             AS INT.
DEF OUTPUT PARAMETER waehrung1-wabkurz      AS CHAR.
DEF OUTPUT PARAMETER err-msg                AS INT INIT 0.
DEF OUTPUT PARAMETER return-flag            AS INT INIT 0.
DEF OUTPUT PARAMETER err-whr                AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung1.

DEF BUFFER waehrung1 FOR waehrung.
DEF BUFFER rline     FOR res-line.
DEF BUFFER gbuff     FOR guest.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung1 THEN 
DO: 
    err-msg = 1.
    /*MT
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvCAREA, "":U) 
        VIEW-AS ALERT-BOX INFORMATION. 
    */
    RETURN. 
END. 
local-nr = waehrung1.waehrungsnr. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung1 WHERE waehrung1.wabkurz = htparam.fchar 
    NO-LOCK NO-ERROR. 
IF (NOT AVAILABLE waehrung1) AND foreign-rate THEN 
DO: 
    err-msg = 2.
    /*MT
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", 
         lvCAREA, "":U) VIEW-AS ALERT-BOX INFORMATION. 
    */
    RETURN. 
END. 
IF AVAILABLE waehrung1 THEN foreign-nr = waehrung1.waehrungsnr. 

FIND FIRST gbuff WHERE gbuff.gastnr = gastnr NO-LOCK.
IF gbuff.notizen[3] NE "" THEN
DO:
    FIND FIRST waehrung1 WHERE waehrung1.wabkurz = gbuff.notizen[3] 
      NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung1 THEN 
    ASSIGN guest-currency = waehrung1.waehrungsnr.
END.

IF t-contcode NE "" THEN
DO:
    DEF VAR tokcounter AS INTEGER NO-UNDO.
    DEF VAR ifTask     AS CHAR    NO-UNDO.
    DEF VAR mesToken   AS CHAR    NO-UNDO.
    DEF VAR mesValue   AS CHAR    NO-UNDO.
    DEF VAR rCode      AS CHAR    NO-UNDO INIT "".
    FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
      = t-contcode NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.logi2 THEN
    DO:
      FIND FIRST ratecode WHERE ratecode.CODE = t-contcode NO-LOCK.
      ifTask = ratecode.char1[5].
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
        CASE mesToken:
          WHEN "RC" THEN rCode = mesValue.
        END CASE.
      END.
      IF rCode NE "" THEN
      DO:
        FIND FIRST ratecode WHERE ratecode.CODE = rCode NO-LOCK.
        FIND FIRST queasy WHERE queasy.key = 18 
          AND queasy.number1 = ratecode.marknr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
          FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
            = queasy.char3 NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung1 THEN
          DO:
            ASSIGN
                waehrung1-wabkurz = waehrung1.wabkurz
                curr-wabnr        = waehrung1.waehrungsnr 
            .
            /*MT
            currency:ADD-FIRST(waehrung1.wabkurz). 
            ASSIGN currency:SCREEN-VALUE = waehrung1.wabkurz. 
            */
          END.
          /*MT
          ENABLE currency WITH FRAME frame1. 
          DISP currency WITH FRAME frame1. 
          */
          return-flag = 1.
          RETURN. 
        END.
      END.
    END.
END.

FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "arrangement" 
    AND reslin-queasy.resnr = reslin-list-resnr 
    AND reslin-queasy.reslinnr = reslin-list-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE reslin-queasy THEN 
DO:
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE reslin-list-betriebsnr 
        AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
        CREATE t-waehrung1.
        BUFFER-COPY waehrung1 TO t-waehrung1.
        /*MT
        currency:ADD-LAST(waehrung1.wabkurz) IN FRAME frame1. 
        */
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr 
        = reslin-list-betriebsnr NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung1 THEN
    DO:
      waehrung1-wabkurz = waehrung1.wabkurz.
      /*MT
      currency:ADD-FIRST(waehrung1.wabkurz). 
      ASSIGN currency:screen-value = waehrung1.wabkurz. 
      */
    END.
    /*MT
    ENABLE currency WITH FRAME frame1. 
    DISP currency WITH FRAME frame1. 
    */
    return-flag = 2.
    RETURN. 
END. 

IF reslin-list-betriebsnr = 0 OR marknr NE 0 THEN 
DO: 
    DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
    IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci" 
        OR marknr NE 0) THEN 
    DO: 
      RELEASE guest-pr.
      IF t-contcode NE "" THEN FIND FIRST guest-pr WHERE guest-pr.CODE = t-contcode
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE guest-pr THEN
      FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE guest-pr THEN 
      DO: 
        IF marknr NE 0 THEN 
        DO: 
          FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = marknr 
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") 
            THEN FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
            = guest-pr.code NO-LOCK NO-ERROR. 
        END. 
        ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
          = guest-pr.code NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          IF queasy.key = 18 THEN FIND FIRST waehrung1 WHERE waehrung1.wabkurz 
            = queasy.char3 NO-LOCK NO-ERROR. 
          ELSE FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung1 THEN 
          DO: 
            found = YES. 
            curr-wabnr = waehrung1.waehrungsnr. 
            FIND FIRST rline WHERE rline.resnr = resnr 
              AND rline.reslinnr = reslinnr EXCLUSIVE-LOCK NO-ERROR. 

            IF AVAILABLE rline THEN 
            DO: 
              rline.betriebsnr = waehrung1.waehrungsnr. 
              FIND CURRENT rline NO-LOCK. 
              reslin-list-betriebsnr = rline.betriebsnr. 
            END. 
          END. 
        END. 
      END.
    END. 
    IF NOT found THEN 
    DO: 
      IF reslin-list-adrflag = YES OR NOT foreign-rate THEN 
      DO: 
        curr-wabnr = local-nr. 
        reslin-list-betriebsnr = local-nr. 
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = local-nr NO-LOCK. 
      END. 
      ELSE 
      DO: 
        IF guest-currency NE 0 THEN curr-wabnr = guest-currency.
        ELSE curr-wabnr = foreign-nr. 
        reslin-list-betriebsnr = curr-wabnr. 
      END. 

      FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE curr-wabnr 
        AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
        CREATE t-waehrung1.
        BUFFER-COPY waehrung1 TO t-waehrung1.
        /*MT
        currency:ADD-LAST(waehrung1.wabkurz) IN FRAME frame1. 
        */
      END. 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = curr-wabnr NO-LOCK. 
      err-whr = 1.
    END. 
END. 
ELSE 
DO: 
    FOR EACH waehrung1 WHERE waehrung1.waehrungsnr NE reslin-list-betriebsnr 
      AND waehrung1.betriebsnr = 0 NO-LOCK BY waehrung1.bezeich: 
      CREATE t-waehrung1.
      BUFFER-COPY waehrung1 TO t-waehrung1.
      /*MT
      currency:ADD-LAST(waehrung1.wabkurz) IN FRAME frame1. 
      */
    END. 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr 
      = reslin-list-betriebsnr NO-LOCK. 
    err-whr = 2.
END. 

waehrung1-wabkurz = waehrung1.wabkurz.
