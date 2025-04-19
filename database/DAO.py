from database.DB_connect import DBConnect
from model import team
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct(YEAR) 
        from teams t 
        where `year` >= 1985
        order by `year` desc
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row['YEAR'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select * 
            from teams t 
            where t.`year` = %s
            """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalariesOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.teamCode , SUM(s.salary) as totSal
            FROM salaries s 
            WHERE s.`year` = %s
            group by s.teamCode 
            """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append([row["teamCode"], row["totSal"]])

        cursor.close()
        conn.close()
        return result
