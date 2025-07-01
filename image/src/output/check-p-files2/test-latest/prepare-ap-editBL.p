
DEF TEMP-TABLE t-l-kredit LIKE l-kredit.

DEF INPUT  PARAMETER recid-ap AS INT.
DEF OUTPUT PARAMETER firma LIKE l-lieferant.firma.
DEF OUTPUT PARAMETER lief-nr LIKE l-lieferant.lief-nr.
DEF OUTPUT PARAMETER TABLE FOR t-l-kredit.

/* Rulita 110225 | Fixing serverless If Available issue git 530 */
FIND FIRST l-kredit WHERE RECID(l-kredit) = recid-ap NO-LOCK NO-ERROR. 
IF AVAILABLE l-kredit THEN
DO:
    CREATE t-l-kredit.
    BUFFER-COPY l-kredit TO t-l-kredit.
    
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-lieferant THEN
    DO:
        firma = l-lieferant.firma.
        lief-nr = l-lieferant.lief-nr.
    END.
END.
/* End Rulita */

