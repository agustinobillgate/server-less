DEFINE TEMP-TABLE age-list 
  FIELD name          AS CHAR 
  FIELD counter       AS INTEGER 
  FIELD lief-nr       AS INTEGER 
  FIELD rgdatum       AS DATE 
  FIELD supplier      AS CHARACTER FORMAT "x(34)" 
  FIELD saldo         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt0         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt1         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt2         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD debt3         AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0 
  FIELD tot-debt      AS DECIMAL FORMAT "->>>,>>>,>>9" INITIAL 0
  FIELD adresse1      AS CHARACTER
  FIELD telefon       AS CHARACTER. 

DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR. 

DEF INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER to-date        AS DATE.
DEF INPUT PARAMETER from-name      AS CHAR.
DEF INPUT PARAMETER to-name        AS CHAR.
DEF INPUT PARAMETER day1           AS INTEGER.
DEF INPUT PARAMETER day2           AS INTEGER.
DEF INPUT PARAMETER day3           AS INTEGER.
DEF INPUT PARAMETER curr-disp      AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR output-list.

/*
DEF VAR pvILanguage    AS INTEGER NO-UNDO.
DEF VAR to-date AS DATE INIT 10/30/14.
DEF VAR from-name AS CHAR INIT "central ice".
DEF VAR to-name AS CHAR INIT "central icf".
DEF VAR day1 AS INT INIT 30.
DEF VAR day2 AS INT INIT 60.
DEF VAR day3 AS INT INIT 90.
DEF VAR t-saldo AS DECIMAL INIT 0.
*/

DEFINE VARIABLE outlist AS CHAR FORMAT "x(142)". 
DEFINE VARIABLE price-decimal AS INTEGER NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ap-age".

RUN htpint.p (491, OUTPUT price-decimal).

IF curr-disp = 1 THEN RUN age-list. /*ALL*/
ELSE IF curr-disp = 2 THEN RUN age-list1. /*Manual AP*/
ELSE IF curr-disp = 3 THEN RUN age-list2. /*Receiving AP*/
ELSE IF curr-disp = 4 THEN RUN age-list3. /*Receiving Invoice*/ /*gerald*/

PROCEDURE age-list: 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE counter AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-liefnr  AS INTEGER. 
DEFINE VARIABLE supplier     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
 
DEFINE VARIABLE ap-saldo AS DECIMAL. 
DEFINE VARIABLE do-it    AS LOGICAL NO-UNDO.

DEFINE BUFFER debt FOR l-kredit. 
 
  /*MTCLOSE QUERY q1. */
  FOR EACH age-list: 
    delete age-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
/**** unpaid / partial paid A/P records *****/ 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date 
    AND l-kredit.opart EQ 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
    BY l-lieferant.firma: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:
      ap-saldo = l-kredit.netto. 
      IF l-kredit.counter NE 0 THEN 
      DO: 
        FOR EACH debt WHERE debt.opart = 1 AND debt.counter = l-kredit.counter 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END. 
      END. 
 
      create age-list. 
      age-list.name     = l-kredit.name. 
      age-list.rgdatum  = l-kredit.rgdatum. 
      age-list.counter  = l-kredit.counter. 
      age-list.lief-nr  = l-kredit.lief-nr. 
      age-list.tot-debt = ap-saldo. 
      age-list.supplier = TRIM(l-lieferant.firma + ", " + l-lieferant.anredefirma).
      age-list.adresse1 = l-lieferant.adresse1.
      age-list.telefon  = l-lieferant.adresse1. 
          

    END.
  END. 
 
/**** Full paid A/P records *****/      . 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND l-kredit.opart EQ 2 
    AND l-kredit.zahlkonto = 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK 
    /*BY l-lieferant.firma*/ BY l-kredit.counter: 
    
   
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:

      /*FIND FIRST debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date NO-LOCK NO-ERROR. 
      IF AVAILABLE debt THEN 
      DO: */
        ap-saldo = l-kredit.netto. 
        FOR EACH debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
          AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END.       
        create age-list. 
        age-list.name = l-kredit.name. 
        age-list.rgdatum = l-kredit.rgdatum. 
        age-list.counter = l-kredit.counter. 
        age-list.lief-nr = l-kredit.lief-nr. 
        age-list.tot-debt = ap-saldo. 
        age-list.supplier = l-lieferant.firma + ", " + l-lieferant.anredefirma.
        age-list.adresse1 = l-lieferant.adresse1.
        age-list.telefon  = l-lieferant.adresse1.
      /*END.*/
    END.
  END. 

/* SY 24/10/2014 
  FOR EACH age-list BY LENGTH(age-list.supplier) DESCENDING:
  END.
*/

  curr-liefnr = 0. 
  counter = 0. 
  FOR EACH age-list WHERE  age-list.tot-debt NE 0 BY age-list.supplier: 
    IF to-date - age-list.rgdatum GT day3 
      THEN age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 
      THEN age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 
      THEN age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 
      
      t-saldo  = t-saldo + ROUND(age-list.tot-debt, 0). 
      t-debt0  = t-debt0 + ROUND(age-list.debt0, 0). 
      t-debt1  = t-debt1 + ROUND(age-list.debt1, 0). 
      t-debt2  = t-debt2 + ROUND(age-list.debt2, 0). 
      t-debt3  = t-debt3 + ROUND(age-list.debt3, 0). 
      IF curr-liefnr = 0 THEN 
      DO: 
        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0).
        debt0 = ROUND(age-list.debt0, 0). 
        debt1 = ROUND(age-list.debt1, 0). 
        debt2 = ROUND(age-list.debt2, 0). 
        debt3 = ROUND(age-list.debt3, 0). 
        counter = counter + 1. 
      END. 
      ELSE IF curr-name NE age-list.supplier THEN 
      DO: 
        IF tot-debt NE 0 THEN
        DO:
          IF price-decimal EQ 0 THEN
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
               + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
          ELSE
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
               + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
          
          RUN fill-in-list. 
        END.
        ELSE counter = counter - 1.

        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0). 
        debt0 = ROUND(age-list.debt0, 0).
        debt1 = ROUND(age-list.debt1, 0).
        debt2 = ROUND(age-list.debt2, 0).
        debt3 = ROUND(age-list.debt3, 0).
        counter = counter + 1. 
      END. 
      ELSE 
      DO: 
        tot-debt = tot-debt + ROUND(age-list.tot-debt, 0).
        debt0 = debt0 + ROUND(age-list.debt0, 0). 
        debt1 = debt1 + ROUND(age-list.debt1, 0). 
        debt2 = debt2 + ROUND(age-list.debt2, 0). 
        debt3 = debt3 + ROUND(age-list.debt3, 0). 
      END. 
      curr-liefnr = age-list.lief-nr. 
      curr-name = age-list.supplier. 
      delete age-list. 
  END. 
  IF counter GT 0 AND tot-debt NE 0 THEN 
  DO: 
      IF price-decimal EQ 0 THEN
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
             + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
      ELSE
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
      RUN fill-in-list. 
  END. 
 
  outlist = 
  "-------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list. 

  IF price-decimal EQ 0 THEN
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 
  ELSE
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>,>>>,>>>,>>9.99").
  RUN fill-in-list. 

  outlist = "". 
  RUN fill-in-list. 
  outlist = STRING(translateExtended ("        Statistic Percentage (%) :",lvCAREA,""), "x(33)") 
    + "                      " 
    + "100.00" 
    + "             " 
    + STRING((t-debt0 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt1 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt2 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt3 / t-saldo * 100), "->>9.99"). 
  RUN fill-in-list. 
  outlist = "". 
  RUN fill-in-list. 
END. 

PROCEDURE age-list1: 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE counter AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-liefnr  AS INTEGER. 
DEFINE VARIABLE supplier     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
 
DEFINE VARIABLE ap-saldo AS DECIMAL. 
DEFINE VARIABLE do-it    AS LOGICAL NO-UNDO.

DEFINE BUFFER debt FOR l-kredit. 
 
  /*MTCLOSE QUERY q1. */
  FOR EACH age-list: 
    delete age-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
/**** unpaid / partial paid A/P records *****/ 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date 
    AND l-kredit.opart EQ 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name
    AND l-kredit.steuercode = 1 NO-LOCK 
    BY l-lieferant.firma: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:
      ap-saldo = l-kredit.netto. 
      IF l-kredit.counter NE 0 THEN 
      DO: 
        FOR EACH debt WHERE debt.opart = 1 AND debt.counter = l-kredit.counter 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END. 
      END. 
 
      create age-list. 
      age-list.name = l-kredit.name. 
      age-list.rgdatum = l-kredit.rgdatum. 
      age-list.counter = l-kredit.counter. 
      age-list.lief-nr = l-kredit.lief-nr. 
      age-list.tot-debt = ap-saldo. 
      age-list.supplier = TRIM(l-lieferant.firma + ", " + l-lieferant.anredefirma).
      age-list.adresse1 = l-lieferant.adresse1.
      age-list.telefon  = l-lieferant.adresse1.
    END.
  END. 
 
/**** Full paid A/P records *****/      . 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND l-kredit.opart EQ 2 
    AND l-kredit.zahlkonto = 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name
    AND l-kredit.steuercode = 1 NO-LOCK 
    /*BY l-lieferant.firma*/ BY l-kredit.counter: 
    
   
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:

      /*FIND FIRST debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date NO-LOCK NO-ERROR. 
      IF AVAILABLE debt THEN 
      DO: */
        ap-saldo = l-kredit.netto. 
        FOR EACH debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
          AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END.       
        create age-list. 
        age-list.name = l-kredit.name. 
        age-list.rgdatum = l-kredit.rgdatum. 
        age-list.counter = l-kredit.counter. 
        age-list.lief-nr = l-kredit.lief-nr. 
        age-list.tot-debt = ap-saldo. 
        age-list.supplier = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
        age-list.adresse1 = l-lieferant.adresse1.
        age-list.telefon  = l-lieferant.adresse1.
      /*END.*/
    END.
  END. 

/* SY 24/10/2014 
  FOR EACH age-list BY LENGTH(age-list.supplier) DESCENDING:
  END.
*/

  curr-liefnr = 0. 
  counter = 0. 
  FOR EACH age-list WHERE  age-list.tot-debt NE 0 BY age-list.supplier: 
    IF to-date - age-list.rgdatum GT day3 
      THEN age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 
      THEN age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 
      THEN age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 
      
      t-saldo  = t-saldo + ROUND(age-list.tot-debt, 0). 
      t-debt0  = t-debt0 + ROUND(age-list.debt0, 0).   
      t-debt1  = t-debt1 + ROUND(age-list.debt1, 0).   
      t-debt2  = t-debt2 + ROUND(age-list.debt2, 0).   
      t-debt3  = t-debt3 + ROUND(age-list.debt3, 0).   
      IF curr-liefnr = 0 THEN 
      DO: 
        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0).
        debt0 = ROUND(age-list.debt0, 0). 
        debt1 = ROUND(age-list.debt1, 0). 
        debt2 = ROUND(age-list.debt2, 0). 
        debt3 = ROUND(age-list.debt3, 0). 
        counter = counter + 1. 
      END. 
      ELSE IF curr-name NE age-list.supplier THEN 
      DO: 
        IF tot-debt NE 0 THEN
        DO:
          IF price-decimal EQ 0 THEN
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
               + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
          ELSE
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
               + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
          
          RUN fill-in-list. 
        END.
        ELSE counter = counter - 1.

        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0). 
        debt0 = ROUND(age-list.debt0, 0).
        debt1 = ROUND(age-list.debt1, 0).
        debt2 = ROUND(age-list.debt2, 0).
        debt3 = ROUND(age-list.debt3, 0).
        counter = counter + 1.  
      END. 
      ELSE 
      DO: 
        tot-debt = tot-debt + ROUND(age-list.tot-debt, 0).
        debt0 = debt0 + ROUND(age-list.debt0, 0). 
        debt1 = debt1 + ROUND(age-list.debt1, 0). 
        debt2 = debt2 + ROUND(age-list.debt2, 0). 
        debt3 = debt3 + ROUND(age-list.debt3, 0). 
      END. 
      curr-liefnr = age-list.lief-nr. 
      curr-name = age-list.supplier. 
      delete age-list. 
  END. 
  IF counter GT 0 AND tot-debt NE 0 THEN 
  DO: 
      IF price-decimal EQ 0 THEN
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
             + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
      ELSE
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
      RUN fill-in-list. 
  END. 
 
  outlist = 
  "-------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list. 

  IF price-decimal EQ 0 THEN
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 
  ELSE
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>,>>>,>>>,>>9.99").
  RUN fill-in-list. 

  outlist = "". 
  RUN fill-in-list. 
  outlist = STRING(translateExtended ("        Statistic Percentage (%) :",lvCAREA,""), "x(33)") 
    + "                      " 
    + "100.00" 
    + "             " 
    + STRING((t-debt0 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt1 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt2 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt3 / t-saldo * 100), "->>9.99"). 
  RUN fill-in-list. 
  outlist = "". 
  RUN fill-in-list. 
END.

PROCEDURE age-list2: 
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE counter AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-liefnr  AS INTEGER. 
DEFINE VARIABLE supplier     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 
 
DEFINE VARIABLE ap-saldo AS DECIMAL. 
DEFINE VARIABLE do-it    AS LOGICAL NO-UNDO.

DEFINE BUFFER debt FOR l-kredit. 
 
  /*MTCLOSE QUERY q1. */
  FOR EACH age-list: 
    delete age-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
/**** unpaid / partial paid A/P records *****/ 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date 
    AND l-kredit.opart EQ 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name
    AND l-kredit.steuercode = 0 NO-LOCK 
    BY l-lieferant.firma: 
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:
      ap-saldo = l-kredit.netto. 
      IF l-kredit.counter NE 0 THEN 
      DO: 
        FOR EACH debt WHERE debt.opart = 1 AND debt.counter = l-kredit.counter 
          AND debt.zahlkonto NE 0 
          AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END. 
      END. 
 
      create age-list. 
      age-list.name = l-kredit.name. 
      age-list.rgdatum = l-kredit.rgdatum. 
      age-list.counter = l-kredit.counter. 
      age-list.lief-nr = l-kredit.lief-nr. 
      age-list.tot-debt = ap-saldo. 
      age-list.supplier = TRIM(l-lieferant.firma + ", " + l-lieferant.anredefirma). 
      age-list.adresse1 = l-lieferant.adresse1.
      age-list.telefon  = l-lieferant.adresse1.

    END.
  END. 
 
/**** Full paid A/P records *****/      . 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND l-kredit.opart EQ 2 
    AND l-kredit.zahlkonto = 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name
    AND l-kredit.steuercode = 0 NO-LOCK 
    /*BY l-lieferant.firma*/ BY l-kredit.counter: 
    
   
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:

      /*FIND FIRST debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
        AND debt.zahlkonto NE 0 AND debt.rgdatum GT to-date NO-LOCK NO-ERROR. 
      IF AVAILABLE debt THEN 
      DO: */
        ap-saldo = l-kredit.netto. 
        FOR EACH debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
          AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date NO-LOCK: 
          ap-saldo = ap-saldo + debt.saldo. 
        END.       
        create age-list. 
        age-list.name = l-kredit.name. 
        age-list.rgdatum = l-kredit.rgdatum. 
        age-list.counter = l-kredit.counter. 
        age-list.lief-nr = l-kredit.lief-nr. 
        age-list.tot-debt = ap-saldo. 
        age-list.supplier = l-lieferant.firma + ", " + l-lieferant.anredefirma. 
        age-list.adresse1 = l-lieferant.adresse1.
        age-list.telefon  = l-lieferant.adresse1.
      /*END.*/
    END.
  END. 

/* SY 24/10/2014 
  FOR EACH age-list BY LENGTH(age-list.supplier) DESCENDING:
  END.
*/

  curr-liefnr = 0. 
  counter = 0. 
  FOR EACH age-list WHERE  age-list.tot-debt NE 0 BY age-list.supplier: 
    IF to-date - age-list.rgdatum GT day3 
      THEN age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 
      THEN age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 
      THEN age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 
      
      t-saldo  = t-saldo + ROUND(age-list.tot-debt, 0). 
      t-debt0  = t-debt0 + ROUND(age-list.debt0, 0).   
      t-debt1  = t-debt1 + ROUND(age-list.debt1, 0).   
      t-debt2  = t-debt2 + ROUND(age-list.debt2, 0).   
      t-debt3  = t-debt3 + ROUND(age-list.debt3, 0).   
      IF curr-liefnr = 0 THEN 
      DO: 
         supplier = age-list.supplier. 
         tot-debt = ROUND(age-list.tot-debt, 0).
         debt0 = ROUND(age-list.debt0, 0). 
         debt1 = ROUND(age-list.debt1, 0). 
         debt2 = ROUND(age-list.debt2, 0). 
         debt3 = ROUND(age-list.debt3, 0). 
         counter = counter + 1. 
      END. 
      ELSE IF curr-name NE age-list.supplier THEN 
      DO: 
        IF tot-debt NE 0 THEN
        DO:
          IF price-decimal EQ 0 THEN
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
               + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
          ELSE
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
               + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
          
          RUN fill-in-list. 
        END.
        ELSE counter = counter - 1.

        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0). 
        debt0 = ROUND(age-list.debt0, 0).
        debt1 = ROUND(age-list.debt1, 0).
        debt2 = ROUND(age-list.debt2, 0).
        debt3 = ROUND(age-list.debt3, 0).
        counter = counter + 1. 
      END. 
      ELSE 
      DO: 
        tot-debt = tot-debt + ROUND(age-list.tot-debt, 0).
        debt0 = debt0 + ROUND(age-list.debt0, 0). 
        debt1 = debt1 + ROUND(age-list.debt1, 0). 
        debt2 = debt2 + ROUND(age-list.debt2, 0). 
        debt3 = debt3 + ROUND(age-list.debt3, 0).
      END. 
      curr-liefnr = age-list.lief-nr. 
      curr-name = age-list.supplier. 
      delete age-list. 
  END. 
  IF counter GT 0 AND tot-debt NE 0 THEN 
  DO: 
      IF price-decimal EQ 0 THEN
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
             + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
      ELSE
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
      RUN fill-in-list. 
  END. 
 
  outlist = 
  "-------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list.

  IF price-decimal EQ 0 THEN
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 
  ELSE
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>,>>>,>>>,>>9.99").
  RUN fill-in-list. 

  outlist = "". 
  RUN fill-in-list. 
  outlist = STRING(translateExtended ("        Statistic Percentage (%) :",lvCAREA,""), "x(33)") 
    + "                      " 
    + "100.00" 
    + "             " 
    + STRING((t-debt0 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt1 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt2 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt3 / t-saldo * 100), "->>9.99"). 
  RUN fill-in-list. 
  outlist = "". 
  RUN fill-in-list. 
END.

PROCEDURE age-list3:
DEFINE VARIABLE billdate AS DATE. 
DEFINE VARIABLE counter AS INTEGER FORMAT ">>>9". 
DEFINE VARIABLE t-debet      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-credit     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-comm       AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-adjust     AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-saldo      AS DECIMAL FORMAT "->>,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt0      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt1      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt2      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE t-debt3      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INITIAL 0. 
DEFINE VARIABLE tmp-saldo    AS DECIMAL FORMAT "->>>>>>>>>>9" INITIAL 0. 
DEFINE VARIABLE curr-name    AS CHARACTER FORMAT "x(24)". 
DEFINE VARIABLE curr-liefnr  AS INTEGER. 
DEFINE VARIABLE supplier     AS CHARACTER FORMAT "x(34)". 
DEFINE VARIABLE debt0        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt1        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt2        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE debt3        AS DECIMAL FORMAT "->>,>>>,>>9". 
DEFINE VARIABLE tot-debt     AS DECIMAL FORMAT "->>>,>>>,>>9". 

DEFINE VARIABLE t-date  AS DATE.
 
DEFINE VARIABLE ap-saldo AS DECIMAL. 
DEFINE VARIABLE do-it    AS LOGICAL NO-UNDO.

DEFINE BUFFER debt FOR l-kredit. 
 
  /*MTCLOSE QUERY q1. */
  FOR EACH age-list: 
    delete age-list. 
  END. 
  FOR EACH output-list: 
    delete output-list. 
  END. 
 
/**** unpaid / partial paid A/P records *****/ 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date 
    AND l-kredit.opart EQ 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK
    BY l-lieferant.firma:
    
    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:
      FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
        AND queasy.char1 = l-kredit.NAME NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN
      DO:
         ap-saldo = l-kredit.netto. 
         IF l-kredit.counter NE 0 THEN 
         DO: 
           FOR EACH debt WHERE debt.opart = 1 AND debt.counter = l-kredit.counter 
             AND debt.zahlkonto NE 0 
             AND debt.rgdatum LE to-date NO-LOCK: 
             ap-saldo = ap-saldo + debt.saldo. 
           END. 
         END. 
         
         create age-list. 
         age-list.name     = l-kredit.name. 
         age-list.rgdatum  = queasy.date1. 
         age-list.counter  = l-kredit.counter. 
         age-list.lief-nr  = l-kredit.lief-nr. 
         age-list.tot-debt = ap-saldo. 
         age-list.supplier = TRIM(l-lieferant.firma + ", " + l-lieferant.anredefirma).
         age-list.adresse1 = l-lieferant.adresse1.
         age-list.telefon  = l-lieferant.adresse1. 
      END.
    END.
  END. 
 
/**** Full paid A/P records *****/      . 
  FOR EACH l-kredit WHERE l-kredit.rgdatum LE to-date AND l-kredit.opart EQ 2 
    AND l-kredit.zahlkonto = 0 NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr 
    AND l-lieferant.firma GE from-name AND l-lieferant.firma LE to-name NO-LOCK
    BY l-kredit.counter: 

    do-it = YES.
    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.

    IF do-it THEN
    DO:
       FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
        AND queasy.char1 = l-kredit.NAME NO-LOCK NO-ERROR.
       IF AVAILABLE queasy THEN
       DO:
           ap-saldo = l-kredit.netto. 
           FOR EACH debt WHERE debt.counter = l-kredit.counter AND debt.opart = 2 
             AND debt.zahlkonto NE 0 AND debt.rgdatum LE to-date NO-LOCK: 
             ap-saldo = ap-saldo + debt.saldo. 
           END.       
         
           create age-list. 
           age-list.name = l-kredit.name. 
           age-list.rgdatum = queasy.date1.
           age-list.counter = l-kredit.counter. 
           age-list.lief-nr = l-kredit.lief-nr. 
           age-list.tot-debt = ap-saldo. 
           age-list.supplier = l-lieferant.firma + ", " + l-lieferant.anredefirma.
           age-list.adresse1 = l-lieferant.adresse1.
           age-list.telefon  = l-lieferant.adresse1.
         /*END.*/
       END.
    END.
  END. 

  curr-liefnr = 0. 
  counter = 0. 
  FOR EACH age-list WHERE  age-list.tot-debt NE 0 BY age-list.supplier: 
    IF to-date - age-list.rgdatum GT day3 
      THEN age-list.debt3 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day2 
      THEN age-list.debt2 = age-list.tot-debt. 
    ELSE IF to-date - age-list.rgdatum GT day1 
      THEN age-list.debt1 = age-list.tot-debt. 
    ELSE age-list.debt0 = age-list.tot-debt. 
      
      t-saldo  = t-saldo + ROUND(age-list.tot-debt, 0).
      t-debt0  = t-debt0 + ROUND(age-list.debt0, 0).   
      t-debt1  = t-debt1 + ROUND(age-list.debt1, 0).   
      t-debt2  = t-debt2 + ROUND(age-list.debt2, 0).   
      t-debt3  = t-debt3 + ROUND(age-list.debt3, 0).   
      IF curr-liefnr = 0 THEN 
      DO: 
        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0).
        debt0 = ROUND(age-list.debt0, 0). 
        debt1 = ROUND(age-list.debt1, 0). 
        debt2 = ROUND(age-list.debt2, 0). 
        debt3 = ROUND(age-list.debt3, 0). 
        counter = counter + 1.  
      END. 
      ELSE IF curr-name NE age-list.supplier THEN 
      DO: 
        IF tot-debt NE 0 THEN
        DO:
          IF price-decimal EQ 0 THEN
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
               + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
               + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
          ELSE
            outlist = "  " + STRING(counter,">>>9") + "  " 
               + STRING(supplier, "x(34)") + "  " 
               + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
               + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
               + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
          
          RUN fill-in-list. 
        END.
        ELSE counter = counter - 1.

        supplier = age-list.supplier. 
        tot-debt = ROUND(age-list.tot-debt, 0). 
        debt0 = ROUND(age-list.debt0, 0).
        debt1 = ROUND(age-list.debt1, 0).
        debt2 = ROUND(age-list.debt2, 0).
        debt3 = ROUND(age-list.debt3, 0).
        counter = counter + 1.
      END. 
      ELSE 
      DO: 
        tot-debt = tot-debt + ROUND(age-list.tot-debt, 0).
        debt0 = debt0 + ROUND(age-list.debt0, 0). 
        debt1 = debt1 + ROUND(age-list.debt1, 0). 
        debt2 = debt2 + ROUND(age-list.debt2, 0). 
        debt3 = debt3 + ROUND(age-list.debt3, 0). 
      END. 
      curr-liefnr = age-list.lief-nr. 
      curr-name = age-list.supplier. 
      delete age-list. 
  END. 
  IF counter GT 0 AND tot-debt NE 0 THEN 
  DO: 
      IF price-decimal EQ 0 THEN
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->,>>>,>>>,>>>,>>9") +  "  " 
             + STRING(debt0, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt1, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt2, "->,>>>,>>>,>>>,>>9") + "  " 
             + STRING(debt3, "->,>>>,>>>,>>>,>>9") + "  ". 
      ELSE
        outlist = "  " + STRING(counter,">>>9") + "  " 
             + STRING(supplier, "x(34)") + "  " 
             + STRING(tot-debt, "->>,>>>,>>>,>>9.99") +  "  " 
             + STRING(debt0, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt1, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt2, "->>,>>>,>>>,>>9.99") + "  " 
             + STRING(debt3, "->>,>>>,>>>,>>9.99") + "  ". 
      RUN fill-in-list. 
  END. 
 
  outlist = 
  "-------------------------------------------------------------------------------------------------------------------------------------------------". 
  RUN fill-in-list. 

  IF price-decimal EQ 0 THEN
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt0, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt1, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt2, "->,>>>,>>>,>>>,>>9") + "  " 
      + STRING(t-debt3, "->,>>>,>>>,>>>,>>9"). 
  ELSE
    outlist = STRING(translateExtended ("           T O T A L  A/P:",lvCAREA,""), "x(26)") 
      + "                  " 
      + STRING(t-saldo, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt0, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt1, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt2, "->>,>>>,>>>,>>9.99") + "  " 
      + STRING(t-debt3, "->>,>>>,>>>,>>9.99").
  RUN fill-in-list. 

  outlist = "". 
  RUN fill-in-list. 
  outlist = STRING(translateExtended ("        Statistic Percentage (%) :",lvCAREA,""), "x(33)") 
    + "                      " 
    + "100.00" 
    + "             " 
    + STRING((t-debt0 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt1 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt2 / t-saldo * 100), "->>9.99") 
    + "             " 
    + STRING((t-debt3 / t-saldo * 100), "->>9.99"). 
  RUN fill-in-list. 
  outlist = "". 
  RUN fill-in-list.
END.
 
PROCEDURE fill-in-list: 
  create output-list. 
  output-list.str = outlist. 
END. 
