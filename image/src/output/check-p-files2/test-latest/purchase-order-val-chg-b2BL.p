
DEFINE TEMP-TABLE q1-list
    FIELD rec-id-l-order    AS INT
    FIELD lief-nr           AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD docu-nr           AS CHARACTER    FORMAT "x(16)"
    FIELD pos               AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD artnr             AS INTEGER      FORMAT ">>>>>>9"
    FIELD bezeich           AS CHARACTER    FORMAT "x(36)"
    FIELD anzahl            AS DECIMAL      FORMAT "->>>,>>9.999"
    FIELD geliefert         AS DECIMAL      FORMAT "->>>,>>9.999"
    FIELD angebot-lief-1    AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD rechnungswert     AS DECIMAL      FORMAT "->,>>>,>>9.999"
    FIELD lief-fax-3        AS CHARACTER    FORMAT "x(15)"
    FIELD txtnr             AS INTEGER      FORMAT ">>9"
    FIELD lieferdatum-eff   AS DATE         FORMAT "99/99/99"
    FIELD einzelpreis       AS DECIMAL      FORMAT "->>,>>9.999"
    FIELD lief-fax-2        AS CHARACTER    FORMAT "x(15)".

DEF INPUT PARAMETER q2-list-docu-nr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH l-order WHERE l-order.docu-nr = q2-list-docu-nr
    AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK BY l-order.pos:
    CREATE q1-list.
    ASSIGN
      q1-list.rec-id-l-order    = RECID(l-order)
      q1-list.lief-nr           = l-order.lief-nr
      q1-list.docu-nr           = l-order.docu-nr
      q1-list.pos               = l-order.pos
      q1-list.artnr             = l-order.artnr
      q1-list.bezeich           = l-art.bezeich
      q1-list.anzahl            = l-order.anzahl
      q1-list.geliefert         = l-order.geliefert
      q1-list.angebot-lief-1    = l-order.angebot-lief[1]
      q1-list.rechnungswert     = l-order.rechnungswert
      q1-list.lief-fax-3        = l-order.lief-fax[3]
      q1-list.txtnr             = l-order.txtnr
      q1-list.lieferdatum-eff   = l-order.lieferdatum-eff
      q1-list.einzelpreis       = l-order.einzelpreis
      q1-list.lief-fax-2        = l-order.lief-fax[2].
END.
