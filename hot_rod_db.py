import sql 
from sql import SQL

HOT_ROD_DB = 'hot_rod.db'

DIRECTION_MOTOR_TABLE = 'DIRECTION_MOTOR'
LAST_ANGLE_COL = 'LAST_ANGLE'

class Database:
    @staticmethod
    def createDirectionTable():
        SQL.createTable(DIRECTION_MOTOR_TABLE, {
            LAST_ANGLE_COL: sql.INTEGER
        }, HOT_ROD_DB)
        if not SQL.rowCount(DIRECTION_MOTOR_TABLE, HOT_ROD_DB):
            SQL.insert(
                DIRECTION_MOTOR_TABLE,
                {LAST_ANGLE_COL: 0},
                HOT_ROD_DB
            )
    
    @staticmethod
    def saveLastDirectionMotorAngle(angle:int):
        SQL.simpleUpdate(
            DIRECTION_MOTOR_TABLE,
            LAST_ANGLE_COL,
            angle,
            HOT_ROD_DB
        )

    @staticmethod
    def getLastDirectionMotorAngle():
        return SQL.value(DIRECTION_MOTOR_TABLE, LAST_ANGLE_COL, 'id', 1, HOT_ROD_DB)
        