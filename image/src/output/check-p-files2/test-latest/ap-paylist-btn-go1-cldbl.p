/*Eko 26062015Add some keyword on output-list*/

DEF TEMP-TABLE t-list 
    FIELD artnr   AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(36)" 
    FIELD betrag  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE output-list 
  FIELD srecid AS INTEGER INITIAL 0
  FIELD remark AS CHAR FORMAT "x(32)" LABEL "Remark"
  FIELD STR    AS CHAR. 

DEF INPUT  PARAMETER all-supp       AS LOGICAL.
DEF INPUT  PARAMETER remark-flag    AS LOGICAL.
DEF INPUT  PARAMETER from-supp      AS CHAR.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER from-remark    AS CHAR.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER sort-type      AS INT.
DEF OUTPUT PARAMETER lief-nr1       AS INT.
DEF OUTPUT PARAMETER ap-exist       AS LOGICAL.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEF BUFFER obuff FOR output-list.

IF sort-type EQ 1 THEN
DO:
  IF all-supp AND NOT remark-flag THEN RUN create-list2. 
  ELSE IF all-supp AND remark-flag THEN RUN create-list2A. 
  ELSE 
  DO: 
    FIND FIRST l-lieferant WHERE l-lieferant.firma = from-supp NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-lieferant AND from-supp NE "" THEN 
    DO:
      err-code = 1.
      RETURN NO-APPLY. 
    END. 
    ELSE IF NOT AVAILABLE l-lieferant AND from-supp = "" THEN 
    DO: 
      all-supp = YES. 
      err-code = 2.
      RUN create-list2. 
    END. 
    ELSE IF AVAILABLE l-lieferant THEN 
    DO: 
      lief-nr1 = l-lieferant.lief-nr. 
      all-supp = NO.
      err-code = 3.
      RUN create-list2B. 
    END. 
  END. 
END.
ELSE IF sort-type EQ 2 THEN
DO:
  IF all-supp AND NOT remark-flag THEN RUN create-list3. 
  ELSE IF all-supp AND remark-flag THEN RUN create-list3A. 
  ELSE 
  DO: 
    FIND FIRST l-lieferant WHERE l-lieferant.firma = from-supp NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-lieferant AND from-supp NE "" THEN 
    DO:
      err-code = 1.
      RETURN NO-APPLY. 
    END. 
    ELSE IF NOT AVAILABLE l-lieferant AND from-supp = "" THEN 
    DO: 
      all-supp = YES. 
      err-code = 2.
      RUN create-list3. 
    END. 
    ELSE IF AVAILABLE l-lieferant THEN 
    DO: 
      lief-nr1 = l-lieferant.lief-nr. 
      all-supp = NO.
      err-code = 3.
      RUN create-list3B. 
    END. 
  END. 
END.
ELSE IF sort-type EQ 3 THEN
DO:
  IF all-supp AND NOT remark-flag THEN RUN create-list4. 
  ELSE IF all-supp AND remark-flag THEN RUN create-list4A. 
  ELSE 
  DO: 
    FIND FIRST l-lieferant WHERE l-lieferant.firma = from-supp NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-lieferant AND from-supp NE "" THEN 
    DO:
      err-code = 1.
      RETURN NO-APPLY. 
    END. 
    ELSE IF NOT AVAILABLE l-lieferant AND from-supp = "" THEN 
    DO: 
      all-supp = YES. 
      err-code = 2.
      RUN create-list4. 
    END. 
    ELSE IF AVAILABLE l-lieferant THEN 
    DO: 
      lief-nr1 = l-lieferant.lief-nr. 
      all-supp = NO.
      err-code = 3.
      RUN create-list4B. 
    END. 
  END. 
END.
ELSE
DO:
  IF all-supp AND NOT remark-flag THEN RUN create-list1. 
  ELSE IF all-supp AND remark-flag THEN RUN create-list1A. 
  ELSE 
  DO: 
    FIND FIRST l-lieferant WHERE l-lieferant.firma = from-supp NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-lieferant AND from-supp NE "" THEN 
    DO:
      err-code = 1.
      RETURN NO-APPLY. 
    END. 
    ELSE IF NOT AVAILABLE l-lieferant AND from-supp = "" THEN 
    DO: 
      all-supp = YES. 
      err-code = 2.
      RUN create-list1. 
    END. 
    ELSE IF AVAILABLE l-lieferant THEN 
    DO: 
      lief-nr1 = l-lieferant.lief-nr. 
      all-supp = NO.
      err-code = 3.
      RUN create-list1B. 
    END. 
  END. 
END.

/* Dzikri 975E4D - sorting by payment date (default) */
PROCEDURE create-list1: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-kredit.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES. 
    
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        /*Mofified bernatd 93227D*/
        /*CREATE output-list. 
        output-list.str = output-list.str + STRING("","x(8)")
          + STRING(receiver, "x(30)").*/
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 
      ELSE 
      DO:
        IF debt.netto = 0 THEN 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING("1.11", "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/
            + STRING(l-kredit.rgdatum)
          .
        END.
        ELSE 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/
            + STRING(l-kredit.rgdatum)
          . 
        END.
      END.
      

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
 
  /*CREATE output-list.*/ 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list1A: 

  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "". 

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
     DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-kredit.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.   
   
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      IF curr-remark = "" THEN curr-remark = l-kredit.bemerk. 
      IF curr-remark NE l-kredit.bemerk THEN 
      DO: 
        CREATE output-list. 
        DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END.
        IF price-decimal = 0 THEN
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
        ELSE
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
        t-credit = 0. 
        CREATE output-list. 
        curr-remark = l-kredit.bemerk. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/ 
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list1B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE sub-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "".
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0.
  DEFINE VARIABLE do-it       AS LOGICAL.

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  ASSIGN
    lief-nr     = 0 
    t-credit    = 0
    curr-remark = ""
  . 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 
    AND l-kredit.lief-nr = lief-nr1 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK BY l-kredit.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.  
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      ASSIGN
        sub-credit    = sub-credit + l-kredit.saldo
        t-list.betrag = t-list.betrag + l-kredit.saldo
      . 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END.
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        /*modified by bernatd 93227D*/
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + "        " 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      DO:
        IF debt.netto = 0 THEN 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING("111111", "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/ 
            + STRING(l-kredit.rgdatum).
        END.
        ELSE 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/ 
            + STRING(l-kredit.rgdatum). 
        END.
      END.
    
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 

      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")   /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")        /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
  
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 

/* Dzikri 975E4D - add sorting by billing date */
PROCEDURE create-list2: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY debt.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES. 
    
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 

        /*CREATE output-list. 
        output-list.str = output-list.str + STRING("","x(8)") 
          + STRING(receiver, "x(30)").*/
          
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
 
  /*CREATE output-list.*/ 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list2A: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "". 

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
     DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY debt.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.   
   
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      IF curr-remark = "" THEN curr-remark = l-kredit.bemerk. 
      IF curr-remark NE l-kredit.bemerk THEN 
      DO: 
        CREATE output-list. 
        DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END.
        IF price-decimal = 0 THEN
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
        ELSE
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
        t-credit = 0. 
        CREATE output-list. 
        curr-remark = l-kredit.bemerk. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/ 
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list2B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE sub-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "".
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0.
  DEFINE VARIABLE do-it       AS LOGICAL.
  
  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  ASSIGN
    lief-nr     = 0 
    t-credit    = 0
    curr-remark = ""
  . 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 
    AND l-kredit.lief-nr = lief-nr1 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK BY debt.rgdatum BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.  
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      ASSIGN
        sub-credit    = sub-credit + l-kredit.saldo
        t-list.betrag = t-list.betrag + l-kredit.saldo
      . 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END.
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + "        " 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      DO:
        IF debt.netto = 0 THEN 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING("0", "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/ 
            + STRING(l-kredit.rgdatum). 
        END.
        ELSE 
        DO:
          ASSIGN
          output-list.srecid = RECID(l-kredit)
          output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/ 
            + STRING(l-kredit.rgdatum). 
        END.
        
      END.
      
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 

      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")   /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")        /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
  
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 

/* Dzikri 975E4D - add sorting by document number */
PROCEDURE create-list3: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-kredit.name BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES. 
    
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        /*modified by bernatd 93227D*/
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + STRING("","x(8)") 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
 
  /*CREATE output-list.*/ 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list3A: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "". 

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
     DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-kredit.name BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.   
   
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      IF curr-remark = "" THEN curr-remark = l-kredit.bemerk. 
      IF curr-remark NE l-kredit.bemerk THEN 
      DO: 
        CREATE output-list. 
        DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END.
        IF price-decimal = 0 THEN
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
        ELSE
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
        t-credit = 0. 
        CREATE output-list. 
        curr-remark = l-kredit.bemerk. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/ 
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list3B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE sub-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "".
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0.
  DEFINE VARIABLE do-it       AS LOGICAL.
  
  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  ASSIGN
    lief-nr     = 0 
    t-credit    = 0
    curr-remark = ""
  . 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 
    AND l-kredit.lief-nr = lief-nr1 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK BY l-kredit.name BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.  
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      ASSIGN
        sub-credit    = sub-credit + l-kredit.saldo
        t-list.betrag = t-list.betrag + l-kredit.saldo
      . 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END.
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + "        " 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 
    
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 

      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")   /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")        /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
  
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 

/* Dzikri 975E4D - add sorting by delivery number */
PROCEDURE create-list4: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-lieferant.firma BY l-kredit.lscheinnr BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES. 
    
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END. 
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + STRING("","x(8)") 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum)
      . 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
 
  /*CREATE output-list. */
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list4A: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i           AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it       AS LOGICAL.
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "". 

  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
     DELETE t-list. 
  END. 
 
  lief-nr = 0. 
  t-credit = 0. 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK 
    BY l-kredit.lscheinnr BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.   
   
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 

      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      t-list.betrag = t-list.betrag + l-kredit.saldo. 
 
      ap-exist = YES. 
      IF curr-remark = "" THEN curr-remark = l-kredit.bemerk. 
      IF curr-remark NE l-kredit.bemerk THEN 
      DO: 
        CREATE output-list. 
        DO i = 1 TO 49: 
          output-list.str = output-list.str + " ". 
        END.
        IF price-decimal = 0 THEN
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
        ELSE
        output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
          + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
        t-credit = 0. 
        CREATE output-list. 
        curr-remark = l-kredit.bemerk. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 
    
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/ 
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/
 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 
 
PROCEDURE create-list4B: 
  DEFINE VARIABLE artnr       AS INTEGER INITIAL 0. 
  DEFINE VARIABLE t-credit    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE sub-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE receiver    AS CHAR FORMAT "x(38)". 
  DEFINE VARIABLE curr-remark AS CHAR INITIAL "".
  DEFINE VARIABLE lief-nr     AS INTEGER INITIAL 0.
  DEFINE VARIABLE do-it       AS LOGICAL.
  
  DEFINE BUFFER debt FOR l-kredit. 
  DEFINE BUFFER art  FOR artikel. 
 
  ap-exist = NO. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
  FOR EACH t-list: 
      DELETE t-list. 
  END. 
 
  ASSIGN
    lief-nr     = 0 
    t-credit    = 0
    curr-remark = ""
  . 
  FOR EACH l-kredit WHERE rgdatum GE from-date AND 
    rgdatum LE to-date AND l-kredit.zahlkonto NE 0 
    AND l-kredit.lief-nr = lief-nr1 NO-LOCK, 
    FIRST debt WHERE debt.counter = l-kredit.counter AND debt.zahlkonto = 0 
    NO-LOCK, 
    FIRST art WHERE art.artnr = l-kredit.zahlkonto AND art.departement = 0 
    NO-LOCK BY l-kredit.lscheinnr BY l-kredit.bemerk: 
 
    do-it = YES.
    /*ITA 100817
    IF from-remark NE "" AND from-remark NE l-kredit.bemerk THEN do-it = NO.    */
    IF from-remark NE "" AND NOT l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = NO. 
    ELSE IF from-remark NE "" AND l-kredit.bemerk MATCHES ("*" + from-remark + "*") THEN do-it = YES.  
    IF do-it THEN
    DO:
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      FIND FIRST t-list WHERE t-list.artnr = l-kredit.zahlkonto NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list. 
        ASSIGN 
          t-list.artnr = art.artnr 
          t-list.bezeich = art.bezeich 
        . 
      END. 
      ASSIGN
        sub-credit    = sub-credit + l-kredit.saldo
        t-list.betrag = t-list.betrag + l-kredit.saldo
      . 
 
      ap-exist = YES. 
      receiver = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        IF lief-nr NE 0 THEN 
        DO: 
          CREATE output-list. 
          DO i = 1 TO 49: 
            output-list.str = output-list.str + " ". 
          END.
          IF price-decimal = 0 THEN
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
          ELSE
          output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
          t-credit = 0. 
        END. 
        
        /*CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + "        " 
          + STRING(receiver, "x(30)"). */
        lief-nr = l-lieferant.lief-nr. 
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
      ELSE
      ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum). 
    
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). 
      ELSE output-list.str = output-list.str + "   ". 

      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") 
          + STRING(l-kredit.bemerk, "x(32)")
          + STRING(receiver, "x(24)")
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/
          + STRING(l-kredit.zahlkonto, "99999")
          + STRING(l-kredit.rechnr, ">>,>>9")   /*MG Kebutuhan Cloud 1C5944*/
          + STRING(art.bezeich, "x(35)")        /*MG Kebutuhan Cloud 1C5944*/
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      . 
    END.
  END. 
  
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
END. 

