'''

'''
import re
import traceback
from lxml import etree

from urllib.parse import urljoin  # url拼接
from utensil import logger
# from utensil.tool import *  # 常用小工具



class AnalyzeHtml:
    def __init__(self, sid=0, aid=0):
        self.sid = sid
        self.aid = aid
        self.aftercare = ["reorganization", "exUrl"]   # 结尾处理

    def set_basic_information(self, sid, aid):  # 设置基础配置信息
        self.set_sid(sid)
        self.set_aid(aid)

    def set_sid(self, sid):  # 设置sid
        self.sid = sid

    def set_aid(self, aid):  # 设置gid
        self.aid = aid

    def parse_xpath_xml(self, html_content, xpath_dict):  # 利用xpath解析html页面
        '''
        :param html_content: 页面内容
        :param xpath_dict: xpath
        :return:
        '''
        html_content = bytes(bytearray(html_content, encoding='utf-8'))  # 预处理避免编码错误


        soup = etree.XML(html_content)
        status, result_dict = self.xpath_analyze(xpath_dict, soup)  # 进行xpath解析的主要函数
        pass
        # logger.debug("xpath解析完成(sid: {}, aid: {})".format(self.sid, self.aid))

        if status:  # 解析完成进行下一步
            if "reorganization" in xpath_dict:  # 存在需要重组的字段，则执行重组
                result_dict = self.xpath_aftercare_reorganization_main(xpath_dict, result_dict)
            if "exUrl" in xpath_dict:  # 存在扩链的字段
                result_dict = self.xpath_aftercare_exurl_main(xpath_dict, result_dict)

            # logger.debug(result_dict)
            return (status, result_dict)
        else:  # 解析失败，返回错误信息
            return (status, result_dict)

    def parse_xpath_html(self, html_content, xpath_dict):  # 利用xpath解析html页面
        '''
        :param html_content: 页面内容
        :param xpath_dict: xpath
        :return:
        '''
        html_content = bytes(bytearray(html_content, encoding='utf-8'))  # 预处理避免编码错误


        soup = etree.HTML(html_content)
        status, result_dict = self.xpath_analyze(xpath_dict, soup)  # 进行xpath解析的主要函数
        pass
        # logger.debug("xpath解析完成(sid: {}, aid: {})".format(self.sid, self.aid))

        if status:  # 解析完成进行下一步
            if "reorganization" in xpath_dict:  # 存在需要重组的字段，则执行重组
                result_dict = self.xpath_aftercare_reorganization_main(xpath_dict, result_dict)
            if "exUrl" in xpath_dict:  # 存在扩链的字段
                result_dict = self.xpath_aftercare_exurl_main(xpath_dict, result_dict)

            # logger.debug(result_dict)
            return (status, result_dict)
        else:  # 解析失败，返回错误信息
            return (status, result_dict)


    def xpath_aftercare_exurl_main(self, xpath_dict, result_dict):  # 处理扩链信息
        exUrl = xpath_dict["exUrl"]
        temp_url = []
        if isinstance(exUrl, dict):
            for key, value in exUrl.items():  # 遍历每一个需要进行扩展的字段
                if key in result_dict:
                    if isinstance(value, int):  # 如果扩链是数字，则初始化默认值
                        value = {
                            "aid": value,
                            "crawl_type": "html",
                            'info_url': {
                                'interval': 1,
                                'download_type': 'html',
                                'repeat_times': 1,
                            }
                        }
                    elif isinstance(value, dict):  # 无需初始化的扩链信息
                        pass
                    else:  # 扩链信息无效
                        pass
                        # logger.warning("扩链字段扩链信息格式不正确(sid: {},aid: {},key: {})".format(self.sid, self.aid, key))
                        continue

                    for url in result_dict[key]:  # 遍历每一个值，完善扩链信息
                        result = self.xpath_aftercare_exurl_one(url, value)
                        if result:
                            temp_url.append(result)
                else:
                    pass
                    # logger.warning("未发现可扩链的字段")
            result_dict["exUrl"] = temp_url
        else:
            pass
            # logger.warning("扩链字段格式不正确(sid: {},aid: {})".format(self.sid, self.aid))
        return result_dict

    def xpath_aftercare_exurl_one(self, url, value):  # 对单个扩链信息的处理
        # if is_url(url):
        #     value["info_url"]["url"] = url
        # else:
        #     value = False
        #     pass
            # logger.warning("url格式不正确(sid: {},aid: {},url: {})".format(self.sid, self.aid, url))
        return value

    def xpath_aftercare_reorganization_main(self, xpath_dict, result_dict):
        '''
        - 获取需要重组的字段名
        - 对每一个字段调用重组
        :param xpath_dict:
        :param result_dict:
        :return:
        '''
        reorganization = xpath_dict["reorganization"]
        result_dict["reorganization"] = []
        if isinstance(reorganization, list):  # 如果是列表，格式正确
            if isinstance(reorganization[0], str):  # 直接对数据进行合并
                result_dict = self.xpath_aftercare_reorganization_one(result_dict, reorganization)
            else:  # 如果第一个值为字符串，说明有多个需要合并的字段
                for value in reorganization:  # 对每一对都进行合并
                    result_dict = self.xpath_aftercare_reorganization_one(result_dict, value)
        else:
            pass
            # logger.warning("'reorganization'字段类型有误(sid: {}, aid: {})".format(self.sid, self.aid))
        return result_dict


    def xpath_aftercare_reorganization_one(self, result_dict, keyword):  # 根据关键字重组部分字段
        '''
        - 测试长度是否匹配
        - 重组数据
        - 数据格式转换
        :param result_dict:
        :param keyword:
        :return:
        '''
        try:
            all_len = result_dict[keyword[0]].__len__()
            temp_data = []
            for key in keyword:
                if result_dict[key].__len__() == all_len:
                    pass
                else:
                    pass
                    # logger.warning("重组时字段长度不匹配(sid: {}, aid: {}, keywords: {})".format(self.sid, self.aid, str(keyword)))
                    return result_dict

            for index in range(all_len):  # 遍历每一个位置
                temp_data_val = []
                for key in keyword:  # 重组结果
                    temp_data_val.append(result_dict[key][index])
                temp_data.append(temp_data_val)

            result_dict["reorganization"].append(self.tuple_to_dict(keyword, temp_data))
            return result_dict
        except:
            return result_dict


    def xpath_analyze(self, xpath_dict, soup):  # 根据xpath解析网页
        result_dict = {}
        try:
            for key, value in xpath_dict.items():  # 获取每一个需要解析的xpath
                if key in self.aftercare:  # 如果是系统关键字，则跳过
                    continue
                elif isinstance(value, str):  # 如果是字符串，直接执行xpath解析
                    result_dict[key] = soup.xpath(value)
                elif isinstance(value, dict):  # 如果是字典，则根据字典解析xpath
                    if "type" in value:
                        if value["type"] == "intercept":  # 截取部分数据
                            result_dict[key] = []
                            for __, data in enumerate(soup.xpath(value["xpath"])):  # 对每一个数据都进行阶段
                                if value["intercept"].__len__() == 1:  # 只有一个截取参数
                                    result_dict[key].append(data[value["intercept"][0]:])
                                elif value["intercept"].__len__() == 2:  # 存在两个截取参数
                                    result_dict[key].append(data[value["intercept"][0]: value["intercept"][1]])
                                else:
                                    pass
                                    # logger.error("xpath截取参数有误 (sid: {}, aid: {}, key: {})".format(self.sid, self.aid, key))
                        elif value["type"] == "splice":  # url拼接
                            result_dict[key] = []
                            for __, data in enumerate(soup.xpath(value["xpath"])):  # 对每一个数据都进行阶段
                                result_dict[key].append(urljoin(value["splice"], data))
                        else:
                            pass
                            # logger.warning("未支持该类型(sid: {}, aid: {}, key: {}, type: {})".format(self.sid, self.aid, key, value["type"]))
                    else:
                        pass
                        # logger.warning("未找到类型参数(sid: {}, aid: {}, key: {})".format(self.sid, self.aid, key))
                        continue
            return (True, result_dict)
        except:
            return (False, traceback.format_exc())

    def tuple_to_dict(self, fields, data):  # 将得到的数据格式化
        result = []
        for data_one in data:
            result.append(dict(zip(fields, data_one)))
        return tuple(result)
