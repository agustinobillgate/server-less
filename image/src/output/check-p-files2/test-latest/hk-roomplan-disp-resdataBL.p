DEF TEMP-TABLE t-res-line
    FIELD rec-id      AS INTEGER
    FIELD ziwech-zeit LIKE res-line.ziwech-zeit.

DEF INPUT PARAMETER i AS INTEGER.
DEF INPUT PARAMETER curr-date AS DATE.
DEF INPUT PARAMETER zinr AS CHAR.
DEF INPUT PARAMETER gstatus AS INTEGER.
DEF INPUT PARAMETER recid1 AS INTEGER.
DEF OUTPUT PARAMETER n-edit AS CHAR.
DEF OUTPUT PARAMETER c-edit AS CHAR.
DEF OUTPUT PARAMETER fgcol-n AS INT.
DEF OUTPUT PARAMETER fgcol-c AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.

IF i = 0 THEN 
DO: 
    FIND FIRST res-line WHERE res-line.active-flag LE 1 AND 
      res-line.abreise = curr-date AND res-line.zinr = /*MTroom-list.*/ zinr 
      AND res-line.resstatus NE 12 NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
      n-edit = "ResNo: " + STRING(res-line.resnr) + "   " 
           + "Room: " + res-line.zinr + chr(10) 
           + "Guest: " + res-line.name + chr(10) 
           + "Arrival: " + STRING(res-line.ankunft) + chr(10) 
           + "Depart: " + STRING(res-line.abreise). 
      c-edit = "Reservation Comment:" + chr(10) 
           + reservation.bemerk + chr(10) 
           + res-line.bemerk.
      fgcol-n = 0.
      fgcol-c = 0.
      /*MTASSIGN n-edit:FGCOLOR IN FRAME frame1 = 0. 
      ASSIGN c-edit:FGCOLOR IN FRAME frame1 = 0. */
    END. 
    ELSE 
    DO: 
      n-edit = "". 
      c-edit = "". 
    END. 
END. 
ELSE IF /*MTroom-list.gstatus[i]*/ gstatus = 9 THEN 
DO: 
    FIND FIRST outorder WHERE RECID(outorder) = /*MTroom-list.recid1[i]*/ recid1 NO-LOCK. 
    n-edit = "". 
    c-edit = "Out-of-order Reason:" + chr(10) 
             + outorder.gespgrund.
    fgcol-c = 12.
    /*MTASSIGN c-edit:FGCOLOR IN FRAME frame1 = 12. */
    release res-line. 
  END. 
  ELSE IF /*room-list.gstatus[i]*/ gstatus = 10 THEN 
  DO: 
  DEFINE buffer resline FOR res-line. 
    FIND FIRST outorder WHERE RECID(outorder) = /*room-list.recid1[i]*/ recid1 NO-LOCK. 
    FIND FIRST resline WHERE resline.resnr = outorder.betriebsnr 
      AND resline.zinr = outorder.zinr AND resline.resstatus = 1 
      NO-LOCK NO-ERROR. 
    n-edit = "". 
    c-edit = "Off-Market Reason:" + chr(10) 
             + outorder.gespgrund + chr(10). 
    IF AVAILABLE resline THEN 
    DO: 
      c-edit = c-edit + "ResNo: " + STRING(resline.resnr) + chr(10) 
                      + "Guest: " + resline.name + chr(10) 
                      + "Arrival: " + STRING(resline.ankunft) + chr(10) 
                      + "Departure: " + STRING(resline.abreise). 
    END.
    fgcol-c = 4.
    /*MTASSIGN c-edit:FGCOLOR IN FRAME frame1 = 4. */
    release res-line. 
END. 
ELSE IF /*MTroom-list.recid1[i]*/ recid1 NE 0 THEN 
DO: 
    FIND FIRST res-line WHERE RECID(res-line) = /*MTroom-list.recid1[i]*/ recid1 NO-LOCK. 
    FIND FIRST reservation WHERE reservation.gastnr = res-line.gastnr 
      AND reservation.resnr = res-line.resnr NO-LOCK. 
    n-edit = "ResNo: " + STRING(res-line.resnr) + "   " 
           + "Room: " + res-line.zinr + chr(10) 
           + "Guest: " + res-line.name + chr(10) 
           + "Arrival: " + STRING(res-line.ankunft) + chr(10) 
           + "Depart: " + STRING(res-line.abreise). 
    c-edit = "Reservation Comment:" + chr(10) 
           + reservation.bemerk + chr(10) 
           + res-line.bemerk. 
    IF /*MTroom-list.gstatus[i]*/ gstatus = 1 THEN 
    DO:
        fgcol-n = 2.
        fgcol-c = 2.
      /*MTASSIGN n-edit:FGCOLOR IN FRAME frame1 = 2. 
      ASSIGN c-edit:FGCOLOR IN FRAME frame1 = 2. */
    END. 
    ELSE IF /*MTroom-list.gstatus[i]*/ gstatus EQ 2 THEN 
    DO: 
        fgcol-n = 1.
        fgcol-c = 1.
      /*MTASSIGN n-edit:FGCOLOR IN FRAME frame1 = 1. 
      ASSIGN c-edit:FGCOLOR IN FRAME frame1 = 1. */
    END. 
    ELSE IF /*MTroom-list.gstatus[i]*/ gstatus EQ 3 THEN 
    DO: 
        fgcol-n = 9.
        fgcol-c = 9.
      /*MTASSIGN n-edit:FGCOLOR IN FRAME frame1 = 9. 
      ASSIGN c-edit:FGCOLOR IN FRAME frame1 = 9. */
    END. 
END. 
ELSE release res-line. 

IF AVAILABLE res-line THEN
DO:
    CREATE t-res-line.
    ASSIGN 
        t-res-line.rec-id      = RECID(res-line)
        t-res-line.ziwech-zeit = res-line.ziwech-zeit.
END.
