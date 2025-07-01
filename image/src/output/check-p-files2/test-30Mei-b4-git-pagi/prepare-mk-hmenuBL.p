
DEFINE TEMP-TABLE q1-list
    FIELD artnr     LIKE h-artikel.artnr
    FIELD bezeich   LIKE h-artikel.bezeich.
 
DEFINE TEMP-TABLE q2-list
    FIELD artnr     LIKE h-artikel.artnr
    FIELD bezeich   LIKE h-artikel.bezeich.

DEFINE TEMP-TABLE hmenu-list LIKE h-menu. 
DEFINE TEMP-TABLE menu-list  LIKE h-menu.

DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER h-artnr        AS INT.
DEF INPUT  PARAMETER menu-nr        AS INT.
DEF INPUT  PARAMETER sorttype       AS INT.
DEF INPUT  PARAMETER from-artnr     AS INT.
DEF INPUT  PARAMETER from-bezeich   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR hmenu-list.
DEF OUTPUT PARAMETER TABLE FOR menu-list.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE buffer h-art FOR h-artikel.
DEFINE buffer h-art1 FOR h-artikel.
DEFINE buffer h-art2 FOR h-artikel.

FOR EACH h-artikel WHERE h-artikel.departement = dept 
    AND h-artikel.artart = 0 AND h-artikel.betriebsnr = 0 
    AND h-artikel.artnr NE h-artnr NO-LOCK: 
    create hmenu-list. 
    hmenu-list.artnr = h-artikel.artnr. 
END. 
 
IF menu-nr NE 0 THEN 
FOR EACH h-menu WHERE h-menu.departement = dept AND h-menu.nr = menu-nr NO-LOCK:
    FIND FIRST h-artikel WHERE h-artikel.artnr = h-menu.artnr AND h-artikel.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE h-artikel THEN
    DO:
        create menu-list. 
        menu-list.nr = menu-nr. 
        menu-list.artnr = h-artikel.artnr. 
        FIND FIRST hmenu-list WHERE hmenu-list.artnr = menu-list.artnr NO-ERROR. 
        IF AVAILABLE hmenu-list THEN delete hmenu-list. 
    END.
END.

IF sorttype = 1 THEN 
FOR EACH hmenu-list WHERE hmenu-list.artnr GE from-artnr NO-LOCK:
    FIND FIRST h-art1 WHERE h-art1.departement = dept AND h-art1.artnr = hmenu-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-art1 THEN
    DO:
        CREATE q1-list.
        ASSIGN
        q1-list.artnr     = h-art1.artnr
        q1-list.bezeich   = h-art1.bezeich.
    END.
END.
ELSE 
FOR EACH hmenu-list NO-LOCK:
    FIND FIRST h-art1 WHERE h-art1.departement = dept AND h-art1.artnr = hmenu-list.artnr AND h-art1.bezeich GE from-bezeich NO-LOCK NO-ERROR.
    IF AVAILABLE h-art1 THEN
    DO:
        CREATE q1-list.
        ASSIGN
        q1-list.artnr     = h-art1.artnr
        q1-list.bezeich   = h-art1.bezeich.
    END.
END.

FOR EACH menu-list NO-LOCK:
    FIND FIRST h-art2 WHERE h-art2.departement = dept AND h-art2.artnr = menu-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-art2 THEN
    DO:
        CREATE q2-list.
        ASSIGN
        q2-list.artnr     = h-art2.artnr
        q2-list.bezeich   = h-art2.bezeich.
    END.
END.
