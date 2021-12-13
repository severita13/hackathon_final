from rest_framework import serializers
from .models import Post, Like, Saved
from applications.review.serializers import ReviewSerializer


class SavedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Saved
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'content',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.review.all()]
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
                print(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.review.all()]
        representation['like'] = instance.like.filter(like=True).count()
        if len(total_rating) > 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        representation['review'] = ReviewSerializer(instance.review.filter(post=instance.id), many=True).data
        return representation