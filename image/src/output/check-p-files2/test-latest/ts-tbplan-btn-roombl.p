DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resrecid AS INT.

DEF OUTPUT PARAMETER resnr1 AS INT.
DEF OUTPUT PARAMETER reslinnr1 AS INT.
DEF OUTPUT PARAMETER room AS CHAR.
DEF OUTPUT PARAMETER gname AS CHAR.
DEF OUTPUT PARAMETER remark   AS CHAR.
DEF OUTPUT PARAMETER klimit   AS DECIMAL.
DEF OUTPUT PARAMETER ksaldo   AS DECIMAL.
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER resline AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER hoga-resnr AS INT.
DEF OUTPUT PARAMETER hoga-reslinnr AS INT.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-tbplan".

/*FD August 05, 2021 => Req Amaranta*/
DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE str AS CHARACTER NO-UNDO.
DEFINE VARIABLE child-age AS CHARACTER NO-UNDO.

FIND FIRST vhp.res-line WHERE RECID(res-line) = resrecid NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.res-line THEN 
DO:
  resline = YES.
  RUN check-creditlimit. 
  resnr1 = vhp.res-line.resnr. 
  reslinnr1 = vhp.res-line.reslinnr. 
  
  hoga-resnr = vhp.res-line.resnr. 
  hoga-reslinnr = vhp.res-line.reslinnr. 
  /*MT*/
  room = vhp.res-line.zinr. 
  gname = vhp.res-line.name. 
  /*MTcurr-room = room. 
  curr-gname = gname. 
  DISP room gname remark WITH FRAME frame1. 
  ENABLE tischnr pax room gname WITH FRAME frame1. */
  IF vhp.res-line.code NE "" THEN 
  DO: 
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 
      AND vhp.queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
    DO: 
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("CASH BASIS Billing Instruction: ",lvCAREA,"") + vhp.queasy.char1.
    END. 
  END. 
  /*MTAPPLY "entry" TO gname. */
  RETURN NO-APPLY. 
END.



PROCEDURE check-creditlimit:
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
  FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST vhp.guest WHERE vhp.guest.gastnr 
    = vhp.res-line.gastnrpay NO-LOCK. 

  FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = vhp.guest.gastnr
      AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.mc-guest THEN
  ASSIGN remark = translateExtended ("Membership No:",lvCAREA,"") 
      + " " + vhp.mc-guest.cardnum + CHR(10).

  IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
  ELSE 
  DO: 
    IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
    ELSE klimit = vhp.htparam.finteger. 
  END. 
  
  ksaldo = 0. 
  FIND FIRST vhp.bill WHERE vhp.bill.resnr = vhp.res-line.resnr 
    AND vhp.bill.reslinnr = vhp.res-line.reslinnr AND vhp.bill.flag = 0 
    AND vhp.bill.zinr = vhp.res-line.zinr NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.bill THEN ksaldo = vhp.bill.saldo. 

  /*FD August 05, 2021 => Req Amaranta*/
  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    str = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(str,1,5) = "ChAge" THEN child-age = SUBSTR(str,6).
  END.

  /*
  remark = remark + STRING(vhp.res-line.ankunft) + " - " 
    + STRING(vhp.res-line.abreise) + CHR(10) 
    + "A " + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
    + "  Ch " + STRING(vhp.res-line.kind1) 
    + " - " + vhp.res-line.arrangement + CHR(10) 
    + vhp.res-line.bemerk. 
  */

  IF child-age NE "" THEN
  DO:
    remark = remark + STRING(vhp.res-line.ankunft) + " - " 
      + STRING(vhp.res-line.abreise) + CHR(10) 
      + "A:" + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
      + " Ch:" + STRING(vhp.res-line.kind1) 
      + " " + "(" + child-age + ")"
      + " - " + vhp.res-line.arrangement + CHR(10) 
      + vhp.res-line.bemerk. 
  END.
  ELSE
  DO:
    remark = remark + STRING(vhp.res-line.ankunft) + " - " 
      + STRING(vhp.res-line.abreise) + CHR(10) 
      + "A:" + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
      + " Ch:" + STRING(vhp.res-line.kind1)       
      + " - " + vhp.res-line.arrangement + CHR(10) 
      + vhp.res-line.bemerk. 
  END.
  
END. 

