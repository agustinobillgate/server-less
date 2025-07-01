
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
  FIELD gst-amount          AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD gst-tot-sales       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"

    /*wen*/
  FIELD zimmeranz           LIKE res-line.zimmeranz

  /* Rulita |  1E88B5 ADJUSTMENT UI PRINT SOA */
  FIELD bill-datum  AS DATE   
  FIELD resv-name       AS CHAR FORMAT "x(32)"

  INDEX rechnr_ix dptnr rechnr debref DESCENDING.


DEF BUFFER soabuff FOR soa-list.
DEFINE VAR zeit  AS INTEGER NO-UNDO.
DEFINE VAR zeit1 AS INTEGER NO-UNDO.

DEFINE VAR str AS CHAR.

DEFINE TEMP-TABLE param-ar
    FIELD param-nr       AS INTEGER
    FIELD param-name     AS CHAR    FORMAT "x(70)" 
    FIELD param-val      AS CHAR    FORMAT "x(150)"
    FIELD param-type     AS CHAR.

DEFINE INPUT PARAMETER show-type AS INTEGER.
DEFINE INPUT PARAMETER bof-month AS DATE.
DEFINE INPUT PARAMETER eof-month AS DATE.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR param-ar.
DEFINE INPUT PARAMETER guestno   AS INTEGER.
DEFINE INPUT PARAMETER curr-day  AS DATE.
DEFINE OUTPUT PARAMETER due-date AS DATE INITIAL TODAY.
DEFINE OUTPUT PARAMETER TABLE FOR soa-list.
DEFINE OUTPUT PARAMETER rech-nr AS INT.
DEFINE OUTPUT PARAMETER bet-nr AS INT.
DEFINE OUTPUT PARAMETER msg-int AS INT.

DEFINE VAR param1 AS CHAR.
DEFINE VAR param2 AS CHAR.
DEFINE VAR param3 AS CHAR.
DEFINE VAR param4 AS CHAR.

/*Anantara uluwatu, sebagai temporary variabel output parameter*/
DEFINE VARIABLE Fnet-lodging    AS DECIMAL NO-UNDO.
DEFINE VARIABLE Lnet-lodging    AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-breakfast   AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-lunch       AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-dinner      AS DECIMAL NO-UNDO.
DEFINE VARIABLE net-others      AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-rmrev     AS DECIMAL NO-UNDO.
DEFINE VARIABLE nett-vat        AS DECIMAL NO-UNDO.
DEFINE VARIABLE nett-service    AS DECIMAL NO-UNDO.


DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-refNo  AS INTEGER. 
DEFINE VARIABLE new-refno   AS INTEGER INITIAL 0. 
DEFINE VARIABLE cl-exist    AS LOGICAL. 
DEFINE VARIABLE saldo       AS DECIMAL. 
DEFINE VARIABLE s           AS CHAR. 
DEFINE VARIABLE i           AS INTEGER INITIAL 0.
DEFINE VARIABLE arrival     AS DATE.
DEFINE VARIABLE departure   AS DATE.
/*DEFINE VARIABLE debt        AS DECIMAL. FT serverless*/
DEFINE VARIABLE debt-amount AS DECIMAL.
DEFINE VARIABLE crdt        AS DECIMAL.
DEFINE VARIABLE fdebt       AS DECIMAL.
DEFINE VARIABLE fcrdt       AS DECIMAL.
DEFINE VARIABLE new-crdt    AS DECIMAL.
DEFINE VARIABLE new-fcrdt   AS DECIMAL.
DEFINE VARIABLE isprintedb4 AS LOGICAL INITIAL NO.

DEFINE BUFFER gast  FOR guest.
DEFINE BUFFER bill1 FOR bill. 
DEFINE BUFFER debt  FOR debitor. 
DEFINE BUFFER debt1 FOR debitor. 

DEFINE BUFFER billine  FOR bill-line.
DEFINE BUFFER hbilline FOR h-bill-line.
DEFINE BUFFER bresline FOR res-line.

DEFINE VARIABLE saldo1  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo2  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo3  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo4  AS DECIMAL      INITIAL 0.

DEFINE VARIABLE other-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE count-zimm AS INTEGER NO-UNDO.

DEF VAR nmonth AS INTEGER.
DEF VAR mnth1 AS INTEGER.
DEF VAR year2 AS INTEGER.
DEF VAR val-param AS INTEGER.
DEF VAR var-param AS CHAR.


RUN create-soalist.


PROCEDURE create-soalist: 
/*
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-refNo  AS INTEGER. 
DEFINE VARIABLE new-refno   AS INTEGER INITIAL 0. 
DEFINE VARIABLE cl-exist    AS LOGICAL. 
DEFINE VARIABLE saldo       AS DECIMAL. 
DEFINE VARIABLE s           AS CHAR. 
DEFINE VARIABLE i           AS INTEGER INITIAL 0.
DEFINE VARIABLE arrival     AS DATE.
DEFINE VARIABLE departure   AS DATE.
DEFINE VARIABLE debt        AS DECIMAL.
DEFINE VARIABLE crdt        AS DECIMAL.
DEFINE VARIABLE fdebt       AS DECIMAL.
DEFINE VARIABLE fcrdt       AS DECIMAL.
DEFINE VARIABLE new-crdt    AS DECIMAL.
DEFINE VARIABLE new-fcrdt   AS DECIMAL.
DEFINE VARIABLE isprintedb4 AS LOGICAL INITIAL NO.

DEFINE BUFFER gast  FOR guest.
DEFINE BUFFER bill1 FOR bill. 
DEFINE BUFFER debt  FOR debitor. 
DEFINE BUFFER debt1 FOR debitor. 

DEFINE BUFFER billine  FOR bill-line.
DEFINE BUFFER hbilline FOR h-bill-line.

DEFINE VARIABLE saldo1  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo2  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo3  AS DECIMAL      INITIAL 0.
DEFINE VARIABLE saldo4  AS DECIMAL      INITIAL 0.
*/

  DEFINE BUFFER bdebt FOR debitor.
  DEFINE BUFFER bdebt1 FOR debitor.

  FOR EACH soa-list: 
    delete soa-list. 
  END. 

  IF show-type = 0 THEN
  DO: 
      FOR EACH debitor WHERE debitor.gastnr = guestno 
          AND debitor.opart LE 1 AND debitor.saldo NE 0
          AND debitor.zahlkonto = 0 NO-LOCK,
          FIRST artikel WHERE artikel.artnr = debitor.artnr AND 
            artikel.artart = 2 AND artikel.departement = 0 NO-LOCK:
          FIND FIRST soa-list WHERE soa-list.gastnr = debitor.gastnr 
            AND soa-list.rechnr = debitor.rechnr
            AND soa-list.dptnr = debitor.betriebsnr NO-ERROR.
          IF NOT AVAILABLE soa-list THEN
          DO:              
              CREATE soa-list.
              ASSIGN soa-list.to-sort   = 1 
                  soa-list.arRecid      = RECID(debitor)
                  soa-list.rechnr       = debitor.rechnr 
                  soa-list.gastnr       = debitor.gastnr
                  soa-list.datum        = debitor.rgdatum
                  soa-list.remarks      = debitor.vesrcod
                  soa-list.dptnr        = debitor.betriebsnr
                  
                  soa-list.artno        = debitor.artnr
                  soa-list.counter      = debitor.counter
                  soa-list.debref       = debitor.debref    /*MTT*/
                  soa-list.saldo        = soa-list.saldo + debitor.saldo
                  soa-list.vesrdep      = debitor.vesrdep.
                  
          END.
      END.

      DEF BUFFER debbt FOR debitor.
      
      /*FIND FIRST soa-list WHERE soa-list.done-step = 0
        USE-INDEX rechnr_ix NO-ERROR.
      DO WHILE AVAILABLE soa-list:FT serverless*/
      FOR EACH soa-list WHERE soa-list.done-step = 0 USE-INDEX rechnr_ix NO-LOCK:
        ASSIGN 
          crdt = 0
          debt-amount = 0
          fcrdt = 0
          fdebt = 0
          new-crdt = 0 
          new-fcrdt = 0 
          isprintedb4 = (soa-list.debref GT 0)
        .
          
        FOR EACH soabuff WHERE soabuff.rechnr = soa-list.rechnr
          AND soabuff.dptnr = soa-list.dptnr
          AND soabuff.artno = soa-list.artno
          AND soabuff.done-step = 0:
          ASSIGN
            soabuff.done-step = 1
            debt-amount       = soabuff.saldo
            fdebt             = fdebt + soabuff.vesrdep 
          .
              
          IF soabuff.counter GT 0 THEN
            FOR EACH debt WHERE 
              debt.rechnr     = soabuff.rechnr 
              AND debt.counter    = soabuff.counter
              /*AND debt.betriebsnr = soabuff.dptnr*/
              AND debt.gastnr     = guestno
              AND debt.zahlkonto  > 0 NO-LOCK:
              ASSIGN
                fcrdt = fcrdt + debt.vesrdep
                crdt  = crdt + debt.saldo
              .
              IF isprintedb4 AND debt.debref = 0 THEN
              ASSIGN
                new-crdt  = new-crdt + crdt
                new-fcrdt = new-fcrdt + fcrdt
              .
            END.

              /*MT 171212 */
          FOR EACH debt WHERE debt.rechnr = soabuff.rechnr 
            AND debt.gastnr = soabuff.gastnr
            AND debt.betriebsnr = soabuff.dptnr
            AND debt.opart LE 1 AND soabuff.saldo NE 0
            AND debt.zahlkonto = 0 AND RECID(debt) NE soa-list.arRecid NO-LOCK,
            FIRST artikel WHERE artikel.artnr = debt.artnr
            AND artikel.artart  = 2 AND artikel.departement = 0 NO-LOCK:
               
            ASSIGN
              debt-amount = debt-amount + debt.saldo
              fdebt = fdebt + debt.vesrdep .
            IF debt.counter GT 0 THEN
              FOR EACH debt1 WHERE debt1.rechnr = debt.rechnr 
                AND debt1.counter  = debt.counter
                AND debt1.artnr = debt.artnr 
                AND debt.gastnr = debitor.gastnr
                AND debt1.zahlkonto  GT 0 NO-LOCK BY debt.rgdatum:
                ASSIGN
                  crdt = crdt + debt.saldo
                  fcrdt = fcrdt + debt.vesrdep.
                IF isprintedb4 AND debt1.debref = 0 THEN
                  ASSIGN
                    new-crdt = new-crdt + crdt
                    new-fcrdt = new-fcrdt + fcrdt.
              END.
          END.
        END.
          
        ASSIGN
          crdt      = - crdt
          fcrdt     = - fcrdt
          new-crdt  = - new-crdt
          new-fcrdt = - new-fcrdt.
          
        FOR EACH soabuff WHERE soabuff.done-step = 1:
          ASSIGN
            soabuff.done-step   = 2
            soabuff.debt        = debt-amount
            soabuff.credit      = crdt
            soabuff.saldo       = debt-amount - crdt
            soabuff.fdebt       = fdebt
            soabuff.fcredit     = fcrdt
            soabuff.fsaldo      = fdebt - fcrdt
            soabuff.newpayment  = new-crdt
            soabuff.newfpayment = new-fcrdt.
        END.
          /*FIND NEXT soa-list WHERE soa-list.done-step = 0
              USE-INDEX rechnr_ix NO-ERROR.FT serverless*/
      END.

/* &&& SLOW */
      FOR EACH soa-list:
          zeit = TIME.
          
          FIND FIRST debitor WHERE RECID(debitor) = soa-list.arRecid NO-LOCK.
          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK.
          
          IF debitor.betriebsnr = 0 THEN
          DO:
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                HIDE MESSAGE NO-PAUSE.
                MESSAGE "Bill " STRING(debitor.rechnr) "NOT FOUND at Department"
                    STRING(debitor.betriebsnr) 
                    VIEW-AS ALERT-BOX INFORMATION.
                IF debitor.debref NE 0 THEN DO:
                    FIND FIRST queasy WHERE queasy.KEY = 192 AND queasy.number1 = debitor.rechnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN soa-list.printed = YES.
                    ELSE IF NOT AVAILABLE queasy THEN soa-list.printed = NO.
                END.
                FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
                IF AVAILABLE gast THEN
                    soa-list.NAME       = gast.name + ", " + gast.vorname1 + " " 
                      + gast.anrede1 + gast.anredefirma.
                ELSE 
                    soa-list.NAME       = guest.name + ", " + guest.vorname1 + " " 
                      + guest.anrede1 + guest.anredefirma.
                NEXT.
            END.
            ASSIGN
                zeit1       = TIME
                other-flag  = NO.
            
            
            FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr AND 
                bill-line.artnr = debitor.artnr AND bill-line.departement = 0 NO-LOCK NO-ERROR.
            FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
    
            ASSIGN
                /*soa-list.datum      = bill.datum*/
                soa-list.refNo      = bill.billref
                soa-list.dptnr      = 0.

            /*ITA*/
            IF bill.billref NE 0 THEN DO:
                FIND FIRST bdebt WHERE bdebt.rechnr = soa-list.rechnr
                    AND bdebt.debref NE 0
                    AND bdebt.counter = soa-list.counter NO-LOCK NO-ERROR.
                IF AVAILABLE bdebt THEN DO:
                    ASSIGN soa-list.saldo = soa-list.saldo - bdebt.saldo
                           soa-list.debt  = soa-list.debt  - bdebt.saldo.
                    
                    IF soa-list.saldo NE 0 THEN DO:
                        FIND FIRST bdebt1 WHERE bdebt1.debref = 0
                            AND bdebt1.rechnr = soa-list.rechnr NO-LOCK NO-ERROR.
                        IF AVAILABLE bdebt1 THEN 
                            ASSIGN soa-list.arRecid = RECID(bdebt1)
                                   other-flag       = YES.
                    END.
                END.
            END.
                                    
            IF bill.billref = 0 THEN soa-list.printed = NO.
            ELSE DO: 
                IF other-flag = YES THEN DO: /*ITA*/
                    FIND FIRST queasy WHERE queasy.KEY = 192 AND queasy.number1 = debitor.rechnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN soa-list.printed = YES.
                    ELSE IF NOT AVAILABLE queasy THEN soa-list.printed = NO.                    
                END.
                ELSE soa-list.printed = YES.
            END.
                
    
            IF bill.logidat NE ? THEN soa-list.printdate  = bill.logidat.
            ELSE soa-list.printdate = TODAY.
             
            IF bill.billref NE 0 THEN
                soa-list.inv-str   = "INV" + STRING(bill.billref, "9999999").
            
            IF AVAILABLE bill-line THEN
                soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.
    
            IF AVAILABLE gast THEN
                soa-list.NAME       = gast.name + ", " + gast.vorname1 + " " 
                  + gast.anrede1 + gast.anredefirma.
            ELSE 
                soa-list.NAME       = guest.name + ", " + guest.vorname1 + " " 
                  + guest.anrede1 + guest.anredefirma.
    
           
            /*request by Sagita*/
            IF bill.resnr GT 0 THEN
            DO:
              FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.reslinnr = 
                bill.parent-nr NO-LOCK NO-ERROR.
           
              IF NOT AVAILABLE res-line THEN
                FIND FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK NO-ERROR.
    
              IF AVAILABLE res-line THEN
              /*MT 13/06/13 */
              DO: 
                  ASSIGN
                      soa-list.ankunft     = res-line.ankunft
                      soa-list.abreise     = res-line.abreise
                      soa-list.zinr        = res-line.zinr
                      soa-list.erwachs     = res-line.erwachs  /*ITA 140415*/
                      soa-list.child1      = res-line.kind1    /*ITA 140415*/
                      soa-list.child2      = res-line.kind2    /*ITA 140415*/
                      soa-list.roomrate    = res-line.zipreis  /*ITA 140415*/
                      soa-list.remarks     = soa-list.remarks + CHR(3) + STRING(res-line.resnr) /*EKO 211215*/.
                  
                  ASSIGN count-zimm = 0.
                  FOR EACH bresline WHERE bresline.resnr = res-line.resnr NO-LOCK:
                      ASSIGN count-zimm    = count-zimm + res-line.zimmeranz
                             soa-list.zimmeranz   = count-zimm.                   
                  END.

                  FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                  IF AVAILABLE zimkateg THEN soa-list.remarks = soa-list.remarks + CHR(3) + zimkateg.kurzbez + CHR(3) + zimkateg.bezeichnung. /*Eko 21 Jan 2015*/
                  ELSE soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3). 

                  /*Eko 19 MAY 2016, Anantara uluwatu*/
                  RUN get-room-breakdown.p(RECID(res-line), res-line.ankunft, 0,
                                           DATE(TODAY), OUTPUT Fnet-lodging, OUTPUT Lnet-lodging,
                                           OUTPUT net-breakfast, OUTPUT net-lunch, OUTPUT net-dinner, OUTPUT net-others,
                                           OUTPUT tot-rmrev, OUTPUT nett-vat, OUTPUT nett-service).

                  soa-list.remarks = soa-list.remarks + CHR(3) + STRING(nett-vat,">>>,>>>,>>9.99") + CHR(3) + STRING(nett-service,">>>,>>>,>>9.99").
                  /*Anantara Uluwatu*/

                  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                      str = ENTRY(i, res-line.zimmer-wunsch, ";").
                      IF SUBSTR(str,1,7) = "voucher" THEN 
                          soa-list.voucherNo1 = SUBSTR(str,8).
                  END.

                 FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                  NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                  DO:
                      /*bernatd 0ECB35 2024*/
                      IF bill.billtyp EQ 2 THEN
                      DO:
                      ASSIGN
                      soa-list.voucherNo2  = reservation.vesrdepot
                      soa-list.NAME    = res-line.NAME.
                      END.
                  END.
              END.
            END.
            ELSE DO:
                ASSIGN soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3) + CHR(3) + CHR(3) + CHR(3). /*Eko Jika nonstay guest bill tidak terdapat renr dan roomcateg*/
                       
            END.

            /*count gst for penang*/
            FOR EACH billine WHERE billine.rechnr = debitor.rechnr AND billine.anzahl NE 0 NO-LOCK:
                FIND FIRST artikel WHERE artikel.artnr = billine.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN DO:
                    IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                    DO:
                         ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + billine.betrag.
                         IF artikel.artart = 1 THEN DO:
                             ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                         END.
                         ELSE DO:
                             IF artikel.mwst-code NE 0 THEN
                                 ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                             IF artikel.mwst-code EQ 0 THEN
                                 ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + billine.betrag.

                         END.
                    END.
                END.
            END.
          END. /* debitor.betriebsnr = 0*/
          ELSE
          DO:
            FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr 
                AND h-bill.departement = debitor.betriebsnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE h-bill THEN
            DO:
                HIDE MESSAGE NO-PAUSE.
                MESSAGE "Bill " STRING (debitor.rechnr) " NOT FOUND at department "
                    STRING(debitor.betriebsnr).
                NEXT.
            END.
            ELSE
            DO:
                
                FIND FIRST hoteldpt WHERE hoteldpt.num = debitor.betriebsnr
                    NO-LOCK.
                
                ASSIGN
                    soa-list.refNo      = h-bill.service[6]
                    soa-list.dptnr      = debitor.betriebsnr
                    soa-list.outlet     = YES
                    .
    
                FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
    
                IF h-bill.bilname NE "" THEN
                    soa-list.NAME       = hoteldpt.depart + " - " + h-bill.bilname.
                ELSE 
                DO:
                    IF AVAILABLE gast THEN
                        soa-list.NAME = hoteldpt.depart + " - " + Gast.name + ", " + 
                            gast.vorname1 + " " + gast.anrede1 + gast.anredefirma.
                    ELSE
                        soa-list.NAME = hoteldpt.depart + " - " + guest.name + ", " + 
                            guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
                END.
                    
    
                IF h-bill.service[7] NE 0 THEN
                DO:
                    IF LENGTH(STRING(h-bill.service[7])) LT 8 THEN
                        soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,1)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 2,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 4,4))).
                    ELSE
                        soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 3,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 5,4))).
                END.
                ELSE soa-list.printdate = TODAY.
    
                IF INTEGER(h-bill.service[6]) NE 0 THEN
                    soa-list.inv-str   = "INV" + STRING(h-bill.service[6], "9999999").
                /*IF AVAILABLE bill-line THEN
                    soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
                
                IF h-bill.service[6] = 0 THEN soa-list.printed = NO.
                ELSE soa-list.printed = YES.

                /*count gst for penang*/
                FOR EACH hbilline WHERE hbilline.rechnr = h-bill.rechnr NO-LOCK:
                    FIND FIRST h-artikel WHERE h-artikel.artnr = hbilline.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE h-artikel THEN DO:
                        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront NO-LOCK NO-ERROR.
                        IF AVAILABLE artikel THEN DO:
                            IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                            DO:
                                 ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + hbilline.betrag.
                                 IF artikel.artart = 1 THEN DO:
                                        ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                                 END.
                                 ELSE DO:
                                     IF artikel.mwst-code NE 0 THEN
                                         ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                                     IF artikel.mwst-code EQ 0 THEN
                                         ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + hbilline.betrag.

                                 END.
                            END.
                        END.
                    END.
                    /* Rulita |  1E88B5 ADJUSTMENT UI PRINT SOA */
                    ASSIGN soa-list.bill-datum = hbilline.bill-datum.
                END.
            END.
          END. /*Outlet bill*/
      END. /* each soa-list*/
  END.
  /*wen*/
  ELSE IF show-type = 2 THEN
  DO:
       FOR EACH debitor WHERE debitor.gastnr = guestno 
          AND debitor.opart LE 1 AND debitor.saldo NE 0
          AND debitor.zahlkonto = 0 NO-LOCK,
          FIRST artikel WHERE artikel.artnr = debitor.artnr AND 
          artikel.artart = 2 AND artikel.departement = 0 NO-LOCK:
          DO:               
              CREATE soa-list.
              ASSIGN soa-list.to-sort   = 1 
                  soa-list.arRecid      = RECID(debitor)
                  soa-list.rechnr       = debitor.rechnr 
                  soa-list.gastnr       = debitor.gastnr
                  soa-list.datum        = debitor.rgdatum
                  soa-list.remarks      = debitor.vesrcod
                  soa-list.dptnr        = debitor.betriebsnr
                  
                  soa-list.artno        = debitor.artnr
                  soa-list.counter      = debitor.counter
                  soa-list.debref       = debitor.debref    /*MTT*/
                  soa-list.saldo        = soa-list.saldo + debitor.saldo
                  soa-list.vesrdep      = debitor.vesrdep.

          END.
      END.

      /*FIND FIRST soa-list WHERE soa-list.done-step = 0
          USE-INDEX rechnr_ix NO-ERROR.
      DO WHILE AVAILABLE soa-list:*/
      FOR EACH soa-list WHERE soa-list.done-step = 0
          USE-INDEX rechnr_ix NO-LOCK:
          ASSIGN 
              crdt = 0
              debt-amount = 0
              fcrdt = 0
              fdebt = 0
              new-crdt = 0
              new-fcrdt = 0 
              isprintedb4 = (soa-list.debref GT 0)
          .
          FOR EACH soabuff WHERE soabuff.rechnr = soa-list.rechnr
              AND soabuff.dptnr = soa-list.dptnr
              AND soabuff.artno = soa-list.artno
              AND soabuff.done-step = 0
              /*AND RECID(soabuff) = RECID(soa-list) FT serverless*/
              AND soabuff.arrecid = soa-list.arrecid:
              ASSIGN
                   soabuff.done-step = 1
                   debt-amount       = soabuff.saldo
                   fdebt             = fdebt + soabuff.vesrdep 
              .
              IF soabuff.counter GT 0 THEN
              FOR EACH debt WHERE 
                  debt.rechnr     = soabuff.rechnr 
                  AND debt.counter    = soabuff.counter
                  /*AND debt.betriebsnr = soabuff.dptnr*/
                  AND debt.gastnr     = guestno
                  AND debt.zahlkonto  > 0 NO-LOCK:
                  ASSIGN
                    fcrdt = fcrdt + debt.vesrdep
                    crdt  = crdt + debt.saldo
                  .
                  IF isprintedb4 AND debt.debref = 0 THEN
                  ASSIGN
                    new-crdt  = new-crdt + crdt
                    new-fcrdt = new-fcrdt + fcrdt
                  .
              END.

              /*MT 171212 */
              FOR EACH debt WHERE debt.rechnr = soabuff.rechnr 
                  AND debt.gastnr = soabuff.gastnr
                  AND debt.betriebsnr = soabuff.dptnr
                  AND debt.opart LE 1 AND soabuff.saldo NE 0 /*1*/
                  AND debt.zahlkonto = 0 AND RECID(debt) NE soa-list.arRecid NO-LOCK,
                  FIRST artikel WHERE artikel.artnr = debt.artnr
                  AND artikel.artart  = 2 AND artikel.departement = 0 NO-LOCK:
                  /*ASSIGN
                     debt = debt + debt.saldo
                     fdebt = fdebt + debt.vesrdep .*/
                  IF debt.counter GT 0 THEN
                  FOR EACH debt1 WHERE debt1.rechnr = debt.rechnr 
                      AND debt1.counter  = debt.counter
                      AND debt1.artnr = debt.artnr 
                      AND debt.gastnr = debitor.gastnr
                      AND debt1.zahlkonto  GT 0 NO-LOCK BY debt.rgdatum:
                      ASSIGN
                          crdt = crdt + debt.saldo
                          fcrdt = fcrdt + debt.vesrdep.
                      IF isprintedb4 AND debt1.debref = 0 THEN
                        ASSIGN
                         new-crdt = new-crdt + crdt
                         new-fcrdt = new-fcrdt + fcrdt.
                  END.
              END.
          END.
          ASSIGN
              crdt      = - crdt
              fcrdt     = - fcrdt
              new-crdt  = - new-crdt
              new-fcrdt = - new-fcrdt
          .
        
         
          /*ITA 020518*/
          FOR EACH soabuff WHERE soabuff.done-step = 1:
              
            ASSIGN
              soabuff.done-step   = 2
              soabuff.debt        = debt-amount
              soabuff.credit      = crdt
              soabuff.saldo       = debt-amount - crdt
              soabuff.fdebt       = fdebt
              soabuff.fcredit     = fcrdt
              soabuff.fsaldo      = fdebt - fcrdt
              soabuff.newpayment  = new-crdt
              soabuff.newfpayment = new-fcrdt
            .
          END.

          /*FIND NEXT soa-list WHERE soa-list.done-step = 0
              USE-INDEX rechnr_ix NO-ERROR.FT serverless*/
      END.

/* &&& SLOW */
      FOR EACH soa-list:
           zeit = TIME.
           
          FIND FIRST debitor WHERE RECID(debitor) = soa-list.arRecid NO-LOCK.

          FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK.
          
          IF debitor.betriebsnr = 0 THEN
          DO:
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bill THEN
            DO:
                HIDE MESSAGE NO-PAUSE.
                MESSAGE "Bill " STRING(debitor.rechnr) "NOT FOUND at Department"
                    STRING(debitor.betriebsnr) 
                    VIEW-AS ALERT-BOX INFORMATION.
                NEXT.
            END.

            zeit1 = TIME.

            FIND FIRST bill-line WHERE bill-line.rechnr = debitor.rechnr AND 
                bill-line.artnr = debitor.artnr AND bill-line.departement = 0
                NO-LOCK NO-ERROR.

            FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK
                NO-ERROR.
    
            ASSIGN
                /*soa-list.datum      = bill.datum 
                soa-list.refNo      = bill.billref*/
                 soa-list.refNo     = debitor.debref
                soa-list.dptnr      = 0.
            
            /*
            IF bill.billref = 0 THEN soa-list.printed = NO.
            ELSE soa-list.printed = YES.
                
            IF bill.billref NE 0 THEN
                soa-list.inv-str   = "INV" + STRING(bill.billref, "9999999").*/

            IF debitor.debref = 0 THEN soa-list.printed = NO.
            ELSE soa-list.printed = YES.

            IF debitor.debref NE 0 THEN 
                ASSIGN soa-list.inv-str   = "INV" + STRING(debitor.debref, "9999999").


    
            IF bill.logidat NE ? THEN soa-list.printdate  = bill.logidat.
            ELSE soa-list.printdate = TODAY.
             
            
            
            IF AVAILABLE bill-line THEN
                soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR. 
    
            IF AVAILABLE gast THEN
                soa-list.NAME       = gast.name + ", " + gast.vorname1 + " " 
                  + gast.anrede1 + gast.anredefirma.
            ELSE 
                soa-list.NAME       = guest.name + ", " + guest.vorname1 + " " 
                  + guest.anrede1 + guest.anredefirma.
    
           
            /*request by Sagita*/
            IF bill.resnr GT 0 THEN
            DO:
              FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.reslinnr = 
                bill.parent-nr NO-LOCK NO-ERROR.
           
              IF NOT AVAILABLE res-line THEN
                FIND FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK NO-ERROR.
    
              IF AVAILABLE res-line THEN
              /*MT 13/06/13 */
              DO: 
                  ASSIGN
                      soa-list.ankunft     = res-line.ankunft
                      soa-list.abreise     = res-line.abreise
                      soa-list.zinr        = res-line.zinr
                      soa-list.erwachs     = res-line.erwachs  /*ITA 140415*/
                      soa-list.child1      = res-line.kind1    /*ITA 140415*/
                      soa-list.child2      = res-line.kind2    /*ITA 140415*/
                      soa-list.roomrate    = res-line.zipreis  /*ITA 140415*/
                      soa-list.remarks     = soa-list.remarks + CHR(3) + STRING(res-line.resnr) /*EKO 211215*/.
                    
                  
                  ASSIGN count-zimm = 0.
                  FOR EACH bresline WHERE bresline.resnr = res-line.resnr NO-LOCK:
                      ASSIGN count-zimm    = count-zimm + res-line.zimmeranz
                             soa-list.zimmeranz   = count-zimm.                   
                  END.

                  FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
                  IF AVAILABLE zimkateg THEN soa-list.remarks = soa-list.remarks + CHR(3) + zimkateg.kurzbez + CHR(3) + zimkateg.bezeichnung. /*Eko 21 Jan 2015*/
                  ELSE soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3). 

                  /*Eko 19 MAY 2016, Anantara uluwatu*/
                  RUN get-room-breakdown.p(RECID(res-line), res-line.ankunft, 0,
                                           DATE(TODAY), OUTPUT Fnet-lodging, OUTPUT Lnet-lodging,
                                           OUTPUT net-breakfast, OUTPUT net-lunch, OUTPUT net-dinner, OUTPUT net-others,
                                           OUTPUT tot-rmrev, OUTPUT nett-vat, OUTPUT nett-service).

                  soa-list.remarks = soa-list.remarks + CHR(3) + STRING(nett-vat,">>>,>>>,>>9.99") + CHR(3) + STRING(nett-service,">>>,>>>,>>9.99").
                  /*Anantara Uluwatu*/

                  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                      str = ENTRY(i, res-line.zimmer-wunsch, ";").
                      IF SUBSTR(str,1,7) = "voucher" THEN 
                          soa-list.voucherNo1 = SUBSTR(str,8).
                  END.

                  FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
                      NO-LOCK NO-ERROR.
                  IF AVAILABLE reservation THEN
                      soa-list.voucherNo2  = reservation.vesrdepot.
              END.
            END.
            ELSE DO:
                ASSIGN soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3) + CHR(3) + CHR(3) + CHR(3). /*Eko Jika nonstay guest bill tidak terdapat renr dan roomcateg*/
            END.

            /*count gst for penang*/
            FOR EACH billine WHERE billine.rechnr = debitor.rechnr AND billine.anzahl NE 0 NO-LOCK:
                FIND FIRST artikel WHERE artikel.artnr = billine.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN DO:
                    IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                    DO:
                         ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + billine.betrag.
                         IF artikel.artart = 1 THEN DO:
                             ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                         END.
                         ELSE DO:
                             IF artikel.mwst-code NE 0 THEN
                                 ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                             IF artikel.mwst-code EQ 0 THEN
                                 ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + billine.betrag.

                         END.
                    END.
                END.
            END.
          END. /* debitor.betriebsnr = 0*/
          ELSE
          DO:
            FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr 
                AND h-bill.departement = debitor.betriebsnr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE h-bill THEN
            DO:
                HIDE MESSAGE NO-PAUSE.
                MESSAGE "Bill " STRING (debitor.rechnr) " NOT FOUND at department "
                    STRING(debitor.betriebsnr).
                NEXT.
            END.
            ELSE
            DO:
               
                FIND FIRST hoteldpt WHERE hoteldpt.num = debitor.betriebsnr
                    NO-LOCK.
                
                ASSIGN
                    soa-list.refNo      = h-bill.service[6]
                    soa-list.dptnr      = debitor.betriebsnr
                    soa-list.outlet     = YES
                    .
    
                FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.
    
                IF h-bill.bilname NE "" THEN
                    soa-list.NAME       = hoteldpt.depart + " - " + h-bill.bilname.
                ELSE 
                DO:
                    IF AVAILABLE gast THEN
                        soa-list.NAME = hoteldpt.depart + " - " + Gast.name + ", " + 
                            gast.vorname1 + " " + gast.anrede1 + gast.anredefirma.
                    ELSE
                        soa-list.NAME = hoteldpt.depart + " - " + guest.name + ", " + 
                            guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
                END.
                    
    
                IF h-bill.service[7] NE 0 THEN
                DO:
                    IF LENGTH(STRING(h-bill.service[7])) LT 8 THEN
                        soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,1)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 2,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 4,4))).
                    ELSE
                        soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 3,2)),
                                              INTEGER(SUBSTR(STRING(h-bill.service[7]), 5,4))).
                END.
                ELSE soa-list.printdate = TODAY.
    
                IF INTEGER(h-bill.service[6]) NE 0 THEN
                    soa-list.inv-str   = "INV" + STRING(h-bill.service[6], "9999999").
                /*IF AVAILABLE bill-line THEN
                    soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
                
                IF h-bill.service[6] = 0 THEN soa-list.printed = NO.
                ELSE soa-list.printed = YES.

                /*count gst for penang*/
                FOR EACH hbilline WHERE hbilline.rechnr = h-bill.rechnr NO-LOCK:
                    FIND FIRST h-artikel WHERE h-artikel.artnr = hbilline.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE h-artikel THEN DO:
                        FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront NO-LOCK NO-ERROR.
                        IF AVAILABLE artikel THEN DO:
                            IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                            DO:
                                 ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + hbilline.betrag.
                                 IF artikel.artart = 1 THEN DO:
                                        ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                                 END.
                                 ELSE DO:
                                     IF artikel.mwst-code NE 0 THEN
                                         ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                                     IF artikel.mwst-code EQ 0 THEN
                                         ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + hbilline.betrag.

                                 END.
                            END.
                        END.
                    END.
                    /* Rulita |  1E88B5 ADJUSTMENT UI PRINT SOA */
                    ASSIGN soa-list.bill-datum = hbilline.bill-datum.
                END.
            END.
          END. /*Outlet bill*/
      END. /* each soa-list*/   
  END.
  ELSE
  DO: 
      DEF VAR nmonth AS INTEGER.
      DEF VAR mnth1 AS INTEGER.
      DEF VAR year2 AS INTEGER.
      DEF VAR counter-saldo AS DECIMAL INITIAL 0.

      DEF VAR val-param AS INTEGER.
      DEF VAR var-param AS CHAR.

      RUN call-paramAr( 4 ,  OUTPUT param4 ).
      IF param4 = "" THEN due-date = curr-day.
      ELSE
      DO:
        var-param = SUBSTR(param4, LENGTH(param4) , 1).   
        val-param = INT(SUBSTR(param4, 1, LENGTH(param4) - 1)). 
        IF var-param = "D" OR var-param = "d" THEN
        DO:
            due-date = eof-month + val-param.
        END.
        ELSE IF var-param = "M" OR var-param = "m" THEN
        DO:
          nmonth = MONTH(eof-month) + val-param.
          IF nmonth > 12 THEN
          DO:
            ASSIGN mnth1 = 1
                   year2 = YEAR (eof-month) + 1.
          END.
          ELSE
          DO:
            ASSIGN mnth1 = nmonth
                   year2 = YEAR (eof-month) .
          END.
          RUN lastDate-inMonth(INPUT mnth1,INPUT year2,OUTPUT due-date).
        END.
        ELSE IF var-param = "Y" OR var-param = "y" THEN
        DO:
            ASSIGN mnth1 = MONTH(eof-month)
                   year2 = YEAR (eof-month) + val-param.
            RUN lastDate-inMonth(INPUT mnth1,INPUT year2,OUTPUT due-date).
        END.
        ELSE 
        DO:
            ASSIGN mnth1 = MONTH(eof-month)
                   year2 = YEAR (eof-month).
            RUN lastDate-inMonth(INPUT mnth1,INPUT year2,OUTPUT due-date).
        END.
      END.
     
      FOR EACH debitor WHERE debitor.gastnr = guestno AND debitor.zahlkonto = 0 
          AND debitor.saldo NE 0 AND debitor.rgdatum LT bof-month /*AND debitor.opart = 0*/ NO-LOCK:
          saldo1 = saldo1 + debitor.saldo.
      END.
    
      FOR EACH debitor WHERE debitor.gastnr = guestno AND debitor.zahlkonto > 0 
          AND debitor.rgdatum LT bof-month 
          AND debitor.saldo NE 0 AND debitor.opart LE 2 NO-LOCK:
          saldo2 = saldo2 + debitor.saldo.
      END.
    
      FOR EACH debitor WHERE debitor.gastnr = guestno AND debitor.zahlkonto > 0 
          AND debitor.rgdatum GE bof-month AND debitor.rgdatum LE eof-month 
          AND debitor.saldo NE 0 AND debitor.opart LE 2 NO-LOCK:
          saldo4 = saldo4 + debitor.saldo.
      END.
    
      RUN call-paramAr( 2 ,  OUTPUT param2 ).

      CREATE soa-list.
      ASSIGN soa-list.to-sort = 0 
             soa-list.NAME    = param2
             soa-list.debt    = 0 /*saldo1 + saldo2*/
             soa-list.credit  = 0
             soa-list.saldo   = saldo1 + saldo2
             soa-list.fsaldo  = saldo1 + saldo2.

      RUN call-paramAr( 1 ,  OUTPUT param1 ).
      IF param1 = "yes" THEN counter-saldo = counter-saldo + saldo1 + saldo2.
      ELSE counter-saldo = 0 .

      FOR EACH debitor WHERE debitor.gastnr = guestno 
          /*AND debitor.opart LE 1 */ AND debitor.saldo NE 0
          AND debitor.zahlkonto = 0 AND 
          debitor.rgdatum GE bof-month  AND debitor.rgdatum LE eof-month NO-LOCK,
          FIRST artikel WHERE artikel.artnr = debitor.artnr AND 
          artikel.artart = 2 AND artikel.departement = 0 NO-LOCK BY debitor.rgdatum BY debitor.rechnr :
          
          IF param1 = "yes" THEN counter-saldo = counter-saldo + debitor.saldo.
          ELSE counter-saldo = debitor.saldo .

          CREATE soa-list.
          ASSIGN soa-list.to-sort   = 1 
                  soa-list.arRecid      = RECID(debitor)
                  soa-list.rechnr       = debitor.rechnr 
                  soa-list.gastnr       = debitor.gastnr
                  soa-list.datum        = debitor.rgdatum
                  soa-list.remarks      = debitor.vesrcod
                  soa-list.dptnr        = debitor.betriebsnr
                  soa-list.debt         = debitor.saldo 
                  soa-list.credit       = 0
                  soa-list.saldo        = counter-saldo /*debitor.saldo*/ 
                  soa-list.fsaldo       = counter-saldo.    
      END.


  FOR EACH soa-list,
      FIRST debitor WHERE RECID(debitor) = soa-list.arRecid NO-LOCK,
      FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK:
      ASSIGN 
          crdt = 0
          debt-amount = 0 
          fcrdt = 0 
          fdebt = 0
          new-crdt = 0 
          new-fcrdt = 0 
          isprintedb4 = FALSE.

      IF debitor.debref NE 0 THEN isprintedb4 = TRUE.
      
      ASSIGN
          debt-amount = debitor.saldo
          fdebt = debitor.vesrdep.
      IF debitor.counter GT 0 THEN
          FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
              AND debt.counter  = debitor.counter
              AND debt.artnr = debitor.artnr 
              AND debt.betriebsnr = debitor.betriebsnr
              AND debt.gastnr = debitor.gastnr
              AND debt.zahlkonto  GT 0 NO-LOCK BY debt.rgdatum:
            ASSIGN
              fcrdt     = fcrdt + debt.vesrdep
              crdt      = crdt + debt.saldo.
            IF isprintedb4 AND debt.debref = 0 THEN
                ASSIGN
                 new-crdt = new-crdt + crdt
                 new-fcrdt = new-fcrdt + fcrdt.
          END.

      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
          AND debt.gastnr = debitor.gastnr
          AND debt.betriebsnr = debitor.betriebsnr
          AND debt.opart LE 1 AND debitor.saldo NE 0
          AND debt.zahlkonto = 0 AND RECID(debt) NE RECID(debitor) NO-LOCK,
          FIRST artikel WHERE artikel.artnr = debt.artnr
          AND artikel.artart  = 2 AND artikel.departement = 0 NO-LOCK:
          ASSIGN
             debt-amount = debt-amount + debt.saldo
             fdebt = fdebt + debt.vesrdep .
          IF debt.counter GT 0 THEN
               FOR EACH debt1 WHERE debt1.rechnr = debt.rechnr 
                  AND debt1.counter  = debt.counter
                  AND debt1.artnr = debt.artnr 
                  AND debt.gastnr = debitor.gastnr
                  AND debt1.zahlkonto  GT 0 NO-LOCK BY debt.rgdatum:
              ASSIGN
                  crdt = crdt + debt.saldo
                  fcrdt = fcrdt + debt.vesrdep.
              IF isprintedb4 AND debt1.debref = 0 THEN
                ASSIGN
                 new-crdt = new-crdt + crdt
                 new-fcrdt = new-fcrdt + fcrdt.
              END.
      END.
      
      ASSIGN
          crdt = - crdt
          fcrdt = - fcrdt
          new-crdt = - new-crdt
          new-fcrdt = - new-fcrdt.

      IF debitor.betriebsnr = 0 THEN
      DO:
        FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bill THEN
        DO:
            rech-nr = debitor.rechnr.
            bet-nr = debitor.betriebsnr.
            msg-int = 1.
            NEXT.
        END.
            
        FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr AND 
            bill-line.artnr = artikel.artnr AND bill-line.departement = 0
            NO-LOCK NO-ERROR.
        FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK.

        ASSIGN
            /*soa-list.datum      = bill.datum*/
            soa-list.refNo      = bill.billref
            soa-list.dptnr      = 0    .
        

        IF bill.billref = 0 THEN soa-list.printed = NO.
        ELSE soa-list.printed = YES.

        IF bill.logidat NE ? THEN soa-list.printdate  = bill.logidat.
        ELSE soa-list.printdate = TODAY.
         
        IF bill.billref NE 0 THEN
            soa-list.inv-str   = "INV" + STRING(bill.billref, "9999999").
        IF AVAILABLE bill-line THEN
            soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.

        IF AVAILABLE gast THEN
            soa-list.NAME       = gast.name + ", " + gast.vorname1 + " " 
              + gast.anrede1 + gast.anredefirma.
        ELSE 
            soa-list.NAME       = guest.name + ", " + guest.vorname1 + " " 
              + guest.anrede1 + guest.anredefirma.

       
        /*request by Sagita*/
       FIND FIRST res-line WHERE res-line.resnr = bill.resnr AND res-line.reslinnr = 
           bill.parent-nr NO-LOCK NO-ERROR.
       
       IF NOT AVAILABLE res-line THEN
           FIND FIRST res-line WHERE res-line.resnr = bill.resnr NO-LOCK NO-ERROR.

       IF AVAILABLE res-line THEN DO:
           ASSIGN
               soa-list.ankunft     = res-line.ankunft
               soa-list.abreise     = res-line.abreise
               soa-list.zinr        = res-line.zinr
               soa-list.erwachs     = res-line.erwachs  /*ITA 140415*/
               soa-list.child1      = res-line.kind1    /*ITA 140415*/
               soa-list.child2      = res-line.kind2    /*ITA 140415*/
               soa-list.roomrate    = res-line.zipreis /*ITA 140415*/    
               soa-list.remarks     = soa-list.remarks + CHR(3) + STRING(res-line.resnr) /*EKO 211215*/.

           ASSIGN count-zimm = 0.
           FOR EACH bresline WHERE bresline.resnr = res-line.resnr NO-LOCK:
              ASSIGN count-zimm    = count-zimm + res-line.zimmeranz
                     soa-list.zimmeranz   = count-zimm.                   
           END.
            
           FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
           IF AVAILABLE zimkateg THEN soa-list.remarks = soa-list.remarks + CHR(3) + zimkateg.kurzbez + CHR(3) + zimkateg.bezeichnung. /*Eko 21 Jan 2015*/
           ELSE soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3). 
    
           /*Eko 19 MAY 2016, Anantara uluwatu*/
           RUN get-room-breakdown.p(RECID(res-line), res-line.ankunft, 0,
                                    DATE(TODAY), OUTPUT Fnet-lodging, OUTPUT Lnet-lodging,
                                    OUTPUT net-breakfast, OUTPUT net-lunch, OUTPUT net-dinner, OUTPUT net-others,
                                    OUTPUT tot-rmrev, OUTPUT nett-vat, OUTPUT nett-service).
    
           soa-list.remarks = soa-list.remarks + CHR(3) + STRING(nett-vat,">>>,>>>,>>9.99") + CHR(3) + STRING(nett-service,">>>,>>>,>>9.99").
           /*Anantara Uluwatu*/
    
           DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
               str = ENTRY(i, res-line.zimmer-wunsch, ";").
               IF SUBSTR(str,1,7) = "voucher" THEN 
                   soa-list.voucherNo1 = SUBSTR(str,8).
           END.
    
           FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
               NO-LOCK NO-ERROR.
           IF AVAILABLE reservation THEN
               soa-list.voucherNo2  = reservation.vesrdepot.
       END.
       ELSE DO:
           ASSIGN soa-list.remarks = soa-list.remarks + CHR(3) + CHR(3) + CHR(3) + CHR(3) + CHR(3). /*Eko Jika nonstay guest bill tidak terdapat renr dan roomcateg*/
       END.


       /*count gst for penang*/
        FOR EACH billine WHERE billine.rechnr = debitor.rechnr AND billine.anzahl NE 0 NO-LOCK:
            FIND FIRST artikel WHERE artikel.artnr = billine.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN DO:
                IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                DO:
                     ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + billine.betrag.
                     IF artikel.artart = 1 THEN DO:
                           ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                     END.
                     ELSE DO:
                         IF artikel.mwst-code NE 0 THEN
                             ASSIGN soa-list.gst-amount = soa-list.gst-amount + (billine.betrag / 1.06).
                         IF artikel.mwst-code EQ 0 THEN
                             ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + billine.betrag.
                     END.
                END.
            END.
        END.
      END. /* debitor.betriebsnr = 0*/
      ELSE
      DO:
         FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr 
            AND h-bill.departement = debitor.betriebsnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE h-bill THEN
        DO:
            rech-nr = debitor.rechnr.
            bet-nr = debitor.betriebsnr.
            msg-int = 2.
            NEXT.
        END.
        ELSE
        DO:
           
            FIND FIRST hoteldpt WHERE hoteldpt.num = debitor.betriebsnr
                NO-LOCK.
            
            ASSIGN
                soa-list.refNo      = h-bill.service[6]
                soa-list.dptnr      = debitor.betriebsnr
                soa-list.outlet     = YES
                .

            FIND FIRST gast WHERE gast.gastnr = debitor.gastnrmember NO-LOCK NO-ERROR.

            IF h-bill.bilname NE "" THEN
                soa-list.NAME       = hoteldpt.depart + " - " + h-bill.bilname.
            ELSE 
            DO:
                IF AVAILABLE gast THEN
                    soa-list.NAME = hoteldpt.depart + " - " + Gast.name + ", " + 
                        gast.vorname1 + " " + gast.anrede1 + gast.anredefirma.
                ELSE
                    soa-list.NAME = hoteldpt.depart + " - " + guest.name + ", " + 
                        guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.
            END.
                

            IF h-bill.service[7] NE 0 THEN
            DO:
                
                IF LENGTH(STRING(h-bill.service[7])) LT 8 THEN
                    soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,1)),
                                          INTEGER(SUBSTR(STRING(h-bill.service[7]), 2,2)),
                                          INTEGER(SUBSTR(STRING(h-bill.service[7]), 4,4))).
                ELSE
                    soa-list.printdate = DATE(INTEGER(SUBSTR(STRING(h-bill.service[7]), 1,2)),
                                          INTEGER(SUBSTR(STRING(h-bill.service[7]), 3,2)),
                                          INTEGER(SUBSTR(STRING(h-bill.service[7]), 5,4))).
                                          
            END.
            ELSE soa-list.printdate = TODAY.

            IF INTEGER(h-bill.service[6]) NE 0 THEN
                soa-list.inv-str   = "INV" + STRING(h-bill.service[6], "9999999").
            /*IF AVAILABLE bill-line THEN
                soa-list.voucherno  = ENTRY(2, bill-line.bezeich, "/") NO-ERROR.*/
            
            IF h-bill.service[6] = 0 THEN soa-list.printed = NO.
            ELSE soa-list.printed = YES.

            /*count gst for penang*/
            FOR EACH hbilline WHERE hbilline.rechnr = h-bill.rechnr NO-LOCK:
                FIND FIRST h-artikel WHERE h-artikel.artnr = hbilline.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE h-artikel THEN DO:
                    FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront NO-LOCK NO-ERROR.
                    IF AVAILABLE artikel THEN DO:
                        IF artikel.artart = 0 OR artikel.artart = 1 OR artikel.artart = 8 OR artikel.artart = 9 THEN 
                        DO:
                             ASSIGN soa-list.gst-tot-sales = soa-list.gst-tot-sales + hbilline.betrag.
                             IF artikel.artart = 1 THEN DO:
                                 ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                             END.
                             ELSE DO:
                                 IF artikel.mwst-code NE 0 THEN
                                     ASSIGN soa-list.gst-amount = soa-list.gst-amount + (hbilline.betrag / 1.06).
                                 IF artikel.mwst-code EQ 0 THEN
                                     ASSIGN soa-list.gst-tot-non-taxable = soa-list.gst-tot-non-taxable + hbilline.betrag.

                             END.
                        END.
                    END.
                END.
                /* Rulita |  1E88B5 ADJUSTMENT UI PRINT SOA */
                ASSIGN soa-list.bill-datum = hbilline.bill-datum.
            END.
        END.
      END. /*Outlet bill*/
  END. /* each soa-list*/
  
  END.

   IF show-type = 1 THEN
   DO:
    RUN call-paramAr( 3 ,  OUTPUT param3 ).

    IF param1 = "yes" THEN counter-saldo = counter-saldo +  saldo3 + saldo4.
    ELSE counter-saldo =  saldo3 + saldo4 .

    CREATE soa-list.
    ASSIGN soa-list.to-sort = 2 
           soa-list.NAME    = param3
           soa-list.debt    = 0
           soa-list.credit  = saldo3 + saldo4
           soa-list.saldo   = counter-saldo 
           soa-list.fsaldo  = counter-saldo.
  END.

  FOR EACH soa-list WHERE soa-list.saldo = 0 AND soa-list.to-sort = 1 : 
    DELETE soa-list. 
  END. 
END.
/*
IF show-type = 2 THEN
DO:
    MESSAGE "in1"
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
    RUN show-type.
END.*/

PROCEDURE call-paramAr:
    DEFINE INPUT PARAMETER nr AS INTEGER.
    DEFINE OUTPUT PARAMETER param-val AS CHAR.

    FIND FIRST param-ar WHERE param-ar.param-nr = nr NO-LOCK NO-ERROR.
    IF AVAILABLE param-ar THEN
        param-val  = param-ar.PARAM-val.
    ELSE                                
        param-val  = "".                
END.



PROCEDURE lastDate-inMonth:
DEFINE INPUT PARAMETER imonth       AS INTEGER.
DEFINE INPUT PARAMETER iyear        AS INTEGER.
DEFINE OUTPUT PARAMETER lastDate    AS DATE. 

DEFINE VARIABLE newmonth AS INTEGER.
DEFINE VARIABLE newyear  AS INTEGER.
DEFINE VARIABLE newdate  AS DATE.

newmonth = imonth + 1. 
IF newmonth > 12 THEN
DO:
    newmonth = newmonth - 12.
    newyear = iyear + 1. 
    newdate = DATE(newmonth, 1, newyear).
    lastdate = newdate - 1.
END.
ELSE
DO:
    newdate = DATE(newmonth , 1, iyear).
    lastdate = newdate - 1.
END.

END PROCEDURE.

