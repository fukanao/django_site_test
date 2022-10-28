from django.shortcuts import render

# myapp/views.py
from myapp.models import Blog
from myapp.models import Products
from myapp.forms import CompoForm
from myapp.forms import EditBlogForm

from django.template import loader

import pprint

from django.views.generic import TemplateView
from django.db.models import Max


class PortalView(TemplateView):
    template_name = 'myapp/portal.html'


class InputCompoObject:
    def __init__(self):
        ## id最大値取得
        self.maxid = 0
        self.title = ''
        self.text = ''
    def set_maxid(self, maxid):
        self.maxid = maxid


compo_maxid_object = Blog.objects.aggregate(Max('id_num'))
compo_maxid =  int(compo_maxid_object['id_num__max'])
input_compo_object_list = []
compo_form_num = 0


def compo_form(request):
    form = CompoForm
    global compo_maxid
    global compo_form_num
    global input_compo_object_list

    ## 入力値オブジェクト作成
    compo_obj = InputCompoObject()
    compo_obj.set_maxid(compo_maxid)

    ## 入力値オブジェクトへインプット関数
    def input_compo_object(form_num, compo_maxid, title, text):
        input_compo_object_list[form_num].maxid = compo_maxid
        input_compo_object_list[form_num].title = form.cleaned_data['title']
        input_compo_object_list[form_num].text = form.cleaned_data['text']

    ## 変数デバッグ用関数
    def debug_var():
        print('form_num =',compo_form_num)
        print('compo_maxid =',compo_maxid)
        print('len object_list =',len(input_compo_object_list))
        for o in input_compo_object_list:
            print('object maxid=',o.maxid)

    print('#68 blog_form実行直後')
    debug_var()

    ## 構成入力画面
    if request.method == 'POST':
        form = CompoForm(request.POST)

        ## プレビューページへ
        if form.is_valid() and ('button_1' in request.POST):
            context = { 'form': form,
                        'compo_num': compo_form_num + 1
                        }
            # object listへobjectを追加
            input_compo_object_list.append(compo_obj)

            compo_maxid += 1

            ## objectへ入力値インプット
            input_compo_object(compo_form_num, compo_maxid, form.cleaned_data['title'],form.cleaned_data['title'])

            print('#87 button_1押した時')
            debug_var()

            return render(request, 'myapp/est_preview.html', context = context)

        ## もう一つの構成登録する
        elif form.is_valid() and ('button_2' in request.POST):
            compo_form_num += 1
            print('#100 button_2押した時')
            debug_var()
            context = {
                'form': form,
                'compo_num': compo_form_num + 1
            }

            return render(request, 'myapp/compo_form.html', context = context)


        ## DBに登録してその他製品登録ページへ
        elif form.is_valid() and ('button_3' in request.POST):
            for input_object in input_compo_object_list:
                blog = Blog.objects.create(
                        id_num = input_object.maxid,
                        title = input_object.title,
                        text = input_object.text,
                )

            # compo object list初期化
            input_compo_object_list = []
            compo_form_num = 0

            print('#135 button_3押した時')
            debug_var()

            return render(request, 'myapp/est_register_ok.html')


        ## リセット
        elif form.is_valid() and ('button_4' in request.POST):
            input_compo_object_list = []
            compo_form_num = 0
            form.title = ''
            form.text = ''

            context = {
                'form': form,
                'compo_num': compo_form_num + 1
            }

            return render(request, 'myapp/compo_form.html', context = context)

    context = {
        'form': form,
        'compo_num': compo_form_num + 1
    }

    return render(request, 'myapp/compo_form.html', context)


def edit_blog_form(request):

    initial_dict = dict(title="TITLE222", text="テキスト")

    form = EditBlogForm(request.GET or None, initial=initial_dict)

    if request.method == 'POST':
        form = EditBlogForm(request.POST)
        if form.is_valid() and ('button_1' in request.POST):
            context = { 'form': form }
            print('button_1')
            return render(request, 'myapp/est_preview.html', context = context)

        elif form.is_valid() and ('button_2' in request.POST):

            ### data 更新時は update(sqlite3)
            blog = Blog.objects.update(
                id_num = form['id_num'].data,
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
            )
 
            return render(request, 'myapp/est_register_ok.html')

    context = {
        'form': form
    }

    return render(request, 'myapp/blog_form.html', dict(form=form))




def list_data(request):

    # dataをリスト表示とデータ選択

    data = Blog.objects.all()
    context = {
            'data': data,
    }

    if request.method == 'POST':
        post_data = request.POST
        post_data_list = list(post_data)
        print('button_value = ', str(post_data_list[1])) #押されたボタンデータ
        print('button_value = ', str(post_data_list[0])) #押されたボタンデータ


        select_id = str(post_data_list[1])
        print("slect_id = ", select_id)

        #押されたボタンデータでデータフィルタ
        select_data = Blog.objects.filter(id_num = select_id)

        id_num = select_data[0].id_num
        title = select_data[0].title
        text = select_data[0].text

        initial_dict = dict(id_num = id_num, title = title, text = text)

        form = EditBlogForm(request.GET or None, initial=initial_dict)

        return render(request, 'myapp/edit_blog_form.html', dict(form=form))

    return render(request, 'myapp/list.html', context)


def select(request):
    
    # ボタン区別テスト

    if request.method == 'POST':
        post_data = request.POST
        print('post_data = ',post_data)

        #print(request.POST["button_1"])

        if 'button_1' in request.POST:
            print("button_1 press!")

            id = 1
            context = data_process(id)

            return render(request, 'myapp/show_data.html', context)

        elif 'button_2' in request.POST:
            #context = { 'id': 2 }

            print("button_2 press!")
        
            id = 2
            context = data_process(id)

            return render(request, 'myapp/show_data.html', context)

    return render(request, 'myapp/select.html')


def show_data(request):

    id = 1

    context = { 'id': id, }

    return render(request, 'myapp/show_data.html', context)

def data_process(id):

    print('data_process!')
    context = {
            'id' : id,
    }

    return context
