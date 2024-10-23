DEFINE TEMP-TABLE excel-list
    FIELD curr-xlsrow AS INTEGER
    FIELD curr-xlscol AS INTEGER
    FIELD curr-val AS CHARACTER.
DEFINE TEMP-TABLE coa-list
    FIELD fibukonto AS   CHARACTER
    FIELD anzahl    AS   INTEGER INIT 0.

DEFINE TEMP-TABLE error-list 
    FIELD curr-xlsrow AS INTEGER
    FIELD curr-xlscol AS INTEGER
    FIELD curr-val AS CHARACTER
    FIELD msg    AS CHAR.

DEFINE TEMP-TABLE t-parameters LIKE parameters.
DEF BUFFER parambuff FOR parameters.
DEFINE INPUT PARAMETER briefnr AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR excel-list.
DEFINE OUTPUT PARAMETER TABLE FOR coa-list.
DEFINE OUTPUT PARAMETER TABLE FOR error-list.
DEFINE OUTPUT PARAMETER error-flag AS LOGICAL INIT NO.

DEFINE VARIABLE flag-combo AS LOGICAL INIT NO.
DEFINE VARIABLE row-combo AS INTEGER INIT 0.
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE str2 AS CHAR.

FOR EACH gl-acct NO-LOCK:
  CREATE coa-list.
  ASSIGN coa-list.fibukonto = gl-acct.fibukonto.
END.

FOR EACH excel-list BY excel-list.curr-xlsrow BY excel-list.curr-xlscol:
  IF excel-list.curr-val MATCHES "*combo-on*" THEN
    ASSIGN
      flag-combo = YES
      row-combo = excel-list.curr-xlsrow.
  IF excel-list.curr-val MATCHES "*combo-off*" THEN flag-combo = NO.
  IF SUBSTR(excel-list.curr-val,1,1) = "$" 
    OR SUBSTR(excel-list.curr-val,1,1) = "^" THEN
  DO:
    CREATE t-parameters.
    ASSIGN
      t-parameters.progname = "GL-Macro"
      t-parameters.SECTION  = STRING(briefnr)
      t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") 
                                    + "-" + STRING(excel-list.curr-xlscol,"99")
      str = ENTRY(1, SUBSTR(excel-list.curr-val,2), ".")
      str2 = ENTRY(1,str,":").
    IF curr-xlsrow GT row-combo AND flag-combo THEN
      t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") 
                              + "-" + STRING(excel-list.curr-xlscol,"99") 
                              + "-" + "combo".
    IF NUM-ENTRIES(str,":") GT 1 AND SUBSTR(excel-list.curr-val,1,1) = "^" THEN
      t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") 
                              + "-" + STRING(excel-list.curr-xlscol,"99") 
                              + "-" + "CF".
    
    IF SUBSTR(excel-list.curr-val,1,1) = "$" THEN 
      ASSIGN t-parameters.vstring = excel-list.curr-val.
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*segmrev*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*segmpers*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*segmroom*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").
    /*ragung request janevela for web PNL*/
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-tot-rm*" THEN 
      ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").  
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-act-rm*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-ooo*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rrom-90*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rrom-91*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-occ-rm*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-wig*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-nguest*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-day-use*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-numcompl*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-rsv*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-arr*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-prs-arr*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-dep*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-prs-dep*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-wig*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-noshow*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-newres*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-cancel*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-earco*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-arrtmr*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-prs-arrtmr*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    ELSE IF SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND excel-list.curr-val MATCHES "*stat-rm-deptmr*" THEN
        ASSIGN t-parameters.vstring = ENTRY(1,SUBSTR(excel-list.curr-val,2),".").    
    /*ragung end*/
    ELSE
    DO: 
      FIND FIRST gl-acct WHERE 
        gl-acct.fibukonto = str2 NO-LOCK NO-ERROR. 
      FIND FIRST artikel WHERE artikel.departement = INTEGER(SUBSTR(str2,1,2))
        AND artikel.artnr = INTEGER(SUBSTR(str2,3)) NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
      DO:
        IF AVAILABLE artikel THEN.
        ELSE 
        DO:
          IF flag-combo THEN.
          ELSE 
          DO:
            CREATE error-list.
            BUFFER-COPY excel-list TO error-list.
            error-list.msg = "GL AcctNo not found in cell".
            error-flag = YES.
          END.
        END.
      END.
      ELSE IF AVAILABLE gl-acct THEN
      DO:
        FIND FIRST coa-list WHERE coa-list.fibukonto = gl-acct.fibukonto
          NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN coa-list.anzahl = coa-list.anzahl + 1.
        t-parameters.vstring = str.
        CASE ENTRY(2, SUBSTR(excel-list.curr-val,2), "."):
          WHEN "BALANCE"        THEN t-parameters.vtype = 1.
          WHEN "YDBALANCE"      THEN t-parameters.vtype = 2.
          WHEN "LASTMON"        THEN t-parameters.vtype = 3.
          WHEN "LASTYR"         THEN t-parameters.vtype = 4.
          WHEN "LYTDBL"         THEN t-parameters.vtype = 5.  
          WHEN "BUDGET"         THEN t-parameters.vtype = 6.
          WHEN "YDBUDGET"       THEN t-parameters.vtype = 7.
          WHEN "LMBUDGET"       THEN t-parameters.vtype = 8.
          WHEN "LYBUDGET"       THEN t-parameters.vtype = 9.
          WHEN "LYTDBG"         THEN t-parameters.vtype = 10.
          WHEN "JAN"            THEN t-parameters.vtype = 11.
          WHEN "FEB"            THEN t-parameters.vtype = 12.
          WHEN "MAR"            THEN t-parameters.vtype = 13.
          WHEN "APR"            THEN t-parameters.vtype = 14.
          WHEN "MAY"            THEN t-parameters.vtype = 15.
          WHEN "JUN"            THEN t-parameters.vtype = 16.
          WHEN "JUL"            THEN t-parameters.vtype = 17.
          WHEN "AUG"            THEN t-parameters.vtype = 18.
          WHEN "SEP"            THEN t-parameters.vtype = 19.
          WHEN "OCT"            THEN t-parameters.vtype = 20.
          WHEN "NOV"            THEN t-parameters.vtype = 21.
          WHEN "DEC"            THEN t-parameters.vtype = 22.
          WHEN "DEBIT"          THEN t-parameters.vtype = 25.
          WHEN "CREDIT"         THEN t-parameters.vtype = 26.
          WHEN "DIFF"           THEN t-parameters.vtype = 27.
          WHEN "LMDIFF"         THEN t-parameters.vtype = 28.
          WHEN "BJAN"           THEN t-parameters.vtype = 31.
          WHEN "BFEB"           THEN t-parameters.vtype = 32.
          WHEN "BMAR"           THEN t-parameters.vtype = 33.
          WHEN "BAPR"           THEN t-parameters.vtype = 34.
          WHEN "BMAY"           THEN t-parameters.vtype = 35.
          WHEN "BJUN"           THEN t-parameters.vtype = 36.
          WHEN "BJUL"           THEN t-parameters.vtype = 37.
          WHEN "BAUG"           THEN t-parameters.vtype = 38.
          WHEN "BSEP"           THEN t-parameters.vtype = 39.
          WHEN "BOCT"           THEN t-parameters.vtype = 40.
          WHEN "BNOV"           THEN t-parameters.vtype = 41.
          WHEN "BDEC"           THEN t-parameters.vtype = 42.
          WHEN "LJAN"           THEN t-parameters.vtype = 43.
          WHEN "LFEB"           THEN t-parameters.vtype = 44.
          WHEN "LMAR"           THEN t-parameters.vtype = 45.
          WHEN "LAPR"           THEN t-parameters.vtype = 46.
          WHEN "LMAY"           THEN t-parameters.vtype = 47.
          WHEN "LJUN"           THEN t-parameters.vtype = 48.
          WHEN "LJUL"           THEN t-parameters.vtype = 49.
          WHEN "LAUG"           THEN t-parameters.vtype = 50.
          WHEN "LSEP"           THEN t-parameters.vtype = 51.
          WHEN "LOCT"           THEN t-parameters.vtype = 52.
          WHEN "LNOV"           THEN t-parameters.vtype = 53.
          WHEN "LDEC"           THEN t-parameters.vtype = 54.
          WHEN "NBJAN"          THEN t-parameters.vtype = 55.
          WHEN "NBFEB"          THEN t-parameters.vtype = 56.
          WHEN "NBMAR"          THEN t-parameters.vtype = 57.
          WHEN "NBAPR"          THEN t-parameters.vtype = 58.
          WHEN "NBMAY"          THEN t-parameters.vtype = 59.
          WHEN "NBJUN"          THEN t-parameters.vtype = 60.
          WHEN "NBJUL"          THEN t-parameters.vtype = 61.
          WHEN "NBAUG"          THEN t-parameters.vtype = 62.
          WHEN "NBSEP"          THEN t-parameters.vtype = 63.
          WHEN "NBOCT"          THEN t-parameters.vtype = 64.
          WHEN "NBNOV"          THEN t-parameters.vtype = 65.
          WHEN "NBDEC"          THEN t-parameters.vtype = 66.
          WHEN "LBJAN"          THEN t-parameters.vtype = 67. /*dody 201016 add keyword Last Year Budget*/
          WHEN "LBFEB"          THEN t-parameters.vtype = 68.
          WHEN "LBMAR"          THEN t-parameters.vtype = 69.
          WHEN "LBAPR"          THEN t-parameters.vtype = 70.
          WHEN "LBMAY"          THEN t-parameters.vtype = 71.
          WHEN "LBJUN"          THEN t-parameters.vtype = 72.
          WHEN "LBJUL"          THEN t-parameters.vtype = 73.
          WHEN "LBAUG"          THEN t-parameters.vtype = 74.
          WHEN "LBSEP"          THEN t-parameters.vtype = 75.
          WHEN "LBOCT"          THEN t-parameters.vtype = 76.
          WHEN "LBNOV"          THEN t-parameters.vtype = 77.
          WHEN "LBDEC"          THEN t-parameters.vtype = 78. /*dody end*/
          WHEN "debit-lsyear"   THEN t-parameters.vtype = 79.
          WHEN "credit-lsyear"  THEN t-parameters.vtype = 80.
          WHEN "debit-lsmonth"  THEN t-parameters.vtype = 81.
          WHEN "credit-lsmonth" THEN t-parameters.vtype = 82.
          WHEN "mapcoa"         THEN t-parameters.vtype = 88. /*gerald 100221 keyword mapping coa*/
		  WHEN "LYLASTMON"      THEN t-parameters.vtype = 89. /*ita 050122 keyword last month last year*/	
          /*geral D5D0FB debit - credit - balance MTD & YTD*/
          WHEN "debit-today"    THEN t-parameters.vtype = 90.
          WHEN "credit-today"   THEN t-parameters.vtype = 91.
          WHEN "debit-MTD"      THEN t-parameters.vtype = 92.
          WHEN "credit-MTD"     THEN t-parameters.vtype = 93.
          WHEN "debit-YTD"      THEN t-parameters.vtype = 94.
          WHEN "credit-YTD"     THEN t-parameters.vtype = 95.
          WHEN "today-balance"  THEN t-parameters.vtype = 96.
          WHEN "MTD-balance"    THEN t-parameters.vtype = 97.
          WHEN "YTD-balance"    THEN t-parameters.vtype = 98.
          /*end geral*/
          /*MG 2 Last Year Actual 02A1F0*/
          WHEN "2LJAN"          THEN t-parameters.vtype = 99.
          WHEN "2LFEB"          THEN t-parameters.vtype = 100.
          WHEN "2LMAR"          THEN t-parameters.vtype = 101.
          WHEN "2LAPR"          THEN t-parameters.vtype = 102.
          WHEN "2LMAY"          THEN t-parameters.vtype = 103.
          WHEN "2LJUN"          THEN t-parameters.vtype = 104.
          WHEN "2LJUL"          THEN t-parameters.vtype = 105.
          WHEN "2LAUG"          THEN t-parameters.vtype = 106.
          WHEN "2LSEP"          THEN t-parameters.vtype = 107.
          WHEN "2LOCT"          THEN t-parameters.vtype = 108.
          WHEN "2LNOV"          THEN t-parameters.vtype = 109.
          WHEN "2LDEC"          THEN t-parameters.vtype = 110.
          /*End MG*/
          OTHERWISE
          DO:
            CREATE error-list.
            BUFFER-COPY excel-list TO error-list.
            error-list.msg = "Postfix not defined".
            error-flag = YES.
          END.
        END CASE.
      END.

      IF (AVAILABLE artikel AND NOT AVAILABLE gl-acct) OR flag-combo THEN
      DO:
        t-parameters.vstring = str.
        t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") + "-" 
                                + STRING(excel-list.curr-xlscol,"99") + "-" 
                                + "REV".
        IF flag-combo THEN
          t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") + "-" 
                                  + STRING(excel-list.curr-xlscol,"99") + "-" 
                                  + "comboREV".
        CASE ENTRY(2, SUBSTR(excel-list.curr-val,2), "."):
          WHEN "MTD"       THEN t-parameters.vtype = 23.
          WHEN "YTD"       THEN t-parameters.vtype = 24.
          WHEN "today"      THEN t-parameters.vtype = 83.
          WHEN "mtd-budget" THEN t-parameters.vtype = 84.
          WHEN "ytd-budget" THEN t-parameters.vtype = 85.
          WHEN "l-mtd"      THEN t-parameters.vtype = 86.
          WHEN "l-ytd"      THEN t-parameters.vtype = 87.
          OTHERWISE
          DO:
            CREATE error-list.
            BUFFER-COPY excel-list TO error-list.
            error-list.msg = "Postfix not defined".
            error-flag = YES.
            RETURN.
          END.
        END CASE.
      END.
    END.

    IF t-parameters.vstring NE "" AND SUBSTR(excel-list.curr-val,1,1) = "^" 
      AND t-parameters.vtype = 0 THEN
    DO:
      t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") + "-" + 
                              STRING(excel-list.curr-xlscol,"99") + "-" + "FO".
      IF flag-combo THEN
        t-parameters.varname  = STRING(excel-list.curr-xlsrow,"9999") + "-" + 
                                STRING(excel-list.curr-xlscol,"99") + "-" + "comboFO".
      CASE ENTRY(2, SUBSTR(excel-list.curr-val,2), "."):
        WHEN "MTD"        THEN t-parameters.vtype = 23.
        WHEN "YTD"        THEN t-parameters.vtype = 24.
        WHEN "today"      THEN t-parameters.vtype = 83.
        WHEN "mtd-budget" THEN t-parameters.vtype = 84.
        WHEN "ytd-budget" THEN t-parameters.vtype = 85.
        WHEN "l-mtd"      THEN t-parameters.vtype = 86.
        WHEN "l-ytd"      THEN t-parameters.vtype = 87.
        OTHERWISE
        DO:
          CREATE error-list.
          BUFFER-COPY excel-list TO error-list.
          error-list.msg = "Postfix not defined".
          error-flag = YES.
        END.
      END CASE.
    END.
  END.
END.

FOR EACH coa-list WHERE coa-list.anzahl NE 0:
    DELETE coa-list.
END.

IF NOT error-flag THEN
DO:
  FIND FIRST t-parameters.
  FIND FIRST parameters WHERE
    parameters.progname            = "GL-Macro"      AND
    parameters.SECTION             = t-parameters.SECTION
    NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE parameters:
    DO TRANSACTION:
      FIND FIRST parambuff WHERE RECID(parambuff) = RECID(parameters)
        EXCLUSIVE-LOCK.
      DELETE parambuff.
      RELEASE parambuff.
    END.
    FIND NEXT parameters WHERE
      parameters.progname            = "GL-Macro"      AND
      parameters.SECTION             = t-parameters.SECTION
      NO-LOCK NO-ERROR.
  END.

  FOR EACH t-parameters NO-LOCK:
    CREATE parameters.
    BUFFER-COPY t-parameters TO parameters.
  END.
END.


