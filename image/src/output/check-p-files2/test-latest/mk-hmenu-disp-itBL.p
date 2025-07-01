DEFINE TEMP-TABLE q1-list
    FIELD artnr     LIKE h-artikel.artnr
    FIELD bezeich   LIKE h-artikel.bezeich.
 
DEFINE TEMP-TABLE q2-list
    FIELD artnr     LIKE h-artikel.artnr
    FIELD bezeich   LIKE h-artikel.bezeich.

DEFINE TEMP-TABLE hmenu-list LIKE h-menu. 
DEFINE TEMP-TABLE menu-list  LIKE h-menu.

DEF INPUT-OUTPUT PARAMETER TABLE FOR hmenu-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR menu-list.
DEF INPUT  PARAMETER sorttype       AS INT.
DEF INPUT  PARAMETER dept           AS INT.
DEF INPUT  PARAMETER from-artnr     AS INT.
DEF INPUT  PARAMETER from-bezeich   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE buffer h-art1 FOR h-artikel.
DEFINE buffer h-art2 FOR h-artikel.

IF sorttype = 1 THEN 
FOR EACH hmenu-list 
    WHERE hmenu-list.artnr GE from-artnr, 
    FIRST h-art1 WHERE h-art1.departement = dept 
    AND h-art1.artnr = hmenu-list.artnr NO-LOCK BY hmenu-list.artnr:
    CREATE q1-list.
    ASSIGN
    q1-list.artnr     = h-art1.artnr
    q1-list.bezeich   = h-art1.bezeich.
END.
ELSE 
FOR EACH hmenu-list, 
    FIRST h-art1 WHERE h-art1.departement = dept 
    AND h-art1.artnr = hmenu-list.artnr 
    AND h-art1.bezeich GE from-bezeich NO-LOCK BY h-art1.bezeich:
    CREATE q1-list.
    ASSIGN
    q1-list.artnr     = h-art1.artnr
    q1-list.bezeich   = h-art1.bezeich.
END.

FOR EACH menu-list NO-LOCK, 
    FIRST h-art2 WHERE h-art2.departement = dept 
    AND h-art2.artnr = menu-list.artnr NO-LOCK 
    BY h-art2.zwkum BY menu-list.artnr:
    CREATE q2-list.
    ASSIGN
    q2-list.artnr     = h-art2.artnr
    q2-list.bezeich   = h-art2.bezeich.
END.
