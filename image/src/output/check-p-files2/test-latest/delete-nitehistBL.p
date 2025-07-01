
DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER datum1    AS DATE.
DEFINE INPUT PARAMETER int1      AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL.

DEFINE VARIABLE billdate    AS DATE. 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH nitehist WHERE nitehist.datum = datum1
            AND nitehist.reihenfolge = int1 :
            DELETE nitehist.
            RELEASE nitehist.
            success-flag = YES.
        END.
        FOR EACH nitestor WHERE nitestor.reihenfolge = int1 NO-LOCK: 
            CREATE vhp.nitehist. 
            ASSIGN  vhp.nitehist.datum = /*datum1*/ billdate
                    vhp.nitehist.reihenfolge = nitestor.reihenfolge 
                    vhp.nitehist.line = nitestor.line  
                    vhp.nitehist.line-nr = nitestor.line-nr. 
        END.
    END.
END CASE.


