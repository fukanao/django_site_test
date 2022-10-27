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
        maxid_object = Blog.objects.aggregate(Max('id_num'))
        self.maxid =  int(maxid_object['id_num__max'])
        print('#25', self.maxid)
        self.title = ''
        self.text = ''

input_blog_object_list = []
form_num = 0

def blog_form(request):
    form = BlogForm

    ## id最大値取得
    maxid_object = Blog.objects.aggregate(Max('id_num'))
    maxid = int(maxid_object['id_num__max'])

    ## 入力値オブジェクト作成
    obj = InputBlogObject()
    #input_blog_object_list.append(obj)
    print('#43 len =',len(input_blog_object_list))

    ## 入力値オブジェクトへインプット関数
    def input_blog_object(form_num, maxid, title, text):
        input_blog_object_list[form_num].maxid = maxid
        input_blog_object_list[form_num].title = form.cleaned_data['title']
        input_blog_object_list[form_num].text = form.cleaned_data['text']
        print('#49',input_blog_object_list[form_num].maxid)

    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid() and ('button_1' in request.POST):
            context = { 'form': form }

            # object listへobjectを追加
            input_blog_object_list.append(obj)

            ## objectへインプットメソッド
            input_blog_object(form_num, maxid + 1, form.cleaned_data['title'],form.cleaned_data['title'])
            print('#56',maxid + 1)
            return render(request, 'myapp/est_preview.html', context = context)

        elif form.is_valid() and ('button_3' in request.POST):
            '''
            blog = Blog.objects.create(
                id_num = input_blog_object_list[form_num].maxid,
                title = input_blog_object_list[form_num].title,
                text = input_blog_object_list[form_num].text,
            )
            '''

            for input_object in input_blog_object_list:
                print('#69',input_object.maxid)
                blog = Blog.objects.create(
                        id_num = input_object.maxid,
                        title = input_object.title,
                        text = input_object.text,
                )
 
            return render(request, 'myapp/est_register_ok.html')

    #print('Prevew POST!')

    context = {
        'form': form
    }

    print(form)
    return render(request, 'myapp/blog_form.html', context)




def edit_blog_form(request):

    initial_dict = dict(title="TITLE222", text="テキスト")
    #initial_dict = dict(title="", text="")

    form = EditBlogForm(request.GET or None, initial=initial_dict)
    #form = EditBlogForm
    #form = EditBlogForm("TITLE")

    #print("form = ", str(form))

    if request.method == 'POST':
        form = EditBlogForm(request.POST)
        #if form.is_valid():
        #print('POST')
        if form.is_valid() and ('button_1' in request.POST):
            context = { 'form': form }
            print('button_1')
            return render(request, 'myapp/est_preview.html', context = context)

        elif form.is_valid() and ('button_2' in request.POST):

            #blog = Blog.objects.create(

            ### data 更新時は update(sqlite3)
            blog = Blog.objects.update(
            #blog = Blog.objects.save(
                id_num = form['id_num'].data,
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
            )
 
            print('button_2')
            return render(request, 'myapp/est_register_ok.html')

    #print('Prevew POST!')

    context = {
        'form': form
    }

    #print("form = ",form)

    #return render(request, 'myapp/blog_form.html', context)
    return render(request, 'myapp/blog_form.html', dict(form=form))




def list_data(request):

    # dataをリスト表示とデータ選択

    data = Blog.objects.all()
    context = {
            'data': data,
    }

    if request.method == 'POST':
        post_data = request.POST
        #print('post_data = ',post_data)
        post_data_list = list(post_data)
        #print('post_data_list_1 = ', str(post_data_list))
        print('button_value = ', str(post_data_list[1])) #押されたボタンデータ
        print('button_value = ', str(post_data_list[0])) #押されたボタンデータ

        #print(str(data.post_data_list[1]))

        select_id = str(post_data_list[1])
        print("slect_id = ", select_id)

        #押されたボタンデータでデータフィルタ
        #select_data = Blog.objects.filter(title = select_title)
        select_data = Blog.objects.filter(id_num = select_id)

        print("select_data[0].id_num = ",select_data[0].id_num)
        print("select_data[0].title = ",select_data[0].title)
        print("select_data[0].text = ",select_data[0].text)

        id_num = select_data[0].id_num
        title = select_data[0].title
        text = select_data[0].text


        initial_dict = dict(id_num = id_num, title = title, text = text)
        #initial_dict = dict(title="TITLE222", text="テキスト")
        #initial_dict = dict(title="", text="")

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

            #context = { 'id': 1 }

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
