DEF TEMP-TABLE t-guest
  FIELD akt-gastnr      AS INTEGER
  FIELD karteityp       AS INTEGER
  FIELD master-gastnr   AS INTEGER
  FIELD pr-flag         AS INTEGER INITIAL 0   /* contRate   */
  FIELD mc-flag         AS LOGICAL INITIAL NO   /* membership */
  FIELD gname           AS CHAR    FORMAT "x(34)" COLUMN-LABEL "Name"
  FIELD adresse         AS CHAR    FORMAT "x(21)" COLUMN-LABEL "Address"
  FIELD steuernr        AS CHAR    FORMAT "x(36)" COLUMN-LABEL "Ref-No"
  FIELD firma           AS CHAR    FORMAT "x(34)" COLUMN-LABEL "Company"
  FIELD namekontakt     AS CHAR    FORMAT "x(24)" COLUMN-LABEL "Name Contact"
  FIELD phonetik3       AS CHAR    FORMAT "x(4)"  COLUMN-LABEL "Sales-ID" 
  FIELD rabatt          AS DECIMAL FORMAT ">9.99" COLUMN-LABEL "Disc(%("
  FIELD endperiode      AS DATE                   COLUMN-LABEL "Expired Date" 
  FIELD firmen-nr       AS INTEGER      COLUMN-LABEL "Comp-No"
  FIELD land            AS CHARACTER
  FIELD wohnort         AS CHARACTER
  FIELD telefon         AS CHARACTER
  FIELD plz             AS CHARACTER
  FIELD geschlecht      AS CHARACTER
  FIELD ausweis-nr1     AS CHARACTER
  FIELD gastnr          AS INTEGER
  FIELD zahlungsart     AS INTEGER FORMAT ">>>>>" 
  FIELD kreditlimit     AS DECIMAL
  FIELD bezeich         AS CHARACTER
  FIELD alertbox        AS LOGICAL INIT NO
  FIELD warningbox      AS LOGICAL INIT NO
  FIELD zimmeranz       AS INTEGER  /*gerald kebutuhan dito web*/
  FIELD bemerk          AS CHAR     /*gerald kebutuhan dito web*/
  FIELD geburt-ort1     AS CHAR
  FIELD nation1         AS CHAR
  FIELD nation2         AS CHAR
  FIELD fax             AS CHAR
  FIELD geburtdatum1    AS DATE
  FIELD email-adr       AS CHAR
  FIELD mobil-telefon   AS CHAR
  FIELD beruf           AS CHAR
  FIELD main-segment    AS CHAR         
  .
DEF INPUT  PARAMETER case-type      AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER sorttype       AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER lname          AS CHAR             NO-UNDO.
DEF INPUT  PARAMETER fname          AS CHAR             NO-UNDO.
DEF INPUT  PARAMETER num1           AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER first-gastnr   AS INTEGER INIT ?   NO-UNDO.
DEF OUTPUT PARAMETER curr-lname     AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER curr-fname     AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER total-record   AS DECIMAL          NO-UNDO.
DEF OUTPUT PARAMETER TABLE          FOR t-guest.
DEFINE VARIABLE counter AS INTEGER INIT 0 NO-UNDO.
DEFINE VARIABLE vipnr1  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr2  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr3  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr4  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr5  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr6  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr7  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr8  AS INTEGER INITIAL 999999999.   
DEFINE VARIABLE vipnr9  AS INTEGER INITIAL 999999999.   
total-record = 0.
FOR EACH guest WHERE guest.karteityp EQ sorttype NO-LOCK:
    total-record = total-record + 1.
END.
CASE case-type:
  WHEN 1 THEN 
  DO:
    /*FOR EACH guest WHERE (guest.gastnr > 0 
      AND guest.karteityp = sorttype AND guest.name MATCHES ("*" + lname + "*")
      AND (guest.vorname1 + guest.anredefirma) MATCHES ("*" + fname + "*") ) NO-LOCK BY guest.NAME: /*ragung 57D133*/*/
    FOR EACH guest WHERE (guest.gastnr > 0 
      AND guest.karteityp = sorttype AND guest.name GT lname
      AND (guest.vorname1 + guest.anredefirma) GE fname) NO-LOCK BY guest.NAME:
      counter = counter + 1.
      IF counter = 1 THEN first-gastnr = guest.gastnr.
      IF (counter GE 30) AND (curr-lname NE guest.NAME) THEN LEAVE.
      CREATE t-guest.
      BUFFER-COPY guest TO t-guest.
      ASSIGN
        t-guest.gname   = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                        + " " + guest.anrede1 
        t-guest.adresse = guest.adresse1 + " " + guest.adresse2
        t-guest.firma   = guest.name + ", " + guest.anredefirma
        t-guest.bemerk  = guest.bemerk
        t-guest.zimmeranz = guest.zimmeranz
        curr-lname      = guest.NAME
        curr-fname      = guest.vorname1 + guest.anredefirma
      .
      RUN check-prcode.
    END.
  END.
  WHEN 2 THEN
  DO:
    IF SUBSTR(lname, 1, 1) NE "*" AND lname NE " " THEN RUN case2A.
    ELSE IF LENGTH(lname) GE 2 AND SUBSTR(lname, 1, 1) EQ "*" THEN RUN case2B.
    ELSE IF lname EQ " " AND fname NE " " THEN RUN case2C.
  END.
  WHEN 3 THEN
  DO:
    IF lname NE "" AND SUBSTR(lname, 1, 1) NE "*" THEN RUN case3A.
    ELSE IF LENGTH(lname) GE 2 AND SUBSTR(lname, 1, 1) EQ "*" THEN RUN case3B.
  END.
  WHEN 4 THEN RUN case4.
  WHEN 5 THEN RUN case5.
  WHEN 6 THEN RUN case6.
  WHEN 7 THEN RUN case7.
  WHEN 8 THEN RUN case8.
  WHEN 9 THEN RUN case9.
END CASE.
RUN get-vipnr.
FOR EACH t-guest :
  FIND FIRST mc-guest WHERE mc-guest.gastnr = t-guest.gastnr
      AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.
  ASSIGN t-guest.mc-flag = AVAILABLE mc-guest.

  FOR EACH guestseg WHERE guestseg.gastnr = t-guest.gastnr NO-LOCK,  
      FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK:
      t-guest.bezeich = ENTRY(1, segment.bezeich, "$$0").
      LEAVE.  
  END.

  FOR EACH guestseg WHERE guestseg.gastnr = t-guest.gastnr NO-LOCK,  
      FIRST segment WHERE segment.segmentcode = guestseg.segmentcode  
      AND segment.betriebsnr = 4 NO-LOCK:
      t-guest.warningbox = YES.
      t-guest.bezeich = ENTRY(1, segment.bezeich, "$$0").
      LEAVE.  
  END.

  FIND FIRST guestseg WHERE guestseg.gastnr = t-guest.gastnr   
    AND (guestseg.segmentcode = vipnr1 OR   
    guestseg.segmentcode = vipnr2 OR   
    guestseg.segmentcode = vipnr3 OR   
    guestseg.segmentcode = vipnr4 OR   
    guestseg.segmentcode = vipnr5 OR   
    guestseg.segmentcode = vipnr6 OR   
    guestseg.segmentcode = vipnr7 OR   
    guestseg.segmentcode = vipnr8 OR   
    guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR.   
  IF AVAILABLE guestseg THEN   
  DO:   
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK.   
    t-guest.alertbox = YES.
    t-guest.bezeich = ENTRY(1, segment.bezeich, "$$0").
  END. 

  FIND FIRST guestseg WHERE guestseg.gastnr EQ t-guest.gastnr
      AND guestseg.reihenfolge EQ 1 NO-LOCK NO-ERROR.
  IF AVAILABLE guestseg THEN
  DO:
    FIND FIRST segment WHERE segment.segmentcode EQ guestseg.segmentcode NO-LOCK NO-ERROR. 
    IF AVAILABLE segment THEN
    DO:
      t-guest.main-segment = STRING(segment.segmentcode) + " - " + ENTRY(1, segment.bezeich, "$$0").
    END.
  END.
END.
PROCEDURE case2A:
  RELEASE guest NO-ERROR.
  IF num1 = 0 THEN FIND FIRST guest WHERE guest.name EQ lname 
    AND guest.karteityp = sorttype AND guest.gastnr GT 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN 
  DO: 
    IF fname NE " " THEN
    DO:
      FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
        AND guest.name EQ lname 
        AND (guest.vorname1 + guest.anredefirma) GE fname) NO-LOCK BY guest.NAME: 
        CREATE t-guest.
        BUFFER-COPY guest TO t-guest.
        ASSIGN
          t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                        + " " + guest.anrede1 
          t-guest.adresse = guest.adresse1 + " " + guest.adresse2
          t-guest.firma   = guest.name + ", " + guest.anredefirma
          curr-lname      = CHR(255)
          curr-fname      = CHR(255)
        .
        RUN check-prcode.
      END.
    END.
    /*gerald validasi jika firstname tidak di isi 395C12*/
    ELSE 
    DO:
      FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
        AND guest.name EQ lname) NO-LOCK BY guest.NAME: 
        CREATE t-guest.
        BUFFER-COPY guest TO t-guest.
        ASSIGN
          t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                        + " " + guest.anrede1 
          t-guest.adresse = guest.adresse1 + " " + guest.adresse2
          t-guest.firma   = guest.name + ", " + guest.anredefirma
          curr-lname      = CHR(255)
          curr-fname      = CHR(255)
        .
        RUN check-prcode.
      END.
    END.
  END. 
  ELSE
  DO:
    IF lname = CHR(255) THEN
    DO:
      curr-lname = lname.
      RETURN.
    END.
    FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
      AND guest.name GT lname 
      AND (guest.vorname1 + guest.anredefirma) GE fname) NO-LOCK BY guest.NAME: 
      counter = counter + 1.
      IF counter = 1 THEN first-gastnr = guest.gastnr.
      IF (counter GE 30) AND (curr-lname NE guest.NAME) THEN LEAVE.
      CREATE t-guest.
      BUFFER-COPY guest TO t-guest.
      ASSIGN
        t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                      + " " + guest.anrede1 
        t-guest.adresse = guest.adresse1 + " " + guest.adresse2
        t-guest.firma   = guest.name + ", " + guest.anredefirma
        curr-lname      = guest.NAME
        curr-fname      = guest.vorname1 + guest.anredefirma
      .
      RUN check-prcode.
    END.
  END.
END.
PROCEDURE case2B:
  IF SUBSTR(lname, LENGTH(lname), 1) NE "*" THEN lname = lname + "*". 
  FOR EACH guest WHERE (guest.gastnr > 0) 
    AND (guest.karteityp = sorttype) 
    AND (guest.NAME + guest.vorname1) MATCHES (lname) 
    NO-LOCK BY guest.NAME: 
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
      curr-fname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case2C:
  FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
    AND (guest.vorname1 + guest.anredefirma) MATCHES "*" + fname + "*") NO-LOCK BY guest.NAME: 
    counter = counter + 1.
    IF counter = 1 THEN first-gastnr = guest.gastnr.
    IF (counter GE 30) AND (curr-lname NE guest.NAME) THEN LEAVE.
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = guest.NAME
      curr-fname      = guest.vorname1 + guest.anredefirma
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case3A:
  FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
    AND SUBSTR(guest.name, 1, LENGTH(lname)) EQ lname 
    AND (guest.vorname1 + guest.anredefirma) GE "") NO-LOCK BY guest.NAME: 
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
      curr-fname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case3B:
  IF SUBSTR(lname, LENGTH(lname), 1) NE "*" THEN lname = lname + "*". 
  FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
    AND (guest.NAME + guest.vorname1) MATCHES (lname) 
    AND (guest.vorname1 + guest.anredefirma) GE fname) NO-LOCK BY guest.NAME: 
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
      curr-fname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case4:
DEF VAR cardNum     AS CHAR NO-UNDO.
DEF VAR from-pos    AS INTEGER NO-UNDO.
DEF VAR to-pos      AS INTEGER NO-UNDO.
  ASSIGN cardNum = lname.
  FIND FIRST mc-guest WHERE mc-guest.cardnum = cardNum NO-LOCK NO-ERROR.
  IF NOT AVAILABLE mc-guest THEN
  DO:
    RUN htpint.p (337, OUTPUT from-pos).
    RUN htpint.p (338, OUTPUT to-pos).
    IF from-pos GT 0 AND to-pos GT 0 THEN
    DO:
      ASSIGN
        cardNum    = SUBSTR(cardNum, from-pos, (to-pos - from-pos + 1))
        curr-fname = cardNum
      .
      FIND FIRST mc-guest WHERE mc-guest.cardnum = cardNum NO-LOCK NO-ERROR.
    END.
  END.
  IF AVAILABLE mc-guest THEN
  DO:
    FIND FIRST guest WHERE guest.gastnr = mc-guest.gastnr NO-LOCK.
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case5:
DEF VAR cardNum     AS CHAR NO-UNDO.
DEF VAR from-pos    AS INTEGER NO-UNDO.
DEF VAR to-pos      AS INTEGER NO-UNDO.
  IF lname = "" THEN RETURN.
  FOR EACH guest WHERE guest.karteityp = 0 AND guest.gastnr GT 0
    /* change MATCHES by Oscar (14 Oktober 2024) - 932990 */
    /* AND guest.ausweis-nr1 = lname NO-LOCK  */
    AND guest.ausweis-nr1 MATCHES "*" + lname + "*" NO-LOCK 
    BY guest.NAME:
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
      curr-fname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case6:
DEF VAR from-gastnr AS INTEGER NO-UNDO.
  ASSIGN from-gastnr = INTEGER(lname).
  FOR EACH guest WHERE guest.karteityp = sorttype 
    AND guest.gastnr GE from-gastnr NO-LOCK BY guest.gastnr: 
    counter = counter + 1.
    IF counter = 1 THEN first-gastnr = guest.gastnr.
    IF counter GE 30 THEN LEAVE.
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = STRING(guest.gastnr + 1)
      curr-fname      = guest.vorname1 + guest.anredefirma
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case7:
  /*MTFIND FIRST guest WHERE guest.gastnr = num1 NO-LOCK NO-ERROR.
  IF AVAILABLE guest THEN
  DO:
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
    .
    FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr
        AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.
    ASSIGN t-guest.mc-flag = AVAILABLE mc-guest.
    ASSIGN
      curr-lname = guest.vorname1
      curr-fname = guest.name
    .
    first-gastnr = guest.gastnr.
  END.*/
  /*MTFOR EACH guest WHERE guest.gastnr LE num1
      AND guest.karteityp = sorttype 
      AND guest.name GE lname 
      AND (guest.vorname1 + guest.anredefirma) GE fname
      NO-LOCK BY guest.NAME: 
      CREATE t-guest.
      BUFFER-COPY guest TO t-guest.
      ASSIGN
        t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                      + " " + guest.anrede1 
        t-guest.adresse = guest.adresse1 + " " + guest.adresse2
        t-guest.firma   = guest.name + ", " + guest.anredefirma
      .
      FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr
          AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.
      ASSIGN t-guest.mc-flag = AVAILABLE mc-guest.
  END.
  ASSIGN
    curr-lname = CHR(255)
    curr-fname = CHR(255)
  .
  
  
  FOR EACH guest WHERE guest.gastnr LE num1
    AND guest.karteityp = sorttype 
    AND guest.name GE lname 
    AND (guest.vorname1 + guest.anredefirma) GE ""
    NO-LOCK BY guest.NAME: 
    counter = counter + 1.
    IF counter = 1 THEN first-gastnr = guest.gastnr.
    IF counter GE 30 THEN LEAVE.
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = STRING(guest.gastnr + 1)
      curr-fname      = guest.vorname1 + guest.anredefirma
    .
  END.*/
      /*MTRELEASE guest NO-ERROR.
      FIND FIRST guest WHERE guest.gastnr = num1 NO-LOCK NO-ERROR. 
      IF AVAILABLE guest THEN 
      DO: */
      DEFINE VARIABLE found AS LOGICAL INIT NO.
      DEFINE VARIABLE curr-gastnr AS INTEGER INIT 0.

      FIND FIRST guest WHERE guest.gastnr = num1 NO-ERROR.
      IF NOT AVAILABLE guest THEN
      DO:
          RETURN NO-APPLY.
      END.
      ASSIGN
        lname = guest.NAME
        curr-gastnr = guest.gastnr.

        FOR EACH guest WHERE ( /*guest.gastnr LE num1 AND*/ guest.karteityp = sorttype 
          AND guest.name GE TRIM(lname)
          AND (guest.vorname1 + guest.anredefirma) GE "") 
          NO-LOCK BY guest.NAME: 
          
          IF guest.gastnr = curr-gastnr THEN found = TRUE.
          IF found THEN 
          DO:
            counter = counter + 1.  
            IF counter = 1 THEN first-gastnr = guest.gastnr.
            IF counter GE 30 THEN LEAVE.
            CREATE t-guest.
            BUFFER-COPY guest TO t-guest.
            ASSIGN
              t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                            + " " + guest.anrede1 
              t-guest.adresse = guest.adresse1 + " " + guest.adresse2
              t-guest.firma   = guest.name + ", " + guest.anredefirma
              curr-lname      = guest.NAME
              curr-fname      = guest.vorname1 + guest.anredefirma
            .
            RUN check-prcode.
          END.         
        END.
        
      /*MTEND. */
      /*MTELSE
      DO:
        IF lname = CHR(255) THEN
        DO:
          curr-lname = lname.
          RETURN.
        END.
        FOR EACH guest WHERE (guest.gastnr > 0 AND guest.karteityp = sorttype 
          AND guest.name GT lname 
          AND (guest.vorname1 + guest.anredefirma) GE fname) NO-LOCK BY guest.NAME: 
          counter = counter + 1.
          IF counter = 1 THEN first-gastnr = guest.gastnr.
          IF (counter GE 30) AND (curr-lname NE guest.NAME) THEN LEAVE.
          CREATE t-guest.
          BUFFER-COPY guest TO t-guest.
          ASSIGN
            t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 
            t-guest.adresse = guest.adresse1 + " " + guest.adresse2
            t-guest.firma   = guest.name + ", " + guest.anredefirma
            curr-lname      = guest.NAME
            curr-fname      = guest.vorname1 + guest.anredefirma
          .
        END.
      END.*/
END.
PROCEDURE case8:
  /* change to FOR EACH to get guest that matches search criteria by Oscar (14 Oktober 2024) - 932990 */
  /* FIND FIRST guest WHERE guest.gastnr) = INTEGER(lname) NO-LOCK NO-ERROR.
  IF NOT AVAILABLE guest THEN RETURN. */
  FOR EACH guest WHERE STRING(guest.gastnr) MATCHES "*" + lname + "*":
    CREATE t-guest.
    BUFFER-COPY guest TO t-guest.
    ASSIGN
      t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                    + " " + guest.anrede1 
      t-guest.adresse = guest.adresse1 + " " + guest.adresse2
      t-guest.firma   = guest.name + ", " + guest.anredefirma
      curr-lname      = CHR(255)
      curr-fname      = CHR(255)
    .
    RUN check-prcode.
  END.
END.
PROCEDURE case9:
    FIND FIRST cl-member WHERE cl-member.codenum = lname NO-LOCK NO-ERROR.
    IF AVAILABLE cl-member THEN DO:
        FIND FIRST guest WHERE guest.gastnr = cl-member.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN DO:
            CREATE t-guest.
            BUFFER-COPY guest TO t-guest.
            ASSIGN
                t-guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                              + " " + guest.anrede1 
                t-guest.adresse = guest.adresse1 + " " + guest.adresse2
                t-guest.firma   = guest.name + ", " + guest.anredefirma
                curr-lname      = CHR(255)
                curr-fname      = CHR(255)
              .
              RUN check-prcode.
        END.
    END.
END PROCEDURE.
PROCEDURE check-prcode:
  FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK:
    FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE 
      AND ratecode.endperiode GT TODAY NO-LOCK NO-ERROR.
    IF AVAILABLE ratecode THEN 
    DO:    
      t-guest.pr-flag = 2.
      RETURN.
    END.
    ELSE
    DO:
      FIND FIRST ratecode WHERE ratecode.CODE = guest-pr.CODE 
         NO-LOCK NO-ERROR.
      IF AVAILABLE ratecode THEN
      DO:
        ASSIGN t-guest.pr-flag = 1.
      END.
    END.
  END.
END.
PROCEDURE get-vipnr: 
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr2 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr3 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr4 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr5 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr6 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr7 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr8 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  IF htparam.finteger NE 0 THEN vipnr9 = htparam.finteger. 
END. 
