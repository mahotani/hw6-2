#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import os
import json, codecs
import jinja2
import cgi

f=codecs.open("station.json","r","utf-8")
trainData=json.load(f)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def render(self, html, values={"graph": trainData}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))
    def get(self):
        self.render("hw6-3.html")

class ResultPage(webapp2.RequestHandler):
    def render(self, html, values={"graph": trainData}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))

    def get(self):
        station1=cgi.escape(self.request.get(u"station1"))
        station2=cgi.escape(self.request.get(u"station2"))
        trainLine=[u"山手線",u"東横線",u"目黒線",u"地上線",u"多摩川線",u"大井町線",u"日比谷線"]
        fromToData=[]
        fromTrain=[]
        toLine=[]
        toTrain=[]
        fromLine=[]
        length=0
        for dict in trainData:
            length+=1
            if station1 in dict.get(u"Stations"):
                fromLine.append(1)
                fromTrain.append(dict.get(u"Name"))
            else:
                fromLine.append(0) 

        for dict in trainData:    
            if station2 in dict.get(u"Stations"):
                toLine.append(1)
                toTrain.append(dict.get(u"Name"))
            else:
                toLine.append(0)

        print(fromTrain)
        print(toTrain)

        i=0
        while i<length:
            if fromLine[i] == toLine[i] and fromLine[i]==1:
                fromToData.append({"print":u"出発地 : "+station1})
                fromToData.append({"print":trainLine[i]})
                fromToData.append({"print":u"目的地 : "+station2})
                fromToData.append({"print":"*****************************"})     
            i+=1

        if fromToData==[]:
            for everyLine in fromTrain:
                index=trainLine.index(everyLine)
                stationList=trainData[index].get(u"Stations")
                for station in stationList:
                    for everyLine2 in toTrain:
                        index2=trainLine.index(everyLine2)
                        if station in trainData[index2].get(u"Stations"):
                            fromToData.append({"print":u"出発地 : "+station1})
                            fromToData.append({"print":trainLine[index]})
                            fromToData.append({"print":u"乗り換え駅 : "+station})
                            fromToData.append({"print":trainLine[index2]})
                            fromToData.append({"print":u"目的地 : "+station2})
                            fromToData.append({"print":"*****************************"})
        
        if fromToData==[]:
            for everyLine in fromTrain:
                index=trainLine.index(everyLine)
                stationList2=trainData[index].get(u"Stations")
                for station in stationList2:
                    for train in trainLine:
                        if train==everyLine:
                            continue
                        index3=trainLine.index(train)
                        if station in trainData[index3].get(u"Stations"):
                            for everyStation in trainData[index3].get(u"Stations"):
                                for everyLine2 in toTrain:
                                    if everyLine2==everyLine:
                                        continue
                                    index4=trainLine.index(everyLine2)
                                    if everyStation in trainData[index4].get(u"Stations"):
                                        fromToData.append({"print":u"出発地 : "+station1})
                                        fromToData.append({"print":everyLine})
                                        fromToData.append({"print":u"乗り換え駅 : "+station})
                                        fromToData.append({"print":trainLine[index3]})
                                        fromToData.append({"print":u"乗り換え駅 : "+everyStation})
                                        fromToData.append({"print":trainLine[index4]})
                                        fromToData.append({"print":u"目的地 : "+station2})
                                        fromToData.append({"print":"*****************************"})
                                        break
        print(fromToData)
        self.render("hw6-4.html",values={"graph2": fromToData})
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/output", ResultPage)
], debug=True)