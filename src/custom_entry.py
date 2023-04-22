import tkinter as tk

class CustomEntry(tk.Entry):
    """
    CustomEntry is a custom tkinter Entry widget that supports placeholders and custom colors.

    Attributes:
        placeholder (str): Placeholder text to be displayed when the input box is empty.
        placeholder_color (str): Color of the placeholder text.
        default_color (str): Default text color when the input box is active.
    """

    def __init__(self, master=None, placeholder=None, placeholder_color='grey', **kwargs):
        """
        Initialize the CustomEntry widget.

        Args:
            master (tkinter object): Parent widget.
            placeholder (str, optional): Placeholder text to be displayed when the input box is empty.
            placeholder_color (str, optional): Color of the placeholder text. Defaults to 'grey'.
            **kwargs: Optional keyword arguments to configure the Entry widget.
        """
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_color = self['fg']
        
        if self.placeholder:
            self.set_placeholder()
        
        self.bind('<FocusIn>', self.clear_placeholder)
        self.bind('<FocusOut>', self.restore_placeholder)

    def set_placeholder(self):
        """
        Set the placeholder text and color.
        """
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def clear_placeholder(self, event):
        """
        Clear the placeholder text and set the text color to the default color when the input box gains focus.

        Args:
            event (tkinter event): The tkinter event associated with the FocusIn event.
        """
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self.config(fg=self.default_color)

    def restore_placeholder(self, event):
        """
        Restore the placeholder text and color when the input box loses focus, and no input is given.

        Args:
            event (tkinter event): The tkinter event associated with the FocusOut event.
        """
        if not self.get():
            self.set_placeholder()