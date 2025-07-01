DEFINE TEMP-TABLE usr-list LIKE bediener
    FIELD email     AS CHAR FORMAT "x(24)" LABEL "E-mail"
    FIELD mphone    AS CHAR FORMAT "x(24)" LABEL "Mobile"
    FIELD pager     AS CHAR FORMAT "x(24)" LABEL "Pager"
    FIELD grp-str   AS CHAR
    FIELD totp-flag AS LOGICAL
    FIELD totp-status AS CHAR. 


DEF OUTPUT PARAMETER TABLE FOR usr-list.

RUN create-usrlist.
RUN create-blist.

DEFINE BUFFER totpdata FOR queasy.

PROCEDURE create-usrlist:
    FOR EACH bediener NO-LOCK:
        CREATE usr-list.
        BUFFER-COPY bediener TO usr-list.
        FIND FIRST queasy WHERE queasy.KEY = 134 AND 
            queasy.number1 = bediener.nr AND queasy.betriebsnr = 0 
            AND queasy.deci1 = 0 AND queasy.logi1 = NO USE-INDEX
            b-num_ix NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
            ASSIGN
                usr-list.email  = queasy.char2
                usr-list.mphone = queasy.char1
                usr-list.pager  = queasy.char3.
        IF bediener.user-group > 0 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 19 
                AND queasy.number1 = bediener.user-group NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                ASSIGN
                    usr-list.grp-str = queasy.char3.
        END.

        /*Masdod 14022025 get totp info*/
        FIND FIRST totpdata WHERE totpdata.KEY EQ 341 AND totpdata.char1 EQ bediener.username NO-LOCK NO-ERROR.
        IF AVAILABLE totpdata THEN 
        DO:
            usr-list.totp-flag = YES.
            IF totpdata.logi1 EQ YES THEN usr-list.totp-status = "ACTIVE".
            ELSE usr-list.totp-status = "INACTIVE".
        END.
    END.
END.


PROCEDURE create-blist:
DEFINE VARIABLE usr-code AS CHAR.
DEFINE BUFFER usrbuff FOR bediener.
  FIND FIRST usr-list WHERE usr-list.betriebsnr = 0
    AND usr-list.flag = 0 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE usr-list: 
    RUN encode-string(usr-list.usercode, OUTPUT usr-code). 
    FIND CURRENT usr-list EXCLUSIVE-LOCK. 
    usr-list.usercode = usr-code. 
    usr-list.betriebsnr = 1. 
    FIND CURRENT usr-list NO-LOCK. 
    FIND FIRST usrbuff WHERE usrbuff.nr = usr-list.nr EXCLUSIVE-LOCK.
    ASSIGN
      usrbuff.usercode = usr-code
      usrbuff.betriebsnr = 1
    .
    FIND CURRENT usrbuff NO-LOCK.
    FIND NEXT usr-list WHERE usr-list.betriebsnr = 0 
      AND usr-list.flag = 0 NO-LOCK NO-ERROR. 
  END. 
END.


PROCEDURE encode-string: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR. 
DEFINE VARIABLE s AS CHAR FORMAT "x(50)". 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE ch AS CHAR INITIAL "". 
 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
  j = random(1,9). 
  in-str = STRING(j) + in-str. 
 
  j = random(1,9). 
  ch = CHR(ASC(STRING(j)) + 23). 
  out-str = ch. 
  j = asc(ch) - 71. 
  DO len = 1 TO length(in-str): 
    out-str = out-str + chr(asc(SUBSTR(in-str,len,1)) + j). 
  END. 
END. 
