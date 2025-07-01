

DEFINE TEMP-TABLE sumcsr-list
    FIELD reihe     AS INTEGER
    FIELD flag      AS INTEGER
    FIELD artart    AS INTEGER
    FIELD dept      AS CHARACTER FORMAT "x(24)"
    FIELD cash      AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD rmfobill  AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD card      AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD CL        AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD revenue   AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD compli    AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD mealcou   AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    FIELD outstand  AS CHARACTER FORMAT "x(19)"   /*FORMAT "->>,>>>,>>>,>>9.99"*/
    .

DEFINE TEMP-TABLE output-list 
  FIELD reihe  AS INTEGER
  FIELD flag   AS INTEGER 
  FIELD artart AS INTEGER 
  FIELD STR    AS CHAR
. 

DEFINE TEMP-TABLE cash-list
    FIELD artnr   AS INTEGER
    FIELD bezeich AS CHAR
    FIELD betrag  AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>>,>>9.99"
.

DEFINE TEMP-TABLE rechnr-list 
  FIELD rechnr AS INTEGER. 
  
DEFINE TEMP-TABLE art-list 
  FIELD artnr   AS INTEGER 
  FIELD artart  AS INTEGER 
  FIELD dept    AS INTEGER 
  FIELD bezeich AS CHAR 
  FIELD revenue AS DECIMAL
. 
 
DEFINE TEMP-TABLE cl-list 
  FIELD begin   AS LOGICAL INITIAL NO
  FIELD flag    AS INTEGER 
  FIELD artnr   AS INTEGER 
  FIELD artart  AS INTEGER 
  FIELD dept    AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(20)" 
  FIELD cash    AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD room    AS DECIMAL FORMAT " ->>,>>>,>>>,>>9.99" 
  FIELD card    AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD cl      AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD gl      AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD revenue AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD compli  AS DECIMAL FORMAT " ->>,>>>,>>9.99" 
  FIELD mcoupon AS DECIMAL FORMAT " ->>,>>>,>>9.99". 

DEFINE INPUT PARAMETER pvILanguage   AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER to-date       AS DATE         NO-UNDO.
DEFINE INPUT PARAMETER short-flag    AS LOGICAL      NO-UNDO. 
DEFINE INPUT PARAMETER foreign-flag  AS LOGICAL      NO-UNDO. 

DEFINE OUTPUT PARAMETER msg-str      AS CHAR INIT "" NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR sumcsr-list.
/* 
DEFINE VARIABLE pvILanguage   AS INTEGER NO-UNDO INITIAL 1.
DEFINE VARIABLE to-date       AS DATE    NO-UNDO INITIAL 01/13/19.
DEFINE VARIABLE short-flag    AS LOGICAL NO-UNDO INITIAL YES. 
DEFINE VARIABLE foreign-flag  AS LOGICAL NO-UNDO INITIAL NO. 
DEFINE VARIABLE msg-str       AS CHAR NO-UNDO.
*/
DEFINE VARIABLE long-digit      AS LOGICAL INIT NO   NO-UNDO.
DEFINE VARIABLE curr-dept       AS INTEGER           NO-UNDO. 
DEFINE VARIABLE price-decimal   AS INTEGER INIT 0    NO-UNDO.
DEFINE VARIABLE curr-bez        AS CHAR              NO-UNDO. 
DEFINE VARIABLE foreign-curr    AS CHAR              NO-UNDO. 
DEFINE VARIABLE from-date       AS DATE              NO-UNDO. 
DEFINE VARIABLE fact1           AS DECIMAL INIT 1    NO-UNDO.
DEFINE VARIABLE curr-tot-cash   AS DECIMAL           NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sum-cashier". 

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

ASSIGN from-date = DATE(month(to-date), 1, year(to-date)). 

RUN create-umsatz.

PROCEDURE create-umsatz: 
DEFINE VARIABLE cash        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE cc          AS DECIMAL NO-UNDO. 
DEFINE VARIABLE cl          AS DECIMAL NO-UNDO. 
DEFINE VARIABLE compli      AS DECIMAL NO-UNDO. 
DEFINE VARIABLE mcoup       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE rest        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE room        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE i           AS INTEGER NO-UNDO. 
DEFINE VARIABLE curr-flag   AS INTEGER NO-UNDO. 
 
DEFINE VARIABLE t1-cash     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-cc       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-cl       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-compli   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-mcoup    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-room     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-revenue  AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t1-gl       AS DECIMAL NO-UNDO. 
 
DEFINE VARIABLE t2-cash     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-cc       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-cl       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-compli   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-mcoup    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-room     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-revenue  AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t2-gl       AS DECIMAL NO-UNDO. 
 
DEFINE VARIABLE t-cash      AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-cc        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-cl        AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-compli    AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-mcoup     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-room      AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-revenue   AS DECIMAL NO-UNDO. 
DEFINE VARIABLE t-gl        AS DECIMAL NO-UNDO. 

DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO. 
DEFINE VARIABLE exchg-rate  AS DECIMAL NO-UNDO.
 
DEFINE VARIABLE amount          AS DECIMAL                      NO-UNDO. 
DEFINE VARIABLE deposit-artnr   AS INTEGER                      NO-UNDO. 
DEFINE VARIABLE deposit-baartnr AS INTEGER                      NO-UNDO.
DEFINE VARIABLE deposit-outlet  AS INTEGER                      NO-UNDO.
DEFINE VARIABLE found-depo-outlet AS LOGICAL INITIAL NO         NO-UNDO.

DEFINE VARIABLE deposit-bez     AS CHAR INITIAL "Deposit (Rsv)" NO-UNDO. 
DEFINE VARIABLE depo-foreign    AS LOGICAL INITIAL NO           NO-UNDO.  
DEFINE VARIABLE banquet-dept    AS INTEGER INITIAL -1           NO-UNDO. 
DEFINE VARIABLE deposit-babez   AS CHAR INITIAL "Deposit (Bqt)" NO-UNDO. 
DEFINE VARIABLE deposit-outbez  AS CHAR INITIAL "Deposit (Outlet)" NO-UNDO.

DEFINE BUFFER bline         FOR bill-line. 
DEFINE BUFFER h-bline       FOR bill-line. 
DEFINE BUFFER depobuff      FOR artikel.
DEFINE BUFFER buff-bline    FOR bill-line.

 
  ASSIGN
    t-cash      = 0 
    t-cc        = 0 
    t-cl        = 0 
    t-compli    = 0 
    t-mcoup     = 0 
    t-revenue   = 0 
    t-room      = 0 
    t-gl        = 0  
    t1-cash     = 0 
    t1-cc       = 0 
    t1-cl       = 0 
    t1-compli   = 0 
    t1-mcoup    = 0 
    t1-revenue  = 0 
    t1-room     = 0 
    t1-gl       = 0  
    t2-cash     = 0 
    t2-cc       = 0 
    t2-cl       = 0 
    t2-compli   = 0 
    t2-mcoup    = 0 
    t2-revenue  = 0 
    t2-room     = 0 
    t2-gl       = 0
  . 
 
  FOR EACH output-list: 
    DELETE output-list. 
  END. 
  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
  FOR EACH cash-list:
      DELETE cash-list.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
  deposit-artnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST artikel WHERE artikel.artnr = deposit-artnr 
    AND artikel.departement = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE artikel THEN 
      ASSIGN
      deposit-bez = artikel.bezeich
      depo-foreign = artikel.pricetab. 
 
  /*FDL July 11, 2023 => Ticket C9FDA6*/
  FIND FIRST htparam WHERE htparam.paramnr = 1361 NO-LOCK. 
  deposit-outlet = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST artikel WHERE artikel.artnr = deposit-outlet 
    AND artikel.departement = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE artikel THEN ASSIGN deposit-outbez = artikel.bezeich.

  FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK.
  IF htparam.finteger NE 0 THEN banquet-dept = htparam.finteger.
  FIND FIRST htparam WHERE htparam.paramnr = 117 NO-LOCK. 
  deposit-baartnr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST depobuff WHERE depobuff.artnr = deposit-baartnr 
    AND depobuff.departement = banquet-dept 
    AND depobuff.artart = 5 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE depobuff THEN
  FIND FIRST depobuff WHERE depobuff.artnr = deposit-baartnr 
    AND depobuff.departement = 0 
    AND depobuff.artart = 5 NO-LOCK NO-ERROR. 
  IF AVAILABLE depobuff THEN deposit-babez = depobuff.bezeich. 

  
/* guest folio  + Master Bill --> revenue */ 
  FOR EACH bill WHERE ((bill.flag = 0 AND bill.datum GE to-date) 
    OR (bill.flag = 1 AND bill.datum GE to-date)) AND bill.resnr GT 0 NO-LOCK, 
    FIRST bline WHERE bline.rechnr = bill.rechnr 
    AND bline.bill-datum = to-date NO-LOCK: 
    curr-dept = bill.rechnr. 
    
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr 
      AND bill-line.bill-datum = to-date NO-LOCK: 
 
      IF foreign-flag THEN amount = bill-line.fremdwbetrag. 
      ELSE amount = bill-line.betrag.            
 
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 
 
      IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = 0 NO-LOCK NO-ERROR. 
      
/* 
   NOT AVAILABLE means: transfer from outlet, AND will be handled BY 
   h-bill-line (artnr = 0) 
*/ 
      IF NOT AVAILABLE artikel THEN 
      DO: 
          msg-str = msg-str + "&W" 
              + translateExtended ("Artikel not found:", lvcAREA,"") + " "
              + translateExtended ("Bill No:", lvcAREA,"") + " " 
              + STRING(bill.rechnr) + "; " 
              + translateExtended ("Article No:", lvcAREA,"") + " " 
              + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
              + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")) 
              .
      END. 
 
      IF AVAILABLE artikel THEN 
      DO: 
        IF artikel.artart = 0 OR artikel.artart = 8 
          OR artikel.artart = 9 OR artikel.artart = 5 THEN 
        DO: 
          do-it = YES.
          IF artikel.artart = 5 AND artikel.departement = 0
              AND bill-line.userinit = "$$" THEN do-it = NO.
          IF do-it THEN
          DO:
            curr-bez = artikel.bezeich. 
            
            FIND FIRST cl-list WHERE cl-list.artnr = artikel.artnr 
              AND cl-list.dept = artikel.departement NO-ERROR. 
            IF NOT AVAILABLE cl-list THEN 
            DO: 
              CREATE cl-list. 
              ASSIGN
                cl-list.flag = -1
                cl-list.artart = artikel.umsatzart 
                cl-list.artnr = artikel.artnr
                cl-list.dept = artikel.departement 
                cl-list.bezeich = STRING(artikel.departement,"99 ") + 
                  STRING(artikel.bezeich, "x(21)")
             . 
            END.
            ASSIGN
              cl-list.room = cl-list.room + amount / fact1
              cl-list.revenue = cl-list.revenue + amount / fact1 
              t1-revenue = t1-revenue + amount / fact1
              t1-room = t1-room + amount / fact1
              t-room = t-room + amount / fact1
            . 
          END.
        END. 
        ELSE IF artikel.artart = 2 OR artikel.artart = 6 OR artikel.artart = 7 
          OR artikel.artart = 11 OR artikel.artart = 12 THEN 
        DO: 
          IF artikel.artart = 6 THEN
          DO:
            FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
            IF NOT AVAILABLE cash-list THEN
            DO:
              CREATE cash-list.
              ASSIGN
                  cash-list.artnr = artikel.artnr
                  cash-list.bezeich = artikel.bezeich
              .
            END.
            
            cash-list.betrag = cash-list.betrag - amount / fact1.
          END.

          FIND FIRST cl-list WHERE cl-list.artnr = artikel.artnr 
            AND cl-list.dept = artikel.departement NO-ERROR. 
          IF NOT AVAILABLE cl-list THEN 
          DO: 
            CREATE cl-list. 
            cl-list.flag = 200. 
            cl-list.artnr = artikel.artnr. 
            cl-list.dept = artikel.departement. 
            cl-list.bezeich = STRING(artikel.bezeich, "x(19)"). 
          END. 
          
          cl-list.revenue = cl-list.revenue - amount / fact1. 
          t2-revenue = t2-revenue - amount / fact1. 
          IF artikel.artart = 2 THEN 
          DO: 
            cl-list.cl = cl-list.cl - amount / fact1. 
            t2-cl = t2-cl - amount / fact1. 
            t-cl = t-cl - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 6 THEN 
          DO: 
            cl-list.cash = cl-list.cash - amount / fact1. 
            t2-cash = t2-cash - amount / fact1. 
            t-cash = t-cash - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 7 THEN 
          DO: 
            cl-list.card = cl-list.card - amount / fact1. 
            t2-cc = t2-cc - amount / fact1. 
            t-cc = t-cc - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 11 THEN 
          DO: 
            cl-list.compli = cl-list.compli - amount / fact1. 
            t2-compli = t2-compli - amount / fact1. 
            t-compli = t-compli - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 12 THEN 
          DO: 
            cl-list.mcoupon = cl-list.mcoupon - amount / fact1. /*Alder - Serverless - Issue 631*/
            t2-mcoup = t2-mcoup - amount / fact1. 
            t-mcoup = t-mcoup - amount / fact1. 
          END.          
        END.        
      END. 
    END. 
  END. 
 
/* Non Stay Guest bills */ 
  FOR EACH bill WHERE ((bill.flag = 0 AND bill.datum GE to-date) 
    OR (bill.flag = 1 AND bill.datum GE to-date)) AND bill.resnr EQ 0 NO-LOCK, 
    FIRST bline WHERE bline.rechnr = bill.rechnr 
    AND bline.bill-datum = to-date NO-LOCK: 
    curr-dept = bill.rechnr. 
    cash = 0. 
    cc = 0. 
    cl = 0. 
    compli = 0. 
    mcoup = 0. 
    room = 0.
    i = 1. 

    
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr 
      AND bill-line.bill-datum = to-date NO-LOCK BY bill-line.sysdate 
      BY bill-line.zeit: 
        
    
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 

      
      IF NOT AVAILABLE artikel AND NUM-ENTRIES(bill-line.bezeich,"*") GT 1 THEN 
      FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
        AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 
      

      IF NOT AVAILABLE artikel THEN 
      DO: 
          msg-str = msg-str + "&W" 
              + translateExtended ("Artikel not found:", lvcAREA,"") + " " 
              + translateExtended ("Bill No:", lvcAREA,"") + " " 
              + STRING(bill.rechnr) + "; " 
              + translateExtended ("Article No:", lvcAREA,"") + " " 
              + STRING(bill-line.artnr) + " - " + bill-line.bezeich 
              + " " + TRIM(STRING(bill-line.betrag, "->>>,>>>,>>9.99")) 
              .
      END. 
      ELSE 
      DO: 
        FIND FIRST zwkum WHERE zwkum.zknr = artikel.zwkum AND 
          zwkum.departement = artikel.departement NO-LOCK. 
        i = i + 1. 
/*    curr-dept = artikel.departement.  */ 
        curr-bez = artikel.bezeich. 
        
        IF foreign-flag THEN amount = bill-line.fremdwbetrag. 
        ELSE amount = bill-line.betrag.                    


        IF artikel.artart = 0 OR artikel.artart = 9 OR artikel.artart = 8 
            /* OR artikel.artart = 1 */ OR artikel.artart = 5 THEN 
        DO:          
          IF artikel.departement = 0 THEN
          DO:
              do-it = YES.
              IF artikel.artart = 5 AND bill-line.userinit = "$$" THEN do-it = NO.
              ELSE IF artikel.artart = 5 AND bill-line.userinit NE "$$" AND artikel.artnr EQ deposit-outlet THEN do-it = NO.
              IF do-it THEN
              DO:
                FIND FIRST cl-list WHERE cl-list.artnr = artikel.artnr 
                  AND cl-list.dept = artikel.departement NO-ERROR. 
                IF NOT AVAILABLE cl-list THEN 
                DO: 
                  CREATE cl-list. 
                  ASSIGN
                    cl-list.flag    = 0
                    cl-list.artart  = artikel.umsatzart 
                    cl-list.artnr   = artikel.artnr
                    cl-list.dept    = artikel.departement 
                    cl-list.bezeich = STRING(artikel.departement,"99 ")
                                     + STRING(artikel.bezeich, "x(21)"). 
                END.
                ASSIGN
                  cl-list.gl = cl-list.gl + amount / fact1
                  cl-list.revenue = cl-list.revenue + amount / fact1 
                  t1-revenue = t1-revenue + amount / fact1. 
              END.
          END.         
          ELSE IF artikel.departement GT 0 THEN DO:
              FIND FIRST cl-list WHERE cl-list.artnr = zwkum.zknr 
                  AND cl-list.dept = zwkum.departement NO-ERROR. 
              IF NOT AVAILABLE cl-list THEN 
              DO: 
                  CREATE cl-list. 
                  ASSIGN
                    cl-list.flag    = 0
                    cl-list.artart  = artikel.umsatzart 
                    cl-list.artnr   = zwkum.zknr
                    cl-list.dept    = zwkum.departement 
                    cl-list.bezeich = STRING(zwkum.departement,"99 ")
                                     + STRING(zwkum.bezeich, "x(21)"). 
              END.
              ASSIGN
                  cl-list.gl = cl-list.gl + amount / fact1
                  cl-list.revenue = cl-list.revenue + amount / fact1 
                  t1-revenue = t1-revenue + amount / fact1. 
          END.
        END.
        ELSE IF artikel.artart = 2 OR artikel.artart = 6 OR artikel.artart = 7 
             OR artikel.artart = 11 OR artikel.artart = 12 THEN 
        DO: 
          /*FDL July 11, 2023 => Ticket C9FDA6*/
          FIND FIRST buff-bline WHERE buff-bline.rechnr EQ bill-line.rechnr
              AND buff-bline.bill-datum EQ bill-line.bill-datum              
              AND buff-bline.artnr EQ deposit-outlet NO-LOCK NO-ERROR.
          IF AVAILABLE buff-bline THEN found-depo-outlet = YES.
          IF found-depo-outlet THEN
          DO:              
              IF artikel.artart = 6 THEN
              DO:
                FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
                IF NOT AVAILABLE cash-list THEN
                DO:
                  CREATE cash-list.
                  ASSIGN
                      cash-list.artnr = artikel.artnr
                      cash-list.bezeich = artikel.bezeich
                  .
                END.
                cash-list.betrag = cash-list.betrag - amount / fact1.                
              END.

              found-depo-outlet = NO.
              NEXT.
          END.

          IF artikel.artart = 6 THEN
          DO:
            FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
            IF NOT AVAILABLE cash-list THEN
            DO:
              CREATE cash-list.
              ASSIGN
                  cash-list.artnr = artikel.artnr
                  cash-list.bezeich = artikel.bezeich
              .
            END.
            cash-list.betrag = cash-list.betrag - amount / fact1.
            cash = cash - amount / fact1. 
          END.

          /*t2-revenue = t2-revenue - amount / fact1. */
          IF artikel.artart = 2 THEN 
          DO:             
            cl = cl - amount / fact1.
            /*t2-cl = t2-cl - amount / fact1. 
            t-cl = t-cl - amount / fact1.*/ 
          END. 
          ELSE IF artikel.artart = 6 THEN 
          DO: 
            /*t2-cash = t2-cash - amount / fact1. 
           t-cash = t-cash - amount / fact1.*/            
          END. 
          ELSE IF artikel.artart = 7 THEN 
          DO: 
            cc = cc - amount / fact1.
            /*t2-cc = t2-cc - amount / fact1. 
            t-cc = t-cc - amount / fact1.             */
          END. 
          ELSE IF artikel.artart = 11 THEN 
          DO: 
            compli = compli - amount / fact1.
            /*t2-compli = t2-compli - amount / fact1. 
            t-compli = t-compli - amount / fact1. */
          END. 
          ELSE IF artikel.artart = 12 THEN 
          DO: 
            mcoup = mcoup - amount / fact1. 
            /*t2-mcoup = t2-mcoup - amount / fact1. 
            t-mcoup = t-mcoup - amount / fact1. */
          END.
          
          /*
          FIND FIRST cl-list WHERE cl-list.artnr = artikel.artnr 
            AND cl-list.dept = artikel.departement NO-ERROR. 
          IF NOT AVAILABLE cl-list THEN 
          DO: 
            CREATE cl-list. 
            cl-list.flag = 200. 
            cl-list.artnr = artikel.artnr. 
            cl-list.dept = artikel.departement. 
            cl-list.bezeich = STRING(artikel.bezeich, "x(19)"). 
          END. 
         
          cl-list.revenue = cl-list.revenue - amount / fact1. 
          t2-revenue = t2-revenue - amount / fact1. 

          IF artikel.artart = 2 THEN 
          DO: 
            cl-list.cl = cl-list.cl - amount / fact1. 
            cl = cl - amount / fact1. 
            t2-cl = t2-cl - amount / fact1. 
            t-cl = t-cl - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 6 THEN 
          DO: 
            cl-list.cash = cl-list.cash - amount / fact1. 
            t2-cash = t2-cash - amount / fact1. 
            t-cash = t-cash - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 7 THEN 
          DO: 
            cl-list.card = cl-list.card - amount / fact1.
            cc = cc - amount / fact1.
            t2-cc = t2-cc - amount / fact1. 
            t-cc = t-cc - amount / fact1.             
          END. 
          ELSE IF artikel.artart = 11 THEN 
          DO: 
            cl-list.compli = cl-list.compli - amount / fact1. 
            compli = compli - amount / fact1.
            t2-compli = t2-compli - amount / fact1. 
            t-compli = t-compli - amount / fact1. 
          END. 
          ELSE IF artikel.artart = 12 THEN 
          DO: 
            cl-list.mcoup = cl-list.mcoup - amount / fact1.
            mcoup = mcoup - amount / fact1. 
            t2-mcoup = t2-mcoup - amount / fact1. 
            t-mcoup = t-mcoup - amount / fact1. 
          END.*/
        END.        
      END. 
    END.

    IF cash NE 0 THEN 
    DO: 
      FIND FIRST cl-list WHERE cl-list.bezeich = "00 CASH" NO-ERROR. 
      IF NOT AVAILABLE cl-list THEN 
      DO: 
        CREATE cl-list. 
        cl-list.bezeich = "00 CASH". 
      END. 
      cl-list.cash = cl-list.cash + cash.
      t1-cash = t1-cash + cash. 
      t-cash = t-cash + cash.
      cash = 0. 
    END. 
    IF cc NE 0 THEN 
    DO: 
      FIND FIRST cl-list WHERE cl-list.bezeich = "00 Credit Cards" NO-ERROR. 
      IF NOT AVAILABLE cl-list THEN 
      DO: 
        CREATE cl-list. 
        cl-list.bezeich = "00 Credit Cards". 
      END. 
      cl-list.card = cl-list.card + cc. 
      t1-cc = t1-cc + cc.
      t-cc = t-cc + cc.
      cc = 0. 
    END. 
    IF cl NE 0 THEN 
    DO: 
      FIND FIRST cl-list WHERE cl-list.bezeich = "00 City Ledger" 
       NO-ERROR. 
      IF NOT AVAILABLE cl-list THEN 
      DO: 
        CREATE cl-list. 
        cl-list.bezeich = "00 City Ledger". 
      END. 
      cl-list.cl = cl-list.cl + cl. 
      t1-cl = t1-cl + cl. 
      t-cl = t-cl + cl.
      cl = 0. 
    END. 
  END.
 
/* deposit payment */ 
  FOR EACH billjournal WHERE billjournal.departement = 0 
    AND billjournal.bill-datum = to-date 
    AND billjournal.billjou-ref GT 0 
    AND billjournal.anzahl NE 0 NO-LOCK,
    FIRST artikel WHERE artikel.artnr = billjournal.artnr
    AND artikel.departement = 0 AND artikel.artart NE 5 NO-LOCK:
    IF NOT depo-foreign THEN
    DO:
        IF foreign-flag THEN amount = billjournal.fremdwaehrng. 
        ELSE amount = billjournal.betrag. 
    END.
    ELSE
    DO:
        FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
        FIND FIRST waehrung WHERE waehrung.wabkurz = foreign-curr NO-LOCK.
        IF to-date LT htparam.fdate THEN
        DO:
            FIND FIRST exrate WHERE exrate.datum = to-date AND
                exrate.artnr = waehrung.waehrungsnr NO-LOCK NO-ERROR.
            IF AVAILABLE exrate THEN 
                exchg-rate = exrate.betrag.
        END.
        IF exchg-rate = 0 THEN
            exchg-rate = waehrung.ankauf / waehrung.einheit.
        amount = billjournal.betrag * exchg-rate.
    END.
    
    cash = 0. 
    cc = 0. 
    cl = 0. 
    compli = 0. 
    mcoup = 0. 
    /* FDL Comment for ticket C9FDA6
    FIND FIRST cl-list WHERE cl-list.artnr = deposit-artnr 
      AND cl-list.dept = 0 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE cl-list THEN 
    DO: 
      CREATE cl-list. 
      cl-list.artnr = deposit-artnr. 
      cl-list.bezeich = STRING(0,"99 ") + STRING(deposit-bez, "x(21)"). 
      cl-list.room = 0. 
    END. 
    cl-list.revenue = cl-list.revenue - amount / fact1. 
    t1-revenue = t1-revenue - amount / fact1. 
    */

    /*FDL July 11, 2023 => Ticket C9FDA6*/
    IF billjournal.rechnr EQ 0 THEN  /*Deposit RSV*/
    DO:
        FIND FIRST cl-list WHERE cl-list.artnr = deposit-artnr 
            AND cl-list.dept = 0 EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE cl-list THEN 
        DO: 
          CREATE cl-list. 
          cl-list.artnr = deposit-artnr. 
          cl-list.bezeich = STRING(0,"99 ") + STRING(deposit-bez, "x(21)"). 
          cl-list.room = 0. 
        END. 
        cl-list.revenue = cl-list.revenue - amount / fact1. 
        t1-revenue = t1-revenue - amount / fact1.
    END.    
    ELSE    /*Deposit Outlet*/
    DO:
        FIND FIRST cl-list WHERE cl-list.artnr = deposit-outlet 
            AND cl-list.dept = 0 EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE cl-list THEN 
        DO: 
          CREATE cl-list. 
          cl-list.artnr = deposit-outlet. 
          cl-list.bezeich = STRING(0,"99 ") + STRING(deposit-outbez, "x(21)").  
          cl-list.room = 0. 
        END. 
        cl-list.revenue = cl-list.revenue - amount / fact1. 
        t1-revenue = t1-revenue - amount / fact1.                    
    END.

    IF artikel.artart = 6 THEN 
    DO: 
      FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
      IF NOT AVAILABLE cash-list THEN
      DO:
        CREATE cash-list.
        ASSIGN
            cash-list.artnr = artikel.artnr
            cash-list.bezeich = artikel.bezeich
        .
      END.
      
      cash-list.betrag = cash-list.betrag - amount / fact1.
      cl-list.cash = cl-list.cash - amount / fact1. 
      cash = cash - amount / fact1. 
      t1-cash = t1-cash - amount / fact1. 
      t-cash = t-cash - amount / fact1. 
    END. 
    ELSE IF artikel.artart = 7 THEN 
    DO: 
      cl-list.card = cl-list.card - amount / fact1. 
      cc = cc - amount / fact1. 
      t1-cc = t1-cc - amount / fact1. 
      t-cc = t-cc - amount / fact1. 
    END. 
    ELSE IF artikel.artart = 2 THEN 
    DO: 
      cl-list.cl = cl-list.cl - amount / fact1. 
      cl = cl - amount / fact1. 
      t1-cl = t1-cl - amount / fact1. 
      t-cl = t-cl - amount / fact1. 
    END. 
  END. 

/* banquet deposit payment */ 
  FOR EACH billjournal WHERE billjournal.artnr = deposit-baartnr
    AND billjournal.departement = depobuff.departement 
    AND billjournal.bill-datum = to-date 
    AND billjournal.billjou-ref GT 0 NO-LOCK:
 
    amount = - billjournal.betrag. 
 
    cash = 0. 
    cc = 0. 
    cl = 0. 
    compli = 0. 
    mcoup = 0. 
    FIND FIRST cl-list WHERE cl-list.artnr = deposit-baartnr 
      AND cl-list.dept = banquet-dept EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE cl-list THEN 
    DO: 
      CREATE cl-list. 
      ASSIGN
        cl-list.dept    = banquet-dept
        cl-list.artnr   = deposit-baartnr
        cl-list.bezeich = STRING(depobuff.departement,"99 ") 
          + STRING(deposit-babez, "x(21)") 
        cl-list.room    = 0
      .
    END. 
    
    cl-list.revenue = cl-list.revenue - amount / fact1. 
    t1-revenue = t1-revenue - amount / fact1. 
    FIND FIRST artikel WHERE artikel.artnr = billjournal.billjou-ref 
      AND artikel.departement = 0 NO-LOCK. 
    IF artikel.artart = 6 THEN 
    DO: 
      FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
      IF NOT AVAILABLE cash-list THEN
      DO:
        CREATE cash-list.
        ASSIGN
            cash-list.artnr = artikel.artnr
            cash-list.bezeich = artikel.bezeich
        .
      END.

      cash-list.betrag = cash-list.betrag - amount / fact1.
      cl-list.cash = cl-list.cash - amount / fact1. 
      cash = cash - amount / fact1. 
      t1-cash = t1-cash - amount / fact1. 
      t-cash = t-cash - amount / fact1. 
    END. 
    ELSE IF artikel.artart = 7 THEN 
    DO: 
      cl-list.card = cl-list.card - amount / fact1. 
      cc = cc - amount / fact1. 
      t1-cc = t1-cc - amount / fact1. 
      t-cc = t-cc - amount / fact1. 
    END. 
    ELSE IF artikel.artart = 2 THEN 
    DO: 
      cl-list.cl = cl-list.cl - amount / fact1. 
      cl = cl - amount / fact1. 
      t1-cl = t1-cl - amount / fact1. 
      t-cl = t-cl - amount / fact1. 
    END. 
  END. 

/*
  CREATE cl-list.
  ASSIGN cl-list.flag = 1
         cl-list.artart = -9
  .
*/

  FOR EACH hoteldpt WHERE hoteldpt.num GE 0 NO-LOCK BY hoteldpt.num: 
    RUN create-rlist. 
    cash = 0. 
    cc = 0. 
    cl = 0. 
    compli = 0. 
    mcoup = 0. 
    room = 0. 
    rest = 0. 
    curr-dept = hoteldpt.num. 
    curr-bez = hoteldpt.depart. 
    
    CREATE cl-list. 
    ASSIGN
      cl-list.begin   = YES
      cl-list.flag    = hoteldpt.num
      cl-list.dept    = hoteldpt.num 
      cl-list.bezeich = STRING(hoteldpt.num, "99 ") 
                      + STRING(hoteldpt.depart, "x(21)")
      . 
    FOR EACH rechnr-list NO-LOCK,
    FIRST h-journal WHERE h-journal.rechnr = rechnr-list.rechnr
      AND h-journal.departement = hoteldpt.num NO-LOCK:
    /*MT
    FIRST h-bill WHERE h-bill.rechnr = rechnr-list.rechnr 
      AND h-bill.departement = hoteldpt.num NO-LOCK:
    */

      FOR EACH h-bill-line WHERE h-bill-line.bill-datum = to-date 
        AND h-bill-line.departement = hoteldpt.num 
        AND h-bill-line.rechnr = h-journal.rechnr NO-LOCK: 
 
        IF foreign-flag THEN amount = h-bill-line.fremdwbetrag. 
        ELSE amount = h-bill-line.betrag. 
        
        
        rest = rest + amount / fact1. 
        IF h-bill-line.artnr NE 0 THEN 
        DO: 
          FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr 
          AND h-artikel.departement = h-bill-line.departement NO-LOCK. 
          IF h-artikel.artart = 0 THEN 
          DO: 
            cl-list.revenue = cl-list.revenue + amount / fact1. 
            t1-revenue = t1-revenue + amount / fact1. 
          END. 
          ELSE IF h-artikel.artart = 6 THEN 
          DO:    
              cash = cash - amount / fact1. 
              FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                  AND artikel.departement = 0 NO-LOCK.
              FIND FIRST cash-list WHERE cash-list.artnr = artikel.artnr NO-ERROR.
              IF NOT AVAILABLE cash-list THEN
              DO:
                CREATE cash-list.
                ASSIGN
                    cash-list.artnr = artikel.artnr
                    cash-list.bezeich = artikel.bezeich
                .
              END.              
              cash-list.betrag = cash-list.betrag - amount / fact1.
          END.
          ELSE IF h-artikel.artart = 7 THEN cc = cc - amount / fact1. 
          ELSE IF h-artikel.artart = 2 THEN cl = cl - amount / fact1. 
          ELSE IF h-artikel.artart = 11 THEN 
          DO: 
            compli = compli - amount / fact1. 
            cl-list.revenue = cl-list.revenue + amount / fact1. 
            t1-revenue = t1-revenue + amount / fact1. 
          END. 
          ELSE IF h-artikel.artart = 12 THEN 
          DO: 
            mcoup = mcoup - amount / fact1. 
            cl-list.revenue = cl-list.revenue + amount / fact1. 
            t1-revenue = t1-revenue + amount / fact1. 
          END. 
        END. 
        ELSE room = room - amount / fact1. /* guest or NS or master bill */ 
      END. 
    END. 

    IF AVAILABLE cl-list THEN 
    ASSIGN
      t1-cash           = t1-cash + cash
      t1-cc             = t1-cc + cc
      t1-cl             = t1-cl + cl 
      t1-compli         = t1-compli + compli 
      t1-mcoup          = t1-mcoup + mcoup
      t1-room           = t1-room + room
      t1-gl             = t1-gl + rest

      t-cash            = t-cash + cash 
      t-cc              = t-cc + cc
      t-cl              = t-cl + cl 
      t-compli          = t-compli + compli
      t-mcoup           = t-mcoup + mcoup
      t-room            = t-room + room
      t-gl              = t-gl + rest
 
      cl-list.cash      = cl-list.cash + cash 
      cl-list.card      = cl-list.card + cc
      cl-list.cl        = cl-list.cl + cl
      cl-list.compli    = cl-list.compli + compli 
      cl-list.mcoupon   = cl-list.mcoupon + mcoup /*Alder - Serverless - Issue 631*/
      cl-list.room      = cl-list.room + room
      cl-list.gl        = cl-list.gl + rest
    . 
  END. 

/*
  t1-revenue = 0.
  FOR EACH cl-list WHERE cl-list.flag LT 200:
      t1-revenue = t1-revenue + cl-list.cash + cl-list.card
          + cl-list.cl + cl-list.room + cl-list.gl.
  END.
*/
  
  ASSIGN
    i         = 0
    curr-flag = -1
  . 
  FOR EACH cl-list BY cl-list.flag BY cl-list.begin DESCENDING
      BY cl-list.artart BY cl-list.artnr:     
    IF cl-list.flag = 200 AND curr-flag NE cl-list.flag THEN 
    DO: 
      curr-flag = cl-list.flag. 
      
      IF price-decimal = 0 AND NOT foreign-flag THEN 
      DO:         
        IF NOT long-digit OR short-flag THEN 
        DO:
          CREATE sumcsr-list.
          CREATE sumcsr-list.
          ASSIGN
            sumcsr-list.dept     = "Subtotal"
            sumcsr-list.cash     = STRING(t1-cash, "->>>,>>>,>>>,>>9.99")    
            sumcsr-list.card     = STRING(t1-cc, "->>>,>>>,>>>,>>9.99")      
            sumcsr-list.CL       = STRING(t1-cl, "->>>,>>>,>>>,>>9.99")      
            sumcsr-list.compli   = STRING(t1-compli, "->>>,>>>,>>>,>>9.99")  
            sumcsr-list.mealcou  = STRING(t1-mcoup, "->>>,>>>,>>>,>>9.99")   
            sumcsr-list.rmfobill = STRING(t1-room, "->>>,>>>,>>>,>>9.99")    
            sumcsr-list.revenue  = STRING(t1-revenue, "->>>,>>>,>>>,>>9.99") 
            sumcsr-list.outstand = STRING(t1-gl, "->>>,>>>,>>>,>>9.99")     
          .

          CREATE sumcsr-list.
          CREATE sumcsr-list.
        END.        
      END. 
      ELSE
      DO:
        CREATE sumcsr-list.
        CREATE sumcsr-list.
        ASSIGN
          sumcsr-list.dept     = "Subtotal"
          sumcsr-list.cash     = STRING(t1-cash, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.card     = STRING(t1-cc, "->>>,>>>,>>>,>>9.99")      
          sumcsr-list.CL       = STRING(t1-cl, "->>>,>>>,>>>,>>9.99")      
          sumcsr-list.compli   = STRING(t1-compli, "->>>,>>>,>>>,>>9.99")  
          sumcsr-list.mealcou  = STRING(t1-mcoup, "->>>,>>>,>>>,>>9.99")   
          sumcsr-list.rmfobill = STRING(t1-room, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.revenue  = STRING(t1-revenue, "->>>,>>>,>>>,>>9.99") 
          sumcsr-list.outstand = STRING(t1-gl, "->>>,>>>,>>>,>>9.99")    
        .

        CREATE sumcsr-list.
        CREATE sumcsr-list.
      END.      
    END.     
       
    CREATE sumcsr-list.
    i = i + 1.
    ASSIGN
      sumcsr-list.reihe  = i 
      sumcsr-list.flag   = cl-list.flag 
      sumcsr-list.artart = cl-list.artart
    . 

    IF cl-list.begin AND cl-list.dept = 0 THEN
    DO:                       
      ASSIGN
        sumcsr-list.dept     = cl-list.bezeich 
        sumcsr-list.cash     = STRING(cl-list.cash, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.rmfobill = STRING(cl-list.room, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.card     = STRING(cl-list.card, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.CL       = STRING(cl-list.cl, "->>>,>>>,>>>,>>9.99")      
        sumcsr-list.revenue  = STRING(cl-list.revenue, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.compli   = STRING(cl-list.compli, "->>>,>>>,>>>,>>9.99") 
        sumcsr-list.mealcou  = STRING(cl-list.mcoupon, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.outstand = STRING(cl-list.gl, "->>>,>>>,>>>,>>9.99")
        .      
    END.
    ELSE IF cl-list.artart GE 0 AND price-decimal = 0 AND NOT foreign-flag THEN 
    DO: 
      IF NOT long-digit OR short-flag THEN 
      DO:        
        ASSIGN
          sumcsr-list.dept     = cl-list.bezeich 
          sumcsr-list.cash     = STRING(cl-list.cash, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.rmfobill = STRING(cl-list.room, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.card     = STRING(cl-list.card, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.CL       = STRING(cl-list.cl, "->>>,>>>,>>>,>>9.99")      
          sumcsr-list.revenue  = STRING(cl-list.revenue, "->>>,>>>,>>>,>>9.99")
          sumcsr-list.compli   = STRING(cl-list.compli, "->>>,>>>,>>>,>>9.99") 
          sumcsr-list.mealcou  = STRING(cl-list.mcoupon, "->>>,>>>,>>>,>>9.99")
          sumcsr-list.outstand = STRING(cl-list.gl, "->>>,>>>,>>>,>>9.99")     
          .
      END.
    END.
    ELSE IF cl-list.artart GE 0 THEN
    DO:       
      ASSIGN
        sumcsr-list.dept     = cl-list.bezeich 
        sumcsr-list.cash     = STRING(cl-list.cash, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.rmfobill = STRING(cl-list.room, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.card     = STRING(cl-list.card, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.CL       = STRING(cl-list.cl, "->>>,>>>,>>>,>>9.99")      
        sumcsr-list.revenue  = STRING(cl-list.revenue, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.compli   = STRING(cl-list.compli, "->>>,>>>,>>>,>>9.99") 
        sumcsr-list.mealcou  = STRING(cl-list.mcoupon, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.outstand = STRING(cl-list.gl, "->>>,>>>,>>>,>>9.99")     
        .
    END.     
  END.   

  FIND FIRST cl-list WHERE cl-list.flag = 200 NO-ERROR. 
  IF NOT AVAILABLE cl-list THEN 
  DO: 
    IF price-decimal = 0 AND NOT foreign-flag THEN 
    DO: 
      IF NOT long-digit OR short-flag THEN 
      DO:
        CREATE sumcsr-list.    
        CREATE sumcsr-list.
        ASSIGN
          sumcsr-list.dept     = "Subtotal"
          sumcsr-list.cash     = STRING(t1-cash, "->>>,>>>,>>>,>>9.99")      
          sumcsr-list.card     = STRING(t1-cc, "->>>,>>>,>>>,>>9.99")        
          sumcsr-list.CL       = STRING(t1-cl, "->>>,>>>,>>>,>>9.99")        
          sumcsr-list.compli   = STRING(t1-compli, "->>>,>>>,>>>,>>9.99")    
          sumcsr-list.mealcou  = STRING(t1-mcoup, "->>>,>>>,>>>,>>9.99")     
          sumcsr-list.rmfobill = STRING(t1-room, "->>>,>>>,>>>,>>9.99")      
          sumcsr-list.revenue  = STRING(t1-revenue, "->>>,>>>,>>>,>>9.99")   
          sumcsr-list.outstand = STRING(t1-gl, "->>>,>>>,>>>,>>9.99")        
        .

        CREATE sumcsr-list.
      END.
    END. 
    ELSE
    DO:
      CREATE sumcsr-list.
      CREATE sumcsr-list.
      ASSIGN
        sumcsr-list.dept     = "Subtotal"
        sumcsr-list.cash     = STRING(t1-cash, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.card     = STRING(t1-cc, "->>>,>>>,>>>,>>9.99")      
        sumcsr-list.CL       = STRING(t1-cl, "->>>,>>>,>>>,>>9.99")      
        sumcsr-list.compli   = STRING(t1-compli, "->>>,>>>,>>>,>>9.99")  
        sumcsr-list.mealcou  = STRING(t1-mcoup, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.rmfobill = STRING(t1-room, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.revenue  = STRING(t1-revenue, "->>>,>>>,>>>,>>9.99") 
        sumcsr-list.outstand = STRING(t1-gl, "->>>,>>>,>>>,>>9.99")     
      .

      CREATE sumcsr-list.
    END.
  END. 

  IF price-decimal = 0 AND NOT foreign-flag THEN 
  DO: 
    IF NOT long-digit OR short-flag THEN 
    DO:
      CREATE sumcsr-list.
      CREATE sumcsr-list.
      ASSIGN
        sumcsr-list.dept     = "Subtotal"
        sumcsr-list.cash     = STRING(t2-cash, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.card     = STRING(t2-cc, "->>>,>>>,>>>,>>9.99")     
        sumcsr-list.CL       = STRING(t2-cl, "->>>,>>>,>>>,>>9.99")     
        sumcsr-list.compli   = STRING(t2-compli, "->>>,>>>,>>>,>>9.99") 
        sumcsr-list.mealcou  = STRING(t2-mcoup, "->>>,>>>,>>>,>>9.99")  
        sumcsr-list.rmfobill = STRING(t2-room, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.revenue  = STRING(t2-revenue, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.outstand = STRING(t2-gl, "->>>,>>>,>>>,>>9.99")     
        .

      CREATE sumcsr-list.
    END.
  END.  
  ELSE
  DO:
    CREATE sumcsr-list.
    CREATE sumcsr-list.
    ASSIGN
      sumcsr-list.dept     = "Subtotal"
      sumcsr-list.cash     = STRING(t2-cash, "->>>,>>>,>>>,>>9.99")     
      sumcsr-list.card     = STRING(t2-cc, "->>>,>>>,>>>,>>9.99")       
      sumcsr-list.CL       = STRING(t2-cl, "->>>,>>>,>>>,>>9.99")       
      sumcsr-list.compli   = STRING(t2-compli, "->>>,>>>,>>>,>>9.99")   
      sumcsr-list.mealcou  = STRING(t2-mcoup, "->>>,>>>,>>>,>>9.99")    
      sumcsr-list.rmfobill = STRING(t2-room, "->>>,>>>,>>>,>>9.99")     
      sumcsr-list.revenue  = STRING(t2-revenue, "->>>,>>>,>>>,>>9.99")  
      sumcsr-list.outstand = STRING(t2-gl, "->>>,>>>,>>>,>>9.99")      
    .

    CREATE sumcsr-list.
  END.
  
  IF price-decimal = 0 AND NOT foreign-flag THEN 
  DO: 
    IF NOT long-digit OR short-flag THEN 
    DO:
      CREATE sumcsr-list.
      ASSIGN
        sumcsr-list.dept     = "T O T A L"
        sumcsr-list.cash     = STRING(t-cash, "->>>,>>>,>>>,>>9.99")    
        sumcsr-list.card     = STRING(t-cc, "->>>,>>>,>>>,>>9.99")      
        sumcsr-list.CL       = STRING(t-cl, "->>>,>>>,>>>,>>9.99")     
        sumcsr-list.compli   = STRING(t-compli, "->>>,>>>,>>>,>>9.99")  
        sumcsr-list.mealcou  = STRING(t-mcoup, "->>>,>>>,>>>,>>9.99")  
        sumcsr-list.rmfobill = STRING(t-room, "->>>,>>>,>>>,>>9.99")   
        sumcsr-list.revenue  = STRING(t-revenue, "->>>,>>>,>>>,>>9.99")
        sumcsr-list.outstand = STRING(t-gl, "->>>,>>>,>>>,>>9.99")     
        .

      CREATE sumcsr-list.
      CREATE sumcsr-list.
    END.
  END.   
  ELSE
  DO:
    CREATE sumcsr-list.
    ASSIGN
      sumcsr-list.dept     = "T O T A L"
      sumcsr-list.cash     = STRING(t-cash, "->>>,>>>,>>>,>>9.99")    
      sumcsr-list.card     = STRING(t-cc, "->>>,>>>,>>>,>>9.99")      
      sumcsr-list.CL       = STRING(t-cl, "->>>,>>>,>>>,>>9.99")      
      sumcsr-list.compli   = STRING(t-compli, "->>>,>>>,>>>,>>9.99")  
      sumcsr-list.mealcou  = STRING(t-mcoup, "->>>,>>>,>>>,>>9.99")   
      sumcsr-list.rmfobill = STRING(t-room, "->>>,>>>,>>>,>>9.99")    
      sumcsr-list.revenue  = STRING(t-revenue, "->>>,>>>,>>>,>>9.99") 
      sumcsr-list.outstand = STRING(t-gl, "->>>,>>>,>>>,>>9.99")     
    .

    CREATE sumcsr-list.
    CREATE sumcsr-list.
  END.

  t-cash = 0.
  FIND FIRST cash-list NO-ERROR.
  IF AVAILABLE cash-list THEN
  DO:
    CREATE sumcsr-list.
    ASSIGN
        i = i + 1
        sumcsr-list.reihe = i
        sumcsr-list.dept = "Cash Breakdown:"
    .

    FOR EACH cash-list:
        CREATE sumcsr-list.
        ASSIGN
            i = i + 1
            t-cash = t-cash + cash-list.betrag
            sumcsr-list.reihe = i
        .
        IF price-decimal = 0 AND NOT foreign-flag THEN
        DO:
          ASSIGN
            sumcsr-list.dept = cash-list.bezeich
            sumcsr-list.cash = STRING(cash-list.betrag, "->>>,>>>,>>>,>>9.99").          
        END.            
        ELSE
        DO:
          ASSIGN
            sumcsr-list.dept = cash-list.bezeich
            sumcsr-list.cash = STRING(cash-list.betrag, "->>>,>>>,>>>,>>9.99").
        END.        
    END.

    CREATE sumcsr-list.
    CREATE sumcsr-list.
    ASSIGN
        i = i + 1
        sumcsr-list.reihe = i
        sumcsr-list.dept = "Total Cash"
    .
    IF price-decimal = 0 AND NOT foreign-flag THEN 
    DO:
      ASSIGN
        sumcsr-list.cash = STRING(t-cash, "->>>,>>>,>>>,>>9.99"). 
    END.
    ELSE
    DO:
      ASSIGN
        sumcsr-list.cash = STRING(t-cash, "->>>,>>>,>>>,>>9.99").
    END.    
  END.
END. 

PROCEDURE create-rlist: 
  FOR EACH rechnr-list: 
    DELETE rechnr-list. 
  END.

  FOR EACH h-journal WHERE h-journal.departement = hoteldpt.num 
    AND h-journal.bill-datum = to-date NO-LOCK: 
    FIND FIRST rechnr-list WHERE rechnr-list.rechnr = h-journal.rechnr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE rechnr-list THEN 
    DO: 
      CREATE rechnr-list. 
      rechnr-list.rechnr = h-journal.rechnr. 
    END. 
  END. 
END. 

