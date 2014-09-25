


def func():
	a = {}
	try:
		print a["not_Key"]
	except:
		print "Error"
	print "below exception"
	a["t"] = "|".join([])
	print a['t']
if __name__ == "__main__":
	func()
