DEFINE TEMP-TABLE res-list LIKE res-line
    FIELD kurzbez           LIKE zimkateg.kurzbez
    FIELD groupname         LIKE reservation.groupname
    FIELD join-flag         AS LOGICAL LABEL "JoinGroup" 
    FIELD mbill-flag        AS LOGICAL LABEL "Assign Mbill" 
    FIELD prev-join         AS LOGICAL
    FIELD prev-mbill        AS LOGICAL.


DEFINE INPUT PARAMETER resNo           AS INTEGER.
DEFINE INPUT PARAMETER selected-resnr  AS INTEGER.
DEFINE INPUT PARAMETER user-init       AS CHAR.
DEFINE INPUT PARAMETER TABLE FOR res-list.

FIND FIRST bediener WHERE bediener.userinit = user-init.
RUN join-it.


PROCEDURE join-it:
DEF VAR RmNo     AS CHAR NO-UNDO.
DEF BUFFER rline FOR res-line.
DEF BUFFER mbuff FOR reservation.
  
  FIND FIRST res-list     NO-ERROR.

  DO TRANSACTION:
      FOR EACH res-line WHERE res-line.resnr = selected-resnr 
          AND res-line.l-zuordnung[5] = 0 NO-LOCK:
          FIND FIRST rline WHERE RECID(rline) = RECID(res-line)
              EXCLUSIVE-LOCK.
          ASSIGN rline.l-zuordnung[5] = selected-resnr.
          FIND CURRENT rline NO-LOCK.
      END.
      
        FIND FIRST mbuff WHERE mbuff.resnr = selected-resnr NO-LOCK.
        FIND FIRST reservation WHERE reservation.resnr = resNo EXCLUSIVE-LOCK.
        ASSIGN 
            reservation.grpflag   = mbuff.grpflag
            reservation.groupname = mbuff.groupname
            reservation.verstat   = mbuff.verstat
        .
        FIND CURRENT reservation NO-LOCK.
      
      FOR EACH res-list WHERE (res-list.prev-join NE res-list.join-flag)
          OR (res-list.prev-mbill NE res-list.mbill-flag):
        FIND FIRST res-line WHERE res-line.resnr = res-list.resnr
          AND res-line.reslinnr = res-list.reslinnr EXCLUSIVE-LOCK.
        
        IF res-list.join-flag THEN 
        DO:
          ASSIGN 
              res-line.l-zuordnung[5] = selected-resnr
              res-line.l-zuordnung[2] = 0.
        END.
        ELSE
        ASSIGN
            res-line.l-zuordnung[2] = 2 
            res-line.l-zuordnung[5] = 0
        .
        FIND CURRENT res-line NO-LOCK.

        IF (res-list.prev-join NE res-list.join-flag) THEN
        DO:
          CREATE res-history. 
          IF res-list.join-flag THEN
          ASSIGN 
            res-history.nr = bediener.nr 
            res-history.datum = TODAY 
            res-history.zeit = TIME
            res-history.action = "Reservation"
            res-history.aenderung = "ResNo: " + STRING(resNo) +
              " RmNo: " + res-line.zinr + " " + res-line.NAME
              + " - Connect to Group ResNo " + STRING(selected-resnr)
          .
          ELSE
          ASSIGN 
            res-history.nr = bediener.nr 
            res-history.datum = TODAY 
            res-history.zeit = TIME
            res-history.action = "Reservation"
            res-history.aenderung = "ResNo: " + STRING(resNo) +
              " RmNo: " + res-line.zinr + " " + res-line.NAME
              + " - Disconnect from Group ResNo " + STRING(selected-resnr)
          .
          FIND CURRENT res-history NO-LOCK. 
          RELEASE res-history. 
        END.

        FOR EACH res-line WHERE res-line.resnr = res-list.resnr
          AND res-line.kontakt-nr = res-list.reslinnr
          AND res-line.l-zuordnung[3] = 1 NO-LOCK:
          FIND FIRST rline WHERE RECID(rline) = RECID(res-line)
              EXCLUSIVE-LOCK.
          IF res-list.join-flag THEN 
            ASSIGN rline.l-zuordnung[5] = selected-resnr.
          ELSE rline.l-zuordnung[5] = 0.
          FIND CURRENT rline NO-LOCK.
        END.
      END.
  END.
END.
