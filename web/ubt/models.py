# -*- coding: utf-8 -*-

from django.db import models


class HourBehaviour(models.Model):

    """
        Basic Model class to record hourly visit data of the system.

        hour: format 'YYYY-MM-DD-HH' to remake the specific hour.


    """

    hour = models.CharField(max_length=15)

    page_view = models.IntegerField()
    user_view = models.IntegerField()
    login_cnt = models.IntegerField()
    search_cnt = models.IntegerField()
    download_cnt = models.IntegerField()
    register_cnt = models.IntegerField()
    upload_cnt = models.IntegerField()
    crawl_cnt = models.IntegerField()

    record_date = models.DateField()
    last_update_time = models.DateTimeField()

    def __unicode__(self):
        return self.hour

    class Meta:
        db_table = "user_behaviour_hourly_static"
        ordering = [-"last_update_time"]
        get_latest_by = "last_update_time"
