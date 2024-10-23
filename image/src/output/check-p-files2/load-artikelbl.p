DEF TEMP-TABLE t-artikel LIKE artikel.
DEF TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER deptNo    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE     FOR artikel-list.
DEF OUTPUT PARAMETER TABLE     FOR t-artikel.


CASE case-type:
  WHEN 1 THEN
  FOR EACH artikel WHERE artikel.departement = deptNo 
    AND artikel.activeflag NO-LOCK:
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 2 THEN
  FOR EACH artikel WHERE artikel.departement = deptNo 
    AND artikel.activeFLag NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
  END.
  WHEN 3 THEN
  FOR EACH artikel WHERE artikel.departement = 0 
    AND (artikel.artart = 2 OR artikel.artart = 7) 
    AND artikel.activeflag NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
  END.
  WHEN 4 THEN
  FOR EACH artikel WHERE artikel.departement = 0 
    AND (artikel.artart = 2 OR artikel.artart = 7) 
    AND artikel.activeflag NO-LOCK:
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 5 THEN
  FOR EACH artikel WHERE artikel.departement = 0 AND artikel.artart = 2 
    AND artikel.activeflag NO-LOCK:
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 6 THEN
  FOR EACH artikel WHERE artikel.departement = deptNo NO-LOCK:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
  END.
  WHEN 7 THEN
  FOR EACH artikel WHERE artikel.departement = 0 
    AND artikel.artart = 7 AND artikel.activeflag NO-LOCK:
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 8 THEN
  FOR EACH artikel WHERE artikel.departement = deptNo NO-LOCK:
    CREATE artikel-list.
    BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 9 THEN
  FOR EACH artikel WHERE artikel.departement = 0 AND artikel.artart = 10 
      AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
      CREATE artikel-list.
      BUFFER-COPY artikel TO artikel-list.
  END.
  WHEN 10 THEN
  FOR EACH artikel WHERE artikel.departement = 0 AND artikel.artart = 4 
      AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
      CREATE artikel-list.
      BUFFER-COPY artikel TO artikel-list.
  END.
  /* SY AUG 26 2017 */
  WHEN 11 THEN
  DO:

      /* SY AUG 31 2017 */
      FIND FIRST hoteldpt WHERE hoteldpt.num = deptNo NO-LOCK
          NO-ERROR.
      IF NOT AVAILABLE hoteldpt THEN RETURN.

      FIND FIRST artikel WHERE artikel.departement = deptNo 
          NO-LOCK NO-ERROR.
      IF AVAILABLE artikel THEN
      DO:
          FOR EACH artikel WHERE artikel.departement = deptNo NO-LOCK:
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
          END.
          RETURN.
      END.
      ELSE
      DO:
          CASE hoteldpt.departtyp:
              WHEN 0 THEN .
              WHEN 1 THEN RUN create-abuff(91).  /* F&B       */
              WHEN 2 THEN RUN create-abuff(93).  /* Mini Bar  */
              WHEN 3 THEN RUN create-abuff(94).  /* Laundry   */
              WHEN 4 THEN RUN create-abuff(92).  /* Banquet   */
              WHEN 5 THEN RUN create-abuff(93).  /* Drugstore */
              WHEN 6 THEN RUN create-abuff(93).  /* Others    */
          END CASE.
          FOR EACH artikel WHERE artikel.departement = deptNo NO-LOCK:
            CREATE t-artikel.
            BUFFER-COPY artikel TO t-artikel.
          END.
      END.
  END.
END CASE.

PROCEDURE create-abuff:
DEF INPUT PARAMETER inp-dept AS INTEGER NO-UNDO.
DEF BUFFER abuff FOR artikel.
DEF BUFFER zbuff FOR zwkum.
    FOR EACH artikel WHERE artikel.departement = inp-dept NO-LOCK:
      DO TRANSACTION:
        CREATE abuff.
        BUFFER-COPY artikel EXCEPT departement eigentuemer TO abuff.
        ASSIGN
            abuff.eigentuemer = NO
            abuff.departement = deptNo
            abuff.endkum      = 100 + deptNo

        .
        IF SUBSTR(abuff.bezeich, LENGTH(abuff.bezeich) - 1) = "01" THEN 
        abuff.bezeich = SUBSTR(abuff.bezeich, 1, LENGTH(abuff.bezeich) - 2)
            + STRING(deptNo, "99").
        FIND CURRENT abuff NO-LOCK.
        RELEASE abuff.
      END.
    END.
    FOR EACH zwkum WHERE zwkum.departement = inp-dept NO-LOCK:
      DO TRANSACTION:
          CREATE zbuff.
          BUFFER-COPY zwkum EXCEPT departement TO zbuff.
          ASSIGN zbuff.departement = deptNo.
          FIND CURRENT zbuff NO-LOCK.
          RELEASE zbuff.
      END.
    END.
    /* SY AUG 31 2017 */
    FIND FIRST ekum WHERE ekum.eknr = 100 + hoteldpt.num 
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE ekum THEN
    DO TRANSACTION:
        CREATE ekum.
        ASSIGN
            ekum.eknr    = 100 + hoteldpt.num
            ekum.bezeich = hoteldpt.depart
        .
        FIND CURRENT ekum NO-LOCK.
        RELEASE ekum.
    END.
END.
