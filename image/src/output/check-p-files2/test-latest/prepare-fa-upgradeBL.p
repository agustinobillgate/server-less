
DEFINE TEMP-TABLE gl-jouhdr1  LIKE gl-jouhdr. 

DEFINE INPUT PARAMETER p-nr         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER nr           AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER name-mathis AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER asset-no    AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER last-close  AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER datum       AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER amt         AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR gl-jouhdr1.


FIND FIRST htparam WHERE paramnr = 558 NO-LOCK NO-ERROR. /* LAST Accounting Period */ 
/* ASSIGN last-close = fdate. */       /* Rulita 211024 | Fixing for serverless */
ASSIGN last-close = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 372 NO-LOCK NO-ERROR.   /* journal posting DATE */ 
ASSIGN datum = htparam.fdate.           /* Rulita 211024 | Fixing for serverless */
 
FIND FIRST fa-artikel WHERE fa-artikel.nr = p-nr NO-LOCK NO-ERROR. 
ASSIGN amt = fa-artikel.warenwert. 
 
FIND FIRST mathis WHERE mathis.nr = nr NO-LOCK NO-ERROR.
ASSIGN name-mathis = mathis.NAME
       asset-no    = mathis.asset.


FOR EACH gl-jouhdr NO-LOCK:
    CREATE gl-jouhdr1.
    BUFFER-COPY gl-jouhdr TO gl-jouhdr1.
END.
