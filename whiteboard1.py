# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 19:11:44 2023

@author: Robert Stuckey
"""

import tkinter as tk
import math

def sqruler(point1,point2):
    return sum([(point1[i]-point2[i])**2 for i in range(0,2)])
def hyperuler(point1,point2):
    d=math.sqrt(sqruler(point1.position,point2.position))
    return 2*math.asinh(d/(2*math.sqrt(point1.position[1]*point2.position[1])))

def motion(event):
    x,y=event.x,event.y
    global cursor
    cursor=(x,y)
    if len(selected)>0:
        selected[0].move([x,y])
    #follower.move([x,y])

def move_object(cursor,chosen):
    if chosen==[]:
        return
    global selected
    if len(selected)==0:
        selected.append(chosen)
        #chosen.select()
    else:
        selected=[]
        
def segment_maker(cursor,chosen):
    global selected
    global templist
    templist.append(chosen)
    if len(templist)==1:
        pass
    else:
        segment(canvas,templist[0],templist[1])
        templist=[]

def circle_point(chosen):
    global templist
    templist.append(chosen)
    if len(templist)==1:
        pass
    else:
        radius=math.sqrt(sqruler(templist[0].position,templist[1].position))
        ctemp=circle(canvas,templist[0],radius)
        templist[1].dependencies.append(ctemp)
        ctemp.dependencies.append(templist[1])


def hyperline(chosen):
    global templist
    templist.append(chosen)
    if len(templist)==1:
        pass
    else:
        hyperbolic_line(universe=canvas,point1=templist[0],point2=templist[1])


def onclick(event):
    global cursor
    x, y = event.x, event.y
    cursor=(x,y)
    if x<360 and x>0 and y<360 and y>0:
        for i in point.point_list:
            if sqruler(cursor,i.position)<100:
                chosen=i
                break
            else:
                chosen=[]
        exec(radio_dictionary[var.get()])
    else:
        pass

   
class point():
    point_list=[]
    def __init__(self,universe,position=[0,0],color="blue",highlight="red"):
        self.radius=2
        self.position=position
        self.widget=universe.create_oval(position[0]+self.radius,position[1]+self.radius,position[0]-self.radius,position[1]-self.radius,fill='red',outline='red')
        self.highlight=highlight
        self.universe=universe
        self.__class__.point_list.append(self)
        self.dependencies=[]
        
    def move(self,new=[0,0]):
        self.universe.coords(self.widget,new[0]+self.radius,new[1]+self.radius,new[0]-self.radius,new[1]-self.radius)
        for i in self.dependencies:
            i.adjust(new,self)
        self.position=new

class segment():
    segment_list=[]
    def __init__(self,universe,point1,point2,color="black"):
        self.universe=universe
        self.widget=universe.create_line(point1.position[0],point1.position[1],point2.position[0],point2.position[1])
        point1.dependencies.append(self)
        point2.dependencies.append(self)
        self.vertices=[point1,point2]
        self.__class__.segment_list.append(self)
    
    def adjust(self,new,point):
        temp=[x for x in self.vertices if x != point][0]
        self.universe.coords(self.widget,new[0],new[1],temp.position[0],temp.position[1])
        
    #def select(self):
    #    self.universe.config(self.widget,color=self.highlight)
class circle():
    circle_list=[]
    def __init__(self,universe,center,radius):
        self.universe=universe
        self.center=center
        self.radius=radius
        self.widget=universe.create_oval(center.position[0]+radius,center.position[1]+radius,center.position[0]-radius,center.position[1]-radius)
        center.dependencies.append(self)
        self.dependencies=[]
        #self.widget.config(bg='')
    
    def adjust(self,new,point):
        if point==self.center:
            for i in self.dependencies:
                inew=[i.position[x]+new[x]-point.position[x] for x in range(0,2)]
                i.move(inew)
            self.universe.coords(self.widget,new[0]+self.radius,new[1]+self.radius,new[0]-self.radius,new[1]-self.radius)
        else:
            self.radius=math.sqrt(sqruler(point.position,self.center.position))
            self.universe.coords(self.widget,self.center.position[0]+self.radius,self.center.position[1]+self.radius,self.center.position[0]-self.radius,self.center.position[1]-self.radius)
    
class hyperbolic_line(circle):
    def __init__(self,universe,point1,point2):
        center=point(universe=universe,
                     position=[(sqruler([0,0],point1.position)-sqruler([0,0],point2.position))*(2*(point1.position[0]-point2.position[0]))**(-1),0])
        radius=math.sqrt(sqruler(center.position,point1.position))
        super().__init__(universe=universe,center=center,radius=radius)
        point1.dependencies.append(self)
        point2.dependencies.append(self)
        
class hyperbolic_circle(circle):
    def __init__(self,universe,center,radius):
        self.universe=universe
        self.hyperbolic_center=center
        self.hyperbolic_radius=radius
        euclidean_center=point(universe,position=[center.position[0],center.position[1]*math.cosh(radius)])
        super.__init__(universe,center=euclidean_center,radius=center.position[1]*math.sinh(radius))
    
    def hyper_center_point(universe,center,point):
        radius=hyperuler(center,point)
        return hyperbolic_circle(universe,center=center,radius=radius)
        
        

        
        

root=tk.Tk()
root.title("Geogebra Clone")
root.geometry("720x720")
origin=[0,0]
root.resizable(True,True)


var=tk.IntVar()
move=tk.Radiobutton(root,text="move",variable=var,value=1)
create_point=tk.Radiobutton(root,text="place point", variable=var,value=2)
create_line_segment=tk.Radiobutton(root,text="create line segment",variable=var,value=3)
circle_center_point=tk.Radiobutton(root,text="circle by center +point",variable=var,value=4)
create_hyperbolic_line=tk.Radiobutton(root,text="hyperbolic line",variable=var,value=5)
radio_dictionary={
        1:"move_object(cursor,chosen)",
        2:"point(universe=canvas,position=list(cursor))",
        3:"segment_maker(cursor,chosen)",
        4:'circle_point(chosen)',
        5:'hyperline(chosen)'
        }
selected=[]
templist=[]


canvas=tk.Canvas(root,bg="white",height=360,width=360)
null_point=point(universe=canvas,position=[-1,-1],color='')

follower=point(universe=canvas)
move.grid(row=1, column=1)
create_point.grid(row=2,column=1)
create_line_segment.grid(row=3,column=1)
circle_center_point.grid(row=4,column=1)
create_hyperbolic_line.grid(row=5,column=1)
canvas.grid(column=2,row=1)


P=point(canvas,[180,180])
Q=point(canvas,[270,270])


root.bind('<Motion>', motion)
canvas.bind("<Button 1>",onclick)


root.mainloop()