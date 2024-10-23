
DEF INPUT  PARAMETER r-recid  AS INT.
DEF INPUT  PARAMETER sorttype AS INT.
DEF OUTPUT PARAMETER its-ok   AS LOGICAL INITIAL YES.

DEFINE buffer resline FOR bk-reser. 

FIND FIRST bk-reser WHERE RECID(bk-reser) = r-recid NO-LOCK NO-ERROR. 
FIND FIRST resline WHERE resline.datum = bk-reser.datum 
    AND resline.raum = bk-reser.raum AND 
    ((resline.von-i GE bk-reser.von-i AND resline.von-i LE bk-reser.bis-i) OR 
     (resline.bis-i GE bk-reser.von-i AND resline.bis-i LE bk-reser.bis-i) OR 
     (bk-reser.von-i GE resline.von-i AND bk-reser.bis-i LE resline.bis-i)) 
    AND (ROWID(resline) NE ROWID(bk-reser)) 
    AND resline.resstatus = sorttype NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN 
DO: 
    IF resline.resstatus = 1 THEN 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Room already blocked (fix).",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. 
      */
      its-ok = NO.
      RETURN. 
    END. 
    IF resline.resstatus = 2 THEN 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Room already blocked (tentative).",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. 
      */
      its-ok = NO. 
      RETURN. 
    END. 
END. 
