"""
This file is part of SyFoS.
SyFoS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SyFoS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SyFoS.  If not, see <http://www.gnu.org/licenses/>.
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LabeledParameterInput(ttk.Frame):
	"""Custom widget for the input of parameter values.
	   It combines a parameter label a checked input and
	   a unit label."""
	def __init__(
		self, 
		root,
		label,
		formulaCharacter,
		formulaCharacterSubscript,
		labelWidth,
		placeholder,
		valueBoundaries,
		unitLabel 
	):
		super().__init__(root)

		self.label = ParameterLabel(
			self,
			label,
			formulaCharacter,
			formulaCharacterSubscript,
			labelWidth
		)
		self.label.pack(side=LEFT, fill=X, expand=YES)

		self.input = CheckedInput(
			self,
			placeholder,
			valueBoundaries
		)
		self.input.pack(side=LEFT, fill=X, expand=YES)

		self.unitLabel = UnitLabel(
			self,
			text=unitLabel
		)
		self.unitLabel.pack(side=LEFT, fill=X, expand=YES)

		self.set_placeholder()

	def set_placeholder(self):
		"""Set the input placeholder."""
		self.input.set_placeholder()

	def set(self, value:str):
		"""Set the value for the input.

		Parameters:
			value(str): New input value.
		"""
		self.input.set_value(value)

	def get(self):
		"""Get the value of the input."""
		return self.input.get()

	def check_for_valid_value(self):
		"""Check if the current input value is valid."""
		return self.input.validValue


class ParameterLabel(tk.Text):
	"""Custom label for the parameter input.
	   Consists of a name and a formula character
	   which can have an additional subscript."""
	def __init__(
		self, 
		root, 
		name, 
		formulaCharacter,
		formulaCharacterSubscript,
		width
	):
		super().__init__(root)

		self.name = name
		self.formulaCharacter = formulaCharacter
		self.formulaCharacterSubscript = formulaCharacterSubscript
		self.width = width

		self._setup_text_tags()
		self._insert_label()
		self._setup_config()

	def _setup_text_tags(self):
		"""Define the different text styles."""
		self.tag_configure(
			"name", 
			font=("Helvetica", 9)
		)
		self.tag_configure(
			"formulaCharacter", 
			font=("Helvetica", 9, "italic")
		)
		self.tag_configure(
			"formulaCharacterSubscript", 
			offset=-2, 
			font=("Helvetica", 8)
		)

	def _insert_label(self):
		"""Insert the given label."""
		self.insert(
			INSERT, 
			self.name, "name", 
			self.formulaCharacter, "formulaCharacter",
			self.formulaCharacterSubscript, "formulaCharacterSubscript"
		)

	def _setup_config(self):
		"""Adjust the config to make it look like a normal label."""
		self.config(
			state="disabled",
			borderwidth=0,
			highlightthickness=0,
			width=self.width, 
			height=1
		)


class CheckedInput(ttk.Entry):
	"""Extends the ttk entry by adding a placeholder 
	   and validation of the input values."""
	def  __init__(
		self, 
		root, 
		placeholder,
		valueBoundaries
	):
		super().__init__(root)

		self.placeholder = placeholder
		self.minValue = valueBoundaries[0]
		self.maxValue = valueBoundaries[1]

		self.validValue = False

		self.bind("<FocusIn>", self._check_for_placeholder)
		self.bind("<FocusOut>", self._validate_value, add="+")

	def set_placeholder(self):
		"""Set the placeholder."""
		self._delete_input()
		self._set_text_color_placeholder()
		self.insert(0, self.placeholder)

		self.validValue = False

	def set_value(self, value: str):
		"""Set the value.

		Parameters:
			value(str): New value.
		"""
		self._delete_input()
		self._set_text_color_valid()
		self.insert(0, value)

		self.validValue = True

	def _check_for_placeholder(self, *args):
		"""Check whether the placeholer is still set when the input get's focus."""
		if self.get() == self.placeholder:
			self.icursor(0)
			self.bind("<KeyPress>", self._remove_placeholder, add="+")

	def _remove_placeholder(self, *args):
		"""Remove the placeholder when something is entered."""
		self._delete_input()
		self._set_text_color_valid()
		self.unbind("<KeyPress>")

	def _validate_value(self, *args):
		"""Check if the input value is a number within it's value range."""
		try:
			currentValue = float(self.get())
		except ValueError:
			if self.get() == "":
				self.set_placeholder()
			elif self.get() != self.placeholder:
				self._hint_false_input()
		else:
			if self.minValue <= currentValue <= self.maxValue:
				self._show_valid_input()
			else:
				self._hint_false_input()

	def _show_valid_input(self):
		"""Mark valid input."""
		self._set_text_color_valid()

		self.validValue = True
			
	def _hint_false_input(self):
		"""Highlight invalid input"""
		self._set_text_color_invalid()

		self.validValue = False

	def _set_text_color_placeholder(self):
		"""Set the text color for the place holder."""
		self.config(foreground="#c4c4c4")

	def _set_text_color_valid(self):
		"""Set the text color for a valid input."""
		self.config(foreground="gray")

	def _set_text_color_invalid(self):
		"""Set the text color for an invalid input."""
		self.config(foreground="red")

	def _delete_input(self):
		"""Delete the current input."""
		self.delete(0, len(self.get()))

class UnitLabel(ttk.Label):
	"""Label to display the unit of the input value."""
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)

		self.config(font=("Helvetica", 8))