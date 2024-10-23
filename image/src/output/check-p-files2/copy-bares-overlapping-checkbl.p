
DEF INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER resnr AS INT.
DEF INPUT  PARAMETER reslinnr AS INT.
DEF INPUT  PARAMETER datum AS DATE.
DEF INPUT  PARAMETER von-i AS INT.
DEF INPUT  PARAMETER bis-i AS INT.
DEF OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "copy-bares".

DEF BUFFER resline FOR bk-reser. 
FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
    AND bk-reser.veran-resnr = reslinnr NO-LOCK. 

FIND FIRST resline WHERE resline.datum = datum 
    AND resline.raum = bk-reser.raum AND 
    ((resline.von-i GE von-i AND resline.von-i LE bis-i) OR 
     (resline.bis-i GE von-i AND resline.bis-i LE bis-i) OR 
     (von-i GE resline.von-i AND bis-i LE resline.bis-i)) 
    AND resline.resstatus = bk-reser.resstatus NO-LOCK NO-ERROR. 
IF NOT AVAILABLE resline THEN RETURN. 
its-ok = NO. 
msg-str = "&W" + translateExtended ("Room already blocked for",lvCAREA,"") + " " + STRING(datum) 
        + CHR(10) + translateExtended ("Starting:",lvCAREA,"") + " " + STRING(resline.von-zeit,"99:99") 
        + " " + translateExtended ("Ending:",lvCAREA,"") + " " + STRING(resline.bis-zeit,"99:99") 
        + CHR(10)
        + translateExtended ("Status set to Waiting List",lvCAREA,"").
