
DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR.

DEFINE INPUT PARAMETER from-art AS INTEGER.
DEFINE INPUT PARAMETER to-art AS INTEGER.
DEFINE INPUT PARAMETER from-dept AS INTEGER.
DEFINE INPUT PARAMETER to-dept AS INTEGER.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.
DEFINE INPUT PARAMETER long-digit AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR output-list.

RUN journal-list.


/*************** PROCEDURES ***************/
 
PROCEDURE journal-list:
DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
DEFINE VARIABLE it-exist AS LOGICAL. 
DEFINE VARIABLE ekumnr AS INTEGER. 
DEF VAR amount AS DECIMAL NO-UNDO. 
 
FIND FIRST htparam WHERE paramnr = 555 NO-LOCK. 
ekumnr = htparam.finteger. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
/* 
  FOR EACH artikel WHERE artikel.artnr GE from-art AND artikel.artnr LE to-art 
      AND artikel.departement GE from-dept 
      AND artikel.departement LE to-dept NO-LOCK 
      BY (artikel.departement * 10000 + artikel.artnr): 
    IF last-dept NE artikel.departement THEN 
      FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-LOCK. 
    last-dept = artikel.departement. 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
      AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
*/ 

  FOR EACH artikel WHERE artikel.artnr GE from-art AND artikel.artnr LE to-art 
    AND artikel.departement GE from-dept AND artikel.departement LE to-dept 
    AND artikel.endkum NE ekumnr NO-LOCK 
    BY (artikel.departement * 10000 + artikel.artnr): 
    IF last-dept NE artikel.departement THEN 
      FIND FIRST hoteldpt WHERE hoteldpt.num = artikel.departement NO-ERROR. 
    last-dept = artikel.departement. 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 

    DO curr-date = from-date TO to-date: 
      FOR EACH billjournal WHERE billjournal.stornogrund NE "" 
        AND billjournal.departement = hoteldpt.num AND bill-datum = curr-date 
        AND billjournal.artnr = artikel.artnr NO-LOCK 
        BY billjournal.sysdate BY billjournal.zeit: 
 
        IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
        ELSE amount = billjournal.betrag. 
 
        it-exist = YES. 
        create output-list. 
        IF NOT long-digit THEN output-list.STR = STRING(billjournal.bill-datum) 
                    + STRING(hoteldpt.depart, "x(16)") 
                    + STRING(billjournal.zinr, "999999") 
                    + STRING(billjournal.rechnr, ">>>>>>>>9") 
                    + STRING(billjournal.artnr, ">>>>9") 
                    + STRING(billjournal.bezeich, "x(24)") 
                    + STRING(billjournal.stornogrund, "x(74)") /*william - EC2332 add 50 spaces*/
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, "->,>>>,>>>,>>9.99") 
                    + STRING(billjournal.zeit, "HH:MM") 
                    + STRING(billjournal.userinit, "x(3)"). 
        ELSE output-list.STR = STRING(billjournal.bill-datum) 
                    + STRING(hoteldpt.depart, "x(16)") 
                    + STRING(billjournal.zinr, "999999") 
                    + STRING(billjournal.rechnr, ">>>>>>>>9") 
                    + STRING(billjournal.artnr, ">>>>9") 
                    + STRING(billjournal.bezeich, "x(24)") 
                    + STRING(billjournal.stornogrund, "x(74)") /*william - EC2332 add 50 spaces*/
                    + STRING(billjournal.anzahl, "-9999") 
                    + STRING(amount, " ->>>,>>>,>>>,>>9") 
                    + STRING(billjournal.zeit, "HH:MM") 
                    + STRING(billjournal.userinit, "x(3)"). 
        qty = qty + billjournal.anzahl. 
        sub-tot = sub-tot + amount. 
        tot = tot + amount. 
      END. 
    END. 
    IF it-exist THEN 
    DO: 
      create output-list. 
      IF NOT long-digit THEN output-list.STR = STRING("", "x(118)") /*william - EC2332 add 50 spaces*/
          + STRING("T O T A L   ", "x(24)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
      ELSE output-list.STR = STRING("", "x(118)")                   /*william - EC2332 add 50 spaces*/
          + STRING("T O T A L   ", "x(24)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
    END. 
  END. 
  create output-list. 
  IF NOT long-digit THEN output-list.STR = STRING("", "x(118)") /*william - EC2332 add 50 spaces*/
          + STRING("Grand TOTAL", "x(24)") 
          + STRING(0, ">>>>>") 
          + STRING(tot, "->,>>>,>>>,>>9.99"). 
  ELSE output-list.STR = STRING("", "x(118)")                   /*william - EC2332 add 50 spaces*/
          + STRING("Grand TOTAL", "x(24)") 
          + STRING(0, ">>>>>") 
          + STRING(tot, " ->>>,>>>,>>>,>>9"). 
END. 
 

