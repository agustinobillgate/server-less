
DEF INPUT  PARAMETER bill-gastnr AS INT.
DEF OUTPUT PARAMETER resname     AS CHAR.

DEFINE VARIABLE g-address   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-wonhort   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-plz       AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-land      AS CHARACTER NO-UNDO.

FIND FIRST guest WHERE guest.gastnr = bill-gastnr NO-LOCK. 

/*FD Oct 06, 2022 => Ticket 559E7C - Bill Address Empty Cause Value=?*/
ASSIGN
    g-address   = guest.adresse1
    g-wonhort   = guest.wohnort
    g-plz       = guest.plz
    g-land      = guest.land
    .
IF g-address EQ ? THEN g-address = "".
IF g-wonhort EQ ? THEN g-wonhort = "".
IF g-plz EQ ? THEN g-plz = "".
IF g-land EQ ? THEN g-land = "".

resname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
          + " " + guest.anrede1 
          + chr(10) + g-address 
          + chr(10) + g-wonhort + " " + g-plz 
          + chr(10) + g-land. 
