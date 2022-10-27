
# myapp/forms.py
from django import forms
from django.forms import Form, ModelForm, IntegerField
from django.core.exceptions import ValidationError
from .models import Blog
from .models import Products

data = Products.objects.all()

products = []

for tmp in data:
    products.append(tmp.product)


#def check_product(input, products_list): で使いまわし
def check_name(input_product, products_list):

    list_num = len(products_list)

    for product in products_list:
        if input_product == product:
            break
    else:
        raise ValidationError('\'' + input_product + '\' リストに存在しない製品番号です')

    if input_product == 'hello':
        raise ValidationError('一致した場合のエラーです')

def check_product(value):
    check_name(value, products)

def check_text(value):
    if value == 'world':
        raise ValidationError('一致した場合のエラーです')


class BlogForm(forms.Form):

    '''
    id_num = IntegerField(
            label='ID', required=True
    )
    '''

    # 入力がからの場合はチェックにまわさない
    title = forms.CharField(
        label='タイトル',
        #required=True,
        required=False,
        max_length=150,
        ##validators=[check_product],
        #initial=initial_title,
    )

    text = forms.CharField(
        label='テキスト',
        required=True,
        max_length=500,
        widget=forms.Textarea,
        ##validators=[check_text],
        #initial=initial_text,
    )


class EditBlogForm(forms.Form):

    # 入力がからの場合はチェックにまわさない

    #print("period:1")

    id_num = forms.IntegerField(
            label='ID',
    )

    title = forms.CharField(
        label='タイトル',
        #required=True,
        required=False,
        max_length=150,
        #validators=[check_title],
        ##validators=[check_product],
        #initial=initial_title,
    )
    text = forms.CharField(
        label='テキスト',
        required=True,
        max_length=500,
        widget=forms.Textarea,
        ###validators=[check_text],
        #initial=initial_text,
    )

