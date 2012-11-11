import re
import sublime, sublime_plugin
import indent

def indent_line(edit, view, line, options):
	line_str = view.substr(line)
	current_indent = indent.current_indent(line_str)
	new_indent = indent.indent(view, line.begin(), options)
	if not current_indent == new_indent:
		view.replace(edit,
		   sublime.Region(line.begin(), 
		                  line.begin() + current_indent),
		   " " * new_indent)

def indent_selection(edit, view, idx, options):
	total = len(view.lines(view.sel()[idx]))

	for i in range(total):
		line = view.lines(view.sel()[idx])[i]
		indent_line(edit, view, line, options)

def indent_selections(edit, view, options):
	total = len(view.sel())

	for i in range(total):
		indent_selection(edit, view, i, options)

def insert_newline_and_indent(edit, view, options):
	idx = view.sel()[0].begin()
	view.insert(edit, idx, 
	            "\n" + indent.get_indent_str(view, idx, options))

###############################
## View file type + regexps

views = {}
options = {
	"clj": {
		"default_indent": "function",
		"regex": re.compile("^(def|defn)$")
	}
}

def get_lisp_file_type(name):
	if name and re.match(".*\.(clj|cljs)$", name):
		return "clj"

def get_view_file_type(view):
	vwid = view.id()
	if vwid in views: return views[vwid]

def get_view_options(view):
	ft = get_view_file_type(view)
	if ft and ft in options:
		return options[ft]

def should_use_lisp_indent(vwid):
	return vwid in views

settings = sublime.load_settings("lispindent.sublime-settings")

def reload_languages():
	l = settings.get("languages")
	for language, opts in l.items():
		print("language = " + language)
	print("reloaded settings!")

settings.add_on_change("languages", reload_languages)
reload_languages()

###############################
## Commands

class LispindentCommand(sublime_plugin.TextCommand):  
    def run(self, edit):
    	view = self.view
    	if should_use_lisp_indent(view.id()):
    		indent_selections(edit, view, get_view_options(view))
    	else:
    		view.run_command("reindent")

class LispindentinsertnewlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		if should_use_lisp_indent(view.id()):
			insert_newline_and_indent(edit, view, get_view_options(view))
		else:
			view.run_command("insert", {"characters": "\n"})

class LispIndentListenerCommand(sublime_plugin.EventListener):
	last_sel = []
	def on_activated(self, view):
		vwid = view.id()
		if not vwid in views:
			file_type = get_lisp_file_type(view.file_name())
			if file_type: views[vwid] = file_type