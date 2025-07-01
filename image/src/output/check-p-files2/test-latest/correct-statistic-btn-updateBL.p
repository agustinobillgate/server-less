DEFINE TEMP-TABLE genlist LIKE genstat
    FIELD rsv-name      AS CHAR FORMAT "x(25)" COLUMN-LABEL "Rsv Name"
    FIELD nat-str       AS CHAR FORMAT "x(3)" COLUMN-LABEL "NAT"
    FIELD ctry-str      AS CHAR FORMAT "x(3)" COLUMN-LABEL "Country"
    FIELD source-str    AS CHAR FORMAT "x(20)" COLUMN-LABEL "Source"
    FIELD segment-str   AS CHAR FORMAT "x(20)" COLUMN-LABEL "Segment"
    FIELD REC-gen AS INTEGER.

DEF INPUT PARAMETER TABLE FOR genlist.
DEF INPUT PARAMETER rec-gen AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
/*
FIND FIRST genlist.
DO TRANSACTION : 
    FIND FIRST genstat WHERE RECID(genstat) = rec-gen EXCLUSIVE-LOCK.
    BUFFER-COPY genlist EXCEPT genlist.datum genlist.zinr TO genstat .
    FIND CURRENT genstat NO-LOCK.
END.*/


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

DO TRANSACTION:
    FIND FIRST genlist NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE genlist:
      FIND FIRST genstat WHERE RECID(genstat) = genlist.rec-gen EXCLUSIVE-LOCK.
      RUN res-history.
      BUFFER-COPY genlist EXCEPT genlist.datum genlist.zinr TO genstat .
      /*FDL Nov 18, 2024: Ticket E6115E*/
      IF (genstat.zipreis EQ 0) AND ((genstat.erwachs + genstat.kind1) GT 0) THEN genstat.res-logic[3] = YES.
      ELSE genstat.res-logic[3] = NO.
      FIND CURRENT genstat NO-LOCK.
      FIND NEXT genlist NO-LOCK NO-ERROR.
    END.
    RELEASE genstat.
END.

PROCEDURE res-history:
  DEFINE VARIABLE temp-segment AS CHAR.
  FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
  FIND FIRST res-line WHERE res-line.resnr = genlist.resnr NO-LOCK NO-ERROR.

  temp-segment = segment.bezeich.
  CREATE res-history. 
  ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.resnr       = genlist.resnr 
        res-history.reslinnr    = res-line.reslinnr 
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "Segment" 
        /*res-history.aenderung = "Segment has been changed to " + segment.bezeich.*/
        res-history.aenderung = "Reservation " + STRING(genlist.resnr) + ", Segment has been changed from " + 
                                temp-segment + " to " + genlist.segment-str.
END.
