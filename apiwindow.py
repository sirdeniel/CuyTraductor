from typing import List
import gi
gi.require_versions({'Gtk': '3.0', 'Gdk':'3.0'})
from gi.repository import Gtk, Gdk

import json

#Gtk.StyleContext.add_class adds style class name
#Gtk.Widget.get_style_context returns the style context

class WindowAPI:
    "Laucnhes the API manager window. Throws an error if json not found."
    def __init__(self, parent_window) -> None:
        self.builder = Gtk.Builder.new_from_file('assets/api.glade')
        self.window = self.builder.get_object('apiwindow')
        self.window.set_modal(True)
        self.window.set_transient_for(parent_window)
        # self.window.connect('destroy', Gtk.main_quit)
        self.window.connect('delete-event', self.hide_on_event)
        
        self.okbtn = self.builder.get_object('okbtn')
        cancelbtn = self.builder.get_object('cancelbtn')
        # cancelbtn.connect("clicked", Gtk.main_quit)
        cancelbtn.connect("clicked", self.hidewindow)
        self.infobox = self.builder.get_object('infobox')

        self.theme_window()

        #remove placeholder (shown in glade)
        [self.infobox.remove(child) for child in self.infobox.get_children()]

        with open("apimodel.json") as f:
            self.apimodel_dict = json.load(f)
            # self.build_windows
            for service in self.apimodel_dict.keys():
                self.build_section( service, self.apimodel_dict[service]['section_title'],
                                    self.apimodel_dict[service]['ordered_fields'])

        self.okbtn.connect("clicked", self.on_okbtn_clicked, self.apimodel_dict)
    
    def hide_on_event(self, widget, event):
        self.window.hide_on_delete()
        return True

    def hidewindow(self, widget):
        self.window.hide()

    def on_okbtn_clicked(self, widget, apimodel_dict):
        with open('apimodel.json', 'w') as fp:
            json.dump(apimodel_dict, fp, indent=4)
        self.window.hide()

    def show_window(self,):
        self.window.show_all()
    
    def theme_window(self,):
        self.css_provider = Gtk.CssProvider.new()
        self.css_provider.load_from_path("assets/style.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def build_section(self, service:str, section_title:str, fields:List[str]):
        title_label = Gtk.Label.new(section_title)
        title_label.get_style_context().add_class("sectiontitle")
        title_label.set_xalign(0)
        section_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        section_box.pack_start(title_label,False, True, 0)

        for field in fields:
            fieldbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
            
            fieldlabel = Gtk.Label.new(field)
            fieldlabel.set_size_request(150, -1)
            fieldlabel.set_xalign(0)
            fieldbox.pack_start(fieldlabel, False, True, 0)
            
            fieldentry = Gtk.Entry.new()
            # connect the change to save value in apimodel_dict
            fieldentry.connect('changed', self.update_field_value, service, field)
            fieldentry.set_visibility(False)
            fieldentry.set_input_purpose(Gtk.InputPurpose.PASSWORD)
            fieldentry.set_invisible_char('●')
            fieldentry.set_text(self.apimodel_dict[service][field]) # load text
            fieldbox.pack_start(fieldentry, True, True, 0)

            section_box.pack_start(fieldbox, False, True, 0)
        pass

        self.infobox.pack_start(section_box, False, True, 5)

    def update_field_value(self, entrywidget, service:str, field:str):
        self.apimodel_dict[service][field] = entrywidget.get_text()
        pass

if __name__ == '__main__':
    apiwin = WindowAPI()
    apiwin.show_window()
    Gtk.main()
