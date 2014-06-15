from django.shortcuts import render


from django.http import HttpResponse
from django.views.generic import View
from django.template import Template, Context, RequestContext


import requests
import json

from marshapp.pizza import Pizza
from marshapp.login import Login
from marshapp.rating import Rating
from django.http.response import HttpResponseRedirect


class MainView(View):

    def get(self, request, *args, **kwargs):
    
        lat = request.GET.get('lat','50')    
        lng = request.GET.get('lng','19')

        place = request.GET.get('place-id', '0')
        rating = request.GET.get('rating', '0')
        comment = request.GET.get('comment', None)
        
        login = request.GET.get('login', '')

        template = Template("""
            <html>
                <head>
                    <h3><title>Pizza Finder</title><h3>
                </head>
                <style>
                body
                    {
                      background: url(http://www.hdwallpapersimages.com/wp-content/uploads/2013/04/Delicious-Pizza.jpg) no-repeat center center fixed; 
                      -webkit-background-size: cover;
                      -moz-background-size: cover;
                      -o-background-size: cover;
                      background-size: cover;
                    }
                </style>
                <body>
                    <div style="
                    	background-color: rgba(255, 255, 255, 0.4); 
                    	width: 400px;
                        height: 200px;
                    	position: absolute;
                        top:0;
                        bottom: 0;
                        left: 0;
                        right: 0;
                    	margin: auto;
                    	border-radius: 10px;">
                    	
                    <h1 style="text-align:center;">Pizza Finder</h1>
                    <form>{% csrf_token %}
                        Latitude: <input type="text" name="lat"><br>
                        Longitude: <input type="text" name="lng"><br>
                        <input style="float:right" type="submit" value="Submit">
                    </form> 
                    </div>
                <ul>
                        <div style="
                        	background-color: rgba(255, 255, 255, 0.7); 
                        	width: 700px;
                            height: auto;
                        	position: absolute;
                            top:100;
                            bottom: 0;
                            left: 0;
                            right: 0;
                        	margin: auto;
                        	border-radius: 10px;">
                    {% for result in results %}
                        <li>
                            <b>{{ result.name }}</b> Your rating: {{result.myrating}}  Overall rating: {{result.overalrating}}<br />
                            <form action="">
                                <input type="hidden" name="login" value="{{ login }}" />
                                <input type="hidden" name="place-id" value="{{ result.id }}" />
                                <select name="rating">
                                    <option value="" disabled="disabled" selected="selected">Your rating</option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                </select><br />
                                <input type="submit" value="Submit">
                                <br />
                            </form>
                            <form action="">
                                <input type="hidden" name="login" value="{{ login }}" />
                                <input type="hidden" name="place-id" value="{{ result.id }}" />
                                <input type="text" name="comment" /><br />
                                <input type="submit" value="Submit">
                                <br />
                            </form>
                            <ul>
                            {% for comment in result.comments %}
                                <li><b>{{ comment.0 }}: </b>{{comment.1 }}</li>
                            {% endfor %}
                            </ul>
                        </li>
                        <hr />
                    {% endfor %}
                </div>
                </ul>
                </body>
            </html>
        """)
        if rating != '0':
            Rating.addRating(login, place, rating)
        if comment != None:
            Rating.addComment(login, place, comment)
        context = Context(Pizza.find(login, float(lat), float(lng),'AIzaSyAi76SIbkDWIal4aPHg5FPCk-fLvV-xSnc'))
        
        return HttpResponse(template.render(context))

class LoginView(View):

    def get(self, request, *args, **kwargs):
    
        login = request.GET.get('login','')    
        password = request.GET.get('pass','')

        template = Template("""
            <html>
            <div style="
                	background-color: rgba(255, 255, 255, 0.6); 
                	width: 400px;
                    height: 200px;
                	position: absolute;
                    top:0;
                    bottom: 100;
                    left: 0;
                    right: 0;
                	margin: auto;
                	border-radius: 10px;">
                <head>
                    <title>Pizza Finder - Login</title>
                </head>
                <style>
                body
                    {
                      background: url(http://www.hdwallpapersimages.com/wp-content/uploads/2013/04/Delicious-Pizza.jpg) no-repeat center center fixed; 
                      -webkit-background-size: cover;
                      -moz-background-size: cover;
                      -o-background-size: cover;
                      background-size: cover;
                    }
                    </style>
                <body>
                    <h1 style="text-align:center;">Pizza Finder</h1>
                    <form method="GET" action="">{% csrf_token %}
                        Login: <input  type="text" name="login"><br>
                        Password: <input  type="password" name="pass"><br><br>

                        <input style="float:right" type="submit" value="Login/Register">
                    </form> 
                </body>
                </div>
            </html>
        """)
        context = RequestContext(request)
        
        if Login.login(login, password):
            return HttpResponseRedirect("pizza?login="+login)
        else:
            if login == '':
                return HttpResponse(template.render(context))
            else:
                Login.register(login, password)
                return HttpResponseRedirect("pizza?login="+login)
            
