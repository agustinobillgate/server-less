/*Eko 18 Juli 2016 Add Create queasy for A/P Voucher Approval*/

DEFINE TEMP-TABLE age-list 
    FIELD selected        AS LOGICAL INITIAL NO 
    FIELD ap-recid        AS INTEGER 
    FIELD counter         AS INTEGER 
    FIELD docu-nr         AS CHAR FORMAT "x(10)" 
    FIELD rechnr          AS INTEGER 
    FIELD lief-nr         AS INTEGER 
    FIELD lscheinnr       AS CHAR FORMAT "x(23)" 
    FIELD supplier        AS CHAR FORMAT "x(24)" 
    FIELD rgdatum         AS DATE 
    FIELD rabatt          AS DECIMAL FORMAT ">9.99" 
    FIELD rabattbetrag    AS DECIMAL FORMAT "->,>>>,>>9.99" 
    FIELD ziel            AS DATE 
    FIELD netto           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
    FIELD user-init       AS CHAR FORMAT "x(2)" 
    FIELD debt            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
    FIELD credit          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0 
    FIELD bemerk          AS CHAR 
    FIELD tot-debt        AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD rec-id          AS INT
    FIELD resname         AS CHAR
    FIELD comments        AS CHAR
    /*gerald 210920 Tauzia LnL*/   
    FIELD fibukonto       LIKE gl-journal.fibukonto     
    FIELD t-bezeich       LIKE gl-acct.bezeich          
    FIELD debt2            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0  
    FIELD recv-date       AS DATE
    .

DEF INPUT-OUTPUT PARAMETER TABLE FOR age-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ap-debtpay".
DEF VAR p-786   AS CHAR INITIAL "".

DEF BUFFER abuff FOR age-list.
DEF BUFFER t-reshist FOR res-history.

/*Eko 18 Juli 2016*/
FIND FIRST htparam WHERE htparam.paramnr = 786.
IF AVAILABLE htparam THEN p-786 = htparam.fchar.

FIND FIRST counters WHERE counters.counter-no = 40 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE counters THEN
DO:
    CREATE counters.
    ASSIGN counters.counter-no = 40
           counters.counter-bez = "Counter for AP Payment Voucher No."
    .
END.
counters.counter = counters.counter + 1.
FIND CURRENT counters NO-LOCK.
msg-str = msg-str + CHR(2)
        + translateExtended ("DONE. A/P Payment Voucher Number",lvCAREA,"")
        + " = " + STRING(counters.counter, "9999999").

FOR EACH abuff WHERE abuff.SELECTED:
    ASSIGN abuff.rechnr = counters.counter.
    FIND FIRST l-kredit WHERE RECID(l-kredit) = abuff.ap-recid
        EXCLUSIVE-LOCK.
    l-kredit.rechnr = counters.counter.
    FIND CURRENT l-kredit NO-LOCK.
END.

/*Eko 18 Juli 2016*/
IF TRIM(p-786) NE "" THEN DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY      = 173
        queasy.number1  = l-kredit.lief-nr
        queasy.number2  = counters.counter
        queasy.char1    = "".
END.
