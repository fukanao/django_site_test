from django.shortcuts import render

# myapp/views.py
from myapp.models import Blog
from myapp.models import Products
from myapp.forms import BlogForm
from myapp.forms import EditBlogForm

from django.template import loader

import pprint

from django.views.generic import TemplateView
from django.db.models import Max


class PortalView(TemplateView):
    template_name = 'myapp/portal.html'


class InputBlogObject:
    def __init__(self):
        ## id最大値取得
        #maxid_object = Blog.objects.aggregate(Max('id_num'))
        #self.maxid =  int(maxid_object['id_num__max'])
        self.maxid = 0
        print('#25', self.maxid)
        self.title = ''
        self.text = ''
    def set_maxid(self, maxid):
        self.maxid = maxid


maxid_object = Blog.objects.aggregate(Max('id_num'))
maxid =  int(maxid_object['id_num__max'])
input_blog_object_list = []
form_num = 0


def blog_form(request):
    form = BlogForm
    global maxid
    global form_num
    global input_blog_object_list

    ## id最大値取得
    #maxid_object = Blog.objects.aggregate(Max('id_num'))
    #maxid = int(maxid_object['id_num__max'])

    ## 入力値オブジェクト作成
    obj = InputBlogObject()
    obj.set_maxid(maxid)

    ## 入力値オブジェクトへインプット関数
    def input_blog_object(form_num, maxid, title, text):
        input_blog_object_list[form_num].maxid = maxid
        input_blog_object_list[form_num].title = form.cleaned_data['title']
        input_blog_object_list[form_num].text = form.cleaned_data['text']
        #print('#49',input_blog_object_list[form_num].maxid)


    def debug_var():
        print('form_num =',form_num)
        print('maxid =',maxid)
        print('len object_list =',len(input_blog_object_list))
        for o in input_blog_object_list:
            print('maxid=',o.maxid)

    print('#58')
    debug_var()

    if request.method == 'POST':
        form = BlogForm(request.POST)

        ## プレビューページへ
        if form.is_valid() and ('button_1' in request.POST):
            context = { 'form': form,
                        'compo_num': form_num + 1
                        }
            # object listへobjectを追加
            input_blog_object_list.append(obj)

            maxid += 1

            ## objectへインプットメソッド
            input_blog_object(form_num, maxid, form.cleaned_data['title'],form.cleaned_data['title'])

            print('#77')
            debug_var()

            return render(request, 'myapp/est_preview.html', context = context)

        ## 登録してもう一つの構成登録する
        elif form.is_valid() and ('button_2' in request.POST):
            form_num += 1
            maxid += 1
            #obj = InputBlogObject()
            #input_blog_object_list.append(obj)
            #print('#75',input_blog_object_list[form_num].maxid)
            print('#89')
            debug_var()


            ## objectへインプットメソッド
            #input_blog_object(form_num, maxid + 1, form.cleaned_data['title'],form.cleaned_data['title'])
            context = {
                'form': form,
                'compo_num': form_num + 1
            }

            return render(request, 'myapp/blog_form.html', context = context)


        ## 登録してその他製品登録ページへ
        elif form.is_valid() and ('button_3' in request.POST):
            '''
            blog = Blog.objects.create(
                id_num = input_blog_object_list[form_num].maxid,
                title = input_blog_object_list[form_num].title,
                text = input_blog_object_list[form_num].text,
            )
            '''

            for input_object in input_blog_object_list:
                blog = Blog.objects.create(
                        id_num = input_object.maxid,
                        title = input_object.title,
                        text = input_object.text,
                )

            # object list初期化
            input_blog_object_list = []
            form_num = 0

            return render(request, 'myapp/est_register_ok.html')

    print('#100',form_num)
    context = {
        'form': form,
        'compo_num': form_num + 1
    }

    return render(request, 'myapp/blog_form.html', context)




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
