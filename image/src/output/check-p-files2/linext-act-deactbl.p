
DEF INPUT PARAMETER  case-type    AS INT.
DEF INPUT PARAMETER  sameResno    AS LOGICAL.
DEF INPUT PARAMETER  resnr        AS INT.
DEF INPUT PARAMETER  reslinnr     AS INT.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

DEF BUFFER intbuff FOR INTERFACE.
DEF BUFFER rbuff FOR res-line.

FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-ERROR.

CASE case-type:
    WHEN 1 THEN RUN activate-linext.
    WHEN 2 THEN RUN deactivate-linext.
END.

PROCEDURE activate-linext:

  FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
  IF NOT htparam.flogical THEN RETURN.  /* License FOR Line Switching */ 

  FIND FIRST interface WHERE interface.key = 2 
    AND interface.zinr = res-line.zinr 
    AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE interface: 

    DO TRANSACTION:
        FIND FIRST intbuff WHERE RECID(intbuff) = RECID(interface)
            EXCLUSIVE-LOCK.
        DELETE intbuff.
        RELEASE intbuff.
    END.

    FIND NEXT interface WHERE interface.key = 2 
      AND interface.zinr = res-line.zinr 
      AND interface.decfield LE 3 NO-LOCK NO-ERROR.
  END. 
  IF AVAILABLE res-line THEN
  DO:
      RUN intevent-1.p( 1, res-line.zinr, "Activate!", res-line.resnr, res-line.reslinnr). 
      success-flag = YES.
  END.
END.


PROCEDURE deactivate-linext:
  
  
  FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
  IF NOT htparam.flogical THEN RETURN.  /* License FOR Line Switching */ 

  FIND FIRST interface WHERE interface.key = 2 
    AND interface.zinr = res-line.zinr 
    AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE interface: 
    FIND CURRENT interface EXCLUSIVE-LOCK. 
    DELETE interface. 
    FIND NEXT interface WHERE interface.key = 2 
      AND interface.zinr = res-line.zinr 
      AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
  END. 
  RUN intevent-1.p( 2, res-line.zinr, "Deactivate!", res-line.resnr, res-line.reslinnr). 
  
  IF sameResNo THEN
  FOR EACH rbuff WHERE rbuff.resnr = res-line.resnr
    AND rbuff.active-flag = 1
    AND rbuff.resstatus = 6
    AND rbuff.zinr NE res-line.zinr NO-LOCK:
    FIND FIRST interface WHERE interface.key = 2 
      AND interface.zinr = rbuff.zinr 
      AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE interface: 
      FIND CURRENT interface EXCLUSIVE-LOCK. 
      DELETE interface. 
      FIND NEXT interface WHERE interface.key = 2 
        AND interface.zinr = rbuff.zinr 
        AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    END.
    RUN intevent-1.p( 2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr).
  END.
  success-flag = YES.
END.
