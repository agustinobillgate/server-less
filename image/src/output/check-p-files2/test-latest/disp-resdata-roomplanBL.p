
DEF TEMP-TABLE buf-res-line
    FIELD gastnr        LIKE res-line.gastnr
    FIELD resnr         LIKE res-line.resnr
    FIELD reslinnr      LIKE res-line.reslinnr
    FIELD active-flag   LIKE res-line.active-flag
    FIELD zinr          LIKE res-line.zinr
    FIELD kurzbez       LIKE zimkateg.kurzbez
    FIELD resstatus     LIKE res-line.resstatus
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise
    FIELD betrieb-gast  LIKE res-line.betrieb-gast
    FIELD zipreis       LIKE res-line.zipreis
    FIELD was-status    LIKE res-line.was-status
    FIELD name          LIKE res-line.name
    FIELD ziwech-zeit   LIKE res-line.ziwech-zeit
    FIELD recid1        AS INT.

DEF TEMP-TABLE buf-reservation
    FIELD gastnr        LIKE reservation.gastnr
    FIELD resnr         LIKE reservation.resnr
    FIELD grpflag       LIKE reservation.grpflag.

DEF INPUT PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-date AS DATE.
DEF INPUT PARAMETER i AS INTEGER.
DEF INPUT PARAMETER zinr AS CHAR.
DEF INPUT PARAMETER gstatus AS INT.
DEF INPUT PARAMETER recid1 AS INT.
DEF OUTPUT PARAMETER n-edit AS CHAR.
DEF OUTPUT PARAMETER c-edit AS CHAR.
DEF OUTPUT PARAMETER fg-col AS INT.
DEF OUTPUT PARAMETER flag-res-line AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER flag-outorder AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER last-zinr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR buf-res-line.
DEF OUTPUT PARAMETER TABLE FOR buf-reservation.
/*DEF VAR pvILanguage AS INT INIT 0.
DEF VAR curr-date AS DATE INIT 01/30/10.
DEF VAR i AS INT INIT 1.
DEF VAR zinr AS CHAR INIT "1905".
DEF VAR gstatus AS INT INIT 2.
DEF VAR recid1 AS INT INIT 2175943.
DEF VAR n-edit AS CHAR.
DEF VAR c-edit AS CHAR.*/

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "disp-resdata-roomplan". 

RUN disp-res-data.

PROCEDURE disp-res-data:
  IF i = 0 THEN 
  DO:
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND 
      res-line.abreise = curr-date AND res-line.zinr = zinr 
      AND res-line.resstatus NE 12 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
      n-edit = "ResNo: " + STRING(res-line.resnr) + "   " 
           + translateExtended ("Room:",lvCAREA,"") + " " + res-line.zinr + chr(10) 
           + translateExtended ("Guest:",lvCAREA,"") + " " + res-line.name + chr(10) 
           + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(res-line.ankunft) + chr(10) 
           + translateExtended ("Depart:",lvCAREA,"") + " " + STRING(res-line.abreise) + chr(10) 
           + translateExtended ("RmRate:",lvCAREA,"") + " " + STRING(res-line.zipreis). 
      IF res-line.betriebsnr GT 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN n-edit = n-edit + " " + waehrung.wabkurz. 
      END. 
      c-edit = translateExtended ("Reservation Comment:",lvCAREA,"") + chr(10) 
           + reservation.bemerk + chr(10) 
           + res-line.bemerk.
      fg-col = 0.
    END. 
    ELSE 
    DO: 
      n-edit = "". 
      c-edit = "". 
    END.
  END. 
  ELSE IF gstatus = 9 THEN 
  DO: 
    FIND FIRST outorder WHERE RECID(outorder) = recid1 NO-LOCK NO-ERROR. 
    n-edit = "". 
    c-edit = translateExtended ("Out-of-order Reason:",lvCAREA,"") + chr(10).
    IF AVAILABLE outorder THEN c-edit = c-edit + outorder.gespgrund.
    fg-col = 12.
    release res-line. 
  END. 
  ELSE IF gstatus = 12 THEN 
  DO: 
    FIND FIRST outorder WHERE RECID(outorder) = recid1 NO-LOCK NO-ERROR. 
    n-edit = "". 
    c-edit = translateExtended ("Out-of-Service Reason:",lvCAREA,"") + chr(10). 
    IF AVAILABLE outorder THEN c-edit = c-edit + outorder.gespgrund.
    fg-col = 12.
    release res-line. 
  END. 
  ELSE IF gstatus = 10 THEN 
  DO: 
  DEFINE buffer resline FOR res-line. 
    FIND FIRST outorder WHERE RECID(outorder) = recid1 NO-LOCK
        NO-ERROR.
    IF AVAILABLE outorder THEN
    DO:
      FIND FIRST resline WHERE resline.resnr = outorder.betriebsnr 
        AND resline.zinr = outorder.zinr AND resline.resstatus = 1 
        NO-LOCK NO-ERROR. 

      n-edit = "". 
      c-edit = translateExtended ("Off-Market Reason:",lvCAREA,"") + chr(10) 
             + outorder.gespgrund + chr(10). 
      IF AVAILABLE resline THEN 
      DO: 
        c-edit = c-edit + translateExtended ("ResNo:",lvCAREA,"") + " " + STRING(resline.resnr) + chr(10) 
                      + translateExtended ("Guest:",lvCAREA,"") + " " + resline.name + chr(10) 
                      + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(resline.ankunft) + chr(10) 
                      + translateExtended ("Departure:",lvCAREA,"") + " " + STRING(resline.abreise). 
      END.
      fg-col = 4.
      RELEASE res-line.
    END.
  END. 
  ELSE IF recid1 NE 0 THEN 
  DO: 
    FIND FIRST res-line WHERE RECID(res-line) = recid1 NO-LOCK. 
    IF NOT AVAILABLE res-line THEN                                /* Rulita 041124 | Fixing For Serverless */
    DO:
        RETURN.
    END.
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
    n-edit = translateExtended ("ResNo:",lvCAREA,"") + " " + STRING(res-line.resnr) + "   " 
           + translateExtended ("Room:",lvCAREA,"") + " " + res-line.zinr + chr(10) 
           + translateExtended ("Guest:",lvCAREA,"") + " " + res-line.name + chr(10) 
           + translateExtended ("Arrival:",lvCAREA,"") + " " + STRING(res-line.ankunft) + chr(10) 
           + translateExtended ("Depart:",lvCAREA,"") + " " + STRING(res-line.abreise) + chr(10) 
           + translateExtended ("RmRate:",lvCAREA,"") + " " + STRING(res-line.zipreis). 
    IF res-line.betriebsnr GT 0 THEN 
    DO: 
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN n-edit = n-edit + " " + waehrung.wabkurz. 
    END. 
    c-edit = translateExtended ("Reservation Comment:",lvCAREA,"") + chr(10) 
           + reservation.bemerk + chr(10) 
           + res-line.bemerk. 
    IF gstatus = 1 THEN fg-col = 2.
    ELSE IF gstatus EQ 2 THEN fg-col = 1.
    ELSE IF gstatus EQ 3 THEN fg-col = 9.
  END. 

  IF AVAILABLE res-line THEN
  DO:
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr
          NO-LOCK.
      CREATE buf-res-line.
      ASSIGN
        buf-res-line.gastnr        = res-line.gastnr
        buf-res-line.resnr         = res-line.resnr
        buf-res-line.reslinnr      = res-line.reslinnr
        buf-res-line.active-flag   = res-line.active-flag
        buf-res-line.zinr          = res-line.zinr
        buf-res-line.kurzbez       = zimkateg.kurzbez
        buf-res-line.resstatus     = res-line.resstatus
        buf-res-line.ankunft       = res-line.ankunft
        buf-res-line.abreise       = res-line.abreise
        buf-res-line.betrieb-gast  = res-line.betrieb-gast
        buf-res-line.zipreis       = res-line.zipreis
        buf-res-line.was-status    = res-line.was-status
        buf-res-line.name          = res-line.name
        buf-res-line.ziwech-zeit   = res-line.ziwech-zeit
        buf-res-line.recid1        = RECID(res-line).
      flag-res-line = YES.
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
          NO-LOCK NO-ERROR.
      IF AVAILABLE reservation THEN
      DO:
          CREATE buf-reservation.
          ASSIGN
            buf-reservation.gastnr   = reservation.gastnr
            buf-reservation.resnr    = reservation.resnr
            buf-reservation.grpflag  = reservation.grpflag.
      END.
      IF res-line.active-flag = 0 THEN
      DO:
        FIND FIRST outorder WHERE outorder.zinr = res-line.zinr 
          AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN flag-outorder = YES.
      END.

      last-zinr = res-line.zinr.
  END.
END.
