DEFINE TEMP-TABLE na-list   
  FIELD reihenfolge AS INTEGER   
  FIELD flag        AS INTEGER   
  FIELD bezeich     LIKE nightaudit.bezeichnung   
  FIELD anz         AS INTEGER FORMAT ">>,>>9".  


DEFINE INPUT-OUTPUT PARAMETER TABLE FOR na-list.
DEFINE INPUT PARAMETER ci-date AS DATE NO-UNDO.

DEFINE OUTPUT PARAMETER i AS INTEGER NO-UNDO.

DEFINE BUFFER breserv FOR reservation.

FOR EACH res-line WHERE res-line.ankunft = ci-date
    AND res-line.active-flag = 0 NO-LOCK:

    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE reservation THEN DO:
        FIND FIRST na-list WHERE na-list.reihenfolge = 4 NO-ERROR. 

        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        CREATE breserv. 
        ASSIGN 
            breserv.resnr      = res-line.resnr 
            breserv.gastnr     = guest.gastnr 
            breserv.gastnrherk = guest.gastnr 
            breserv.name       = guest.name
            breserv.herkunft   = guest.name + ", " + guest.vorname1 + guest.anredefirma 
            i = i + 1
            na-list.anz = na-list.anz + 1
        .   
        RELEASE breserv.
    END.
END.
