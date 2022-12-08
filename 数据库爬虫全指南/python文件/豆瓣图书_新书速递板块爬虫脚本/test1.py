import re
a=' 45.00元'
price_path = str(re.findall(r'.*?(\d+.\d{2})元', a)[0])
print(price_path)

