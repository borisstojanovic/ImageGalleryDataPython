import plotly.graph_objects as go
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import Images, Comment, User
import plotly
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(req):
    return render(req, 'imagestat\\index.html', {'page_title': 'ImageStat'})


def images(req):
    image_list = Images.objects.all()
    page = req.GET.get('page', 1)

    paginator = Paginator(image_list, 7)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    return render(req, 'imagestat\\images.html', {'images': images})


def users(req):
    user_list = User.objects.all()
    page = req.GET.get('page', 1)

    paginator = Paginator(user_list, 7)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(req, 'imagestat\\users.html', {'users': users})


def imagesbydate(request):
    images = Images.objects.extra({'time': "date(time)"}). \
        values('time').annotate(created_count=Count('id')).order_by('time')

    images = list(images)

    if len(images) == 0:
        return render(request, "imagestat\\graph.html", context={'title': "No Data"})
    else:
        y_data = [x.get('created_count') for x in images]
        x_data1 = [x.get('time') for x in images]
        scatter = plotly.graph_objs.Scatter(x=x_data1, y=y_data, name='New Images', mode='markers + lines')

        y_data2 = [x.get('created_count') for x in images]
        x_data2 = [x.get('time') for x in images]

        i = 1
        while len(y_data2) > i:
            y_data2[i] = y_data2[i - 1] + y_data2[i]
            i += 1

        scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Total Images', mode='markers + lines')

        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data1[0] if len(x_data1) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day
        fig = plotly.graph_objs.Figure(data=[scatter, scatter2], layout=layout)
        plot_div = plot(fig, output_type='div')
        return render(request, "imagestat\\graph.html", context={'title': "Images", 'plot_div': plot_div})


def usersbydate(request):
    x_data = User.objects.extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)

    if len(x_data) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': "No Data"})
    else:
        y_data = [x.get('created_count') for x in x_data]
        x_data2 = [x.get('date_created') for x in x_data]
        scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data, name='New Users', mode='markers + lines')

        y_data2 = [x.get('created_count') for x in x_data]
        i = 1
        while len(y_data2) > i:
            y_data2[i] = y_data2[i - 1] + y_data2[i]
            i += 1

        scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Total Users', mode='markers + lines')

        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data2[0] if len(x_data2) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day
        fig = plotly.graph_objs.Figure(data=[scatter, scatter2], layout=layout)
        plot_div = plot(fig, output_type='div')
        return render(request, "imagestat\\graph.html", context={'title': "Users", 'plot_div': plot_div})


def commentsbydate(request):
    x_data = Comment.objects.extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    if len(x_data) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': "No Data"})
    else:
        y_data = [x.get('created_count') for x in x_data]
        x_data2 = [x.get('date_created') for x in x_data]
        scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data, name='New Comments', mode='markers + lines')

        y_data2 = [x.get('created_count') for x in x_data]
        i = 1
        while len(y_data2) > i:
            y_data2[i] = y_data2[i - 1] + y_data2[i]
            i += 1

        scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Total Comments', mode='markers + lines')

        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data2[0] if len(x_data2) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day
        fig = plotly.graph_objs.Figure(data=[scatter, scatter2], layout=layout)
        plot_div = plot(fig, output_type='div')
        return render(request, "imagestat\\graph.html", context={'title': "Comments", 'plot_div': plot_div})


def commentsbyimage(request, id):
    x_data = Comment.objects.filter(image_id=id).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    if len(x_data) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': "No Data"})
    else:
        y_data = [x.get('created_count') for x in x_data]
        x_data2 = [x.get('date_created') for x in x_data]
        scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data)
        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data2[0] if len(x_data2) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day
        fig = plotly.graph_objs.Figure(data=[scatter], layout=layout)
        plot_div = plot(fig, output_type='div')
        return render(request, "imagestat\\graph.html", context={'plot_div': plot_div})


def commentsbyimagetotal(request, id):
    x_data = Comment.objects.filter(image_id=id).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    if len(x_data) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': 'No Data'})
    else:
        y_data = [x.get('created_count') for x in x_data]
        i = 1
        while len(y_data) > i:
            y_data[i] = y_data[i - 1] + y_data[i]
            i += 1

        x_data2 = [x.get('date_created') for x in x_data]
        scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data)
        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data2[0] if len(x_data2) else datetime.datetime.now(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day
        fig = plotly.graph_objs.Figure(data=[scatter], layout=layout)
        plot_div = plot(fig, output_type='div')
        return render(request, "imagestat\\graph.html", context={'plot_div': plot_div})


def useractivity(request, id):
    comments = Comment.objects.filter(user_id=id).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')

    images = Images.objects.filter(owner_id=id).extra({'time': "date(time)"}). \
        values('time').annotate(created_count=Count('id')).order_by('time')

    if len(comments) == 0 and len(images) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': "No data"})
    else:
        comments = list(comments)
        y_data1 = [x.get('created_count') for x in comments]

        x_data1 = [x.get('date_created') for x in comments]
        scatter1 = plotly.graph_objs.Scatter(x=x_data1, y=y_data1, name='Comments', mode='markers + lines')

        images = list(images)
        y_data2 = [x.get('created_count') for x in images]

        x_data2 = [x.get('time') for x in images]
        scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Images', mode='markers + lines')

        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data1[0] if len(x_data1) else x_data2[0] if len(
                                                     x_data2) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day

        fig = plotly.graph_objs.Figure(data=[scatter1, scatter2], layout=layout)
        plot_div = plot(fig, output_type='div')

        return render(request, "imagestat\\graph.html", context={'plot_div': plot_div})


def totalactivity(request):
    comments = Comment.objects.extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')

    images = Images.objects.extra({'time': "date(time)"}). \
        values('time').annotate(created_count=Count('id')).order_by('time')

    users = User.objects.extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')

    if len(comments) == 0 and len(images) == 0 and len(users) == 0:
        return render(request, "imagestat\\graph.html", context={'plot_div': "No data"})
    else:
        comments = list(comments)
        y_data1 = [x.get('created_count') for x in comments]

        x_data1 = [x.get('date_created') for x in comments]
        scatter1 = plotly.graph_objs.Scatter(x=x_data1, y=y_data1, name='Comments', mode='markers + lines')

        images = list(images)
        y_data2 = [x.get('created_count') for x in images]

        x_data2 = [x.get('time') for x in images]
        scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Images', mode='markers + lines')

        users = list(users)
        y_data3 = [x.get('created_count') for x in users]
        x_data3 = [x.get('date_created') for x in users]
        scatter3 = plotly.graph_objs.Scatter(x=x_data3, y=y_data3, name='Users', mode='markers + lines')

        layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                                 'tick0': x_data1[0] if len(x_data1) else x_data2[0] if len(
                                                     x_data2) else datetime.date.today(),
                                                 'tickmode': 'linear',
                                                 'dtick': 86400000.0 * 1})  # 1 day

        fig = plotly.graph_objs.Figure(data=[scatter1, scatter2, scatter3], layout=layout)
        plot_div = plot(fig, output_type='div')

        return render(request, "imagestat\\graph.html", context={'plot_div': plot_div})
