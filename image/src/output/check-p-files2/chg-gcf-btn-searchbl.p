
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER master-gastnr AS INT.
DEF OUTPUT PARAMETER progname AS CHAR.
DEF OUTPUT PARAMETER mastername AS CHAR.
DEF OUTPUT PARAMETER gbuff-gastnr AS INT.


DEFINE VARIABLE ext-char AS CHAR NO-UNDO.
DEFINE BUFFER gbuff      FOR guest.

IF case-type = 0 THEN
DO:
    FIND FIRST gbuff WHERE gbuff.gastnr = master-gastnr NO-LOCK NO-ERROR.
    mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma 
    + " " + gbuff.anrede1.
    RETURN.
END.

FIND FIRST htparam WHERE paramnr = 148 NO-LOCK.
ASSIGN ext-char = htparam.fchar.
FIND FIRST gbuff WHERE gbuff.gastnr = master-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE gbuff THEN
DO:
    gbuff-gastnr = gbuff.gastnr. 
    progname = "chg-gcf" + ext-char + STRING(gbuff.karteityp) + "UI.p".
    mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma 
    + " " + gbuff.anrede1.
END.
