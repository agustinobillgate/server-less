
DEF INPUT  PARAMETER gcfmember AS INT.
DEF INPUT  PARAMETER inp-resNo AS INT.
DEF INPUT  PARAMETER res-mode AS CHAR.
DEF OUTPUT PARAMETER billname AS CHAR.
DEF OUTPUT PARAMETER billadress AS CHAR.
DEF OUTPUT PARAMETER billcity AS CHAR.
DEF OUTPUT PARAMETER billland AS CHAR.
DEF OUTPUT PARAMETER name-editor AS CHAR.
DEF OUTPUT PARAMETER avail-mbuff AS INT.

DEFINE BUFFER member1 FOR guest.
DEFINE BUFFER mbuff   FOR master.

FIND FIRST member1 WHERE member1.gastnr = gcfmember NO-LOCK. 
billname    = member1.name + ", " + member1.vorname1 
            + member1.anredefirma + " " + member1.anrede1.
billadress  = member1.adresse1.
billcity    = member1.wohnort + " " + member1.plz. 
billland    = "".


FIND FIRST nation WHERE nation.kurzbez = member1.land NO-LOCK NO-ERROR. 
IF AVAILABLE nation THEN billland = nation.bezeich. 
name-editor = billname + chr(10) + chr(10) 
            + billadress + chr(10) 
            + billcity + chr(10) + chr(10) 
            + billland. 

IF res-mode EQ "new" THEN 
DO:
    FIND FIRST mbuff WHERE mbuff.resnr = inp-resNo NO-LOCK NO-ERROR.
    IF member1.zahlungsart = 0 AND NOT AVAILABLE mbuff THEN
        avail-mbuff = 1.
    ELSE avail-mbuff = 2.
END.
