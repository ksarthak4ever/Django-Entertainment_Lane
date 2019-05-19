from django.db import models


class Collection(models.Model):
	title = models.CharField(max_length=255)

class Video(models.Model):
	title = models.CharField(max_length=255)
	url = models.URLField()
	youtube_id = models.CharField(max_length=255)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
