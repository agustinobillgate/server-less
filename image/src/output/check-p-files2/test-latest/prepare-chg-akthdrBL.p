

DEFINE TEMP-TABLE akthdr1 LIKE akthdr.
DEFINE TEMP-TABLE t-akt-code LIKE akt-code.

DEF INPUT  PARAMETER aktnr AS INT.
DEF OUTPUT PARAMETER lname AS CHAR.
DEF OUTPUT PARAMETER namekontakt AS CHAR.
DEF OUTPUT PARAMETER kontakt-nr AS INT.
DEF OUTPUT PARAMETER comment AS CHAR.
DEF OUTPUT PARAMETER avail-guest AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER guest-gastnr AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR akthdr1.
DEF OUTPUT PARAMETER TABLE FOR t-akt-code.

/*Alder - Serverless - Issue 590 - Start*/
FIND FIRST akthdr WHERE akthdr.aktnr EQ aktnr NO-LOCK NO-ERROR.
IF AVAILABLE akthdr THEN
DO:
    RUN create-akthdr.

    FIND FIRST guest WHERE guest.gastnr EQ akthdr.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        lname = guest.NAME + ", " + guest.anredefirma.
        avail-guest = YES.
        guest-gastnr = guest.gastnr.

        FIND FIRST akt-kont WHERE akt-kont.gastnr EQ guest.gastnr 
            AND akt-kont.kontakt-nr EQ akthdr.kontakt-nr NO-LOCK NO-ERROR.
        IF AVAILABLE akt-kont THEN
        DO:
            namekontakt = akt-kont.NAME + ", " + akt-kont.vorname + " " + akt-kont.anrede.
            kontakt-nr = akt-kont.kontakt-nr.
        END.
        comment = akthdr.bemerk.
    END.
END.

FOR EACH akt-code NO-LOCK:
    CREATE t-akt-code.
    BUFFER-COPY akt-code TO t-akt-code.
END.

PROCEDURE create-akthdr:
    CREATE akthdr1.
    BUFFER-COPY akthdr TO akthdr1.
END PROCEDURE.
/*Alder - Serverless - Issue 590 - End*/

/*
FIND FIRST akthdr WHERE akthdr.aktnr = aktnr EXCLUSIVE-LOCK. 
RUN create-akthdr.


FIND FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK.
lname = guest.NAME + ", " + guest.anredefirma. 
avail-guest = YES.
guest-gastnr = guest.gastnr.

FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr 
    AND akt-kont.kontakt-nr = akthdr1.kontakt-nr NO-LOCK NO-ERROR. 
IF AVAILABLE akt-kont THEN 
DO: 
    namekontakt = akt-kont.name + ", " + akt-kont.vorname 
       + " " + akt-kont.anrede. 
    kontakt-nr = akt-kont.kontakt-nr. 
END.  
comment = akthdr1.bemerk. 

FOR EACH akt-code NO-LOCK:
    CREATE t-akt-code.
    BUFFER-COPY akt-code TO t-akt-code.
END.

PROCEDURE create-akthdr:
    CREATE akthdr1.
    BUFFER-COPY akthdr TO akthdr1.
END.
*/


