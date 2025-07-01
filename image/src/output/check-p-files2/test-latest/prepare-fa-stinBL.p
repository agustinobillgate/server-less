DEFINE TEMP-TABLE fa-list LIKE mathis
   FIELD bezeich AS CHAR.
DEFINE TEMP-TABLE lief-list LIKE l-lieferant.

DEFINE INPUT PARAMETER a-bezeich AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER billdate AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR fa-list.
DEFINE OUTPUT PARAMETER TABLE FOR lief-list.

FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 

/*gerald add fa-grup.flag = 0 17544F*/
FOR EACH mathis WHERE mathis.name GE a-bezeich NO-LOCK, 
    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
    AND NOT fa-artikel.posted AND fa-artikel.loeschflag = 0 
    AND fa-artikel.next-depn = ? NO-LOCK, 
    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr
    AND fa-grup.flag = 0 NO-LOCK:
    CREATE fa-list.
    BUFFER-COPY mathis TO fa-list.
    ASSIGN fa-list.bezeich     = fa-grup.bezeich.
END.

FOR EACH l-lieferant NO-LOCK:
    CREATE lief-list.
    BUFFER-COPY l-lieferant TO lief-list.
END.
