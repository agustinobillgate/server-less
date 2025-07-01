DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.
DEFINE OUTPUT PARAMETER j       AS INTEGER INIT 0 NO-UNDO.


RUN del-old-l-op.

PROCEDURE del-old-l-op: 
DEFINE VARIABLE anz AS INTEGER. 
DEFINE VARIABLE lscheinnr AS CHAR. 
 
  /*MTmess-str = translateExtended ("Deleted old stock moving journals",lvCAREA,"") 
      + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
 
  FOR EACH l-lager NO-LOCK: 
    FIND FIRST l-op WHERE l-op.loeschflag = 0 AND l-op.pos GE 0 
       AND l-op.lager-nr = l-lager.lager-nr AND l-op.op-art = 1 
       AND l-op.lscheinnr = l-op.docu-nr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE l-op: 
      DO TRANSACTION: 
        FIND CURRENT l-op EXCLUSIVE-LOCK. 
        l-op.loeschflag = 1. 
        FIND CURRENT l-op NO-LOCK. 
        i = i + 1. 
        /*MTmess-str = translateExtended ("Number of purchase records",lvCAREA,"") 
            + " " + STRING(i). 
        DISP mess-str WITH FRAME frame1. */
      END. 
      FIND NEXT l-op WHERE l-op.loeschflag = 0 AND l-op.pos GE 0 
        AND l-op.lager-nr = l-lager.lager-nr AND l-op.op-art = 1 
        AND l-op.lscheinnr = l-op.docu-nr NO-LOCK NO-ERROR. 
    END. 
  END. 
 
  j = 0. 
  FIND FIRST fa-op WHERE fa-op.loeschflag = 0 
    AND fa-op.lscheinnr = fa-op.docu-nr NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE fa-op: 
    DO TRANSACTION: 
      FIND CURRENT fa-op EXCLUSIVE-LOCK. 
      fa-op.loeschflag = 1. 
      FIND CURRENT fa-op NO-LOCK. 
      j = j + 1. 
      /*MTmess-str = translateExtended ("Number of FA-purchase records",lvCAREA,"") 
          + " " + STRING(j). 
      DISP mess-str WITH FRAME frame1. */
      FIND NEXT fa-op WHERE fa-op.loeschflag = 0 
        AND fa-op.lscheinnr = fa-op.docu-nr NO-LOCK NO-ERROR. 
    END. 
  END. 
/* 
  i = 0. 
  FIND FIRST htparam WHERE paramnr = 883 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz LT 60 THEN anz = 60. 
  FIND FIRST fa-op WHERE fa-op.loeschflag GE 1 
    AND (fa-op.datum + anz) LT ci-date NO-ERROR. 
  DO WHILE AVAILABLE fa-op: 
    DO TRANSACTION: 
      FIND CURRENT fa-op EXCLUSIVE-LOCK. 
      delete fa-op. 
      i = i + 1. 
      mess-str = translateExtended ("Number of deleted FA-records",lvCAREA,"") 
          + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. 
    END. 
    FIND NEXT fa-op WHERE fa-op.loeschflag GE 1 
        AND (fa-op.datum + anz) LT ci-date NO-ERROR. 
  END. 
  PAUSE 0. 
*/ 
END. 

