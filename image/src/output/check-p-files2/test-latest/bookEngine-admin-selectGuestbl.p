DEFINE TEMP-TABLE tguest
   FIELD gastnr     AS INTEGER
   FIELD name       AS CHARACTER.
   
DEFINE OUTPUT PARAMETER TABLE FOR tguest.   
   
FOR EACH guest WHERE guest.karteityp EQ 2 NO-LOCK:  
    CREATE tguest.
    ASSIGN
        tguest.gastnr       = guest.gastnr
        tguest.name         = guest.name.
END.
