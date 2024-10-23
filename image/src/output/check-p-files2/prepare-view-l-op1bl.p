
DEFINE buffer sys-user FOR bediener. 
DEFINE TEMP-TABLE q1-list
    FIELD datum         LIKE l-op.datum
    FIELD lager-nr      LIKE l-op.lager-nr
    FIELD artnr         LIKE l-op.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD anzahl        LIKE l-op.anzahl
    FIELD einzelpreis   LIKE l-op.einzelpreis
    FIELD warenwert     LIKE l-op.warenwert
    FIELD lscheinnr     LIKE l-op.lscheinnr
    FIELD username      LIKE sys-user.username
    FIELD zeit          LIKE l-op.zeit
    FIELD stornogrund   LIKE l-op.stornogrund
    FIELD pos           LIKE l-op.pos.

DEFINE TEMP-TABLE q11-list
    FIELD datum         LIKE l-op.datum
    FIELD lager-nr      LIKE l-op.lager-nr
    FIELD artnr         LIKE l-op.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD anzahl        LIKE l-op.anzahl
    FIELD lscheinnr     LIKE l-op.lscheinnr
    FIELD username      LIKE sys-user.username
    FIELD zeit          LIKE l-op.zeit
    FIELD stornogrund   LIKE l-op.stornogrund
    FIELD pos           LIKE l-op.pos.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR q11-list.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 


IF show-price THEN 
DO: 
  FOR EACH l-op WHERE l-op.docu-nr = docu-nr 
      AND l-op.pos GT 0 AND l-op.loeschflag = 0 
      AND l-op.op-art = 1 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
      FIRST sys-user WHERE sys-user.nr = l-op.fuellflag 
      NO-LOCK BY l-op.lscheinnr BY l-op.pos:
      CREATE q1-list.
      ASSIGN
          q1-list.datum         = l-op.datum
          q1-list.lager-nr      = l-op.lager-nr
          q1-list.artnr         = l-op.artnr
          q1-list.bezeich       = l-artikel.bezeich
          q1-list.anzahl        = l-op.anzahl
          q1-list.einzelpreis   = l-op.einzelpreis
          q1-list.warenwert     = l-op.warenwert
          q1-list.lscheinnr     = l-op.lscheinnr
          q1-list.username      = sys-user.username
          q1-list.zeit          = l-op.zeit
          q1-list.stornogrund   = l-op.stornogrund
          q1-list.pos           = l-op.pos.
  END.
END. 
ELSE 
DO: 
  FOR EACH l-op WHERE l-op.docu-nr = docu-nr 
      AND l-op.pos GT 0 AND l-op.loeschflag = 0 
      AND l-op.op-art = 1 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
      FIRST sys-user WHERE sys-user.nr = l-op.fuellflag 
      NO-LOCK BY l-op.lscheinnr BY l-op.pos:
      CREATE q11-list.
      ASSIGN
          q11-list.datum         = l-op.datum
          q11-list.lager-nr      = l-op.lager-nr
          q11-list.artnr         = l-op.artnr
          q11-list.bezeich       = l-artikel.bezeich
          q11-list.anzahl        = l-op.anzahl
          q11-list.lscheinnr     = l-op.lscheinnr
          q11-list.username      = sys-user.username
          q11-list.zeit          = l-op.zeit
          q11-list.stornogrund   = l-op.stornogrund
          q11-list.pos           = l-op.pos.
  END.
END. 
