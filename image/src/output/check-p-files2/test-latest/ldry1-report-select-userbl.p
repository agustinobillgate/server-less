DEFINE TEMP-TABLE q2-list
    FIELD departement LIKE kellner.departement
    FIELD depart      LIKE hoteldpt.depart
    FIELD kellner-nr  LIKE kellner.kellner-nr
    FIELD kellnername LIKE kellner.kellnername
    FIELD recid-kellner AS INT.

DEF INPUT PARAMETER ldry-dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

FOR EACH kellner WHERE kellner.departement = ldry-dept NO-LOCK,
    FIRST hoteldpt WHERE hoteldpt.num = kellner.departement 
    NO-LOCK BY kellner.kellner-nr:
    CREATE q2-list.
    ASSIGN
    q2-list.departement = kellner.departement
    q2-list.depart      = hoteldpt.depart
    q2-list.kellner-nr  = kellner.kellner-nr
    q2-list.kellnername = kellner.kellnername
    q2-list.recid-kellner = RECID(kellner).
END.
