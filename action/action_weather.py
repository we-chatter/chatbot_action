# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   action_weather.py
 
@Time    :   2020/8/23 8:27 下午
 
@Desc    :
 
"""
import pathlib
import os
import logging

from typing import Any, Text, Dict, List, Union

from model import Action
from model.Events import SlotSet, AllSlotsReset
from model.Executor import CollectingDispatcher
from model.Interfaces import Tracker

from service.weather.seniverse import SeniverseWeatherAPI
from utils.time_utils import get_time_unit

api_secret = "Sq6NfAburbGs9MGQb"
sw = SeniverseWeatherAPI(api_secret)


class ActionReportWeather(Action):
    """
    天气查询
    """

    def name(self) -> Text:
        return "action_report_weather"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""
        return ["address", "date-time"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date-time')

        if date_time is None:
            date_time = '今天'
        date_time_number = get_time_unit(date_time)  # 传入时间关键词，返回归一化的时间

        if isinstance(date_time_number, str):  # parse date_time failed
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time_number]))]
        elif date_time_number is None:
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time]))]
        else:
            condition = sw.get_weather_by_city_and_day(address, date_time_number)  # 调用天气API
            weather_data = forecast_to_text(address, condition)

        return [SlotSet("matches", "{}".format(weather_data))]


def forecast_to_text(address, condition):
    msg_tpl = "{city} {date} 的天气情况为：{condition}；气温：{temp_low}-{temp_high} 度"
    msg = msg_tpl.format(
        city= address,
        date=condition.date,
        condition=condition.condition,
        temp_low=condition.low_temperature,
        temp_high=condition.high_temperature
    )
    return msg
