
DEF INPUT  PARAMETER resrecid AS INT.
DEF OUTPUT PARAMETER klimit   AS DECIMAL.
DEF OUTPUT PARAMETER ksaldo LIKE vhp.bill.saldo.
DEF OUTPUT PARAMETER remark AS CHAR.

/*FD August 05, 2021 => Req Amaranta*/
DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE str AS CHARACTER NO-UNDO.
DEFINE VARIABLE child-age AS CHARACTER NO-UNDO.

FIND FIRST vhp.res-line WHERE RECID(res-line) = resrecid NO-LOCK NO-ERROR. 
RUN check-creditlimit.

PROCEDURE check-creditlimit: 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 
  FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
  FIND FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrpay NO-LOCK. 

  FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = vhp.guest.gastnr
      AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.mc-guest THEN
  ASSIGN remark = "Membership No: "+ vhp.mc-guest.cardnum + CHR(10).

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
  
  /*
  remark = STRING(vhp.res-line.ankunft) + " - " 
    + STRING(vhp.res-line.abreise) + chr(10) 
    + "A " + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
    + "  Ch " + STRING(vhp.res-line.kind1) 
    + " - " + vhp.res-line.arrangement + chr(10) 
    + vhp.res-line.bemerk. 
  */

  /*FD August 05, 2021 => Req Amaranta*/
  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    str = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(str,1,5) = "ChAge" THEN child-age = SUBSTR(str,6).
  END.
  
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
