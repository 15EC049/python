
import sys
import re

#----------------FILE_HANDLE----------------
err_file=open("convertion_error.txt", "w")
#----------------GLOBAL VARIABLES-------------
conv_svpp=0
conv_vpp=0
curr_lane=''
curr_lane_num=0
curr_file=''
lanes=["//======Allrights Reserved by Primesoc Technologies======="]
err=["Invalid Param declaration","File not found","Param not defined"]
#------------------DICTIONERIES-----------------
#Dictionery to store VPP param variables
vpp_param ={
		"NAME":"VPP_PARAM",
		"SCRIPT_DEBUG":0
	   }
#Dictionery to store SVPP param variables
svpp_param ={
		"NAME":"SVPP_PARAM",
		"SCRIPT_DEBUG":0
	    }
#Dictionery to store loop variables
loop_variable={
		"NAME":"LOOP_VARIABLE",
		"SCRIPT_DEBUG":0,
		"for_repeat":0,
		"if_repeat":0,
		"while_repat":0
	    }

#------------------FUNCTION DEFINITIONS-------------

#Error Log Function
def log_error(fil,st,e,lane,num):
	err_string="Error"
	if conv_svpp:
		err_string="SVPP_ERROR  "
	elif conv_vpp:
		err_string="VPP_ERROR  "

	err_string=err_string+fil+" || "+st+" "+err[e]
	
	if lane !="":
		err_string=err_string+" || Lane_num="+str(num)+"\n"
	#print err_string
	err_file.write(err_string)
#To add New value of update Existing
def add_to_param(param,key,value):
	param[key]=value;
	if(svpp_param["SCRIPT_DEBUG"]):
		print param["NAME"]+"->>"+key+"="+str(svpp_param[key])

def read_param(param,key):
	value=''
	try :
		value=param[key];
		if(param["SCRIPT_DEBUG"]):
			print param["NAME"]+"|Read|"+key+"="+str(param[key])
	except KeyError:	
		log_error(curr_file,key,2,curr_lane,curr_lane_num)
	return str(value)

#to read Verilog Files
def read_vpp_files(f_name):
	global curr_file
	try:
	 	fh= open(f_name, "r")
		curr_file=f_name
		for lane in fh:
			lane=lane.rstrip("\n")
			lanes.append(lane)
		convert(lanes)
		for x in range (1,len(lanes)):
			lanes.pop(x)
	except IOError:
		print f_name+":File Not Found"
		log_error(f_name,'',1,'',0)

#To read SystemVerilog Files
def read_svpp_file(f_name):
	global curr_file
	try:
	 	fh= open(f_name, "r")
		curr_file=f_name
		for lane in fh:
			lane=lane.rstrip("\n")
			lanes.append(lane)
		convert(lanes)
		for x in range (1,len(lanes)):
			lanes.pop()
	except IOError:
		print f_name+":File Not Found"
		log_error(f_name,'',1,'',0)

#Convert to Verilog or System Verilog
def convert(lanes):
	global curr_lane
	global curr_lane_num
	for lane in lanes:
		curr_lane=lane
		curr_lane_num=lanes.index(curr_lane)
		x = re.findall("`let", lane)
		if x:
			declare_param(lane)


def declare_param(lane):
	lane=lane.lstrip()
	key=''
	val=0
	t1=0
	global curr_lane
	if(re.findall("^`let", lane)):
		lane = re.sub("`let", "", lane)
		lane=lane.strip()
		t2=re.split("#|//",lane)
		x = t2[0].split("=")
		x[0]=x[0].strip()
		key=x[0]
		if len(x)==2:
			rhs=x[1]
			var=re.findall("\w+", rhs)
			print var
			if len(var)>1:
				for x in var:
					x=x.strip()
					y=unicode(x)
					if not y.isnumeric():
						try :
							t1=vpp_param[x] if conv_vpp  else svpp_param[x]
						except KeyError:	
							log_error(curr_file,x,2,curr_lane,curr_lane_num)
						rhs=re.sub(r"\b{}\b".format(x),str(t1), rhs)

				val=int(eval(rhs))
				add_to_param(vpp_param if conv_vpp  else svpp_param,key,val)
			else :
				var[0]=var[0].strip()
				y=unicode(var[0])
				if y.isnumeric():
					val=int(var[0])
				else :
					val = read_param(vpp_param if conv_vpp  else svpp_param,key)

				add_to_param(vpp_param if conv_vpp  else svpp_param,key,val)
					

		else :
			log_error(curr_file,'',0,curr_lane,curr_lane_num-1)
			
	
def assign_param():
	print lane
	

#===============Main Code==================
conv_svpp=1
conv_vpp=0
add_to_param(vpp_param if conv_vpp  else svpp_param,"SCRIPT_DEBUG",0)
read_svpp_file("param_tb.vpp")
#conv_svpp=0
#conv_vpp=1
#add_to_param(vpp_param if conv_vpp  else svpp_param,"SCRIPT_DEBUG",0)
#read_svpp_file("qdma_param.vpp")




#=============TEST AREA=======================
conv_svpp=1
conv_vpp=0
add_to_param(vpp_param if conv_vpp  else svpp_param,"SCRIPT_DEBUG",1)
print "HTC_QUEUE_DEPTH="+read_param(vpp_param if conv_vpp  else svpp_param,"HTC_QUEUE_DEPTH")	

