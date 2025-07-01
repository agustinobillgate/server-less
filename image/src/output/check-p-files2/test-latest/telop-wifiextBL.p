
DEF INPUT PARAMETER  case-type    AS INT.
DEF INPUT PARAMETER  resnr        AS INT.
DEF INPUT PARAMETER  reslinnr     AS INT.
DEF INPUT PARAMETER  sameResNo    AS LOGICAL.

DEF BUFFER rbuff FOR res-line.

FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-ERROR.

IF case-type = 1 THEN
DO:
    FIND FIRST interface WHERE interface.key = 9
        AND interface.zinr = res-line.zinr 
        AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE interface: 
        FIND CURRENT interface EXCLUSIVE-LOCK. 
        delete interface. 
        FIND NEXT interface WHERE interface.key = 9
          AND interface.zinr = res-line.zinr 
          AND interface.decfield LE 3 NO-LOCK NO-ERROR. 
    END.
    RUN intevent-1.p( 1, res-line.zinr, "Activate!", res-line.resnr, res-line.reslinnr).
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST interface WHERE interface.key = 10
        AND interface.zinr = res-line.zinr 
        AND interface.decfield LE 10 NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE interface: 
        FIND CURRENT interface EXCLUSIVE-LOCK. 
        DELETE interface. 
        FIND NEXT interface WHERE interface.key = 10
          AND interface.zinr = res-line.zinr 
          AND interface.decfield LE 10 NO-LOCK NO-ERROR. 
    END.
    RUN intevent-1.p( 2, res-line.zinr, "Deactivate!", res-line.resnr, res-line.reslinnr). 

    IF sameResNo THEN
    FOR EACH rbuff WHERE rbuff.resnr = res-line.resnr
      AND rbuff.active-flag = 1
      AND rbuff.resstatus = 6
      AND rbuff.zinr NE res-line.zinr NO-LOCK:
      FIND FIRST interface WHERE interface.key = 10
        AND interface.zinr = rbuff.zinr 
        AND interface.decfield LE 10 NO-LOCK NO-ERROR. 
      DO WHILE AVAILABLE interface: 
        FIND CURRENT interface EXCLUSIVE-LOCK. 
        DELETE interface. 
        FIND NEXT interface WHERE interface.key = 10
          AND interface.zinr = rbuff.zinr 
          AND interface.decfield LE 10 NO-LOCK NO-ERROR. 
      END.
      RUN intevent-1.p( 2, rbuff.zinr, "Deactivate!", rbuff.resnr, rbuff.reslinnr).
    END.

END.
