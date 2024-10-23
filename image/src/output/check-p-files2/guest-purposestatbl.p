/* Created By Gerald for Purpose Stay Statistic 30012020  */

DEFINE TEMP-TABLE gmember
    FIELD nr                AS INT
    FIELD name              AS CHAR     FORMAT "x(56)"
    FIELD adresse1          AS CHAR     FORMAT "x(56)"
    FIELD email-adr         AS CHAR     FORMAT "x(30)"
    FIELD ankunft           AS DATE     FORMAT 99/99/99
    FIELD abreise           AS DATE     FORMAT 99/99/99
    .

DEFINE INPUT PARAMETER f-date AS DATE.
DEFINE INPUT PARAMETER t-date AS DATE.
DEFINE INPUT PARAMETER pur-stay AS CHAR.
DEFINE INPUT PARAMETER mi-ch  AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR gmember.

DEFINE VARIABLE s AS CHAR INITIAL "".
DEFINE VARIABLE num     AS INTEGER.
DEFINE VARIABLE number  AS INTEGER.
DEFINE VARIABLE pur-nr  AS INTEGER.
DEFINE VARIABLE p-nr    AS INTEGER.

RUN disp-arlist.

/************************* PROCEDURE ************* ************/
PROCEDURE disp-arlist:
  /*IF mi-ch = "ytd" THEN
  DO:*/
    FOR EACH genstat WHERE genstat.datum GE f-date AND genstat.datum LE t-date AND genstat.zinr NE "" AND genstat.res-logic[2] USE-INDEX DATE_ix ,
        FIRST guest WHERE guest.gastnr EQ genstat.gastnrmember NO-LOCK BY guest.NAME :
        FIND FIRST res-line WHERE res-line.gastnrmember EQ genstat.gastnrmember NO-ERROR.
         
        IF AVAILABLE res-line THEN
        DO: 
            p-nr = 0.
            DO num = 1 TO NUM-ENTRIES(genstat.res-char[2], ";"):
               s = ENTRY(num,genstat.res-char[2], ";").
               IF s MATCHES("SEGM_PUR*") THEN
               p-nr = INTEGER (SUBSTR(s, INDEX(s, "SEGM_PUR") + 8)).
            END.
            
            FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.char3 = pur-stay NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                pur-nr = queasy.number1.
            END.
            IF pur-stay = "UNKNOWN" THEN
            DO:
                pur-nr = 0.
            END.
            
            IF pur-nr = p-nr THEN
            DO:
              CREATE gmember.
              ASSIGN 
                 gmember.NAME      = guest.NAME + guest.anrede1
                 gmember.adresse1  = guest.adresse1
                 gmember.email-adr = guest.email-adr
                 gmember.ankunft   = res-line.ankunft
                 gmember.abreise   = res-line.abreise
                 .
            END.
        END.
     END.
  /*END.*/
END.
