DEFINE TEMP-TABLE aktcustlist
    FIELD name          LIKE guest.name 
    FIELD gastnr        LIKE guest.gastnr
    FIELD anrede1       LIKE guest.anrede1
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD adresse1      LIKE guest.adresse1 
    FIELD plz           LIKE guest.plz
    FIELD wohnort       LIKE guest.wohnort.



DEFINE OUTPUT PARAMETER TABLE FOR aktcustlist.


FOR EACH akt-cust WHERE akt-cust.userinit = userinit NO-LOCK, 
    FIRST guest WHERE guest.gastnr = akt-cust.gastnr NO-LOCK BY guest.NAME:
    CREATE aktcustlist.
    ASSIGN
        aktcustlist.name          = guest.name 
        aktcustlist.gastnr        = guest.gastnr
        aktcustlist.anrede1       = guest.anrede1
        aktcustlist.anredefirma   = guest.anredefirma
        aktcustlist.adresse1      = guest.adresse1 
        aktcustlist.plz           = guest.plz
        aktcustlist.wohnort       = guest.wohnort.
END.
