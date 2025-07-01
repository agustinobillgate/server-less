
DEFINE TEMP-TABLE guest1
    FIELD gastnr LIKE guest.gastnr
    FIELD name LIKE guest.name
    FIELD vorname1 LIKE guest.vorname1
    FIELD anrede1 LIKE guest.anrede1
    FIELD nation1 LIKE guest.nation1
    FIELD wohnort LIKE guest.wohnort
    FIELD land LIKE guest.land
    FIELD adresse1 LIKE guest.adresse1
    FIELD telefon LIKE guest.telefon
    FIELD ausweis-nr1 LIKE guest.ausweis-nr1.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER famname AS CHAR.
DEFINE INPUT PARAMETER name1 AS CHAR.
DEFINE INPUT PARAMETER gname AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR guest1.

IF case-type = 1 THEN
FOR EACH guest WHERE (guest.name + guest.vorname1) MATCHES famname 
    AND guest.vorname1 GE name1 
    AND guest.karteityp = 0 
    AND guest.gastnr GT 0 NO-LOCK USE-INDEX typ-wohn-name_ix BY guest.name:
    CREATE guest1.
    ASSIGN 
        guest1.gastnr = guest.gastnr
        guest1.name = guest.name
        guest1.vorname1 = guest.vorname1
        guest1.anrede1 = guest.anrede1
        guest1.nation1 = guest.nation1
        guest1.wohnort = guest.wohnort
        guest1.land = guest.land
        guest1.adresse1 = guest.adresse1
        guest1.telefon = guest.telefon
        guest1.ausweis-nr1 = guest.ausweis-nr1.
END.
ELSE IF case-type = 2 THEN
FOR EACH guest WHERE guest.name EQ gname 
    AND guest.vorname1 GE name1 
    AND guest.karteityp = 0 
    AND guest.gastnr GT 0 NO-LOCK USE-INDEX ganame_index BY guest.name:
    CREATE guest1.
    ASSIGN 
        guest1.gastnr = guest.gastnr
        guest1.name = guest.name
        guest1.vorname1 = guest.vorname1
        guest1.anrede1 = guest.anrede1
        guest1.nation1 = guest.nation1
        guest1.wohnort = guest.wohnort
        guest1.land = guest.land
        guest1.adresse1 = guest.adresse1
        guest1.telefon = guest.telefon
        guest1.ausweis-nr1 = guest.ausweis-nr1.
END.
ELSE IF case-type = 3 THEN
FOR EACH guest WHERE guest.NAME EQ gname 
    AND guest.vorname1 EQ name1
    AND guest.karteityp = 0 
    AND guest.gastnr GT 0 NO-LOCK USE-INDEX typ-wohn-name_ix BY guest.name:
    CREATE guest1.
    ASSIGN 
        guest1.gastnr = guest.gastnr
        guest1.name = guest.name
        guest1.vorname1 = guest.vorname1
        guest1.anrede1 = guest.anrede1
        guest1.nation1 = guest.nation1
        guest1.wohnort = guest.wohnort
        guest1.land = guest.land
        guest1.adresse1 = guest.adresse1
        guest1.telefon = guest.telefon
        guest1.ausweis-nr1 = guest.ausweis-nr1.
END.
