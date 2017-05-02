import re
from collections import OrderedDict
import copy
import redistool

dic = OrderedDict()
prev_dic = OrderedDict()
process_step = "unprocessed"

def add_ffmpeg_state_to_redis(taskid, line):	
	# pdb.set_trace()
	global process_step  
	global prev_dic
	global dic
	# state line
	if line =='all_complete\n':
		dic['all_complete'] = 'all complete! Please download file in file list!'
		process_step = 'all_complete'
	

	#get line content
	if process_step == 'unprocessed':
		global process_total_time
		
		reobj = re.compile(r'.*?Duration:.*?start.*?bitrate.*?')
		if reobj.match(line):
			head = line.find('Duration:')
			process_time_list = line[int(head)+10:int(head)+20].split(':')
			process_total_time = (float(process_time_list[0])*3600+float(process_time_list[1])*60+float(process_time_list[2]))

		reobj = re.compile(r'.*?size.*?time.*?bitrate.*?')
		if reobj.match(line):	
			present = line.find('time')
			process_now_list = line[int(present)+5:int(present)+15].split(':')
			process_now_time = (float(process_now_list[0])*3600+float(process_now_list[1])*60+float(process_now_list[2]))
			dic[process_step] = 'Transcoding :' + str(line[:-1]) + ' schedule: %0.1f %% ...'% (float(process_now_time/process_total_time)*100)
			
	elif process_step == 'all_complete':
		pass
	if dic != prev_dic:
		redistool.redis_set('_'.join(["task","status",taskid]), "Begin to process one task...\n" + '\n'.join(dic.values()))	
	prev_dic = copy.deepcopy(dic)
	
