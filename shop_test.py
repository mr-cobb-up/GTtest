from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import logging

logging.basicConfig(
    filename='shop_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ShopAutoTest:
    def __init__(self):
        # Appium 2.0 설정 방식
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.automation_name = 'UiAutomator2'
        options.device_name = '디바이스이름'
        options.app_package = 'com.kakaogames.gdtskr'
        options.app_activity = 'com.kakaogame.KGUnityPlayerActivity'
        options.no_reset = True
        options.full_reset = False
        options.dont_stop_app_on_reset = True

        # Appium 서버 연결
        self.driver = webdriver.Remote('http://localhost:4723', options=options)

        # 상품 좌표
        self.item_positions = [
            {"x": 864, "y": 658},  # 상품 1
            {"x": 1400, "y": 658},  # 상품 2
            {"x": 1900, "y": 658}  # 상품 3
        ]

        # 버튼 좌표
        self.buttons = {
            "purchase": {"x": 1800, "y": 925},  # 구매 버튼
            "cancel": {"x": 500, "y": 400},  # 취소 버튼
            "confirm": {"x": 1220, "y": 864},  # 확인 버튼
            "back": {"x": 2207, "y": 55}  # 뒤로가기
        }

    def tap_coordinates(self, x, y):
        try:
            self.driver.tap([(x, y)])
            logging.info(f"탭 실행: ({x}, {y})")
            time.sleep(1)
        except Exception as e:
            logging.error(f"탭 실행 실패: ({x}, {y}) - {str(e)}")

    def scroll_down(self):
        try:
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] * 0.5
            start_y = screen_size['height'] * 0.8
            end_y = screen_size['height'] * 0.15

            self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
            logging.info("스크롤 다운 실행")
            time.sleep(1)
        except Exception as e:
            logging.error(f"스크롤 실패: {str(e)}")

    def test_single_item(self, item_position):
        try:
            # 상품 클릭
            self.tap_coordinates(item_position["x"], item_position["y"])
            time.sleep(1)

            # 구매 버튼 클릭
            self.tap_coordinates(self.buttons["purchase"]["x"],
                                 self.buttons["purchase"]["y"])
            time.sleep(1)

            # 취소 버튼 클릭
            self.tap_coordinates(self.buttons["cancel"]["x"],
                                 self.buttons["cancel"]["y"])
            time.sleep(1)

            # 확인 버튼 클릭
            self.tap_coordinates(self.buttons["confirm"]["x"],
                                 self.buttons["confirm"]["y"])
            time.sleep(1)

            # 뒤로가기 버튼 클릭
            self.tap_coordinates(self.buttons["back"]["x"],
                                 self.buttons["back"]["y"])
            time.sleep(1)

            logging.info(f"상품 테스트 완료: ({item_position['x']}, {item_position['y']})")

        except Exception as e:
            logging.error(f"상품 테스트 실패: {str(e)}")

    def run_shop_test(self):
        try:
            logging.info("상점 테스트 시작")

            items_tested = 0
            total_items = 19  # 총 테스트할 상품 수

            while items_tested < total_items:
                # 현재 화면의 3개 상품 테스트
                for position in self.item_positions:
                    if items_tested >= total_items:
                        break
                    self.test_single_item(position)
                    items_tested += 1
                    logging.info(f"테스트 진행률: {items_tested}/{total_items}")

                # 다음 3개 상품을 위해 스크롤
                if items_tested < total_items:
                    self.scroll_down()
                    time.sleep(2)

            logging.info("모든 상품 테스트 완료")

        except Exception as e:
            logging.error(f"테스트 중 오류 발생: {str(e)}")
        finally:
            self.driver.quit()


# 테스트 실행
if __name__ == "__main__":
    test = ShopAutoTest()
    test.run_shop_test()
