# form1_mvc - tkinter form #1 (extended)
#
# Based on the form1.py example by James Nash.
# Refactored and extended by Henrik Tunedal.
#
# This version demonstrates the Model-View-Controller design pattern
# and adds field validation functionality. Benefits of MVC:
#
#   1. The model and controller can be tested with automated unit tests.
#
#   2. Multiple views can present the same data by sharing a model.
#
# To run the unit tests, invoke the unittest module:
#
#   python3 -m unittest form1_mvc.py
#

import tkinter as tk
import tkinter.messagebox
from functools import partial
from unittest import TestCase
from unittest.mock import Mock


class Form1Model:
    def __init__(self, indata, validators={}):
        self.labels = list(indata.keys())
        self.values = {k: tk.StringVar(value=v) for k, v in indata.items()}
        self.errors = {k: tk.StringVar() for k in indata}
        self.is_valid = tk.BooleanVar()
        self.results = dict(indata)

        self._validators = validators
        self._invalid = set()

        for label, value in self.values.items():
            validate = partial(self._validate, label)
            TkVarBinding.bind_callback(validate, value)
            validate()

    def save(self):
        self.results = {k: var.get() for k, var in self.values.items()}

    def _validate(self, label):
        validator = self._validators.get(label)
        if validator:
            error = validator(self.values[label].get())
            self.errors[label].set(error or '')
            if error:
                self._invalid.add(label)
            elif label in self._invalid:
                self._invalid.remove(label)

        self.is_valid.set(not self._invalid)


class Form1View:
    def __init__(self, model, controller_factory, pos=None, title=None):
        self._model = model
        self._root = tk.Toplevel()
        self._controller = controller_factory(self)
        if pos:
            x, y = pos
            self._root.geometry('+%d+%d' % (x, y))
        if title:
            self._root.title(title)
        self._build_form()

    def close(self):
        self._root.destroy()

    def show_message(self, caption, text):
        tkinter.messagebox.showinfo(caption, text, parent=self._root)

    def _build_form(self):
        root, model, controller = self._root, self._model, self._controller

        for i, label in enumerate(model.labels):
            wlabel = tk.Label(root, text=label,
                              font=('calibre', 10, 'bold'))
            wentry = tk.Entry(root, textvariable=model.values[label],
                              highlightthickness=1,
                              font=('calibre', 10, 'normal'))
            werror = tk.Label(root, textvariable=model.errors[label],
                              foreground='red',
                              font=('calibre', 10, 'normal'))
            wlabel.grid(row=2*i, column=0)
            wentry.grid(row=2*i, column=1)
            werror.grid(row=2*i+1, column=1)

            TkVarBinding.bind_widget_property(
                wentry, 'highlightbackground',
                model.errors[label],
                partial(lambda error, default: 'red' if error else default,
                        default=wentry.cget('highlightbackground')))

        sub_btn = tk.Button(root, text='Submit', command=controller.on_submit)
        sub_btn.grid(row=2*(i+1), column=1)

        TkVarBinding.bind_widget_property(
            sub_btn, 'state',
            model.is_valid,
            lambda valid: 'normal' if valid else 'disabled')


class Form1Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def on_submit(self):
        model = self._model
        model.save()

        message = '\n'.join(f'{k}: {v}' for k, v in model.results.items())

        view = self._view
        view.show_message('Form submitted', message)
        view.close()


class TkApp:
    def __init__(self):
        self._root = tk.Tk()
        self._root.withdraw()
        self._root.bind_class('Toplevel', '<Destroy>',
                              self._on_toplevel_destroy, add='+')

    def run(self):
        self._root.mainloop()

    def close(self):
        self._root.event_generate('<Destroy>', when='tail')

    def _on_toplevel_destroy(self, event):
        windows = self._root.children.values()
        if not any(w is not event.widget for w in windows):
            self.close()


class TkVarBinding:
    def __init__(self, bound_var):
        self._bound_var = bound_var
        self._trace_id = None
        self._last_value = None

    @property
    def value(self):
        return self._bound_var.get()

    def bind(self, on_change):
        self.close()
        self._on_change = on_change
        self._last_value = self.value
        self._trace_id = self._bound_var.trace_add('write', self._on_write)

    def close(self):
        trace_id = self._trace_id
        if trace_id is not None:
            self._bound_var.trace_remove('write', trace_id)
            self._on_change = None
            self._last_value = None
            self._trace_id = None

    def _on_write(self, varname, index, mode):
        new_value = self.value
        if new_value != self._last_value:
            self._last_value = new_value
            self._on_change()

    @classmethod
    def bind_callback(cls, on_change, var):
        binding = cls(var)
        binding.bind(on_change)
        return binding

    @classmethod
    def bind_widget_property(cls, widget, propname, var, transform=None):
        def update_prop():
            value = transform(binding.value) if transform else binding.value
            widget.config({propname: value})

        def on_destroy(event):
            if event.widget is widget:
                binding.close()

        binding = cls.bind_callback(update_prop, var)
        widget.bind('<Destroy>', on_destroy, add='+')
        update_prop()


class ModelTest(TestCase):
    def test_that_it_returns_initial_values_initially(self):
        model = Form1Model({'a': '100'})
        self.assertEqual({'a': '100'}, model.results)

    def test_that_it_returns_saved_values_after_save(self):
        model = Form1Model({'a': '100'})
        binding = model.values['a']

        binding.set('200')
        model.save()
        binding.set('300')

        self.assertEqual({'a': '200'}, model.results)

    def test_that_it_validates_initial_data(self):
        validators = {'a': lambda s: s != 'good' and 'bad data'}
        valid_model = Form1Model({'a': 'good'}, validators)
        invalid_model = Form1Model({'a': 'bad'}, validators)

        self.assertTrue(valid_model.is_valid.get())
        self.assertEqual('', valid_model.errors['a'].get())
        self.assertFalse(invalid_model.is_valid.get())
        self.assertEqual('bad data', invalid_model.errors['a'].get())

    def test_that_it_validates_changed_data(self):
        validators = {'a': lambda s: s != 'good' and 'bad data'}
        valid_model = Form1Model({'a': 'good'}, validators)
        invalid_model = Form1Model({'a': 'bad'}, validators)

        valid_model.values['a'].set('bad')
        invalid_model.values['a'].set('good')

        self.assertFalse(valid_model.is_valid.get())
        self.assertEqual('bad data', valid_model.errors['a'].get())
        self.assertTrue(invalid_model.is_valid.get())
        self.assertEqual('', invalid_model.errors['a'].get())

    def setUp(self):
        # The StringVar objects used by the model require a Tkinter
        # main window, so we instantiate our TkApp class to create a
        # hidden window.
        try:
            self.__app = TkApp()
        except Exception:
            self.skipTest('Tkinter not available')

    def tearDown(self):
        self.__app.close()


class ControllerTest(TestCase):
    def test_that_it_saves_model_when_submitted(self):
        model, view, controller = self.__create_controller()
        controller.on_submit()
        model.save.assert_called()

    def test_that_it_closes_view_when_submitted(self):
        model, view, controller = self.__create_controller()
        controller.on_submit()
        view.close.assert_called()

    def test_that_it_displays_submitted_values(self):
        model, view, controller = self.__create_controller()
        model.save.side_effect = partial(
            model.results.update,
            {'a': 'AAA', 'b': 'BBB'})

        controller.on_submit()

        view.show_message.assert_called_once_with(
            'Form submitted', 'a: AAA\nb: BBB')

    def __create_controller(self):
        model = Mock(results={})
        view = Mock()
        controller = Form1Controller(model, view)
        return model, view, controller


def create_view(model, pos, title):
    create_controller = partial(Form1Controller, model)
    return Form1View(model, create_controller, pos, title)


def create_validator(error_message, required_condition):
    return lambda s: None if required_condition(s) else error_message


def main():
    defaults = {'name': '', 'password': 'abc123', 'phone': '+46-'}

    validators = {
        'name': create_validator(
            'Name is required',
            lambda s: len(s) > 0),
        'password': create_validator(
            'Password too short',
            lambda s: len(s) >= 6),
        'phone': create_validator(
            'Invalid character',
            lambda s: all(c in '+- 0123456789' for c in s)),
    }

    app = TkApp()

    model1 = Form1Model(defaults, validators)
    create_view(model1, (100, 100), 'Editing model 1')
    create_view(model1, (100, 300), 'Editing model 1')

    model2 = Form1Model(defaults, validators)
    create_view(model2, (500, 150), 'Editing model 2')
    create_view(model2, (500, 350), 'Editing model 2')

    app.run()
    print('model1 results:', model1.results)
    print('model2 results:', model2.results)


if __name__ == '__main__':
    main()
