DEF TEMP-TABLE t-resline  
    FIELD resnr     LIKE res-line.resnr  
    FIELD reslinnr  LIKE res-line.reslinnr  
    FIELD zinr      LIKE res-line.zinr  
    FIELD name      LIKE res-line.name.  
  
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER resrecid       AS INT.  
  
DEF OUTPUT PARAMETER klimit         AS DECIMAL.  
DEF OUTPUT PARAMETER ksaldo         LIKE vhp.bill.saldo.  
DEF OUTPUT PARAMETER remark         AS CHAR.  
DEF OUTPUT PARAMETER msg-str        AS CHAR.  
DEF OUTPUT PARAMETER TABLE FOR t-resline.  
  
{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "TS-table".  
  
FIND FIRST vhp.res-line WHERE RECID(res-line) = resrecid NO-LOCK NO-ERROR.   
IF AVAILABLE vhp.res-line THEN   
DO:   
  RUN ts-table-check-creditlimitbl.p  
      (resrecid, OUTPUT klimit, OUTPUT ksaldo, OUTPUT remark).  
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
  CREATE t-resline.
  ASSIGN
      t-resline.resnr     = res-line.resnr  
      t-resline.reslinnr  = res-line.reslinnr  
      t-resline.zinr      = res-line.zinr  
      t-resline.name      = res-line.name.
  RETURN NO-APPLY.   
END.   
