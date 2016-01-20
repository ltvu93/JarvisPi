# coding: utf-8
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
	else:
		return text_to_num_1(text)

def num_to_text_1(num):
	if num == 0:
		return " KHÔNG "
	elif num == 1:
		return " MỘT "
	elif num == 2:
		return " HAI "
	elif num == 3:
		return " BA "
	elif num == 4:
		return " BỐN "
	elif num == 5:
		return " NĂM "
	elif num == 6:
		return " SÁU "
	elif num == 7:
		return " BẢY "
	elif num == 8:
		return " TÁM "
	elif num == 9:
		return " CHÍN "



def num_to_text_2(num):
	if num < 10:
		return num_to_text_1(num)
	elif num < 100 and num >= 10:
		d = num / 10
		u = num % 10
		if d == 1:
			if u != 5:
				return " MƯỜI " + num_to_text_1(u)
			elif u == 0:
				return " MƯỜI "
			else:
				return " MƯỜI LĂM "
		else:
			if u == 1:
				return num_to_text_1(d) + " MƯƠI MỐT"
			elif u == 5:
				return num_to_text_1(d) + " MƯƠI LĂM"
			elif u == 0:
				return num_to_text_1(d) + " MƯƠI"
			else:
				return num_to_text_1(d) + " MƯƠI" + num_to_text_1(u)

def num_to_text_3(num):
	if num < 100:
		return num_to_text_2(num)
	elif num < 1000 and num >= 100:
		h = num / 100
		du = num % 100
		d = du / 10
		u = du % 10
		if d == 0:
			if u != 0:
				return num_to_text_1(h) + " TRĂM LINH" + num_to_text_1(u)
			else:
				return num_to_text_1(h) + " TRĂM"
		else:
			return num_to_text_1(h) + " TRĂM " + num_to_text_2(du)

def num_to_text(num):
	if num < 1000:
		return num_to_text_3(num)
	elif num < 10000 and num >= 1000:
		t = num / 1000
		hdu = num % 1000
		h = hdu / 100
		du = hdu % 100
		d = du / 10
		u = du % 10
		if hdu == 0:
			return num_to_text_1(t) + " NGHÌN "
		else:
			if h == 0:
				if d == 0:
					if u != 0:
						return num_to_text_1(t) + " NGHÌN " + num_to_text_1(h) + " TRĂM LINH" + num_to_text_1(u)
					else:
						return num_to_text_1(t) + " NGHÌN " + num_to_text_1(h) + " TRĂM"
				else:
                                        return num_to_text_1(t) + " NGHÌN " + num_to_text_1(h) + " TRĂM" + num_to_text_2(du)
			else:
				return num_to_text_1(t) + " NGHÌN " + num_to_text_3(hdu)

def find_num_and_replace(string):
        result = string
        chars = re.findall(r'[^A-Za-z0-9 đáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềễểệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵĐÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỄỂỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ]+', result, re.I)
        i = 0
        while (i < len(chars)):
                result = result.replace(str(chars[i]),"")
                i += 1
        number = re.findall(r'\d+', string)
        i = 0
        while (i < len(number)):
                result = result.replace(str(number[i]), str(num_to_text(int(number[i]))))
                i += 1
        return result
