DEFINE INPUT PARAMETER username AS CHARACTER.
DEFINE INPUT PARAMETER userkey AS CHARACTER.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.

/*
DEFINE VARIABLE username AS CHARACTER INITIAL "sindata".
DEFINE VARIABLE userkey AS CHARACTER INITIAL "e2acff2c86b8054380c7040e46fe9d682c82b6c8".
DEFINE VARIABLE ok-flag AS LOGICAL INITIAL NO.
DEFINE VARIABLE licenseNr AS CHARACTER INITIAL "1374".
*/

DEFINE VARIABLE licenseNr AS CHARACTER.
DEFINE VARIABLE password AS CHARACTER.

DEFINE VARIABLE tmp-userkey AS CHARACTER.
DEFINE VARIABLE output-userkey AS CHARACTER.
DEFINE VARIABLE sha-userkey AS CHARACTER.

DEFINE VARIABLE stop-flag AS LOGICAL INITIAL NO.

DEF TEMP-TABLE t-bediener LIKE bediener.

/*testing purpose : YES*/
DEFINE VARIABLE has-license AS LOGICAL INITIAL YES.
DEFINE VARIABLE nonce       AS CHAR.
DEFINE VARIABLE timestamp   AS CHAR.
/*23/04/2024 START*/
IF NUM-ENTRIES(userkey,"|") GT 1 THEN
DO:
    nonce     = ENTRY(2,userkey,"|") NO-ERROR.
    timestamp = ENTRY(3,userkey,"|") NO-ERROR.
        
    userkey = ENTRY(1,userkey,"|") NO-ERROR.
    /*
    IF nonce NE ? and timestamp NE ? THEN
    DO:
        FIND FIRST queasy WHERE queasy.key EQ 290
            AND queasy.char1 EQ nonce 
            AND queasy.char2 EQ timestamp NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN RETURN.
        ELSE
        DO:
            CREATE queasy.
            queasy.key     = 290.
            queasy.char1   = nonce.
            queasy.char2   = timestamp.
            queasy.date1   = TODAY.
            queasy.number1 = TIME.
        END.
        RELEASE queasy.
    END.
    MESSAGE STRING(TIME,"HH:MM:SS") + "-start deleting queasy" VIEW-AS ALERT-BOX INFO BUTTONS OK.
    FIND FIRST queasy WHERE queasy.key EQ 290 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        MESSAGE STRING(TIME,"HH:MM:SS") + "-get queasy: " + STRING(RECID(queasy)) + "|" + queasy.char2 VIEW-AS ALERT-BOX INFO BUTTONS OK.
        IF (DATETIME(TODAY,TIME * 1000) - DATETIME(queasy.date1,queasy.number1 * 1000)) / 1000 GT 1800 THEN
        DO:
            MESSAGE STRING(TIME,"HH:MM:SS") + "-deleteing queasy: " + STRING(RECID(queasy)) + "|" + queasy.char2 VIEW-AS ALERT-BOX INFO BUTTONS OK.
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            DELETE queasy.
        END.
        FIND NEXT queasy WHERE queasy.key EQ 290 NO-LOCK NO-ERROR.
    END.
    MESSAGE STRING(TIME,"HH:MM:SS") + "-end deleting queasy" VIEW-AS ALERT-BOX INFO BUTTONS OK.
    */
END.
/*23/04/2024 END*/

RUN check-htp-licensebl.p (OUTPUT stop-flag).
IF stop-flag THEN
DO:
    IF stop-flag THEN
    DO:
        MESSAGE "stop-flag: " STRING(stop-flag) VIEW-AS ALERT-BOX INFO BUTTONS OK.
        RETURN.
    END.
END.

/*RUN htplogic.p(1102, OUTPUT has-license).*/
IF has-license THEN
DO:
  RUN read-bedienerlistbl.p (2,username,OUTPUT TABLE t-bediener).

  FIND FIRST t-bediener NO-LOCK NO-ERROR.
  IF NOT AVAILABLE t-bediener THEN RETURN.
  RUN decode-string1(t-bediener.usercode, OUTPUT password).

  FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
  IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
    RUN decode-string(ptexte, OUTPUT licenseNr). 
  ELSE 
  DO: 
    MESSAGE "paramtext 243 empty string" VIEW-AS ALERT-BOX INFO BUTTONS OK.
    RETURN. 
  END. 

  DEFINE VARIABLE i AS INTEGER.

  /* Check userkey */
  username = CAPS(username).

  RUN check-userkey(username,CAPS(password),licenseNr).

  IF NOT ok-flag THEN 
  DO:
    RUN check-userkey(username,LC(password),licenseNr).
  END.
END.

PROCEDURE check-userkey:
  DEFINE INPUT PARAMETER inp-username AS CHAR.
  DEFINE INPUT PARAMETER inp-password AS CHAR.
  DEFINE INPUT PARAMETER inp-license AS CHAR.

  tmp-userkey = inp-license + inp-username + inp-password.

  output-userkey = "".

  DO i = 1 TO LENGTH(tmp-userkey):
    output-userkey = output-userkey + "#" + SUBSTRING(tmp-userkey,i,1).
  END.
  output-userKey = output-userkey + "#".

  sha-userkey = HEX-ENCODE(SHA1-DIGEST(output-userkey)).

  IF sha-userkey = userkey THEN
  DO:
    ok-flag = YES.
  END.
  ELSE
  DO:
        MESSAGE "sha-userkey: " sha-userkey skip
                "userkey: " userkey VIEW-AS ALERT-BOX INFO BUTTONS OK.
  END.

END.


PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 71. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
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

