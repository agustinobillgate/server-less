DEFINE INPUT PARAMETER deptno AS INT.
DEFINE OUTPUT PARAMETER deptname AS CHAR.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ deptno NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN deptname = CAPS(hoteldpt.depart).
