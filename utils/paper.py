'''
分页组件：
    使用方法：
        from  utils.paper import Pagination
        all_count = models.Host.objects.all().count()
        page_obj = Pagination(request.GET.get('page'),all_count,request.path_info)

        host_list=models.Host.objects.all()[page_obj.start:page_obj.end]
        return  render(request,"host.html",{"page_html":page_obj.page_html,"host_list":host_list})

    HTML：
        <style>
            .pager a{
                display: inline-block;
                padding: 3px 5px;
                margin: 0 3px;
                border: 1px solid #dddddd;
            }
            .pager a.active{
                background-color: cadetblue;
                color: white;
            }
        </style>
        <div class="pager">
            {{ page_html}}
        </div>

'''
# -*- coding: utf-8 -*-
__author__ = 'ShengLeQi'

from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self,current_page,total_count,base_url,per_page_count=10,max_page_num=11):
        """
        :param current_page:用户请求当前页
        :param per_page_count:每页显示条数
        :param base_url:基础路径
        :param total_count:数据库中查到的总条数
        :param max_page_num:最多页面上显示的页码
        """

        total_page_count, div = divmod(total_count, per_page_count)
        if div:
            total_page_count +=1
        self.total_page_count=total_page_count

        try:
            current_page=int(current_page)

        except Exception as  e:
            current_page=1

        if current_page>total_page_count:
            current_page=total_page_count

        self.current_page=current_page
        self.per_page_count=per_page_count
        self.base_url=base_url
        self.total_count=total_count
        self.max_page_num=max_page_num

    @property
    def start(self):
        return  (self.current_page - 1)*self.per_page_count

    @property
    def end(self):
        return  self.current_page*self.per_page_count

    @property
    def page_html(self):
        page_list = []

        half_max_page_num = int(self.max_page_num / 2)

        # 如果显示的页面数据小于最大页数
        if self.total_page_count <= self.max_page_num:
            page_start = 1
            page_end = self.total_page_count
        else:  # 如果显示的页面数据大于最大页数

            if self.current_page <= self.max_page_num:
                page_start = 1
                page_end = self.max_page_num
            else:
                if (self.current_page + 5) >= self.total_page_count:
                    page_start = self.total_page_count - 11
                    page_end = self.total_page_count
                else:
                    page_start = self.current_page - half_max_page_num  # 当前页-5
                    page_end = self.current_page + half_max_page_num  # 当前页+5

        # 上一页
        if self.current_page <= 1:
            prev = "<a href='#'>上一页</a>"
        else:
            prev = "<a href='%s?page=%s'>上一页</a>" % (self.base_url,self.current_page - 1,)
        page_list.append(prev)

        for i in range(page_start, page_end + 1):
            if i == self.current_page:  # 当点击当前页
                tag = "<a class='active' href='%s?page=%s'>%s</a>" % (self.base_url,i, i,)
            else:
                tag = "<a href='%s?page=%s'>%s</a>" % (self.base_url,i, i,)
            page_list.append(tag)

        # 下一页
        if self.current_page >= self.total_page_count:
            nex = "<a href='#'>下一页</a>"
        else:
            nex = "<a href='%s?page=%s'>下一页</a>" % (self.base_url,self.current_page + 1,)
        page_list.append(nex)

        return  mark_safe("".join(page_list))


