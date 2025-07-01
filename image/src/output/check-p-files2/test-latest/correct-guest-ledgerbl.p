
DEFINE TEMP-TABLE output-list 
  FIELD flag     AS INTEGER 
  FIELD artart   AS INTEGER 
  FIELD str      AS CHAR
  FIELD ankunft  AS DATE LABEL "Arrival"
  FIELD ankzeit  AS CHAR FORMAT "x(8)" LABEL "Checked-In".

DEFINE TEMP-TABLE m-list 
  FIELD resnr   AS INTEGER 
  FIELD zinr    AS CHAR 
  FIELD abreise AS DATE. 

DEFINE TEMP-TABLE sum-list 
  FIELD bezeich AS CHAR FORMAT "x(16)" 
  FIELD debit   AS DECIMAL FORMAT ">>>,>>>,>>9.99"   INIT 0
  FIELD credit  AS DECIMAL FORMAT ">>>,>>>,>>9.99"   INIT 0
  FIELD balance AS DECIMAL FORMAT "->>>,>>>,>>9.99" INIT 0. 

DEFINE TEMP-TABLE s-list 
  FIELD i-counter   AS INTEGER INITIAL 0
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD artnr       AS INTEGER 
  FIELD dept        AS INTEGER 
  FIELD gname       AS CHAR FORMAT "x(24)" 
  FIELD zinr        LIKE zimmer.zinr
  FIELD abreise     AS DATE INITIAL ? 
  FIELD bill-datum  AS DATE
  FIELD rechnr      AS INTEGER FORMAT ">>>>>>9" 
  FIELD billtyp     AS CHAR FORMAT "x(2)" 
  FIELD billnr      AS INTEGER FORMAT "9" 
  FIELD bezeich     AS CHAR FORMAT "x(16)" 
  FIELD prevbal     AS DECIMAL FORMAT "->>>,>>>,>>9.99" INIT 0
  FIELD debit       AS DECIMAL FORMAT "->>,>>>,>>9.99"  INIT 0
  FIELD credit      AS DECIMAL FORMAT "->>,>>>,>>9.99"  INIT 0
  FIELD balance     AS DECIMAL FORMAT "->>>,>>>,>>9.99"
  FIELD ankunft     AS DATE INITIAL ?
  FIELD ankzeit     AS CHAR INITIAL "". 

DEFINE TEMP-TABLE ns-list 
  FIELD rechnr      AS INTEGER 
  FIELD saldo       AS DECIMAL INITIAL 0
  FIELD prevbal     AS DECIMAL INITIAL 0. 

DEF TEMP-TABLE bill-alert
    FIELD rechnr AS INTEGER.

DEF TEMP-TABLE bill-list
    FIELD rechnr        AS INTEGER
    FIELD billnr        AS INTEGER
    FIELD resnr         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD ankzeit       AS INTEGER
    FIELD ankunft       AS DATE
    FIELD abreise       AS DATE
    FIELD first-date    AS DATE INIT ?
    FIELD last-date     AS DATE INIT ?
    FIELD zinr          AS CHAR
    FIELD gname         AS CHAR
    FIELD billtype      AS CHAR 

    FIELD betrag        AS DECIMAL
    INDEX rechnr_ix     rechnr
    INDEX rechnrtype_ix rechnr billtype
    INDEX datetype_ix   first-date last-date billtype
.



DEFINE INPUT PARAMETER fdate AS DATE NO-UNDO.
DEFINE INPUT PARAMETER tdate AS DATE NO-UNDO.

DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO.

DEFINE VARIABLE billdate AS DATE NO-UNDO.
DEFINE VARIABLE heute    AS DATE NO-UNDO.
DEFINE VARIABLE ank-flag AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE sorttype AS INTEGER NO-UNDO INIT 1.
DEFINE VARIABLE prevbal         AS DECIMAL. 
DEFINE VARIABLE debit           AS DECIMAL. 
DEFINE VARIABLE credit          AS DECIMAL. 
DEFINE VARIABLE balance         AS DECIMAL. 
DEFINE VARIABLE current-counter AS INTEGER NO-UNDO.
DEFINE VARIABLE t-prevbal       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-debit         AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-credit        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE t-balance       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-bline       AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-rechnr     AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-flag       AS INTEGER INITIAL 0. 
DEFINE VARIABLE long-digit      AS LOGICAL. 
DEFINE VARIABLE fact1           AS INTEGER. 
DEFINE VARIABLE short-flag      AS LOGICAL INITIAL NO.
DEFINE VARIABLE outstanding     AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE    NO-UNDO.
DEFINE VARIABLE curr-time       AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 246 NO-LOCK NO-ERROR. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR. 
curr-date = htparam.fdate.

IF NOT long-digit OR NOT short-flag THEN fact1 = 1. 
ELSE fact1 = 1000. 


ASSIGN curr-time = TIME.
DO billdate = fdate TO tdate:
    ASSIGN
          tot-bline       = 0
          current-counter = 0
          t-prevbal       = 0
          t-debit         = 0
          t-credit        = 0
          t-balance       = 0
          outstanding     = 0
          heute           = billdate
      .

    RUN create-bill-list.
    RUN create-umsatz.

    IF outstanding NE 0 THEN DO:
         IF billdate LT curr-date THEN DO:
             FIND FIRST uebertrag WHERE uebertrag.datum = billdate NO-LOCK NO-ERROR.
             IF AVAILABLE uebertrag THEN DO:
                 FIND CURRENT uebertrag EXCLUSIVE-LOCK.
                 ASSIGN uebertrag.betrag = outstanding.
                 FIND CURRENT uebertrag NO-LOCK.
                 RELEASE uebertrag.
             END.
             ELSE DO:
                 CREATE uebertrag.
                 ASSIGN uebertrag.datum  = billdate
                        uebertrag.betrag = outstanding.
                        
             END.
         END.
    END.  
    ASSIGN success-flag = YES.
END.
/*MESSAGE STRING(TIME - curr-time, "HH:MM:SS") VIEW-AS ALERT-BOX INFO.*/


PROCEDURE create-bill-list:
 DEFINE BUFFER bline FOR bill-line.

  FOR EACH bill-list:
      DELETE bill-list.
  END.
  /* Dzikri 0ED804 - imbalance correction with outstanding
  FOR EACH bill WHERE bill.rechnr GT 0
      AND bill.flag = 1 NO-LOCK,
      FIRST bill-line WHERE bill-line.rechnr = bill.rechnr
        AND bill-line.bill-datum = billdate NO-LOCK :

        CREATE bill-list.
        ASSIGN 
            bill-list.resnr  = bill.resnr
            bill-list.zinr   = bill.zinr
            bill-list.rechnr = bill.rechnr
            bill-list.billnr = bill.billnr
        .
        IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN 
        DO:
          FIND FIRST res-line WHERE res-line.resnr = bill.resnr
              AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
          ASSIGN bill-list.billtype = "G".
          IF AVAILABLE res-line THEN
          ASSIGN
              bill-list.resnr    = res-line.resnr
              bill-list.reslinnr = res-line.reslinnr
              bill-list.ankunft  = res-line.ankunft
              bill-list.abreise  = res-line.abreise
              bill-list.ankzeit  = res-line.ankzeit
              bill-list.zinr     = res-line.zinr 
              bill-list.gname    = res-line.NAME
          .
        END.
        ELSE IF bill.resnr GT 0 THEN ASSIGN bill-list.billtype = "M".
        ELSE ASSIGN bill-list.billtype = "N".
        
        /*IF bill.flag = 0 THEN bill-list.last-date = heute. */
        
        IF bill-list.gname = "" THEN
        DO:
          FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK
              NO-ERROR.
          IF AVAILABLE guest THEN bill-list.gname = guest.NAME.
        END.
   
    
        FIND FIRST bline WHERE bline.rechnr = bill-list.rechnr 
          NO-LOCK USE-INDEX bildat_index NO-ERROR.
        IF AVAILABLE bline THEN 
        DO:    
          ASSIGN bill-list.first-date = bline.bill-datum
                 bill-list.betrag     = bline.betrag.
          IF bill.flag = 1 AND bill-list.last-date EQ ? THEN
          DO:
            FIND LAST bline WHERE bline.rechnr = bill-list.rechnr 
              NO-LOCK USE-INDEX bildat_index NO-ERROR.
            IF AVAILABLE bline THEN 
              ASSIGN bill-list.last-date = bline.bill-datum.
          END.
        END.
  END.

  FOR EACH bill WHERE bill.rechnr GT 0
      AND bill.flag = 0 NO-LOCK :

        CREATE bill-list.
        ASSIGN 
            bill-list.resnr  = bill.resnr
            bill-list.zinr   = bill.zinr
            bill-list.rechnr = bill.rechnr
            bill-list.billnr = bill.billnr
            bill-list.last-date = heute
        .
        IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN 
        DO:
          FIND FIRST res-line WHERE res-line.resnr = bill.resnr
              AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
          ASSIGN bill-list.billtype = "G".
          IF AVAILABLE res-line THEN
          ASSIGN
              bill-list.resnr    = res-line.resnr
              bill-list.reslinnr = res-line.reslinnr
              bill-list.ankunft  = res-line.ankunft
              bill-list.abreise  = res-line.abreise
              bill-list.ankzeit  = res-line.ankzeit
              bill-list.zinr     = res-line.zinr 
              bill-list.gname    = res-line.NAME
          .
        END.
        ELSE IF bill.resnr GT 0 THEN ASSIGN bill-list.billtype = "M".
        ELSE ASSIGN bill-list.billtype = "N".
        
        /*IF bill.flag = 0 THEN bill-list.last-date = heute. */
        
        IF bill-list.gname = "" THEN
        DO:
          FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK
              NO-ERROR.
          IF AVAILABLE guest THEN bill-list.gname = guest.NAME.
        END.
   
    
        FIND FIRST bline WHERE bline.rechnr = bill-list.rechnr 
          NO-LOCK USE-INDEX bildat_index NO-ERROR.
        IF AVAILABLE bline THEN 
        DO:    
          ASSIGN bill-list.first-date = bline.bill-datum
                 bill-list.betrag     = bline.betrag.          
        END.
  END.

  /*FDL 29 Jan, 2024 => Stack Trace Gammara*/ 
    Dzikri 0ED804 - END */
  FIND FIRST bill WHERE bill.rechnr GT 0 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE bill:
  
    CREATE bill-list.
    ASSIGN 
        bill-list.resnr  = bill.resnr
        bill-list.zinr   = bill.zinr
        bill-list.rechnr = bill.rechnr
        bill-list.billnr = bill.billnr
    .
    IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN 
    DO:
      FIND FIRST res-line WHERE res-line.resnr = bill.resnr
          AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
      ASSIGN bill-list.billtype = "G".
      IF AVAILABLE res-line THEN
      ASSIGN
          bill-list.resnr    = res-line.resnr
          bill-list.reslinnr = res-line.reslinnr
          bill-list.ankunft  = res-line.ankunft
          bill-list.abreise  = res-line.abreise
          bill-list.ankzeit  = res-line.ankzeit
          bill-list.zinr     = res-line.zinr 
          bill-list.gname    = res-line.NAME
      .
    END.
    ELSE IF bill.resnr GT 0 THEN ASSIGN bill-list.billtype = "M".
    ELSE ASSIGN bill-list.billtype = "N".
    
    IF bill.flag = 0 THEN bill-list.last-date = heute. 
    
    IF bill-list.gname = "" THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK
          NO-ERROR.
      IF AVAILABLE guest THEN bill-list.gname = guest.NAME.
    END.

    IF bill.flag = 1 THEN
    DO:
      FIND FIRST bill-alert WHERE bill-alert.rechnr = bill.rechnr
        NO-ERROR.
      IF AVAILABLE bill-alert THEN ASSIGN bill-list.last-date = heute.               
    END.

    FIND FIRST bill-line WHERE bill-line.rechnr = bill-list.rechnr 
      NO-LOCK USE-INDEX bildat_index NO-ERROR.
    IF AVAILABLE bill-line THEN 
    DO:    
      ASSIGN bill-list.first-date = bill-line.bill-datum
             bill-list.betrag = bill-line.betrag.
      IF bill.flag = 1 AND bill-list.last-date EQ ? THEN
      DO:
        FIND LAST bill-line WHERE bill-line.rechnr = bill-list.rechnr 
          NO-LOCK USE-INDEX bildat_index NO-ERROR.
        IF AVAILABLE bill-line THEN 
          ASSIGN bill-list.last-date = bill-line.bill-datum.
      END.
    END.  

    IF bill-list.first-date = ? THEN DELETE bill-list.
    ELSE IF bill-list.first-date GT billdate THEN DELETE bill-list.
    ELSE IF bill-list.last-date LT billdate THEN DELETE bill-list.

    FIND NEXT bill WHERE bill.rechnr GT 0 NO-LOCK NO-ERROR.
  END.
END.

PROCEDURE create-umsatz:  
  DEF VAR s AS DECIMAL INITIAL 0.

  FOR EACH ns-list: 
    DELETE ns-list. 
  END. 
 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH sum-list: 
    DELETE sum-list. 
  END. 
  FOR EACH m-list: 
    DELETE m-list. 
  END. 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 

 
  IF /* billdate NE heute AND */ ank-flag THEN 
  DO:
      IF sorttype = 1 THEN
      FOR EACH bill-list WHERE bill-list.billtype = "G" 
          BY bill-list.ankunft BY bill-list.ankzeit
          BY bill-list.gname BY bill-list.zinr
          BY bill-list.billnr:
          RUN create-data2.
      END.
      ELSE
      FOR EACH bill-list WHERE bill-list.billtype = "G" 
          BY bill-list.ankunft BY bill-list.ankzeit
          BY bill-list.zinr BY bill-list.gname
          BY bill-list.billnr:
          RUN create-data2.
      END.
  END.                                   
  ELSE IF /* billdate NE heute AND */ NOT ank-flag THEN 
  DO:
      IF sorttype = 1 THEN
      FOR EACH bill-list WHERE bill-list.billtype = "G" 
          BY bill-list.gname BY bill-list.zinr
          BY bill-list.billnr:
          RUN create-data2.
      END.
      ELSE
      FOR EACH bill-list WHERE bill-list.billtype = "G" 
          BY bill-list.zinr BY bill-list.gname
          BY bill-list.billnr:
          RUN create-data2.
      END.
  END.

  FOR EACH bill-list WHERE bill-list.billtype = "M" 
      BY bill-list.rechnr:
      FIND FIRST res-line WHERE res-line.resnr = bill-list.resnr 
          AND res-line.zinr NE "" AND res-line.resstatus NE 12 
          NO-LOCK NO-ERROR. 
      CREATE m-list. 
      ASSIGN m-list.resnr = bill-list.resnr. 
      IF AVAILABLE res-line THEN 
      ASSIGN 
          m-list.zinr    = res-line.zinr 
          m-list.abreise = res-line.abreise
      .
      ASSIGN
          prevbal        = 0 
          debit          = 0 
          credit         = 0 
          balance        = 0
      . 
      FOR EACH bill-line WHERE bill-line.rechnr = bill-list.rechnr 
        AND bill-line.bill-datum LE billdate NO-LOCK BY bill-line.bezeich: 

        FIND FIRST s-list WHERE s-list.artnr = bill-line.artnr 
          AND s-list.dept = bill-line.departement 
          AND s-list.rechnr = bill-line.rechnr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement 
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = 0 NO-LOCK NO-ERROR. 
 
          CREATE s-list. 
          ASSIGN
            current-counter   = current-counter + 1
            s-list.i-counter  = current-counter
            s-list.gname      = bill-list.gname
            s-list.flag       = 1
            s-list.artnr      = bill-line.artnr 
            s-list.dept       = bill-line.departement 
            s-list.abreise    = m-list.abreise
            s-list.bill-datum = bill-line.bill-datum
            s-list.zinr       = m-list.zinr 
            s-list.rechnr     = bill-list.rechnr 
            s-list.billtyp    = "M"
            s-list.billnr     = 1
            s-list.prevbal    = 0
            s-list.balance    = balance 
          . 

          IF AVAILABLE artikel THEN s-list.bezeich = artikel.bezeich. 
          ELSE s-list.bezeich = bill-line.bezeich. 
        END.        
        IF bill-line.bill-datum LT billdate THEN 
        DO: 
          s-list.prevbal = s-list.prevbal + bill-line.betrag / fact1. 
          prevbal = prevbal + bill-line.betrag / fact1. 
          s-list.balance = s-list.balance + bill-line.betrag / fact1. 
          t-prevbal = t-prevbal + bill-line.betrag / fact1. 
        END. 
        ELSE 
        DO: 
          IF bill-line.betrag GT 0 THEN 
          DO: 
            s-list.debit = s-list.debit + bill-line.betrag / fact1. 
            debit = debit + bill-line.betrag / fact1. 
            t-debit = t-debit + bill-line.betrag / fact1. 
          END. 
          ELSE 
          DO: 
            s-list.credit = s-list.credit - bill-line.betrag / fact1. 
            credit = credit - bill-line.betrag / fact1. 
            t-credit = t-credit - bill-line.betrag / fact1. 
          END. 
          s-list.balance = s-list.balance + bill-line.betrag / fact1. 
        END. 
        balance = balance + bill-line.betrag / fact1. 
        t-balance = t-balance + bill-line.betrag / fact1. 
      END. 
  END. 
 
  /* NS Bill */ 
  FOR EACH bill-list WHERE bill-list.billtype = "N" 
    BY bill-list.gname:
    
    ASSIGN
      prevbal   = 0
      debit     = 0 
      credit    = 0 
      balance   = 0
    . 

    FOR EACH bill-line WHERE bill-line.rechnr = bill-list.rechnr 
      AND bill-line.bill-datum LE billdate NO-LOCK
      BY bill-line.bill-datum BY bill-line.artnr 
      BY bill-line.departement: 
      tot-bline = tot-bline + 1.
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR.
      IF NOT AVAILABLE artikel THEN
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = 0 NO-LOCK NO-ERROR.

      FIND FIRST s-list WHERE s-list.artnr = artikel.artnr 
        AND s-list.dept = artikel.departement 
        AND s-list.rechnr = bill-line.rechnr NO-LOCK NO-ERROR. 

      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list.
        ASSIGN
          current-counter   = current-counter + 1
          s-list.i-counter  = current-counter
          s-list.gname      = bill-list.gname
          s-list.flag       = 2
          s-list.artnr      = bill-line.artnr 
          s-list.dept       = bill-line.departement 
          s-list.rechnr     = bill-list.rechnr
          s-list.billtyp    = "NS"
          s-list.billnr     = bill-list.billnr 
          s-list.prevbal    = 0
          s-list.balance    = 0
          s-list.bill-datum = bill-line.bill-datum
        . 
        IF AVAILABLE artikel THEN s-list.bezeich = artikel.bezeich.
        ELSE s-list.bezeich = "[!] " + bill-line.bezeich.
      END. 

      IF bill-line.bill-datum LT billdate THEN 
      DO: 
        s-list.prevbal = s-list.prevbal + bill-line.betrag / fact1. 
        prevbal = prevbal + bill-line.betrag / fact1. 
        t-prevbal = t-prevbal + bill-line.betrag / fact1. 
        s-list.balance = s-list.balance + bill-line.betrag / fact1. 
      END. 
      ELSE 
      DO: 
        IF bill-line.betrag GT 0 THEN 
        DO: 
          s-list.debit = s-list.debit + bill-line.betrag / fact1. 
          debit = debit + bill-line.betrag / fact1. 
          t-debit = t-debit + bill-line.betrag / fact1. 
        END. 
        ELSE 
        DO: 
          s-list.credit = s-list.credit - bill-line.betrag / fact1. 
          credit = credit - bill-line.betrag / fact1. 
          t-credit = t-credit - bill-line.betrag / fact1. 
        END. 
        s-list.balance = s-list.balance + bill-line.betrag / fact1. 
      END. 
      balance = balance + bill-line.betrag / fact1. 
      t-balance = t-balance + bill-line.betrag / fact1. 
    END. 
  END. 

  ASSIGN outstanding = t-prevbal + t-debit - t-credit.
END.

PROCEDURE create-data2:

    ASSIGN
        prevbal = 0 
        debit   = 0 
        credit  = 0 
        balance = 0
    . 
    FOR EACH bill-line WHERE bill-line.rechnr = bill-list.rechnr 
      AND bill-line.bill-datum LE billdate NO-LOCK
      BY bill-line.bezeich
      BY bill-line.bill-datum BY bill-line.zeit: 
      tot-bline = tot-bline + 1.
      FIND FIRST s-list WHERE s-list.artnr = bill-line.artnr 
        AND s-list.dept = bill-line.departement 
        AND s-list.rechnr = bill-line.rechnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE s-list THEN 
      DO: 
        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = bill-line.departement 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        
        /*
        IF NOT AVAILABLE artikel THEN 
        DO: 

          HIDE MESSAGE NO-PAUSE. 
          MESSAGE translateExtended ("Artikel not found:", lvcAREA,"") + " " 
              + translateExtended ("Bill No:", lvcAREA,"") + " " 
              + STRING(bill-list.rechnr) + "; " 
              + translateExtended ("Article No:", lvcAREA,"") + " " 
              + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
              + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")) 
              VIEW-AS ALERT-BOX WARNING. 
        END. */

        CREATE s-list. 
        ASSIGN       
          current-counter     = current-counter + 1
          s-list.i-counter    = current-counter
          s-list.gname        = bill-list.gname
          s-list.flag         = 0
          s-list.artnr        = bill-line.artnr 
          s-list.dept         = bill-line.departement 
          s-list.zinr         = bill-list.zinr
          s-list.abreise      = bill-list.abreise 
          s-list.bill-datum   = bill-line.bill-datum
          s-list.rechnr       = bill-list.rechnr
          s-list.billtyp      = "  "
          s-list.prevbal      = 0
          s-list.balance      = 0 
          s-list.billnr       = bill-list.billnr
          s-list.ankunft      = bill-list.ankunft
          s-list.ankzeit      = STRING(bill-list.ankzeit, "HH:MM:SS")
        . 
        IF AVAILABLE artikel THEN s-list.bezeich = artikel.bezeich. 
        ELSE s-list.bezeich = bill-line.bezeich. 
      END. 
      IF bill-line.bill-datum LT billdate THEN 
      DO: 
        s-list.prevbal = s-list.prevbal + bill-line.betrag / fact1. 
        prevbal = prevbal + bill-line.betrag / fact1. 
        t-prevbal = t-prevbal + bill-line.betrag / fact1. 
      END. 
      ELSE 
      DO: 
        IF bill-line.betrag GT 0 THEN 
        DO: 
          s-list.debit = s-list.debit + bill-line.betrag / fact1. 
          debit = debit + bill-line.betrag / fact1. 
          t-debit = t-debit + bill-line.betrag / fact1. 
        END. 
        ELSE 
        DO: 
          s-list.credit = s-list.credit - bill-line.betrag / fact1. 
          credit = credit - bill-line.betrag / fact1. 
          t-credit = t-credit - bill-line.betrag / fact1. 
        END. 
      END. 
      ASSIGN
        balance        = balance + bill-line.betrag / fact1
        t-balance      = t-balance + bill-line.betrag / fact1
        s-list.balance = balance
      . 
    END. 
END.
