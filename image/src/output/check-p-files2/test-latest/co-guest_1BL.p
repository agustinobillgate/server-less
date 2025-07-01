
DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS INTEGER INITIAL 0 
  FIELD reihe      AS INTEGER INITIAL 0
  FIELD zinr       LIKE res-line.zinr 
  FIELD name       AS CHAR FORMAT "x(24)" COLUMN-LABEL "Guest Name" 
  FIELD zipreis    LIKE res-line.zipreis FORMAT ">>>,>>>,>>9.99" 
  FIELD s-zipreis  AS CHAR FORMAT "x(12)" INITIAL "" LABEL "   Room-Rate" 
  FIELD rechnr     LIKE bill.rechnr FORMAT ">>>,>>>,>>>" 
  FIELD ankunft    LIKE res-line.ankunft INITIAL ? 
  FIELD abreise    LIKE res-line.abreise INITIAL ? 
  FIELD cotime     AS CHAR FORMAT "x(5)" COLUMN-LABEL "CO-Time" 
  FIELD deposit    AS DECIMAL FORMAT ">,>>>,>>>,>>9"   COLUMN-LABEL "Deposit" 
  FIELD s-deposit  AS CHAR FORMAT "x(17)" COLUMN-LABEL "Deposit" 
  FIELD cash       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Cash" 
  FIELD s-cash     AS CHAR FORMAT "x(17)" COLUMN-LABEL "Cash" 
  FIELD cc         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "CreditCard" 
  FIELD s-cc       AS CHAR FORMAT "x(17)" COLUMN-LABEL "CreditCard" 
  FIELD cl         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" COLUMN-LABEL "CityLedger" 
  FIELD s-cl       AS CHAR FORMAT "x(17)" COLUMN-LABEL "CityLedger"
  FIELD tot        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Total" 
  FIELD s-tot      AS CHAR FORMAT "x(17)" COLUMN-LABEL "Total" 
  FIELD resnr      AS INTEGER FORMAT ">>>>>>>" INITIAL 0 COLUMN-LABEL "ResNo"
  FIELD company    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Company"
  /* ragung */
  FIELD bill-balance AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Bill Balance" 
  FIELD reslin-no  AS INTEGER
.

DEF INPUT PARAMETER case-type       AS INTEGER.
DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER fr-date         AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER price-decimal   AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.
/*
DEF VAR pvILanguage AS INT INIT 0.
DEF VAR case-type AS INT INIT 1.
DEF VAR fr-date AS DATE INIT 01/01/09.
DEF VAR to-date AS DATE INIT 01/01/09.
DEF VAR price-decimal AS INT INIT 0.
*/
DEFINE VARIABLE tot-rm      AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-deposit AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-cash    AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-cc      AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-cl      AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-amt     AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE tot-bb      AS DECIMAL INITIAL 0 NO-UNDO.
{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "co-guest". 

DEFINE BUFFER bresline FOR res-line.
 
IF case-type = 1 THEN RUN disp-billbalance.
ELSE RUN disp-DUbalance.

/******************************************************************************/

FOR EACH cl-list:   /*FD 25-10-19*/
    ASSIGN
        cl-list.s-deposit = STRING(cl-list.deposit,"->,>>>,>>>,>>9.99")
        cl-list.s-cc = STRING(cl-list.cc,"->,>>>,>>>,>>9.99")
        cl-list.s-cl = STRING(cl-list.cl,"->,>>>,>>>,>>9.99")
        cl-list.s-cash = STRING(cl-list.cash,"->,>>>,>>>,>>9.99")
        cl-list.s-tot = STRING(cl-list.tot,"->,>>>,>>>,>>9.99")
    .
END.

PROCEDURE disp-billbalance:
  DEFINE VARIABLE gname      AS CHAR. 
  DEFINE VARIABLE curr-zinr  AS CHAR INITIAL "". 
  DEFINE VARIABLE curr-resnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE billno     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE b-bal      AS INTEGER INITIAL 0. 
  DEFINE VARIABLE do-it      AS LOGICAL NO-UNDO INITIAL YES.

  tot-rm = 0.
  tot-deposit = 0.
  tot-cash = 0.
  tot-cc = 0.
  tot-cl = 0.
  tot-amt = 0.
  
  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
 
  FOR EACH res-line WHERE active-flag = 2 AND res-line.abreise GE fr-date 
      AND res-line.abreise LE to-date AND resstatus NE 9 
    AND resstatus NE 10 AND resstatus NE 99 NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
    BY res-line.zinr BY res-line.resnr BY res-line.reslinnr: 
    
    ASSIGN do-it = YES.

    FIND FIRST bresline WHERE bresline.resnr = res-line.resnr 
        AND bresline.reslinnr NE res-line.resstatus
        AND bresline.resstatus NE 12 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bresline THEN ASSIGN do-it = NO.
    
    IF do-it = YES THEN DO:
        billno = 0.
        b-bal  = 0.
        FIND FIRST bill WHERE bill.resnr = res-line.resnr 
          AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN 
            ASSIGN
            billno = bill.rechnr
            b-bal  = bill.saldo.
        ELSE 
        DO:
          FIND FIRST billhis WHERE billhis.resnr = res-line.resnr 
            AND billhis.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
          IF AVAILABLE billhis THEN billno = billhis.rechnr.
        END.
    
        IF curr-zinr NE res-line.zinr THEN 
        DO: 
          curr-zinr = res-line.zinr. 
          curr-resnr = res-line.resnr. 
          tot-rm = tot-rm + 1. 
        END. 
        ELSE IF curr-resnr NE res-line.resnr THEN 
        DO: 
          curr-resnr = res-line.resnr. 
          tot-rm = tot-rm + 1. 
        END. 
     
        create cl-list. 
        ASSIGN 
          cl-list.resnr             = reservation.resnr
          cl-list.reslin-no         = res-line.reslinnr
          cl-list.company           = reservation.name 
          cl-list.zinr              = res-line.zinr 
          cl-list.zipreis           = res-line.zipreis 
          cl-list.ankunft           = res-line.ankunft 
          cl-list.abreise           = res-line.abreise
          cl-list.rechnr            = billno
          cl-list.cotime            = STRING(res-line.abreisezeit,"HH:MM")
          cl-list.bill-balance      = b-bal. 
        
        IF res-line.resstatus = 12 THEN cl-list.name = translateExtended ("** Extra Bill",lvCAREA,""). 
        ELSE cl-list.name = res-line.name. 
     
        FOR EACH bill-line WHERE bill-line.rechnr = billno NO-LOCK: 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR. 
          IF AVAILABLE artikel THEN
          DO:
            IF artikel.artart = 2 THEN 
            DO: 
              cl-list.cl = cl-list.cl - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cl = tot-cl - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 5 THEN 
            DO: 
              cl-list.deposit = cl-list.deposit - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-deposit = tot-deposit - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 6 THEN 
            DO: 
              cl-list.cash = cl-list.cash - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cash = tot-cash - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 7 THEN 
            DO: 
              cl-list.cc = cl-list.cc - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cc = tot-cc - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END.
          END.           
        END.
    END.     
  END. 
 /*Modified by Bernatd 2024 F4E78F*/
  FOR EACH cl-list WHERE cl-list.flag = 0: 
    IF price-decimal = 0 THEN 
    DO: 
      IF cl-list.zipreis LE 9999999 THEN 
        cl-list.s-zipreis = STRING(cl-list.zipreis,">,>>>,>>9.99"). 
      ELSE 
        cl-list.s-zipreis = STRING(cl-list.zipreis," >>>,>>>,>>9.99"). 
    END. 
    ELSE DO:
      IF cl-list.zipreis LE 9999999 THEN 
        cl-list.s-zipreis = STRING(cl-list.zipreis,">,>>>,>>9.99"). 
      ELSE 
        cl-list.s-zipreis = STRING(cl-list.zipreis," >>>,>>>,>>9.99"). 
    END.
  END. 
  /*end bernatd*/
 
  CREATE cl-list. 
  ASSIGN 
      cl-list.reihe     = 1
      cl-list.NAME      = translateExtended ("Total C/O Room(s)",lvCAREA,"") 
      cl-list.s-zipreis = STRING(tot-rm,">>>>>>>>>>>9") 
      cl-list.deposit   = tot-deposit 
      cl-list.cash      = tot-cash 
      cl-list.cc        = tot-cc 
      cl-list.cl        = tot-cl 
      cl-list.tot       = tot-amt. 
 
  /*OPEN QUERY q1 FOR EACH cl-list NO-LOCK. */
END.


PROCEDURE disp-DUbalance: 
  DEFINE VARIABLE gname      AS CHAR. 
  DEFINE VARIABLE curr-zinr  AS CHAR INITIAL "". 
  DEFINE VARIABLE curr-resnr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE billno     AS INTEGER INITIAL 0. 
  DEFINE VARIABLE b-bal      AS INTEGER INITIAL 0.
  DEFINE VARIABLE do-it      AS LOGICAL INITIAL YES.
 
  tot-rm = 0.
  tot-deposit = 0.
  tot-cash = 0.
  tot-cc = 0.
  tot-cl = 0.
  tot-amt = 0.

  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
 
  FOR EACH res-line WHERE active-flag = 2 AND res-line.ankunft GE fr-date
    AND res-line.ankunft LE to-date
    AND res-line.abreise = res-line.ankunft AND resstatus NE 9 
    AND resstatus NE 10 AND resstatus NE 99 NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK
    BY res-line.zinr BY res-line.resnr BY res-line.reslinnr: 
    
    ASSIGN do-it = YES.
    FIND FIRST bresline WHERE bresline.resnr = res-line.resnr 
        AND bresline.reslinnr NE res-line.resstatus
        AND bresline.resstatus NE 12 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bresline THEN ASSIGN do-it = NO.
    
    IF do-it = YES THEN DO:
        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK. 
        billno = 0.
        b-bal  = 0.
        FIND FIRST bill WHERE bill.resnr = res-line.resnr 
          AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN DO:
             ASSIGN
             billno = bill.rechnr
             b-bal  = bill.saldo.
        END.
        ELSE 
        DO:
          FIND FIRST billhis WHERE billhis.resnr = res-line.resnr 
            AND billhis.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
          IF AVAILABLE billhis THEN billno = billhis.rechnr.
        END.
    
        IF curr-zinr NE res-line.zinr THEN 
        DO: 
          curr-zinr = res-line.zinr. 
          curr-resnr = res-line.resnr. 
          tot-rm = tot-rm + 1. 
        END. 
        ELSE IF curr-resnr NE res-line.resnr THEN 
        DO: 
          curr-resnr = res-line.resnr. 
          tot-rm = tot-rm + 1. 
        END. 
     
        CREATE cl-list. 
        ASSIGN 
          cl-list.resnr         = reservation.resnr
          cl-list.reslin-no     = res-line.reslinnr
          cl-list.company       = reservation.name 
          cl-list.zinr          = res-line.zinr 
          cl-list.zipreis       = res-line.zipreis 
          cl-list.rechnr        = billno 
          cl-list.ankunft       = res-line.ankunft 
          cl-list.abreise       = res-line.abreise
          cl-list.cotime        = STRING(res-line.abreisezeit,"HH:MM") 
          cl-list.bill-balance  = b-bal. 
    
        FIND FIRST bill-line WHERE bill-line.departement = 0
            AND bill-line.artnr = arrangement.argt-artikelnr
            AND bill-line.bill-datum = res-line.ankunft
            AND bill-line.massnr = res-line.resnr
            AND bill-line.billin-nr = res-line.reslinnr
            USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN cl-list.flag = 1.
     
        IF res-line.resstatus = 12 THEN cl-list.name = translateExtended ("** Extra Bill",lvCAREA,""). 
        ELSE cl-list.name = res-line.name. 
     
        FOR EACH bill-line WHERE bill-line.rechnr = billno NO-LOCK: 
          FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN
          DO:
            IF artikel.artart = 2 THEN 
            DO: 
              cl-list.cl = cl-list.cl - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cl = tot-cl - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 5 THEN 
            DO: 
              cl-list.deposit = cl-list.deposit - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-deposit = tot-deposit - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 6 THEN 
            DO: 
              cl-list.cash = cl-list.cash - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cash = tot-cash - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END. 
            IF artikel.artart = 7 THEN 
            DO: 
              cl-list.cc = cl-list.cc - bill-line.betrag. 
              cl-list.tot = cl-list.tot - bill-line.betrag. 
              tot-cc = tot-cc - bill-line.betrag. 
              tot-amt = tot-amt - bill-line.betrag. 
            END.
          END. 
        END.
    END.    
  END. 
  
  /*Modified by Bernatd 2024 F4E78F*/
  FOR EACH cl-list /*WHERE cl-list.flag = 0*/: 
    IF price-decimal = 0 THEN 
    DO: 
      IF cl-list.zipreis LE 9999999 THEN 
        cl-list.s-zipreis = STRING(cl-list.zipreis,">,>>>,>>9.99"). 
      ELSE 
        cl-list.s-zipreis = STRING(cl-list.zipreis," >>>,>>>,>>9.99"). 
    END. 
    ELSE DO:
      IF cl-list.zipreis LE 9999999 THEN 
        cl-list.s-zipreis = STRING(cl-list.zipreis,">,>>>,>>9.99"). 
      ELSE 
        cl-list.s-zipreis = STRING(cl-list.zipreis," >>>,>>>,>>9.99"). 
    END.
  END. 
  /*end bernatd*/

  CREATE cl-list. 
  ASSIGN 
      cl-list.flag      = 2
      cl-list.reihe     = 1
      cl-list.NAME      = translateExtended ("Total C/O Room(s)",lvCAREA,"") 
      cl-list.s-zipreis = STRING(tot-rm,">>>>>>>>>>>9") 
      cl-list.deposit   = tot-deposit 
      cl-list.cash      = tot-cash 
      cl-list.cc        = tot-cc 
      cl-list.cl        = tot-cl 
      cl-list.tot       = tot-amt. 
 
  /*OPEN QUERY q1 FOR EACH cl-list NO-LOCK. */
END. 





