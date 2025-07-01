DEF TEMP-TABLE t-list 
    FIELD artnr   AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(36)" 
    FIELD betrag  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE output-list 
  FIELD srecid AS INTEGER INITIAL 0
  FIELD remark AS CHAR FORMAT "x(32)" LABEL "Remark"
  FIELD STR    AS CHAR. 

DEFINE TEMP-TABLE ap-paymentlist
    FIELD srecid     AS INTEGER INIT 0
    FIELD remark     AS CHARACTER 
    FIELD billdate   AS DATE
    FIELD docu-nr    AS CHARACTER
    FIELD ap-amount  AS DECIMAL
    FIELD pay-amount AS DECIMAL
    FIELD pay-date   AS DATE
    FIELD id         AS CHARACTER
    FIELD pay-art    AS CHARACTER
    FIELD supplier   AS CHARACTER
    FIELD deliv-note AS CHARACTER
    FIELD bank-name  AS CHARACTER
    FIELD bank-an    AS CHARACTER
    FIELD bank-acc   AS CHARACTER
    .

DEF INPUT  PARAMETER all-supp       AS LOGICAL.
DEF INPUT  PARAMETER remark-flag    AS LOGICAL.
DEF INPUT  PARAMETER from-supp      AS CHAR.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER from-remark    AS CHAR.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER lief-nr1       AS INT.
DEF OUTPUT PARAMETER ap-exist       AS LOGICAL.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR ap-paymentlist.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEF VAR amount AS CHAR.

/* Malik serverless 854 comment 
RUN ap-paylist-btn-go-cldbl.p (all-supp, remark-flag, from-supp, from-date, to-date,
                 from-remark, price-decimal, OUTPUT lief-nr1, OUTPUT ap-exist,
                 OUTPUT err-code, OUTPUT TABLE output-list, OUTPUT TABLE t-list).*/

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
    RUN create-list2. 
  END. 
END. 

/* 
FOR EACH output-list:
    /* Naufal Afthar - 7B83E5 -> adjust substring*/
    amount = TRIM(SUBSTRING(output-list.str,39,25)).

    IF amount MATCHES "*TOTAL*" THEN amount = "".
    ELSE IF amount MATCHES "*Grand TOTAL*" THEN amount = "".
    /* 854 */
    CREATE ap-paymentlist.
     /*ASSIGN */
        ap-paymentlist.srecid      = output-list.srecid.
        ap-paymentlist.remark      = output-list.remark.
        ap-paymentlist.billdate    = DATE(TRIM(SUBSTRING(output-list.str,1,8))).
        ap-paymentlist.docu-nr     = TRIM(SUBSTRING(output-list.str,9,30)).
        ap-paymentlist.ap-amount   = DECIMAL(amount).
        ap-paymentlist.pay-amount  = DECIMAL(TRIM(SUBSTRING(output-list.str,64,25))).
        ap-paymentlist.pay-date    = DATE(TRIM(SUBSTRING(output-list.str,89,8))).
        ap-paymentlist.id          = TRIM(SUBSTRING(output-list.str,97,3)).
        ap-paymentlist.pay-art     = SUBSTRING(output-list.str,100,20).
        ap-paymentlist.supplier    = SUBSTRING(output-list.STR,152,24).  /*MG Kebutuhan Cloud 1C5944*/
        ap-paymentlist.deliv-note  = SUBSTRING(output-list.str,176,30) . /*MG Kebutuhan Cloud 1C5944*/
        ap-paymentlist.bank-name   = SUBSTRING(output-list.str,252,35).  /*MY #27C683 start*/
        ap-paymentlist.bank-an     = SUBSTRING(output-list.str,287,35).
        ap-paymentlist.bank-acc    = SUBSTRING(output-list.str,322,35).  /*MY #27C683 end*/
        
    /* end Naufal Afthar*/

    /*IF ap-paymentlist.docu-nr NE "" THEN
    DO:
        FIND FIRST l-kredit WHERE l-kredit.NAME EQ ap-paymentlist.docu-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-kredit THEN
        DO:
            ap-paymentlist.deliv-note  = l-kredit.lscheinnr.
        END.
    END.*/
END. */


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

    MESSAGE "TEST 1".
 
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
          /* Malik Serverless 854 comment 
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
          t-credit = 0. */
          CREATE ap-paymentlist.
          /*DO i = 1 TO 49:
            output-list.str = output-list.str + " ". 
          END. */
          ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
          ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).
          IF price-decimal = 0 THEN
          DO:
            /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
                + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount   = DECIMAL(STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9")).
          END.  
          ELSE
          DO:
            /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount   = DECIMAL(STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99")).
          END.
          t-credit = 0.
        END. 
        /* 
        CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + STRING("","x(8)") 
          + STRING(receiver, "x(30)"). 
        lief-nr = l-lieferant.lief-nr. */
        CREATE ap-paymentlist. 
        CREATE ap-paymentlist. 
        /* 
        output-list.str = output-list.str + STRING("","x(8)") 
          + STRING(receiver, "x(30)"). */
        ap-paymentlist.billdate     = DATE(STRING(" ","x(8)")).
        ap-paymentlist.docu-nr      = TRIM(STRING(receiver, "x(30)")).
        lief-nr = l-lieferant.lief-nr.
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      /* Malik Serverless 854 comment 
      CREATE output-list. 
      IF price-decimal = 0 THEN
      ASSIGN
        output-list.srecid = RECID(l-kredit) 
        output-list.str = STRING(debt.rgdatum) /* 8 */ 
          + STRING(l-kredit.name, "x(30)") /* 38 */
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") /* 38 + 24 = 62 */
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") /* 62 + 24 = 86 */
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum) /* 86 + 8 = 94 */
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
      . */
      CREATE ap-paymentlist. 
      IF price-decimal = 0 THEN
      DO:
        /* 
        ASSIGN
            output-list.srecid = RECID(l-kredit) 
            output-list.str = STRING(debt.rgdatum) /* 8 */ 
            + STRING(l-kredit.name, "x(30)") /* 38 */
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") /* 38 + 24 = 62 */
            + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9") /* 62 + 24 = 86 */
            /* end Naufal Afthar*/
            + STRING(l-kredit.rgdatum) /* 86 + 8 = 94 */
        .*/
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).
      END. 
      ELSE
      DO:
        /* 
        ASSIGN
            output-list.srecid = RECID(l-kredit)
            output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
            + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
            /* end Naufal Afthar*/
            + STRING(l-kredit.rgdatum)
        .*/
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).
      END.


      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
      DO:
            /* 
            output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). /* 100 */*/
            ap-paymentlist.id   = TRIM(STRING(bediener.userinit,"x(3)")). 
      END.  
      ELSE
      DO:
            /* 
            output-list.str = output-list.str + "   ". */
            ap-paymentlist.id   = TRIM(STRING(" ","x(3)")). 
      END.
    
      /* 
      ASSIGN
        output-list.str = output-list.str 
          + STRING(art.bezeich,"x(20)") /* 120 */
          + STRING(l-kredit.bemerk, "x(32)") /* 152 */
          + STRING(receiver, "x(24)") /* 176 */
          + STRING(l-kredit.lscheinnr, "x(30)") /*Eko 26062015*/ /* 206 */
          + STRING(l-kredit.zahlkonto, "99999") /* 211 */
          + STRING(l-kredit.rechnr, ">>,>>9")  /*MG Kebutuhan Cloud 1C5944*/ /* 217 */
          + STRING(art.bezeich, "x(35)")       /*MG Kebutuhan Cloud 1C5944*/ /* 252 */
          + STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")  /*MY #27C683 start*/ /* 287 */
          + STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)") /* 322 */
          + STRING(l-lieferant.kontonr, "x(35)")                /*MY #27C683 end*/ /* 357 */
        output-list.remark = l-kredit.bemerk 
        tot-credit = tot-credit + l-kredit.saldo
      .*/
        ASSIGN
            ap-paymentlist.pay-art      = STRING(art.bezeich,"x(20)")
            ap-paymentlist.supplier     = STRING(receiver, "x(24)")
            ap-paymentlist.deliv-note   = STRING(l-kredit.lscheinnr, "x(30)")
            ap-paymentlist.bank-name    = STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")
            ap-paymentlist.bank-an      = STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
            ap-paymentlist.bank-acc     = STRING(l-lieferant.kontonr, "x(35)")
            ap-paymentlist.remark       = l-kredit.bemerk
            tot-credit = tot-credit + l-kredit.saldo
        .
    END.
  END. 
 
  /* 
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
 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/

  CREATE ap-paymentlist. 
  /* 
  DO i = 1 TO 49:  
    output-list.str = output-list.str + " ". 
  END.*/
  ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
  ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).

  IF price-decimal = 0 THEN
  DO:
    /* 
    output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
        + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"))).
  END.
  ELSE
  DO:
    /* 
    output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
        + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"))).
  END.
 
  /* 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/
  CREATE ap-paymentlist.
  CREATE ap-paymentlist.
  ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
  ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).
  IF price-decimal = 0 THEN
  DO:
    /* 
    output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
        + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"))).

  END.
  ELSE
  DO:
    /* 
    output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
        + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99"))).
  END.
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

    MESSAGE "TEST 2".
 
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
        /* Malik Serverless 854 comment 
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
        curr-remark = l-kredit.bemerk. */
        CREATE ap-paymentlist.
        ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
        ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).
        IF price-decimal = 0 THEN
        DO:
            /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"))).
        END.
        ELSE
        DO:
            /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
            + STRING(t-credit, "->,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->,>>>,>>>,>>>,>>9.99"))).
        END.
        t-credit = 0. 
        CREATE ap-paymentlist. 
        curr-remark = l-kredit.bemerk.

      END. 
      t-credit = t-credit + l-kredit.saldo. 

      /* 
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
          + STRING(l-kredit.rgdatum). */
      CREATE ap-paymentlist.
      IF price-decimal = 0 THEN
      DO:
        /* 
        ASSIGN
            output-list.srecid = RECID(l-kredit)
            output-list.str = STRING(debt.rgdatum) 
            + STRING(l-kredit.name, "x(30)") 
            /* Naufal Afthar - 7B83E5 -> extend format*/
            + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9") 
            + STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9") 
            /* end Naufal Afthar*/
            + STRING(l-kredit.rgdatum). */
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))   
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, " ->>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).
      END.
      ELSE
      DO:
        /* 
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum).*/
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))   
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).      
      END.

      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
      DO:
        /* 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)").*/
        ap-paymentlist.id   = TRIM(STRING(bediener.userinit,"x(3)")).  
      END.
      ELSE
      DO:
        /* 
        output-list.str = output-list.str + "   ".*/
        ap-paymentlist.id   = TRIM(STRING(" ","x(3)")). 
      END.
    
        /* 
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
        . */
        ASSIGN
            ap-paymentlist.pay-art      = STRING(art.bezeich,"x(20)")
            ap-paymentlist.supplier     = STRING(receiver, "x(24)")
            ap-paymentlist.deliv-note   = STRING(l-kredit.lscheinnr, "x(30)")
            ap-paymentlist.bank-name    = STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")
            ap-paymentlist.bank-an      = STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
            ap-paymentlist.bank-acc     = STRING(l-lieferant.kontonr, "x(35)")
            ap-paymentlist.remark       = l-kredit.bemerk
            tot-credit = tot-credit + l-kredit.saldo
        .
    END.
  END. 
  
  /* 
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
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
  CREATE ap-paymentlist. 
  /* 
  DO i = 1 TO 49:  
    output-list.str = output-list.str + " ". 
  END.*/
  ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
  ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).

  IF price-decimal = 0 THEN
  DO:
    /* 
     output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
    */
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(tot-credit, "->>>,>>>,>>>,>>>,>>9"))).
  END.
  ELSE
  DO:
    /* 
    output-list.str = output-list.str + STRING("Grand TOTAL", "x(12)") 
    + STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/
    */
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(tot-credit, "->,>>>,>>>,>>>,>>9.99"))).
  END.
 
  /* 
  CREATE output-list. 
  CREATE output-list. 
  DO i = 1 TO 43: 
      output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
     + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/
  CREATE ap-paymentlist.
  CREATE ap-paymentlist.
  ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
  ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).
  IF price-decimal = 0 THEN
  DO:
    /* 
    output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
        + STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(tot-credit, "->>>,>>>,>>>,>>>,>>>,>>9"))).
  END.
  ELSE
  DO:
    /* 
    output-list.str = output-list.str + STRING("Grand TOTAL", "x(14)") 
        + STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99").  /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(tot-credit, "->,>>>,>>>,>>>,>>>,>>9.99"))).

  END.
END. 
 
PROCEDURE create-list2: 
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

    MESSAGE "TEST 3".
 
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
          /* Malik Serverless 854 comment 
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
          t-credit = 0. */
          CREATE ap-paymentlist.
          ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
          ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).
          IF price-decimal = 0 THEN
          DO:
              /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
                + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"))).
          END.  
          ELSE
          DO:
            /* 
            output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
                + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
            ap-paymentlist.ap-amount    = 0.
            ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"))).
          END.
          t-credit = 0.
        END. 
        /* 
        CREATE output-list. 
        CREATE output-list. 
        output-list.str = output-list.str + "        " 
          + STRING(receiver, "x(30)"). 
        lief-nr = l-lieferant.lief-nr.*/
        CREATE ap-paymentlist. 
        CREATE ap-paymentlist.
        ap-paymentlist.billdate     = DATE(STRING(" ","x(8)")).
        ap-paymentlist.docu-nr      = TRIM(STRING(receiver, "x(30)")).
        lief-nr = l-lieferant.lief-nr.  
      END. 
      t-credit = t-credit + l-kredit.saldo. 

      /* Malik Serverless 854 comment 
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
          + STRING(l-kredit.rgdatum). */
    
      CREATE ap-paymentlist. 
      IF price-decimal = 0 THEN
      DO:
        /* 
       ASSIGN
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9") 
          + STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9") 
          /* end Naufal Afthar*/
          + STRING(l-kredit.rgdatum). 
        .*/
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->>>,>>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, "->>>,>>>,>>>,>>>,>>9")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).
      END. 
      ELSE
      DO:
        /* 
        output-list.srecid = RECID(l-kredit)
        output-list.str = STRING(debt.rgdatum) 
          + STRING(l-kredit.name, "x(30)") 
          /* Naufal Afthar - 7B83E5 -> extend format*/
          + STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99") 
          + STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")
          /* end Naufal Afthar*/ 
          + STRING(l-kredit.rgdatum).
        .*/
        ASSIGN
            ap-paymentlist.srecid       = RECID(l-kredit)
            ap-paymentlist.billdate     = DATE(TRIM(STRING(debt.rgdatum)))
            ap-paymentlist.docu-nr      = TRIM(STRING(l-kredit.name, "x(30)"))
            ap-paymentlist.ap-amount    = DECIMAL(TRIM(STRING(debt.netto, "->,>>>,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-amount   = DECIMAL(TRIM(STRING(l-kredit.saldo, "->,>>>,>>>,>>>,>>>,>>9.99")))
            ap-paymentlist.pay-date     = DATE(TRIM(STRING(l-kredit.rgdatum))).
      END.
      
    
      FIND FIRST bediener WHERE bediener.nr = l-kredit.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN 
      DO:
        /* 
        output-list.str = output-list.str + STRING(bediener.userinit,"x(3)"). */
        ap-paymentlist.id   = TRIM(STRING(bediener.userinit,"x(3)")).
      END.
      ELSE
      DO:
        /* 
       output-list.str = output-list.str + "   ". */
       ap-paymentlist.id   = TRIM(STRING(" ","x(3)")).
      END.

      /* 
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
      .*/
       ASSIGN
            ap-paymentlist.pay-art      = STRING(art.bezeich,"x(20)")
            ap-paymentlist.supplier     = STRING(receiver, "x(24)")
            ap-paymentlist.deliv-note   = STRING(l-kredit.lscheinnr, "x(30)")
            ap-paymentlist.bank-name    = STRING(ENTRY(1, l-lieferant.bank, "a/n"), "x(35)")
            ap-paymentlist.bank-an      = STRING(SUBSTR(l-lieferant.bank, LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) + 5, LENGTH(l-lieferant.bank) - LENGTH(ENTRY(1, l-lieferant.bank, "a/n")) - 3), "x(35)")
            ap-paymentlist.bank-acc     = STRING(l-lieferant.kontonr, "x(35)")
            ap-paymentlist.remark       = l-kredit.bemerk
            tot-credit = tot-credit + l-kredit.saldo
        .
    END.
  END. 
  
  /* 
  CREATE output-list. 
  DO i = 1 TO 49: 
    output-list.str = output-list.str + " ". 
  END.
  IF price-decimal = 0 THEN
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/
  ELSE
  output-list.str = output-list.str + STRING("TOTAL", "x(6)") 
    + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
 
  CREATE ap-paymentlist.
  ap-paymentlist.billdate   = DATE(TRIM(STRING(" ", "x(8)"))).
  ap-paymentlist.docu-nr    = TRIM(STRING(" ", "x(30)")).

  IF price-decimal = 0 THEN
  DO:
    /* 
    output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
        + STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->>>,>>>,>>>,>>>,>>>,>>9"))).
  END.
  ELSE
  DO:
    /* 
    output-list.str = output-list.str + STRING("TOTAL", "x(8)") 
        + STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"). /* Naufal Afthar - 7B83E5 -> extend format*/*/
    ap-paymentlist.ap-amount    = 0.
    ap-paymentlist.pay-amount  = DECIMAL(TRIM(STRING(t-credit, "->,>>>,>>>,>>>,>>>,>>9.99"))).
  END.

END. 
