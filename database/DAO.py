from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():
    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from airports a 
order by a.AIRPORT asc """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(n , idMapAeroporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.iata_code , COUNT(*) as N
from (select a.ID , a.IATA_CODE , f.AIRLINE_ID , COUNT(*)
from airports a , flights f 
where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
group by a.ID , a.IATA_CODE , f.AIRLINE_ID
) as t
group by t.id , t.iata_code 
having N >= %s
order by n asc"""

        cursor.execute(query, (n , ))

        for row in cursor:
            result.append(idMapAeroporti[row["ID"]])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , COUNT(*) as peso
from flights f 
group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        #for row in cursor:
            #result.append(idMapA[row["ORIGIN_AIRPORT_ID"]],
                          #idMapA[row["DESTINATION_AIRPORT_ID"]],
                          #row["peso"])

        for row in cursor:
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID , t1.DESTINATION_AIRPORT_ID , coalesce(t1.n,0) + coalesce(t1.n,0) as peso
                    FROM (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
                    left Join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID 
                    and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID 
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null
                    """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #                idMapA[row["DESTINATION_AIRPORT_ID"]],
            #                row["peso"]
            #                ))

            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result



