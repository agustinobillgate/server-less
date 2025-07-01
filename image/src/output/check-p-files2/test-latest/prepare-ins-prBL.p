DEFINE TEMP-TABLE s-list 
  FIELD pos         AS INTEGER
  FIELD artnr       AS INTEGER 
  FIELD new-created AS LOGICAL INITIAL NO
  FIELD bemerk      AS CHAR FORMAT "x(24)"
. 

DEFINE TEMP-TABLE t-l-orderhdr  
    FIELD docu-nr       LIKE l-orderhdr.docu-nr
    FIELD besteller     LIKE l-orderhdr.besteller
    FIELD angebot-lief  LIKE l-orderhdr.angebot-lief
    FIELD bestelldatum  LIKE l-orderhdr.bestelldatum
    FIELD lieferdatum   LIKE l-orderhdr.lieferdatum
    .

DEFINE TEMP-TABLE ins-list
    FIELD t-recid       AS INT
    FIELD artnr         LIKE l-order.artnr 
    FIELD bezeich       LIKE l-artikel.bezeich 
    FIELD anzahl        LIKE l-order.anzahl 
    FIELD traubensort   LIKE l-artikel.traubensort 
    FIELD txtnr         LIKE l-order.txtnr 
    FIELD lieferdatum   LIKE l-order.lieferdatum 
    FIELD stornogrund   LIKE l-order.stornogrund 
    FIELD bemerk        AS CHAR FORMAT "x(24)"
    FIELD quality       LIKE l-order.quality
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD new-created   AS LOGICAL INIT NO
    FIELD lief-nr       LIKE l-order.lief-nr
    FIELD op-art        LIKE l-order.op-art
    FIELD docu-nr       LIKE l-order.docu-nr
    FIELD bestelldatum  LIKE l-order.bestelldatum
    .
    
DEFINE BUFFER l-art FOR l-artikel. 


DEFINE INPUT PARAMETER docu-nr      AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER billdate    AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER comments    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER deptname    AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER pos         AS INT  NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEFINE OUTPUT PARAMETER TABLE FOR ins-list.    

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr NO-LOCK. 
 
FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
  AND parameters.section = "Name" 
  AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] 
  NO-LOCK NO-ERROR. 
IF AVAILABLE parameters THEN deptname = parameters.vstring. 
 
IF AVAILABLE l-orderhdr THEN
DO: 
    comments = l-orderhdr.lief-fax[3]. 
    CREATE t-l-orderhdr.
    BUFFER-COPY l-orderhdr TO t-l-orderhdr.
END.
 
RUN create-list. 
  
FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.lief-nr = 0 AND l-order.loeschflag LE 1 
    NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK, 
    FIRST s-list WHERE s-list.artnr = l-order.artnr BY s-list.pos DESCENDING. 
    CREATE ins-list.
    ASSIGN  ins-list.t-recid       = RECID(l-order)
            ins-list.artnr         = l-order.artnr 
            ins-list.bezeich       = l-art.bezeich 
            ins-list.anzahl        = l-order.anzahl 
            ins-list.traubensort   = l-art.traubensort 
            ins-list.txtnr         = l-order.txtnr 
            ins-list.lieferdatum   = l-order.lieferdatum 
            ins-list.stornogrund   = l-order.stornogrund 
            ins-list.bemerk        = s-list.bemerk 
            ins-list.quality       = l-order.quality
            ins-list.jahrgang      = l-art.jahrgang
            ins-list.new-created   = s-list.new-created
            ins-list.lief-nr       = l-order.lief-nr
            ins-list.op-art        = l-order.op-art
            ins-list.docu-nr       = l-order.docu-nr
            ins-list.bestelldatum  = l-order.bestelldatum
            .
END.
                                                        
/******************************* PROCEDURES ***********************************/  
PROCEDURE create-list: 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND l-order.pos GT 0 
    AND l-order.lief-nr = 0 AND l-order.loeschflag LE 1 NO-LOCK
    BY l-order.pos: 
    CREATE s-list.
    ASSIGN
      s-list.artnr  = l-order.artnr
      s-list.pos    = l-order.pos
      s-list.bemerk = l-order.besteller
      pos           = l-order.pos
    .
  END. 
END. 

