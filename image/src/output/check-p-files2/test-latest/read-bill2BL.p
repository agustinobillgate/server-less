
/*FDL Dec 24, 2024: 5A4D76 - Could not update field 'vesrdepot' of target in a BUFFER-COPY statement*/
DEF TEMP-TABLE t-bill
    FIELD zinr              LIKE bill.zinr             
    FIELD flag              LIKE bill.flag             
    FIELD rechnr            LIKE bill.rechnr           
    FIELD resnr             LIKE bill.resnr            
    FIELD gastnr            LIKE bill.gastnr           
    FIELD saldo             LIKE bill.saldo            
    FIELD gesamtumsatz      LIKE bill.gesamtumsatz     
    FIELD logisumsatz       LIKE bill.logisumsatz      
    FIELD arrangemdat       LIKE bill.arrangemdat      
    FIELD rgdruck           LIKE bill.rgdruck          
    FIELD logiernachte      LIKE bill.logiernachte     
    FIELD reslinnr          LIKE bill.reslinnr         
    FIELD argtumsatz        LIKE bill.argtumsatz       
    FIELD f-b-umsatz        LIKE bill.f-b-umsatz       
    FIELD sonst-umsatz      LIKE bill.sonst-umsatz     
    FIELD billnr            LIKE bill.billnr           
    FIELD firstper          LIKE bill.firstper         
    FIELD billkur           LIKE bill.billkur          
    FIELD logidat           LIKE bill.logidat          
    FIELD bilname           LIKE bill.bilname          
    FIELD teleinheit        LIKE bill.teleinheit       
    FIELD telsumme          LIKE bill.telsumme         
    FIELD segmentcode       LIKE bill.segmentcode      
    FIELD printnr           LIKE bill.printnr          
    FIELD billbankett       LIKE bill.billbankett      
    FIELD service           LIKE bill.service          
    FIELD mwst              LIKE bill.mwst             
    FIELD umleit-zinr       LIKE bill.umleit-zinr      
    FIELD billmaster        LIKE bill.billmaster       
    FIELD datum             LIKE bill.datum            
    FIELD taxsumme          LIKE bill.taxsumme         
    FIELD name              LIKE bill.name             
    FIELD billtyp           LIKE bill.billtyp          
    FIELD parent-nr         LIKE bill.parent-nr        
    FIELD restargt          LIKE bill.restargt         
    FIELD init-argt         LIKE bill.init-argt        
    FIELD rest-tage         LIKE bill.rest-tage        
    FIELD ums-kurz          LIKE bill.ums-kurz         
    FIELD ums-lang          LIKE bill.ums-lang         
    FIELD nextargt-bookdate LIKE bill.nextargt-bookdate
    FIELD roomcharge        LIKE bill.roomcharge       
    FIELD oldzinr           LIKE bill.oldzinr          
    FIELD t-rechnr          LIKE bill.t-rechnr         
    FIELD rechnr2           LIKE bill.rechnr2          
    FIELD betriebsnr        LIKE bill.betriebsnr       
    FIELD vesrdep           LIKE bill.vesrdep          
    FIELD vesrdat           LIKE bill.vesrdat          
    FIELD vesrdepot         AS CHARACTER
    FIELD vesrdepot2        AS CHARACTER
    FIELD vesrcod           AS CHARACTER
    FIELD verstat           LIKE bill.verstat     
    FIELD kontakt-nr        LIKE bill.kontakt-nr  
    FIELD betrieb-gast      LIKE bill.betrieb-gast
    FIELD billref           LIKE bill.billref     
    FIELD bl-recid          AS INTEGER    
    .

DEF INPUT  PARAMETER case-type      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER billNo         AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resNo          AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinNo       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER actFlag        AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER roomNo         AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER datum1         AS DATE    NO-UNDO.
DEF INPUT  PARAMETER datum2         AS DATE    NO-UNDO.
DEF INPUT  PARAMETER saldo1         AS DECIMAL NO-UNDO.
DEF INPUT  PARAMETER saldo2         AS DECIMAL NO-UNDO.

DEF OUTPUT PARAMETER telbill-flag   AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER babill-flag    AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-bill.

DEF VAR ba-dept   AS INTEGER NO-UNDO.
DEF VAR bill-date AS DATE    NO-UNDO.

/*ITA 130616*/
DEF VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEFINE BUFFER tbuff FOR bill.


RUN htpdate.p(110, OUTPUT bill-date).
RUN htpint.p(900, OUTPUT ba-dept).
IF ba-dept = 0 THEN ba-dept = -1.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST bill WHERE bill.rechnr = billNo NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 2 THEN
  DO:
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo
          AND bill.parent-nr NE 0 AND bill.flag = actFlag 
          AND bill.zinr = roomNo NO-LOCK: 
          RUN cr-bill.
      END.
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo 
          AND bill.parent-nr = reslinNo AND bill.billnr = billNo 
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 4 THEN
  DO:
      FOR EACH bill WHERE bill.resnr = resNo AND bill.parent-nr = reslinNo
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK: 
          RUN cr-bill.
      END.
  END.
  WHEN 5 THEN
  DO:
      FIND FIRST bill WHERE RECID(bill) = billNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN RUN cr-bill.
  END.                                   
  WHEN 6 THEN 
  DO:
    FIND FIRST bill WHERE bill.flag = actFlag AND bill.datum GE datum1
        AND bill.datum LE datum2 AND bill.saldo NE 0
        USE-INDEX flagdat_ix NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 7 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag
          AND (bill.saldo GE saldo1 OR bill.saldo LE - saldo2) NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 8 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag AND bill.vesrdepot = roomNo 
          AND bill.billtyp = billNo USE-INDEX vesr2_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST bill WHERE bill.flag = actFlag 
          AND bill.rechnr = reslinNo
          AND bill.resnr = resNo
          AND bill.reslinnr = 1
          AND bill.billtyp = billNo
          USE-INDEX vesr2_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 10 THEN
  DO:
      FOR EACH bill WHERE bill.zinr = roomNo
          AND bill.flag = actFlag NO-LOCK,
          FIRST res-line WHERE res-line.resnr = bill.resnr
          AND res-line.reslinnr = bill.reslinnr NO-LOCK:
          RUN cr-bill.
      END.
  END.
  WHEN 11 THEN
  DO:
      FOR EACH bill WHERE bill.zinr = roomNo
          AND bill.flag = actFlag NO-LOCK:
          RUN cr-bill.
      END.
  END.
  WHEN 12 THEN
  DO:
      FIND FIRST bill WHERE bill.resnr = resNo 
          AND bill.parent-nr = reslinNo 
          AND bill.parent-nr NE 0 AND bill.billnr = billNo 
          AND bill.flag = actFlag AND bill.zinr = roomNo NO-LOCK. 
      IF AVAILABLE bill THEN RUN cr-bill.
  END.
  WHEN 13 THEN /*FD Test for cashless with card for NS*/
  DO:
      FIND FIRST bill WHERE bill.gastnr EQ resNo
          AND bill.flag EQ actFlag 
          AND bill.vesrdepot2 EQ roomNo NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN RUN cr-bill.
  END.

END CASE.

PROCEDURE cr-bill:
    ASSIGN bl-saldo = 0.
    FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK:
          ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
    END.

    IF bl-saldo NE bill.saldo THEN DO:
        FIND FIRST tbuff WHERE RECID(tbuff) = RECID(bill) EXCLUSIVE-LOCK.
        tbuff.saldo = bl-saldo.
        FIND CURRENT tbuff NO-LOCK.
        RELEASE tbuff.
    END.

    CREATE t-bill.
    BUFFER-COPY bill EXCEPT bill.vesrdepot TO t-bill.
    t-bill.vesrdepot = bill.vesrdepot. /*FDL Dec 24, 2024: 5A4D76 - Could not update field 'vesrdepot' of target in a BUFFER-COPY statement*/
    t-bill.bl-recid = RECID(bill).
    IF bill.rechnr GT 0 THEN 
    DO: 
      FIND FIRST nebenst WHERE nebenst.zinr = "" 
        AND nebenst.rechnr = bill.rechnr NO-LOCK NO-ERROR. 
      telbill-flag = AVAILABLE nebenst.
      IF ba-dept GT 0 AND bill.billtyp = ba-dept THEN
        RUN check-banquet.
    END. 
END.

PROCEDURE check-banquet: 

  FIND FIRST bk-veran WHERE bk-veran.rechnr = bill.rechnr NO-LOCK NO-ERROR. 
  IF AVAILABLE bk-veran AND bk-veran.activeflag = 0 THEN 
  DO: 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
      AND bk-reser.datum GT bill-date 
      AND bk-reser.resstatus LE 3 NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN 
    DO: 
      babill-flag = YES. 
      RETURN. 
    END. 
 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
      AND bk-reser.datum = bill-date AND bk-reser.resstatus = 1 
      AND (bk-reser.bis-i * 1800) GT TIME NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN 
    DO: 
      babill-flag = YES. 
      RETURN. 
    END. 
  END. 
END. 

