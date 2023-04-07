import pymysql
import uvicorn 
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi import FastAPI

app = FastAPI()

# 데이터베이스 연결 설정


@app.get("/")
async def root():
    
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="54ecv9g8",
        database="dust_sensor",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    # SQL 쿼리 실행
    sql = "SELECT * FROM device_value"
    cursor.execute(sql)

    # 쿼리 결과 반환
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return result

@app.get("/insert_data")
async def insert_data(device_id: int, value1: int, value2: int = None, value3: int = None, value4: int = None,
                      value5: int = None, value6: int = None, value7: int = None, value8: int = None, value9: int = None,
                      value10: int = None, value11: int = None, value12: int = None, value13: int = None, value14: int = None):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="54ecv9g8",
        database="dust_sensor",
        cursorclass=pymysql.cursors.DictCursor
    )
    # 커서 생성
    cursor = connection.cursor()
    
    # 데이터 삽입 쿼리
    insert_query = "INSERT INTO device_value (device_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    # 쿼리 실행
    cursor.execute(insert_query, (device_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14))
    
    # 변경 내용을 커밋
    connection.commit()
    
    # 연결 종료
    cursor.close()
    connection.close()
    
    return {"message": "Data inserted successfully."}


if __name__ == '__main__': uvicorn.run(app=app,host="0.0.0.0",port=8000)

