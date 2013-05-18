import re
import sublime, sublime_plugin
try:
	import indent
except:
	from lispindent import indent

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
	total = len(view.sel())
	out = []

	for i in range(total):
		region = view.sel()[i]
		view.erase(edit, region)
		idx = region.begin()
		out += [sublime.Region(idx, idx)]

	sel = view.sel()
	sel.clear()
	for region in out: sel.add(region)

	for i in range(total):
		idx = view.sel()[i].begin()
		view.insert(edit, idx,
			"\n" + indent.get_indent_str(view, idx, options))

###############################
## View file type + regexps

views = {}
filetypes = []
options = {}

def get_lisp_file_type(view):
	for (language, regex, syntax) in filetypes:
		view_syntax = view.settings().get('syntax')
		syntax_matches = syntax and view_syntax.endswith(syntax)
		file_name = view.file_name()
		filename_matches = file_name and regex.match(file_name)
		if filename_matches or syntax_matches:
			return language

def get_view_file_type(view):
	vwid = view.id()
	if vwid in views: return views[vwid]

def get_view_options(view):
	ft = get_view_file_type(view)
	if ft and (ft in options):
		return options[ft]

def should_use_lisp_indent(view):
	return view.id() in views

def test_view(view):
	vwid = view.id()
	if not vwid in views:
		file_type = get_lisp_file_type(view)
		if file_type: views[vwid] = file_type

def test_current_view():
	win = sublime.active_window()
	if win:
		view = win.active_view()
		test_view(view)

def join_regex(regex):
	if isinstance(regex, str):
		return regex
	else:
		out = ""
		for part in regex: out += part
		return out

settings = None
def reload_languages():
	l = settings.get("languages")
	for language, opts in l.items():
		regex = join_regex(opts["regex"])
		compiled = {
			"detect": re.compile(opts["detect"]),
			"default_indent": opts["default_indent"],
			"regex": re.compile(regex)
		}
		filetypes.append((language, compiled["detect"], opts.get("syntax", None)))
		options[language] = compiled

reload_has_init = False
def init_env():
	global reload_has_init
	global settings
	if not reload_has_init:
		settings = sublime.load_settings("lispindent.sublime-settings")
		settings.add_on_change("languages", reload_languages)
		reload_languages()
		reload_has_init = True
		test_current_view()

###############################
## Commands

class LispindentCommand(sublime_plugin.TextCommand):  
	def run(self, edit):
		init_env()
		view = self.view
		test_view(view)
		if should_use_lisp_indent(view):
			indent_selections(edit, view, get_view_options(view))
		else:
			view.run_command("reindent")

class LispindentinsertnewlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		init_env()
		view = self.view
		test_view(view)
		if should_use_lisp_indent(view):
			insert_newline_and_indent(edit, view, get_view_options(view))
		else:
			view.run_command("insert", {"characters": "\n"})

class LispIndentListenerCommand(sublime_plugin.EventListener):
	def on_query_context(self, view, key, operator, operand, match_all):
		if key == "shoulduselispindent":
			init_env()
			test_view(view)
			return should_use_lisp_indent(view)

####
#### Override
def listen_to_syntax_change(view):
	def on_syntax_change():
		# this should "reload the view"
		pass

	view.settings().add_on_change("syntax", on_syntax_change)

class ViewOverrideRunNNNNNNNNNNNNNNNNNNNNNNCommand(sublime_plugin.TextCommand):
	def __init__(this, view):
		old_run_command = getattr(view, "run_command")

		def new_run_command(name, args={}):
			if name == "reindent":
				init_env()
				test_view(view)
				if should_use_lisp_indent(view):
					old_run_command("lispindent")
				else:
					old_run_command("reindent")
			else:
				old_run_command(name, args)

		setattr(view, "run_command", new_run_command)

		listen_to_syntax_change(view)

	def run(this, edit):
		pass
