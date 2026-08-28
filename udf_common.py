from datetime import datetime,timedelta,date
from dateutil import tz
import pytz
from pytz import timezone
from dateutil.relativedelta import relativedelta
#import boto3

def get_help(fn):
	'''print function definition'''
	return fn.__doc__

def utc_convert(timestamp_utc , to_timezone='America/Chicago'):
	'''Converts a UTC timestamp to CST'''
	try:
		if len(timestamp_utc) == 13:
			to_zone = tz.gettz(to_timezone)
			converted_cst = datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%Y-%m-%d %H:%M:%S.%f')
			return converted_cst
		elif len(timestamp_utc) == 10:
			to_zone = tz.gettz(to_timezone)
			converted_cst = datetime.fromtimestamp(float(timestamp_utc), tz=to_zone).strftime('%Y-%m-%d %H:%M:%S.%f')
			return converted_cst
		else:
			return None
	except:
		return None

def timezone_convert(input_col, from_timezone, to_timezone='America/Chicago'):
	'''Convert from one timezone to another'''
	try:
		t = datetime.strptime(input_col, '%Y-%m-%d %H:%M:%S.%f')
		utcnow = timezone('utc').localize(datetime.utcnow()) # generic time
		from_zone = utcnow.astimezone(timezone(from_timezone)).replace(tzinfo=None)
		to_zone = utcnow.astimezone(timezone(to_timezone)).replace(tzinfo=None)
		offset = relativedelta(to_zone, from_zone) 
		to_zone = (t + timedelta(hours = offset.hours)).strftime('%Y-%m-%d %H:%M:%S.%f')
		return to_zone
	except:
		return None

def get_date_id(timestamp_utc):
	'''Get Date in CST from the UTC timestamp '''
	try:
		to_zone = tz.gettz('America/Chicago')
		year = datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%Y')
		month = datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%m')
		day = datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%d')
		date_id = year + '-' + month + '-' + day
		return date_id
	except:
		return '0'

def get_time_id(timestamp_utc):
	'''Get Seconds in CST(for that day) from UTC timestamp'''
	try:
		to_zone = tz.gettz('America/Chicago')
		hours = int(datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%H'))
		mins = int(datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%M'))
		secs = int(datetime.fromtimestamp(float(timestamp_utc)/1000.0, tz=to_zone).strftime('%S'))
		time_id = (hours*3600) + (mins*60) + (secs)
		return time_id
	except:
		return None

def is_digit(value):
	'''Check if the input arg passed is a digit(Integer value) or not'''
	if value:
		return str(value).isdigit()
	else:
		return False

def is_decimal(value):
	'''Check if the input arg passed is a decimal or not'''
	try:
		value = float(value)
		if value:
			return isinstance(value, float)
		else:
			return False
	except:
		return False

def replace_char(x, y, *args):
	'''Replace optional special characters(*args) in a column(x) that is passed to the function
	 with a value that needs to be replaced(y)'''
	for arg in args:
		if x is not None:
			s = x.replace(arg, y)
		else:
			return None
	return s

def get_index(x, y):
	'''Checks if a char(y) is present in the input string(x)'''
	s = str(x).find(y)
	return s

def modify_values(x, y, req_value, default):
	'''Return a value(y) if col x = req_value else return default'''
	if x.lower() == req_value:
		return y
	else:
		return default

def is_not_null_check(value):
	'''Check if the input argument is null or not'''
	if (value is not None and str(value) != ''):
		return True
	else:
		return False

def null_check(inputcol, default):
	'''Return default value if null else return the inputcolumn value itself'''
	if (inputcol is not None and inputcol.strip() != ''):
		return str(inputcol).strip()
	else:
		return default

def check_schema(x, y):
	diff_list = list(set(y) - set(x))
	if len(diff_list) != 0:
		#email_notification(', '.join(diff_list))
		print ('schema mismatch')
	else:
		print ('schema match')
		
def email_notification(x, y):
	session = boto3.Session(profile_name='dw_etl')
	client = session.client('ses',region_name='us-east-1')
	response = client.send_email(
		Destination={
		'ToAddresses': ['cvadapalli-contractor@cars.com']
		},
		Message={
		'Body': {
		'Text': {'Charset': 'UTF-8','Data': 'Expected Schema: \n' + x + '\n' + '\nInput File Schema: \n' + y}},
		'Subject': {'Charset': 'UTF-8','Data': 'schema_mismatch for ' + prefix}},
		Source='cvadapalli-contractor@cars.com'
		)

def digit_check(x, y, default, compare=None):
	'''Check if the input(x) passed is a decimal or not along with null checks '''
	if (str(compare).lower() == 'digit_check'):
		if (x is not None and str(x).strip() != '' and is_decimal(x)):
			x = y
		else:
			x = default
		return x
	else:
		if (x is not None and str(x).strip() != ''):
			x = y
		else:
			x = default
		return x

def length_check(x, l, y, default, compare=None):
	'''Check if the input col passed is null,length of input col passed is greater than or lesser than a certain value'''
	l = int(l)
	if (str(compare).lower() == 'greaterthan'):
		if (x is not None and str(x).strip() != '' and len(str(x).strip()) >= l):
			x = y
		else:
			x = default
		return x
	elif (str(compare).lower() == 'lesserthan'):
		if (x is not None and str(x).strip() != '' and len(str(x).strip()) <= l):
			x = y
		else:
			x = default
		return x

def length_digit_check(x, l, y, default, compare=None):
	'''Check if the ,length of input col passed is greater than or lesser than a certain value and 
	also check if the input col passed is a decimal or not'''
	l = int(l)
	if (str(compare).lower() == 'greaterthan'):
		if (x is None or str(x).strip() == '' or is_decimal(x) == False or len(str(x).strip()) >= l):
			x = default
		else:
			x = y
		return x
	elif (str(compare).lower() == 'lesserthan'):
		if (x is None or str(x).strip() == '' or is_decimal(x) == False or len(str(x).strip()) <= l):
			x = default
		else:
			x = y
		return x

def index_check(x, y, l, z, default, compare=None):
	'''Assign the value to the input col passed based on the condition if the input argument contains 
	a certain char(s)'''
	l = int(l)
	if (str(compare).lower() == 'greaterthan'):
		if (x is not None and str(x).strip() != '' and get_index(x,y) >= l):
			x = z
		else:
			x = default
		return x
	elif (str(compare).lower() == 'lesserthan'):
		if (x is not None and str(x).strip() != '' and get_index(x,y) <= l):
			x = z
		else:
			x = default
		return x