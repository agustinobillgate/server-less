DEFINE TEMP-TABLE temp 
    FIELD pos AS int 
    FIELD bezeich AS CHAR 
    FIELD artnr AS int. 

DEFINE TEMP-TABLE Rhbline 
  FIELD nr AS INTEGER 
  FIELD rid AS INTEGER. 


DEF INPUT PARAMETER TABLE FOR temp.
DEF INPUT PARAMETER TABLE FOR Rhbline.
DEF INPUT PARAMETER tableno      AS INTEGER. 
DEF INPUT PARAMETER bilrecid     AS INTEGER. 
DEF INPUT PARAMETER new-waiter   AS INTEGER. 
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER tischnr AS INT.
/*
MESSAGE 
    "tableno     = " tableno        skip
    "bilrecid    = " bilrecid       skip
    "new-waiter  = " new-waiter     skip
    "rec-id      = " rec-id         skip
    "curr-waiter = " curr-waiter    skip
    "dept        = " dept           skip
    "tischnr     = " tischnr    
    VIEW-AS ALERT-BOX INFO BUTTONS OK.

FOR EACH temp:
    MESSAGE 
        "pos     = " temp.pos       skip
        "bezeich = " temp.bezeich   skip
        "artnr   = " temp.artnr  
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
END.

FOR EACH Rhbline:
    MESSAGE 
        "nr  = " Rhbline.nr     SKIP
        "rid = " Rhbline.rid
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
END.
*/
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id NO-LOCK NO-ERROR.
RUN move-table.

PROCEDURE move-table: 
DEFINE VARIABLE i                   AS INTEGER. 
DEFINE VARIABLE billDate            AS DATE.

DEFINE VARIABLE f-discArt     AS INTEGER INITIAL -1 NO-UNDO. 
DEFINE VARIABLE b-discArt     AS INTEGER INITIAL -1 NO-UNDO. 
DEFINE VARIABLE b2-discArt    AS INTEGER INITIAL -1 NO-UNDO. 
DEFINE VARIABLE o-discArt     AS INTEGER INITIAL -1 NO-UNDO. 

DEFINE VARIABLE move-amt      AS DECIMAL INITIAL 0  NO-UNDO.

DEFINE BUFFER hbill FOR vhp.h-bill.

  FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. /*rest food disc artNo */ 
  IF vhp.htparam.finteger NE 0 THEN f-discArt = vhp.htparam.finteger.
  FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. /*rest bev disc artNo  */ 
  IF vhp.htparam.finteger NE 0 THEN b-discArt = vhp.htparam.finteger.
  FIND FIRST vhp.htparam WHERE paramnr = 1009 NO-LOCK. /*rest bev disc2 artNo*/ 
  IF vhp.htparam.finteger NE 0 THEN b2-discArt = vhp.htparam.finteger.
  FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. /*rest other disc artNo*/ 
  IF vhp.htparam.finteger NE 0 THEN o-discArt = vhp.htparam.finteger.


  IF new-waiter = 0 THEN new-waiter = curr-waiter. 
  IF bilrecid NE 0 THEN FIND FIRST hbill WHERE RECID(hbill) = bilrecid 
    EXCLUSIVE-LOCK. 
  ELSE 
  DO: 
    FIND FIRST vhp.counters WHERE vhp.counters.counter-no = (100 + dept) 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.counters THEN FIND CURRENT vhp.counters EXCLUSIVE-LOCK. 
    ELSE 
    DO: 
      FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = dept NO-LOCK. 
      CREATE vhp.counters. 
      vhp.counters.counter-no = 100 + dept. 
      vhp.counters.counter-bez = "Outlet Invoice: " + hoteldpt.depart. 
    END. 
    vhp.counters.counter = vhp.counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 
    CREATE hbill. 
    ASSIGN 
      hbill.tischnr =  tableno 
      hbill.departement = dept 
      hbill.kellner-nr = curr-waiter 
      hbill.rechnr = vhp.counters.counter 
      hbill.belegung = 1. 
/* 
    IF hoga-resnr GT 0 THEN 
    DO: 
      ASSIGN 
        hbill.resnr = hoga-resnr 
        hbill.reslinnr = hoga-reslinnr. 
      IF hogatex-flag THEN hbill.service[2] = hoga-host. 
    END. 
*/ 
    RELEASE vhp.counters.
  END. 
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
  vhp.h-bill.rgdruck = 0. 

  FOR EACH temp: 
    FIND FIRST Rhbline WHERE Rhbline.nr = temp.pos. 
    FIND FIRST vhp.h-bill-line WHERE RECID(vhp.h-bill-line) = Rhbline.rid 
      EXCLUSIVE-LOCK. 
    
    ASSIGN
      move-amt = move-amt + vhp.h-bill-line.betrag
      billDate = vhp.h-bill-line.bill-datum
    .

    IF vhp.h-bill-line.artnr = f-discArt THEN
    FOR EACH vhp.h-journal WHERE 
       vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum   AND
       vhp.h-journal.departement = vhp.h-bill-line.departement AND
       vhp.h-journal.rechnr = vhp.h-bill-line.rechnr           AND
      (vhp.h-journal.artnr = f-discArt  OR
       vhp.h-journal.artnr = b-discArt  OR
       vhp.h-journal.artnr = b2-discArt OR
       vhp.h-journal.artnr = o-discArt)                        AND
       vhp.h-journal.zeit = vhp.h-bill-line.zeit:
       ASSIGN
         vhp.h-journal.tischnr = tableno 
         vhp.h-journal.rechnr  = hbill.rechnr
       . 
    END.
    ELSE
    DO:
      FIND FIRST vhp.h-journal WHERE 
        vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum   AND
        vhp.h-journal.departement = vhp.h-bill-line.departement AND
        vhp.h-journal.rechnr = vhp.h-bill-line.rechnr           AND
        vhp.h-journal.artnr = vhp.h-bill-line.artnr             AND
         vhp.h-journal.zeit = vhp.h-bill-line.zeit EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE vhp.h-journal THEN
      DO:
        ASSIGN
          vhp.h-journal.tischnr = tableno 
          vhp.h-journal.rechnr  = hbill.rechnr
        .
        FIND CURRENT vhp.h-journal NO-LOCK.
      END.
    END.
/*
    CREATE vhp.h-journal. 
    ASSIGN 
      vhp.h-journal.rechnr = vhp.h-bill.rechnr 
      vhp.h-journal.artnr = vhp.h-bill-line.artnr 
      vhp.h-journal.anzahl = vhp.h-bill-line.anzahl 
      vhp.h-journal.epreis = vhp.h-bill-line.epreis 
      vhp.h-journal.bezeich = "To Table " + STRING(tableno) 
       + " *" + STRING(hbill.rechnr) 
      vhp .h-journal.tischnr = tischnr  /* table# TO be transferred */ 
      vhp.h-journal.departement = vhp.h-bill.departement 
      vhp.h-journal.zeit = time + add-zeit 
      vhp.h-journal.kellner-nr = curr-waiter 
      vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum 
      vhp.h-journal.artnrfront = 0 
      vhp.h-journal.aendertext = "" 
      vhp.h-journal.betrag = - vhp.h-bill-line.betrag. 
    FIND CURRENT vhp.h-journal NO-LOCK. 
 
    CREATE vhp.h-journal. 
    ASSIGN 
      vhp.h-journal.rechnr = hbill.rechnr 
      vhp.h-journal.artnr = vhp.h-bill-line.artnr 
      vhp.h-journal.anzahl = vhp.h-bill-line.anzahl 
      vhp.h-journal.epreis = vhp.h-bill-line.epreis 
      vhp.h-journal.bezeich = "From Table " + STRING(tischnr) 
        + " *" + STRING(vhp.h-bill.rechnr) 
      vhp.h-journal.tischnr =  tableno  /* Transfer TO this table# */ 
      vhp.h-journal.departement = vhp.h-bill.departement 
      vhp.h-journal.zeit = time + add-zeit
      vhp.h-journal.kellner-nr = new-waiter 
      vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum 
      vhp.h-journal.artnrfront = 0 
      vhp.h-journal.aendertext = "" 
      vhp.h-journal.betrag = vhp.h-bill-line.betrag. 
    FIND CURRENT vhp.h-journal NO-LOCK. 
*/
    ASSIGN 
      vhp.h-bill-line.waehrungsnr = 0 
      vhp.h-bill-line.tischnr = tableno 
      vhp.h-bill-line.rechnr = hbill.rechnr. 
    FIND CURRENT vhp.h-bill-line NO-LOCK. 
  
    vhp.h-bill.saldo =  vhp.h-bill.saldo - vhp.h-bill-line.betrag. 
    hbill.saldo = hbill.saldo + vhp.h-bill-line.betrag. 
  END. 

  CREATE vhp.h-journal. 
  ASSIGN 
    vhp.h-journal.rechnr        = vhp.h-bill.rechnr 
    vhp.h-journal.artnr         = 0 
    vhp.h-journal.anzahl        = 0 
    vhp.h-journal.epreis        = 0 
    vhp.h-journal.bezeich       = "To Table " + STRING(tableno) 
     + " *" + STRING(hbill.rechnr) 
    vhp .h-journal.tischnr      = tischnr  /* table# TO be transferred */ 
    vhp.h-journal.departement   = vhp.h-bill.departement 
    vhp.h-journal.zeit          = TIME 
    vhp.h-journal.kellner-nr    = curr-waiter 
    vhp.h-journal.bill-datum    = billDate 
    vhp.h-journal.artnrfront    = 0 
    vhp.h-journal.aendertext    = "" 
    vhp.h-journal.betrag        = - move-amt
  . 
  FIND CURRENT vhp.h-journal NO-LOCK. 

  CREATE vhp.h-journal. 
  ASSIGN 
    vhp.h-journal.rechnr        = hbill.rechnr 
    vhp.h-journal.artnr         = 0
    vhp.h-journal.anzahl        = 0 
    vhp.h-journal.epreis        = 0
    vhp.h-journal.bezeich       = "From Table " + STRING(tischnr) 
      + " *" + STRING(vhp.h-bill.rechnr) 
    vhp.h-journal.tischnr       =  tableno  /* Transfer TO this table# */ 
    vhp.h-journal.departement   = vhp.h-bill.departement 
    vhp.h-journal.zeit          = TIME
    vhp.h-journal.kellner-nr    = new-waiter 
    vhp.h-journal.bill-datum    = billDate 
    vhp.h-journal.artnrfront    = 0 
    vhp.h-journal.aendertext    = "" 
    vhp.h-journal.betrag        = move-amt
  .
  FIND CURRENT vhp.h-journal NO-LOCK. 

  FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
    AND vhp.queasy.number1 = dept
    AND vhp.queasy.number2 = tableno /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.queasy AND vhp.queasy.date1 = ? THEN
  DO:
    FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
    IF vhp.queasy.date1 = ? THEN
    ASSIGN vhp.queasy.number3 = TIME
           vhp.queasy.date1   = TODAY
    .
    FIND CURRENT vhp.queasy NO-LOCK.
    RELEASE queasy. /*FDL Feb 20, 2024 => Ticket E7D104*/
  END.

  FIND CURRENT hbill NO-LOCK. 
  FIND CURRENT vhp.h-bill NO-LOCK. 
  /*FDL Feb 20, 2024 => Ticket E7D104*/
  RELEASE hbill.
  RELEASE h-bill.

  FOR EACH temp: 
    DELETE temp. 
  END. 
  FOR EACH Rhbline: 
    DELETE Rhbline. 
  END.
  /*MT
  DO i = 1 TO num-field : 
    right-menu[i] = "". 
  END. 
  curr-Rapos = 1. 
  max-Rapos = 0. 
  balance = 0. 
  DISP right-menu balance WITH FRAME frame1.
  */
END. 
