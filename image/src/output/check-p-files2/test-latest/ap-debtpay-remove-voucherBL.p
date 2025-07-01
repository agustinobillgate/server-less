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
  FIELD debt2           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0  
  FIELD recv-date       AS DATE
  .

DEF INPUT-OUTPUT PARAMETER TABLE FOR age-list.

DEFINE buffer abuff FOR age-list.
DEFINE buffer debt  FOR l-kredit. 

FOR EACH age-list WHERE age-list.SELECTED:
    FIND FIRST queasy WHERE queasy.KEY = 173
        AND queasy.number1 = age-list.lief-nr
        AND queasy.number2 = age-list.rechnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK NO-ERROR.
        DELETE queasy.
        RELEASE queasy.
    END.

    ASSIGN 
        age-list.rechnr = 0
        age-list.SELECTED = NO
    .
    FIND FIRST l-kredit WHERE RECID(l-kredit) = age-list.ap-recid
        EXCLUSIVE-LOCK.
    ASSIGN l-kredit.rechnr = 0.
    FIND CURRENT l-kredit NO-LOCK.
END.

