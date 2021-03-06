import sublime
import sublime_plugin
import sys


class SetOutputFormatCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		super(SetOutputFormatCommand, self).__init__(view)
		self.st_settings = sublime.load_settings("Graphvizer.sublime-settings")

	# Called when menu is checked
	def run(self, edit, output_format):
		old_output_format = self.view.settings().get("output_format")
		if old_output_format != output_format:
			self.view.settings().set("output_format", output_format)
			_mod = sys.modules["Graphvizer.graphvizer"]
			core_listener = _mod.__plugins__[0]
			core_listener.rendering(self.view) # render image

	# Called when menu is shown. Used to determine whether a menu should be checked.
	def is_checked(self, output_format):
		# If menus are shown for the first time, we need to set the default engine.
		if self.view.settings().get("output_format") is None:
			self.view.settings().set("output_format", self.st_settings.get("default_output_format"))

		if output_format == self.view.settings().get("output_format"):
			return True
		else:
			return False

	def is_enabled(self):
		if self.view.settings().get("syntax") == "Packages/Graphviz/DOT.sublime-syntax":
			return True
		else:
			return False
