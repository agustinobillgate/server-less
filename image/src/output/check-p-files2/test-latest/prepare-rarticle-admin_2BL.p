
DEFINE TEMP-TABLE wbuff 
    FIELD departement AS INTEGER
    FIELD zknr AS INTEGER
    FIELD bez  LIKE wgrpdep.bezeich.

DEFINE TEMP-TABLE q1-list LIKE h-artikel
    FIELD bez           LIKE wbuff.bez
    FIELD zknr          LIKE wbuff.zknr
    
    FIELD bezeich2      LIKE queasy.char3
    FIELD zk-bezeich    LIKE wgrpdep.bezeich
    FIELD ek-bezeich    LIKE wgrpdep.bezeich
    FIELD fart-bezeich  LIKE artikel.bezeich
    FIELD fo-dept       AS INT
    FIELD barcode       AS CHAR.

DEF INPUT  PARAMETER dept       AS INT.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER d-bezeich  AS CHAR.
DEF OUTPUT PARAMETER only-corp-access AS LOGICAL. /*FDL July 12, 2023 => Ticket 637C7D*/
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 1204 NO-LOCK.  
only-corp-access = htparam.flogical. 

FOR EACH wgrpdep WHERE wgrpdep.departement = dept NO-LOCK:
    CREATE wbuff.
    ASSIGN
        wbuff.departement = dept
        wbuff.zknr        = wgrpdep.zknr
        wbuff.bez         = wgrpdep.bezeich
    .
END.

FIND FIRST hoteldpt WHERE hoteldpt.num = dept NO-LOCK. 
d-bezeich = hoteldpt.depart.

FOR EACH h-artikel WHERE h-artikel.departement = dept NO-LOCK, 
    FIRST wbuff WHERE wbuff.zknr = h-artikel.zwkum
    AND wbuff.departement = h-artikel.departement NO-LOCK
    BY h-artikel.activeflag DESCENDING BY h-artikel.artnr:
    CREATE q1-list.
    BUFFER-COPY h-artikel TO q1-list.
    ASSIGN q1-list.bez = wbuff.bez
           q1-list.zknr = wbuff.zknr.


    FIND FIRST queasy WHERE queasy.key = 38 
        AND queasy.number1 = h-artikel.departement
        AND queasy.number2 = h-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN q1-list.bezeich2 = queasy.char3.

    FIND FIRST wgrpdep WHERE wgrpdep.zknr = h-artikel.zwkum 
        AND wgrpdep.departement = dept NO-LOCK NO-ERROR. 
    IF AVAILABLE wgrpdep THEN q1-list.zk-bezeich = wgrpdep.bezeich.
    ELSE q1-list.zk-bezeich = "?????". 

    FIND FIRST wgrpgen WHERE wgrpgen.eknr = h-artikel.endkum NO-LOCK NO-ERROR. 
    IF AVAILABLE wgrpgen THEN q1-list.ek-bezeich = wgrpgen.bezeich. 
    ELSE q1-list.ek-bezeich = "?????". 

    IF h-artikel.artart LE 1 THEN q1-list.fo-dept = dept. 
    ELSE q1-list.fo-dept = 0. 

    FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
        AND artikel.departement = q1-list.fo-dept NO-LOCK NO-ERROR. /* Malik Serverelss : fo-dept -> q1-list.fo-dept */
    IF AVAILABLE artikel THEN q1-list.fart-bezeich = artikel.bezeich. 
    ELSE q1-list.fart-bezeich = "????????". 

    FIND FIRST queasy WHERE queasy.key = 200
        AND queasy.number1 = h-artikel.departement
        AND queasy.number2 = h-artikel.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN q1-list.barcode = queasy.char1.
END.
