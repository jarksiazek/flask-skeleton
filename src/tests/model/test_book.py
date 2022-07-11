import json
import time
from datetime import datetime
from datetime import timedelta
from typing import Dict
from unittest import TestCase
from unittest.mock import patch

from src.web.const import create_app
from src.web.const import db
from src.web.model.channel import Book

CHANNEL_NAME = "slack_channel_name"
CHANNEL_ID = "slack_channel_id"
REQUESTOR = "requestor_id"
BLOCKS: Dict[str, str] = dict()
REQUEST_TYPE_LIST = ["cloud-help"]
EVENT_TS = "1212121.12121"
REQUEST_LINK = "REQUEST_LINK"


class TestIntegrationChannel(TestCase):
    def setUp(
        self,
    ):
        app = create_app("src.tests.config.Config")
        db.init_app(app.flask_app)
        app.flask_app.app_context().push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_update_or_register_new_record_results_add_new_given_new_record(self):
        # given - table channel is empty
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        # when adding new record
        Channel().update_or_register_new_record(
            CHANNEL_NAME, CHANNEL_ID, REQUESTOR, BLOCKS, REQUEST_TYPE_LIST, EVENT_TS, REQUEST_LINK
        )

        # then - new records has been added
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(CHANNEL_NAME, channels[0].slack_channel_name)
        self.assertEqual(CHANNEL_ID, channels[0].slack_channel_id)
        self.assertEqual(REQUESTOR, channels[0].requestor_id)
        self.assertEqual(json.dumps(BLOCKS), channels[0].blocks)
        self.assertEqual(json.dumps({"message": REQUEST_TYPE_LIST, "reaction": []}), channels[0].request_type_list)

    def test_update_or_register_new_record_results_update_record_given_record_exists(self):
        # given - table has one record
        self._add_testing_record()
        # when the existing record has been modified
        request_type_list = ["cloud-incident", "cloud-bug"]
        Channel().update_or_register_new_record(
            CHANNEL_NAME, CHANNEL_ID, REQUESTOR, BLOCKS, request_type_list, EVENT_TS, REQUEST_LINK
        )

        # then - record has been updated
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(request_type_list, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual([], json.loads(channels[0].request_type_list).get("reaction"))

    def test_close_request_results_closed_request_given_main_record_exists(self):
        # given - table has one record
        self._add_testing_record()

        reaction_ts = time.time()

        # when record has been closed
        Channel().close_request(CHANNEL_ID, EVENT_TS, reaction_ts, COMPLETION_REACTIONS_TUPLE[0])

        # then - record has been changed to close status
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(REQUEST_TYPE_LIST, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual(list(COMPLETION_REACTIONS_TUPLE), json.loads(channels[0].request_type_list).get("reaction"))

    def test_save_labels_results_label_is_added_given_record_has_no_labels(self):
        # given - table has one record
        self._add_testing_record()

        # when record has been updated with new label
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_id", ["Tool1", "Tool2"])

        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(["Tool1", "Tool2"], json.loads(channels[0].labels)["new_question_id"])

    def test_save_labels_results_label_is_updated_given_record_has_label(self):
        # given - table has one record
        self._add_testing_record()
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_1", ["Tool1", "Tool2"])
        channels = db.session.query(Channel).all()
        self.assertEqual(["Tool1", "Tool2"], json.loads(channels[0].labels)["new_question_1"])

        # when record has been updated with new label
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_1", ["Tool3", "Tool4"])

        updated_channels = db.session.query(Channel).all()
        self.assertEqual(1, len(updated_channels))
        self.assertEqual(["Tool3", "Tool4"], json.loads(updated_channels[0].labels)["new_question_1"])

    def test_save_labels_results_label_is_added_given_record_has_label(self):
        # given - table has one record
        self._add_testing_record()
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_1", ["Tool1", "Tool2"])
        channels = db.session.query(Channel).all()
        self.assertEqual(["Tool1", "Tool2"], json.loads(channels[0].labels)["new_question_1"])

        # when record has been updated with new label and new id
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_2", ["Tool3", "Tool4"])

        updated_channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(["Tool1", "Tool2"], json.loads(updated_channels[0].labels)["new_question_1"])
        self.assertEqual(["Tool3", "Tool4"], json.loads(updated_channels[0].labels)["new_question_2"])

    def test_remove_all_labels_results_label_is_removed(self):
        # given - table has one record
        self._add_testing_record()
        Channel().save_labels(CHANNEL_ID, EVENT_TS, "new_question_1", ["Tool1", "Tool2"])
        channels = db.session.query(Channel).all()
        self.assertEqual(["Tool1", "Tool2"], json.loads(channels[0].labels)["new_question_1"])

        # when record has been updated with new label and new id
        Channel().remove_all_labels(CHANNEL_ID, EVENT_TS)

        updated_channels = db.session.query(Channel).all()
        self.assertEqual(1, len(updated_channels))
        self.assertIsNone(updated_channels[0].labels)

    def test_reopen_request_results_reopened_request_given_main_record_exists(self):
        # given - table has one record
        self._add_testing_record()

        reaction_ts = time.time()

        # when record has been closed
        Channel().close_request(CHANNEL_ID, EVENT_TS, reaction_ts, COMPLETION_REACTIONS_TUPLE[0])

        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(REQUEST_TYPE_LIST, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual(list(COMPLETION_REACTIONS_TUPLE), json.loads(channels[0].request_type_list).get("reaction"))

        # and reopen
        Channel().reopen_request(CHANNEL_ID, EVENT_TS, COMPLETION_REACTIONS_TUPLE[0])

        # then - record has been changed to open status
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(REQUEST_TYPE_LIST, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual([], json.loads(channels[0].request_type_list).get("reaction"))

    def test_add_reaction_to_request_results_record_has_new_emoji_given_main_record_exists(self):
        # given - table has one record
        self._add_testing_record()

        reaction = list(CLOUD_EMOJI_ALIAS_LIST)[3]
        # when record has been modified
        Channel().add_reaction_to_request(CHANNEL_ID, EVENT_TS, reaction)

        # then - record has new reaction
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(REQUEST_TYPE_LIST, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual([reaction], json.loads(channels[0].request_type_list).get("reaction"))

    def test_remove_reaction_from_request_results_record_has_new_emoji_given_main_record_exists(self):
        # given - table has one record
        reaction = list(CLOUD_EMOJI_ALIAS_LIST)[3]
        self._add_testing_record_with_reaction_type_list([reaction])

        # when record has been modified
        Channel().remove_reaction_from_request(CHANNEL_ID, EVENT_TS, reaction)

        # then - the reaction was removed from the record
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))
        self.assertEqual(REQUEST_TYPE_LIST, json.loads(channels[0].request_type_list).get("message"))
        self.assertEqual([], json.loads(channels[0].request_type_list).get("reaction"))

    def test_get_last_working_day_records_sorted_by_date_returns_records(self):
        utc_now = datetime.strptime("2022-04-22 12:00:21", slack_datetime_fmt)
        self._add_channel_records_with_dates(
            [
                "2022-04-21 21:34:58",
                "2022-04-21 8:00:21",
                "2022-04-22 21:34:58",
                "2022-04-20 21:34:58",
            ]
        )
        results = Channel().get_last_working_day_records_sorted_by_date(CHANNEL_ID, utc_now)
        dates = [datetime.fromtimestamp(x.event_ts).strftime(slack_datetime_fmt) for x in results]
        self.assertEqual(2, len(results))
        self.assertTrue(set(dates), {"2022-04-21 21:34:58", "2022-04-21 8:00:21"})

    def test_get_list_of_request_by_return_list_given_only_today_events_should_be_added_to_list(self):
        today_timestamp = datetime.today().timestamp()
        yesterday_timestamp = (datetime.today() - timedelta(days=1)).timestamp()
        threads = [
            ChannelThread(id=1, author_id="author", thread_ts=11.11, event_ts=11.11),
            ChannelThread(id=2, author_id="author", thread_ts=11.11, event_ts=11.11),
        ]
        channel1 = Channel(
            request_status=RequestStatusEnum.NEW_RECORD.value, event_ts=today_timestamp, thread_message=threads
        )
        channel2 = Channel(request_status=RequestStatusEnum.WORKING.value, event_ts=today_timestamp)
        channel3 = Channel(request_status=RequestStatusEnum.COMPLETED.value, event_ts=yesterday_timestamp)

        self._add_testing_records([channel1, channel2, channel3])

        with patch.object(ControlPanel, "get_channel_id_by_channel_name", return_value=CHANNEL_ID):
            result = Channel().get_list_of_request_by(
                CHANNEL_NAME, datetime.today(), datetime.today(), ["initial", "working", "completed"]
            )
        self.assertEqual(2, len(result))

    def test_get_dict_request_id_and_thread_counts(self):
        today_timestamp = datetime.today().timestamp()
        yesterday_timestamp = (datetime.today() - timedelta(days=1)).timestamp()
        threads_channel_1 = [
            ChannelThread(id=1, author_id="author", thread_ts=11.11, event_ts=11.11),
            ChannelThread(id=2, author_id="author", thread_ts=11.11, event_ts=11.11),
        ]
        threads_channel_2 = [ChannelThread(id=3, author_id="author", thread_ts=11.11, event_ts=11.11)]
        channel1 = Channel(
            request_status=RequestStatusEnum.NEW_RECORD.value,
            event_ts=today_timestamp,
            thread_message=threads_channel_1,
        )
        channel2 = Channel(
            request_status=RequestStatusEnum.NEW_RECORD.value,
            event_ts=yesterday_timestamp,
            thread_message=threads_channel_2,
        )
        self._add_testing_records([channel1, channel2])

        result = ChannelThread().get_dict_request_id_and_thread_counts(
            CHANNEL_ID, datetime.today() - timedelta(days=1), datetime.today()
        )
        self.assertEqual(2, len(result.items()))
        self.assertEqual(2, result[1])
        self.assertEqual(1, result[2])

    def _add_testing_record(self):
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        existing_channel = Channel(
            slack_channel_name=CHANNEL_NAME,
            slack_channel_id=CHANNEL_ID,
            requestor_id=REQUESTOR,
            request_status=RequestStatusEnum.NEW_RECORD.value,
            event_ts=EVENT_TS,
            request_type_list=json.dumps({"message": REQUEST_TYPE_LIST, "reaction": []}),
        )
        db.session.add(existing_channel)
        db.session.commit()
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))

    def _add_testing_records(self, channels_to_add: list[Channel]):
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        for channel in channels_to_add:
            channel.slack_channel_name = f"#{CHANNEL_NAME}"
            channel.slack_channel_id = CHANNEL_ID
            channel.requestor_id = REQUESTOR
            db.session.add(channel)
            db.session.commit()

        channels = db.session.query(Channel).all()
        self.assertEqual(len(channels_to_add), len(channels))

    def _add_testing_record_with_reaction_type_list(self, reaction_list):
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        existing_channel = Channel(
            slack_channel_name=CHANNEL_NAME,
            slack_channel_id=CHANNEL_ID,
            requestor_id=REQUESTOR,
            request_status=RequestStatusEnum.NEW_RECORD.value,
            event_ts=EVENT_TS,
            request_type_list=json.dumps({"message": REQUEST_TYPE_LIST, "reaction": reaction_list}),
        )
        db.session.add(existing_channel)
        db.session.commit()
        channels = db.session.query(Channel).all()
        self.assertEqual(1, len(channels))

    def _add_channel_records_with_dates(self, date_list):
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        for date in date_list:
            channel = Channel(
                slack_channel_name=CHANNEL_NAME,
                slack_channel_id=CHANNEL_ID,
                requestor_id=REQUESTOR,
                request_status=RequestStatusEnum.NEW_RECORD.value,
                event_ts=datetime.strptime(date, slack_datetime_fmt).timestamp(),
                request_type_list=json.dumps({"message": REQUEST_TYPE_LIST, "reaction": []}),
            )
            db.session.add(channel)
            db.session.commit()
        channels = db.session.query(Channel).all()
        self.assertEqual(len(date_list), len(channels))

    def _add_channel_records_with_dates_and_completion_status(self, data_list):
        channels = db.session.query(Channel).all()
        self.assertEqual(0, len(channels))

        for data in data_list:
            channel = Channel(
                slack_channel_name=CHANNEL_NAME,
                slack_channel_id=CHANNEL_ID,
                requestor_id=REQUESTOR,
                request_status=data[1].value,
                event_ts=datetime.strptime(data[0], slack_datetime_fmt).timestamp(),
                request_type_list=json.dumps({"message": REQUEST_TYPE_LIST, "reaction": []}),
            )
            db.session.add(channel)
            db.session.commit()
        channels = db.session.query(Channel).all()
        self.assertEqual(len(data_list), len(channels))
