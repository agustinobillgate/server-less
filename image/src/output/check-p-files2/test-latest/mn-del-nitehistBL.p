
DEFINE VARIABLE datum1      AS DATE INITIAL ?.
DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN del-nitehist.


PROCEDURE del-nitehist: 
DEFINE VARIABLE store-flag  AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE anz         AS INTEGER INITIAL 0  NO-UNDO.
DEFINE VARIABLE curr-date   AS DATE    INITIAL ?  NO-UNDO.
DEFINE BUFFER nbuff         FOR vhp.nitehis.

  FIND FIRST htparam WHERE paramnr = 230 NO-LOCK. 
  IF htparam.feldtyp = 4 AND htparam.flogical THEN store-flag = YES. 
  IF NOT store-flag THEN RETURN. 
  FIND FIRST htparam WHERE htparam.paramnr = 238 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 60. 
    IF CONNECTED ("vhparch") THEN
    DO:
        datum1 = ci-date - anz.
        RUN mnstart-arch.p('del-nitehis', 0, datum1).
    END.
    ELSE
    DO:
      FIND FIRST vhp.nitehist /* WHERE vhp.nitehist.datum LE (ci-date - anz) */
        USE-INDEX date_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE vhp.nitehis:
        IF vhp.nitehis.datum GT (ci-date - anz) THEN LEAVE.
        DO TRANSACTION:
          FIND FIRST nbuff WHERE RECID(nbuff) = RECID(vhp.nitehis) EXCLUSIVE-LOCK.
          DELETE nbuff.
          RELEASE nbuff.
        END.
        FIND NEXT vhp.nitehist /* WHERE vhp.nitehist.datum LE (ci-date - anz) */
          USE-INDEX date_ix NO-LOCK NO-ERROR.
      END. 
    END. 

    /*MT 24/04/13 */
    FIND FIRST nightaudit WHERE nightaudit.programm = "nt-onlinetax.p" 
       OR nightaudit.programm = "nt-aiirevenue.p" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE nightaudit THEN RETURN.
    FIND FIRST vhp.nitehist WHERE vhp.nitehist.reihenfolge = nightaudit.reihenfolge
      USE-INDEX date_ix NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE vhp.nitehis:
      IF vhp.nitehis.datum GT (ci-date - 65) THEN LEAVE.
      DO TRANSACTION:
        FIND FIRST nbuff WHERE RECID(nbuff) = RECID(vhp.nitehis) EXCLUSIVE-LOCK.
        DELETE nbuff.
        RELEASE nbuff.
      END.
      FIND NEXT vhp.nitehist WHERE vhp.nitehist.reihenfolge = nightaudit.reihenfolge
        USE-INDEX date_ix NO-LOCK NO-ERROR.
    END. 

  PAUSE 0. 
END. 

/*MT
PROCEDURE del-nitehist:
DEFINE VARIABLE store-flag AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE anz AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE BUFFER nbuff FOR vhp.nitehis.

  FIND FIRST htparam WHERE paramnr = 230 NO-LOCK. 
  IF htparam.feldtyp = 4 AND htparam.flogical THEN store-flag = YES. 
  IF NOT store-flag THEN RETURN. 
  FIND FIRST htparam WHERE htparam.paramnr = 238 NO-LOCK. 
  anz = htparam.finteger. 
  IF anz = 0 THEN anz = 35. 
    
  FOR EACH vhp.nitehist WHERE vhp.nitehist.datum LE (ci-date - anz) 
    AND vhp.nitehis.reihenfolge LT 10000000 NO-LOCK:
    DO TRANSACTION:
      FIND FIRST nbuff WHERE RECID(nbuff) = RECID(vhp.nitehis) EXCLUSIVE-LOCK.
      DELETE nbuff.
      RELEASE nbuff.
    END.
  END. 

  FIND FIRST nightaudit WHERE nightaudit.programm = "nt-onlinetax" 
     NO-LOCK NO-ERROR.
  IF NOT AVAILABLE nightaudit THEN RETURN.
  FIND FIRST vhp.nitehist WHERE vhp.nitehist.reihenfolge = nightaudit.reihenfolge
    USE-INDEX date_ix NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE vhp.nitehis:
    IF vhp.nitehis.datum GT (ci-date - 65) THEN LEAVE.
    DO TRANSACTION:
      FIND FIRST nbuff WHERE RECID(nbuff) = RECID(vhp.nitehis) EXCLUSIVE-LOCK.
      DELETE nbuff.
      RELEASE nbuff.
    END.
    FIND NEXT vhp.nitehist WHERE vhp.nitehist.reihenfolge = nightaudit.reihenfolge
      USE-INDEX date_ix NO-LOCK NO-ERROR.
  END. 


END. 
*/
