
DEFINE TEMP-TABLE t-vipnr
    FIELD vip-nr1 AS INT
    FIELD vip-nr2 AS INT
    FIELD vip-nr3 AS INT
    FIELD vip-nr4 AS INT
    FIELD vip-nr5 AS INT
    FIELD vip-nr6 AS INT
    FIELD vip-nr7 AS INT
    FIELD vip-nr8 AS INT
    FIELD vip-nr9 AS INT
    FIELD vip-nr10 AS INT.

DEFINE INPUT  PARAMETER user-init       AS CHAR.
DEFINE OUTPUT PARAMETER ci-date         AS DATE.
DEFINE OUTPUT PARAMETER show-rate       AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER p-297           AS INT.
DEFINE OUTPUT PARAMETER LnL-filepath    AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-vipnr.


FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 857*/ /*IF AVAILABLE*/
IF AVAILABLE htparam THEN
DO:
    IF htparam.fchar NE "" THEN 
    DO: 
        LnL-filepath = htparam.fchar. 
        IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN
        DO:
            LnL-filepath = LnL-filepath + "\". 
            /*MTLnL-filepath = LnL-filepath + LnL-prog. */
        END.
    END. 
END.


FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 857*/ /*IF AVAILABLE*/
IF AVAILABLE htparam THEN
DO:
    p-297 = htparam.finteger.
END.


FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 857*/ /*IF AVAILABLE*/
IF AVAILABLE htparam THEN
DO:
    ci-date = htparam.fdate. 
END.


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 857*/ /*IF AVAILABLE*/
IF AVAILABLE bediener THEN
DO:
    IF SUBSTR(bediener.permissions, 35, 1) NE "0" THEN show-rate = YES. 
END.


RUN fill-vipnr.

PROCEDURE fill-vipnr: /*Alder - Serverless - Issue 857*/ /*IF AVAILABLE*/
    CREATE t-vipnr.

    FIND FIRST htparam WHERE paramnr = 700 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr1 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 701 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr2 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 702 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr3 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 703 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr4 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 704 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr5 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 705 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr6 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 706 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr7 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 707 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr8 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 708 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr9 = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 712 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN t-vipnr.vip-nr10 = htparam.finteger. 
END. 
