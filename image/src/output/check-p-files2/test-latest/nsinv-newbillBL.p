DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid              AS INTEGER
.

DEFINE INPUT PARAMETER gastnr     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER curr-dept  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER transdate  AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER user-init  AS CHAR     NO-UNDO.

DEFINE OUTPUT PARAMETER gname     AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.

DEFINE VARIABLE dept AS CHARACTER FORMAT "X(20)". /*william add department 6DBA24*/

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK. /*william add department 6DBA24*/

CREATE bill.     
IF transdate NE ? THEN bill.datum = transdate. 
ELSE bill.datum = htparam.fdate. 

ASSIGN
    bill.gastnr     = gastnr
    bill.billtyp    = curr-dept
    bill.name       = guest.name + ", " + guest.vorname1 
                    + guest.anredefirma
    bill.bilname    = bill.NAME
    bill.reslinnr   = 1
    bill.rgdruck    = 1 
    gname           = bill.name
    dept            = hoteldpt.depart /*william add department 6DBA24*/
. 
FIND CURRENT bill NO-LOCK. 

CREATE t-bill.
BUFFER-COPY bill TO t-bill.
ASSIGN t-bill.bl-recid = INTEGER(RECID(bill)).

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
CREATE res-history.
ASSIGN
  res-history.nr      = bediener.nr
  res-history.datum   = TODAY
  res-history.zeit    = TIME
  res-history.action  = "Nonstay Bill"
  res-history.aenderung  = "Create new non stay bill, Department : " + dept + " BillNo : " + STRING(bill.rechnr) + " BillName : " + gname. /*william add department 6DBA24*/
.
FIND CURRENT res-history NO-LOCK.
