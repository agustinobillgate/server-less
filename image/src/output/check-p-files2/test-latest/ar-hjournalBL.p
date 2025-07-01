DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR. 

DEFINE INPUT  PARAMETER from-art        AS INTEGER.
DEFINE INPUT  PARAMETER to-art          AS INTEGER.
DEFINE INPUT  PARAMETER from-dept       AS INTEGER.
DEFINE INPUT  PARAMETER to-dept         AS INTEGER.
DEFINE INPUT  PARAMETER from-date       AS DATE.
DEFINE INPUT  PARAMETER to-date         AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE long-digit AS LOGICAL. 
DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
DEFINE VARIABLE it-exist AS LOGICAL. 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  IF from-art = 0 THEN 
  FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
      AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
      FOR EACH h-journal WHERE h-journal.artnr = 0 
          AND h-journal.departement = hoteldpt.num 
          AND h-journal.bill-datum = curr-date NO-LOCK: /* Malik Serverless 278 : bill-datum -> h-journal.bill-datum */
        it-exist = YES. 
        create output-list. 
        IF NOT long-digit THEN output-list.str = STRING(h-journal.bill-datum) /* Malik Serverless 278 : STR -> output-list.str */
                    + STRING(h-journal.tischnr, "9999") 
                    + STRING(h-journal.rechnr, "9,999,999") 
                    + STRING(h-journal.artnr, "99999") 
                    + STRING(h-journal.bezeich, "x(28)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(h-journal.anzahl, "-9999") 
                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                    + STRING(h-journal.zeit, "HH:MM:SS") 
                    + STRING(h-journal.kellner-nr, "999"). 
        ELSE output-list.str = STRING(h-journal.bill-datum) /* Malik Serverless 278 : STR -> output-list.str */
                    + STRING(h-journal.tischnr, "9999") 
                    + STRING(h-journal.rechnr, "9,999,999") 
                    + STRING(h-journal.artnr, "99999") 
                    + STRING(h-journal.bezeich, "x(28)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(h-journal.anzahl, "-9999") 
                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                    + STRING(h-journal.zeit, "HH:MM:SS") 
                    + STRING(h-journal.kellner-nr, "999"). 
        qty = qty + h-journal.anzahl. 
        sub-tot = sub-tot + h-journal.betrag. 
        tot = tot + h-journal.betrag. 
      END. 
    END. 
    IF it-exist THEN 
    DO: 
      create output-list. 
      IF NOT long-digit THEN output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
          + STRING("T O T A L   ", "x(12)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
      ELSE output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
          + STRING("T O T A L   ", "x(12)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
    END. 
  END. 
 
  last-dept = - 1. 
  FOR EACH h-artikel WHERE h-artikel.artnr GE from-art 
    AND h-artikel.artnr LE to-art 
    AND (h-artikel.artart = 2 OR h-artikel.artart = 7) 
    AND h-artikel.departement GE from-dept 
    AND h-artikel.departement LE to-dept NO-LOCK, 
    FIRST hoteldpt WHERE hoteldpt.num = h-artikel.departement NO-LOCK 
    BY h-artikel.departement BY h-artikel.artnr: 
    last-dept = h-artikel.departement. 
    sub-tot = 0. 
    it-exist = NO. 
    qty = 0. 
    DO curr-date = from-date TO to-date: 
      FOR EACH h-journal WHERE h-journal.artnr = h-artikel.artnr 
          AND h-journal.departement = h-artikel.departement 
          AND h-journal.bill-datum = curr-date NO-LOCK: 
        it-exist = YES. 
        create output-list. 
        IF NOT long-digit THEN output-list.str = STRING(h-journal.bill-datum) /* Malik Serverless 278 : STR -> output-list.str */
                    + STRING(h-journal.tischnr, "9999") 
                    + STRING(h-journal.rechnr, "9,999,999") 
                    + STRING(h-journal.artnr, "99999") 
                    + STRING(h-journal.bezeich, "x(28)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(h-journal.anzahl, "-9999") 
                    + STRING(h-journal.betrag, "->,>>>,>>>,>>9.99") 
                    + STRING(h-journal.zeit, "HH:MM:SS") 
                    + STRING(h-journal.kellner-nr, "999"). 
        ELSE output-list.str = STRING(h-journal.bill-datum) /* Malik Serverless 278 : STR -> output-list.str */
                    + STRING(h-journal.tischnr, "9999") 
                    + STRING(h-journal.rechnr, "9,999,999") 
                    + STRING(h-journal.artnr, "99999") 
                    + STRING(h-journal.bezeich, "x(28)") 
                    + STRING(hoteldpt.depart, "x(12)") 
                    + STRING(h-journal.anzahl, "-9999") 
                    + STRING(h-journal.betrag, " ->>>,>>>,>>>,>>9") 
                    + STRING(h-journal.zeit, "HH:MM:SS") 
                    + STRING(h-journal.kellner-nr, "999"). 
        qty = qty + h-journal.anzahl. 
        sub-tot = sub-tot + h-journal.betrag. 
        tot = tot + h-journal.betrag. 
      END. 
    END. 
    IF it-exist THEN 
    DO: 
      create output-list. 
      IF NOT long-digit THEN output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
          + STRING("T O T A L   ", "x(12)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, "->,>>>,>>>,>>9.99"). 
      ELSE output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
          + STRING("T O T A L   ", "x(12)") 
          + STRING(qty, "-9999") 
          + STRING(sub-tot, " ->>>,>>>,>>>,>>9"). 
    END. 
  END. 
  create output-list. 
  IF NOT long-digit THEN output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
    + STRING("Grand TOTAL ", "x(12)") 
    + STRING(0, "-9999") 
    + STRING(tot, "->,>>>,>>>,>>9.99"). 
  ELSE output-list.str = STRING("", "x(54)") /* Malik Serverless 278 : STR -> output-list.str */
    + STRING("Grand TOTAL ", "x(12)") 
    + STRING(0, "-9999") 
    + STRING(tot, " ->>>,>>>,>>>,>>9"). 
