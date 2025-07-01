
DEFINE TEMP-TABLE soa-list 
  FIELD counter     AS INTEGER INIT 0
  FIELD debref      AS INTEGER
  FIELD done-step   AS INTEGER INIT 0
  FIELD artno       AS INTEGER
  FIELD vesrdep     AS DECIMAL
  FIELD to-sort     AS INTEGER
  FIELD outlet      AS LOGICAL INITIAL NO 
  FIELD datum       AS DATE LABEL "Date"
  FIELD ankunft     AS DATE 
  FIELD abreise     AS DATE
  FIELD gastnr      AS INTEGER 
  FIELD name        AS CHAR     FORMAT "x(32)"      LABEL "Guest Name" 
  FIELD inv-str     AS CHAR     FORMAT "x(10)"      LABEL "Invoice No"
  FIELD rechnr      AS INTEGER  FORMAT ">>>>>>>>9"  LABEL "BillNo" 
  FIELD refNo       AS INTEGER  FORMAT "9999999"    LABEL "RefNo"
  FIELD voucherNo   AS CHAR     FORMAT "x(12)"      LABEL "Reference" 
  /*MT 13/06/13 */
  FIELD voucherNo1  AS CHAR     FORMAT "x(12)"      LABEL "Vouvher No 1"
  FIELD voucherNo2  AS CHAR     FORMAT "x(12)"      LABEL "Vouvher No 2"
  FIELD saldo       AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL "Balance" 
  FIELD fsaldo      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL "Foreign"
  FIELD printed     AS LOGICAL INITIAL NO LABEL "Printed" 
  FIELD selected    AS LOGICAL INITIAL NO LABEL "Selected"
  FIELD printdate   AS DATE INITIAL TODAY
  FIELD dptnr       AS INTEGER  FORMAT "99" LABEL "Dept"
  /*New*/
  FIELD debt        AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  LABEL "Debt"
  FIELD credit      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  LABEL "Credit"
  FIELD fdebt       AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  LABEL "FDebt"
  FIELD fcredit     AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"  LABEL "FCredit"
  FIELD remarks     AS CHAR     FORMAT "x(40)"               LABEL "Remarks"
  FIELD arRecid     AS INTEGER
  FIELD newPayment  AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL "New Payment"
  FIELD newfPayment AS DECIMAL  FORMAT "->>>,>>9.99"        LABEL "New Payment"
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo"   /*MT 24/07/12 */    
  /*ITA 140415*/
  FIELD erwachs     AS INTEGER
  FIELD child1      AS INTEGER
  FIELD child2      AS INTEGER
  FIELD roomrate    AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99"
  FIELD tot-amount  AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD tot-balance AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD exrate      AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD tot-exrate  AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"              
  /*for penang*/
  FIELD gst-tot-non-taxable AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD gst-amount          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.9999999999999"
  FIELD gst-tot-sales       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99999999999999"      
  /*wen*/
  FIELD zimmeranz           LIKE res-line.zimmeranz
  /*gerald flag A/R FO dan A/R Manual CD4450*/
  FIELD ar-flag             AS INTEGER
  /*gerald foreign exchange 498EA1*/
  FIELD foreign-exchg       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  /*Gerald booker A66C06*/
  FIELD resv-name       AS CHAR FORMAT "x(32)"  LABEL "Bill Reveiver"

  /*naufal afthar #D2A668 - 12/09/24*/
  FIELD voucher-res-line AS CHAR FORMAT "x(16)" LABEL "Voucher No Reservation"

  INDEX rechnr_ix dptnr rechnr debref DESCENDING.

DEFINE TEMP-TABLE t-payload-list
    FIELD user-init AS CHARACTER. /* Naufal Afthar - 94078C*/

DEFINE INPUT PARAMETER TABLE FOR soa-list.
DEFINE INPUT PARAMETER TABLE FOR t-payload-list.
DEFINE INPUT PARAMETER reference AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

/* Naufal Afthar - 94078C -> add system log when attach SOA*/
FIND FIRST t-payload-list NO-LOCK NO-ERROR.

RUN update-ref.


PROCEDURE update-ref:
  DEFINE BUFFER bill1   FOR bill.    
  DEFINE BUFFER debt1   FOR debitor.
  DEFINE BUFFER debt2   FOR debitor.
  DEFINE BUFFER h-bill1 FOR h-bill.
  DEFINE BUFFER soa-list1 FOR soa-list.
  DEFINE BUFFER soa-list2 FOR soa-list.

  /* Naufal Afthar - 94078C*/
  DEFINE VARIABLE rechnr-list AS CHARACTER.

  FOR EACH soa-list :
    /* FIND FIRST soa-list WHERE RECID(soa-list) = RECID(soa-list1) EXCLUSIVE-LOCK. */      /* Rulita 121224 | Fixing for serverless issue git 268 */
    soa-list.refno = reference.
    soa-list.inv-str = "INV" + STRING(reference, "9999999").
    /* FIND CURRENT soa-list NO-LOCK. */

    /* Naufal Afthar - 94078C*/
    rechnr-list = rechnr-list + STRING(soa-list.rechnr) + ", ".
    
    IF NOT soa-list.outlet THEN
    DO:             
        FIND FIRST bill1 WHERE bill1.rechnr = soa-list.rechnr NO-LOCK NO-ERROR.
        IF AVAILABLE bill1 AND bill1.billref = 0 THEN
        DO:
            FIND CURRENT bill1 EXCLUSIVE-LOCK. 
            bill1.billref = reference. 
            bill1.logidat = TODAY.
            FIND CURRENT bill1 NO-LOCK.
        END.
        ELSE DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY = 192
                queasy.number1 = soa-list.rechnr
                queasy.number2 = reference
                queasy.date1   = TODAY.
        END.

        IF soa-list.counter NE 0 THEN DO:
            FOR EACH debt1 WHERE debt1.rechnr = soa-list.rechnr 
                AND debt1.opart LE 1 AND debt1.counter = soa-list.counter
                AND debt1.betriebsnr = 0 AND debt1.saldo NE 0 NO-LOCK: 
                FIND FIRST debt2 WHERE RECID(debt2) = RECID(debt1) EXCLUSIVE-LOCK.
                debt2.debref = reference.
                FIND CURRENT debt2 NO-LOCK.            
            END.          
        END.
        ELSE DO:
            FOR EACH debt1 WHERE debt1.rechnr = soa-list.rechnr 
                AND debt1.opart LE 1 AND debt1.betriebsnr = 0 
                AND debt1.saldo NE 0 AND RECID(debt1) = soa-list.arRecid NO-LOCK: 
                FIND FIRST debt2 WHERE RECID(debt2) = RECID(debt1) EXCLUSIVE-LOCK.
                debt2.debref = reference.
                FIND CURRENT debt2 NO-LOCK.
            END.          
        END.
        ASSIGN success-flag = YES.
    END.
    ELSE
    DO: 
        FIND FIRST h-bill1 WHERE h-bill1.rechnr = soa-list.rechnr
            AND h-bill1.departement = soa-list.dptnr.
        h-bill1.service[6] = DECIMAL(reference).
        h-bill1.service[7] = DECIMAL(STRING(MONTH(TODAY), "99") + STRING(DAY(TODAY), "99") + 
            STRING(YEAR(TODAY), "9999")).
        FIND CURRENT h-bill1 NO-LOCK.
        FOR EACH debt1 WHERE debt1.rechnr = soa-list.rechnr AND debt1.opart LE 1
            /*AND debt1.counter = 0*/ AND debt1.betriebsnr GT 0 NO-LOCK:
            
            FIND FIRST debt2 WHERE RECID(debt2) = RECID(debt1)
                EXCLUSIVE-LOCK.
            
            debt2.debref = reference.
            FIND CURRENT debt2 NO-LOCK.
            success-flag = YES.
        END.                           
    END.
  END. /* each soa-list*/

  /* Naufal Afthar - 94078C -> add system log when attach SOA*/
  FIND FIRST bediener WHERE bediener.userinit EQ t-payload-list.user-init NO-LOCK NO-ERROR.
  IF AVAILABLE bediener THEN 
  DO:
      MESSAGE "masuk res history".
      CREATE res-history.
      ASSIGN
          res-history.nr        = bediener.nr
          res-history.datum     = TODAY
          res-history.zeit      = TIME
          res-history.action    = "Statement Of Account"
          res-history.aenderung = "Transaction Bill Number " + SUBSTRING(rechnr-list, 1, LENGTH(rechnr-list) - 2) + 
                                    " has been printed / has been attached to Invoice NO : " + 
                                    STRING(reference, "9999999").
  END.
END.
