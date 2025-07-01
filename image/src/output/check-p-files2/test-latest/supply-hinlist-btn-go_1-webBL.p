/*31 Juli 2015 Eko, mengganti str-list menjadi TEMP-TABLE */
DEF TEMP-TABLE str-list
  FIELD artnr       AS INTEGER 
  FIELD lager-nr    AS INTEGER 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR 
  FIELD qty         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD warenwert   AS DECIMAL
  FIELD datum       AS DATE
  FIELD st          AS INTEGER
  FIELD supplier    AS CHARACTER
  FIELD article     AS INTEGER
  FIELD DESCRIPTION AS CHARACTER
  FIELD d-unit      AS CHARACTER
  FIELD price       AS DECIMAL
  FIELD inc-qty    AS DECIMAL
  FIELD amount      AS DECIMAL
  FIELD docu-no     AS CHARACTER
  FIELD deliv-no    AS CHARACTER
  FIELD ID          AS CHAR FORMAT "x(4)"  
  /*gst for penang*/
  FIELD gstid       AS CHAR
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS DECIMAL
  FIELD tot-amt     AS DECIMAL
  FIELD lief-nr     AS INTEGER
  /*geral for web*/
  FIELD fibu        AS CHAR
  FIELD fibu-bez    AS CHAR  
  /*ITA for request vietname */
  FIELD addvat-value    AS DECIMAL
  /* Bily Add Amount excl */
  FIELD amountexcl      AS DECIMAL
  FIELD invoice-nr  AS CHAR FORMAT "x(16)" INITIAL "" LABEL "Invoice No"
  /* Oscar (13/01/24) - 98F7A0 - add serial number and invoice-date in incoming report */
  FIELD serial-number AS CHARACTER
  FIELD invoice-date AS DATE
  /* Oscar (12/02/25) - DDB12D - add serial number and invoice-date in incoming report */
  FIELD remark-artikel AS CHARACTER
  /* Oscar (20/02/25) - A74530 - add AP Voucher Number to show */
  FIELD ap-voucher AS INTEGER
  FIELD disc-amount     AS DECIMAL
  FIELD addvat-amount   AS DECIMAL
  FIELD disc-amount2    AS DECIMAL
  FIELD vat-amount      AS DECIMAL
.

DEFINE TEMP-TABLE taxcode-list
  FIELD taxcode   AS CHAR
  FIELD taxamount AS DECIMAL.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER from-supp AS CHAR.
DEFINE INPUT  PARAMETER from-doc  AS CHAR.
DEFINE INPUT  PARAMETER sorttype  AS INT.
DEFINE INPUT  PARAMETER from-grp  AS INT.
DEFINE INPUT  PARAMETER to-grp    AS INT.
DEFINE INPUT  PARAMETER store     AS INT.
DEFINE INPUT  PARAMETER all-supp  AS LOGICAL.
DEFINE INPUT  PARAMETER all-doc   AS LOGICAL.
DEFINE INPUT  PARAMETER from-date AS DATE.
DEFINE INPUT  PARAMETER to-date   AS DATE.
DEFINE INPUT  PARAMETER TABLE FOR taxcode-list.
DEFINE OUTPUT PARAMETER err-code  AS INT INIT 0.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE supp-nr        AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE long-digit     AS LOGICAL NO-UNDO.
DEFINE VARIABLE tot-anz        AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-amount     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-amountexcl AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-tax        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-amt        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE tot-price      AS DECIMAL NO-UNDO. 
DEFINE VARIABLE counter        AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE loopi          AS INTEGER NO-UNDO.
DEFINE VARIABLE unit-price     AS DECIMAL.

DEFINE BUFFER buff-l-kredit FOR l-kredit.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "supply-hinlist".

IF from-supp NE "" THEN 
DO: 
  FIND FIRST l-lieferant WHERE l-lieferant.firma = from-supp NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-lieferant THEN 
  DO:
    err-code = 1.
    RETURN NO-APPLY.
  END. 
  ELSE supp-nr = l-lieferant.lief-nr.
END.

IF from-doc NE "" THEN 
DO:
  FIND FIRST l-ophis WHERE l-ophis.docu-nr = from-doc NO-LOCK NO-ERROR.
  IF NOT AVAILABLE l-ophis THEN 
  DO:
    err-code = 4.
    RETURN NO-APPLY.
  END. 
END.

IF sorttype = 1 THEN
DO:
  IF NOT all-supp AND from-supp EQ "" THEN 
  DO: 
    err-code = 2.
    RETURN NO-APPLY. 
  END. 
  
  IF all-supp /*AND sorttype = 1*/ THEN 
  DO:
    /*MT 200912 
    IF from-grp = 0 AND to-grp = 0 THEN RUN create-list1. /* all grup */
    ELSE 
    */
    RUN create-list11.
  END. 
  ELSE
  DO:
      IF supp-nr NE 0 THEN
      DO: 
        /*MT 200912 
        IF from-grp = 0 AND to-grp = 0 THEN RUN create-list2. /* all grup */
        ELSE 
        */
        RUN create-list22.
      END.
  END.
  /*
  ELSE IF all-supp AND sorttype = 2 THEN 
  DO: 
    IF from-grp = 0 THEN RUN create-list1a. 
    ELSE RUN create-list11a.
  END. 
  ELSE IF NOT all-supp AND sorttype = 1 THEN 
  DO: 
    IF from-grp = 0 THEN RUN create-list2. 
    ELSE RUN create-list22. 
  END. 
  ELSE IF NOT all-supp AND sorttype = 2 THEN 
  DO: 
    IF from-grp = 0 THEN RUN create-list2a. 
    ELSE RUN create-list22a. 
  END. */
END.

ELSE IF sorttype = 2 THEN
DO:
  IF NOT all-doc AND from-doc EQ "" THEN 
  DO: 
    err-code = 3.
    RETURN NO-APPLY. 
  END. 

  IF all-doc THEN
  DO:
    IF from-supp NE "" AND supp-nr NE 0 THEN 
    DO:
      IF from-grp EQ 0 THEN RUN create-list1as. 
      ELSE RUN create-list11as.
    END.
    ELSE 
    DO:
      IF from-grp EQ 0 THEN RUN create-list1a. 
      ELSE RUN create-list11a.
    END.
  END.
  ELSE
  DO:
    IF from-grp EQ 0 THEN RUN create-list1ar. 
    ELSE RUN create-list11ar.
  END.
END.

 
ELSE IF sorttype = 3 THEN
DO:
  IF NOT all-doc AND from-doc EQ "" THEN 
  DO: 
    /*err-code = 3.*/
    RETURN NO-APPLY. 
  END. 

  IF all-doc THEN
  DO:
    IF from-supp NE "" AND supp-nr NE 0 THEN DO:
      IF from-grp = 0 THEN RUN create-list1bs. 
      ELSE RUN create-list11bs.
    END.
    ELSE DO:
      IF from-grp = 0 THEN RUN create-list1b. 
      ELSE RUN create-list11b.
    END.
  END.
  ELSE
  DO:
    IF from-grp = 0 THEN RUN create-list1br. 
    ELSE RUN create-list11br.
  END.
END.

/* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
/* Oscar (22 November 2024) - B42772 - fix total ammount not shown on some filter */

PROCEDURE create-list1a: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price  AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 


PROCEDURE create-list1ar: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0. 
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list11: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0. 
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO: 
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich /*BY l-ophis.artnr*/:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lief-nr EQ 0 THEN lief-nr = l-lieferant.lief-nr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich /*BY l-ophis.artnr*/:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lief-nr EQ 0 THEN lief-nr = l-lieferant.lief-nr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 


PROCEDURE create-list11a: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:  
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list11ar: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.
  
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list22: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL NO.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.
  
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl - 23/09/24 */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.op-art EQ 1 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK 
      BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich /*BY l-ophis.artnr*/:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lief-nr EQ 0 THEN lief-nr = l-lieferant.lief-nr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END. 
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/  
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK
      BY l-lieferant.firma BY l-ophis.datum BY l-artikel.bezeich /*BY l-ophis.artnr*/:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lief-nr EQ 0 THEN lief-nr = l-lieferant.lief-nr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 


/*ITA 050314*/
PROCEDURE create-list1b: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END.

PROCEDURE create-list11b: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0. 
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
  
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list1br: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz     = 0.
  tot-price  = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list11br: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:  
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr GT 0 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND l-ophis.docu-nr EQ from-doc 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-ophis.lief-nr NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END.

PROCEDURE create-list1as: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price  AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr
      NO-LOCK
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr
      NO-LOCK
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list11as: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr 
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK 
      BY l-ophis.lscheinnr BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF lscheinnr EQ "" THEN lscheinnr = l-ophis.lscheinnr.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.

  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "T O T A L" 
        str-list.qty        = t-anz 
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE create-list1bs: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.
  
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END.

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END.

PROCEDURE create-list11bs: 
  DEFINE VARIABLE t-anz        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-amt        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-tax        AS DECIMAL   INITIAL 0. 
  DEFINE VARIABLE t-inv        AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE t-price      AS DECIMAL   INITIAL 0.
  DEFINE VARIABLE lief-nr      AS INTEGER   INITIAL 0.
  DEFINE VARIABLE lscheinnr    AS CHARACTER INITIAL "".
  DEFINE VARIABLE utt-bezeich  AS CHARACTER INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL   INITIAL 0. /* Bily Add Amount excl */
  DEFINE VARIABLE count-data   AS INTEGER   INITIAL 0.
  DEFINE VARIABLE show-total   AS LOGICAL   INITIAL YES.

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  DEFINE VARIABLE pure-bundle-unit-price AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz         = 0.
  tot-price       = 0.
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.

  IF store EQ 0 THEN 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
  ELSE 
  DO:
    FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
      AND l-ophis.datum LE to-date 
      AND l-ophis.lief-nr EQ l-lieferant.lief-nr  
      AND l-ophis.op-art EQ 1 
      AND l-ophis.anzahl NE 0 
      AND l-ophis.lager-nr EQ store 
      AND NOT (LENGTH(l-ophis.fibukonto) GT 8 
      AND SUBSTRING(l-ophis.fibukonto,length(l-ophis.fibukonto) - length("CANCELLED") + 1,length(l-ophis.fibukonto)) EQ "CANCELLED")   /*gerald for not include cancelled receiving 4B0C09*/
      NO-LOCK USE-INDEX lief-op-dat_ix, 
      FIRST l-artikel WHERE l-artikel.artnr EQ l-ophis.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 200912 */
      AND l-artikel.endkum LE to-grp      /*MT 200912 */
      NO-LOCK,
      FIRST l-untergrup WHERE l-untergrup.zwkum EQ l-artikel.zwkum NO-LOCK  /*ITA 050314*/
      BY l-untergrup.bezeich BY l-ophis.datum BY l-artikel.bezeich:
        count-data = count-data + 1.
        /* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
        IF utt-bezeich EQ "" THEN utt-bezeich = l-untergrup.bezeich.
        RUN processing-data-in-loop (sorttype, show-total, INPUT-OUTPUT lief-nr, INPUT-OUTPUT lscheinnr, INPUT-OUTPUT utt-bezeich,
                                    INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt,       
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT t-price,
                                    INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT amt).
    END.
  END.
 
  /* Oscar (02 Januari 2024) - 3EE885 - add validation to show total or hide and show total only when data is not blank */
  IF show-total THEN
  DO:
    IF count-data GT 0 THEN
    DO:
      CREATE str-list.

      ASSIGN
        str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
        str-list.qty        = t-anz
        str-list.inc-qty    = t-anz 
        str-list.amount     = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv 
        str-list.price      = 0.
    END.

    IF count-data GT 0 THEN
    DO:
    
      CREATE str-list. 
    
      CREATE str-list.
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL" 
        str-list.qty        = tot-anz 
        str-list.inc-qty    = tot-anz
        str-list.amount     = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt
        str-list.price      = 0. 

    END.
  END.
  ELSE
  DO:
    CREATE str-list. 
    
    CREATE str-list.
    ASSIGN
      str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt
      str-list.price      = 0. 
  END.
END. 

PROCEDURE convert-fibu: 
  DEFINE INPUT PARAMETER konto AS CHAR. 
  DEFINE OUTPUT PARAMETER s    AS CHAR INITIAL "". 
  DEFINE OUTPUT PARAMETER bez  AS CHAR INITIAL "".
  DEFINE VARIABLE ch AS CHAR. 
  DEFINE VARIABLE i  AS INTEGER. 
  DEFINE VARIABLE j  AS INTEGER. 
 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = konto NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN RETURN. 

  bez = gl-acct.bezeich.
 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 

/* Oscar (22 November 2024) - 46C113 - moving the proses in the loop to one function */
PROCEDURE processing-data-in-loop:
  DEFINE INPUT PARAMETER sorttype            AS INTEGER.
  DEFINE INPUT PARAMETER show-total          AS LOGICAL.
  DEFINE INPUT-OUTPUT PARAMETER lief-nr      AS INTEGER.
  DEFINE INPUT-OUTPUT PARAMETER lscheinnr    AS CHARACTER.
  DEFINE INPUT-OUTPUT PARAMETER utt-bezeich  AS CHARACTER.
  DEFINE INPUT-OUTPUT PARAMETER t-anz    AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-amt        AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-tax        AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-inv        AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-price  AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER amt          AS DECIMAL INITIAL 0.

  /* Oscar (22 November 2024) - 46C113 - uniform the data that being output like active */


  FIND FIRST l-ophhis WHERE l-ophhis.op-typ EQ "STI" AND l-ophhis.lscheinnr EQ l-ophis.lscheinnr AND l-ophhis.datum EQ l-ophis.datum NO-LOCK NO-ERROR.

  /* Oscar (22 November 2024) - 46C113 - add validation to show total or not */
  IF show-total THEN
  DO:

    /* Oscar (22 November 2024) - 46C113 - add validation to grouping based on what sorttype is used */
    /* Oscar (22/11/2024) - 46C113 - adding total for anz and price of delivery and mess */
    IF sorttype EQ 1 THEN
    DO: 
      IF lief-nr NE l-lieferant.lief-nr THEN 
      DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list.
        ASSIGN
          str-list.DESCRIPTION = "T O T A L"
          str-list.inc-qty    = t-anz
          str-list.qty        = t-anz
          str-list.amount     = t-amt
          str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
          str-list.tax-amount = t-tax
          str-list.tot-amt    = t-inv
          str-list.price      = 0
          
          t-anz         = 0 
          t-amt         = 0
          t-amountexcl  = 0 /* Bily Add Amount excl */
          t-tax         = 0
          t-inv         = 0
          t-price       = 0. 

        create str-list. 
      END. 
    END.
    ELSE IF sorttype EQ 2 THEN
    DO:
      IF lscheinnr NE l-ophis.lscheinnr THEN 
      DO: 
        lscheinnr = l-ophis.lscheinnr. 
        create str-list.
        ASSIGN
          str-list.DESCRIPTION = "T O T A L"
          str-list.inc-qty    = t-anz
          str-list.qty        = t-anz
          str-list.amount     = t-amt
          str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
          str-list.tax-amount = t-tax
          str-list.tot-amt    = t-inv
          str-list.price      = 0
          
          t-anz         = 0 
          t-amt         = 0
          t-amountexcl  = 0 /* Bily Add Amount excl */
          t-tax         = 0
          t-inv         = 0
          t-price       = 0. 
        create str-list. 
      END. 
    END.
    ELSE IF sorttype EQ 3 THEN
    DO:
      IF utt-bezeich NE l-untergrup.bezeich THEN 
      DO: 
        create str-list.
        ASSIGN
          str-list.DESCRIPTION = "TOTAL SUB-GROUP: " + utt-bezeich
          str-list.inc-qty    = t-anz
          str-list.qty        = t-anz
          str-list.amount     = t-amt
          str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
          str-list.tax-amount = t-tax
          str-list.tot-amt    = t-inv
          str-list.price      = 0
          
          t-anz         = 0 
          t-amt         = 0
          t-amountexcl  = 0 /* Bily Add Amount excl */
          t-tax         = 0
          t-inv         = 0
          t-price       = 0. 
        utt-bezeich = l-untergrup.bezeich. 
        create str-list. 
      END. 
    END.
  END.
  
  t-anz = t-anz + l-ophis.anzahl. 
  tot-anz = tot-anz + l-ophis.anzahl. 

  /* t-amt = t-amt + l-ophis.warenwert.
  t-amountexcl = t-amountexcl + l-ophis.warenwert. /* Bily Add Amount Excl */
  tot-anz = tot-anz + l-ophis.anzahl. 
  tot-amount = tot-amount + l-ophis.warenwert. 
  tot-amountexcl = tot-amountexcl + l-ophis.warenwert. /* Bily Add Amount Excl */ */

  /* Oscar (02/01/2025) - 3EE885 - complete this code from Mbak Ita for uniform output */
  FIND FIRST queasy WHERE queasy.KEY EQ 304 
    AND queasy.char1 EQ l-ophis.lscheinnr 
    AND queasy.number1 EQ l-ophis.artnr NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
      ASSIGN 
        t-amt = t-amt + (l-ophis.warenwert + (l-ophis.warenwert * (queasy.deci1 / 100)))
        tot-amount = tot-amount + (l-ophis.warenwert + (l-ophis.warenwert * (queasy.deci1 / 100)))
        t-amountexcl = t-amountexcl + l-ophis.warenwert
        tot-amountexcl = tot-amountexcl + l-ophis.warenwert. /* Bily Add Amount excl */
  ELSE 
      ASSIGN 
        t-amt = t-amt + l-ophis.warenwert
        tot-amount = tot-amount + l-ophis.warenwert
        t-amountexcl = t-amountexcl + l-ophis.warenwert
        tot-amountexcl = tot-amountexcl + l-ophis.warenwert. /* Bily Add Amount excl */

  FIND FIRST str-list WHERE str-list.docu-nr EQ l-ophis.docu-nr 
    AND str-list.artnr EQ l-ophis.artnr 
    AND str-list.lager-nr EQ l-ophis.lager-nr 
    AND str-list.lscheinnr EQ l-ophis.lscheinnr 
    AND str-list.epreis EQ l-ophis.einzelpreis NO-LOCK NO-ERROR. 
  
  IF AVAILABLE str-list THEN 
  DO: 
    /* str-list.qty          = str-list.qty + l-ophis.anzahl. 
    str-list.warenwert    = str-list.warenwert + l-ophis.warenwert. 
    str-list.inc-qty      = str-list.qty.
    str-list.amount       = str-list.warenwert.
    str-list.amountexcl   = str-list.amountexcl + l-ophis.warenwert. /* Bily Add Amount Excl */
    FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
    IF AVAILABLE taxcode-list THEN DO:
        ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                
                str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                t-inv   = t-inv + (l-ophis.warenwert + amt)
                tot-amt = tot-amt + (l-ophis.warenwert + amt).
    END. */

    str-list.qty = str-list.qty + l-ophis.anzahl.
    str-list.inc-qty = str-list.inc-qty + l-ophis.anzahl.

    /* Oscar (22/11/2024) - 46C113 - complete this code from Mbak Ita for uniform output */
    FIND FIRST queasy WHERE queasy.KEY EQ 304 
      AND queasy.char1 EQ l-ophis.lscheinnr 
      AND queasy.number1 EQ l-ophis.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        ASSIGN 
          str-list.addvat-value = queasy.deci1
          str-list.warenwert    = str-list.warenwert + (l-ophis.warenwert + (l-ophis.warenwert * (queasy.deci1 / 100)))
          str-list.amountexcl   = str-list.amountexcl + l-ophis.warenwert. /* Bily Add Amount excl */
    ELSE 
        ASSIGN 
          str-list.warenwert = str-list.warenwert + l-ophis.warenwert
          str-list.amountexcl = str-list.amountexcl + l-ophis.warenwert. /* Bily Add Amount excl */

    str-list.amount = str-list.warenwert.

    FIND FIRST taxcode-list WHERE taxcode-list.taxcode EQ str-list.tax-code NO-LOCK NO-ERROR.
    IF AVAILABLE taxcode-list THEN 
    DO:
      ASSIGN 
        amt                 = l-ophis.warenwert * taxcode-list.taxamount
        str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
        t-tax               = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
        tot-tax             = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
        
        str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
        t-inv            = t-inv + (l-ophis.warenwert + amt)
        tot-amt          = tot-amt + (l-ophis.warenwert + amt).
    END.

    /*FDL Jan 23, 2025: F26793*/
    FIND FIRST queasy WHERE queasy.KEY EQ 336 
        AND queasy.char1 EQ l-ophis.lscheinnr
        AND queasy.number2 EQ l-ophis.artnr
        AND DEC(queasy.char2) EQ l-ophis.einzelpreis NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            str-list.disc-amount = str-list.disc-amount + queasy.deci1 + queasy.deci2
            /*str-list.disc-amount2 = str-list.disc-amount2 + queasy.deci2*/
            str-list.vat-amount = str-list.vat-amount
            str-list.addvat-amount = str-list.addvat-amount + DEC(queasy.char3)
            .
    END.
  END. 
  ELSE 
  DO: 
    CREATE str-list.
    IF AVAILABLE l-ophhis THEN 
    DO: 
      str-list.invoice-nr = l-ophhis.fibukonto.
    END.

    str-list.lief-nr   = l-ophis.lief-nr.
    str-list.artnr     = l-ophis.artnr. 
    str-list.lager-nr  = l-ophis.lager-nr. 
    str-list.docu-nr   = l-ophis.docu-nr. 
    str-list.lscheinnr = l-ophis.lscheinnr. 

    str-list.epreis    = l-ophis.einzelpreis. 
    /* str-list.warenwert = l-ophis.warenwert.  */

    /* Oscar (20/02/25) - A74530 - add AP Voucher Number to show */
    FIND FIRST buff-l-kredit WHERE buff-l-kredit.lscheinnr EQ l-ophis.lscheinnr NO-LOCK NO-ERROR.
    IF AVAILABLE buff-l-kredit THEN
        str-list.ap-voucher = buff-l-kredit.rechnr.
    ELSE
        str-list.ap-voucher = 0.

    /*ITA Request vietnam*/
    FIND FIRST queasy WHERE queasy.KEY EQ 304 
      AND queasy.char1 EQ l-ophis.lscheinnr 
      AND queasy.number1 EQ l-ophis.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        ASSIGN 
            str-list.addvat-value = queasy.deci1
            str-list.warenwert    = l-ophis.warenwert + (l-ophis.warenwert * (queasy.deci1 / 100))
            str-list.amountexcl   = l-ophis.warenwert. /* Bily Add Amount excl */
    ELSE 
        ASSIGN 
            str-list.warenwert =  l-ophis.warenwert
            str-list.amountexcl = l-ophis.warenwert. /* Bily Add Amount excl */

    /* Oscar (14/01/24) - 98F7A0 - show additional information in incoming report */
    FIND FIRST queasy WHERE queasy.KEY EQ 335 AND queasy.char1 EQ l-ophis.lscheinnr
      AND queasy.number1 = l-ophis.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      str-list.serial-number = queasy.char2.
      str-list.invoice-date = queasy.date2.
    END.
    ELSE
    DO:
      str-list.serial-number = "".
      str-list.invoice-date = ?.
    END.

    /* Oscar (12/02/25) - DDB12D - show remark in incoming report */
    FIND FIRST queasy WHERE queasy.KEY EQ 340 
      AND queasy.char1 EQ l-ophis.lscheinnr
      AND queasy.number1 EQ l-ophis.artnr
      AND queasy.deci1 EQ l-ophis.einzelpreis NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
      str-list.remark-artikel = queasy.char2.
    END.
    ELSE
    DO:
      str-list.remark-artikel = "".
    END.

    /*FDL Jan 23, 2025: F26793*/
    FIND FIRST queasy WHERE queasy.KEY EQ 336 
        AND queasy.char1 EQ l-ophis.lscheinnr
        AND queasy.number2 EQ l-ophis.artnr
        AND DEC(queasy.char2) EQ l-ophis.einzelpreis NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            str-list.disc-amount = queasy.deci1 + queasy.deci2
            /*str-list.disc-amount2 = queasy.deci2*/
            str-list.vat-amount = queasy.deci3
            str-list.addvat-amount = DEC(queasy.char3)
            .
    END.

    RUN convert-fibu(l-ophis.fibukonto, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 

    ASSIGN
        str-list.datum        = l-ophis.datum
        str-list.st           = l-ophis.lager-nr
        str-list.article      = l-artikel.artnr
        str-list.DESCRIPTION  = l-artikel.bezeich

        str-list.d-unit       = l-artikel.traubensorte
        str-list.qty          = l-ophis.anzahl
        str-list.inc-qty      = l-ophis.anzahl

        str-list.amount       = l-ophis.warenwert
        str-list.supplier     = l-lieferant.firma
        str-list.tax-code     = l-artikel.lief-artnr[3].

    IF l-lieferant.plz NE " " THEN DO:
      IF l-lieferant.plz MATCHES "*#*" THEN DO:
        DO loopi = 1 TO NUM-ENTRIES(l-lieferant.plz,"#"):
          IF ENTRY(loopi + 1, l-lieferant.plz, "#") NE " "  THEN DO:
            ASSIGN str-list.gstid = ENTRY(loopi + 1, l-lieferant.plz, "#").
            LEAVE.
          END.                   
        END.
      END.
    END.
  
    FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
    IF AVAILABLE taxcode-list THEN 
    DO:
      ASSIGN 
        str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
        t-tax               = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
        tot-tax             = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
        
        str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
        t-inv            = t-inv + (l-ophis.warenwert + str-list.tax-amount)
        tot-amt          = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
    END.

    IF l-ophis.docu-nr EQ l-ophis.lscheinnr THEN
        str-list.docu-no = translateExtended ("Direct Purchase   ",lvCAREA,"").
    ELSE str-list.docu-no = l-ophis.docu-nr.

    ASSIGN
      str-list.deliv-no   = l-ophis.lscheinnr 
      str-list.price      = l-ophis.einzelpreis
      
      t-price    = t-price + str-list.price.
      tot-price  = tot-price + str-list.price.
    .
  END.
END.
