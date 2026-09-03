from django import forms

from blog_app.models import Article


class _CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "status", "content", "twitter_post")  # "word_count"


class CreateArticleForm(forms.Form):
    ARTICLE_STATUSES = (
        ("draft", "draft"),
        ("inprogress", "in progress"),
        ("published", "published"),
    )
    title = forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=ARTICLE_STATUSES)
    content = forms.CharField(widget=forms.Textarea)
    # word_count = forms.IntegerField()
    twitter_post = forms.CharField(widget=forms.Textarea, required=False)
