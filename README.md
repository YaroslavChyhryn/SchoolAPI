# Task 10 - SQL
Application that inserts/updates/deletes data in the database using sqlalchemy and flask rest framework.

<br>ApiDocs - ```/apidocs```, also  redirect from root - ```/```

## Installation
1. Install - [PostgreSQL](https://www.postgresql.org/).
2. Create user and database. Assign all privileges on the database to the user.
3. Modify - **local_config.py** with your user and database. 

4. Create tables in database:
```python manager.py createtables```
<br/>or create tables and generated data:
```python manager.py testdb```
6. Run server:
```python manager.py runserver```
## Manager help
1. Run  server:
``` python manage.py runserer```
2. Create tables in database:
``` python manage.py createtables```
3. Drop tables in database:
``` python manage.py droptables```
4. Generate and insert to database test data:
``` python manage.py testdb```
## Example
##### 1.Find all groups with less or equals student count.
```bash
curl -X GET -d "max_students=10" http://localhost:5000/api/v1/groups
```
##### 2.Find all students related to the course with a given name.
```bash
curl -X GET -d "course_name=Math" http://localhost:5000/api/v1/students
```
##### 3.Add new student
```bash
curl -X POST -H "Content-Type: application/json" --data "{\"first_name\":\"test1\",\"last_name\":\"test2\",\"group_id\":7}" http://localhost:5000/api/v1/students
```
##### 4.Delete student by STUDENT_ID
```bash
curl -X DELETE http://localhost:5000/api/v1/students/5
```
##### 5.Add a student to the course (from a list)
```bash
curl -X POST -H "Content-Type: application/json" --data "{\"students\": [1, 2, 3]}" http://localhost:5000/api/v1/courses/5/students
```
##### 6.Remove the student from one of his or her courses
```bash
curl -X DELETE -H "Content-Type: application/json" --data "{\"courses\":[1, 2, 3]}" http://localhost:5000/api/v1/students/5/courses
```
### Coverage report:
```bash
coverage report --omit="*venv\*","*tests\*"
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
school_api\__init__.py                    0      0   100%
school_api\app.py                        15      1    93%
school_api\config.py                     27      0   100%
school_api\data_generator.py             51      0   100%
school_api\db.py                          7      0   100%
school_api\local_config.py                2      0   100%
school_api\models\__init__.py             1      0   100%
school_api\models\models.py              27      3    89%
school_api\resources\__init__.py          0      0   100%
school_api\resources\v1\__init__.py       0      0   100%
school_api\resources\v1\api.py           16      0   100%
school_api\resources\v1\course.py        64      4    94%
school_api\resources\v1\group.py         63      2    97%
school_api\resources\v1\parser.py        19      0   100%
school_api\resources\v1\student.py       76      5    93%
school_api\schema\__init__.py             0      0   100%
school_api\schema\school_schema.py       17      0   100%
school_api\services\__init__.py           0      0   100%
school_api\services\services.py          75      0   100%
---------------------------------------------------------
TOTAL                                   460     15    97%

```
### Todo list
- [x] Consume json
- [ ] Validation 
- [ ] Response formats json/xml
- [ ] Auth
- [x] Swagger
- [x] Test happy path
- [ ] Test exceptional cases
- [ ] Child relationship as url in response, depth param
## License
[MIT](https://choosealicense.com/licenses/mit/)