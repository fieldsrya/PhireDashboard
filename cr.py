from dbConn import orcl
from flask import jsonify

with orcl() as db:

    def getOpenCRs(username):
        sql = "SELECT COUNT(1) FROM PS_PHI_CR_TBL"
        sql = sql + " WHERE (lower(PHI_ASSIGN_TO) = :usrname"
        sql = sql + " OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = :usrname ))"
        sql = sql + " AND PHI_CR_STATUS NOT IN (\'CLSD\',\'CNCL\')"
        params = {'usrname': username}

        data = db.dbExecuteFetchOne(sql, params)

        if data[0] > 0:
            sql = "SELECT \'<a href=\"https://phire.uc.edu/\' || PHI_CR_NUM || \'\" target=\"_blank\">\' || PHI_CR_NUM || \'</a>\', PHI_CR_STATUS, PHI_TITLE"
            sql = sql + " FROM PS_PHI_CR_TBL"
            sql = sql + " WHERE (lower(PHI_ASSIGN_TO) = :usrname"
            sql = sql + " OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = :usrname ))"
            sql = sql + " AND PHI_CR_STATUS NOT IN (\'CLSD\',\'CNCL\',\'CLNA\')"
            params = {'usrname': username}
            issues = db.dbExecuteFetchAll(sql, params)
            return jsonify(issues)
        else:
            noCRs = [['0','0','No CRs Assigned']]
            return jsonify(noCRs)

    def getOpenIssues(username):
        
        sql = "SELECT \'<a href=\"https://phire.uc.edu/\' || PHI_ISSUE_NUM || \'\" target=\"_blank\">\' || PHI_ISSUE_NUM || \'</a>\', PHI_ISSUE_STATUS, PHI_ASSIGN_TO, to_char(cast(PHI_OPEN_DTTM as date), \'MM/DD/YYYY HH24:MI:SS\'), PHI_TITLE"
        sql = sql + " FROM PS_PHI_ISSUE I"
        sql = sql + " INNER JOIN PS_PHI_LOOKUP_TBL LU ON I.PHI_ISSUE_TYPE = LU.PHI_FIELD_VALUE"
        sql = sql + " WHERE (lower(PHI_ASSIGN_TO) = :usrname"
        sql = sql + " OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = :usrname ))"
        sql = sql + " AND PHI_ISSUE_STATUS NOT IN (\'CLSD\',\'CNCL\',\'CLNA\')"
        sql = sql + " AND LU.PHI_DOMAIN_ID = \'CS\'"
        sql = sql + " AND LU.PHI_FIELD_NAME = \'ISSUE TYPE\'"
        params = {'usrname': username}
        issues = db.dbExecuteFetchAll(sql, params)
        return jsonify(issues)
        # this is how to read a LOB and display
        #lobDecode = data[1][0].read()
