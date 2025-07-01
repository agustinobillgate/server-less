
DEF INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER o-resnr AS INT.
DEF INPUT PARAMETER o-reslinnr AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER msg-strQ AS CHAR.
DEF OUTPUT PARAMETER recid-bk-reser AS INT.

{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "bqt-cutoff".   

DEFINE VARIABLE gname AS CHAR NO-UNDO.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = o-resnr 
  USE-INDEX vernr-ix NO-LOCK. 
IF NOT AVAILABLE bk-veran THEN RETURN. /*FT serverless*/

IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
   + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
   + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
   + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
   + bk-veran.deposit-payment[9]) GT 0 THEN 
DO: 
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
    AND bk-reser.veran-resnr NE o-reslinnr
    AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bk-reser THEN 
  DO: 
      msg-str = translateExtended ("Deposit exists, cancel reservation not possible.",lvCAREA,"").
      RETURN. 
  END. 
END. 

IF bk-veran.rechnr > 0 THEN 
DO: 
  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
    AND bk-reser.veran-resnr NE o-reslinnr 
    AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bk-reser THEN 
  DO: 
      msg-str = translateExtended ("Bill exists, cancel reservation not possible.",lvCAREA,"").
      RETURN.
  END. 
END. 

FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE guest THEN gname = guest.NAME.
FIND FIRST bk-reser WHERE bk-reser.veran-nr = o-resnr
  AND bk-reser.veran-seite = o-reslinnr NO-LOCK NO-ERROR. 

IF AVAILABLE bk-reser THEN /*FT serverless*/
DO:
    FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK. 
    IF AVAILABLE bk-raum THEN
        msg-strQ = "&Q" + translateExtended ("Do you really want to delete reservation of",lvCAREA,"")
            + CHR(10)
            + gname + " - " + translateExtended ("Room:",lvCAREA,"") + " " + bk-raum.bezeich
            + CHR(10)
            + translateExtended ("Date:",lvCAREA,"") + " " + STRING(bk-reser.datum) + " - " + STRING(bk-reser.bis-datum)
            + "  " + translateExtended ("Time:",lvCAREA,"") + " " + STRING(bk-reser.von-zeit,"99:99")
            + " - " + STRING(bk-reser.bis-zeit,"99:99") + "?".
    recid-bk-reser = RECID(bk-reser).
END.
    
