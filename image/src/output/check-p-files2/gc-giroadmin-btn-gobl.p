DEF TEMP-TABLE g-list LIKE gc-giro 
    FIELD acctNo LIKE gl-acct.fibukonto
    FIELD s-recid AS INTEGER
.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER case-type  AS INT.
DEF INPUT  PARAMETER s-recid    AS INT.
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF INPUT  PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "gc-giroAdmin".

FIND FIRST g-list.
IF case-type = 1 THEN       /*chg*/
DO :
    RUN chk-gc.
    FIND FIRST gc-giro WHERE RECID(gc-giro) = s-recid EXCLUSIVE-LOCK.
    BUFFER-COPY g-list TO gc-giro.
    ASSIGN 
        gc-giro.fibukonto = g-list.acctNo
        gc-giro.changed   = TODAY
        gc-giro.CID       = user-init
    .
    FIND CURRENT gc-giro NO-LOCK.
    success-flag = YES.
END.
IF case-type = 2 THEN       /*add*/
DO:
    RUN chk-gc.
    IF err-code = 0 THEN
    DO:
        CREATE gc-giro.
        BUFFER-COPY g-list TO gc-giro.
        ASSIGN 
            gc-giro.fibukonto = g-list.acctNo
        .
        FIND CURRENT gc-giro NO-LOCK.
        success-flag = YES.
    END.
END.

PROCEDURE chk-gc:
    IF case-type = 1 THEN
    FIND FIRST gc-giro WHERE gc-giro.bankname = g-list.bankname
        AND gc-giro.gironum = g-list.gironum 
        AND RECID(gc-giro) NE s-recid NO-LOCK NO-ERROR.
    ELSE IF case-type = 2 THEN
    FIND FIRST gc-giro WHERE gc-giro.bankname = g-list.bankname
        AND gc-giro.gironum = g-list.gironum NO-LOCK NO-ERROR.

    IF AVAILABLE gc-giro THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Giro number already exists.",lvCAREA,"").
        /*APPLY "entry" TO g-list.gironum.*/
        err-code = 1.
        RETURN NO-APPLY.
    END.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.acctno
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Account number not found.",lvCAREA,"").
        /*APPLY "entry" TO g-list.acctNo.*/
        err-code = 2.
        RETURN NO-APPLY.
    END.
END.
