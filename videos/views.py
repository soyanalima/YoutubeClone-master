from django.db.models import Count
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, View
from django.views.decorators.http import require_http_methods
from django.core import serializers

from django.shortcuts import render

from .models import Video, Comment

videos = [
  {
    "model": "videos.video",
    "pk": 1,
    "fields": {
      "title": "Wakey Wakey...",
      "views": 0,
      "author": "Don't Hug Me .I'm Scared",
      "youtube_id": "tkFpNVxzhTs",
      "thumbnail_url": "https://i.ytimg.com/vi/tkFpNVxzhTs/default.jpg",
      "slug": "wakey-wakey",
      #"active": true,
      "likes": [
        1
      ],
      "dislikes": [
        1
      ]
    }
  }
]
    
def list_videos(request):
    return render(request,'videos/list.html', {'videos': videos})


class VideoListView(ListView):
    model=Video
    template_name="videos/list.html"
    paginate_by = 1

class VideoDetailView(DetailView):
    model=Video
    template_name="videos/detail.html"
    query_set=Video.objects.all()
    slug_field="slug"
    slug_url_kwarg="slug"

    def get_context_data(self, **kwargs):
        ContextOfTheView=super().get_context_data(**kwargs)

        video=self.get_object()

        likes=Video.objects.filter(youtube_id=video.youtube_id).aggregate(dislikes_count=Count('dislikes'), likes_count=Count('likes'))

        ContextOfTheView["comments"]=Comment.objects.filter(video=video)
        ContextOfTheView["likes"]=likes
        return ContextOfTheView



    def render_to_response(self, context, **response_kwargs):
        video=self.get_object()
        video.views=video.views + 1
        video.save()
        
        return super().render_to_response(context, **response_kwargs)

@require_http_methods(["POST"])
def comment_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user
    x=Video.objects.get(youtube_id=youtube_id)
    
    comment_req=request.POST.get("comment")
    
    comment=Comment.objects.create(
        video=x,
        user=user_logged,
        comment=comment_req
    )

    return redirect(reverse_lazy("videos:detail", kwargs={"slug": x.slug}))



@require_http_methods(["POST"])
def like_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user

    video=Video.objects.filter(youtube_id=youtube_id).first()

    if not video:
        return JsonResponse({'error': 'invalid video id'}, status=400)

    video.likes.add(user_logged)

    video.save()

    data={
        "ok": "Like saved"
    }

    return JsonResponse(initial_data)


@require_http_methods(["POST"])
def dislike_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user

    video=Video.objects.filter(youtube_id=youtube_id, active=True)[0]
    

    video.dislikes.add(user_logged)

    video.save()
   
    data={
        "ok": "Dislike saved"
    }

    return JsonResponse(initial_data)

