
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER trecid         AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER reason-str     AS CHAR.
DEF INPUT  PARAMETER curr-select    AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "approve-list".

DEF BUFFER qbuff FOR queasy.
FIND FIRST queasy WHERE RECID(queasy) = trecid NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO TRANSACTION:
    CREATE qbuff.
    BUFFER-COPY queasy TO qbuff.
    ASSIGN 
        qbuff.logi1      = YES
        qbuff.betriebsnr = 1
        qbuff.number2    = INTEGER(RECID(queasy))
        qbuff.char2      = qbuff.char2 + ";" + user-init 
          + STRING(MONTH(TODAY), "99") + "/" + STRING(DAY(TODAY), "99") + "/"
          + STRING((YEAR(TODAY) - 2000), "99") + ";" + STRING(TIME, "HH:MM:SS")
        qbuff.char3      = reason-str
    .
    IF curr-select = "approve" THEN
        qbuff.logi2      = YES. /*Approve*/
    ELSE qbuff.logi2     = NO.  /*Reject*/
    FIND CURRENT qbuff NO-LOCK.
    RELEASE qbuff.

    FIND CURRENT queasy EXCLUSIVE-LOCK.
    DELETE queasy.
    RELEASE queasy.
END.
ELSE
DO:
    msg-str = msg-str + CHR(2)
            + translateExtended("The request has been cancelled by user.", lvCAREA, "")
            + CHR(10)
            + translateExtended("Update no longer possible.", lvCAREA, "").
END.

