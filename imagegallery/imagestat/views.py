import plotly.graph_objects as go
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import Images, Comment, User
import plotly
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home2(request):
    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8, marker_color='green')],
                    output_type='div')
    return render(request, "imagestat\\test2.html", context={'plot_div': plot_div})


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


def imagesbydate(request):
    x_data = Images.objects.extra({'date_created': "date(time)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('time')

    x_data = list(x_data)

    y_data = [x.get('created_count') for x in x_data]
    x_data2 = [x.get('date_created') for x in x_data]
    scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data)
    layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                             'tick0': x_data2[0] if len(x_data2) else datetime.date.today(),
                                             'tickmode': 'linear',
                                             'dtick': 86400000.0 * 1})  # 1 day
    fig = plotly.graph_objs.Figure(data=[scatter], layout=layout)
    plot_div = plot(fig, output_type='div')
    return render(request, "imagestat\\test2.html", context={'plot_div': plot_div})


def commentsbyimage(request, id):
    x_data = Comment.objects.filter(image_id=id).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    y_data = [x.get('created_count') for x in x_data]
    x_data2 = [x.get('date_created') for x in x_data]
    print(x_data2)
    print(y_data)
    scatter = plotly.graph_objs.Scatter(x=x_data2, y=y_data)
    layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                             'tick0': x_data2[0] if len(x_data2) else datetime.date.today(),
                                             'tickmode': 'linear',
                                             'dtick': 86400000.0 * 1})  # 1 day
    fig = plotly.graph_objs.Figure(data=[scatter], layout=layout)
    plot_div = plot(fig, output_type='div')
    return render(request, "imagestat\\test2.html", context={'plot_div': plot_div})


def commentsbyimagetotal(request, id):
    x_data = Comment.objects.filter(image_id=id).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    if len(x_data) == 0:
        return render(request, "imagestat\\test2.html", context={'plot_div': 'No Data'})
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
        return render(request, "imagestat\\test2.html", context={'plot_div': plot_div})


def useractivity(request):
    x_data = Comment.objects.filter(user_id=2).extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    y_data1 = [x.get('created_count') for x in x_data]

    x_data1 = [x.get('date_created') for x in x_data]
    scatter1 = plotly.graph_objs.Scatter(x=x_data1, y=y_data1, name='Comments', mode='markers + lines')

    x_data = Images.objects.filter(owner_id=2).extra({'time': "date(time)"}). \
        values('time').annotate(created_count=Count('id')).order_by('time')
    x_data = list(x_data)
    y_data2 = [x.get('created_count') for x in x_data]

    x_data2 = [x.get('time') for x in x_data]
    scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Images', mode='markers + lines')

    layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                             'tick0': x_data1[0] if len(x_data1) else x_data2[0] if len(x_data2) else datetime.date.today(),
                                             'tickmode': 'linear',
                                             'dtick': 86400000.0 * 1})  # 1 day

    fig = plotly.graph_objs.Figure(data=[scatter1, scatter2], layout=layout)
    plot_div = plot(fig, output_type='div')

    return render(request, "imagestat\\test2.html", context={'plot_div': plot_div})


def totalactivity(request):
    x_data = Comment.objects.extra({'date_created': "date(date_created)"}). \
        values('date_created').annotate(created_count=Count('id')).order_by('date_created')
    x_data = list(x_data)
    y_data1 = [x.get('created_count') for x in x_data]

    x_data1 = [x.get('date_created') for x in x_data]
    scatter1 = plotly.graph_objs.Scatter(x=x_data1, y=y_data1, name='Comments', mode='markers + lines')

    x_data = Images.objects.extra({'time': "date(time)"}). \
        values('time').annotate(created_count=Count('id')).order_by('time')
    x_data = list(x_data)
    y_data2 = [x.get('created_count') for x in x_data]

    x_data2 = [x.get('time') for x in x_data]
    scatter2 = plotly.graph_objs.Scatter(x=x_data2, y=y_data2, name='Images', mode='markers + lines')

    layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
                                             'tick0': x_data1[0] if len(x_data1) else x_data2[0] if len(x_data2) else datetime.datetime.now(),
                                             'tickmode': 'linear',
                                             'dtick': 86400000.0 * 1})  # 1 day

    fig = plotly.graph_objs.Figure(data=[scatter1, scatter2], layout=layout)
    plot_div = plot(fig, output_type='div')

    return render(request, "imagestat\\test2.html", context={'title': 'Activity', 'plot_div': plot_div})
