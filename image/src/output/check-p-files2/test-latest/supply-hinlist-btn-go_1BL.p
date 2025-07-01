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
    FIELD inc-qty     AS DECIMAL
    FIELD amount      AS DECIMAL
    FIELD docu-no     AS CHARACTER
    FIELD deliv-no     AS CHARACTER
    
    /*gst for penang*/
    FIELD gstid       AS CHAR
    FIELD tax-code    AS CHAR
    FIELD tax-amount  AS DECIMAL
    FIELD tot-amt     AS DECIMAL
    FIELD lief-nr     AS INTEGER. 

DEFINE TEMP-TABLE taxcode-list
    FIELD taxcode   AS CHAR
    FIELD taxamount AS DECIMAL.

DEF INPUT  PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER from-supp AS CHAR.
DEF INPUT  PARAMETER from-doc  AS CHAR.
DEF INPUT  PARAMETER sorttype  AS INT.
DEF INPUT  PARAMETER from-grp  AS INT.
DEF INPUT  PARAMETER to-grp    AS INT.
DEF INPUT  PARAMETER store     AS INT.
DEF INPUT  PARAMETER all-supp  AS LOGICAL.
DEF INPUT  PARAMETER all-doc   AS LOGICAL.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER to-date   AS DATE.
DEF INPUT  PARAMETER TABLE FOR taxcode-list.

DEF OUTPUT PARAMETER err-code  AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE i AS INT.
DEFINE VARIABLE supp-nr AS INT INITIAL 0.
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-amount AS DECIMAL. 
DEFINE VARIABLE long-digit AS LOGICAL. 
DEFINE VARIABLE tot-tax    AS DECIMAL. 
DEFINE VARIABLE tot-amt    AS DECIMAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

DEFINE VARIABLE loopi   AS INTEGER  NO-UNDO.

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
    FIND FIRST vhp.l-ophis WHERE vhp.l-ophis.docu-nr = from-doc NO-LOCK NO-ERROR.
    IF NOT AVAILABLE vhp.l-ophis THEN 
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
          ELSE .
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
        IF from-supp NE "" AND supp-nr NE 0 THEN DO:
            IF from-grp = 0 THEN RUN create-list1as. 
            ELSE RUN create-list11as.
        END.
        ELSE DO:
            IF from-grp = 0 THEN RUN create-list1a. 
            ELSE RUN create-list11a.
        END.
      END.
      ELSE
      DO:
        IF from-grp = 0 THEN RUN create-list1ar. 
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


PROCEDURE create-list1a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 


          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.
            
          ASSIGN str-list.deliv-no      = vhp.l-ophis.lscheinnr.

        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list.
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.supplier = "T O T A L"
    str-list.qty = t-anz
    str-list.inc-qty = t-anz
    str-list.amount = t-amt.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier = "GRAND TOTAL"
     str-list.qty = tot-anz
     str-list.inc-qty = tot-anz
     str-list.amount = tot-amount.
END. 

PROCEDURE create-list1ar: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz = 0. 
  tot-amount = 0. 
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum:
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.          
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.

  create str-list.
  ASSIGN
     str-list.supplier = "GRAND TOTAL"
     str-list.qty = tot-anz
     str-list.inc-qty = tot-anz
     str-list.amount = tot-amount. 
END. 


PROCEDURE create-list11: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0. 
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz    = 0. 
  tot-amount = 0. 
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO: 
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK, 
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY l-lieferant.firma BY vhp.l-ophis.datum BY l-ophis.artnr /*BY vhp.l-ophis.artnr*/:
        IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
        IF lief-nr NE l-lieferant.lief-nr THEN 
        DO: 
          lief-nr = l-lieferant.lief-nr. 
          create str-list.
          ASSIGN
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty          = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert    = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

          ASSIGN str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END.
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.datum BY l-lieferant.firma BY l-ophis.artnr /*BY vhp.l-ophis.artnr*/:
        IF lief-nr = 0 THEN lief-nr = l-lieferant.lief-nr. 
        IF lief-nr NE l-lieferant.lief-nr THEN 
        DO:
          lief-nr = l-lieferant.lief-nr. 
          create str-list.
          ASSIGN
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO:
          str-list.qty          = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert    = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert.

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.


          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list.
  
  ASSIGN
    str-list.supplier   = "T O T A L"
    str-list.qty        = t-anz
    str-list.inc-qty    = t-anz
    str-list.amount     = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier   = "GRAND TOTAL"
     str-list.qty        = tot-anz
     str-list.inc-qty    = tot-anz
     str-list.amount     = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 
 
PROCEDURE create-list11a: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv     AS DECIMAL INITIAL 0.
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  /*MTSTATUS DEFAULT "Processing...".*/ 
  
 FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0. 
  tot-tax    = 0. 
  tot-amt    = 0. 
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum:
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.     
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
  ELSE 
  DO:  
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
          DISP l-ophis.lscheinnr.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list.
          ASSIGN
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0. 
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr        = vhp.l-ophis.artnr. 
          str-list.lager-nr     = vhp.l-ophis.lager-nr. 
          str-list.docu-nr      = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr    = vhp.l-ophis.lscheinnr. 
          str-list.qty          = vhp.l-ophis.anzahl. 
          str-list.epreis       = vhp.l-ophis.einzelpreis. 
          str-list.warenwert    = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list.
  ASSIGN
    str-list.supplier   = "T O T A L"
    str-list.qty        = t-anz
    str-list.inc-qty    = t-anz
    str-list.amount     = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.

  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier   = "GRAND TOTAL"
     str-list.qty        = tot-anz
     str-list.inc-qty    = tot-anz
     str-list.amount     = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 
 
PROCEDURE create-list11ar: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  
/*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.  
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr        = vhp.l-ophis.artnr. 
          str-list.lager-nr     = vhp.l-ophis.lager-nr. 
          str-list.docu-nr      = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr    = vhp.l-ophis.lscheinnr. 
          str-list.qty          = vhp.l-ophis.anzahl. 
          str-list.epreis       = vhp.l-ophis.einzelpreis. 
          str-list.warenwert    = vhp.l-ophis.warenwert. 
        
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
         BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum:
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.    
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr        = vhp.l-ophis.artnr. 
          str-list.lager-nr     = vhp.l-ophis.lager-nr. 
          str-list.docu-nr      = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr    = vhp.l-ophis.lscheinnr. 
          str-list.qty          = vhp.l-ophis.anzahl. 
          str-list.epreis       = vhp.l-ophis.einzelpreis. 
          str-list.warenwert    = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.

  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 

PROCEDURE create-list22: 
DEFINE VARIABLE t-anz   AS DEC.
DEFINE VARIABLE t-amt   AS DEC.
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0. 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  
/*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0. 
  t-tax    = 0.
  t-inv    = 0.
  tot-tax  = 0.
  tot-amt  = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.op-art = 1 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/  
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 200912 */
        AND l-artikel.endkum LE to-grp      /*MT 200912 */
        NO-LOCK BY vhp.l-ophis.datum BY l-ophis.artnr /*BY vhp.l-ophis.artnr*/:
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert.
          
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum      
              str-list.st           = vhp.l-ophis.lager-nr   
              str-list.supplier     = l-lieferant.firma      
              str-list.article      = l-artikel.artnr        
              str-list.DESCRIPTION  = l-artikel.bezeich      
              str-list.d-unit       = l-artikel.traubensort  
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl     
              str-list.amount       = vhp.l-ophis.warenwert 
              str-list.docu-no      = vhp.l-ophis.docu-nr
              str-list.deliv-no     = vhp.l-ophis.lscheinnr
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          
        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND vhp.l-ophis.op-art = 1 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/  
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
        AND l-artikel.endkum GE from-grp    /*MT 200912 */
        AND l-artikel.endkum LE to-grp      /*MT 200912 */
        NO-LOCK BY vhp.l-ophis.datum BY l-ophis.artnr /*BY vhp.l-ophis.artnr*/:
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty          = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert    = str-list.warenwert + vhp.l-ophis.warenwert.     
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert.

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum      
              str-list.st           = vhp.l-ophis.lager-nr   
              str-list.supplier     = l-lieferant.firma      
              str-list.article      = l-artikel.artnr        
              str-list.DESCRIPTION  = l-artikel.bezeich      
              str-list.d-unit       = l-artikel.traubensort  
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl     
              str-list.amount       = vhp.l-ophis.warenwert 
              str-list.docu-no      = vhp.l-ophis.docu-nr
              str-list.deliv-no     = vhp.l-ophis.lscheinnr
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.
        END. 
      END. 
  END.
 
  create str-list.
  ASSIGN
     str-list.supplier = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty    = tot-anz
     str-list.amount     = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 
 
/*ITA 050314*/
PROCEDURE create-list1b: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0. 
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY vhp.l-ophis.datum BY l-ophis.artnr BY l-untergrup.bezeich BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr 
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.  
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY vhp.l-ophis.datum BY l-ophis.artnr BY l-untergrup.bezeich BY l-artikel.bezeich:
        /*
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich.
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.       
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.


          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt
    str-list.tax-amount  = t-tax
    str-list.tot-amt     = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END.

PROCEDURE create-list11b: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 
  /*MTSTATUS DEFAULT "Processing...".*/ 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.
  
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY vhp.l-ophis.datum BY l-ophis.artnr /*BY l-ophis.artnr*/ BY l-untergrup.bezeich BY l-artikel.bezeich :

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. */

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.
          
          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END.

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
        BY vhp.l-ophis.datum BY l-ophis.artnr BY l-untergrup.bezeich BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.

        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 


PROCEDURE create-list1br: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
        BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. */

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.


          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.

  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt
    str-list.tax-amount  = t-tax
    str-list.tot-amt     = t-inv.
  create str-list. 

  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 

PROCEDURE create-list11br: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.

 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date 
        AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY l-ophis.artnr BY l-untergrup.bezeich BY l-artikel.bezeich BY vhp.l-ophis.datum :

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 

          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr        = vhp.l-ophis.artnr. 
          str-list.lager-nr     = vhp.l-ophis.lager-nr. 
          str-list.docu-nr      = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr    = vhp.l-ophis.lscheinnr. 
          str-list.qty          = vhp.l-ophis.anzahl. 
          str-list.epreis       = vhp.l-ophis.einzelpreis. 
          str-list.warenwert    = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
  ELSE 
  DO:  
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr GT 0 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND vhp.l-ophis.docu-nr = from-doc 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich :

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.

  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.
  create str-list. 

  create str-list.
  ASSIGN
     str-list.supplier = "GRAND TOTAL"
     str-list.qty      = tot-anz
     str-list.inc-qty  = tot-anz
     str-list.amount   = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 

PROCEDURE create-list1as: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "".


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  /*MTSTATUS DEFAULT "Processing...".*/ 

  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
        BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum:
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty      = t-anz
            str-list.inc-qty  = t-anz
            str-list.amount   = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 


          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.

        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
        BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list.
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty      = t-anz
            str-list.inc-qty  = t-anz
            str-list.amount   = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.supplier = "T O T A L"
    str-list.qty      = t-anz
    str-list.inc-qty  = t-anz
    str-list.amount   = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 

/*lanjutkan dari sini*/
PROCEDURE create-list11as: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.

DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 
  /*MTSTATUS DEFAULT "Processing...".*/ 


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz = 0. 
  tot-amount = 0. 
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr 
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
        BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum :
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier   = "T O T A L"
            str-list.qty        = t-anz
            str-list.inc-qty    = t-anz
            str-list.amount     = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.
          
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.     
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.

        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK 
        BY vhp.l-ophis.lscheinnr BY l-ophis.artnr BY vhp.l-ophis.datum:
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list.
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list.
  ASSIGN
    str-list.supplier   = "T O T A L"
    str-list.qty        = t-anz
    str-list.inc-qty    = t-anz
    str-list.amount     = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 


PROCEDURE create-list1bs: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lief-nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 

DEFINE VARIABLE amt AS DECIMAL NO-UNDO.
  
/*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 
  tot-anz    = 0. 
  tot-amount = 0. 
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
        BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr 
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.  
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 

          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
        BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:
        /*
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount = t-tax
            str-list.tot-amt    = t-inv.

          lscheinnr = l-untergrup.bezeich.
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 
        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert.       
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.


          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt
    str-list.tax-amount = t-tax
    str-list.tot-amt    = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END.



PROCEDURE create-list11bs: 
DEFINE VARIABLE t-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL INITIAL 0. 

DEFINE VARIABLE t-tax AS DECIMAL INITIAL 0.
DEFINE VARIABLE t-inv AS DECIMAL INITIAL 0.
DEFINE VARIABLE lscheinnr AS CHAR INITIAL "". 


DEFINE VARIABLE amt AS DECIMAL NO-UNDO.

  /*MTSTATUS DEFAULT "Processing...".*/ 
  FOR EACH str-list: 
    delete str-list. 
  END. 

  tot-anz    = 0. 
  tot-amount = 0.
  tot-tax    = 0.
  tot-amt    = 0.
 
  IF store = 0 THEN 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
         BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END. */

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.
          
          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0.
          t-tax = 0.
          t-inv = 0.
          
          create str-list. 
        END.

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.


          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
  ELSE 
  DO:
      FOR EACH vhp.l-ophis WHERE vhp.l-ophis.datum GE from-date AND vhp.l-ophis.datum LE to-date 
        AND vhp.l-ophis.lief-nr = l-lieferant.lief-nr  
        AND vhp.l-ophis.op-art = 1 
        AND vhp.l-ophis.anzahl NE 0 
        AND vhp.l-ophis.lager-nr = store 
        AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*")   /*gerald for not include cancelled receiving 4B0C09*/
        NO-LOCK USE-INDEX lief-op-dat_ix, 
        FIRST l-artikel WHERE l-artikel.artnr = vhp.l-ophis.artnr 
          AND l-artikel.endkum GE from-grp    /*MT 200912 */
          AND l-artikel.endkum LE to-grp      /*MT 200912 */
          NO-LOCK,
        FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK  /*ITA 050314*/
        BY l-ophis.artnr BY l-untergrup.bezeich BY vhp.l-ophis.datum BY l-artikel.bezeich:

        /*FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = vhp.l-ophis.lscheinnr. 
        IF lscheinnr NE vhp.l-ophis.lscheinnr THEN 
        DO: 
          lscheinnr = vhp.l-ophis.lscheinnr. 
          create str-list. 
          ASSIGN
            str-list.supplier = "T O T A L"
            str-list.qty = t-anz
            str-list.inc-qty = t-anz
            str-list.amount = t-amt.
          t-anz = 0. 
          t-amt = 0. 
          create str-list. 
        END.*/

        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = vhp.l-ophis.lief-nr NO-LOCK NO-ERROR.
        IF lscheinnr = "" THEN lscheinnr = l-untergrup.bezeich. 
        IF lscheinnr NE l-untergrup.bezeich THEN 
        DO: 
          create str-list. 
          ASSIGN
            str-list.DESCRIPTION = lscheinnr
            str-list.supplier    = "T O T A L"
            str-list.qty         = t-anz
            str-list.inc-qty     = t-anz
            str-list.amount      = t-amt
            str-list.tax-amount  = t-tax
            str-list.tot-amt     = t-inv.

          lscheinnr = l-untergrup.bezeich. 
          t-anz = 0. 
          t-amt = 0. 
          t-tax = 0.
          t-inv = 0.
          create str-list. 
        END. 

        t-anz = t-anz + vhp.l-ophis.anzahl. 
        t-amt = t-amt + vhp.l-ophis.warenwert. 
        tot-anz = tot-anz + vhp.l-ophis.anzahl. 
        tot-amount = tot-amount + vhp.l-ophis.warenwert. 
        FIND FIRST str-list WHERE str-list.docu-nr = vhp.l-ophis.docu-nr 
          AND str-list.artnr = vhp.l-ophis.artnr 
          AND str-list.lager-nr = vhp.l-ophis.lager-nr 
          AND str-list.lscheinnr = vhp.l-ophis.lscheinnr 
          AND str-list.epreis = vhp.l-ophis.einzelpreis NO-LOCK NO-ERROR. 
        IF AVAILABLE str-list THEN 
        DO: 
          str-list.qty = str-list.qty + vhp.l-ophis.anzahl. 
          str-list.warenwert = str-list.warenwert + vhp.l-ophis.warenwert. 
          str-list.inc-qty      = str-list.qty.
          str-list.amount       = str-list.warenwert.

          FIND FIRST taxcode-list WHERE taxcode-list.taxcode = str-list.tax-code NO-LOCK NO-ERROR.
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN amt                 = l-ophis.warenwert * taxcode-list.taxamount
                     str-list.tax-amount = str-list.tax-amount + (l-ophis.warenwert * taxcode-list.taxamount)
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = str-list.tot-amt + (l-ophis.warenwert + amt)
                     t-inv   = t-inv + (l-ophis.warenwert + amt)
                     tot-amt = tot-amt + (l-ophis.warenwert + amt).
          END.
        END. 
        ELSE 
        DO: 
          create str-list. 
          str-list.artnr = vhp.l-ophis.artnr. 
          str-list.lager-nr = vhp.l-ophis.lager-nr. 
          str-list.docu-nr = vhp.l-ophis.docu-nr. 
          str-list.lscheinnr = vhp.l-ophis.lscheinnr. 
          str-list.qty = vhp.l-ophis.anzahl. 
          str-list.epreis = vhp.l-ophis.einzelpreis. 
          str-list.warenwert = vhp.l-ophis.warenwert. 
          ASSIGN
              str-list.datum        = vhp.l-ophis.datum
              str-list.st           = vhp.l-ophis.lager-nr
              str-list.supplier     = l-lieferant.firma
              str-list.article      = l-artikel.artnr
              str-list.DESCRIPTION  = l-artikel.bezeich
              str-list.d-unit       = l-artikel.traubensort
              str-list.price        = vhp.l-ophis.einzelpreis
              str-list.inc-qty      = vhp.l-ophis.anzahl
              str-list.amount       = vhp.l-ophis.warenwert
              str-list.lief-nr      = vhp.l-ophis.lief-nr
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
          IF AVAILABLE taxcode-list THEN DO:
              ASSIGN str-list.tax-amount = l-ophis.warenwert * taxcode-list.taxamount
                     t-tax   = t-tax   + (l-ophis.warenwert * taxcode-list.taxamount)
                     tot-tax = tot-tax + (l-ophis.warenwert * taxcode-list.taxamount) 
                     
                     str-list.tot-amt = l-ophis.warenwert + str-list.tax-amount
                     t-inv   = t-inv + (l-ophis.warenwert + str-list.tax-amount)
                     tot-amt = tot-amt + (l-ophis.warenwert + str-list.tax-amount).
          END.

          IF vhp.l-ophis.docu-nr = vhp.l-ophis.lscheinnr THEN
              str-list.docu-no      = "Direct Pchase   ".
          ELSE str-list.docu-no      = vhp.l-ophis.docu-nr.

              str-list.deliv-no      = vhp.l-ophis.lscheinnr.
        END. 
      END. 
  END.
 
  create str-list. 
  ASSIGN
    str-list.DESCRIPTION = lscheinnr
    str-list.supplier    = "T O T A L"
    str-list.qty         = t-anz
    str-list.inc-qty     = t-anz
    str-list.amount      = t-amt
    str-list.tax-amount  = t-tax
    str-list.tot-amt     = t-inv.
  create str-list. 
 
  create str-list.
  ASSIGN
     str-list.supplier  = "GRAND TOTAL"
     str-list.qty       = tot-anz
     str-list.inc-qty   = tot-anz
     str-list.amount    = tot-amount
     str-list.tax-amount = tot-tax
     str-list.tot-amt    = tot-amt.
END. 
/*end*/
 
