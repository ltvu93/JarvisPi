import re

def text_to_num_1(text):
	if text == "KHÔNG":
		return 0
	elif text == "MỘT" or text == "MỐT":
		return 1
	elif text == "HAI":
		return 2
	elif text == "BA":
		return 3
	elif text == "BỐN" or text == "TƯ":
		return 4
	elif text == "NĂM" or text == "LĂM":
		return 5
	elif text == "SÁU":
		return 6
	elif text == "BẢY":
		return 7
	elif text == "TÁM":
		return 8
	elif text == "CHÍN":
		return 9

def text_to_num_2(text):
	if "MƯỜI" in text or "MƯƠI" in text:
		if "MƯỜI" in text:
			u = text.split("MƯỜI")
			if u[1] != "":
				num = u[1].strip()
				return 10 + int(text_to_num_1(num))
			else:
				return 10
		elif "MƯƠI" in text:
			u = text.split("MƯƠI")
			if u[1] != "":
				num0 = u[0].strip()
				num1 = u[1].strip()
				return int(text_to_num_1(num0)) * 10 + int(text_to_num_1(num1))
			else:
				num0 = u[0].strip()
				return int(text_to_num_1(num0)) * 10