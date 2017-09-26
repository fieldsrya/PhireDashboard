from dbConn import orcl
from flask import jsonify

with orcl() as db:

    def getOpenCRs(username):
        sql = ' SELECT COUNT(1) \
        FROM PS_PHI_CR_TBL \
        WHERE (lower(PHI_ASSIGN_TO) = \'' + username + '\' \
         OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = \'' + username + '\')) \
        AND PHI_CR_STATUS NOT IN (\'CLSD\',\'CNCL\') '
        data = db.dbExecuteFetchOne(sql)
        if data[0] > 0:
            sql = ' SELECT \'<a href="https://phire.uc.edu/\' || PHI_CR_NUM || \'" target="_blank">\' || PHI_CR_NUM || \'</a>\', PHI_CR_STATUS, PHI_TITLE \
            FROM PS_PHI_CR_TBL \
            WHERE (lower(PHI_ASSIGN_TO) = \'' + username + '\' \
            OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = \'' + username + '\')) \
            AND PHI_CR_STATUS NOT IN (\'CLSD\',\'CNCL\') '
            issues = db.dbExecuteFetchAll(sql)
            return jsonify(issues)
        else:
            noCRs = [['0','0','No CRs Assigned']]
            return jsonify(noCRs)

    def getOpenIssues(username):
        sql = ' SELECT \'<a href="https://phire.uc.edu/\' || PHI_ISSUE_NUM || \'" target="_blank">\' || PHI_ISSUE_NUM || \'</a>\', PHI_ISSUE_STATUS, PHI_ASSIGN_TO, to_char(cast(PHI_OPEN_DTTM as date), \'MM/DD/YYYY HH24:MI:SS\'),\
         PHI_TITLE FROM PS_PHI_ISSUE \
         WHERE (lower(PHI_ASSIGN_TO) = \'' + username + '\' \
         OR lower(PHI_ASSIGN_TO) IN (SELECT LOWER(ROLENAME) FROM PS_ROLEUSER_VW WHERE lower(OPRID) = \'' + username + '\'))\
         AND PHI_ISSUE_STATUS NOT IN (\'CLSD\',\'CNCL\') '

        issues = db.dbExecuteFetchAll(sql)
        return jsonify(issues)
        # this is how to read a LOB and display
        #lobDecode = data[1][0].read()
