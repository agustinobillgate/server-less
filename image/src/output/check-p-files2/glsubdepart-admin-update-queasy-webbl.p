/*FD Nov 09, 2020 => BL for vhp web based, move from UI progress*/

DEF TEMP-TABLE g-list        LIKE queasy.
DEF TEMP-TABLE t-queasy      LIKE queasy.

DEFINE INPUT PARAMETER curr-mode AS CHARACTER.
DEFINE INPUT PARAMETER t-gl-depart-nr AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-queasy.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR g-list.

DEFINE BUFFER queasy1 FOR t-queasy.

DEF VARIABLE new-number AS INTEGER NO-UNDO INIT 1.

FIND FIRST g-list NO-ERROR.

IF curr-mode = "add" THEN
DO:
  FOR EACH g-list:
      CREATE t-queasy.
      BUFFER-COPY g-list TO t-queasy.
  END.  
  
  FOR EACH queasy1 BY queasy1.number1 DESCENDING:
      new-number = queasy1.number1 + 1.
      LEAVE.
  END.
  ASSIGN 
      t-queasy.number1 = new-number
      t-queasy.number2 = t-gl-depart-nr
  .

  FOR EACH t-queasy:
      FIND FIRST g-list WHERE g-list.KEY = t-queasy.KEY
          AND g-list.char1 = t-queasy.char1 EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE g-list THEN
      DO:
          BUFFER-COPY t-queasy TO g-list.
          FIND CURRENT g-list NO-LOCK.
          RELEASE g-list.
      END.
  END.
END.
ELSE IF curr-mode = "chg" THEN
DO:
    FOR EACH g-list:
        FIND FIRST t-queasy WHERE t-queasy.KEY = g-list.KEY
            AND t-queasy.char1 = g-list.char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE t-queasy THEN
        DO:
            BUFFER-COPY g-list TO t-queasy.
            ASSIGN t-queasy.number2 = t-gl-depart-nr.
            FIND CURRENT t-queasy NO-LOCK.
            RELEASE t-queasy.
        END.
    END. 
END.

