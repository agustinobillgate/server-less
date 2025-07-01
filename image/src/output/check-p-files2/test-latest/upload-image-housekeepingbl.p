DEFINE INPUT PARAMETER case-type AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER record-key AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER imagedata AS LONGCHAR NO-UNDO.
DEFINE INPUT PARAMETER imagedescription AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str AS CHAR NO-UNDO.

DEFINE VARIABLE i AS INTEGER NO-UNDO.
DEFINE VARIABLE lastNumber AS INTEGER NO-UNDO.
DEFINE VARIABLE last-guestbook-nr AS INTEGER NO-UNDO.
DEFINE VARIABLE pointer AS MEMPTR NO-UNDO.

DEFINE VARIABLE max-images AS INTEGER NO-UNDO.

max-images = 3.

IF case-type NE "OOO" AND
   case-type NE "LostAndFound" THEN RETURN.

IF imagedescription EQ ? THEN
DO:
  imagedescription = "".
END.

FOR EACH queasy WHERE queasy.KEY EQ 195 AND
  queasy.char1 EQ case-type + ";" + record-key 
  NO-LOCK BY queasy.number2 :

  lastNumber = queasy.number2.
  i = i + 1.
END.

IF i LT max-images THEN
DO:
  CREATE queasy.
  ASSIGN
    queasy.char1 = case-type + ";" + record-key
    queasy.char3 = imagedescription
    queasy.KEY = 195
    queasy.number2 = lastNumber + 1
    .    

  FIND FIRST guestbook WHERE guestbook.gastnr LE -40000000 NO-LOCK NO-ERROR.
  
  IF NOT AVAILABLE guestbook THEN
  DO:
    CREATE guestbook.
    guestbook.gastnr = -40000000.
  END.
  ELSE
  DO:
    last-guestbook-nr = guestbook.gastnr.
    CREATE guestbook.  
    guestbook.gastnr = last-guestbook-nr - 1.
  END.
  pointer = BASE64-DECODE(imagedata).
  COPY-LOB pointer TO guestbook.imagefile.
  
  queasy.number1 = guestbook.gastnr.

  FIND CURRENT guestbook NO-LOCK.
  RELEASE guestbook.
  FIND CURRENT queasy NO-LOCK.
  RELEASE queasy.
END.
ELSE
DO:
  msg-str = "You are only allowed to upload up to " + STRING(max-images)
     + " images for each room".
END.


