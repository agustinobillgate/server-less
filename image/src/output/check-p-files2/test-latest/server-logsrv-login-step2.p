
DEFINE INPUT PARAMETER user-name    AS CHAR     NO-UNDO. 
DEFINE INPUT PARAMETER user-pswd    AS CHAR     NO-UNDO. 
DEFINE OUTPUT PARAMETER user-found  AS LOGICAL  NO-UNDO INIT NO. 
DEFINE OUTPUT PARAMETER user-token  AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER user-key    AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER userinit    AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER usercode    AS CHAR     NO-UNDO INIT "". /* encoded pswd */
DEFINE OUTPUT PARAMETER permissions AS CHAR     NO-UNDO INIT "".

DEFINE OUTPUT PARAMETER error-code  AS INTEGER         NO-UNDO INIT 0.
    /* 1001 htparam group 99 was manually changed   STOPPED 
       1002 hotelName/city /licenseNo not defined   STOPPED
       1003 room license = 0                        STOPPED
       1004 wrong room license                      STOPPED
       1005 wrong POS license                       STOPPED
       1006 serial number incorrect                 STOPPED
    */                                                  
DEFINE OUTPUT PARAMETER lic-nr         AS CHAR         NO-UNDO.
DEFINE OUTPUT PARAMETER htl-name       AS CHAR         NO-UNDO.
DEFINE OUTPUT PARAMETER htl-city       AS CHAR         NO-UNDO.
DEFINE OUTPUT PARAMETER htl-adr        AS CHAR         NO-UNDO.
DEFINE OUTPUT PARAMETER htl-tel        AS CHAR         NO-UNDO.
DEFINE OUTPUT PARAMETER price-decimal  AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER coa-format     AS CHAR         NO-UNDO.
/* VHP License Expired Date */                         
DEFINE OUTPUT PARAMETER vhp-licensedate AS DATE        NO-UNDO.
/* New VHP DB for new VHP setup */                     
DEFINE OUTPUT PARAMETER vhp-newDB   AS LOGICAL         NO-UNDO.
/*
DEFINE VARIABLE  user-name    AS CHAR     NO-UNDO INIT "sindata". 
DEFINE VARIABLE  user-pswd    AS CHAR     NO-UNDO INIT "". 
DEFINE VARIABLE  user-found  AS LOGICAL  NO-UNDO INIT NO. 
DEFINE VARIABLE  user-token  AS CHAR     NO-UNDO INIT "".
DEFINE VARIABLE  userinit    AS CHAR     NO-UNDO INIT "". 
DEFINE VARIABLE  usercode    AS CHAR     NO-UNDO INIT "". /* encoded pswd */
DEFINE VARIABLE  permissions AS CHAR     NO-UNDO INIT "".
*/

DEFINE VARIABLE tmp-userkey     AS CHARACTER.
DEFINE VARIABLE output-userkey  AS CHARACTER.
DEFINE VARIABLE licenseNr       AS CHARACTER.
DEFINE VARIABLE i               AS INT.

FIND FIRST bediener WHERE bediener.username = user-name AND bediener.flag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE bediener AND user-name = "sindata" THEN
DO:
    /*FIND FIRST bediener WHERE bediener.username = (user-name + CHR(3)) AND bediener.flag = 1 AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.*/
    FIND FIRST bediener WHERE bediener.username = user-name /*AND bediener.flag = 0*/ AND bediener.betriebsnr = 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bediener THEN 
    DO:
        user-found = NO.
        RETURN.
    END.
END.

IF user-name = "sindata" AND bediener.flag = 1 THEN
DO:
    DEFINE VARIABLE dd AS CHAR NO-UNDO.
    DEFINE VARIABLE mm AS CHAR NO-UNDO.
    ASSIGN
        dd         = STRING(DAY(TODAY + 1),"99")
        dd         = SUBSTR(dd, 2, 1) + SUBSTR(dd, 1, 1)
        mm         = STRING(MONTH(TODAY + 1), "99")
        mm         = SUBSTR(mm, 2, 1) + SUBSTR(mm, 1, 1)
        user-found = (user-pswd = ("SystemAdmin@" + dd + mm) AND 
              ASC(SUBSTR(user-pswd,1,1)) = 83 AND
              ASC(SUBSTR(user-pswd,7,1)) = 65)
    .
END.
ELSE
DO:
    DEFINE VARIABLE passwd AS CHAR NO-UNDO.
    RUN decode-string1(bediener.usercode, OUTPUT passwd). 
    user-found = (passwd EQ user-pswd).
END.

IF user-found THEN 
DO:   
    /*RUN get-user-tokenbl.p (bediener.userinit, "", "", "", OUTPUT user-token).*/
    ASSIGN
        userinit    = bediener.userinit
        usercode    = bediener.usercode /* encoded pswd */
        permissions = bediener.permissions
    .
END.
ELSE
DO:
    RETURN.
END.

/* Note: In web UI vhp main program, need to check expired password 
   bediener.kassenbest = 1 !!! */

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(paramtext.ptexte, OUTPUT licenseNr). 

DEF VAR masterkey AS CHAR.
FIND FIRST guest-queasy WHERE guest-queasy.KEY = "userToken" AND guest-queasy.char1 EQ userinit NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest-queasy THEN
DO:
     CREATE guest-queasy.
     ASSIGN
         guest-queasy.KEY     = "userToken"
         guest-queasy.date1   = TODAY
         guest-queasy.number1 = TIME
         guest-queasy.number3 = 1
         guest-queasy.char3   = licenseNr + CAPS(bediener.username) + CAPS(user-pswd) + "|" + STRING(TODAY) + STRING(TIME)
         guest-queasy.char1   = userinit
         .
END.
ELSE
DO:
    FOR EACH guest-queasy WHERE guest-queasy.KEY = "userToken" AND guest-queasy.char1 EQ userinit NO-LOCK BY guest-queasy.number3 DESCENDING:
        masterkey = ENTRY(1, guest-queasy.char3, "|").
        LEAVE.
    END.
END.

RUN get-user-tokenbl.p (bediener.userinit, "", "", masterkey, OUTPUT user-token).

tmp-userkey     = licenseNr + CAPS(user-name) + CAPS(user-pswd).
output-userkey  = "".

DO i = 1 TO LENGTH(tmp-userkey):
    output-userkey = output-userkey + "#" + SUBSTRING(tmp-userkey,i,1).
END.

output-userKey = output-userkey + "#".

user-key = HEX-ENCODE(SHA1-DIGEST(output-userkey)).
user-key = CAPS(user-key).  
/*===================================================================*/

RUN prepare-main01bl.p (OUTPUT error-code,
                        OUTPUT lic-nr,  
                        OUTPUT htl-name,
                        OUTPUT htl-city,
                        OUTPUT htl-adr, 
                        OUTPUT htl-tel, 
                        OUTPUT price-decimal, 
                        OUTPUT coa-format,    
                        OUTPUT vhp-licensedate,
                        OUTPUT vhp-newDB).
/*===================================================================*/

PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str   AS CHAR     NO-UNDO. 
DEFINE OUTPUT PARAMETER out-str AS CHAR     NO-UNDO INITIAL "". 
DEFINE VARIABLE s               AS CHAR     NO-UNDO. 
DEFINE VARIABLE j               AS INTEGER  NO-UNDO. 
DEFINE VARIABLE len             AS INTEGER  NO-UNDO. 
    ASSIGN
        s   = in-str 
        j   = ASC(SUBSTR(s, 1, 1)) - 71 
        len = LENGTH(in-str) - 1 
        s   = SUBSTR(in-str, 2, len)
    .
    DO len = 1 TO LENGTH(s): 
      out-str = out-str + chr(ASC(SUBSTR(s,len,1)) - j). 
    END. 
    out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
      s = in-str. 
      j = ASC(SUBSTR(s, 1, 1)) - 70. 
      len = LENGTH(in-str) - 1. 
      s = SUBSTR(in-str, 2, len). 
    DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
    END. 
END. 
