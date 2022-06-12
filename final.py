#!/usr/bin/env python
# coding: utf-8

# In[3]:


import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk
import numpy as np
from tkinter.simpledialog import askinteger,askstring
import random
win=tk.Tk()
win.title("圖像處理")
win.geometry("700x700")

# frame1 載入檔案
frame1=tk.Frame(win,width=700,height=30)
frame1.grid(row=0,column=0,columnspan=2)
file_text=tk.Text(frame1,width=80,height=1)
file_text.grid(row=0,column=0,padx=20,pady=20)
# frame2 顯示圖片
frame2=tk.Frame(win,width=500,height=500)
frame2.grid(row=1,column=0)
file_label=tk.Label(frame2)
file_label.grid(row=1,column=0,rowspan=5,columnspan=5)
# 載入檔案 按鈕
def fun_file_button():
    global file,image,imgtk,hei,wid,flag
    file_text.delete("1.0","end")
    file=filedialog.askopenfilename(title="選擇圖片",filetypes=[("All Files","*.*"),("jpeg files","*.jpg"),("png files","*.png")])
    file_text.insert("insert",file)
    image=Image.open(file)
    # 長寬最大400 紀錄長寬
    if image.width>=image.height:
        mul=image.width/400.0
        image=image.resize((400,int(image.height/mul)))
        wid=image.width
        hei=image.height
    elif image.width<image.height:
        mul=image.height/400.0
        image=image.resize((int(image.width/mul),400))
        wid=image.width
        hei=image.height
    flag=0
    imgtk=ImageTk.PhotoImage(image)
    file_label.imgtk=imgtk
    file_label.configure(image=imgtk)
# 灰度化 按鈕
def gray_button():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    for i in range(hei):
        for j in range(wid):
            gray=(image_temp[i][j][0]+image_temp[i][j][1]+image_temp[i][j][2])/3
            image_temp[i][j][0]=gray
            image_temp[i][j][1]=gray
            image_temp[i][j][2]=gray
    image_new=Image.fromarray(image_temp)
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
#灰度化 按鈕
def gray_button2():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    image_temp=255*(image_temp/255)**2
    for i in range(hei):
        for j in range(wid):
            gray=(image_temp[i][j][0]+image_temp[i][j][1]+image_temp[i][j][2])/3
            image_temp[i][j][0]=gray
            image_temp[i][j][1]=gray
            image_temp[i][j][2]=gray
    image_new=Image.fromarray(image_temp.astype(np.uint8))
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
#灰度反向 按鈕
def gray_button3():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    image_temp=255*(image_temp/255)**2
    image_temp=255-image_temp
    for i in range(hei):
        for j in range(wid):
            gray=(image_temp[i][j][0]+image_temp[i][j][1]+image_temp[i][j][2])/3
            image_temp[i][j][0]=gray
            image_temp[i][j][1]=gray
            image_temp[i][j][2]=gray
    image_new=Image.fromarray(image_temp.astype(np.uint8))
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 復原 按鈕
def original():
    global flag,wid,hei
    flag=0
    wid=image.width
    hei=image.height
    imgtk=ImageTk.PhotoImage(image)
    file_label.imgtk=imgtk
    file_label.configure(image=imgtk)
#SVD 壓縮
def svd_button():
    global flag,image_new
    if flag==0:
        image_new=np.array(image)
    else:
        image_new=np.array(image_new)
    def svd(matrix, k):
        u, z, v = np.linalg.svd(matrix)
        u = u[:, 0:k]
        z = np.diag(z[0:k])
        v = v[0:k, :]
        a = u.dot(z).dot(v)
        a[a < 0] = 0
        a[a > 255] = 255
        return a
    image_new[:,:,0]=svd(image_new[:,:,0], 10)
    image_new[:,:,1]=svd(image_new[:,:,1], 10)
    image_new[:,:,2]=svd(image_new[:,:,2], 10)
    image_new=Image.fromarray(image_new)
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 圖像量化 按鈕
def quantization_button():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    for i in range(hei):
        for j in range(wid):
            for k in range(3): 
                if image_temp[i][j][k] < 128:
                    image_temp[i][j][k] = 0
                else:
                    image_temp[i][j][k] = 128
    image_new=Image.fromarray(image_temp.astype(np.uint8))
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 馬賽克 按鈕
def mosaic_button():
    global image_new,flag
    num=askinteger(title="輸入馬賽克格數n",prompt="n*n")
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    numHeight = hei/num
    numwidth = wid/num
    for i in range(num):
        y = int(i*numHeight)
        for j in range(num):
            x = int(j*numwidth)
            b = image_temp[y][x][0]
            g = image_temp[y][x][1]
            r = image_temp[y][x][2]
            for n in range(int(numHeight)):
                for m in range(int(numwidth)):
                    image_temp[y+n][x+m][0] = b
                    image_temp[y+n][x+m][1] = g
                    image_temp[y+n][x+m][2] = r
    image_new=Image.fromarray(image_temp.astype(np.uint8))
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 旋轉 按鈕
def rotate_button():
    global image_new,flag,wid,hei
    if flag==0:
        image_new=image.transpose(Image.ROTATE_90)
    else:
        image_new=image_new.transpose(Image.ROTATE_90)
    wid=image_new.width
    hei=image_new.height
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 模糊 按鈕
def fuzzy_button():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    image_temp=cv2.blur(image_temp,(15,15))
    image_new=Image.fromarray(image_temp)
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 裁切 按鈕
def cut_button():
    global image_new,flag,wid,hei
    x_s=askinteger(title="輸入橫向起點",prompt="0~"+str(wid))
    x_e=askinteger(title="輸入橫向終點",prompt="0~"+str(wid))
    y_s=askinteger(title="輸入縱向起點",prompt="0~"+str(hei))
    y_e=askinteger(title="輸入縱向終點",prompt="0~"+str(hei))
    if flag==0:
        image_new=image.crop((x_s,y_s,x_e,y_e))
    else:
        image_new=image_new.crop((x_s,y_s,x_e,y_e))
    wid=image_new.width
    hei=image_new.height
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 毀損 按鈕
def error_button():
    global image_new,flag
    if flag==0:
        image_temp=np.array(image)
    else:
        image_temp=np.array(image_new)
    for i in range(hei):
        for j in range(wid):
            image_temp[i][j]=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    image_new=Image.fromarray(image_temp)
    flag=1
    image_new_tk=ImageTk.PhotoImage(image_new)
    file_label.imgtk=image_new_tk
    file_label.configure(image=image_new_tk)
# 儲存 按鈕
def save_button():
    global image_new,flag
    file_save=filedialog.asksaveasfilename(title="儲存檔案",filetypes=[("All Files","*.*"),("jpeg files","*.jpg"),("png files","*.png")])
    image_new.save(str(file_save)+".jpg")
file_button=tk.Button(frame1,text="選擇檔案",command=fun_file_button)
file_button.grid(row=0,column=1,padx=10,pady=10,sticky="n")
frame3=tk.Frame(win,width=200,height=500)
frame3.grid(row=1,column=1)
file_button=tk.Button(frame3,text="儲存",command=save_button)
file_button.grid(row=0,column=0,pady=10,sticky="n")
file_button=tk.Button(frame3,text="復原",command=original)
file_button.grid(row=1,column=0,pady=10,sticky="n")
file_button=tk.Button(frame3,text="旋轉",command=rotate_button)
file_button.grid(row=2,column=0,pady=10,sticky="n")
file_button=tk.Button(frame3,text="裁切",command=cut_button)
file_button.grid(row=3,column=0,pady=10,sticky="n")
frame4=tk.Frame(win,width=500,height=30)
frame4.grid(row=2,column=0)
file_button=tk.Button(frame4,text="灰度1",command=gray_button)
file_button.grid(row=0,column=0,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="灰度2",command=gray_button2)
file_button.grid(row=0,column=1,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="灰度反向",command=gray_button3)
file_button.grid(row=0,column=2,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="SVD",command=svd_button)
file_button.grid(row=0,column=3,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="圖像量化",command=quantization_button)
file_button.grid(row=0,column=4,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="馬賽克",command=mosaic_button)
file_button.grid(row=0,column=5,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="模糊",command=fuzzy_button)
file_button.grid(row=0,column=6,padx=20,pady=20,sticky="nw")
file_button=tk.Button(frame4,text="毀損",command=error_button)
file_button.grid(row=1,column=0,padx=20,pady=20,sticky="nw")


win.mainloop()


# In[ ]:





# In[ ]:




