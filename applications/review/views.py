from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.review.models import Review
from applications.review.permissions import IsReviewAuthor
from applications.review.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated, ]
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsReviewAuthor, ]
        return [permission() for permission in permissions]


    def get_serializer_context(self):
        return {'request': self.request}

