DEFINE INPUT PARAMETER case-type AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER record-key AS CHAR.
DEFINE INPUT PARAMETER image-nr AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.

DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE pointer AS MEMPTR NO-UNDO.

IF case-type NE "OOO" AND
   case-type NE "LostAndFound" THEN RETURN.


FOR EACH queasy WHERE queasy.KEY EQ 195 AND
  queasy.char1 EQ case-type + ";" + record-key
   NO-LOCK BY queasy.number2 :

  i = i + 1.

  IF image-nr EQ i THEN
  DO:
    LEAVE.
  END.
END.

IF AVAILABLE queasy THEN
DO:
  FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number1
    EXCLUSIVE-LOCK NO-ERROR.

  IF AVAILABLE guestbook THEN
  DO:
    DELETE guestbook.
  END.

  FIND CURRENT queasy EXCLUSIVE-LOCK.
  DELETE queasy.
END.

