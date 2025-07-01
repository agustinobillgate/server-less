DEFINE TEMP-TABLE c-list 
  FIELD gastnr      AS INTEGER 
  FIELD name        AS CHAR FORMAT "x(32)" LABEL "Guest Name" 
  FIELD nat         LIKE guest.nation1 FORMAT "x(4)"
  FIELD resnr1      LIKE res-line.resnr FORMAT ">>>>>>>"
  FIELD ankunft1    LIKE res-line.ankunft INITIAL ?
  FIELD abreise1    LIKE res-line.abreise INITIAL ?
  FIELD zinr1       LIKE res-line.zinr
  FIELD resnr2      LIKE res-line.resnr FORMAT ">>>>>>>"
  FIELD ankunft2    LIKE res-line.ankunft INITIAL ?
  FIELD abreise2    LIKE res-line.abreise INITIAL ?
  FIELD zinr2       LIKE res-line.zinr
  FIELD resnr3      LIKE res-line.resnr FORMAT ">>>>>>>"
  FIELD ankunft3    LIKE res-line.ankunft INITIAL ?
  FIELD abreise3    LIKE res-line.abreise INITIAL ?
  FIELD zinr3       LIKE res-line.zinr
.

DEFINE OUTPUT PARAMETER TABLE FOR c-list.

FOR EACH c-list: 
  DELETE c-list. 
END. 

FOR EACH segment WHERE segment.betriebsnr = 4 NO-LOCK:
  FOR EACH guestseg WHERE guestseg.segmentcode = segment.segmentcode
      NO-LOCK:
      FIND FIRST c-list WHERE c-list.gastnr = guestseg.gastnr NO-ERROR.
      IF NOT AVAILABLE c-list THEN
      DO:
          FIND FIRST guest WHERE guest.gastnr = guestseg.gastnr NO-LOCK.
          CREATE c-list.
          ASSIGN
              c-list.gastnr = guest.gastnr
              c-list.NAME   = guest.NAME + ", " + guest.vorname1
              c-list.nat    = guest.nation1
          .
      END.
  END.
END.

FOR EACH c-list:
  FOR EACH history WHERE history.gastnr = c-list.gastnr
      AND NOT history.zi-wechsel BY history.abreise DESCENDING:
      ASSIGN
          c-list.resnr1   = history.resnr
          c-list.zinr1    = history.zinr
          c-list.ankunft1 = history.ankunft
          c-list.abreise1 = history.abreise
      .
      LEAVE.
  END.
  FIND FIRST res-line WHERE (res-line.gastnr = c-list.gastnr OR res-line.gastnrmember = c-list.gastnr)  /*william 05/01/24 add res-line.gastnrmember = c-list.gastnr 29BE6F*/
      AND res-line.active-flag = 1 AND res-line.resstatus NE 12
      NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN
  ASSIGN
      c-list.resnr2   = res-line.resnr
      c-list.zinr2    = res-line.zinr
      c-list.ankunft2 = res-line.ankunft
      c-list.abreise2 = res-line.abreise
  .
  FOR EACH res-line WHERE res-line.gastnrmember = c-list.gastnr
      AND res-line.active-flag = 0 NO-LOCK BY res-line.ankunft:
    ASSIGN
      c-list.resnr3   = res-line.resnr
      c-list.zinr3    = res-line.zinr
      c-list.ankunft3 = res-line.ankunft
      c-list.abreise3 = res-line.abreise
    .
    LEAVE.
  END.
END.
