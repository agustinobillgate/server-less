DEFINE TEMP-TABLE t-h-menu LIKE h-menu
    FIELD art-desc AS CHARACTER.

DEFINE INPUT PARAMETER article-no   AS INTEGER.
DEFINE INPUT PARAMETER dept-no      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-menu.

DEFINE BUFFER buff-hart FOR h-artikel.

FIND FIRST h-artikel WHERE h-artikel.artnr EQ article-no
    AND h-artikel.departement EQ dept-no NO-LOCK NO-ERROR.
IF AVAILABLE h-artikel THEN
DO:
    FOR EACH h-menu WHERE h-menu.nr EQ h-artikel.betriebsnr
        AND h-menu.departement EQ h-artikel.departement,
        FIRST buff-hart WHERE buff-hart.artnr EQ h-menu.artnr
        AND buff-hart.departement EQ h-menu.departement NO-LOCK:

        CREATE t-h-menu.
        BUFFER-COPY h-menu TO t-h-menu.
        t-h-menu.art-desc = buff-hart.bezeich.
    END.
END.
