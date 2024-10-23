
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF INPUT  PARAMETER ap-recid           AS INT.
DEF OUTPUT PARAMETER from-date          AS DATE.
DEF OUTPUT PARAMETER to-date            AS DATE.
DEF OUTPUT PARAMETER lieferant-recid    AS INT.
DEF OUTPUT PARAMETER l-kredit-recid     AS INT.
DEF OUTPUT PARAMETER from-supp          AS CHAR INIT "".
DEF OUTPUT PARAMETER char1              AS CHAR.
DEF OUTPUT PARAMETER all-supp           AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER long-digit         AS LOGICAL.
DEF OUTPUT PARAMETER show-price         AS LOGICAL.
DEF OUTPUT PARAMETER log1               AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER gst-flag           AS LOGICAL INIT NO.

DEFINE VARIABLE start-endkum            AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    char1 = htparam.fchar. 
    log1  = YES.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

IF ap-recid NE 0 THEN
DO:
  FIND FIRST l-kredit WHERE RECID(l-kredit) = ap-recid NO-LOCK.
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK.
  ASSIGN
    from-date       = l-kredit.rgdatum
    to-date         = l-kredit.rgdatum
    from-supp       = l-lieferant.firma
    from-supp       = from-supp + ";" + l-kredit.NAME
    all-supp        = NO
    lieferant-recid = RECID(l-lieferant)
    l-kredit-recid  = RECID(l-kredit).

  ASSIGN start-endkum = 0.

  FIND FIRST l-op WHERE l-op.datum = l-kredit.rgdatum AND l-op.lief-nr = l-kredit.lief-nr NO-LOCK NO-ERROR.
  IF AVAILABLE l-op THEN DO:
      FOR EACH l-op WHERE l-op.datum = l-kredit.rgdatum AND l-op.lief-nr = l-kredit.lief-nr NO-LOCK,
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK BY l-artikel.endkum :
    
          IF start-endkum = 0 THEN ASSIGN from-supp = from-supp + ";" + STRING(l-artikel.endkum).
          IF l-artikel.endkum GE start-endkum THEN
              ASSIGN start-endkum = l-artikel.endkum.
      END.
  END.
  ELSE DO:
      FOR EACH l-ophis WHERE l-ophis.datum = l-kredit.rgdatum AND l-ophis.lief-nr = l-kredit.lief-nr NO-LOCK,
          FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK BY l-artikel.endkum :
    
          IF start-endkum = 0 THEN ASSIGN from-supp = from-supp + ";" + STRING(l-artikel.endkum).
          IF l-artikel.endkum GE start-endkum THEN
              ASSIGN start-endkum = l-artikel.endkum.
      END.
  END.
  ASSIGN from-supp = from-supp + ";" + STRING(start-endkum) + ";".
  
END.
ELSE
DO:
  RUN htpdate.p(110, OUTPUT from-date).
  ASSIGN to-date = from-date.
END.

/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.
