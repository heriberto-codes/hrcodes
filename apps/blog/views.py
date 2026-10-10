import re
from html import unescape

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django.urls import reverse

from apps.blog.models import Like, Post


GUARDRAILS_INSIGHT_SLUG = (
    'i-revived-my-reactredux-app-with-turtle-ai-and-learned-where-'
    'ai-guardrails-can-go-too-far'
)

RELATED_INSIGHT_CHANNELS = (
    {
        'slug': 'how-constraints-changed-the-way-i-think-about-algorithms',
        'name': 'Constraints',
        'frequency': '91.1',
    },
    {
        'slug': (
            'i-revived-a-9-year-old-app-with-openai-codex-with-a-product-'
            'engineer-mindset'
        ),
        'name': 'Revival',
        'frequency': '93.9',
    },
)

GUARDRAILS_CHAPTERS = (
    {
        'id': 'insight-problem',
        'number': '01',
        'label': 'Diagnose',
        'tone': 'paper',
        'heading': 'The Problem: More Than an Old React App',
    },
    {
        'id': 'insight-approach',
        'number': '02',
        'label': 'Structure',
        'tone': 'navy',
        'heading': 'The Approach: Plan-Driven Product Engineering',
    },
    {
        'id': 'insight-turtle',
        'number': '03',
        'label': 'Guardrail',
        'tone': 'image',
        'heading': 'Introducing Turtle AI',
    },
    {
        'id': 'insight-shipped',
        'number': '04',
        'label': 'Deliver',
        'tone': 'paper',
        'heading': 'What Turtle AI Helped Me Ship',
    },
    {
        'id': 'insight-learned',
        'number': '05',
        'label': 'Learn',
        'tone': 'navy',
        'heading': 'What I Learned from Turtle AI',
    },
    {
        'id': 'insight-heavy',
        'number': '06',
        'label': 'Rebalance',
        'tone': 'alert',
        'heading': 'Where Turtle AI Became Too Heavy',
    },
    {
        'id': 'insight-result',
        'number': '07',
        'label': 'Result',
        'tone': 'result',
        'heading': 'The Result',
    },
)

GUARDRAILS_HEADING_PATTERN = re.compile(
    r'(?=<h2(?:\s[^>]*)?>)',
    re.IGNORECASE,
)
GUARDRAILS_HEADING_TEXT_PATTERN = re.compile(
    r'<h2(?:\s[^>]*)?>(.*?)</h2>',
    re.IGNORECASE | re.DOTALL,
)
GUARDRAILS_PAYLOAD_HEADING = 'highlander react/redux project'
GUARDRAILS_PAYLOAD_LINK_PATTERN = re.compile(
    r'<a\b[^>]*\bhref=(["\'])(.*?)\1[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
GUARDRAILS_PAYLOADS = (
    {'label': '01 / Demo', 'title': 'Open Highlander React/Redux'},
    {'label': '02 / Source', 'title': 'Inspect the application'},
    {'label': '03 / Workflow', 'title': 'Inspect Turtle AI'},
)


def _guardrails_transcript(body):
    body_parts = GUARDRAILS_HEADING_PATTERN.split(body or '')
    intro = body_parts[0]
    chapters = [{**chapter, 'html': ''} for chapter in GUARDRAILS_CHAPTERS]
    chapter_indexes = {
        chapter['heading'].casefold(): index
        for index, chapter in enumerate(GUARDRAILS_CHAPTERS)
    }
    current_chapter_index = 0
    payload_html = ''
    collecting_payload = False

    for body_part in body_parts[1:]:
        heading_match = GUARDRAILS_HEADING_TEXT_PATTERN.match(body_part)
        if heading_match:
            heading = strip_tags(heading_match.group(1)).strip().casefold()
            if heading == GUARDRAILS_PAYLOAD_HEADING:
                collecting_payload = True
            current_chapter_index = chapter_indexes.get(
                heading,
                current_chapter_index,
            )

        if collecting_payload:
            payload_html += body_part
            continue

        chapters[current_chapter_index]['html'] += body_part

    payload_matches = GUARDRAILS_PAYLOAD_LINK_PATTERN.findall(payload_html)
    if len(payload_matches) == len(GUARDRAILS_PAYLOADS):
        payloads = [
            {
                **payload,
                'href': unescape(payload_match[1]),
            }
            for payload, payload_match in zip(
                GUARDRAILS_PAYLOADS,
                payload_matches,
            )
        ]
    else:
        chapters[-1]['html'] += payload_html
        payloads = []

    return intro, chapters, payloads

def blog_index(request):
    try: 
        posts = Post.objects.all().order_by('-created_on')
        context = {
            'posts': posts,
        }
        return render(request, 'blog/blog_index.html', context)
    
    except Post.DoesNotExist:
        return render(request, 'blog_post_error_page.html')

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts":posts
    }
    return render(request, 'blog/blog_category.html', context)

def blog_detail(request, pk, slug):
    post = get_object_or_404(
        Post.objects.prefetch_related('categories'),
        pk=pk,
        slug=slug,
        status=1,
    )

    if post.slug == GUARDRAILS_INSIGHT_SLUG:
        insight_intro, insight_chapters, insight_payloads = (
            _guardrails_transcript(post.body)
        )
        related_posts_by_slug = {
            related_post.slug: related_post
            for related_post in Post.objects.filter(
                slug__in=[
                    channel['slug'] for channel in RELATED_INSIGHT_CHANNELS
                ],
                status=1,
            ).prefetch_related('categories')
        }
        related_signals = [
            {**channel, 'post': related_posts_by_slug[channel['slug']]}
            for channel in RELATED_INSIGHT_CHANNELS
            if channel['slug'] in related_posts_by_slug
        ]
        return render(
            request,
            'blog/insight_detail.html',
            {
                'post': post,
                'insight_intro': insight_intro,
                'insight_chapters': insight_chapters,
                'insight_payloads': insight_payloads,
                'related_signals': related_signals,
            },
        )

    like, created = Like.objects.get_or_create(post=post)
    post_was_liked = request.GET.get('liked') == 'true'
    context = {
        'post': post,
        'slug': post.slug,
        'like': like,
        'post_was_liked': post_was_liked,
    }

    return render(request, 'blog/blog_detail.html', context)


def like_post(request, pk, slug):
    # get the post by id 
    post = get_object_or_404(Post, pk=pk)
    # get the set of liked post from the session or create an empty set 
    liked_posts = list(request.session.get('liked_posts', set()))
    # check if the post has already been liked in the current session 
    if post.pk not in liked_posts:
        # if not liked, create a like instance and increment the like 
        liked, created = Like.objects.get_or_create(post=post) 
        liked.increment_likes()
        # add the post to the set of liked posts in the session 
        liked_posts.append(post.pk)
        request.session['liked_posts'] = liked_posts

    # return HttpResponseRedirect(reverse('blog_detail', args=[pk, slug]))
    return HttpResponseRedirect(reverse('blog_detail', args=[pk, slug]) + '?liked=true')

#TODO add some color to the blog detail error page and the blog post error page
