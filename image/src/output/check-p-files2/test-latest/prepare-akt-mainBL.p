
DEFINE TEMP-TABLE q1-list
    FIELD name          LIKE guest.name
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD anrede1       LIKE guest.anrede1
    FIELD firmen-nr     LIKE guest.firmen-nr
    FIELD adresse1      LIKE guest.adresse1
    FIELD plz           LIKE guest.plz
    FIELD wohnort       LIKE guest.wohnort
    FIELD telefon       LIKE guest.telefon
    FIELD fax           LIKE guest.fax
    FIELD rabatt        LIKE guest.rabatt
    FIELD endperiode    LIKE guest.endperiode
    FIELD namekontakt   LIKE guest.namekontakt
    FIELD gastnr        LIKE akt-cust.gastnr
    FIELD userinit      LIKE akt-cust.userinit
    FIELD datum         LIKE akt-cust.datum
    FIELD c-init        LIKE akt-cust.c-init
    FIELD rec-id        AS INT.

DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER lname AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH akt-cust WHERE akt-cust.userinit = user-init NO-LOCK, 
    FIRST guest WHERE guest.gastnr = akt-cust.gastnr 
    AND guest.phonetik3 = akt-cust.userinit AND guest.NAME GE lname 
    AND guest.gastnr GT 0 NO-LOCK BY guest.NAME:
    CREATE q1-list.
    ASSIGN
        q1-list.name          = guest.name
        q1-list.anredefirma   = guest.anredefirma
        q1-list.anrede1       = guest.anrede1
        q1-list.firmen-nr     = guest.firmen-nr
        q1-list.adresse1      = guest.adresse1
        q1-list.plz           = guest.plz
        q1-list.wohnort       = guest.wohnort
        q1-list.telefon       = guest.telefon
        q1-list.fax           = guest.fax
        q1-list.rabatt        = guest.rabatt
        q1-list.endperiode    = guest.endperiode
        q1-list.namekontakt   = guest.namekontakt
        q1-list.gastnr        = akt-cust.gastnr
        q1-list.userinit      = akt-cust.userinit
        q1-list.datum         = akt-cust.datum
        q1-list.c-init        = akt-cust.c-init
        q1-list.rec-id        = RECID(akt-cust).
END.
