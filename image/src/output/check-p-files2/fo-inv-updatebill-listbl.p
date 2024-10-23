
DEFINE TEMP-TABLE t-bill LIKE bill.
DEFINE TEMP-TABLE spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER.

DEFINE TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE tp-bediener  LIKE bediener.

DEFINE INPUT PARAMETER bil-recid        AS INTEGER.
DEFINE INPUT PARAMETER curr-rechnr      AS INTEGER.
DEFINE INPUT PARAMETER tbill-flag       AS INTEGER.
DEFINE INPUT PARAMETER change-date      AS LOGICAL.
DEFINE INPUT PARAMETER resnr            AS INTEGER.
DEFINE INPUT PARAMETER reslinnr         AS INTEGER.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER.
DEFINE INPUT PARAMETER bil-flag         AS INTEGER.
DEFINE INPUT PARAMETER transdate        AS DATE.
DEFINE INPUT PARAMETER billart          AS INTEGER.
DEFINE INPUT PARAMETER curr-department  AS INTEGER.
DEFINE INPUT PARAMETER amount           AS DECIMAL.
DEFINE INPUT PARAMETER amount-foreign   AS DECIMAL.
DEFINE INPUT PARAMETER description      AS CHAR.
DEFINE INPUT PARAMETER qty              AS INT.
DEFINE INPUT PARAMETER curr-room        AS CHAR.
DEFINE INPUT PARAMETER user-init        AS CHAR.
DEFINE INPUT PARAMETER artnr            AS INTEGER.
DEFINE INPUT PARAMETER price            AS DECIMAL.
DEFINE INPUT PARAMETER exchg-rate       AS DECIMAL.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER p-83             AS LOGICAL.
DEFINE INPUT PARAMETER kreditlimit      AS DECIMAL.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT PARAMETER bill-date        AS DATE.
DEFINE INPUT PARAMETER voucher-nr       AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER cancel-str       AS CHAR.

{SupertransBL.i}
DEFINE OUTPUT PARAMETER msgStr          AS CHARACTER.
DEFINE OUTPUT PARAMETER master-str      AS CHAR.
DEFINE OUTPUT PARAMETER master-rechnr   AS CHAR.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER void-approve    AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER flag2           AS INTEGER.
DEFINE OUTPUT PARAMETER flag3           AS INTEGER.
DEFINE OUTPUT PARAMETER tot-balance     AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.
DEFINE OUTPUT PARAMETER TABLE FOR spbill-list.

DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "fo-inv-updatebill-list".
DEFINE VARIABLE room            AS CHARACTER.
DEFINE VARIABLE gname           AS CHARACTER.
/*DEFINE VARIABLE bil-recid       AS INTEGER.*/
DEFINE VARIABLE billdatum       AS DATE.
DEFINE VARIABLE skip-it         AS LOGICAL NO-UNDO INITIAL NO.
DEFINE VARIABLE buff-rechnr     AS INTEGER.
DEFINE VARIABLE master-flag     AS LOGICAL NO-UNDO.  
DEFINE VARIABLE currZeit        AS INTEGER NO-UNDO.
DEFINE VARIABLE ex-rate         AS DECIMAL.
DEFINE VARIABLE mess-str        AS CHARACTER.
DEFINE VARIABLE msg-str         AS CHARACTER.
DEFINE VARIABLE flag1           AS INT.
DEFINE VARIABLE rechnr          AS INT.
DEFINE VARIABLE cancel-flag     AS LOGICAL.
DEFINE VARIABLE p-253           AS LOGICAL.

DEFINE VARIABLE zugriff         AS LOGICAL INITIAL YES.
DEFINE VARIABLE err-str         AS CHARACTER.
/******************************************************************************/
RUN htplogic.p(253, OUTPUT p-253).
IF p-253 THEN
DO: 
    HIDE MESSAGE NO-PAUSE. 
    msgStr = translateExtended ("Night Audit is running, posting not possible",lvCAREA,""). 
    RETURN.
END.

/*RUN prepare-fo-invoice1bl.p (curr-rechnr, OUTPUT room, OUTPUT gname, OUTPUT bil-recid).*/
IF curr-rechnr NE 0 THEN
DO:
    RUN read-billbl.p(2, curr-rechnr, resnr, 
        reslinnr, bil-flag, OUTPUT TABLE t-bill).
    FIND FIRST t-bill NO-ERROR.
    IF AVAILABLE t-bill AND t-bill.flag EQ 1 THEN
    DO:
        RUN zugriff-test(user-init, 38, 2, OUTPUT zugriff, OUTPUT msgStr). /*FD April 22, 2021*/
        IF NOT zugriff THEN
        DO:
            msgStr = translateExtended ("Not possible",lvCAREA,"") 
                    + CHR(10) +
                    translateExtended ("Selected Bill Already Closed",lvCAREA,""). 
            RETURN.
        END.        
    END.
END.

RUN htpdate.p (110, OUTPUT billdatum).
IF transdate NE ? THEN billdatum = transdate.
FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line AND tbill-flag = 1 AND change-date THEN
DO:
    IF billdatum GT res-line.abreise THEN
    DO:
        msgStr = translateExtended ("Posting Date Can not be later than Check-out Date",lvCAREA,"")
                + " " + STRING(res-line.abreise). 
        RETURN.
    END.
END.

FIND FIRST artikel WHERE artikel.artnr = billart 
    AND artikel.departement = curr-department NO-LOCK NO-ERROR.

IF artikel.artart = 9 AND artikel.artgrp = 0 THEN
DO: 
    RUN fo-invoice-update-bill1bl.p (resnr, reslinnr, billdatum, OUTPUT skip-it, OUTPUT buff-rechnr).
    IF skip-it THEN 
    DO:
        IF buff-rechnr = -1 THEN
        DO:
            msgStr = translateExtended ("Posting Room Charge is not allowed when Night Audit is Running.",lvCAREA,""). 
        END.
        ELSE
        DO:
            msgStr = translateExtended ("Not possible",lvCAREA,"") + chr(10) + translateExtended ("Room Charge Already Posted",lvCAREA,"") + " to bill no " + STRING(buff-rechnr).
        END.
        RETURN.
    END.
END.


ASSIGN
    currZeit    = TIME
    master-flag = NO
.

DO TRANSACTION:
    IF tbill-flag = 0 THEN 
    DO: 
        RUN fo-invoice-update-masterbillbl.p
                       (pvILanguage, bil-recid, curr-department, currZeit,
                       amount, amount-foreign, billart, description, qty,
                       curr-room, user-init, artikel.artnr, price,
                       cancel-str, exchg-rate, price-decimal, double-currency,
                       OUTPUT ex-rate, OUTPUT mess-str, OUTPUT master-str,
                       OUTPUT master-rechnr, INPUT-OUTPUT master-flag). 
        IF mess-str NE "" THEN msgStr = mess-str. 
    END.
END.

IF NOT master-flag THEN 
DO: 
    RUN fo-invoice-update-bill2bl.p
                 (pvILanguage, bil-recid, artikel.artnr,
                 bil-flag, amount, amount-foreign, price-decimal,
                 double-currency, foreign-rate, bill-date, transdate,
                 billart, description, qty, curr-room, user-init, artikel.artnr,
                 price, cancel-str, currZeit, voucher-nr, exchg-rate,
                 bil-recid, artikel.departement,
                 OUTPUT msg-str, OUTPUT balance, OUTPUT balance-foreign,
                 OUTPUT cancel-flag, OUTPUT void-approve, OUTPUT flag1,
                 OUTPUT flag2, OUTPUT flag3, OUTPUT rechnr,
                 OUTPUT TABLE t-bill).

    IF msg-str NE "" THEN
    DO:
        msgStr = msg-str.
        RETURN.
    END.
    
    FIND FIRST t-bill NO-LOCK.
    IF flag2 = 1 THEN
    DO:
        IF balance GT kreditlimit THEN RUN red-bcol.
    END.
    IF flag3 = 1 THEN
    DO:
        IF balance GT kreditlimit THEN RUN red-bcol.
        IF AVAILABLE t-bill THEN RUN disp-bill-line.
    END.
END.

IF bil-flag = 0 THEN 
DO: 
    tot-balance = 0. 
    IF t-bill.parent-nr = 0 THEN tot-balance = t-bill.saldo. 
    ELSE RUN fo-invoice-disp-totbalancebl.p(bil-recid, OUTPUT tot-balance).
END. 

cancel-str = "".

/*********************************PROCEDURE*************************************/
PROCEDURE red-bcol:
    IF p-83 THEN
    DO:
        msgStr = translateExtended ("Transaction goes over creditlimit of",lvCAREA,"") 
                + " " + TRIM(STRING(kreditlimit,">,>>>,>>>,>>9.99")).
    END.
END PROCEDURE.

PROCEDURE disp-bill-line:
    RUN fo-invoice-disp-bill-linebl.p(bil-recid, double-currency, 
        OUTPUT TABLE t-bill-line, OUTPUT TABLE spbill-list).
END PROCEDURE.

PROCEDURE zugriff-test:
DEFINE INPUT PARAMETER user-init   AS CHAR FORMAT "x(2)".   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.   
DEFINE OUTPUT PARAMETER msgStr     AS CHARACTER.

DEFINE VARIABLE n               AS INTEGER.  
DEFINE VARIABLE perm            AS INTEGER EXTENT 120 FORMAT "9". /* Malik 4CD2E2 */   
DEFINE VARIABLE s1              AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2              AS CHAR FORMAT "x(1)".

    IF user-init EQ "" THEN
    DO:
        zugriff = NO.
        msgStr = translateExtended ("User not defined.",lvCAREA,"").
        RETURN.
    END.
    ELSE
    DO:
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE tp-bediener.
            BUFFER-COPY bediener TO tp-bediener.
        END.
        ELSE
        DO:
            zugriff = NO.  
            msgStr = translateExtended ("User not defined.",lvCAREA,"").
            RETURN.
        END.
    END.

    DO n = 1 TO LENGTH(tp-bediener.permissions):   
        perm[n] = INTEGER(SUBSTR(tp-bediener.permissions, n, 1)).   
    END.   
    IF perm[array-nr] LT expected-nr THEN   
    DO:   
        zugriff = NO.   
        s1 = STRING(array-nr, "999").   
        s2 = STRING(expected-nr).
        msgStr = translateExtended ("Sorry, No Access Right, Access Code =",lvCAREA,"") + " "
            + s1 + s2.
        RETURN.
    END.
END PROCEDURE.
