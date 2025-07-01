/*MESSAGE "a1"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
DEFINE TEMP-TABLE t-parameters LIKE parameters.
DEFINE TEMP-TABLE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD traubensort   LIKE l-artikel.traubensorte
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell
    FIELD min-bestand   LIKE l-artikel.min-bestand
    FIELD anzverbrauch  LIKE l-artikel.anzverbrauch.

DEF OUTPUT PARAMETER billdate       AS DATE. 
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR cost-list.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

RUN create-costlist.
RUN check-appr.
FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" NO-LOCK:
    CREATE t-parameters.
    BUFFER-COPY parameters TO t-parameters.
END.

FOR EACH l-artikel:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.traubensort   = l-artikel.traubensorte /* Malik Serverless 528 l-artikel.traubensort -> l-artikel.traubensorte */
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.jahrgang      = l-artikel.jahrgang
    t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
    t-l-artikel.min-bestand   = l-artikel.min-bestand
    t-l-artikel.anzverbrauch  = l-artikel.anzverbrauch.
END.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.nr = INTEGER(parameters.varname). 
    cost-list.bezeich = parameters.vstring. 
  END. 
END. 
 
PROCEDURE check-appr:
DEF VARIABLE approve-str AS CHAR NO-UNDO.
DEF BUFFER   lbuff       FOR l-orderhdr.
    FOR EACH l-orderhdr NO-LOCK :
        /* IF lief-fax[2] MATCHES "*;*" THEN . */
        IF l-orderhdr.lief-fax[2] MATCHES "*;*" THEN .      /* Rulita 181024 | Fixing for serverless */
        ELSE
        DO TRANSACTION:
            FIND FIRST lbuff WHERE RECID(lbuff) = RECID(l-orderhdr)
                EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
            IF AVAILABLE lbuff THEN
            DO:
              ASSIGN approve-str = lbuff.lief-fax[2].
              IF lbuff.lief-fax[2] EQ "" THEN
                ASSIGN lbuff.lief-fax[2] = " ; ; ; ".
              ELSE 
                ASSIGN lbuff.lief-fax[2] = approve-str + ";" 
                    + approve-str + ";" + approve-str + ";" + approve-str. 
              FIND CURRENT lbuff NO-LOCK.
            END.
        END.
    END.
END PROCEDURE.


