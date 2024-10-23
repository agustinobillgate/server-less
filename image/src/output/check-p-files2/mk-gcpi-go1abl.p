DEFINE TEMP-TABLE pbuff       LIKE gc-pi.

DEF INPUT PARAMETER TABLE FOR pbuff.
DEF INPUT PARAMETER pi-type     AS CHAR.
DEF INPUT PARAMETER pay-type    AS CHAR.
DEF INPUT PARAMETER pay-acctNo  AS CHAR.
DEF INPUT PARAMETER rcvName     AS CHAR.
DEF INPUT PARAMETER bemerk      AS CHAR.
DEF INPUT PARAMETER pi-number   AS CHAR.

FIND FIRST pbuff.
FIND FIRST gc-pitype WHERE 
  gc-pitype.bezeich = pi-type NO-LOCK.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = pi-number NO-LOCK.
FIND CURRENT gc-PI EXCLUSIVE-LOCK.
BUFFER-COPY pbuff TO gc-PI.
ASSIGN 
  gc-PI.rcvName     = rcvName
  gc-PI.bemerk      = bemerk
  gc-PI.pay-type    = INTEGER(SUBSTR(pay-type,1,1))
  gc-PI.credit-fibu = pay-acctNo
  gc-pi.pi-type     = gc-pitype.nr
.
