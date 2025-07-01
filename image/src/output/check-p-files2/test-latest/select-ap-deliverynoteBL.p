
DEFINE TEMP-TABLE b1-list
    FIELD rgdatum   LIKE l-kredit.rgdatum
    FIELD NAME      LIKE l-kredit.NAME
    FIELD lscheinnr LIKE l-kredit.lscheinnr
    FIELD saldo     LIKE l-kredit.saldo
    FIELD opart     LIKE l-kredit.opart.

DEF INPUT  PARAMETER lief-nr     AS INT.
DEF INPUT  PARAMETER from-date   AS DATE.
DEF INPUT  PARAMETER to-date     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

FOR EACH l-kredit WHERE l-kredit.lief-nr = lief-nr
    AND l-kredit.zahlkonto = 0
    AND l-kredit.rgdatum GE from-date
    AND l-kredit.rgdatum LE to-date NO-LOCK
    BY l-kredit.rgdatum BY l-kredit.NAME:
    CREATE b1-list.
    ASSIGN
      b1-list.rgdatum   = l-kredit.rgdatum
      b1-list.NAME      = l-kredit.NAME
      b1-list.lscheinnr = l-kredit.lscheinnr
      b1-list.saldo     = l-kredit.saldo
      b1-list.opart     = l-kredit.opart.
END.
