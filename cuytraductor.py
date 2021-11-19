import gi
gi.require_versions({'Gtk': '3.0','GdkPixbuf':'2.0', 'Gdk':'3.0', 'GLib':'2.0'})
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib
import threading

import dochandler
import apiwindow

class App:

    def __init__(self, ):
        """
        Widgets expected:
        widget_names = ('cbfrom', 'doc_in_button', 'cbto', 'entsuffix','cbprovider',
                        'gobutton', 'tofilebox', 'mainwindow', 'lbfeedback')
        """
        builder = Gtk.Builder.new_from_file('assets/main.glade')
        self.lbfeedback = builder.get_object('lbfeedback') # Gtk.Label
        self.doc_handler:dochandler.DocHandler = dochandler.DocHandler()
        self.window = builder.get_object('mainwindow') # Gtk.Window
        self.theme_window() # theme fonts or any widget with css

        doc_in_button = builder.get_object('doc_in_button') # Gtk.Button
        doc_in_button.drag_dest_set(Gtk.DestDefaults.DROP, [], Gdk.DragAction.COPY)
        doc_in_button.drag_dest_add_uri_targets()

        # gifs for result feedback
        self.animready = GdkPixbuf.PixbufAnimation.new_from_file('assets/doc-ready.gif')
        self.animsus = GdkPixbuf.PixbufAnimation.new_from_file('assets/doc-sus.gif')
        self.animtranslating = GdkPixbuf.PixbufAnimation.new_from_file('assets/doc-translating.gif')
        self.resultanim = builder.get_object('resultanim') # Gtk.Image

        self.doc_handler = dochandler.DocHandler()
        self.languages = builder.get_object('languages') # Gtk.ListStore
        self.languages.clear() # removes all existing rows (from glade file)
        # Gtk.ListStore.inser(index, row)
        [self.languages.insert(-1, [lang]) for lang in self.doc_handler.supported_languages]

        self.provider = builder.get_object('provider') # Gtk.ListStore
        self.provider.clear() 
        [self.provider.insert(-1, [prov]) for prov in self.doc_handler.supported_providers]

        cbprovider = builder.get_object('cbprovider')
        idx = self.doc_handler.supported_providers.index(self.doc_handler.selected_provider)
        cbprovider.set_active(idx)
        cbprovider.connect('changed', self.update_selected_provider)

        cbfrom = builder.get_object('cbfrom')
        idx = self.doc_handler.supported_languages.index(self.doc_handler.from_lang)
        cbfrom.set_active(idx)
        cbfrom.connect('changed', self.update_from_lang)
        cbto = builder.get_object('cbto')
        idx = self.doc_handler.supported_languages.index(self.doc_handler.to_lang)
        cbto.set_active(idx)
        cbto.connect('changed', self.update_to_lang)

        entsuffix = builder.get_object("entsuffix")
        entsuffix.set_text(self.doc_handler.suffix)
        entsuffix.connect('changed', self.update_suffix)

        # feedback the output name before translating
        # lbfeedback = builder.get_object("lbfeedback")
        # self.doc_handler.set_lbfeedback(lbfeedback)

        self.keyswindow = apiwindow.WindowAPI(self.window)

        builder.connect_signals(self)
        self.window.show_all()
        Gtk.main()

    ################ SIGNALS #############################

    def on_keysbutton_clicked(self, widget):
        self.keyswindow.show_window()
        pass

    def on_doc_in_button_clicked(self, lbdrop):
        # native file chooser is better for the end-user
        dialog = Gtk.FileChooserNative.new("Abrir documento Word",
                self.window, Gtk.FileChooserAction.OPEN, "Aceptar", "Cancelar")
        # filter extension of files allowed
        filter = Gtk.FileFilter()
        filter.add_pattern("*.docx;*.doc")
        filter.set_name("Documentos Word")
        dialog.add_filter(filter)
        
        # waiting for user input
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            uri = dialog.get_uri()
            self.checknload(uri, lbdrop)
        dialog.destroy()
        pass

    def on_doc_in_button_drag_data_received(self, lbdrop, dragcontext, x, y, data, info, time):
        #               context,  success, delete, time
        Gtk.drag_finish(dragcontext, True, False, time)
        uri = data.get_uris()[0] # support for 1 doc at a time
        print("The uri:", uri)
        self.checknload(uri, lbdrop)

    def on_gobutton_clicked(self, gobutton):
        if self.doc_handler and self.doc_handler.can_translate():
            thread = threading.Thread(target=self.doc_handler.start_translation,
                                    args=(GLib.idle_add,
                                        self.update_lbparagraph,
                                        self.result_succeded,
                                        self.result_needs_check))
            thread.daemon = True
            thread.start()
            self.resultanim.set_from_animation(self.animtranslating)
        else:
            print("Already translating bro")

    def on_main_destroy(self, widget):
        Gtk.main_quit()
    ################ END OF SIGNALS #############################

    def update_suffix(self, entsuffix):
        self.doc_handler.suffix = entsuffix.get_text()
        self.doc_handler.save_docsettings()

    def update_from_lang(self, cbfrom):
        self.doc_handler.from_lang = self.doc_handler.supported_languages[cbfrom.get_active()]
        self.doc_handler.save_docsettings()

    def update_to_lang(self, cbto):
        self.doc_handler.to_lang = self.doc_handler.supported_languages[cbto.get_active()]
        self.doc_handler.save_docsettings()

    def update_selected_provider(self, cbprov):
        self.doc_handler.selected_provider = self.doc_handler.supported_providers[cbprov.get_active()]
        self.doc_handler.save_docsettings()
    
    def checknload(self, uri:str, lbdrop):
        if not dochandler.is_a_word_doc(uri):
            return # do nothing, exit function
        if self.doc_handler.can_translate():
            self.doc_handler.set_document(uri)
            lbdrop.set_text(self.doc_handler.get_filename()) # update ui

    def update_lbparagraph(self, info:str):
        "Used in GLib.iddle_add(). Must return False once finished."
        self.lbfeedback.set_text(info)
        return False # always return False to GLib.idle_add() to avoid errors

    def result_succeded(self,):
        self.resultanim.set_from_animation(self.animready)
        success_message = f"{self.doc_handler.get_output_filename()}!"
        self.lbfeedback.set_text(success_message)

    def result_needs_check(self,):
        self.resultanim.set_from_animation(self.animsus)
        suspicious_message = f"Revisar {self.doc_handler.get_output_filename()}"
        self.lbfeedback.set_text(suspicious_message)
    
    def theme_window(self,):
        self.css_provider = Gtk.CssProvider.new()
        self.css_provider.load_from_path("assets/style.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.css_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == '__main__':
    appplication = App()
