DEFINE TEMP-TABLE t-l-lieferant   LIKE l-lieferant
    FIELD t-recid   AS INT
    FIELD email     AS CHAR FORMAT "x(30)" LABEL "Email".

DEFINE INPUT PARAMETER supply-recid     AS INT  NO-UNDO.
DEFINE OUTPUT PARAMETER segm-bezeich    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-lieferant.

FIND FIRST l-lieferant WHERE RECID(l-lieferant) = supply-recid NO-LOCK NO-ERROR. 
IF AVAILABLE l-lieferant THEN
DO:
    CREATE t-l-lieferant.
    BUFFER-COPY l-lieferant TO t-l-lieferant.

    /* Rulita 110225 | Fixing serverless issue git 535 */
    IF l-lieferant.segment1 NE 0 THEN 
        FIND FIRST l-segment WHERE l-segment.l-segmentcode = l-lieferant.segment1 NO-LOCK NO-ERROR. 
        IF AVAILABLE l-segment THEN segm-bezeich = l-segment.l-bezeich. 
        
    /* End Rulita */
END.


