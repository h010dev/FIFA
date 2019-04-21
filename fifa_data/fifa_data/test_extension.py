import datetime
import json
import os
from scrapy.extensions.corestats import CoreStats


class CustomStats(CoreStats):

    def __init__(self, stats, file=None, data=None):
        super().__init__(stats)
        self.file = file
        self.data = data

    def spider_opened(self, spider):

        # User spider name to set file name:
        # log_dir = 'C:\\Users\\E46Racing\\Documents\\PycharmProjects\\FIFA\\fifa_data\\logs'
        file_name = str(spider.name + '_log' + '.json')
        # os.path.join(log_dir, file_name)
        self.file = file_name

        # Check to see if file exists:
        exists = os.path.isfile(file_name)

        if exists:

            with open(self.file) as json_file:
                self.data = json.load(json_file)

            status = self.data['finish_reason']

            # Check to see if last spider run was completed successfully:
            if status not in ['finished']:
                for stat in self.data.keys():
                    try:
                        self.stats.set_value(stat, self.data[stat], spider=spider)
                    except KeyError:
                        pass

            else:
                # Reset stats if last run was completed without errors/shutdown:
                self.stats.clear_stats()
        else:
            pass

        self.stats.set_value('start_time', datetime.datetime.now(), spider=spider)
        self.stats.set_value('spider_name', spider.name)

    def spider_closed(self, spider, reason):
        finish_time = datetime.datetime.now()
        elapsed_time = finish_time - self.stats.get_value('start_time')

        # Add previous run's elapsed time to current run:
        try:
            elapsed_time_seconds = elapsed_time.total_seconds() + self.stats.get_value('elapsed_time_seconds')
        except TypeError:
            elapsed_time_seconds = elapsed_time.total_seconds()

        self.stats.set_value('elapsed_time_seconds', elapsed_time_seconds, spider=spider)
        self.stats.set_value('finish_time', finish_time, spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)
        with open(self.file, 'w') as outfile:
            json.dump(self.stats.get_stats(), outfile, default=str)
