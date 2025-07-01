

DEFINE TEMP-TABLE guest1 LIKE guest.
DEFINE TEMP-TABLE akt-kont1 LIKE akt-kont.

DEF INPUT PARAMETER inp-gastnr AS INTEGER.
DEF OUTPUT PARAMETER lname AS CHAR.
DEF OUTPUT PARAMETER namekontakt AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR guest1.
DEF OUTPUT PARAMETER TABLE FOR akt-kont1.

CREATE guest1.
CREATE akt-kont1.
FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
DO:
   guest1.gastnr = guest.gastnr.
   lname = guest.NAME + ", " + guest.anredefirma.
   guest1.adresse1 = guest.adresse1.
   guest1.adresse2 = guest.adresse2.
   guest1.adresse3 = guest.adresse3.
   guest1.wohnort = guest.wohnort.
   guest1.plz = guest.plz.
   guest1.land = guest.land.
   guest1.telefon = guest.telefon.
   guest1.fax = guest.fax.
   guest1.email-adr = guest.email-adr.
END.
FIND FIRST akt-kont WHERE akt-kont.gastnr = inp-gastnr AND akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR.
IF AVAILABLE akt-kont THEN
DO:
   namekontakt = akt-kont.name + ", " + akt-kont.vorname 
                      + " " + akt-kont.anrede.
   akt-kont1.geburtdatum1 = akt-kont.geburtdatum1.
   akt-kont1.geburt-ort1 = akt-kont.geburt-ort1.
   akt-kont1.telefon = akt-kont.telefon.
   akt-kont1.durchwahl = akt-kont.durchwahl.
   akt-kont1.abteilung = akt-kont.abteilung.
   akt-kont1.funktion = akt-kont.funktion.
   akt-kont1.email-adr = akt-kont.email-adr.
END.
