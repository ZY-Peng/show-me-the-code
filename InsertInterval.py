# -*- coding: utf-8 -*-
def insert(intervals,interval):
	result=[]
	length=len(intervals)
	flag=0
	isInserted=False
	while flag<length:
		if isInserted:
			result.append(intervals[flag])
		elif intervals[flag][0]>interval[1]:
			result.append(interval)
			result.append(intervals[flag])
			isInserted=True
		elif intervals[flag][1]<interval[0]:
			result.append(intervals[flag])
		else :
			interval[0]=min(interval[0],intervals[flag][0])
			interval[1]=max(interval[1],intervals[flag][1])
		flag+=1
	if  not isInserted:
		result.append(interval)
	print(result)

insert([[3,5],[6,7],[8,10],[12,16]],[1,2])
