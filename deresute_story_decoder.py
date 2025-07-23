import os,re,base64

dic_cmd = {
0:"title",1:"outline",2:"chara",3:"visible",
4:"type",5:"face",6:"focus",7:"background",
8:"print",9:"tag",10:"goto",11:"bgm",
12:"touch",13:"choice",14:"vo",15:"wait",
16:"in_L",17:"in_R",18:"out_L",19:"out_R",
20:"fadein",21:"fadeout",22:"in_float",23:"out_float",
24:"jump",25:"shake",26:"pop",27:"nod",
28:"question_right",29:"question_left",
30:"se",31:"black_out",32:"black_in",33:"white_out",
34:"white_in",35:"transition",36:"situation",37:"color_fadein",
38:"flash",39:"shake_text",40:"text_size",41:"shake_screen",
42:"double",43:"flower_y",44:"flower_r",45:"concent",
46:"find_l",47:"find_r",48:"laugh_l",49:"laugh_r",
50:"chord_l",51:"chord_r",52:"sweat_l",53:"sweat_r",
54:"question_l",55:"question_r",56:"angry",57:"drop_l",58:"drop_r",
59:"live",60:"scale",61:"title_telop",62:"window_visible",63:"log",
64:"novoice",65:"attract",66:"change",67:"fadeout_all",
}

def SplitCommandByteRow(bytes_data: bytearray) -> list:
	data_size=len(bytes_data)
	result= []
	i = 0
	while (i < data_size):
		cmd_id=int.from_bytes(bytes_data[i:i+2], byteorder='big')
		#print(bytes_data[i:i+2])
		ptr = i+2
		cmd_data=[]
		while True:
			length = int.from_bytes(bytes_data[ptr:ptr+4], byteorder='big')
			if ( length == 0 ):
				break
			data_byte = bytes_data[ptr+4:ptr+4+length]
			cmd_data.append(bytes(data_byte))
			ptr = ptr+4+length
		i = ptr+4
		cmd_data=DeserializeLine(cmd_data)
		result.append([cmd_id,cmd_data])
	return result

def BitInverse(byte_in: bytearray) -> bytearray:
	num = len(byte_in)
	byte_out=bytearray()
	for i in range(num):
		if (i % 3 == 0):
			byte_out.append((~byte_in[i]) & 0xFF)
		else:
			byte_out.append(byte_in[i])
	return byte_out

def DeserializeLine(cmd_byte: list) -> list:
	cmd_data = []
	for i in range(0, len(cmd_byte)):
		byte_args_inv=BitInverse(cmd_byte[i])
		string_b64 = byte_args_inv.decode('utf-8')
		bytes_decoded = base64.b64decode(string_b64)
		cmd_data.append(bytes_decoded.decode('utf-8'))
	if (cmd_data == []):
		cmd_data.append("Null")
	return cmd_data

#main
if not os.path.exists("./out"):
        os.mkdir("./out")

pattern = re.compile(r'.*storydata_.*.bytes')
input_files=os.listdir("./")
for input_file in input_files:
	input_name = os.path.splitext(os.path.basename(input_file))[0]
	if pattern.match(input_file):
		print("input file:",input_file)
		with open(os.path.basename(input_file), 'rb') as file:
			bytes_data = file.read()
		#list format:[id,data]
		cmd_list = SplitCommandByteRow(bytes_data)
		output_file='./out/'+input_name+'.txt'
		with open(output_file, 'w',encoding='utf-8') as outfile:
			print("output file:",output_file)
			for data in cmd_list:
				outfile.write("id:"+str(data[0])+" | cmd:"+str(dic_cmd.get(data[0]))+'\n')
				outfile.write("data:"+str(data[1])+'\n\n')

	else:
		print("input file:",input_file,"unmatch")
		continue

print('decode done')
os.system('pause')
