
DEFINE TEMP-TABLE output-list 
  FIELD debtrecid AS INTEGER 
  FIELD debt-day AS INTEGER  
  FIELD STR AS CHAR. 


DEFINE INPUT PARAMETER  from-art    AS INTEGER.
DEFINE INPUT PARAMETER  to-art      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE day1 AS INTEGER. 
DEFINE VARIABLE day2 AS INTEGER. 
DEFINE VARIABLE day3 AS INTEGER. 
 
DEFINE VARIABLE letter1 AS INTEGER. 
DEFINE VARIABLE letter2 AS INTEGER. 
DEFINE VARIABLE letter3 AS INTEGER. 

DEFINE VARIABLE price-decimal AS INTEGER. 

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
day1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
day2 = htparam.finteger + day1. 
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
day3 = htparam.finteger + day2. 
 
FIND FIRST htparam WHERE paramnr = 670 NO-LOCK. 
letter1 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 671 NO-LOCK. 
letter2 = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 388 NO-LOCK. 
letter3 = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

RUN create-list.


PROCEDURE create-list: 
DEFINE VARIABLE artnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-debit AS DECIMAL. 
DEFINE VARIABLE tot-debit AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE receiver AS CHAR FORMAT "x(38)". 
DEFINE VARIABLE address1  AS CHAR FORMAT "x(32)".
DEFINE VARIABLE address2  AS CHAR FORMAT "x(32)".
DEFINE VARIABLE address3  AS CHAR FORMAT "x(32)".
DEFINE VARIABLE contact   AS CHAR FORMAT "x(32)".
DEFINE buffer debtpay FOR debitor. 
DEFINE VARIABLE debt-pay AS DECIMAL. 
DEFINE VARIABLE outstand AS DECIMAL. 
DEFINE VARIABLE debt-day AS INTEGER. 
DEFINE VARIABLE maildate AS CHAR FORMAT "x(8)". 
DEFINE VARIABLE periode_stay AS CHAR FORMAT "x(20)". 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH debitor WHERE debitor.zahlkonto = 0 AND debitor.opart = 0 
    AND debitor.artnr GE from-art AND debitor.artnr LE to-art NO-LOCK, 
    FIRST artikel WHERE artikel.artnr = debitor.artnr 
    AND artikel.artart = 2 AND artikel.departement = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK
    BY artikel.artnr BY debitor.rgdatum BY debitor.name:

    FIND FIRST res-line WHERE res-line.gastnr EQ debitor.gastnr NO-LOCK NO-ERROR.  /* 19/08/22 28085B Rulita | Add Periode Stay (Check in - check out) */
    IF AVAILABLE res-line THEN
    periode_stay = STRING(res-line.ankunft) + " - " + STRING(res-line.abreise).
 
    FIND FIRST akt-kon WHERE akt-kon.gastnr EQ guest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE akt-kon THEN contact = akt-kon.NAME.
    address1  = guest.adresse1.
    address2  = guest.adresse2.
    address3  = guest.adresse3.

    debt-day = today - debitor.rgdatum. 
    IF debt-day GT day1 THEN 
    DO: 
      receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1. 

      debt-pay = 0. 
      FOR EACH debtpay WHERE debtpay.rechnr = debitor.rechnr 
        AND debtpay.opart = 1 AND debtpay.counter = debitor.counter 
        NO-LOCK: 
        debt-pay = debt-pay + debtpay.saldo. 
      END. 
      outstand = debitor.saldo + debt-pay. 
 
      maildate = "". 
      IF versanddat NE ? THEN maildate = STRING(versanddat). 
      
      
      create output-list. 
      ASSIGN
          output-list.debtrecid = RECID(debitor) 
          output-list.debt-day = debt-day
          .
          /*output-list.gastnr = guest.gastnr
          output-list.due-date = DATE(due-date).*/
      
      
      IF price-decimal = 2 THEN
      STR = STRING(artikel.bezeich, "x(16)") 
        + STRING(debitor.rgdatum) 
        + STRING(debitor.rechnr, ">>>>>>>>9") 
        + STRING(receiver, "x(24)") 
        + STRING(debitor.saldo, "->>,>>>,>>9.99") 
        + STRING(debt-pay, "->>,>>>,>>9.99") 
        + STRING(outstand, "->>,>>>,>>9.99") 
        + STRING(debt-day, ">>>9") 
        + STRING(maildate, "x(8)") 
        + STRING(debitor.mahnstufe, ">9")
        + STRING(address1, "x(32)")
        + STRING(address2, "x(32)")
        + STRING(address3, "x(32)")
        + STRING(contact, "x(32)")
        + STRING(periode_stay, "x(20)").             /* 19/08/22 28085B Rulita | Add Periode Stay (Check in - check out) */
      ELSE
      STR = STRING(artikel.bezeich, "x(16)") 
        + STRING(debitor.rgdatum) 
        + STRING(debitor.rechnr, ">>>>>>>>9") 
        + STRING(receiver, "x(24)") 
        + STRING(debitor.saldo, "->,>>>,>>>,>>9") 
        + STRING(debt-pay, "->,>>>,>>>,>>9") 
        + STRING(outstand, "->,>>>,>>>,>>9") 
        + STRING(debt-day, ">>>9") 
        + STRING(maildate, "x(8)") 
        + STRING(debitor.mahnstufe, ">9")
        + STRING(address1, "x(32)")  
        + STRING(address2, "x(32)")  
        + STRING(address3, "x(32)")
        + STRING(contact, "x(32)")
        + STRING(periode_stay, "x(20)").             /* 19/08/22 28085B Rulita | Add Periode Stay (Check in - check out) */
    END. 
  END. 
END. 

