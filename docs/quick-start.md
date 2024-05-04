# Airflow In Action

https://airflow.apache.org/docs/apache-airflow/stable/start.html

## Installation

1. Set home directory
   `~/airflow` by default
```bash
export AIRFLOW_HOME=${PWD}/airflow
```
2. Install Airflow
```bash
sh airflow-install.sh
```

3. run Airflow
- initialize the database
- create the default user
- start the web server
```bash
airflow standalone
```

4. access the web server
http://localhost:8080

## Configuration
1. airflow.cfg: [Configuration reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
2. Admin -> Configuration

| 설정 카테고리 | 설정 이름 | 설명 | 예시 |
|--------------|-----------|------|------|
| 핵심(Core) | `dags_folder` | DAG 파일이 저장되는 절대 경로입니다. | `/home/user/airflow/dags` |
| 핵심(Core) | `hostname_callable` | 호스트명을 결정하는 함수의 경로입니다. | `airflow.utils.net.getfqdn` |
| 핵심(Core) | `might_contain_dag_callable` | Python 파일이 DAG를 포함하고 있는지 확인하는 함수의 경로입니다. | `airflow.utils.file.might_contain_dag_via_default_heuristic` |
| 핵심(Core) | `default_timezone` | 시간대의 기본값 설정입니다. | `UTC` |
| 핵심(Core) | `executor` | Airflow가 사용할 실행기 클래스입니다. | `LocalExecutor` |
| 핵심(Core) | `auth_manager` | 인증 관리자 클래스의 경로입니다. | `airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager` |
| 핵심(Core) | `parallelism` | 동시에 실행될 수 있는 최대 태스크 인스턴스 수입니다. | `32` |
| 핵심(Core) | `max_active_tasks_per_dag` | 각 DAG가 동시에 실행할 수 있는 최대 태스크 인스턴스 수입니다. | `16` |
| 핵심(Core) | `dags_are_paused_at_creation` | DAG가 생성될 때 기본적으로 일시 중지되는지 여부입니다. | `True` |
| 핵심(Core) | `max_active_runs_per_dag` | 각 DAG의 최대 활성 실행 수입니다. | `16` |
| 핵심(Core) | `load_examples` | 예제 DAG를 로드할지 여부입니다. | `False` (프로덕션 환경에서 사용) |
| 핵심(Core) | `plugins_folder` | 플러그인이 저장된 폴더의 경로입니다. | `/home/user/airflow/plugins` |
| 핵심(Core) | `fernet_key` | 데이터베이스에 저장된 연결 비밀번호를 암호화하는 데 사용되는 키입니다. | `cF1QePbIz9tOYQeS16P0q3RbuVpTXs3O13UsPws1MGA=` |
| 데이터베이스(Database) | `sql_alchemy_conn` | 메타데이터 데이터베이스에 대한 SqlAlchemy 연결 문자열입니다. | `postgresql+psycopg2://airflow:airflow@localhost/airflow` |
| 로깅(Logging) | `base_log_folder` | 로그 파일을 저장할 기본 폴더의 경로입니다. | `/home/user/airflow/logs` |
| 로깅(Logging) | `remote_logging` | 로그를 원격 위치에 저장할지 여부입니다. | `True` (AWS S3 같은 외부 스토리지 사용 시) |
| 스케줄러(Scheduler) | `catchup_by_default` | 스케줄러가 기본적으로 DAG 실행을 추적할지 결정합니다. | `False` (과거 실행 누락 방지) |
| 웹서버(Webserver) | `web_server_port` | 웹서버가 사용할 포트 번호입니다. | `8080` |
| 웹서버(Webserver) | `web_server_host` | 웹서버가 사용할 호스트 주소입니다. | `0.0.0.0` (모든 IP에서 접근 허용) |
| 이메일(Email) | `email_backend` | 이메일 알림을 보내는 데 사용할 백엔드입니다

## Production
- [Production Deployment](https://airflow.apache.org/docs/apache-airflow/stable/production-deployment.html)
```bash
# initialize the meta data db to the newest version 
airflow db migrate

# create the default user to access to web server
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

# start the web server
airflow webserver --port 8080

# start the scheduler
# 1. check dag folder and update the status of the tasks
# 2. scheduler will add tasks to queue
# 3. send tasks to the workers
# 4. workers will execute the tasks
# 5. workers will update the status of the tasks
# 6. scheduler will update the status of the tasks
airflow scheduler
```
> if you don't set home direction (`export AIRFLOW_HOME=${PWD}/airflow`), 
> commands won't run as expected

change web server user password
```bash
 airflow users reset-password --username admin
```

## Commands
You can run command to run tasks or dags
```bash
# airflow tasks test <dag_id> <task_id> <start_date>
airflow tasks test example_bash_operator runme_0 2015-01-01
```
```bash
# airflow dags backfill <dag_id> --start-date <start_date> --end-date <end_date>
airflow dags backfill example_bash_operator \
    --start-date 2015-01-01 \
    --end-date 2015-01-02
```