DEFINE TEMP-TABLE supply-list   LIKE l-lieferant
    FIELD t-recid           AS INT.

DEFINE OUTPUT PARAMETER param992        AS LOGICAL  NO-UNDO.
DEFINE OUTPUT PARAMETER comments        AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER first-liefnr    AS INT      NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER curr-firma      AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER TABLE FOR supply-list.

DEFINE VARIABLE counter         AS INT  NO-UNDO INIT 0.

FOR EACH l-lieferant WHERE l-lieferant.lief-nr GT 0 AND 
    l-lieferant.firma NE "" /*AND 
    l-lieferant.anredefirma GE ""*/ NO-LOCK BY l-lieferant.firma. 
     /*counter = counter + 1.
   IF counter = 1 THEN first-liefnr = l-lieferant.lief-nr.
    IF (counter GE 30) AND (curr-firma NE l-lieferant.firma) THEN LEAVE.*/
    CREATE supply-list.
    BUFFER-COPY l-lieferant TO supply-list.
    ASSIGN supply-list.t-recid = RECID(l-lieferant)
           curr-firma = l-lieferant.firma
           comments = l-lieferant.notizen[1].
END.   

FIND FIRST htparam WHERE paramnr = 992 NO-LOCK. 
param992 = htparam.flogical.
