import pymysql
import uvicorn 
from fastapi.responses import HTMLResponse

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import urllib

app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

def my_url_for(request: Request, name: str, **path_params: any) -> str:
    url = request.url_for(name, **path_params)
    parsed = list(urllib.parse.urlparse(url))
    # parsed[1] = '52.79.233.189' 
    parsed[1] = '127.0.0.1:8000'
    
    # parsed[1] = 'airfit.ai'  # Change the domain name
    return urllib.parse.urlunparse(parsed)

app.mount("/static", StaticFiles(directory="static"), name="static") 
#app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules") 

templates = Jinja2Templates(directory="templates") 
templates.env.globals['my_url_for'] = my_url_for

@app.get("/login", response_class=HTMLResponse) 
async def login(request: Request): 
	return templates.TemplateResponse("login.html", {"request": request}) 


# @app.route('/auth', methods=['POST'])
# def auth():
#     # 클라이언트에서 보낸 폼 데이터 가져오기
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # FastAPI의 /login 엔드포인트에 로그인 요청 전달
#     response = app.post('/login', json={'username': username, 'password': password})

#     # 로그인 실패 시 Flask에서 예외 발생
#     if response.status_code != 200:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     # 로그인 성공 시 Flask에서 메인 페이지로 리디렉션
#     return app(my_url_for('main'))


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="54ecv9g8",
    database="dust_sensor",
    cursorclass=pymysql.cursors.DictCursor
)

@app.on_event("shutdown")
async def shutdown_event():
     conn.close()

@app.get("/main", response_class=HTMLResponse) 
async def main(request: Request): 
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM device"
            cursor.execute(sql)
            devices = cursor.fetchall()
            if devices is None:
                return {"message": "Data not found"}
            else:
                return templates.TemplateResponse("main.html", {"request": request, "devices": devices, "user": ""})
    except Exception as e:
        return {"error": str(e)}


@app.post("/update_data")
async def update_device(data: dict):
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM device_value WHERE did = " + str(data['id']) + " ORDER BY timestamp DESC LIMIT 1"
            cursor.execute(sql)
            device = cursor.fetchone()
            if device is None:
                return {"message": "Data not found"}
            else:
                return {"value": device}
    except Exception as e:
        return {"message": "error"}
    
    
@app.post("/update_base_data")
async def update_base_device(data: dict):
    print(data)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE device SET ALERT_V_RATE1 = %s, ALERT_V_RATE2 = %s, ALERT_V_RATE3 = %s WHERE ID = %s"
            values = (data['alert_v_rate1'], data['alert_v_rate2'], data['alert_v_rate3'], data['id'])
            cursor.execute(sql, values)
            conn.commit()
            
            return {"message": "success"}
    except Exception as e:
        print(e)
        return {"message": "error"}


# @app.post("/chart")
# async def chart(data: dict):
#     try:
#         with conn.cursor() as cursor:
#             sql = "SELECT * FROM device_value WHERE did = " + str(data['id']) + " ORDER BY timestamp DESC LIMIT 1000"
#             cursor.execute(sql)
#             device = cursor.fetchone()
#             if device is None:
#                 return {"message": "Data not found"}
#             else:
#                 return {"value": device}
#     except Exception as e:
#         return {"message": "error"}

# db 에서 데이터 가져와서 넘겨준다.

# import jwt
# import secrets



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # JWT 토큰 설정
# SECRET_KEY = secrets.token_urlsafe(32)
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# #ID USER NAME PASSWORD EMAIL ORG(String) DEVICE_ID(Int) AUTH_LEVEL(Int) CREATE_AT
# class User(BaseModel):
#     username: str
#     email: str
#     password: str


# def create_user(user: User):
#     hashed_password = pwd_context.hash(user.password)
    
    
# @app.post("/signup")
# async def signup(user: User):
#     existing_user = get_user(user.username)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     create_user(user)
#     return {"message": "User created successfully"}


# def get_user(username: str):
#     print()
#     # 데이터베이스에서 해당 사용자 정보 가져오기
#     # ...

# # JWT 토큰 생성 함수
# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# @app.route('/login')
# def login():
#     return render_template('login.html')



# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user(form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     if not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get("/insert")
async def insert_data(did: int, 
                      v1: int, v2: int = None, v3: int = None, 
                      c1: int = None, c2: int = None, c3: int = None, 
                      e1: int = None, e2: int = None, e3: int = None,
                      r1: int = None, r2: int = None, r3: int = None, r4: int = None, r5: int = None):
    if did == 0: 
        return

    try:
        with conn.cursor() as cursor:
            insert_query = "INSERT INTO device_value (did, v1, v2, v3, c1, c2, c3, e1, e2, e3, r1, r2, r3, r4, r5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (did, v1, v2, v3, c1, c2, c3, e1, e2, e3, r1, r2, r3, r4, r5))
            conn.commit()
            
            return {"message": "Data inserted successfully."}
    except Exception as e:
        return {"error": str(e)}
    
    

if __name__ == '__main__': uvicorn.run(app=app,host="0.0.0.0",port=8000)

