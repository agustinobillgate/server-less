
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

DEFINE TEMP-TABLE gacct-balance-list
    FIELD i-counter AS INTEGER INITIAL 0
    FIELD flag      AS INTEGER INITIAL 0
    FIELD artnr     AS INTEGER
    FIELD dept      AS INTEGER
    FIELD ankunft   AS DATE 
    FIELD ankzeit   AS CHAR 
    FIELD typebill  AS CHAR FORMAT "x(2)" 
    FIELD billdatum AS DATE
    FIELD guest     AS CHAR FORMAT "x(24)"
    FIELD roomno    AS CHAR FORMAT "x(4)"
    FIELD billno    AS INT  FORMAT ">>>>>>>"
    FIELD billnr    AS INTEGER FORMAT "9"
    FIELD bezeich   AS CHAR FORMAT "x(16)"
    FIELD prevbala  AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD debit     AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD credit    AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD balance   AS DEC  FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD depart    AS DATE
    .

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

DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR bill-alert.
DEF INPUT  PARAMETER heute         AS DATE.
DEF INPUT  PARAMETER billdate      AS DATE.
DEF INPUT  PARAMETER ank-flag      AS LOGICAL.
DEF INPUT  PARAMETER sorttype      AS INT.
DEF INPUT  PARAMETER fact1         AS INT.
DEF INPUT  PARAMETER price-decimal AS INT.
DEF INPUT  PARAMETER short-flag    AS LOGICAL.
DEF OUTPUT PARAMETER msg-str       AS CHAR.
DEF OUTPUT PARAMETER msg-str2      AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR gacct-balance-list.

/*
DEFINE VARIABLE pvILanguage AS INTEGER NO-UNDO INITIAL ?.
/*DEFINE VARIABLE TABLE FOR bill-alert.*/
DEFINE VARIABLE heute         AS DATE INITIAL 09/20/24.
DEFINE VARIABLE billdate      AS DATE INITIAL 09/01/24.
DEFINE VARIABLE ank-flag      AS LOGICAL INITIAL NO.
DEFINE VARIABLE sorttype      AS INT INITIAL 0.
DEFINE VARIABLE fact1         AS INT INITIAL 1.
DEFINE VARIABLE price-decimal AS INT INITIAL 0.
DEFINE VARIABLE short-flag    AS LOGICAL INITIAL YES.
DEFINE VARIABLE msg-str       AS CHAR INITIAL "".
DEFINE VARIABLE msg-str2      AS CHAR INITIAL "".
DEFINE VARIABLE idFlag         AS CHAR INITIAL "". */

DEFINE VARIABLE i               AS INTEGER. 
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
DEFINE VARIABLE jl              AS INTEGER INITIAL 0.

DEFINE BUFFER bline FOR bill-line.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gacct-balance".

ASSIGN
      tot-bline       = 0
      current-counter = 0
      t-prevbal       = 0
      t-debit         = 0
      t-credit        = 0
      t-balance       = 0
  .

msg-str = "success".

MESSAGE "display update" VIEW-AS ALERT-BOX.
RUN create-bill-list.
RUN create-umsatz. 

PROCEDURE create-bill-list:

  DEFINE VARIABLE first-date AS DATE.
  DEFINE VARIABLE last-date AS DATE.
  DEFINE VARIABLE rbilldate AS DATE.

  rbilldate = billdate - 30.


  FOR EACH bill-list:
      DELETE bill-list.
  END.

  FOR EACH bill WHERE bill.rechnr GT 0 AND (bill.flag = 0 OR (bill.datum GE rbilldate AND bill.flag = 1)) NO-LOCK USE-INDEX rechnr_index
    BY bill.rechnr:
  /*FOR EACH bill WHERE bill.rechnr GT 0 AND bill.datum GE billdate NO-LOCK USE-INDEX rechnr_index:*/
    ASSIGN
      last-date = ?
      first-date = ?.

    IF bill.flag = 0 THEN last-date = heute. 

    IF bill.flag = 1 THEN
    DO:
      FIND FIRST bill-alert WHERE bill-alert.rechnr = bill.rechnr
        NO-ERROR.
      IF AVAILABLE bill-alert THEN last-date = heute.               
    END.

    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK BY bill-line.bill-datum:
      first-date = bill-line.bill-datum.
      LEAVE.
    END.

    /*FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK USE-INDEX bildat_index.
    IF AVAILABLE bill-line THEN first-date = bill-line.bill-datum.*/

    IF bill.flag = 1 AND last-date EQ ? THEN 
    DO:
      FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK BY bill-line.bill-datum DESC:
          last-date = bill-line.bill-datum.
          LEAVE.
      END.
      /*FIND LAST bline WHERE bline.rechnr = bill.rechnr 
          NO-LOCK USE-INDEX bildat_index NO-ERROR.
      IF AVAILABLE bline THEN last-date = bline.bill-datum.*/
    END.  

    IF first-date = ? THEN NEXT.
    ELSE IF first-date GT billdate THEN NEXT.
    ELSE IF last-date LT billdate THEN NEXT.

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
    
    IF bill-list.gname = "" THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK
          NO-ERROR.
      IF AVAILABLE guest THEN bill-list.gname = guest.NAME.
    END.
  END.
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

        /*IF NOT AVAILABLE artikel THEN 
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

  FOR EACH gacct-balance-list.
      DELETE gacct-balance-list.
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
 
          /*IF NOT AVAILABLE artikel THEN 
          DO: 
              HIDE MESSAGE NO-PAUSE. 
              MESSAGE translateExtended ("Artikel not found:", lvcAREA,"") + " " 
                  + translateExtended ("Bill No:", lvcAREA,"") + " " 
                  + STRING(bill-list.rechnr) + "; " 
                  + translateExtended ("Article No:", lvcAREA,"") + " " 
                  + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
                  + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")) 
                  VIEW-AS ALERT-BOX WARNING. 
          END.*/ 
 
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
  
  ASSIGN
    curr-rechnr = 0 
    curr-flag   = 0
    balance     = 0
  . 
 
  FOR EACH s-list /*BY s-list.rechnr*/ BY s-list.i-counter: 
      IF s-list.debit NE 0 OR s-list.credit NE 0 THEN 
      DO: 
        FIND FIRST sum-list WHERE sum-list.bezeich = s-list.bezeich NO-ERROR. 
        IF NOT AVAILABLE sum-list THEN 
        DO: 
          CREATE sum-list. 
          sum-list.bezeich = s-list.bezeich. 
        END. 
        sum-list.debit   = sum-list.debit + s-list.debit. 
        sum-list.credit  = sum-list.credit + s-list.credit. 
        sum-list.balance = sum-list.balance + s-list.debit - s-list.credit. 
      END. 
      IF curr-rechnr NE s-list.rechnr THEN 
      DO: 
        ASSIGN
          balance = s-list.prevbal + s-list.debit - s-list.credit
          s-list.balance = balance
        .
        IF curr-rechnr NE 0 THEN 
        DO:
          CREATE gacct-balance-list. 
        END.
            
        CREATE gacct-balance-list. 
        ASSIGN
          gacct-balance-list.ankunft    = s-list.ankunft
          gacct-balance-list.ankzeit    = s-list.ankzeit
          gacct-balance-list.depart     = s-list.abreise
          gacct-balance-list.typebill   = s-list.billtyp
          gacct-balance-list.guest      = s-list.gname
          gacct-balance-list.roomno     = s-list.zinr
          gacct-balance-list.billno     = s-list.rechnr
        .

        IF price-decimal = 0 THEN
        DO:
          IF short-flag THEN
          DO:
            ASSIGN
              gacct-balance-list.bezeich  = s-list.bezeich
              gacct-balance-list.prevbala = s-list.prevbal
              gacct-balance-list.debit    = s-list.debit
              gacct-balance-list.credit   = s-list.credit 
              gacct-balance-list.balance  = s-list.balance
            .
          END.
          ELSE
          DO:
            ASSIGN
              gacct-balance-list.bezeich  = s-list.bezeich
              gacct-balance-list.prevbala = s-list.prevbal
              gacct-balance-list.debit    = s-list.debit
              gacct-balance-list.credit   = s-list.credit 
              gacct-balance-list.balance  = s-list.balance
            .
          END.
        END.
        ELSE
        DO:
          ASSIGN
            gacct-balance-list.bezeich  = s-list.bezeich
            gacct-balance-list.prevbala = s-list.prevbal
            gacct-balance-list.debit    = s-list.debit
            gacct-balance-list.credit   = s-list.credit 
            gacct-balance-list.balance  = s-list.balance
          .
        END.
        curr-rechnr = gacct-balance-list.billno.
      END. 
      ELSE 
      DO: 
        ASSIGN
          balance = balance + s-list.prevbal + s-list.debit - s-list.credit
          s-list.balance = balance
        .

        CREATE gacct-balance-list. 
        ASSIGN
          gacct-balance-list.ankunft = s-list.ankunft
          gacct-balance-list.ankzeit = s-list.ankzeit
        .

        IF price-decimal = 0 THEN
        DO:
          IF short-flag THEN
          DO:
            ASSIGN
              gacct-balance-list.bezeich  = s-list.bezeich
              gacct-balance-list.prevbala = s-list.prevbal
              gacct-balance-list.debit    = s-list.debit
              gacct-balance-list.credit   = s-list.credit 
              gacct-balance-list.balance  = s-list.balance
            .
          END.
          ELSE
          DO:
            ASSIGN
              gacct-balance-list.bezeich  = s-list.bezeich
              gacct-balance-list.prevbala = s-list.prevbal
              gacct-balance-list.debit    = s-list.debit
              gacct-balance-list.credit   = s-list.credit 
              gacct-balance-list.balance  = s-list.balance
            .
          END.
        END.
        ELSE
        DO:
          ASSIGN
            gacct-balance-list.bezeich  = s-list.bezeich
            gacct-balance-list.prevbala = s-list.prevbal
            gacct-balance-list.debit    = s-list.debit
            gacct-balance-list.credit   = s-list.credit 
            gacct-balance-list.balance  = s-list.balance
          .
        END.      
      END. 
      /*DELETE gacct-balance-list. */
  END.

  CREATE gacct-balance-list.
  IF price-decimal = 0 THEN
  DO:
      IF short-flag THEN
      DO:
        ASSIGN
          gacct-balance-list.bezeich  = "T O T A L"
          gacct-balance-list.prevbala = t-prevbal
          gacct-balance-list.debit    = t-debit
          gacct-balance-list.credit   = t-credit 
          gacct-balance-list.balance  = t-balance
        .
      END.
      ELSE
      DO:
        ASSIGN
          gacct-balance-list.bezeich  = "T O T A L"
          gacct-balance-list.prevbala = t-prevbal 
          gacct-balance-list.debit    = t-debit   
          gacct-balance-list.credit   = t-credit  
          gacct-balance-list.balance  = t-balance 
        .
      END.
  END.
  ELSE
  DO:
    ASSIGN
      gacct-balance-list.bezeich  = "T O T A L"
      gacct-balance-list.prevbala = t-prevbal 
      gacct-balance-list.debit    = t-debit   
      gacct-balance-list.credit   = t-credit  
      gacct-balance-list.balance  = t-balance 
    .
  END.
 
  CREATE gacct-balance-list. 
  CREATE gacct-balance-list.
  FIND FIRST uebertrag WHERE uebertrag.datum = billdate NO-LOCK NO-ERROR.
  IF price-decimal = 0 THEN
  DO:
    ASSIGN
      gacct-balance-list.bezeich = "Outstanding"
      gacct-balance-list.balance = t-prevbal + t-debit - t-credit
    .
    IF AVAILABLE uebertrag THEN
    DO:
      CREATE gacct-balance-list.
      ASSIGN
        gacct-balance-list.bezeich = "Stored Guest Ledger Amount:"
        gacct-balance-list.balance = uebertrag.betrag
      .
    END.
  END.
  ELSE
  DO:
    ASSIGN
      gacct-balance-list.bezeich = "Outstanding"
      gacct-balance-list.balance = t-prevbal + t-debit - t-credit
    .
    IF AVAILABLE uebertrag THEN
    DO:
      CREATE gacct-balance-list.
      ASSIGN
        gacct-balance-list.bezeich = "Stored Guest Ledger Amount:"
        gacct-balance-list.balance = uebertrag.betrag
      .
    END.
  END.
/* 
  CREATE output-list. 
  DO i = 1 TO 99: 
    output-list.str = output-list.str + "-". 
  END. 
*/ 
  CREATE gacct-balance-list. 
  CREATE gacct-balance-list. 
   
  gacct-balance-list.guest = "Summary of Transaction". 
  t-debit = 0. 
  t-credit = 0. 
  t-balance = 0. 
  FOR EACH sum-list BY sum-list.bezeich: 
    CREATE gacct-balance-list. 
    gacct-balance-list.guest = sum-list.bezeich. 
    
    IF price-decimal = 0 THEN
    DO:
      IF short-flag THEN
      DO:
        ASSIGN
          gacct-balance-list.debit    = sum-list.debit
          gacct-balance-list.credit   = sum-list.credit
          gacct-balance-list.balance  = sum-list.balance
        .
      END.
      ELSE
      DO:
        ASSIGN
          gacct-balance-list.debit    = sum-list.debit
          gacct-balance-list.credit   = sum-list.credit
          gacct-balance-list.balance  = sum-list.balance
        .
      END.
    END.
    ELSE
    DO:
      ASSIGN
        gacct-balance-list.debit    = sum-list.debit
        gacct-balance-list.credit   = sum-list.credit
        gacct-balance-list.balance  = sum-list.balance
      .      
    END.
    t-debit = t-debit + sum-list.debit.   
    t-credit = t-credit + sum-list.credit.
  END. 
  t-balance = t-debit - t-credit. 
  
  CREATE gacct-balance-list. 
  gacct-balance-list.guest = "T o t a l". 
   
  IF price-decimal = 0 THEN
  DO:
    IF short-flag THEN
    DO:
      ASSIGN
        gacct-balance-list.debit   = t-debit 
        gacct-balance-list.credit  = t-credit
        gacct-balance-list.balance = t-balance
      .
    END.
    ELSE
    DO:
      ASSIGN
        gacct-balance-list.debit   = t-debit 
        gacct-balance-list.credit  = t-credit
        gacct-balance-list.balance = t-balance
      .
    END.
  END.
  ELSE
  DO:
    ASSIGN
        gacct-balance-list.debit   = t-debit 
        gacct-balance-list.credit  = t-credit
        gacct-balance-list.balance = t-balance
      .
  END.
END. 


/****MT
PROCEDURE create-bill-list:

  FOR EACH bill-list:
      DELETE bill-list.
  END.

  FOR EACH bill WHERE bill.rechnr GT 0 NO-LOCK:
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
      ASSIGN bill-list.first-date = bill-line.bill-datum.
      IF bill.flag = 1 AND bill-list.last-date EQ ? THEN
      DO:
        FIND LAST bill-line WHERE bill-line.rechnr = bill-list.rechnr 
          NO-LOCK USE-INDEX bildat_index NO-ERROR.
        IF AVAILABLE bill-line THEN 
          ASSIGN bill-list.last-date = bill-line.bill-datum.
      END.
    END.
  
  END.
  
  FOR EACH bill-list:
     IF bill-list.first-date = ? THEN DELETE bill-list.
     ELSE IF bill-list.first-date GT billdate THEN DELETE bill-list.
     ELSE IF bill-list.last-date LT billdate THEN DELETE bill-list.
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
          AND s-list.rechnr = bill-line.rechnr NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement 
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = 0 NO-LOCK NO-ERROR. 
 
          IF NOT AVAILABLE artikel THEN 
          DO: 
              msg-str = msg-str + CHR(2) + "&W"
                      + translateExtended ("Artikel not found:", lvcAREA,"") + " " 
                      + translateExtended ("Bill No:", lvcAREA,"") + " " 
                      + STRING(bill-list.rechnr) + "; " 
                      + translateExtended ("Article No:", lvcAREA,"") + " " 
                      + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
                      + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")).
          END. 
 
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
        AND s-list.rechnr = bill-line.rechnr NO-ERROR. 

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
  
  ASSIGN
    curr-rechnr = 0 
    curr-flag   = 0
    balance     = 0
  . 
 
  FOR EACH s-list BY s-list.i-counter: 

      IF s-list.debit NE 0 OR s-list.credit NE 0 THEN 
      DO: 
        FIND FIRST sum-list WHERE sum-list.bezeich = s-list.bezeich NO-ERROR. 
        IF NOT AVAILABLE sum-list THEN 
        DO: 
          CREATE sum-list. 
          sum-list.bezeich = s-list.bezeich. 
        END. 
        sum-list.debit   = sum-list.debit + s-list.debit. 
        sum-list.credit  = sum-list.credit + s-list.credit. 
        sum-list.balance = sum-list.balance + s-list.debit - s-list.credit. 
      END. 
      IF curr-rechnr NE s-list.rechnr THEN 
      DO: 
        ASSIGN
          balance = s-list.prevbal + s-list.debit - s-list.credit
          s-list.balance = balance
        .
        IF curr-rechnr NE 0 THEN CREATE output-list. 
        CREATE output-list. 
        ASSIGN
          output-list.ankunft = s-list.ankunft
          output-list.ankzeit = s-list.ankzeit
        .
        output-list.str = STRING(s-list.billtyp, "x(2)") 
        + STRING(s-list.gname, "x(24)") 
        + STRING(s-list.zinr, "x(6)") 
        + STRING(s-list.rechnr, ">>>>>>9"). 
        IF price-decimal = 0 THEN 
        DO: 
          IF short-flag THEN output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
          + STRING(s-list.prevbal, "->,>>>,>>>,>>9") 
          + STRING(s-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
          + STRING(s-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
          + STRING(s-list.balance, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/
          ELSE output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
          + STRING(s-list.prevbal, "->>>>>>>>>>>>9") 
          + STRING(s-list.debit, ">>>>>>>>>>>>>>9") /*IT 100513*/
          + STRING(s-list.credit, ">>>>>>>>>>>>>9") /*IT 100513*/
          + STRING(s-list.balance, "->>>>>>>>>>>>>>>>9"). /*IT 100513*/ 
        END. 
        ELSE 
        output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
        + STRING(s-list.prevbal, "->>,>>>,>>9.99") 
        + STRING(s-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(s-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(s-list.balance, "->>,>>>,>>>,>>9.99"). /*IT 100513*/
        IF s-list.abreise NE ? THEN output-list.str = output-list.str + STRING(s-list.abreise). 
        ELSE output-list.str = output-list.str + STRING("","x(8)"). 
        curr-rechnr = s-list.rechnr. 
      END. 
      ELSE 
      DO: 
        ASSIGN
          balance = balance + s-list.prevbal + s-list.debit - s-list.credit
          s-list.balance = balance
        .
        CREATE output-list. 
        ASSIGN
          output-list.ankunft = s-list.ankunft
          output-list.ankzeit = s-list.ankzeit
        .
        output-list.str = STRING("", "x(39)"). 
        IF price-decimal = 0 THEN 
        DO: 
          IF short-flag THEN output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
          + STRING(s-list.prevbal, "->,>>>,>>>,>>9") 
          + STRING(s-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
          + STRING(s-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
          + STRING(s-list.balance, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/
          ELSE output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
          + STRING(s-list.prevbal, "->>>>>>>>>>>>9") 
        + STRING(s-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(s-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(s-list.balance, "->>,>>>,>>>,>>9.99").  /*IT 100513*/
        END. 
        ELSE 
        output-list.str = output-list.str + STRING(s-list.bezeich, "x(16)") 
        + STRING(s-list.prevbal, "->>,>>>,>>9.99") 
        + STRING(s-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(s-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(s-list.balance, "->>,>>>,>>>,>>9.99").  /*IT 100513*/
      END. 
      DELETE s-list.
  END. 
  
  CREATE output-list. 
  DO i = 1 TO 118: 
    output-list.str = output-list.str + "-". 
  END. 
  CREATE output-list. 
  output-list.str = STRING("", "x(39)"). 
  
  IF price-decimal = 0 THEN 
  DO: 
    IF short-flag THEN output-list.str = output-list.str + STRING("T o t a l", "x(16)") 
        + STRING(t-prevbal, "->,>>>,>>>,>>9") 
        + STRING(t-debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-balance, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/ 
    ELSE output-list.str = output-list.str + STRING("T o t a l", "x(16)") 
        + STRING(t-prevbal, "->>>>>>>>>>>>9") 
        + STRING(t-debit,   ">>>>>>>>>>>>>>9") /*IT 100513*/
        + STRING(t-credit,  ">>>>>>>>>>>>>>9") /*IT 100513*/
        + STRING(t-balance, "->>>>>>>>>>>>>>>>9"). /*IT 100513*/
  END. 
  ELSE 
  output-list.str = output-list.str + STRING("T o t a l", "x(16)") 
        + STRING(t-prevbal, "->>,>>>,>>9.99") 
        + STRING(t-debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-balance, "->>,>>>,>>>,>>9.99"). /*IT 100513*/
  
  CREATE output-list. 
  DO i = 1 TO 118: 
    output-list.str = output-list.str + "-". 
  END. 
  CREATE output-list. 
  output-list.str = STRING("", "x(39)"). 
  IF price-decimal = 0 THEN 
  DO: 
    FIND FIRST uebertrag WHERE uebertrag.datum = billdate NO-LOCK NO-ERROR.
    output-list.str = output-list.str + STRING("Outstanding", "x(16)") 
        + STRING(0, "->>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING((t-prevbal + t-debit - t-credit), "->,>>>,>>>,>>>,>>9"). /*IT 100513*/
    IF AVAILABLE uebertrag THEN
    DO:
      CREATE output-list. 
      output-list.str = STRING("", "x(39)"). 
      output-list.str = output-list.str + STRING("Stored Guest Ledger Amount:", "x(30)") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>,>>>>>>") 
        + STRING(uebertrag.betrag, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/
    END.
  END.
  ELSE 
  DO:
    output-list.str = output-list.str + STRING("T o t a l", "x(18)") 
        + STRING(0, "->>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING((t-prevbal + t-debit - t-credit), "->,>>>,>>>,>>9.99"). /*IT 100513*/
    IF AVAILABLE uebertrag THEN
    DO:
      CREATE output-list. 
      output-list.str = STRING("", "x(39)"). 
      output-list.str = output-list.str + STRING("Stored Guest Ledger Amount:", "x(30)") 
        + STRING(0, ">>>>>>>>>>>>>") 
        + STRING(0, ">>>>>>,>>>>>>") 
        + STRING(uebertrag.betrag, "->>,>>>,>>9.99"). 
    END.
  END.
/* 
  CREATE output-list. 
  DO i = 1 TO 99: 
    output-list.str = output-list.str + "-". 
  END. 
*/ 
  CREATE output-list. 
  CREATE output-list. 
  output-list.str = "  Summary of Transaction". 
  CREATE output-list. 
  DO i = 1 TO 118: 
    output-list.str = output-list.str + "-". 
  END. 
  t-debit = 0. 
  t-credit = 0. 
  t-balance = 0. 
  FOR EACH sum-list BY sum-list.bezeich: 
    CREATE output-list. 
    output-list.str = "  " + STRING(sum-list.bezeich, "x(26)"). 
    DO i = 1 TO 41: 
      output-list.str = output-list.str + " ". 
    END. 
    IF price-decimal = 0 THEN 
    DO: 
      IF short-flag THEN output-list.str = output-list.str 
        + STRING(sum-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(sum-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(sum-list.balance, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/
      ELSE output-list.str = output-list.str 
        + STRING(sum-list.debit, ">>>>>>>>>>>>>>9") 
        + STRING(sum-list.credit, ">>>>>>>>>>>>>9") 
        + STRING(sum-list.balance, "->>>>>>>>>>>>>>>>9"). /*IT 100513*/
    END. 
    ELSE output-list.str = output-list.str 
        + STRING(sum-list.debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(sum-list.credit, ">>>,>>>,>>>,>>9") /*IT 100513*/ 
        + STRING(sum-list.balance, "->>,>>>,>>>,>>9.99"). /*IT 100513*/ 
    t-debit = t-debit + sum-list.debit. 
    t-credit = t-credit + sum-list.credit. 
  END. 
  t-balance = t-debit - t-credit. 
  CREATE output-list. 
  DO i = 1 TO 118: 
    output-list.str = output-list.str + "-". 
  END. 
  CREATE output-list. 
  output-list.str = "  " + STRING("T o t a l", "x(26)"). 
  DO i = 1 TO 41: 
    output-list.str = output-list.str + " ". 
  END. 
  IF price-decimal = 0 THEN 
  DO: 
    IF short-flag THEN output-list.str = output-list.str 
        + STRING(t-debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-balance, "->,>>>,>>>,>>>,>>9"). /*IT 100513*/ 
    ELSE output-list.str = output-list.str 
        + STRING(t-debit, ">>>>>>>>>>>>>>9")  /*IT 100513*/
        + STRING(t-credit, ">>>>>>>>>>>>>>9") /*IT 100513*/
        + STRING(t-balance, "->>>>>>>>>>>>>>>>9"). /*IT 100513*/ 
  END. 
  ELSE output-list.str = output-list.str 
        + STRING(t-debit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-credit, ">>>,>>>,>>>,>>9") /*IT 100513*/
        + STRING(t-balance, "->>,>>>,>>>,>>9.99"). /*IT 100513*/ 
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
        AND s-list.rechnr = bill-line.rechnr NO-ERROR.
      IF NOT AVAILABLE s-list THEN 
      DO: 
        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = bill-line.departement 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
        FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 

        IF NOT AVAILABLE artikel THEN 
        DO: 
          msg-str2 = msg-str2 + CHR(2) + "&W"
                   + translateExtended ("Artikel not found:", lvcAREA,"") + " " 
                   + translateExtended ("Bill No:", lvcAREA,"") + " " 
                   + STRING(bill-list.rechnr) + "; " 
                   + translateExtended ("Article No:", lvcAREA,"") + " " 
                   + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
                   + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")).
        END. 

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
*/
