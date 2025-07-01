

DEFINE BUFFER ubuff FOR bediener.
DEF TEMP-TABLE output-list
    FIELD docu-nr       LIKE gc-pi.docu-nr
    FIELD u-username    LIKE bediener.username
    FIELD b-username    LIKE bediener.username
    FIELD bezeich       LIKE gc-pitype.bezeich
    FIELD bemerk        LIKE gc-pi.bemerk
    FIELD betrag        LIKE gc-pi.betrag
    FIELD path          LIKE PRINTER.path
    FIELD avail-gc-pitype AS LOGICAL.

DEF TEMP-TABLE t-gc-PIbline LIKE gc-PIbline
    FIELD rec-id AS INT.
    
DEF INPUT PARAM docu-nr    AS CHAR.
DEF INPUT PARAM user-init  AS CHAR.
DEF INPUT PARAM printer-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR t-gc-PIbline.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK.
FIND FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK NO-ERROR.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID NO-LOCK.
FIND FIRST PRINTER WHERE PRINTER.nr = printer-nr NO-LOCK.

CREATE output-list.

IF AVAILABLE gc-pitype THEN
DO:
    ASSIGN output-list.avail-gc-pitype = YES
           output-list.bezeich = gc-pitype.bezeich.
END.

ASSIGN 
    output-list.docu-nr = gc-pi.docu-nr
    output-list.u-username = ubuff.username
    output-list.b-username = bediener.username
    output-list.bemerk = gc-pi.bemerk
    output-list.betrag = gc-pi.betrag
    output-list.path = PRINTER.path.


FOR EACH gc-PIbline WHERE gc-PIbline.docu-nr = gc-pi.docu-nr
    NO-LOCK BY gc-PIbline.created BY gc-PIbline.zeit:
    CREATE t-gc-PIbline.
    BUFFER-COPY gc-PIbline TO t-gc-PIbline.
END.

