from api.new_api import Newser
import requests
import pytest
from utils import get_channel_data,init_logger
import allure

@allure.feature("新闻")
class Test_news():
    # 设置类夹具请求前，初始化一次api接口
    def setup_class(self):
        self.new_api = Newser()
        self.logger = init_logger("api")

    # 设置方法夹具请求前
    def setup(self):
        self.session = requests.Session()

    # 设置方法夹具请求后
    def teardown(self):
        # if self.session not None
        # 判断有没有session，如果有就关闭没有就忽视
        if self.session:
            self.session.close()

    # 标 记使用传参化，数据驱动
    @allure.story("频道")
    @pytest.mark.parametrize(['channel', 'num', 'start', 'appkey'], get_channel_data())
    def test_01_success(self, channel, num, start, appkey):
        r = self.new_api.get_news(self.session, channel, num, start, appkey)
        # 断言
        dainfo = "channel{},num{},start{},appkey{}".format(channel, num, start, appkey)
        self.logger.info(dainfo)
        assert r.status_code == 200
        assert r.json().get("code") == "10000"
        assert "查询成功" in r.json().get("msg")

    @allure.story("key错误")
    def test_02_key_error(self):
        r = self.new_api.get_news_channel(self.session, self.new_api.appkey)

        assert r.status_code == 200
        assert r.json().get("code") == "10000"
        assert "查询成功" in r.json().get("msg")

