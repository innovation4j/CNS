import logging
import logging.handlers
import os
import datetime

global current_date

# 현재 파일 경로 및 파일명 찾기
current_dir = os.path.dirname(os.path.realpath(__file__))
current_file = os.path.basename(__file__)
current_file_name = current_file[:-3]  # xxxx.py
current_date = datetime.datetime.now().strftime("%Y%m%d")
current_date = '20210822'

LOG_FILENAME = './logs/iot-{}.log'.format(current_date)
FLAG_PRINT = 'FLAG_PRINT'
FLAG_LOG = 'FLAG_LOG'
FLAG_WAIT = 0
FLAG_WORK = 1

LOG_FLAG = FLAG_LOG
PRINT_FLAG = FLAG_WAIT

# 로그 저장할 폴더 생성

log_dir = f"logs/"
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

# 로거 생성
iotlog = logging.getLogger('iot') # 로거 이름: test
iotlog.setLevel(logging.DEBUG) # 로깅 수준: DEBUG

def LOG(f_eqptid, f_dir, f_msg):
  global current_date
  if current_date != datetime.datetime.now().strftime("%Y%m%d") : 
    current_date = datetime.datetime.now().strftime("%Y%m%d")

  if LOG_FLAG == FLAG_LOG:
    sub_dir = f'{log_dir}/{f_eqptid}/{current_date}/{f_dir}'

    if not os.path.exists(sub_dir):
      os.makedirs(sub_dir)
      
    LOG_FILENAME = sub_dir+f'/{current_date}_{f_eqptid}_{f_dir}.log'

    # # 핸들러 생성
    file_handler = logging.handlers.TimedRotatingFileHandler(
      filename=LOG_FILENAME, when='midnight', interval=1,  encoding='utf-8'
      ) # 자정마다 한 번씩 로테이션

    iotlog.removeHandler(file_handler)
    for h in iotlog.handlers:
      iotlog.removeHandler(h)

    iotlog.addHandler(file_handler) # 로거에 핸들러 추가
    formatter = logging.Formatter(
      '%(asctime)s  %(message)s'
      )
    file_handler.setFormatter(formatter) # 핸들러에 로깅 포맷 할당

    iotlog.info(str(f_msg))
  if LOG_FLAG == FLAG_PRINT:
    print(f_msg)

def EXP_LOG(f_eqptid, f_msg):
  global current_date
  if current_date != datetime.datetime.now().strftime("%Y%m%d") : 
    current_date = datetime.datetime.now().strftime("%Y%m%d")

  if LOG_FLAG == FLAG_LOG:
    sub_dir = f'{log_dir}/{f_eqptid}/{current_date}/EXP'
    
    if not os.path.exists(sub_dir):
      os.makedirs(sub_dir)
      
    EXP_LOG_FILENAME = sub_dir+f'/{current_date}_{f_eqptid}_EXP.log'

    # 핸들러 생성
    file_handler = logging.handlers.TimedRotatingFileHandler(
      filename=EXP_LOG_FILENAME, when='midnight', interval=1,  encoding='utf-8'
      ) # 자정마다 한 번씩 로테이션

    iotlog.removeHandler(file_handler)
    for h in iotlog.handlers:
      iotlog.removeHandler(h)

    iotlog.addHandler(file_handler) # 로거에 핸들러 추가
    formatter = logging.Formatter(
      '%(message)s'
      )
    file_handler.setFormatter(formatter) # 핸들러에 로깅 포맷 할당

    iotlog.info(str(f_msg))
  if LOG_FLAG == FLAG_PRINT:
    print(f_msg)


if __name__ == "__main__":
    LOG('3','iot log test')