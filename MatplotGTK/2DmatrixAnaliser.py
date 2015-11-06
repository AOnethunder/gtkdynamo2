import os, sys

def find_minimum_path (X_norm, outpath = None):
	
	if outpath == None:
		outpath = os.environ.get('HOME')                

	
	""" 
	
	#=============== generating the minimum energy reaction path ========================#
	#	plot 1D                                                                          #
	#														                             #
	#	lista   -  contain  the  energy valors 				                             #
	#	frame_list include the coordinates x and y (matrix)                              #
	#   X_norm  - Matrix - normalized                                                    #
	#   outpath - output path                                                            #
	#------------------------------------------------------------------------------------#
	
	
	"""
		

	
	lista , frame_list = minimum_path(X_norm)

	if not os.path.exists (outpath + "/MinimumPath"): os.mkdir (outpath + "/MinimumPath")
	MinimumPath = outpath + "/MinimumPath"	
	import shutil
	
	
							#--------------------------------#
							#     building the log file      #
							#--------------------------------#
	#=====================================================================================#	
	n = 0
	arq  = open(outpath+"/MinimumPath"+"/"+"process.log", "w")	                 #creates an process.log to save the minimum path energy data generated by the GTKDyn
	text = "----------  Generated by EasyHybrid  ----------\n\nThis proceeding might generate artifacts, the results should be interpreted with caution.\nFor further information, please acess: https://sites.google.com/site/EasyHybrid/ \n\nEnergy values in kJ/mol\n\n"
	
	
	#text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s" % (coord2_ATOM1,     coord2_ATOM1_name)
	for i in frame_list:
		shutil.copy2(outpath + '/frame_'+i+'.pkl', MinimumPath+'/frame'+str(n)+'.pkl')
		
		frame_x_y = 'frame_'+i+'.pkl'
		frame_new = 'frame'+str(n)+'.pkl'
		energy    =  str(lista[n])
		
		string = '%15s   --->   %15s   =   %15s\n' % (frame_x_y, frame_new, energy)
		
		#string = 'frame_'+i+'.pkl   --->  frame'+str(n)+'.pkl    = '+ str(lista[n])+' kJ/mol\n'
		text = text + string
		n = n + 1
	arq.writelines(text)
	arq.close()
	#=====================================================================================#	
	
	 
	frames = range(len(lista))
	return frames, lista
	#
	
	#self.render_plot( frames, lista )
	#render_plot(self, x, y, title = 'GTK Dynamo', xlabel = 'Frame', ylabel = 'Energy (kJ/mol)', grid_flag = True)
	return 0
	#(self, matrix, title = 'GTK Dynamo 2D SCAN', xlabel = 'r(3 - 4)', ylabel = 'r(1 - 2)'):


def minimum_path(X):
	lista = []
	px = 0
	py = 0

	# rminimum path energy frames
	frame_list = []
	frame = str(px)+ "_" +str(py)
	frame_list.append(frame)


	print X[px][py]
	lista.append(X[px][py])
	while 1 != 0:
		try:
			p1 = X[px+1][py+0]
		except:
			p1 = 1000000000000000
		try:
			p2 = X[px+0][py+1]
		except:
			p2 = 1000000000000000
		try:	
			p3 = X[px+1][py+1]
		except:
			p3 = 1000000000000000		
		
		
		if p3 < p2 and p3 < p1:
			print p3
			px = px + 1
			py = py + 1
			lista.append(p3)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p2 < p1 and p2 < p3:
			print p2
			px = px + 0
			py = py + 1
			lista.append(p2)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p1 < p2 and p1 < p3:
			print p1
			px = px + 1
			py = py + 0
			lista.append(p1)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
			
		if p1 == 1000000000000000 and p2 == 1000000000000000 and p3 == 1000000000000000:
			break
	return lista , frame_list
	
