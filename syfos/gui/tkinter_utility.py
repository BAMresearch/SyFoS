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
	"""Custom widget"""
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
		""""""
		self.input.set_placeholder()

	def set(self, value:str):
		""""""
		self.input.set_value(value)

	def get(self):
		""""""
		return self.input.get()

	def check_value(self):
		""""""
		return self.input.validValue


class ParameterLabel(tk.Text):
	""""""
	def __init__(
		self, 
		root, 
		label, 
		formulaCharacter,
		formulaCharacterSubscript,
		width
	):
		super().__init__(root)

		self.label = label
		self.formulaCharacter = formulaCharacter
		self.formulaCharacterSubscript = formulaCharacterSubscript
		self.width = width

		self._setup_text_tags()
		self._insert_label()
		self._setup_config()

	def _setup_text_tags(self):
		"""Define the different text styles."""
		self.tag_configure(
			"label", 
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
			self.label, "label", 
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
	"""Helper class that extends the ttk entry by adding a placeholder 
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

		self.bind("<FocusIn>", self._change_value)
		self.bind("<FocusOut>", self._validate_value, add="+")

	def set_placeholder(self):
		"""Set the placeholder."""
		self._delete_input()
		self._set_text_color_placeholder()
		self.insert(0, self.placeholder)

		self.validValue = False

	def set_value(self, value: str):
		""""""
		self._delete_input()
		self._set_text_color_valid()
		self.insert(0, value)

		self.validValue = True

	def _change_value(self, *args):
		""""""
		if self.get() == self.placeholder:
			self.icursor(0)
			self.bind("<KeyPress>", self._remove_placeholder, add="+")

	def _remove_placeholder(self, *args):
		"""Remove the placeholder when something is entered."""
		self._delete_input()
		self._set_text_color_valid()
		self.unbind("<KeyPress>")

	def _validate_value(self, *args):
		"""Check if the input value is a number and within it's value range."""
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
		self.config(foreground="gray")

	def _set_text_color_valid(self):
		"""Set the text color for a valid input."""
		self.config(foreground="black")

	def _set_text_color_invalid(self):
		"""Set the text color for an invalid input."""
		self.config(foreground="red")

	def _delete_input(self):
		"""Delete the current input."""
		self.delete(0, len(self.get()))

class UnitLabel(ttk.Label):
	""""""
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)

		self.config(font=("Helvetica", 8))