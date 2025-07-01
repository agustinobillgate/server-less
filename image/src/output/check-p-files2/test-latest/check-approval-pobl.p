/*CURRENT-WINDOW:WIDTH = 200. */
DEFINE TEMP-TABLE po-list
    FIELD lief-nr       AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD docu-nr       AS CHARACTER    FORMAT "x(16)"
    FIELD bestelldatum  AS DATE         FORMAT "99/99/99"
    FIELD lieferdatum   AS DATE         FORMAT "99/99/99"
    FIELD wabkurz       AS CHARACTER    FORMAT "x(4)"
    FIELD bestellart    AS CHARACTER    FORMAT "x(10)"
    FIELD gedruckt      AS DATE         FORMAT "99/99/99"
    FIELD besteller     AS CHARACTER    FORMAT "x(24)"
    FIELD lief-fax-3    AS CHARACTER    FORMAT "x(15)"
    FIELD lief-fax-2    AS CHARACTER    FORMAT "x(15)"
    FIELD rechnungswert AS DECIMAL      FORMAT "->,>>>,>>9.999"
    FIELD rec-id        AS INT
    FIELD approval-lvl  AS LOGICAL EXTENT 4 INIT NO
    FIELD approval-id   AS CHAR EXTENT 4
    FIELD need-approval AS CHAR.

DEFINE TEMP-TABLE q245
    FIELD KEY       AS INTEGER
    FIELD docu-nr   AS CHARACTER
    FIELD user-init AS CHARACTER
    FIELD app-id    AS CHARACTER
    FIELD app-no    AS INTEGER
    FIELD sign-id   AS INTEGER FORMAT "->>>>>>>>>>".

DEFINE TEMP-TABLE mess-list 
  FIELD nr          AS INTEGER LABEL "No" 
  FIELD reslinnr    AS INTEGER 
  FIELD betriebsnr  AS INTEGER 
  FIELD mess-recid  AS INTEGER 
  FIELD datum       AS DATE LABEL "Date" INITIAL ? 
  FIELD mess-str    AS CHAR FORMAT "x(80)" LABEL "Message Text". 
 
DEFINE TEMP-TABLE qsy-list
    FIELD docu-nr AS CHAR.


DEFINE INPUT PARAMETER user-init AS CHAR.
/*
DEFINE VARIABLE user-init AS CHAR INIT "01".
*/
DEFINE VARIABLE nr        AS INT.
DEFINE VARIABLE loop-init AS INT.
DEFINE VARIABLE do-alert  AS LOGICAL INIT NO.
DEFINE VARIABLE app-lvl   AS INT.
DEFINE VARIABLE use-po-esignature AS LOGICAL INIT NO.
DEFINE VARIABLE billdate  AS DATE NO-UNDO.

DEF VAR a AS CHAR.
DEF VAR b AS CHAR.
DEF VAR c AS CHAR.
DEF VAR d AS CHAR.

DEFINE BUFFER bmessage FOR messages.

RUN htplogic.p (71, OUTPUT use-po-esignature).

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
billdate = htparam.fdate.

a = STRING(TIME,"HH:MM:SS").
/*MESSAGE "start a: " a
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
FIND FIRST l-orderhdr WHERE l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK NO-ERROR.
DO WHILE AVAILABLE l-orderhdr:
    FIND FIRST queasy WHERE queasy.KEY EQ 245 
        AND queasy.char1 EQ l-orderhdr.docu-nr
        AND queasy.number1 GE 1 
        AND queasy.number1 LT 4 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:

        FIND FIRST qsy-list WHERE TRIM(qsy-list.docu-nr) EQ TRIM(queasy.char1) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE qsy-list THEN
        DO:
            CREATE qsy-list.
            ASSIGN qsy-list.docu-nr = queasy.char1.
    
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            FIND FIRST messages WHERE messages.zinr EQ qsy-list.docu-nr AND messages.gastnr EQ bediener.nr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE messages THEN DO:
                DELETE messages.
            END.
        END.

        FIND NEXT queasy WHERE queasy.KEY EQ 245 
        AND queasy.char1 EQ l-orderhdr.docu-nr
        AND queasy.number1 GE 1 
        AND queasy.number1 LT 4 NO-LOCK NO-ERROR.
    END.
    FIND NEXT l-orderhdr WHERE l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK NO-ERROR.
END.
b = STRING(TIME,"HH:MM:SS").
/*MESSAGE "start b: " b VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
FIND FIRST messages EXCLUSIVE-LOCK NO-ERROR.
DO WHILE AVAILABLE messages:
    DELETE messages.   
    FIND NEXT messages EXCLUSIVE-LOCK NO-ERROR.
END.

c = STRING(TIME,"HH:MM:SS").
/*MESSAGE "start c : " c
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
IF use-po-esignature THEN
DO:
    FIND FIRST qsy-list NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE qsy-list.
        FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr EQ qsy-list.docu-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-orderhdr THEN
        DO:
            CREATE po-list.
            ASSIGN
            po-list.lief-nr       = l-orderhdr.lief-nr
            po-list.docu-nr       = l-orderhdr.docu-nr
            po-list.bestelldatum  = l-orderhdr.bestelldatum
            po-list.lieferdatum   = l-orderhdr.lieferdatum
            po-list.bestellart    = l-orderhdr.bestellart
            po-list.gedruckt      = l-orderhdr.gedruckt
            po-list.besteller     = l-orderhdr.besteller
            po-list.lief-fax-3    = l-orderhdr.lief-fax[3]
            po-list.rec-id        = RECID(l-orderhdr).
        
            FOR EACH queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ po-list.docu-nr NO-LOCK:
                        
                /*DISP queasy.char1 FORMAT "x(20)" queasy.number1.*/
    
                IF queasy.number1 EQ 1 THEN po-list.approval-lvl[1] = YES.
                IF queasy.number1 EQ 2 THEN po-list.approval-lvl[2] = YES.
                IF queasy.number1 EQ 3 THEN po-list.approval-lvl[3] = YES.
                IF queasy.number1 EQ 4 THEN po-list.approval-lvl[4] = YES.
            END.
        
            IF po-list.approval-lvl[1] EQ NO THEN DELETE po-list. 
            ELSE
            DO:
                FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN
                DO:
                    IF SUBSTR(bediener.permissions, 89, 2) GE '2' THEN po-list.approval-id[1] = bediener.userinit.
                    IF SUBSTR(bediener.permissions, 90, 2) GE '2' THEN po-list.approval-id[2] = bediener.userinit.
                    IF SUBSTR(bediener.permissions, 91, 2) GE '2' THEN po-list.approval-id[3] = bediener.userinit.
                    IF SUBSTR(bediener.permissions, 92, 2) GE '2' THEN po-list.approval-id[4] = bediener.userinit.
                END.
            
                IF po-list.approval-lvl[1] EQ YES THEN 
                    ASSIGN app-lvl = 1 
                           po-list.need-approval = "2nd Approval".
                IF po-list.approval-lvl[2] EQ YES THEN 
                    ASSIGN app-lvl = 2
                           po-list.need-approval = "3rd Approval".
                IF po-list.approval-lvl[3] EQ YES THEN 
                    ASSIGN app-lvl = 3
                           po-list.need-approval = "4th Approval".
            
                /*DISP po-list.docu-nr po-list.approval-lvl po-list.approval-id po-list.need-approval user-init WITH WIDTH 180. */
            
                IF po-list.approval-lvl[1] EQ YES 
                    AND po-list.approval-lvl[2] EQ YES 
                    AND po-list.approval-lvl[3] EQ YES 
                    AND po-list.approval-lvl[4] EQ YES THEN .
                ELSE
                DO:
                    DO loop-init = 2 TO 4:
                        IF po-list.approval-id[loop-init] EQ user-init AND po-list.approval-lvl[loop-init] EQ NO THEN 
                        DO:
                            IF po-list.approval-lvl[loop-init - 1] EQ YES THEN
                            DO:
                                /*DISP po-list.docu-nr po-list.approval-lvl po-list.approval-id po-list.need-approval user-init WITH WIDTH 180.*/ 
                                FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                                FIND FIRST messages WHERE messages.zinr EQ po-list.docu-nr AND messages.gastnr EQ bediener.nr NO-LOCK NO-ERROR.
                                IF NOT AVAILABLE messages THEN
                                DO:
                                    CREATE messages.
                                    ASSIGN 
                                        messages.zeit         = TIME
                                        messages.gastnr       = bediener.nr
                                        messages.zinr         = po-list.docu-nr
                                        messages.messtext[10] = STRING(po-list.lief-nr)
                                        messages.NAME         = STRING(YEAR(TODAY),"9999") + "/" + STRING(MONTH(TODAY),"99") + "/" + STRING(DAY(TODAY),"99")
                                        messages.usre         = user-init
                                        messages.messtext[7]  = STRING(po-list.approval-id[1]) + "|" + STRING(po-list.approval-id[2]) + "|" + STRING(po-list.approval-id[3]) + "|" + STRING(po-list.approval-id[4])
                                        messages.messtext[8]  = STRING(po-list.approval-lvl[1]) + "|" + STRING(po-list.approval-lvl[2]) + "|" + STRING(po-list.approval-lvl[3]) + "|" + STRING(po-list.approval-lvl[4])
                                        messages.messtext[9]  = STRING(app-lvl)
                                        messages.messtext[1]  = "PO Number " + po-list.docu-nr + " Need " + po-list.need-approval.
                                END.
                            END.
                        END.
                    END.
                END.
            END.
        END.
        FIND NEXT qsy-list NO-LOCK NO-ERROR. 
    END.
END.
d = STRING(TIME,"HH:MM:SS").
/*MESSAGE "done d : " d
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
/*
FOR EACH messages:
    DISP messages.zinr messages.messtext[1].
END.*/
