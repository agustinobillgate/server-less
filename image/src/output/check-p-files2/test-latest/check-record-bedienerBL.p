
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER userinit AS CHAR.
DEF INPUT  PARAMETER bed-userinit AS CHAR.
DEF INPUT  PARAMETER nr AS INT.
DEF OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "check-record-bediener".

RUN check-record.

PROCEDURE check-record: 
  
  FIND FIRST bill-line WHERE bill-line.userinit = userinit NO-LOCK NO-ERROR. 
  IF AVAILABLE bill-line THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Bill line exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST billjournal WHERE billjournal.userinit = userinit NO-LOCK NO-ERROR. 
  IF AVAILABLE billjournal THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Bill journal exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST h-bill-line WHERE h-bill-line.kellner-nr = nr 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE h-bill-line THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Restaurant bill line exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST h-journal WHERE h-journal.kellner-nr = nr NO-LOCK NO-ERROR. 
  IF AVAILABLE h-journal THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Restaurant bill journal exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST zimmer WHERE zimmer.bediener-nr-stat = nr NO-LOCK NO-ERROR. 
  IF AVAILABLE zimmer THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Last status changed of Room-# :",lvCAREA,"") + zimmer.zinr 
            + " " + translateExtended ("by this user-id, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST debitor WHERE debitor.bediener-nr = nr NO-LOCK NO-ERROR. 
  IF AVAILABLE debitor THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("A/R record exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST l-kredit WHERE l-kredit.bediener-nr = nr NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("A/P record exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST res-line WHERE res-line.cancelled-id = userinit 
    OR res-line.changed-id = bed-userinit NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Reservation exists, deleting not possible.",lvCAREA,"").
  END. 
 
  FIND FIRST reservation WHERE reservation.useridanlage = userinit 
    OR reservation.useridmutat = bed-userinit NO-LOCK NO-ERROR. 
  IF AVAILABLE reservation THEN 
  DO: 
    its-ok = NO. 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Reservation exists, deleting not possible.",lvCAREA,"").
  END. 

END. 
