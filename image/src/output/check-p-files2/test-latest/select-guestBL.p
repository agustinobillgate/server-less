DEFINE TEMP-TABLE t-guest
    FIELD gastnr        LIKE guest.gastnr
    FIELD name          LIKE guest.name
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD wohnort       LIKE guest.wohnort
    FIELD adresse1      LIKE guest.adresse1
    FIELD vorname1      LIKE guest.vorname1
    FIELD anrede1       LIKE guest.anrede1.

DEF INPUT PARAMETER sorttype  AS INTEGER.
DEF INPUT PARAMETER curr-name AS CHAR.
DEF OUTPUT PARAMETER TABLE    FOR t-guest.

DEF VAR to-name               AS CHAR INIT "" NO-UNDO.

IF ASC(SUBSTR(curr-name,1,1)) LE 255 THEN 
  to-name = SUBSTR(curr-name,1,1) + "zzzz".

IF SUBSTR(curr-name,1,1) = "*" THEN
FOR EACH guest WHERE guest.name MATCHES curr-name 
  AND guest.karteityp = sorttype 
  AND guest.gastnr GT 0 USE-INDEX typ-wohn-name_ix NO-LOCK BY guest.NAME :
  CREATE t-guest.
  ASSIGN
    t-guest.gastnr        = guest.gastnr
    t-guest.name          = guest.name
    t-guest.anredefirma   = guest.anredefirma
    t-guest.wohnort       = guest.wohnort
    t-guest.adresse1      = guest.adresse1
    t-guest.vorname1      = guest.vorname1
    t-guest.anrede1       = guest.anrede1
  .
END.
ELSE IF to-name NE "" THEN
FOR EACH guest WHERE guest.name GE curr-name 
  AND guest.NAME LE to-name
  AND guest.karteityp = sorttype 
  AND guest.gastnr GT 0 USE-INDEX typ-wohn-name_ix NO-LOCK BY guest.NAME:
  CREATE t-guest.
  ASSIGN
    t-guest.gastnr        = guest.gastnr
    t-guest.name          = guest.name
    t-guest.anredefirma   = guest.anredefirma
    t-guest.wohnort       = guest.wohnort
    t-guest.adresse1      = guest.adresse1
    t-guest.vorname1      = guest.vorname1
    t-guest.anrede1       = guest.anrede1
  .
END.
ELSE
FOR EACH guest WHERE guest.name GE curr-name 
  AND guest.karteityp = sorttype 
  AND guest.gastnr GT 0 USE-INDEX typ-wohn-name_ix NO-LOCK BY guest.NAME:
  CREATE t-guest.
  ASSIGN
    t-guest.gastnr        = guest.gastnr
    t-guest.name          = guest.name
    t-guest.anredefirma   = guest.anredefirma
    t-guest.wohnort       = guest.wohnort
    t-guest.adresse1      = guest.adresse1
    t-guest.vorname1      = guest.vorname1
    t-guest.anrede1       = guest.anrede1
  .
END.
