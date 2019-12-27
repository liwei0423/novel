from django.http import HttpResponse
from django.shortcuts import render
from utils.mysql_DBUtils import mysql
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 《星辰变》章节列表
def main(request):
    sql = "SELECT id,title FROM novel order by id asc;"
    book_list = mysql.getAll(sql)
    # result = json.dumps(result, cls=MyEncoder, ensure_ascii=False, indent=4)
    # result = json.loads(result)

    paginator = Paginator(book_list, 10)

    try:
        current_num = int(request.GET.get('page',1))  #当你在url内输入的?page = 页码数  显示你输入的页面数目 默认为第2页
        book_list = paginator.page(current_num)
    except EmptyPage:
            book_list = paginator.page(1)  #当你输入的page是不存在的时候就会报错

    if paginator.num_pages > 11:  # 如果分页的数目大于11
            if current_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 11)  # 按钮数
            elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(current_num - 5, current_num + 1)  # 显示的按钮数

            else:
                pageRange = range(current_num - 5, current_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

    else:
        pageRange = paginator.page_range()  # 正常分配

    #context = {'book_list': book_list,'pageRange': pageRange}
    return render(request, 'novel_list.html',  locals())


# def chapter(request):
#     id = request.GET['id']
#     sql = "SELECT content FROM novel where id = %(id)s;"
#     param = {"id": id}
#     result = mysql.getOne(sql, param)
#     result['content'] = result['content'].decode('utf-8')
#     context = {}
#     context["content"] =  result['content']
#     return render(request, 'novel.html', context)

'''
单个章节
此处 novel_id 对应 urls.py 中的 <int:novel_id>
你可以访问：http://localhost:8000/chapter/1/
'''
def chapter(request, novel_id):
    sql = "SELECT title,content FROM novel where id = %(id)s;"
    param = {"id": novel_id}
    result = mysql.getOne(sql, param)
    # result['title'] = result['title'].decode('utf-8')
    # result['content'] = result['content'].decode('utf-8')
    context = {'novel': result}
    return render(request, 'novel.html', context)

