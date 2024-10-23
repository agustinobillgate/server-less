
DEF INPUT  PARAM user-init          AS CHAR             NO-UNDO.
DEF OUTPUT PARAM telop-sensitive    AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM setting-sensitive  AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM condotel-sensitive AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM club-sensitive     AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM eng-sensitive      AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM repgen-sensitive   AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM wo-sensitive       AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM new-contrate       AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAM ci-date            AS DATE             NO-UNDO.
DEF OUTPUT PARAM hpname-training    AS CHAR    INIT ""  NO-UNDO.
DEF OUTPUT PARAM aktlist-flag       AS LOGICAL INIT NO  NO-UNDO.
DEF OUTPUT PARAM dynarate-flag      AS LOGICAL INIT YES NO-UNDO.

DEF OUTPUT PARAM htl-city           AS CHAR INIT ""    NO-UNDO.
DEF OUTPUT PARAM curr-htl-city      AS CHAR INIT ""    NO-UNDO.

DEF OUTPUT PARAM p-1072             AS LOGICAL.
DEF OUTPUT PARAM p-244              AS CHAR.
DEF OUTPUT PARAM p-975              AS INT.
DEF OUTPUT PARAM p-996              AS LOGICAL.
DEF OUTPUT PARAM p-1002             AS LOGICAL.
DEF OUTPUT PARAM p-997              AS LOGICAL.
DEF OUTPUT PARAM p-988              AS LOGICAL.
DEF OUTPUT PARAM p-992              AS LOGICAL.
DEF OUTPUT PARAM p-1016             AS LOGICAL.
DEF OUTPUT PARAM p-868              AS CHAR.
DEF OUTPUT PARAM p-990              AS LOGICAL.
DEF OUTPUT PARAM p-1015             AS LOGICAL.
DEF OUTPUT PARAM p-169              AS CHAR.
DEF OUTPUT PARAM p-991              AS LOGICAL.
DEF OUTPUT PARAM p-2000             AS LOGICAL.
DEF OUTPUT PARAM p-329              AS LOGICAL.
DEF OUTPUT PARAM p-985              AS LOGICAL.

DEF VARIABLE golf-license           AS LOGICAL NO-UNDO INIT NO.

FIND FIRST paramtext WHERE txtnr = 204 NO-ERROR. 
curr-htl-city = paramtext.ptexte.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK NO-ERROR.
dynarate-flag = AVAILABLE queasy.

FIND FIRST htparam WHERE htparam.paramnr = 6001 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND NOT htparam.flogical
  THEN telop-sensitive = NO.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 169 NO-LOCK. 
hpname-training = vhp.htparam.fchar.

FIND FIRST htparam WHERE paramnr = 999 NO-LOCK. 
IF htparam.flogical THEN setting-sensitive = NO. 
 
FIND FIRST htparam WHERE paramnr = 981 NO-LOCK. 
IF NOT htparam.flogical THEN condotel-sensitive = NO. 
 
FIND FIRST htparam WHERE paramnr = 1114 NO-LOCK. 
IF NOT htparam.flogical THEN club-sensitive = NO. 
 
FIND FIRST htparam WHERE paramnr = 319 NO-LOCK. 
IF NOT htparam.flogical OR htparam.paramgr NE 99 
  THEN eng-sensitive = NO. 

FIND FIRST htparam WHERE paramnr = 1072 NO-LOCK. 
IF NOT htparam.flogical OR htparam.paramgr NE 99
  THEN repgen-sensitive = NO. 

FIND FIRST queasy WHERE queasy.KEY = 28 NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN wo-sensitive = FALSE.

FIND FIRST htparam WHERE htparam.paramnr = 1002 NO-LOCK. /* sales Lic */
IF htparam.flogical THEN
DO:
  FIND FIRST akt-line WHERE akt-line.userinit = user-init
    AND akt-line.datum GE (ci-date - 1) AND akt-line.datum LE ci-date
    NO-LOCK NO-ERROR.
  aktlist-flag = AVAILABLE akt-line. 
END. 

FIND FIRST paramtext WHERE paramtext.txtnr GE 203.
htl-city = paramtext.ptexte.

RUN htplogic.p (1072, OUTPUT p-1072).

/* SY 14 SEPT 2015 */
RUN htpchar.p  (244,  OUTPUT p-244).
FIND FIRST htparam WHERE htparam.paramnr = 299 NO-LOCK.
IF htparam.paramgr = 99 AND htparam.flogical THEN
     p-244 = p-244 + CHR(2) + "YES".
ELSE p-244 = p-244 + CHR(2) + "NO". 

RUN htpint.p   (975,  OUTPUT p-975).
RUN htplogic.p (996,  OUTPUT p-996).
RUN htplogic.p (1002, OUTPUT p-1002).
RUN htplogic.p (997,  OUTPUT p-997).
RUN htplogic.p (988,  OUTPUT p-988).
RUN htplogic.p (992,  OUTPUT p-992).
RUN htplogic.p (1016, OUTPUT p-1016).
RUN htpchar.p  (868,  OUTPUT p-868).
RUN htplogic.p (990,  OUTPUT p-990).
RUN htplogic.p (1015, OUTPUT p-1015). /* VHP Lite */
RUN htpchar.p  (169,  OUTPUT p-169).
RUN htplogic.p (991,  OUTPUT p-991).
RUN htplogic.p (2000, OUTPUT p-2000).
RUN htplogic.p (329,  OUTPUT p-329).
RUN htplogic.p (985,  OUTPUT p-985).
