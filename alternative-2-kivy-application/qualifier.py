"""This is a basic "Hello world" using Kivy.

It uses the Builder to load a KVlang string, that describe a widget
tree, here containing only one element, the root, a Label displaying
"Hello world!"
"""

from kivy.app import App
from kivy.lang import Builder


# KVLang is a yaml-inspired declarative language to describe user
# interfaces you can find an introduction to its syntax here
# https://kivy.org/doc/stable/guide/lang.html

# for an even shorter introduction…
# basically widgets are declared nested by indentation, and properties
# are similarly defined in the scope (indentation level) of the widget
# they relate to. It also allows defining canvas (graphical)
# instructions much in the same way as Widget.
# KVlang also allows declaring "rules" for widget classes, these rules
# will similarly declare a tree of widget children, properties and
# canvas instructions, that will be automatically applied to all
# instances of these classes, these rules are declarede using the class
# name around pointy brackets, e.g: "<MyCustomLabel>:".would declare a
# rule applied to all instances of the MyCustomLabel class (which you
# could define as a subclass of kivy.uix.label.Label).
# The string can contain at most one "root" rule, which is a rule
# without <> around its name, this rule is treated differently, it
# directly instanciates a widget of the class, and adds the declared
# properties, graphical instructions and children widgets to it. This
# widget is returned by the Builder.load_string (or Builder.load_file)
# call, so it can be added to the widget tree, either as root, or to an
# existing parent widget of your choice.

KV_RULES = """
Label:
    text: 'Hello world!'
"""


class Application(App):
    """The application class manages the lifecycle of your program, it
    has events like on_start, on_stop, etc.

    see https://kivy.org/doc/stable/api-kivy.app.html for more information.
    """

    def build(self):
        """whatever is returned by `build` will be the root of the
        widget tree of the application, and be accessible through the
        `root` attribute of the Application object.

        You can also delete this method and rely on the default behavior
        of loading a kv file in the same directory, named like the
        application class, but lower case. here, it would be
        application.kv.
        """

        return Builder.load_string(KV_RULES)


if __name__ == "__main__":
    # calling run method of the application will build the widget tree,
    # and start the event loop.
    Application().run()
