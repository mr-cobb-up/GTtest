from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
import logging
import random

logging.basicConfig(
    filename='touch_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class TouchTest:
    def __init__(self):
        # Appium 설정
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.automation_name = 'UiAutomator2'
        options.device_name = '디바이스이름'
        options.app_package = 'com.kakaogames.gdtskr'
        options.app_activity = 'com.kakaogame.KGUnityPlayerActivity'
        options.no_reset = True

        # Appium 서버 연결
        self.driver = webdriver.Remote('http://localhost:4723', options=options)

        # 터치할 좌표들 정의
        self.touch_positions = [
            {"name": "위", "x": 366, "y": 663},
            {"name": "왼쪽", "x": 226, "y": 803},
            {"name": "아래", "x": 361, "y": 937},
            {"name": "오른쪽", "x": 512, "y": 797},
            {"name": "좌상향", "x": 248, "y": 668},
            {"name": "좌하향", "x": 248, "y": 921},
            {"name": "우하향", "x": 469, "y": 910},
            {"name": "우상향", "x": 485, "y": 673},
            {"name": "공격", "x": 1864, "y": 883},
            {"name": "스킬", "x": 1945, "y": 684},
            {"name": "달리기", "x": 2155, "y": 867}
        ]

    def touch_and_hold(self, position, duration=3):
        try:
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(
                self.driver,
                mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )

            actions.w3c_actions.pointer_action.move_to_location(
                position["x"], position["y"]
            )
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            logging.info(f"{position['name']} 터치 유지 중: ({position['x']}, {position['y']}) - {duration}초")

        except Exception as e:
            logging.error(f"터치 실패: {str(e)}")

    def run_random_touch_test(self):
        try:
            logging.info("랜덤 터치 테스트 시작")

            while True:  # 무한 반복
                try:
                    # 랜덤하게 위치 선택
                    selected_position = random.choice(self.touch_positions)

                    # 선택된 위치 터치 및 유지 (3초)
                    self.touch_and_hold(selected_position, 3)

                    # 1초 대기
                    time.sleep(1)

                    logging.info(f"다음 테스트 준비...")

                except KeyboardInterrupt:
                    logging.info("이용자가 테스트를 중단했습니다.")
                    break
                except Exception as e:
                    logging.error(f"반복 중 오류 발생: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"테스트 중 오류 발생: {str(e)}")
        finally:
            self.driver.quit()


# 테스트 실행
if __name__ == "__main__":
    test = TouchTest()
    try:
        test.run_random_touch_test()
    except KeyboardInterrupt:
        print("\n테스트가 중단되었습니다.")
