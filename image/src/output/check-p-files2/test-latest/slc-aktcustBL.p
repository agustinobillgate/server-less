DEFINE TEMP-TABLE gast
    FIELD gastnr        LIKE guest.gastnr
    FIELD name          LIKE guest.name 
    FIELD vorname1      LIKE guest.vorname1 
    FIELD anrede1       LIKE guest.anrede1
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD adresse       AS CHAR
    FIELD plz           LIKE guest.plz
    FIELD wohnort       LIKE guest.wohnort
    FIELD phonetik3     LIKE guest.phonetik3
    FIELD karteityp     LIKE guest.karteityp.

DEFINE INPUT  PARAMETER gname     AS CHAR NO-UNDO.
DEFINE INPUT  PARAMETER user-init AS CHAR NO-UNDO.
DEFINE INPUT  PARAMETER sorttype  AS INT NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR gast.

IF sorttype EQ 0 THEN   /*FD July 09, 2021 => Amaranta Prambanan, ticket 4CE07E from Dwi S*/
DO:
    FOR EACH guest WHERE guest.name GE gname  
        AND guest.gastnr GT 0 AND guest.karteityp = sorttype NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr EQ guest.gastnr BY guest.NAME:
           
        CREATE gast.
        ASSIGN
            gast.gastnr        = guest.gastnr
            gast.name          = guest.name 
            gast.vorname1      = guest.vorname1 
            gast.anrede1       = guest.anrede1
            gast.anredefirma   = guest.anredefirma
            gast.adresse       = (guest.adresse1 + "," + guest.adresse2 + "," + guest.adresse3)
            gast.plz           = guest.plz
            gast.wohnort       = guest.wohnort
            gast.phonetik3     = guest.phonetik3
            gast.karteityp     = guest.karteityp.
    END.
END.
ELSE
DO:
    FOR EACH guest WHERE guest.name GE gname  
        AND guest.gastnr GT 0 AND guest.phonetik3 = user-init 
        AND guest.karteityp = sorttype NO-LOCK BY guest.NAME:
           
        CREATE gast.
        ASSIGN
            gast.gastnr        = guest.gastnr
            gast.name          = guest.name 
            gast.vorname1      = guest.vorname1 
            gast.anrede1       = guest.anrede1
            gast.anredefirma   = guest.anredefirma
            gast.adresse       = (guest.adresse1 + "," + guest.adresse2 + "," + guest.adresse3)
            gast.plz           = guest.plz
            gast.wohnort       = guest.wohnort
            gast.phonetik3     = guest.phonetik3
            gast.karteityp     = guest.karteityp.
    END.
END.

