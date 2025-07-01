DEFINE TEMP-TABLE revenue-list
    FIELD payment-type  AS CHAR FORMAT "x(15)"
    FIELD amount        AS DECIMAL FORMAT "->>>>>>>>>>>>"
    FIELD accounttype   AS CHAR
    FIELD accountname   AS CHAR FORMAT "x(15)"
    FIELD comment       AS CHAR
    FIELD bill-datum    AS DATE
    FIELD revenue-recid AS INT
    FIELD bill-number   AS INT
    FIELD send-flag     AS LOGICAL.

DEFINE TEMP-TABLE art-list
    FIELD vhp-artdept  AS INTEGER   FORMAT ">>9"    LABEL "Dept"
    FIELD vhp-artnr    AS INTEGER   FORMAT ">>>>9"  LABEL "Art No"
    FIELD vhp-arttype  AS CHARACTER FORMAT "x(15)"  LABEL "VHP Art Type"
    FIELD vhp-artname  AS CHARACTER FORMAT "x(30)"  LABEL "VHP Art Description"
    FIELD rms-artname  AS CHARACTER FORMAT "x(25)"  LABEL "RMS Art Description"
    FIELD rms-arttype  AS CHARACTER FORMAT "x(15)"  LABEL "RMS Art Type"
    .
/**/
DEFINE INPUT PARAMETER art-dept  AS INT.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR revenue-list.
/*
DEFINE VAR casetype AS INT.
DEFINE VAR art-dept AS INT.
DEFINE VAR rec-id AS INT.

casetype = 1.
art-dept = 1.
*/
DEFINE VARIABLE article-list AS CHAR.

/*
/*ALIPAY, AMERICAN EXPRESS, DINERS CLUB, JCB, VISA, MASTERCARD, UNION PAY, VISA, WECHAT PAY*/
article-list = "9913=DINERS CLUB;9936=JCB;9930=VISA;9931=MASTERCARD;9937=UNION PAY".
art-dept     = 1.
*/
DEFINE VARIABLE loop-i     AS INT.
DEFINE VARIABLE messtoken  AS CHAR.
DEFINE VARIABLE getartname AS CHAR.
DEFINE VARIABLE getartno   AS INT.
DEFINE VARIABLE bill-date  AS DATE.

FIND FIRST queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 97 AND queasy.date1 GE from-date AND queasy.date1 LE to-date NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY        = 242
        queasy.number1    = 97
        queasy.number2    = art-dept
        queasy.date1      = bill-date
        queasy.char1      = "Revenue NonStay Periode : " + STRING(bill-date,"99-99-9999")
        queasy.logi1      = NO
        queasy.betriebsnr = RECID(queasy).
END.
FIND CURRENT queasy.
RELEASE queasy.

FOR EACH queasy WHERE queasy.KEY EQ 242 AND queasy.number1 EQ 98 
    AND queasy.number2 EQ art-dept NO-LOCK BY queasy.number2 BY queasy.number3:
    IF queasy.char3 NE "" THEN
    DO:
        CREATE art-list.
        ASSIGN 
            art-list.vhp-artdept = queasy.number2    
            art-list.vhp-artnr   = queasy.number3         
            art-list.vhp-artname = queasy.char1  
            art-list.rms-arttype = queasy.char2
            art-list.rms-artname = queasy.char3.
    END.
END.
RELEASE queasy.

DEFINE BUFFER buffqueasy FOR queasy.
FOR EACH buffqueasy WHERE buffqueasy.KEY EQ 242 AND buffqueasy.number1 EQ 97 AND buffqueasy.logi1 EQ NO NO-LOCK:
    FOR EACH art-list:
        
        CREATE revenue-list.
        ASSIGN 
            revenue-list.accountname   = art-list.rms-artname
            revenue-list.payment-type  = art-list.rms-arttype
            revenue-list.accounttype   = "extras"
            revenue-list.bill-datum    = buffqueasy.date1
            revenue-list.revenue-recid = buffqueasy.betriebsnr
            revenue-list.send-flag     = buffqueasy.logi1.
    
        FOR EACH h-journal WHERE h-journal.departement EQ art-dept
            AND h-journal.artnr EQ art-list.vhp-artnr 
            AND h-journal.bill-datum EQ buffqueasy.date1 NO-LOCK:
            revenue-list.amount = revenue-list.amount + h-journal.betrag.
            revenue-list.bill-number = h-journal.rechnr.
        END.
        revenue-list.amount = - (revenue-list.amount).
    END. 
END.
