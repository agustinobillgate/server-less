DEFINE TEMP-TABLE str-list 
  FIELD h-recid     AS INTEGER INITIAL 0 
  FIELD l-recid     AS INTEGER INITIAL 0 
  FIELD lief-nr     AS INTEGER 
  FIELD billdate    AS DATE 
  FIELD artnr       AS INTEGER 
  FIELD lager-nr    AS INTEGER 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR INITIAL "" 
  FIELD invoice-nr  AS CHAR FORMAT "x(16)" INITIAL "" LABEL "Invoice No" 
  FIELD qty         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD DATE        AS DATE
  FIELD st          AS INTEGER
  FIELD supplier    AS CHARACTER
  FIELD article     AS INTEGER
  FIELD DESCRIPTION AS CHARACTER
  FIELD d-unit      AS CHARACTER
  FIELD price       AS DECIMAL
  FIELD inc-qty     AS DECIMAL
  FIELD amount      AS DECIMAL
  FIELD docu-no     AS CHARACTER
  FIELD deliv-note  AS CHARACTER
  FIELD ID          AS CHAR FORMAT "x(4)"
  FIELD fibu        LIKE l-op.stornogrund
  /*gst for penang*/
  FIELD gstid       AS CHAR
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS DECIMAL
  FIELD tot-amt     AS DECIMAL
  FIELD desc1       LIKE gl-acct.bezeich
  /*Geral for web*/
  FIELD fibu-bez    LIKE gl-acct.bezeich
  /*Agung for web*/
  FIELD pos         AS INTEGER

  /*ITA for request vietname */
  FIELD addvat-value    AS DECIMAL

  /* Bily Add Amount excl */
  FIELD amountexcl      AS DECIMAL
.  


DEFINE TEMP-TABLE taxcode-list
    FIELD taxcode   AS CHAR
    FIELD taxamount AS DECIMAL.

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER last-artnr         AS INT.
DEF INPUT  PARAMETER lieferant-recid    AS INT.
DEF INPUT  PARAMETER l-kredit-recid     AS INT.
DEF INPUT  PARAMETER ap-recid           AS INT.
DEF INPUT  PARAMETER long-digit         AS LOGICAL.
DEF INPUT  PARAMETER show-price         AS LOGICAL.
DEF INPUT  PARAMETER store              AS INT.
DEF INPUT  PARAMETER all-supp           AS LOGICAL.
DEF INPUT  PARAMETER sorttype           AS INT.
DEF INPUT  PARAMETER from-grp           AS INT.
DEF INPUT  PARAMETER to-grp             AS INT.
DEF INPUT  PARAMETER from-date          AS DATE.
DEF INPUT  PARAMETER to-date            AS DATE.
DEF INPUT  PARAMETER TABLE FOR taxcode-list.

DEF OUTPUT PARAMETER first-artnr  AS INT.
DEF OUTPUT PARAMETER curr-artnr   AS INT.
DEF OUTPUT PARAMETER last-artnr1  AS INT.
DEF OUTPUT PARAMETER unit-price         AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR str-list.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "supply-inlist".

DEFINE VARIABLE tot-anz    AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL.
DEFINE VARIABLE tot-amountexcl AS DECIMAL.
DEFINE VARIABLE tot-tax    AS DECIMAL. 
DEFINE VARIABLE tot-amt    AS DECIMAL. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE counter AS INTEGER  NO-UNDO INIT 0.
DEFINE VARIABLE loopi   AS INTEGER  NO-UNDO.

FIND FIRST l-lieferant WHERE RECID(l-lieferant) = lieferant-recid NO-ERROR.
FIND FIRST l-kredit WHERE RECID(l-kredit) = l-kredit-recid NO-ERROR.


  IF all-supp AND sorttype = 1 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list1. 
    ELSE
    */ 
    RUN create-list11. 
  END. 
  ELSE IF NOT all-supp AND sorttype = 1 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list2. 
    ELSE
    */ 

    RUN create-list22.
  END. 
 
  ELSE IF all-supp AND sorttype = 2 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list1a. 
    ELSE
    */ 
    RUN create-list11a.
  END. 
  ELSE IF NOT all-supp AND sorttype = 2 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list2a. 
    ELSE
    */ 
    RUN create-list22a.
  END. 
 
  ELSE IF all-supp AND sorttype = 3 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list1b. 
    ELSE
    */ 
    RUN create-list11b.
  END. 
  ELSE IF NOT all-supp AND sorttype = 3 THEN 
  DO: 
    /*MT 20/09/12
    IF from-grp = 0 THEN RUN create-list2b. 
    ELSE
    */ 
    RUN create-list22b. 
  END. 


PROCEDURE create-list11: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0.
DEFINE VARIABLE t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz         = 0. 
  tot-amount      = 0.
  tot-amountexcl  = 0. /* Bily Add Amount excl */
  tot-tax         = 0.
  tot-amt         = 0.
 
  IF store = 0 THEN 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.lief-nr GT 0 
      /*  AND l-op.loeschflag = 0 */ 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.op-art = 1 
      /*    AND l-op.warenwert NE 0  */ 
      NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
      BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich: 
      RUN assign-create-list11(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT t-tax,
                               INPUT-OUTPUT t-inv, INPUT-OUTPUT lief-nr).
  END. 
  
  ELSE 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.lief-nr GT 0 
      /*  AND l-op.loeschflag = 0 */ 
      AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
      AND l-op.op-art = 1 
      /*    AND l-op.warenwert NE 0  */ 
      AND l-op.lager-nr = store 
      NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
      BY l-lieferant.firma BY l-op.datum BY l-artikel.bezeich:
      RUN assign-create-list11(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT t-tax,
                               INPUT-OUTPUT t-inv, INPUT-OUTPUT lief-nr).
  END. 
  RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT t-tax,
                               INPUT-OUTPUT t-inv).
  create str-list.
  ASSIGN
    str-list.DESCRIPTION = "T O T A L" 
    str-list.qty        = t-anz 
    str-list.inc-qty    = t-anz 
    str-list.amount     = t-amt
    str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv. 
  create str-list. 
 
  create str-list.
  ASSIGN
    str-list.DESCRIPTION = "GRAND TOTAL" 
    str-list.qty        = tot-anz 
    str-list.inc-qty    = tot-anz
    str-list.amount     = tot-amount
    str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = tot-tax
    str-list.tot-amt    = tot-amt. 
END.

PROCEDURE assign-create-list11:
DEFINE INPUT-OUTPUT PARAMETER t-anz         AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-amt         AS DECIMAL INITIAL 0.
DEFINE INPUT-OUTPUT PARAMETER t-amountexcl  AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
DEFINE INPUT-OUTPUT PARAMETER t-tax         AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-inv         AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER lief-nr       AS INTEGER INITIAL 0. 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
      = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 
 
    IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
    IF lief-nr NE l-lieferant.lief-nr THEN 
    DO: 
        lief-nr = l-lieferant.lief-nr. 
        create str-list. 
        ASSIGN
          str-list.DESCRIPTION = "T O T A L" 
          str-list.qty        = t-anz 
          str-list.inc-qty    = t-anz 
          str-list.amount     = t-amt
          str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
          str-list.tax-amount = t-tax
          str-list.tot-amt    = t-inv
          
          t-anz         = 0 
          t-amt         = 0
          t-amountexcl  = 0 /* Bily Add Amount excl */
          t-tax         = 0
          t-inv         = 0. 
        create str-list. 
    END. 
    t-anz = t-anz + l-op.anzahl. 
    IF show-price THEN DO: 
        /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN t-amt = t-amt + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     tot-amount = tot-amount + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     t-amountexcl = t-amountexcl + l-op.warenwert
                     tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
          ELSE ASSIGN t-amt = t-amt + l-op.warenwert
                      tot-amount = tot-amount + l-op.warenwert
                      t-amountexcl = t-amountexcl + l-op.warenwert
                      tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
    END.
    tot-anz = tot-anz + l-op.anzahl. 
    /*IF show-price THEN tot-amount = tot-amount + l-op.warenwert. */
    IF show-price THEN unit-price = l-op.einzelpreis. 
    FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
      AND str-list.artnr = l-op.artnr 
      AND str-list.lager-nr = l-op.lager-nr 
      AND str-list.lscheinnr = l-op.lscheinnr 
      AND str-list.epreis = l-op.einzelpreis NO-LOCK NO-ERROR. 
    IF AVAILABLE str-list THEN 
    DO: 
      str-list.qty = str-list.qty + l-op.anzahl.
      IF show-price THEN DO:
          /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN str-list.addvat-value = queasy.deci1
                     str-list.warenwert    = str-list.warenwert + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     str-list.amountexcl   = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
          ELSE ASSIGN str-list.warenwert = str-list.warenwert + l-op.warenwert
                     str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
      END.
        
      ASSIGN
        str-list.inc-qty = str-list.qty  
        str-list.amount = str-list.warenwert. 

      FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                 str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                 t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                 t-inv   = t-inv + (l-op.warenwert + amt)
                 tot-amt = tot-amt + (l-op.warenwert + amt).
      END.
    END. 
    ELSE 
    DO: 
      CREATE str-list. 
      RUN add-id.
      IF AVAILABLE l-ophdr THEN 
      DO: 
        str-list.invoice-nr = l-ophdr.fibukonto. 
        str-list.h-recid = RECID(l-ophdr). 
      END. 
      str-list.l-recid      = RECID(l-op). 
      str-list.lief-nr      = l-op.lief-nr. 
      str-list.billdate     = l-op.datum. 
      str-list.artnr        = l-op.artnr. 
      str-list.lager-nr     = l-op.lager-nr. 
      str-list.docu-nr      = l-op.docu-nr. 
      str-list.lscheinnr    = l-op.lscheinnr. 
      str-list.qty          = l-op.anzahl. 
      str-list.epreis       = l-op.einzelpreis. 
      str-list.pos          = l-op.pos.

      IF show-price THEN DO:
          /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN str-list.addvat-value = queasy.deci1
                     str-list.warenwert    = l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100))
                     str-list.amountexcl   = l-op.warenwert. /* Bily Add Amount excl */
          ELSE ASSIGN str-list.warenwert =  l-op.warenwert
                     str-list.amountexcl = l-op.warenwert. /* Bily Add Amount excl */
      END.

      RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
        
      ASSIGN
        str-list.DATE = l-op.datum 
        str-list.st = l-op.lager-nr 
        str-list.article = l-artikel.artnr
        str-list.DESCRIPTION = l-artikel.bezeich
        str-list.d-unit = l-artikel.traubensort 
        str-list.inc-qty = l-op.anzahl 
        str-list.amount = str-list.warenwert
        str-list.supplier = l-lieferant.firma
        str-list.tax-code = l-artikel.lief-artnr[3]. 

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
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                 t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                 t-inv   = t-inv + (l-op.warenwert + str-list.tax-amount)
                 tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
      END.

 
      IF l-op.docu-nr = l-op.lscheinnr THEN 
        str-list.docu-no = translateExtended ("Direct Purchase   ",lvCAREA,""). 
      ELSE  str-list.docu-no = l-op.docu-nr. 
   
      ASSIGN
        str-list.deliv-note = l-op.lscheinnr 
        str-list.price = unit-price.
    END. 
END.
 
PROCEDURE create-list11a: 
  DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
  DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
  DEFINE VARIABLE lscheinnr AS CHAR INITIAL "".
  DEFINE VARIABLE t-amountexcl  AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
  
    /*MTstatus default "Processing...".*/ 
    FOR EACH str-list: 
      delete str-list. 
    END.
  
    tot-anz    = 0. 
    tot-amount = 0.
    tot-amountexcl = 0. /* Bily Add Amount excl */
    tot-tax    = 0.
    tot-amt    = 0.
   
    IF store = 0 THEN 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.lief-nr GT 0 
        /*  AND l-op.loeschflag = 0 */ 
        AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
        AND l-op.op-art = 1 
        /*    AND l-op.warenwert NE 0  */ 
        NO-LOCK USE-INDEX lief_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
        AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
        NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
        BY l-op.datum BY l-op.lscheinnr BY l-artikel.bezeich:
        RUN assign-create-list11a(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                  INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                  INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
    END. 
   
    ELSE 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.lief-nr GT 0 
        /*  AND l-op.loeschflag = 0 */ 
        AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
        AND l-op.op-art = 1 
        /*    AND l-op.warenwert NE 0  */ 
        AND l-op.lager-nr = store 
        NO-LOCK USE-INDEX lief_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
        AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
        NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
        BY l-op.datum BY l-op.lscheinnr BY l-artikel.bezeich: 
        RUN assign-create-list11a(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                  INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                  INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
    END. 
    RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-tax,
                       INPUT-OUTPUT t-inv, INPUT-OUTPUT t-amountexcl). 
  
    create str-list.
    ASSIGN
      str-list.DESCRIPTION = "T O T A L" 
      str-list.qty        = t-anz 
      str-list.inc-qty    = t-anz 
      str-list.amount     = t-amt
      str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = t-tax
      str-list.tot-amt    = t-inv. 
    create str-list. 
   
    create str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt. 
  
  END.
  
  PROCEDURE assign-create-list11a:
  DEFINE INPUT-OUTPUT PARAMETER t-anz     AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-amt     AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-tax     AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-inv     AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
  DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */

  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  
      FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
        = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-op.lscheinnr. 
      IF lscheinnr NE l-op.lscheinnr THEN 
      DO: 
          lscheinnr = l-op.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = "T O T A L" 
            str-list.qty        = t-anz 
            str-list.inc-qty    = t-anz 
            str-list.amount     = t-amt
            str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv

            t-anz = 0 
            t-amt = 0
            t-amountexcl = 0 /* Bily Add Amount excl */
            t-tax = 0
            t-inv = 0. 
          create str-list. 
      END. 
      t-anz = t-anz + l-op.anzahl. 
      /*IF show-price THEN t-amt = t-amt + l-op.warenwert. */
  
       IF show-price THEN DO: 
          /*ITA Request vietnam*/
            FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                  AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN t-amt = t-amt + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                       tot-amount = tot-amount + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                       t-amountexcl = t-amountexcl + l-op.warenwert
                       tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
            ELSE ASSIGN t-amt = t-amt + l-op.warenwert
                        tot-amount = tot-amount + l-op.warenwert
                        t-amountexcl = t-amountexcl + l-op.warenwert
                      tot-amountexcl = tot-amountexcl + l-op.warenwert. 
      END.
  
      tot-anz = tot-anz + l-op.anzahl. 
      /*IF show-price THEN tot-amount = tot-amount + l-op.warenwert. */
      IF show-price THEN unit-price = l-op.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
        AND str-list.artnr = l-op.artnr 
        AND str-list.lager-nr = l-op.lager-nr 
        AND str-list.lscheinnr = l-op.lscheinnr 
        AND str-list.epreis = l-op.einzelpreis 
        AND str-list.billdate = l-op.datum NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-op.anzahl. 
  
        IF show-price THEN DO:
            /*ITA Request vietnam*/
            FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                  AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN str-list.addvat-value = queasy.deci1
                       str-list.warenwert     = str-list.warenwert + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                       str-list.amountexcl   = str-list.amountexcl + l-op.warenwert.
            ELSE ASSIGN str-list.warenwert = str-list.warenwert + l-op.warenwert
                       str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
        END.
  
        ASSIGN
          str-list.inc-qty = str-list.qty
          str-list.amount = str-list.warenwert
          str-list.amountexcl = str-list.amountexcl. /* Bily Add Amount excl */
  
        FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
        IF AVAILABLE taxcode-list THEN DO:
            ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                   str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                   t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                   tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                   
                   str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                   t-inv   = t-inv + (l-op.warenwert + amt)
                   tot-amt = tot-amt + (l-op.warenwert + amt).
        END.
      END. 
      ELSE 
      DO: 
        create str-list. 
        RUN add-id.
        IF AVAILABLE l-ophdr THEN 
        DO: 
          str-list.invoice-nr = l-ophdr.fibukonto. 
          str-list.h-recid = RECID(l-ophdr). 
        END. 
        str-list.l-recid = RECID(l-op). 
        str-list.lief-nr = l-op.lief-nr. 
        str-list.billdate = l-op.datum. 
        str-list.artnr = l-op.artnr. 
        str-list.lager-nr = l-op.lager-nr. 
        str-list.docu-nr = l-op.docu-nr. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.qty = l-op.anzahl. 
        str-list.epreis = l-op.einzelpreis. 
        str-list.pos          = l-op.pos.
       
        IF show-price THEN DO:
            /*ITA Request vietnam*/
            FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                  AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN str-list.addvat-value = queasy.deci1
                       str-list.warenwert    = l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100))
                       str-list.amountexcl   = l-op.warenwert.
            ELSE ASSIGN str-list.warenwert =  l-op.warenwert
                        str-list.amountexcl = l-op.warenwert. /* Bily Add Amount excl */
        END.
  
        RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
      
        ASSIGN
          str-list.DATE = l-op.datum 
          str-list.st = l-op.lager-nr 
          str-list.article = l-artikel.artnr
          str-list.DESCRIPTION = l-artikel.bezeich
          str-list.d-unit = l-artikel.traubensort 
          str-list.inc-qty = l-op.anzahl
          str-list.amount = str-list.warenwert
          str-list.amountexcl = str-list.amountexcl
          str-list.supplier = l-lieferant.firma
          str-list.tax-code = l-artikel.lief-artnr[3].
  
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
        IF AVAILABLE taxcode-list THEN DO:
            ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                   t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                   tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                   
                   str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                   t-inv   = t-inv + (l-op.warenwert + str-list.tax-amount)
                   tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
        END.
   
        IF l-op.docu-nr = l-op.lscheinnr THEN 
          str-list.docu-no = translateExtended ("Direct Purchase   ",lvCAREA,""). 
        ELSE  str-list.docu-no = l-op.docu-nr. 
     
        ASSIGN
          str-list.deliv-note = l-op.lscheinnr 
          str-list.price = unit-price.
     END. 
  END.  
 
  PROCEDURE create-list11b: 
    DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-tax     AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-inv     AS DECIMAL INITIAL 0.
    DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
    DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "".
    DEFINE VARIABLE t-amountexcl  AS DECIMAL INITIAL 0. /* Bily Add Amount excl */ 
    
      /*MTstatus default "Processing...".*/ 
      FOR EACH str-list: 
        DELETE str-list. 
      END. 
     
      tot-anz = 0. 
      tot-amount = 0.
      tot-amountexcl = 0. /* Bily Add Amount excl */
      tot-tax    = 0.
      tot-tax    = 0.
      tot-amt    = 0.
     
      IF store = 0 THEN 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.lief-nr GT 0 AND l-op.loeschflag LE 1 
          AND l-op.op-art = 1 NO-LOCK USE-INDEX lief_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
          AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
          NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
          BY l-untergrup.bezeich BY l-artikel.bezeich BY l-op.datum: 
          RUN assign-create-list11b(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                    INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
      END. 
     
      ELSE 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.lief-nr GT 0 AND l-op.loeschflag LE 1 
          AND l-op.op-art = 1 AND l-op.lager-nr = store NO-LOCK USE-INDEX lief_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
          AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
          NO-LOCK, 
          FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK, 
          FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
          BY l-untergrup.bezeich BY l-op.datum BY l-artikel.bezeich:
          RUN assign-create-list11b(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                    INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                    INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
      END. 
      RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-tax,
                         INPUT-OUTPUT t-inv, INPUT-OUTPUT t-amountexcl).  
      
      create str-list.
      ASSIGN
        str-list.DESCRIPTION = lscheinnr 
        str-list.qty = t-anz 
        str-list.inc-qty = t-anz
        str-list.amount  = t-amt 
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv
        str-list.supplier = "T O T A L". 
     
      create str-list. 
     
      create str-list. 
      ASSIGN
        str-list.DESCRIPTION = "GRAND TOTAL"
        str-list.qty = tot-anz 
        str-list.inc-qty = tot-anz 
        str-list.amount  = tot-amount
        str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = tot-tax
        str-list.tot-amt    = tot-amt. 
    
    END. 
    PROCEDURE assign-create-list11b:
    DEFINE INPUT-OUTPUT PARAMETER t-anz     AS DECIMAL INITIAL 0. 
    DEFINE INPUT-OUTPUT PARAMETER t-amt     AS DECIMAL INITIAL 0.
    DEFINE INPUT-OUTPUT PARAMETER t-tax     AS DECIMAL INITIAL 0. 
    DEFINE INPUT-OUTPUT PARAMETER t-inv     AS DECIMAL INITIAL 0. 
    DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
    DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
    
    DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
    
        FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
          = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 
     
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO:   
            create str-list.
            ASSIGN
              str-list.DESCRIPTION = lscheinnr 
              str-list.qty = t-anz 
              str-list.inc-qty = t-anz
              str-list.amount  = t-amt
              str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
              str-list.supplier = "T O T A L"
              str-list.tax-amount = t-tax
              str-list.tot-amt    = t-inv. 
    
          lscheinnr = l-untergrup.bezeich. 
     
          t-anz = 0. 
          t-amt = 0.
          t-amountexcl = 0. /* Bily Add Amount excl */
          t-tax = 0.
          t-inv = 0.
    
          create str-list. 
        END. 
     
        t-anz = t-anz + l-op.anzahl. 
        /*IF show-price THEN t-amt = t-amt + l-op.warenwert. */
    
         IF show-price THEN DO: 
            /*ITA Request vietnam*/
              FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                    AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN
                  ASSIGN t-amt = t-amt + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                         tot-amount = tot-amount + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                         t-amountexcl = t-amountexcl + l-op.warenwert
                        tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
              ELSE ASSIGN t-amt = t-amt + l-op.warenwert
                          tot-amount = tot-amount + l-op.warenwert
                          t-amountexcl = t-amountexcl + l-op.warenwert
                          tot-amountexcl = tot-amountexcl + l-op.warenwert.  
        END.
    
        tot-anz = tot-anz + l-op.anzahl. 
        /*IF show-price THEN tot-amount = tot-amount + l-op.warenwert. */
        IF show-price THEN unit-price = l-op.einzelpreis. 
     
        FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
          AND str-list.lscheinnr = l-op.lscheinnr 
          AND str-list.lager-nr = l-op.lager-nr 
          AND str-list.artnr = l-op.artnr 
          AND str-list.epreis = l-op.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
            str-list.qty = str-list.qty + l-op.anzahl. 
    
    
            IF show-price THEN DO:
              /*ITA Request vietnam*/
              FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                    AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN
                  ASSIGN str-list.addvat-value = queasy.deci1
                         str-list.warenwert    = str-list.warenwert + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                         str-list.amountexcl   = str-list.amountexcl + l-op.warenwert.
              ELSE ASSIGN str-list.warenwert = str-list.warenwert + l-op.warenwert
                         str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
            END.
    
            ASSIGN
              str-list.inc-qty = str-list.qty
              str-list.amount = str-list.warenwert
              str-list.amountexcl = str-list.amountexcl. /* Bily Add Amount excl */ 
    
          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                     t-inv   = t-inv + (l-op.warenwert + amt)
                     tot-amt = tot-amt + (l-op.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          RUN add-id.
          IF AVAILABLE l-ophdr THEN 
          DO: 
            str-list.invoice-nr = l-ophdr.fibukonto. 
            str-list.h-recid = RECID(l-ophdr). 
          END. 
          str-list.l-recid = RECID(l-op). 
          str-list.lief-nr = l-op.lief-nr. 
          str-list.billdate = l-op.datum. 
          str-list.artnr = l-op.artnr. 
          str-list.lager-nr = l-op.lager-nr. 
          str-list.docu-nr = l-op.docu-nr. 
          str-list.lscheinnr = l-op.lscheinnr. 
          str-list.qty = l-op.anzahl. 
          str-list.epreis = l-op.einzelpreis. 
          str-list.pos          = l-op.pos.
    
          IF show-price THEN DO:
              /*ITA Request vietnam*/
              FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                    AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE queasy THEN
                  ASSIGN str-list.addvat-value = queasy.deci1
                         str-list.warenwert    = (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                         str-list.amountexcl   = l-op.warenwert.
              ELSE ASSIGN str-list.warenwert = l-op.warenwert
              str-list.amountexcl = l-op.warenwert. /* Bily Add Amount excl */
          END.
    
          RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
         
          ASSIGN
            str-list.DATE = l-op.datum
            str-list.st = l-op.lager-nr 
            str-list.article = l-artikel.artnr
            str-list.DESCRIPTION = l-artikel.bezeich
            str-list.d-unit = l-artikel.traubensort 
            str-list.inc-qty = l-op.anzahl
            str-list.amount = str-list.warenwert
            str-list.amountexcl = str-list.amountexcl 
            str-list.supplier = l-lieferant.firma
            str-list.tax-code = l-artikel.lief-artnr[3].
    
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-op.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
          END.
     
          IF l-op.docu-nr = l-op.lscheinnr THEN 
            str-list.docu-no = translateExtended ("Direct Purchase   ",lvCAREA,""). 
          ELSE  str-list.docu-no = l-op.docu-nr. 
       
          ASSIGN
            str-list.deliv-note = l-op.lscheinnr 
            str-list.price = unit-price.
        END. 
    END.
    
    


PROCEDURE create-hislist:
DEF INPUT-OUTPUT PARAM t-anz         AS DECIMAL.
DEF INPUT-OUTPUT PARAM t-amt         AS DECIMAL.
DEF INPUT-OUTPUT PARAM t-amountexcl  AS DECIMAL. /* Bily Add Amount excl */
DEF INPUT-OUTPUT PARAM t-tax         AS DECIMAL.
DEF INPUT-OUTPUT PARAM t-inv         AS DECIMAL.

DEF VAR close-date  AS DATE NO-UNDO.
DEF VAR close-date2 AS DATE NO-UNDO.

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK NO-ERROR.
           close-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 221 NO-LOCK NO-ERROR.
           close-date2 = htparam.fdate.

  IF ap-recid = 0 THEN RETURN.
  IF from-date NE to-date THEN RETURN.

/*  
  cari close-date  dari close-date-inv1.
  cari close-date2 dari close-date-inv1.
*/  
  IF close-date LT close-date2 THEN close-date = close-date2.
  close-date = DATE(MONTH(close-date), 1, YEAR(close-date)).
  IF to-date GE close-date THEN RETURN.

  FOR EACH l-ophis NO-LOCK WHERE 
      l-ophis.docu-nr EQ l-kredit.NAME AND
      l-ophis.lscheinnr EQ l-kredit.lscheinnr AND
      l-ophis.op-art = 1 AND
      l-ophis.datum = to-date:

      ASSIGN
          t-anz = t-anz + l-ophis.anzahl
          t-amt = t-amt + l-ophis.warenwert
      .

      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr NO-LOCK.
      FIND FIRST l-artikel   WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK.
      FIND FIRST l-ophhis    WHERE l-ophhis.op-typ = "STI" 
          AND l-ophhis.lscheinnr = l-ophis.lscheinnr 
          AND l-ophhis.datum = l-ophis.datum NO-LOCK NO-ERROR. 

      CREATE str-list. 
      IF AVAILABLE l-ophhis THEN 
      DO: 
        str-list.invoice-nr = l-ophhis.fibukonto. 
        str-list.h-recid = 0. 
      END. 
      ASSIGN
        str-list.l-recid        = 0
        str-list.lief-nr        = l-ophis.lief-nr
        str-list.billdate       = l-ophis.datum
        str-list.artnr          = l-ophis.artnr 
        str-list.lager-nr       = l-ophis.lager-nr 
        str-list.docu-nr        = l-ophis.docu-nr 
        str-list.lscheinnr      = l-ophis.lscheinnr 
        str-list.qty            = l-ophis.anzahl
        str-list.epreis         = l-ophis.einzelpreis 
        str-list.warenwert      = l-ophis.warenwert
        str-list.DATE           = l-ophis.datum
        str-list.st             = l-ophis.lager-nr 
        str-list.article        = l-artikel.artnr 
        str-list.DESCRIPTION    = l-artikel.bezeich
        str-list.d-unit         = l-artikel.traubensort
        str-list.inc-qty        = l-ophis.anzahl
        str-list.amount         = str-list.warenwert
        str-list.amountexcl     = l-ophis.warenwert /* Bily Add Amount excl */
        str-list.supplier       = l-lieferant.firma
        str-list.tax-code       = l-artikel.lief-artnr[3]. 

        FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
        IF AVAILABLE taxcode-list THEN DO:
            ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                   t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                   
                   str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                   t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount).
        END.

      IF l-ophis.docu-nr = l-ophis.lscheinnr THEN 
        str-list.docu-no        = "Direct Purchase". 
      ELSE str-list.docu-no     = l-ophis.docu-nr.
      
      ASSIGN
        str-list.deliv-note     = l-ophis.lscheinnr
        str-list.price          = unit-price. 

      RUN convert-fibu(l-ophis.fibukonto, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
    END. 
END.

PROCEDURE create-list22: 
  DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE lscheinnr AS CHAR INITIAL " ".
  DEFINE VARIABLE t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */

  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0.
  tot-amountexcl = 0. /* Bily Add Amount excl - 23/09/24 */
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.lief-nr = l-lieferant.lief-nr 
      AND l-op.loeschflag LE 1 /* AND l-op.warenwert NE 0 */ 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK BY l-op.datum BY l-artikel.bezeich:

      RUN assign-create-list22(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl,
                               INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT lscheinnr).
  END. 
 
  ELSE 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
      AND l-op.lief-nr = l-lieferant.lief-nr 
      AND l-op.loeschflag LE 1 /* AND l-op.warenwert NE 0 */ 
      AND l-op.lager-nr = store 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK BY l-op.datum BY l-artikel.bezeich:

      RUN assign-create-list22(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl,
                               INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT lscheinnr).
  END. 
  RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT t-tax,
                     INPUT-OUTPUT t-inv).

  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = "T O T A L" 
    str-list.qty        = t-anz 
    str-list.inc-qty    = t-anz 
    str-list.amount     = t-amt
    str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv. 
  create str-list. 

  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = "GRAND TOTAL" 
    str-list.qty = tot-anz  
    str-list.inc-qty = tot-anz 
    str-list.amount = tot-amount
    str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = tot-tax
    str-list.tot-amt    = tot-amt. 
END.

PROCEDURE assign-create-list22:
DEFINE INPUT-OUTPUT PARAMETER t-anz     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-amt     AS DECIMAL INITIAL 0.
DEFINE INPUT-OUTPUT PARAMETER t-tax     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-inv     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
      = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 

    IF lscheinnr = "" THEN lscheinnr = l-op.lscheinnr.

    IF lscheinnr NE l-op.lscheinnr THEN 
    DO: 
      lscheinnr = l-op.lscheinnr. 
      create str-list.
      ASSIGN
        str-list.DESCRIPTION = "T O T A L"
        str-list.qty         = t-anz 
        str-list.inc-qty     = t-anz
        str-list.amount      = t-amt
        str-list.amountexcl  = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount  = t-tax
        str-list.tot-amt     = t-inv. 

      t-anz = 0. 
      t-amt = 0.
      t-amountexcl = 0. /* Bily Add Amount excl */
      t-tax = 0.
      t-inv = 0.

      create str-list. 
    END. 
 
    tot-anz = tot-anz + l-op.anzahl. 
    tot-amount = tot-amount + l-op.warenwert.
    tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
    /* Perlu ditambahi dengan amount excl? Bily*/
    IF show-price THEN unit-price = l-op.einzelpreis. 
    FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
      AND str-list.artnr = l-op.artnr 
      AND str-list.lager-nr = l-op.lager-nr 
      AND str-list.lscheinnr = l-op.lscheinnr 
      AND str-list.epreis = l-op.einzelpreis NO-LOCK NO-ERROR. 
    IF AVAILABLE str-list THEN 
    DO: 
      str-list.qty = str-list.qty + l-op.anzahl. 
      /*IF show-price THEN str-list.warenwert = str-list.warenwert + l-op.warenwert. */

      IF show-price THEN DO:
          /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN str-list.addvat-value = queasy.deci1
                     str-list.warenwert    = str-list.warenwert + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     str-list.amountexcl   = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
          ELSE ASSIGN str-list.warenwert = str-list.warenwert + l-op.warenwert
                     str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
      END.

      str-list.inc-qty = str-list.qty. 
      str-list.amount = str-list.warenwert.

      FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                 str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                 tot-amt = tot-amt + (l-op.warenwert + amt).
      END.
    END. 
    ELSE 
    DO: 
      create str-list. 
      RUN add-id.
      IF AVAILABLE l-ophdr THEN 
      DO: 
        str-list.invoice-nr = l-ophdr.fibukonto. 
        str-list.h-recid = RECID(l-ophdr). 
      END. 
      str-list.l-recid = RECID(l-op). 
      str-list.lief-nr = l-op.lief-nr. 
      str-list.billdate = l-op.datum. 
      str-list.artnr = l-op.artnr. 
      str-list.lager-nr = l-op.lager-nr. 
      str-list.docu-nr = l-op.docu-nr. 
      str-list.lscheinnr = l-op.lscheinnr. 
      str-list.qty = l-op.anzahl. 
      str-list.epreis = l-op.einzelpreis. 
      str-list.pos    = l-op.pos.
      /*IF show-price THEN str-list.warenwert = l-op.warenwert. */

      IF show-price THEN DO:
          /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN str-list.addvat-value = queasy.deci1
                     str-list.warenwert    = str-list.warenwert + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     str-list.amountexcl   = l-op.warenwert. /* Bily Add Amount Without Tax */
          ELSE ASSIGN str-list.warenwert = str-list.warenwert + l-op.warenwert
                     str-list.amountexcl = l-op.warenwert. /* Bily Add Amount Without Tax */
      END.


      RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
 
      ASSIGN
        str-list.DATE = l-op.datum 
        str-list.st = l-op.lager-nr 
        str-list.article = l-artikel.artnr 
        str-list.DESCRIPTION = l-artikel.bezeich
        str-list.d-unit = l-artikel.traubensort
        str-list.inc-qty = l-op.anzahl 
        str-list.amount = str-list.warenwert 
        str-list.supplier = l-lieferant.firma 
        str-list.docu-no = l-op.docu-nr
        str-list.deliv-note = l-op.lscheinnr
        str-list.price = unit-price
        str-list.tax-code = l-artikel.lief-artnr[3].

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
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                 tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
      END.
    END. 
END.
 
PROCEDURE create-list22a: 
  DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
  DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
  DEFINE VARIABLE lscheinnr AS CHAR INITIAL "".
  DEFINE VARIABLE t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
  
    /*MTstatus default "Processing...".*/ 
    FOR EACH str-list: 
      delete str-list. 
    END. 
    tot-anz = 0. 
    tot-amount = 0.
    tot-amountexcl = 0. /* Bily Add Amount excl */
    tot-tax    = 0.
    tot-tax    = 0.
    tot-amt    = 0.
   
    IF store = 0 THEN 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
        AND l-op.lief-nr = l-lieferant.lief-nr 
        /*  AND l-op.loeschflag = 0 */ 
        AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
        AND l-op.op-art = 1 
        /*    AND l-op.warenwert NE 0 */ 
        NO-LOCK USE-INDEX lief_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
        AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
        NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
        BY l-op.datum BY l-op.lscheinnr BY l-artikel.bezeich:
        RUN assign-create-list22a(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                  INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                  INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
    END. 
   
    ELSE 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
        AND l-op.lief-nr = l-lieferant.lief-nr 
        /*  AND l-op.loeschflag = 0 */ 
        AND l-op.loeschflag LE 1   /* changedate: 10/29/99 */ 
        AND l-op.op-art = 1 
        /*    AND l-op.warenwert NE 0  */ 
        AND l-op.lager-nr = store 
        NO-LOCK USE-INDEX lief_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
        AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
        NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
        BY l-op.datum BY l-op.lscheinnr BY l-artikel.bezeich:
  
        RUN assign-create-list22a(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, 
                                  INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, 
                                  INPUT-OUTPUT lscheinnr, INPUT-OUTPUT t-amountexcl).
    END. 
    RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-tax,
                       INPUT-OUTPUT t-inv, INPUT-OUTPUT t-amountexcl).
  
    create str-list. 
    ASSIGN
      str-list.DESCRIPTION = "T O T A L" 
      str-list.qty        = t-anz 
      str-list.inc-qty    = t-anz 
      str-list.amount     = t-amt
      str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = t-tax
      str-list.tot-amt    = t-inv. 
    create str-list. 
   
    create str-list.
    ASSIGN
      str-list.DESCRIPTION = "GRAND TOTAL" 
      str-list.qty        = tot-anz 
      str-list.inc-qty    = tot-anz
      str-list.amount     = tot-amount
      str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
      str-list.tax-amount = tot-tax
      str-list.tot-amt    = tot-amt. 
  END.
  PROCEDURE assign-create-list22a:
  DEFINE INPUT-OUTPUT PARAMETER t-anz     AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-amt     AS DECIMAL INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-tax     AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-inv     AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHAR.
  DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
      
  DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  
      FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
        = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 
   
      IF lscheinnr = "" THEN lscheinnr = l-op.lscheinnr. 
      IF lscheinnr NE l-op.lscheinnr THEN 
      DO: 
        lscheinnr = l-op.lscheinnr. 
        create str-list.
        ASSIGN
          str-list.DESCRIPTION = "T O T A L"
          str-list.qty = t-anz 
          str-list.inc-qty = t-anz
          str-list.amount = t-amt
          str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
          str-list.tax-amount = t-tax
          str-list.tot-amt    = t-inv. 
  
        t-anz = 0. 
        t-amt = 0.
        t-amountexcl = 0. /* Bily Add Amount excl */
        t-tax = 0.
        t-inv = 0.
  
        create str-list. 
      END. 
      t-anz = t-anz + l-op.anzahl. 
      /*IF show-price THEN t-amt = t-amt + l-op.warenwert. */
  
      IF show-price THEN DO: 
          /*ITA Request vietnam*/
            FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                  AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN t-amt = t-amt + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                       tot-amount = tot-amount + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                       t-amountexcl = t-amountexcl + l-op.warenwert
                       tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
            ELSE ASSIGN t-amt = t-amt + l-op.warenwert
                        tot-amount = tot-amount + l-op.warenwert
                        t-amountexcl = t-amountexcl + l-op.warenwert
                      tot-amountexcl = tot-amountexcl + l-op.warenwert.  
      END.
  
      tot-anz = tot-anz + l-op.anzahl. 
      /*IF show-price THEN tot-amount = tot-amount + l-op.warenwert. */
      IF show-price THEN unit-price = l-op.einzelpreis. 
      FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
        AND str-list.artnr = l-op.artnr 
        AND str-list.lager-nr = l-op.lager-nr 
        AND str-list.lscheinnr = l-op.lscheinnr 
        AND str-list.epreis = l-op.einzelpreis NO-LOCK NO-ERROR. 
      IF AVAILABLE str-list THEN 
      DO: 
        str-list.qty = str-list.qty + l-op.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-op.warenwert.
          str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
        ASSIGN
          str-list.inc-qty = str-list.qty
          str-list.amount = str-list.warenwert
          str-list.amountexcl = str-list.amountexcl. /* Bily Add Amount excl */
  
        FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
        IF AVAILABLE taxcode-list THEN DO:
            ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                   str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                   t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                   tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                   
                   str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                   t-inv   = t-inv + (l-op.warenwert + amt)
                   tot-amt = tot-amt + (l-op.warenwert + amt).
        END.
      END. 
      ELSE 
      DO: 
        create str-list. 
        RUN add-id.
        IF AVAILABLE l-ophdr THEN 
        DO: 
          str-list.invoice-nr = l-ophdr.fibukonto. 
          str-list.h-recid = RECID(l-ophdr). 
        END. 
        str-list.l-recid = RECID(l-op). 
        str-list.lief-nr = l-op.lief-nr. 
        str-list.billdate = l-op.datum. 
        str-list.artnr = l-op.artnr. 
        str-list.lager-nr = l-op.lager-nr. 
        str-list.docu-nr = l-op.docu-nr. 
        str-list.lscheinnr = l-op.lscheinnr. 
        str-list.qty = l-op.anzahl. 
        str-list.epreis = l-op.einzelpreis. 
        str-list.pos    = l-op.pos.
        IF show-price THEN str-list.warenwert = l-op.warenwert. 
  
        RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
   
        ASSIGN
          str-list.DATE = l-op.datum
          str-list.st = l-op.lager-nr
          str-list.article = l-artikel.artnr 
          str-list.DESCRIPTION = l-artikel.bezeich 
          str-list.d-unit = l-artikel.traubensort
          str-list.inc-qty = l-op.anzahl 
          str-list.amount = str-list.warenwert
          str-list.amountexcl = str-list.amountexcl 
          str-list.supplier = l-lieferant.firma
          str-list.tax-code = l-artikel.lief-artnr[3].
  
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
        IF AVAILABLE taxcode-list THEN DO:
            ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                   t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                   tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                   
                   str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                   t-inv   = t-inv + (l-op.warenwert + str-list.tax-amount)
                   tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
        END.
  
   
        IF l-op.docu-nr = l-op.lscheinnr THEN
          str-list.docu-no = translateExtended ("Direct Purchase   ",lvCAREA,"").
        ELSE str-list.docu-no = l-op.docu-nr. 
       
        ASSIGN 
          str-list.deliv-note = l-op.lscheinnr 
          str-list.price = unit-price. 
      END. 
  END.  
 
PROCEDURE create-list22b: 
DEFINE VARIABLE t-anz     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt     AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-tax     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv     AS DECIMAL INITIAL 0.
DEFINE VARIABLE lief-nr   AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR    INITIAL "". 
DEFINE VARIABLE t-amountexcl AS DECIMAL INITIAL 0. /* Bily Add Amount excl */
  /*MTstatus default "Processing...".*/ 
  FOR EACH str-list: 
    DELETE str-list. 
  END. 
 
  tot-anz    = 0. 
  tot-amount = 0.
  tot-amountexcl = 0. /* Bily Add Amount excl */
  tot-tax    = 0.
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.lief-nr = l-lieferant.lief-nr AND l-op.loeschflag LE 1 
      AND l-op.op-art = 1 NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
      BY l-untergrup.bezeich BY l-artikel.bezeich BY l-op.datum:
      RUN assign-create-list22b(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl,
                                INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT lscheinnr).
  END. 
 
  ELSE 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date
      AND l-op.lief-nr = l-lieferant.lief-nr AND l-op.loeschflag LE 1 
      AND l-op.op-art = 1 AND l-op.lager-nr = store NO-LOCK USE-INDEX lief_ix, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
      AND l-artikel.endkum GE from-grp    /*MT 20/09/12 */
      AND l-artikel.endkum LE to-grp      /*MT 20/09/12 */
      NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
      BY l-untergrup.bezeich BY l-op.datum BY l-artikel.bezeich:
      RUN assign-create-list22b(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl,
                                INPUT-OUTPUT t-tax, INPUT-OUTPUT t-inv, INPUT-OUTPUT lscheinnr).
  END. 
  RUN create-hislist(INPUT-OUTPUT t-anz, INPUT-OUTPUT t-amt, INPUT-OUTPUT t-amountexcl, INPUT-OUTPUT t-tax,
                     INPUT-OUTPUT t-inv).

  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr 
    str-list.qty = t-anz  
    str-list.inc-qty = t-anz 
    str-list.amount = t-amt
    str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv. 
    str-list.supplier = "T O T A L". 
 
  create str-list. 
 
  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = "GRAND TOTAL" 
    str-list.qty = tot-anz
    str-list.inc-qty = tot-anz
    str-list.amount = tot-amount
    str-list.amountexcl = tot-amountexcl /* Bily Add Amount excl */
    str-list.tax-amount = tot-tax
    str-list.tot-amt    = tot-amt. 

END.
PROCEDURE assign-create-list22b:
DEFINE INPUT-OUTPUT PARAMETER t-anz     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-amt     AS DECIMAL INITIAL 0.
DEFINE INPUT-OUTPUT PARAMETER t-tax     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER t-inv     AS DECIMAL INITIAL 0. 
DEFINE INPUT-OUTPUT PARAMETER lscheinnr AS CHAR    INITIAL "".
DEFINE INPUT-OUTPUT PARAMETER t-amountexcl AS DECIMAL INITIAL 0.

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STI" AND l-ophdr.lscheinnr 
      = l-op.lscheinnr AND l-ophdr.datum = l-op.datum NO-LOCK NO-ERROR. 
 
    IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
    IF lscheinnr NE l-untergrup.bezeich THEN 
    DO:
      create str-list.
      ASSIGN
        str-list.DESCRIPTION = lscheinnr 
        str-list.qty = t-anz 
        str-list.inc-qty = t-anz
        str-list.amount  = t-amt
        str-list.amountexcl = t-amountexcl /* Bily Add Amount excl */
        str-list.tax-amount = t-tax
        str-list.tot-amt    = t-inv
        str-list.supplier = "T O T A L"
        lscheinnr = l-untergrup.bezeich.

      t-anz = 0. 
      t-amt = 0.
      t-amountexcl = 0. /* Bily Add Amount excl */
      t-tax = 0.
      t-inv = 0.
      create str-list. 
    END. 
 
    t-anz = t-anz + l-op.anzahl. 
    /*IF show-price THEN t-amt = t-amt + l-op.warenwert.*/
     IF show-price THEN DO: 
        /*ITA Request vietnam*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
                AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
              ASSIGN t-amt = t-amt + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     tot-amount = tot-amount + (l-op.warenwert + (l-op.warenwert * (queasy.deci1 / 100)))
                     t-amountexcl = t-amountexcl + l-op.warenwert
                     tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
          ELSE ASSIGN t-amt = t-amt + l-op.warenwert
                      tot-amount = tot-amount + l-op.warenwert
                      t-amountexcl = t-amountexcl + l-op.warenwert
                      tot-amountexcl = tot-amountexcl + l-op.warenwert. /* Bily Add Amount excl */
    END.
    tot-anz = tot-anz + l-op.anzahl. 
    /*IF show-price THEN tot-amount = tot-amount + l-op.warenwert. */
    IF show-price THEN unit-price = l-op.einzelpreis. 
 
    FIND FIRST str-list WHERE str-list.docu-nr = l-op.docu-nr 
      AND str-list.lscheinnr = l-op.lscheinnr 
      AND str-list.lager-nr = l-op.lager-nr 
      AND str-list.artnr = l-op.artnr 
      AND str-list.epreis = l-op.einzelpreis NO-LOCK NO-ERROR. 
    IF AVAILABLE str-list THEN 
    DO: 

        str-list.qty = str-list.qty + l-op.anzahl. 
        IF show-price THEN 
          str-list.warenwert = str-list.warenwert + l-op.warenwert.
          str-list.amountexcl = str-list.amountexcl + l-op.warenwert. /* Bily Add Amount excl */
        str-list.inc-qty = str-list.qty. 
        str-list.amount = str-list.warenwert.
        str-list.amountexcl = str-list.amountexcl. /* Bily Add Amount excl */

      FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN amt                 = l-op.warenwert * taxcode-list.taxamount
                 str-list.tax-amount = str-list.tax-amount + (l-op.warenwert * taxcode-list.taxamount)
                 t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = str-list.tot-amt + (l-op.warenwert + amt)
                 t-inv   = t-inv + (l-op.warenwert + amt)
                 tot-amt = tot-amt + (l-op.warenwert + amt).
      END.
    END. 
    ELSE 
    DO: 
      create str-list. 
      RUN add-id.
      IF AVAILABLE l-ophdr THEN 
      DO: 
        str-list.invoice-nr = l-ophdr.fibukonto. 
        str-list.h-recid = RECID(l-ophdr). 
      END. 
      str-list.l-recid = RECID(l-op). 
      str-list.lief-nr = l-op.lief-nr. 
      str-list.billdate = l-op.datum. 
      str-list.artnr = l-op.artnr. 
      str-list.lager-nr = l-op.lager-nr. 
      str-list.docu-nr = l-op.docu-nr. 
      str-list.lscheinnr = l-op.lscheinnr. 
      str-list.qty = l-op.anzahl. 
      str-list.epreis = l-op.einzelpreis. 
      str-list.pos    = l-op.pos.
      IF show-price THEN str-list.warenwert = l-op.warenwert. 
      RUN convert-fibu(l-op.stornogrund, OUTPUT str-list.fibu, OUTPUT str-list.fibu-bez). 
 
      ASSIGN
        str-list.DATE = l-op.datum 
        str-list.st = l-op.lager-nr
        str-list.article = l-artikel.artnr 
        str-list.DESCRIPTION = l-artikel.bezeich
        str-list.d-unit = l-artikel.traubensort 
        str-list.inc-qty = l-op.anzahl
        str-list.amount = str-list.warenwert
        str-list.amountexcl = str-list.amountexcl 
        str-list.supplier = l-lieferant.firma
        str-list.tax-code = l-artikel.lief-artnr[3].

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
      IF AVAILABLE taxcode-list THEN DO:
          ASSIGN str-list.tax-amount = l-op.warenwert * taxcode-list.taxamount
                 t-tax   = t-tax   + (l-op.warenwert * taxcode-list.taxamount)
                 tot-tax = tot-tax + (l-op.warenwert * taxcode-list.taxamount) 
                 
                 str-list.tot-amt = l-op.warenwert + str-list.tax-amount
                 t-inv   = t-inv + (l-op.warenwert + str-list.tax-amount)
                 tot-amt = tot-amt + (l-op.warenwert + str-list.tax-amount).
      END.
 
      IF l-op.docu-nr = l-op.lscheinnr THEN 
      str-list.docu-no = translateExtended ("Direct Purchase ",lvCAREA,""). 
      ELSE str-list.docu-no = l-op.docu-nr. 
       
      ASSIGN
        str-list.deliv-note = l-op.lscheinnr
        str-list.price = unit-price. 
    END. 
END.

PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.

    FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
        str-list.id = usr.userinit.
    ELSE str-list.id = "??".
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


