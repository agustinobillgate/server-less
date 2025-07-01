
DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR. 

DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE t-debit     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-debit   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE i           AS INTEGER NO-UNDO. 
DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)" NO-UNDO INITIAL "". 
DEFINE VARIABLE datum       AS DATE NO-UNDO INITIAL ?. 
DEFINE VARIABLE tot-saldo   AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE tot-netto   AS DECIMAL NO-UNDO INIT 0.

  FOR EACH output-list: 
    DELETE output-list. 
  END. 

  FOR EACH ap-journal WHERE rgdatum GE from-date AND 
    rgdatum LE to-date /* AND ap-journal.zahlkonto = 0 */ NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = ap-journal.lief-nr NO-LOCK 
    BY ap-journal.sysdate BY ap-journal.zeit: 
    
    ASSIGN receiver = l-lieferant.firma. 
    FIND FIRST bediener WHERE bediener.userinit = ap-journal.userinit NO-LOCK NO-ERROR. 
    create output-list. 
    
    IF ap-journal.zahlkonto = 0 THEN 
    DO: 
      output-list.str = STRING(ap-journal.rgdatum) 
      + STRING(receiver, "x(20)") 
      + STRING(ap-journal.docu-nr, "x(11)") 
      + STRING(ap-journal.lscheinnr, "x(11)") 
      + STRING(ap-journal.netto, " ->,>>>,>>>,>>9.99") 
      + STRING("", "x(38)")
      + STRING(ap-journal.userinit, "x(3)") 
      + STRING(ap-journal.bemerk, "x(12)") 
      + STRING(ap-journal.sysdate) 
      + STRING(ap-journal.zeit, "HH:MM"). 
      ASSIGN tot-netto = tot-netto + ap-journal.netto.
    END. 
    ELSE 
    DO: 
      FIND FIRST artikel WHERE artikel.artnr = ap-journal.zahlkonto 
        AND artikel.departement = 0 NO-LOCK. 
      output-list.str = STRING(ap-journal.rgdatum) 
      + STRING(receiver, "x(20)") 
      + STRING(ap-journal.docu-nr, "x(11)") 
      + STRING(ap-journal.lscheinnr, "x(11)") 
      + STRING("", "x(18)") 
      + STRING(ap-journal.saldo, " ->,>>>,>>>,>>9.99") 
      + STRING(ap-journal.zahlkonto, ">>>9") 
      + STRING(artikel.bezeich, "x(16)") 
      + STRING(ap-journal.userinit, "x(3)") 
      + STRING(ap-journal.bemerk, "x(12)") 
      + STRING(ap-journal.sysdate) 
      + STRING(ap-journal.zeit, "HH:MM"). 
      ASSIGN tot-saldo = tot-saldo + ap-journal.saldo.

    END.           
  END. 

  /*ITA030815*/
  CREATE output-list.

  CREATE output-list.
  output-list.str = STRING(" ", "x(8)") 
                    + STRING("T O T A L", "x(20)") 
                    + STRING(" ", "x(11)") 
                    + STRING(" ", "x(11)") 
                    + STRING(tot-netto, "->>,>>>,>>>,>>9.99") 
                    + STRING(tot-saldo, "->>,>>>,>>>,>>9.99") 
                    + STRING(" ", "x(3)") 
                    + STRING(" ", "x(12)") 
                    + STRING(" ") 
                    + STRING(" "). 
  /*end*/

END. 
