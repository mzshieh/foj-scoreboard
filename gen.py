import time
import datetime

def head(data):
	a='''
		<!DOCTYPE html>
			<html lang="en">
			<head>
				<!-- Required meta tags -->
				<meta http-equiv="content-type" content="text/html; charset=UTF-8">
				<meta http-equiv="content-language" content="English">
				<meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=yes">
				<meta name="keywords" content="Intorduction, Algorithms, Homework, Scoreboard, NCTU, CS">
				<meta name="discription" content="">
				<!-- title -->
				<title>HW{0}</title>
				<link rel="icon" type="image/png" href="https://lh3.googleusercontent.com/3txMoTdolI_JziAIDnOQuki1JeEbHXsGnMW-XdvxqL63cuYYqxrbwJ8VsL2jH5gjRdM-=w300">
				<!-- Bootstrap CSS -->
				<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
			</head>
			<body>
				<div class="container">
					<table class="table table-striped table-hover table-bordered">
					<caption class="text-center" style="caption-side: top">
						<h2 style="color: #000000;">Homework {1} - Scoreboard</h2>
					</caption>
					<caption class="text-right" style="caption-side: bottom">
						<em><small>Generated at {2}</small></em>
					</caption>
		'''
	st=datetime.datetime.now()
	return a.format(data, data, st)

def tail():
	return '</table></div></body></html>'

def thead(data):
	ret='<thead><tr>'
	for s in data:
		ret+='<th class="text-center">{0}</th>'.format(s)
	return ret+'</tr></thead>'

def tbody(data):
	ret='<tbody>'
	data = list(data.items())
	data.sort()
	for S, T in data:
		ret+='<tr><td class="text-center">{0}</td>'.format(S)
		for s in T:
			if s<0:
				s=c=''
			elif s==100:
				c='table-success'
			else:
				c='table-danger'
			ret+='<td class="text-center {0}">{1}</td>'.format(c, s)
		ret+='</tr>'
	return ret+'</tbody>'

def table(I, H, B):
	html=''
	html+=head(I)
	html+=thead(H)
	html+=tbody(B)
	html+=tail()
	return html
