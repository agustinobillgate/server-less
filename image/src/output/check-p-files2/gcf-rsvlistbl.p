
DEF TEMP-TABLE rline-list
  FIELD  resstatus AS INTEGER 
  FIELD  resnr     LIKE res-line.resnr FORMAT ">>>>>>9"
  FIELD  name      LIKE res-line.NAME  FORMAT "x(32)" 
  FIELD  ankunft   LIKE res-line.ankunft
  FIELD  abreise   LIKE res-line.abreise
  FIELD  zinr      LIKE res-line.zinr
.

DEF INPUT  PARAMETER gastNo AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR rline-list.

FOR EACH res-line WHERE res-line.gastnrmember = gastNo
  /*AND res-line.active-flag    LE 1 */
  AND res-line.resstatus      NE 12
  AND res-line.resstatus      NE 99
  AND res-line.l-zuordnung[3] NE 1 NO-LOCK: 
 FIND FIRST history WHERE history.gastnr = gastNo  NO-ERROR.
 FIND FIRST guest WHERE guest.gastnr = gastNo  NO-ERROR.
  CREATE rline-list.
 BUFFER-COPY res-line EXCEPT res-line.NAME TO rline-list .
 ASSIGN
     rline-list.NAME = guest.NAME.
END.
