from django import forms

from notes.models import Notes


class CreateNoteForm(forms.ModelForm):

	class Meta:
		model = Notes
		fields = ['title', 'body','share_view','share_edit']



class UpdateNoteForm(forms.ModelForm):

	class Meta:
		model = Notes
		fields = ['title', 'body','share_view','share_edit']

	def save(self, commit=True):
		notes = self.instance
		notes.title = self.cleaned_data['title']
		notes.body = self.cleaned_data['body']
		notes.share_view = self.cleaned_data['share_view']
		notes.share_edit = self.cleaned_data['share_edit']



		if commit:
			notes.save()
		return notes