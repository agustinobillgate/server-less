DEFINE TEMP-TABLE s-list 
    FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "000000000000" 
    FIELD debit     LIKE gl-journal.debit 
    FIELD credit    LIKE gl-journal.credit
    FIELD flag      AS LOGICAL INIT NO
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD remark    AS CHARACTER. /*agung add remark*/


DEFINE INPUT PARAMETER language-code    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER docu-nr          AS CHAR.
DEFINE INPUT PARAMETER lief-nr          AS INTEGER. 
DEFINE INPUT PARAMETER firma            AS CHAR.
DEFINE INPUT PARAMETER invoice          AS CHAR. 
DEFINE INPUT PARAMETER rgdatum          AS DATE. 
DEFINE INPUT PARAMETER saldo            AS DECIMAL.    
DEFINE INPUT PARAMETER disc             AS DECIMAL. 
DEFINE INPUT PARAMETER d-amount         AS DECIMAL. 
DEFINE INPUT PARAMETER netto            AS DECIMAL. 
DEFINE INPUT PARAMETER ziel             AS INTEGER INIT 30. 
DEFINE INPUT PARAMETER ap-other         AS CHAR.   
DEFINE INPUT PARAMETER comments         AS CHAR. 
DEFINE INPUT PARAMETER balance          AS DECIMAL. 
DEFINE INPUT PARAMETER s-list-fibukonto AS CHAR.
DEFINE INPUT PARAMETER s-list-debit     AS DECIMAL.
DEFINE INPUT PARAMETER journ-flag       AS LOGICAL. 
DEFINE INPUT PARAMETER nr               AS INTEGER. 
DEFINE INPUT PARAMETER user-init        AS CHAR.
DEFINE INPUT PARAMETER tax-code         AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER tax-amt          AS CHAR NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR s-list.

DEFINE OUTPUT PARAMETER msg-str  AS CHAR.
DEFINE OUTPUT PARAMETER fl-code  AS INTEGER.
DEFINE OUTPUT PARAMETER avail-gl AS LOGICAL. 
DEFINE OUTPUT PARAMETER err-code AS CHAR. 

DEFINE VARIABLE avail-sbuff         AS LOGICAL.
DEFINE VARIABLE closed-date         AS DATE .
DEFINE VARIABLE defaultrgdatum      AS DATE .
DEFINE VARIABLE p-2000              AS LOGICAL.
DEFINE VARIABLE av-gl-acct          AS LOGICAL.
DEFINE VARIABLE ap-acct             AS CHAR. 
DEFINE VARIABLE gst-flag            AS LOGICAL NO-UNDO. /*ITA 260926*/
DEFINE VARIABLE bediener-nr         AS INTEGER.

DEFINE VARIABLE debit               AS DECIMAL. 
DEFINE VARIABLE credit              AS DECIMAL. 

DEFINE BUFFER sbuff FOR s-list. 
DEFINE BUFFER tp-bediener FOR bediener.

RUN prepare-mk-apbl.p (OUTPUT closed-date, OUTPUT defaultrgdatum, OUTPUT p-2000,
                    OUTPUT av-gl-acct, OUTPUT ap-acct, OUTPUT ap-other, OUTPUT gst-flag).

FIND FIRST sbuff WHERE (sbuff.debit NE 0 OR sbuff.credit NE 0) NO-LOCK NO-ERROR.
IF NOT AVAILABLE sbuff THEN
DO:
    avail-sbuff = NO.
END.    
ELSE avail-sbuff = YES.

IF firma = "" THEN 
DO: 
    msg-str  = "Supplier not yet defined.".
    err-code = "7 - " + msg-str. 
    RETURN. 
END. 
ELSE IF docu-nr = "" THEN 
DO: 
    msg-str  = "document number not yet defined.". 
    err-code = "8 - " + msg-str. 
    RETURN. 
END. 
ELSE IF invoice = "" THEN 
DO: 
    msg-str  = "Invoice number not yet defined.".
    err-code = "9 - " + msg-str. 
    RETURN. 
END. 
ELSE IF saldo = 0 THEN 
DO: 
    msg-str  = "A/P amount not yet defined.".
    err-code = "10 - " + msg-str. 
    RETURN. 
END. 
ELSE IF rgdatum = ? THEN 
DO:  
    msg-str = "A/P DATE not yet defined.".
    err-code = "11 - " + msg-str. 
    RETURN. 
END.
ELSE IF rgdatum LE closed-date THEN
DO:
    msg-str  = "Date should be later than " + STRING(closed-date).
    err-code = "12 - " + msg-str. 
    RETURN.
END.   

FIND FIRST tp-bediener WHERE tp-bediener.userinit EQ user-init NO-LOCK NO-ERROR.
IF AVAILABLE tp-bediener THEN
DO:
    bediener-nr = tp-bediener.nr.
END.   
ELSE bediener-nr = nr.

RUN mk-ap-btn-ok_1bl.p
    (INPUT-OUTPUT TABLE s-list, language-code, invoice, journ-flag, balance,
     avail-sbuff, docu-nr, rgdatum, lief-nr, disc, saldo, d-amount,
     ziel, bediener-nr, comments, netto, user-init, ap-other, user-init, firma, 
     s-list-fibukonto, s-list-debit, tax-code, tax-amt, 
     OUTPUT msg-str, OUTPUT fl-code, OUTPUT avail-gl).

IF NOT avail-gl THEN 
DO: 
    msg-str = "G/L account number not defined.".
    err-code = "13 - " + msg-str. 

    FOR EACH s-list:
        IF s-list.flag THEN
        DO:
            ASSIGN
                s-list.debit = s-list.debit
                s-list.fibukonto = "000000000000".
        END.        
    END.
    RETURN. 
END.

IF msg-str NE "" THEN
DO:
    err-code = STRING(fl-code) + " - " + msg-str.
    RETURN.
END.


