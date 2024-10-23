DEF TEMP-TABLE t-h-artikel LIKE h-artikel  
    FIELD rec-id AS INT.  
  
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER rec-id         AS INT.  
DEF INPUT  PARAMETER guestnr        AS INT.  
DEF INPUT  PARAMETER curr-dept      AS INT.  
DEF INPUT  PARAMETER paid           AS DECIMAL.  
DEF INPUT  PARAMETER exchg-rate     AS DECIMAL.  
DEF INPUT  PARAMETER price-decimal  AS INT.  
DEF INPUT  PARAMETER balance        AS DECIMAL.  
DEF INPUT  PARAMETER transdate      AS DATE.  
DEF INPUT  PARAMETER disc-art1      AS INT.  
DEF INPUT  PARAMETER disc-art2      AS INT.  
DEF INPUT  PARAMETER disc-art3      AS INT.  
DEF INPUT  PARAMETER kellner-kellner-nr AS INT.  
  
DEF OUTPUT PARAMETER billart        AS INT.  
DEF OUTPUT PARAMETER qty            AS INT.  
DEF OUTPUT PARAMETER description    AS CHAR.  
DEF OUTPUT PARAMETER price          AS DECIMAL.  
DEF OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.  
DEF OUTPUT PARAMETER amount         LIKE vhp.bill-line.betrag.  
DEF OUTPUT PARAMETER bill-date      AS DATE.  
DEF OUTPUT PARAMETER fl-code        AS INT INIT 0.  
DEF OUTPUT PARAMETER fl-code1       AS INT INIT 0.  
DEF OUTPUT PARAMETER msg-str        AS CHAR.  
DEF OUTPUT PARAMETER var-testing    AS CHAR INIT "".  
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.  
  
DEFINE BUFFER bill-guest FOR vhp.guest.   
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.  
  RUN check-rpaymentbl.p (pvILanguage, guestnr, curr-dept, OUTPUT billart,  
                          OUTPUT msg-str).  
  IF billart GT 0 THEN   
  DO:  
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept   
      AND vhp.h-artikel.artnrfront = billart   
      AND vhp.h-artikel.artart = 2 NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.h-artikel THEN   
    DO:   
      FIND FIRST bill-guest WHERE bill-guest.gastnr = guestnr NO-LOCK.   
      ASSIGN  
        billart = vhp.h-artikel.artnr  
        qty = 1  
        description = vhp.h-artikel.bezeich   
        price = 0  
        amount-foreign = ROUND(paid / exchg-rate, 2).   
        amount = paid  
      .   
        
      IF vhp.h-bill.resnr = 0 THEN  
      DO:  
          FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.  
          ASSIGN vhp.h-bill.resnr    = bill-guest.gastnr  
                 vhp.h-bill.reslinnr = 0  
                 vhp.h-bill.bilname  = bill-guest.NAME + ", " + bill-guest.vorname1
                                    + " " + bill-guest.anrede1
          .  
          FIND CURRENT vhp.h-bill NO-LOCK.  
      END.  
        
      IF price-decimal = 0 AND (balance + paid) GE -1   
          AND (balance + paid) LE 1 THEN RUN fill-cover.   
      ELSE IF price-decimal = 2 AND (balance + paid) GE -0.01  
          AND (balance + paid) LE 0.01 THEN RUN fill-cover.  
      fl-code = 1.  
      /*MTRUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront).   
      DISP balance WITH FRAME frame1.   
      IF double-currency THEN DISP balance-foreign WITH FRAME frame1. */  
    /* PAUSE 1. */   
    END.   
    ELSE DO:   
      fl-code = 2.  
    END.   
  END.   
  ELSE /*MTAPPLY "entry" TO billart IN FRAME frame1.*/ fl-code = 3.  
  
IF AVAILABLE h-artikel THEN  
DO:  
    CREATE t-h-artikel.  
    BUFFER-COPY h-artikel TO t-h-artikel.  
    ASSIGN t-h-artikel.rec-id = RECID(h-artikel).  
END.  
  
  
PROCEDURE fill-cover:   
  DEF VAR f-pax  AS INTEGER INITIAL 0   NO-UNDO.   
  DEF VAR b-pax  AS INTEGER INITIAL 0   NO-UNDO.  
    
  DEF BUFFER h-art1 FOR vhp.h-artikel.   
  DEF BUFFER tbuff  FOR vhp.tisch.  
  
  DO TRANSACTION:   
      
    FIND FIRST tbuff WHERE tbuff.tischnr = vhp.h-bill.tischnr   
        AND tbuff.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.  
    IF AVAILABLE tbuff AND tbuff.roomcharge AND tbuff.kellner-nr NE 0 THEN  
    DO:  
        FIND CURRENT tbuff EXCLUSIVE-LOCK.  
        ASSIGN tbuff.kellner-nr = 0.  
        FIND CURRENT tbuff NO-LOCK.  
    END.  
    RUN release-TBplan.  
  
    IF vhp.h-bill.resnr GT 0 THEN   
    RUN rest-addgastinfo.p(vhp.h-bill.departement, vhp.h-bill.rechnr,  
      vhp.h-bill.resnr, vhp.h-bill.reslinnr, 0, transdate).  
  
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
    ASSIGN vhp.h-bill.kellner-nr = kellner-kellner-nr NO-ERROR.  
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 739 NO-LOCK.  
    IF vhp.htparam.flogical THEN   
    DO:  
      fl-code1 = 1.  
      /*MTRUN TS-voucherUI.p(OUTPUT str).  
      IF str NE "" THEN ASSIGN vhp.h-bill.service[5] = DECIMAL(str).*/  
    END.  
    FIND CURRENT vhp.h-bill NO-LOCK.  
  
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.   
    /* vhp.bill DATE */   
    bill-date = vhp.htparam.fdate.   
    IF transdate NE ? THEN bill-date = transdate.   
    ELSE   
    DO:   
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */   
      IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1.   
    END.   
   
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = 0   
      AND vhp.h-umsatz.departement = curr-dept AND   
      vhp.h-umsatz.betriebsnr = curr-dept   
      AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.   
    IF NOT AVAILABLE vhp.h-umsatz THEN   
    DO:   
      create vhp.h-umsatz.   
      vhp.h-umsatz.artnr = 0.   
      vhp.h-umsatz.departement = curr-dept.   
      vhp.h-umsatz.betriebsnr = curr-dept.   
      vhp.h-umsatz.datum = bill-date.   
    END.   
    vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + vhp.h-bill.belegung.   
   
    IF vhp.h-bill.belegung NE 0 THEN   
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr   
        AND vhp.h-bill-line.departement = vhp.h-bill.departement   
        AND vhp.h-bill-line.artnr NE disc-art1   
        AND vhp.h-bill-line.artnr NE disc-art2   
        AND vhp.h-bill-line.artnr NE disc-art3 NO-LOCK,   
        FIRST h-art1 WHERE h-art1.artnr = vhp.h-bill-line.artnr   
        AND h-art1.departement = vhp.h-bill-line.departement   
        AND h-art1.artart = 0 NO-LOCK,   
        FIRST vhp.artikel WHERE vhp.artikel.artnr = h-art1.artnrfront   
        AND vhp.artikel.departement = h-art1.departement NO-LOCK:   
        IF vhp.artikel.umsatzart = 3 OR vhp.artikel.umsatzart = 5 THEN   
            f-pax = f-pax + h-bill-line.anzahl.   
        ELSE IF vhp.artikel.umsatzart = 6 THEN   
            b-pax = b-pax + h-bill-line.anzahl.   
    END.   
   
    IF vhp.h-bill.belegung > 0 THEN   
    DO:   
        IF f-pax > vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung.   
        IF b-pax > vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung.   
    END.   
    ELSE IF vhp.h-bill.belegung < 0 THEN   
    DO:   
        IF f-pax < vhp.h-bill.belegung THEN f-pax = vhp.h-bill.belegung.   
        IF b-pax < vhp.h-bill.belegung THEN b-pax = vhp.h-bill.belegung.   
    END.   
    vhp.h-umsatz.betrag = vhp.h-umsatz.betrag + f-pax.   
    vhp.h-umsatz.nettobetrag = vhp.h-umsatz.nettobetrag + b-pax.   
   
    FIND CURRENT vhp.h-umsatz NO-LOCK.   
    RELEASE vhp.h-umsatz.   
  END.   
END.   
  
  
  
PROCEDURE release-TBplan:  
    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31   
      AND vhp.queasy.number1 = vhp.h-bill.departement  
      AND vhp.queasy.number2 = vhp.h-bill.tischnr NO-LOCK NO-ERROR.  
    IF AVAILABLE vhp.queasy THEN  
    DO TRANSACTION:  
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.  
      ASSIGN vhp.queasy.number3 = 0  
             vhp.queasy.date1 = ?.  
      FIND CURRENT vhp.queasy NO-LOCK.  
      RELEASE vhp.queasy.  
    END.  
END.  
