# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   util.py
 
@Time    :   2020/8/23 10:13 下午
 
@Desc    :   kbqa工具类
 
"""

from typing import Text, Callable, Dict, List, Any, Optional
import typing

from model.Events import SlotSet
from model.Executor import Tracker

SLOT_MENTION = "mention"
SLOT_OBJECT_TYPE = "object_type"
SLOT_ATTRIBUTE = "attribute"
SLOT_LISTED_OBJECTS = "knowledge_base_listed_objects"
SLOT_LAST_OBJECT = "knowledge_base_last_object"
SLOT_LAST_OBJECT_TYPE = "knowledge_base_last_object_type"


def get_object_name(
        tracker: "Tracker",
        ordinal_mention_mapping: Dict[Text, Callable],
        use_last_object_mention: bool = True
) -> Optional[Text]:
    """

    :param tracker:
    :param ordinal_mention_mapping:
    :param use_last_object_mention:
    :return:
    """

    return None


def resolve_mention(
        tracker: "Tracker",
        ordinal_mention_mapping: Dict[Text, Callable]
) -> Optional[Text]:
    """

    :param tracker:
    :param ordinal_mention_mapping:
    :return:
    """
    return None


def get_attribute_slots(
        tracker: "Tracker",
        object_attributes: List[Text]
) -> List[Dict[Text, Text]]:
    """
    获取slot的属性
    :param tracker:
    :param object_attributes:
    :return: a list of attributes
    """
    attributes = []

    return attributes


def reset_attributes_slots(
        tacker: "Tracker",
        object_attributes: List[Text]
) -> List[Dict]:
    """
    重置Slots
    :param tacker:
    :param object_attributes:
    :return:  a list of Slots
    """
    slots = []

    return slots
