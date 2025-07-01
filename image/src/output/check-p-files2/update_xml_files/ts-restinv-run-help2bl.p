DEF TEMP-TABLE menu-list  
    FIELD request      AS CHAR   
    FIELD krecid       AS INTEGER INITIAL 0   
    FIELD posted       AS LOGICAL INITIAL NO   
    FIELD nr           AS INTEGER FORMAT ">>>" LABEL "No"   
    FIELD artnr        LIKE vhp.h-artikel.artnr   
    FIELD bezeich      LIKE vhp.h-artikel.bezeich   
    FIELD anzahl       LIKE vhp.h-bill-line.anzahl INITIAL 1   
    FIELD price        AS DECIMAL   
    FIELD betrag       AS DECIMAL   
    FIELD voucher      AS CHAR INITIAL "".  
  

DEF INPUT PARAMETER TABLE FOR menu-list.  
DEF INPUT PARAMETER pvILanguage         AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER session-parameter   AS CHAR.  
DEF INPUT PARAMETER do-it               AS LOGICAL.  
DEF INPUT PARAMETER tischnr             AS INT.  
DEF INPUT PARAMETER curr-dept           AS INT.  
DEF INPUT PARAMETER curr-waiter         AS INT.  
DEF INPUT PARAMETER rechnr              AS INT.  
DEF INPUT PARAMETER departement         AS INT.  
DEF INPUT PARAMETER user-init           AS CHAR.  
DEF OUTPUT PARAMETER bill-date          AS DATE.  
DEF OUTPUT PARAMETER error-str          AS CHAR.  
  
DEFINE VARIABLE disc-art1 AS INTEGER. /*FDL*/
DEFINE VARIABLE disc-art2 AS INTEGER. /*FDL*/
DEFINE VARIABLE disc-art3 AS INTEGER. /*FDL*/
DEFINE VARIABLE head-recid AS INTEGER. /*FDL*/
DEFINE VARIABLE i AS INTEGER. /*MASDOD*/

FIND FIRST htparam WHERE htparam.paramnr EQ 557 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art1 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 596 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art2 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 556 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art3 = htparam.finteger.

FOR EACH menu-list WHERE menu-list.nr = 0 AND menu-list.REQUEST NE "":  
    RUN create-request-journal.  
    DELETE menu-list.  
END.  
IF do-it THEN RUN add-kitchprbl.p(pvILanguage, session-parameter, departement,  
                                  rechnr, bill-date, user-init, OUTPUT error-str).  

/*FDL => Feature Kitchen Display
IF do-it THEN
DO:
    RUN htpdate.p(110, OUTPUT bill-date). 

    FOR EACH menu-list WHERE menu-list.artnr EQ disc-art1
        OR menu-list.artnr EQ disc-art2
        OR menu-list.artnr EQ disc-art3: 

        DELETE menu-list.  
    END.
    
    CREATE queasy.
    ASSIGN
        queasy.KEY      = 257
        queasy.number1  = curr-dept
        queasy.number2  = rechnr
        queasy.number3  = tischnr
        queasy.char1    = "kds-header"
        queasy.char2    = user-init
        queasy.date1    = bill-date
        queasy.logi1    = NO
        queasy.deci1    = TIME
        .
    FIND CURRENT queasy NO-LOCK.
    head-recid = RECID(queasy).

    FOR EACH menu-list /*WHERE menu-list.nr GT 0*/ NO-LOCK BY menu-list.nr:
        FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ rechnr
            AND h-bill-line.departement EQ curr-dept
            AND h-bill-line.artnr EQ menu-list.artnr
            AND h-bill-line.anzahl EQ menu-list.anzahl
            AND h-bill-line.bill-datum EQ bill-date NO-LOCK:

            FIND FIRST queasy WHERE queasy.KEY EQ 255
                AND queasy.char1 EQ "kds-line"
                AND queasy.number3 EQ INT(RECID(h-bill-line)) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                DO i = 1 TO h-bill-line.anzahl:
                    CREATE queasy.
                    ASSIGN
                        queasy.KEY      = 255
                        queasy.number1  = curr-dept
                        queasy.number2  = rechnr
                        queasy.number3  = RECID(h-bill-line) 
                        queasy.char1    = "kds-line"
                        queasy.char2    = user-init
                        queasy.date1    = h-bill-line.bill-datum
                        queasy.deci1    = h-bill-line.zeit
                        queasy.deci2    = head-recid
                        queasy.logi1    = NO
                        queasy.betriebsnr = i
                        .
                END.
            END.
        END.
    END.
END.
*/
PROCEDURE create-request-journal:  
  RUN htpdate.p(110, OUTPUT bill-date).  
  CREATE vhp.h-journal.   
  ASSIGN   
    vhp.h-journal.artnr       = menu-list.artnr  
    vhp.h-journal.bezeich     = "<!" + menu-list.bezeich + "!>"  
    vhp.h-journal.aendertext  = menu-list.REQUEST   
    vhp.h-journal.anzahl      = /*menu-list.anzahl*/ 0   
    vhp.h-journal.epreis      = /*menu-list.price */ 0   
    vhp.h-journal.rechnr      = rechnr   
    vhp.h-journal.tischnr     = tischnr   
    vhp.h-journal.departement = curr-dept   
    vhp.h-journal.zeit        = TIME  
    vhp.h-journal.kellner-nr  = curr-waiter   
    vhp.h-journal.bill-datum  = bill-date   
    vhp.h-journal.sysdate     = TODAY  
  .   
END.  
  
