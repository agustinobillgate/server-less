
DEF INPUT PARAMETER t-gastnrmember AS INT.
DEF INPUT PARAMETER ext-char AS CHAR.
DEF OUTPUT PARAMETER progname AS CHAR.
DEF OUTPUT PARAMETER t-gastnr AS INT.

FIND FIRST guest WHERE guest.gastnr = t-gastnrmember NO-LOCK. 
progname = "chg-gcf" + ext-char + STRING(guest.karteityp) + "UI.p".
t-gastnr = guest.gastnr.
