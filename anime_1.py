from tkinter import *
from tkinter import messagebox
#from tkinter import font
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import os
from time import sleep

one_time = True

class StartPage:
    def __init__(self,master):
        self.master = master
        #self.master.configure(bg='#009999') #root background
        #self.l1 = Label(self.master,text='Kiss Batch Downloader',width=50,fg='white')
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688',height=2,bd=2)
        self.l1.pack(fill=X)
        self.f1 = Frame(self.master)
        self.f1.pack(fill=X)
        self.i1 = IntVar()
        self.i2 = IntVar()
        self.i1.initialize(1)
        self.i2.initialize(1)
        self.rb1 = Radiobutton(self.f1,text='Firefox',value = 1,variable=self.i1)#,bg='#006688',fg='#ff9977')
        self.rb1.pack(fill=X)
        self.rb2 = Radiobutton(self.f1, text='Chrome', value = 2, variable=self.i1)#,bg='#446688',fg='#aa9977')
        self.rb2.pack(fill=X)
        self.cb1 = Checkbutton(self.master,text='Visible',variable=self.i2)#,bg='#222222',fg='#dddddd')
        self.cb1.pack(fill=X)
        self.b1 = Button(self.master,text='Start',command=self.func1)#,bg='#006633',fg='white')
        self.b1.pack(fill=X)
        self.b2 = Button(self.master,text='Exit',command=lambda : exit_all())#,bg='#882244',fg='white')
        self.b2.pack(fill=X)

    def func1(self):
        global thread_open_browser
        thread_open_browser = threading.Thread(target=open_browser,args=[self.i1.get(),self.i2.get()])
        thread_open_browser.start()
        #open_browser(self.i1.get(),self.i2.get())
        if os.path.isfile('user_a.txt'):
            global user,passw
            file = open('user_a.txt', 'r')
            user = file.readline()
            passw = file.readline()
            file.close()
            show_frame(self.master,LoginWait)
        else:
            show_frame(self.master,LoginPage)

class LoginPage:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#009999')  # root background
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.f1 = Frame(self.master)
        self.f1.pack(fill=X)
        self.l2 = Label(self.f1, text='UserName : ').pack(side=LEFT)
        self.e1 = Entry(self.f1,width=45)
        self.e1.pack(side=LEFT)
        self.b1 = Button(self.f1,text='Clear',command=lambda:self.e1.delete(0,END)).pack(side=RIGHT)

        self.f2 = Frame(self.master)
        self.f2.pack(fill=X)
        self.l3 = Label(self.f2, text='Password  : ').pack(side=LEFT)
        self.e2 = Entry(self.f2, width=45)
        self.e2.pack(side=LEFT)
        self.b2 = Button(self.f2, text='Clear', command=lambda: self.e2.delete(0,END)).pack(side=RIGHT)

        self.b3 = Button(self.master, text='Submit',command=self.func1).pack(fill=X)

    def func1(self):
        global user,passw
        user = self.e1.get()
        passw = self.e2.get()
        file = open('user_a.txt', 'w')
        file.write(user + '\n' + passw)
        file.close()
        show_frame(self.master,LoginWait)

        #if check_login_success() :
         #   show_frame(self.master,Page1)
        #else:
         #   show_frame(self.master,LoginPage)

class LoginWait:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#009999')  # root background
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.t1 = Text(self.master,width=50,height=5)
        self.t1.pack()
        self.b1 = Button(self.master,text='Exit',command=lambda :exit_all())
        self.b1.pack(fill=X)
        thread_open_browser.join()
        thread_login = threading.Thread(target=self.do_login)
        thread_login.start()
        #self.do_login()


    def do_login(self):
        #print('is alive thread_open_browser : ',thread_open_browser.isAlive())
        global user,passw
        self.t1.insert(END, "Logging In...\n")
        browser.get('https://kissanime.ru/Login')
        element_present = EC.presence_of_element_located((By.ID, 'btnSubmit'))
        WebDriverWait(browser, timeout).until(element_present)

        browser.find_element_by_id('username').send_keys(user)
        browser.find_element_by_id('password').send_keys(passw)
        try:
            browser.find_element_by_id('btnSubmit').click()
        except:
            browser.find_element_by_id('password').send_keys(Keys.ENTER)

        element_present = EC.presence_of_element_located((By.ID, 'containerRoot'))
        WebDriverWait(browser, timeout).until(element_present)
        if check_login_success():
            self.t1.insert(END,'Login Success\n')
            sleep(1)
            show_frame(self.master,Page1)
        else:
            self.t1.insert(END, 'Login Failed\n')
            sleep(2)
            show_frame(self.master,LoginPage)


class Page1:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#00CCBB')  # root background
        self.l1 = Label(self.master, text='Kiss Batch Downloader')
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.f1 = Frame(self.master)
        self.f1.pack()
        self.i1 = StringVar()
        self.l2 = Label(self.f1, text='Enter URL : ')
        self.l2.pack(side=LEFT)
        self.e1 = Entry(self.f1,width=50)
        self.e1.pack(side=LEFT)
        self.b3 = Button(self.f1, text='Clear', command=lambda: self.e1.delete(0, END)).pack(side=RIGHT)
        self.b1 = Button(self.master, text='Start',command = lambda: self.func1())
        self.b1.pack(fill=X)
        self.b2 = Button(self.master, text='Exit', command=lambda: exit_all())
        self.b2.pack(fill=X)

    def func1(self):
        global URL
        URL = self.e1.get()
        show_frame(self.master,WaitingLoad)

class WaitingLoad:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#009999')  # root background
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.t1 = Text(self.master, width=50, height=5)
        self.t1.pack()
        self.t1.insert(INSERT,'Waiting...to...load.....')
        self.b1 = Button(self.master, text='Exit', command=lambda: exit_all())
        self.b1.pack(fill=X)

        #global one_time
        #if one_time:
        #    one_time = False
        global thread_open_link
        thread_open_link = threading.Thread(target=self.open_url)
        thread_open_link.start()

    def func1(self):
        #thread_open_link.join()
        self.generate_links()
        show_frame(self.master, Page2)

    def open_url(self):
        global name
        name = URL.split('/')[-1]

        ##    browser.set_page_load_timeout(30)
        try:
            print('Waiting...to...open')
            browser.set_page_load_timeout(30)
            browser.get(URL)
        except:
            mes = messagebox.askretrycancel(title='Error',message="Error : URL not working")
            if mes:
                show_frame(self.master,Page1)
            else:
                exit_all()
        print('starting func1')
        threading.Thread(target=self.func1).start()

    def generate_links(self):
        global list_of_a,list_of_names,links
        list_of_a = browser.find_elements_by_css_selector('td > a')
        list_of_a.reverse()
        links = []
        list_of_names = []

        for elem in list_of_a:
            try:
                links.append(elem.get_attribute('href') + '&s=rapidvideo')
                list_of_names.append(elem.text)
            except:
                print("Error in links : ", elem.text)  # add the code later



class Page2:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#009999')  # root background
        self.lst = list_of_names
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.f1 = Frame(self.master)
        self.f1.pack(fill=X)
        self.scroll = Scrollbar(self.f1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.lb1 = Listbox(self.f1,width=60,yscrollcommand=self.scroll.set)

        self.list_insert()

        self.lb1.pack(side=LEFT)
        self.scroll.config(command=self.lb1.yview)

        self.f2 = Frame(self.master,width=5)
        self.f2.pack(fill=X)
        self.l2 = Label(self.f2,text='Start : ',width=10).pack(side=LEFT,fill=Y)
        self.sc1 = Scale(self.f2,from_=0,to = len(self.lst)-1,orient=HORIZONTAL,width=15,length=280,sliderlength=100,bg='red')
        self.sc1.pack(side=LEFT)

        self.f3 = Frame(self.master, width=5)
        self.f3.pack(fill=X)
        self.l3 = Label(self.f3, text='End : ', width=10).pack(side=LEFT, fill=Y)
        self.sc2 = Scale(self.f3, from_=0, to=len(self.lst)-1, orient=HORIZONTAL, width=15, length=280,sliderlength=100,bg='blue',fg='white')
        self.sc2.pack(side=LEFT)
        self.sc2.set(len(self.lst))

        self.b1 = Button(self.master, text='Start', command=lambda: self.func1())
        self.b1.pack(fill=X)
        self.b2 = Button(self.master, text='Exit', command=lambda: exit_all())
        self.b2.pack(fill=X)

    def list_insert(self):
        for a in self.lst:
            if self.lst.index(a)<10:
                self.lb1.insert(self.lst.index(a),'    '+str(self.lst.index(a))+'  :  '+a)
            else:
                self.lb1.insert(self.lst.index(a), '  ' + str(self.lst.index(a)) + '  :  ' + a)
        if len(self.lst) < 21:
            self.lb1.configure(height=len(self.lst))
        else:
            self.lb1.configure(height=20)

    def func1(self):
        global start,end
        start = self.sc1.get()
        end   = self.sc2.get() + 1
        show_frame(self.master, Page3)

class Page3:
    def __init__(self,master):
        self.master = master
        self.master.configure(bg='#009999')  # root background
        self.l1 = Label(self.master, text='Kiss Batch Downloader', width=50)
        self.l1.configure(bg='#006688', height=2)
        self.l1.pack(fill=X)
        self.f1 = Frame(self.master)
        self.f1.pack(fill=X)
        self.scroll = Scrollbar(self.f1)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.lb1 = Listbox(self.f1, width=90,height=20, yscrollcommand=self.scroll.set)
        #self.list_insert()
        self.lb1.pack(side=LEFT)
        self.scroll.config(command=self.lb1.yview)

        self.b1 = Button(self.master, text='Start', command=lambda: show_frame(self.master, Page1))
        self.b1.pack(fill=X)
        self.b2 = Button(self.master, text='Exit', command=lambda: exit_all())
        self.b2.pack(fill=X)

        self.thread_download_drama = threading.Thread(target=self.get_rv_links)
        self.thread_download_drama.start()
        threading.Thread(target=self.func1).start()

    def func1(self):
        self.thread_download_drama.join()
        self.write_to_file()

    def download_episode(self,link):
        print(link)
        self.lb1.insert(END,str(link+'\n'))
        browser.get('about:blank')
        try:
            #threading.Thread(target=browser.get,args=[link]).start()
            browser.get(link)
        except TimeoutException:
            pass
        ##        return DownloadEpisode(browser,link)
        except WebDriverException:
            print('Page not found ', link)
            self.lb1.insert(END,str('Page not found '+link+'\n'))
            return 'Error Page not found'
        except Exception as e:
            print(e)
            self.lb1.insert(END,str(e)+'\n')
            return 'Error1' + str(e)
        #threading.Thread(target=browser.get, args=[link]).start()
        element_present = EC.presence_of_element_located((By.ID, 'divDownload'))
        WebDriverWait(browser, timeout).until(element_present)
        try:
            href = browser.find_element_by_id('divDownload')
            href = href.find_element_by_tag_name('a')
            link_rv = (href.get_attribute('href'))
            print(link_rv)
            self.lb1.insert(END,str(link_rv+'\n'))
            return link_rv
        ##        listOfEpName.append(listOfNames[i+start])
        except Exception as e:
            self.lb1.insert(END,str(e+' : '+link+'\n'))
            print(e, link)  ##listOfNames[i+start])
            return 'Error2 ' + e

    def get_rv_links(self):
        if is_firefox:
            browser.set_page_load_timeout(1)
            print('load timeout : 1')
        else:
            browser.set_page_load_timeout(6) #increase this value if not working
            print('load timeout : 6')
        global   links_rv,list_of_ep_name
        links_rv = []
        list_of_ep_name = []

        try:
            for i in range(end - start):
                self.lb1.insert(END,"Downloading "+str(list_of_names[i + start])+'\n')
                print("Downloading ", list_of_names[i + start])
                link = self.download_episode(links[start + i])
                links_rv.append(link)
                list_of_ep_name.append(list_of_names[i + start])
                if 'Error' in link:
                    print("Error Not Found : ", list_of_names[i + start])
                    self.lb1.insert(END,str("Error Not Found " + str(list_of_names[i + start]) + '\n'))
        except Exception as e:
            print("Error3 : ", e)
            self.lb1.insert(END,str('Error3: '+str(e)+'\n'))
        #finally:
        #    return links_rv, list_of_ep_name

    def write_to_file(self):
        file = open(name + '_RV.txt', 'w')
        str1 = '\n'.join(links_rv)
        file.write(str1)
        file.close()
        file = open(name + '_O.txt', 'w')
        str2 = '\n'.join(list_of_ep_name)
        file.write(str2)
        file.close()
        print("RapidVideo Links Saved in " + name + "_RV.txt File ")
        self.lb1.insert(END,str("RapidVideo Links Saved in " + name + "_RV.txt File "))
        print("Now Use RP_Downloader.py to create txt file of live links")
        self.lb1.insert(END, "Now Use RP_Downloader.py to create txt file of live links")
        messagebox.showinfo(title='Download Complete',message=f'Your Download is Completed and Links are saved in {name}_RV.txt\n')
##==============================================================##

def exit_all():
    try:
        browser.close()
    except:
        pass
    root.quit()

def show_frame(self,show):
    self.destroy()
    global p,frame
    frame = Frame(root)
    frame.grid(row=0,column=0)
    p = show(frame)
    frame.tkraise()

##=======================================================##
def open_browser(firefox=1,visible=1):
    global browser,is_browser_open,is_firefox,is_chrome
    is_chrome=False
    is_firefox=False
    if firefox == 1:
        options = webdriver.firefox.options.Options()
        is_firefox = True
    else:
        options = webdriver.chrome.options.Options()
        is_chrome = False
    if visible == 0:
        options.headless = True
        print('Opening headless browser...')

    if firefox == 1:
        browser = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
    else:
        browser = webdriver.Chrome(options=options)
    if firefox == 1:
        print('Installing Ghostery (To remove ads)...')
        ##    browser = webdriver.Chrome();
        # browser.maximize_window()
        addonpath = os.getcwd()+"\\firefox@ghostery.com.xpi"
        browser.install_addon(addonpath,temporary=True)
    is_browser_open = True
    #return browser

def check_login_success():
    try:
        browser.find_element_by_class_name('error')
        mes = messagebox.showerror(title='Wrong Details', message='Maybe you entered wrong username or password \nPlease enter login details again ')
        os.remove('user_a.txt')
        return False
    except:
        global is_logged_in
        is_logged_in = True
        #messagebox.showinfo("Login Success")
        return True

##============================================================================##
if __name__=="__main__":
    global root,browser,timeout,is_logged_in,is_browser_open
    is_logged_in = False
    is_browser_open = False
    timeout=20
    root = Tk()
    #root.geometry("200x200+120+120")
    root.title('Kiss Downloader')
    frame = Frame(root)
    frame.grid(row=0,column=0)
    p = StartPage(frame)
    root.mainloop()