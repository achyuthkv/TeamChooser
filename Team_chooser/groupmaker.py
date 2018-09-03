import os
import functools
from bottle import jinja2_view, route, run, redirect, request
import csv
import random


view = functools.partial(jinja2_view, template_lookup=['templates'])

@route('/',name='group')
@view('groupmaker.html')
def group():
	return { 'title':'Group Maker'}

@route('/', method="post")
@view('groupmaker.html')
def groupmaker():
	choose_file = request.forms.get('csvfile')
	membersInGroup=int(request.forms.get('groupsize',4))
	col_name=request.forms.get('col_name')


	L1 = []
	with open(choose_file, 'r' ,encoding='utf-8') as f:
		rd = csv.DictReader(f)

		for line in rd: 
			L1.append(f"{line[col_name]}")

	group=1
	#membersInGroup=int(input("Enter the number of people in the Group: "))
	check = membersInGroup

	with open('result.csv','w', newline='') as f:
		wr = csv.writer(f, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)

		for participant in L1[:]:               
			if membersInGroup==check:
				#print("Group {} consists of;".format(group))
				wr.writerow(f"Group {group} consists of : ")
				membersInGroup=0
				group+=1
			person=random.choice(L1)
			#print(person)
			wr.writerow(person)

			membersInGroup+=1
			L1.remove(str(person))
	return {}
	
if os.environ.get('APP_LOCATION') == 'heroku':
	run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
	run(host='localhost', port=8080, debug=True)			
