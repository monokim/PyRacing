import pygame
import Objects.Object as Ob
import random
import subprocess

class Scene:
    def __init__(self, display, music):
        self.stage = -1
        self.wait = False
        self.clear = False
        self.battle = False
        self.energy_boss = 1.0
        self.energy_me = 1.0
        self.select_x = 1
        self.select_y = 1
        self.action = False
        self.animation = False
        self.done = False
        self.music = music


        #chapter 1
        self.actions = [0, 0, 0, 0]
        self.battle_count = 0
        self.from_x = 300
        self.from_y = 300
        self.end_x = 900
        self.end_y = 150
        self.current_x = 0
        self.current_y = 0
        self.music.load_music("Resources/keyboard.mp3")
        self.schwein = Ob.object(display.load_image("Resources/schwein.png"), self.music.load_sound("Resources/schwein.wav"))
        self.bear = Ob.object(display.load_image("Resources/bear.png"), self.music.load_sound("Resources/bear.wav"))
        self.cyborg = Ob.object(display.load_image("Resources/cyborg.png"), self.music.load_sound("Resources/cyborg.wav"))
        self.resign = Ob.object(display.load_image("Resources/resign.png"), self.music.load_sound("Resources/resign.wav"))
        self.effect = Ob.object(display.load_image("Resources/effect.png"))
        self.excel = Ob.object(display.load_image("Resources/excel.png"), self.music.load_sound("Resources/resign.wav"))

        #chapter 2
        self.lernen = False
        self.answer = ""
        self.count = 0
        self.correct = 0
        self.correct_answer = ""
        self.problem = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.answers = ["weil", "deshalb", "e", "en", "seit", "dem", "ehe", "der hund", "das bier", "blauer", "bist", "hast", "gespielt", "desto", " geht"]

        #chapter 3
        self.drive = False


    def scene_start(self, display, input):
        if self.clear == True:
            self.stage = self.stage + 1
            self.clear = False
            display.clear()

        if self.stage == -1:
            if self.wait == False:
                display.set_text("Journey of Jannie", 130, 200, font_size = 130)
                display.set_text("Press SPACE", 500, 400, font_size = 50)
                self.wait = True
            elif self.wait == True:
                # wait for keyboard input
                if input == pygame.K_SPACE:
                    self.clear = True
                    self.wait = False
                    self.music.play_music()
        elif self.stage == 0:
            # Journey of Jannie Intro
            if self.wait == False:
                display.set_text("Jannie는 새로운 삶을 살고 싶어한다.", 100, 130, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                display.set_text("30살이 된 기념으로 여행을 준비한다.", 100, 230, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                display.set_text("새로운 삶을 향한 모험을 시작 하려는순간", 100, 330, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                display.set_text("삼성 부장의 방해가 시작되는데...", 100, 430, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                display.set_text("Press SPACE", 500, 530, font_size = 50)
                self.wait = True
            elif self.wait == True:
                if input == pygame.K_SPACE:
                    self.clear = True
                    self.wait = False
                    self.music.load_music("Resources/battle.mp3")
                    self.music.play_music()

        ######################################################################################
        # stage 1 battle
        elif self.stage == 1:
            if self.energy_boss <= 0:
                #마지막 대사와 애니메이션
                self.music.stop_music()
                if self.wait == False:
                    self.stage_1_ending(display)
                    self.wait = True
                elif self.wait == True:
                    #다음 스테이지로
                    if input == pygame.K_SPACE:
                        self.clear = True
                        self.wait = False
            else:
                if self.battle_count == 2:
                    result = self.stage_1_action_animation(display, 5)
                    if result == 1:
                        self.energy_me = self.energy_me - 0.8
                        self.battle_count = 99

                if self.wait == False and self.battle == False:
                    # meet the boss
                    self.stage_1_intro(display)
                    self.wait = True
                elif self.wait == True and self.battle == False:
                    if input == pygame.K_SPACE:
                        self.battle = True
                        self.wait = False
                elif self.wait == False and self.battle == True and self.action == False:
                    # battle GUI setting
                    self.stage_1_set_battle_UI(display)
                    #select action
                    if input == pygame.K_LEFT or input == pygame.K_RIGHT:
                        self.select_x = -self.select_x
                    if input == pygame.K_SPACE:
                        if self.select_x == 1:
                            self.action = True
                        elif self.select_x == -1:
                            display.draw_dialog_area()
                            display.set_text("퇴근시간이 되지 않아", 150, 530, lang="kor", mode='each')
                            display.set_text("도망치지 못했다.", 150, 600, lang="kor", mode='each')
                            pygame.time.Clock().tick(1)
                        self.select_x = 1
                elif self.wait == False and self.battle == True and self.action == True:
                    #select actions
                    self.stage_1_select_actions(display)
                    if input == pygame.K_LEFT or input == pygame.K_RIGHT:
                        self.select_x = -self.select_x
                    elif input == pygame.K_UP or input == pygame.K_DOWN:
                            self.select_y = -self.select_y
                    elif input == pygame.K_SPACE:
                        self.wait = True
                elif self.wait == True and self.battle == True and self.action == True:
                    # battle animation and back to select actions
                    if self.select_x == 1 and self.select_y == 1:
                        #독일어 욕
                        if self.actions[0] == 0:
                            #actions animation
                            result = self.stage_1_action_animation(display, 1)
                            if result == 1:
                                self.battle_count = self.battle_count + 1
                                self.energy_boss = self.energy_boss - 0.1
                                self.actions[0] = 1
                                self.wait = False
                                self.action = False
                        else:
                            #이미 사용했다
                            self.stage_1_already_used(display)
                            self.wait = False
                    elif self.select_x == -1 and self.select_y == 1:
                        #검은곰어택
                        if self.actions[1] == 0:
                            #actions animation
                            result = self.stage_1_action_animation(display, 2)
                            if result == 1:
                                self.battle_count = self.battle_count + 1
                                self.energy_boss = self.energy_boss - 0.2
                                self.actions[1] = 1
                                self.wait = False
                                self.action = False
                        else:
                            #이미 사용했다
                            self.stage_1_already_used(display)
                            self.wait = False
                        pass
                    elif self.select_x == 1 and self.select_y == -1:
                        #사이보그 펀치
                        if self.actions[2] == 0:
                            #actions animation
                            result = self.stage_1_action_animation(display, 3)
                            if result == 1:
                                self.battle_count = self.battle_count + 1
                                self.energy_boss = self.energy_boss - 0.3
                                self.actions[2] = 1
                                self.wait = False
                                self.action = False
                        else:
                            #이미 사용했다
                            self.stage_1_already_used(display)
                            self.wait = False
                    elif self.select_x == -1 and self.select_y == -1:
                        #사직서 제출
                        if self.actions[3] == 0:
                            #actions animation
                            result = self.stage_1_action_animation(display, 4)
                            if result == 1:
                                self.battle_count = self.battle_count + 1
                                self.energy_boss = self.energy_boss - 0.4
                                self.actions[3] = 1
                                self.wait = False
                                self.action = False
                        else:
                            #이미 사용했다
                            self.stage_1_already_used(display)
                            self.wait = False

#############################################################################################
        # stage 2 Deutsch lernen
        elif self.stage == 2:
            if self.count == 10:
                if self.wait == False:
                    self.stage_2_result(display)
                    if self.correct >= 7:
                        #pass
                        self.stage_2_pass(display)
                        self.stage_2_ending(display)
                        self.wait = True
                    else:
                        self.stage_2_fail(display)
                        self.wait = False
                        self.lernen = False
                        self.correct = 0
                        self.count = 0
                elif self.wait == True:
                    if input == pygame.K_SPACE:
                        self.clear = True
                        self.wait = False
            else:
                #print("out count ", self.count)
                if self.wait == False and self.lernen == False:
                    self.stage_2_intro(display)
                    self.wait = True
                elif self.wait == True and self.lernen == False:
                    if input == pygame.K_SPACE:
                        self.lernen = True
                        self.wait = False
                        self.stage_2_set_UI(display)
                elif self.wait == False and self.lernen == True:
                    result = self.stage_2_set_problem(display)
                    if result == 1:
                        self.wait = True
                        self.answer = ""
                elif self.wait == True and self.lernen == True:
                    if input == 13:
                        # 정답 비교
                        #print("c : ", self.correct_answer, " / s : ", self.answer)
                        if self.correct_answer == self.answer:
                            self.correct = self.correct + 1
                        self.wait = False
                        self.count = self.count + 1
                    elif (input >= pygame.K_a and input <= pygame.K_z) or input == pygame.K_SPACE:
                        self.answer = self.answer + chr(input)
                    elif input == pygame.K_BACKSPACE:
                        self.answer = self.answer[:-1]
                    # clear text area
                    display.clear_area(200, 500)
                    display.set_text(self.answer, 400, 500, font_size = 100)

############################################################################################
        # stage 3 Driving
        elif self.stage == 3:
            if self.wait == False and self.drive == False:
                self.stage_3_intro(display)
                self.wait = True
            elif self.wait == True and self.drive == False:
                if input == pygame.K_SPACE:
                    self.drive = True
                    self.wait = False
                    self.stage_3_set_UI(display)
                    subprocess.call(['C:\\Users\\mingo\\Desktop\\Mono\\Workspace\\Driving Test\\Driving.exe'])




###################################################################

    def stage_1_intro(self, display):
        display.clear()
        display.draw_dialog_area()
        display.set_image("Resources/boss.png", 1100, 50)
        display.set_text("너는 삼성에서 영원히 나갈 수 없다!", 150, 530, lang="kor", mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("나의 공격을 받아랏! ", 150, 615, lang="kor", mode='each')

    def stage_1_set_battle_UI(self, display):
        display.clear()
        display.draw_dialog_area()
        display.set_image("Resources/boss.png", 1100, 50)
        display.set_text("Boss", 550, 20, font_size=50)
        display.draw_energy_bar(550, 100, self.energy_boss)

        display.set_text("Jannie", 100, 370, font_size=50)
        display.draw_energy_bar(100, 450, self.energy_me)

        display.draw_battle_area()
        display.set_text("싸운다", 700, 570, lang='kor', font_size=50)
        display.set_text("도망친다", 950, 570, lang='kor', font_size=50)
        if self.select_x == 1:
            display.draw_select_triangle(680, 595)
        elif self.select_x == -1:
            display.draw_select_triangle(930, 595)

    def stage_1_select_actions(self, display):
        display.clear()
        display.draw_dialog_area()
        display.set_image("Resources/boss.png", 1100, 50)
        display.set_text("Boss", 550, 20, font_size=50)
        display.draw_energy_bar(550, 100, self.energy_boss)
        display.set_text("Jannie", 100, 370, font_size=50)
        display.draw_energy_bar(100, 450, self.energy_me)
        display.draw_battle_area()

        display.set_text("독일어욕", 650, 525, lang='kor', font_size=40)
        display.set_text("검은곰어택", 920, 525, lang='kor', font_size=40)
        display.set_text("사이보그펀치", 650, 615, lang='kor', font_size=40)
        display.set_text("사직서 제출", 920, 615, lang='kor', font_size=40)
        x = 0
        y = 0
        if self.select_x == 1:
            x = 640
        elif self.select_x == -1:
            x = 910
        if self.select_y == 1:
            y = 545
        elif self.select_y == -1:
            y = 635
        display.draw_select_triangle(x, y)

    def stage_1_action_animation(self, display, action):
        display.clear()
        display.draw_dialog_area()
        display.set_image("Resources/boss.png", 1100, 50)
        display.set_text("Boss", 550, 20, font_size=50)
        display.draw_energy_bar(550, 100, self.energy_boss)
        display.set_text("Jannie", 100, 370, font_size=50)
        display.draw_energy_bar(100, 450, self.energy_me)
        if action == 1:
            if self.animation == False and self.done == False:
                self.current_x = self.from_x
                self.current_y = self.from_y
                display.blit_image(self.schwein.get_image(), self.from_x, self.from_y)
                self.music.play_sound(self.schwein.get_sound())
                self.animation = True
            elif self.animation == True and self.done == False:
                self.current_x = self.current_x + 30
                self.current_y = self.current_y - 5
                display.blit_image(self.schwein.get_image(), self.current_x, self.current_y)
                pygame.time.Clock().tick(30)
                if self.current_x >= self.end_x:
                    self.done = True
            if self.animation == True and self.done == True:
                display.blit_image(self.effect.get_image(), self.current_x + 150, self.current_y)
                display.set_text("부장은 독일어를 이해하지 못했다.", 150, 530, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                display.set_text("효과는 미미햇다.", 150, 615, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                self.animation = False
                self.done = False
                return 1

        elif action == 2:
            #animation 검은곰어택
            if self.animation == False and self.done == False:
                self.current_x = 1000
                self.current_y = 150
                display.blit_image(self.bear.get_image(), 700, 200)
                self.music.play_sound(self.bear.get_sound())
                self.animation = True
            elif self.animation == True and self.done == False:
                display.blit_image(self.bear.get_image(), 700, 200)
                self.current_x = self.current_x + 10
                self.current_y = self.current_y + 5
                display.draw_line([1000, 50], [self.current_x, self.current_y-100])
                display.draw_line([1000, 150], [self.current_x, self.current_y])
                display.draw_line([1000, 250], [self.current_x, self.current_y+100])
                pygame.time.Clock().tick(60)
                if self.current_x >= 1300:
                    self.done = True
            if self.animation == True and self.done == True:
                display.set_text("꾸어어어어어어엉!!", 150, 530, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                display.set_text("그럭저럭 데미지가 있는듯하다.", 150, 615, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(5)
                self.animation = False
                self.done = False
                return 1
        elif action == 3:
            #animation 사이보그 펀치
            if self.animation == False and self.done == False:
                self.current_x = 1
                display.blit_image(self.cyborg.get_image(), 500, -150)
                self.music.play_sound(self.cyborg.get_sound())
                self.animation = True
            elif self.animation == True and self.done == False:
                display.blit_image(self.cyborg.get_image(), 500, -150)
                #타격 이펙트
                for i in range(int(self.current_x / 5 + 1)):
                    display.blit_image(self.effect.get_image(), i*100 + 1000, self.end_y + i*10)
                    display.blit_image(self.effect.get_image(), i*100 + 1000, self.end_y + i*20 + 100)
                self.current_x = self.current_x + 1
                pygame.time.Clock().tick(30)
                if self.current_x >= 50:
                    self.done = True
            if self.animation == True and self.done == True:
                display.set_text("뀨엑!!!!", 150, 530, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                display.set_text("매우 아파한다...", 150, 615, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                self.animation = False
                self.done = False
                return 1
        elif action == 4:
            #animation 사직서 제출
            if self.animation == False and self.done == False:
                self.current_x = self.from_x
                self.current_y = self.from_y
                display.blit_image(self.resign.get_image(), self.from_x, self.from_y)
                self.animation = True
            elif self.animation == True and self.done == False:
                self.current_x = self.current_x + 30
                self.current_y = self.current_y - 5
                display.blit_image(self.resign.get_image(), self.current_x, self.current_y)
                pygame.time.Clock().tick(30)
                if self.current_x >= self.end_x:
                    self.done = True
            if self.animation == True and self.done == True:
                display.blit_image(self.effect.get_image(), self.current_x + 150, self.current_y)
                display.set_text("안돼!! 설 선물은 너가 필요해!!!", 150, 530, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                display.set_text("효과는 굉장했다!!!", 150, 615, lang='kor', mode='each')
                pygame.time.Clock().tick(1)
                pygame.time.Clock().tick(1)
                self.animation = False
                self.done = False
                return 1
        elif action == 5:
            #animation 부장 어택
            self.current_x = 650
            self.current_y = 100
            display.set_text("부장의 갑작스러운 공격!!!", 150, 530, lang='kor', mode='each')
            pygame.time.Clock().tick(1)
            display.set_text("설 선물 엑셀로 준비해오세요!!!", 150, 615, lang='kor', mode='each')
            pygame.time.Clock().tick(1)
            display.blit_image(self.excel.get_image(), self.from_x, self.from_y)
            self.music.play_sound(self.excel.get_sound())

            for i in range(20):
                self.current_x = self.current_x - 25
                self.current_y = self.current_y + 5
                display.clear()
                display.blit_image(self.excel.get_image(), self.current_x, self.current_y)
                display.draw_dialog_area()
                display.set_image("Resources/boss.png", 1100, 50)
                display.draw_energy_bar(550, 100, self.energy_boss)
                display.set_text("Jannie", 100, 370, font_size=50)
                display.draw_energy_bar(100, 450, self.energy_me)
                display.set_text("부장의 갑작스러운 공격!!!", 150, 530, lang='kor')
                display.set_text("설 선물 엑셀로 준비해오세요!!!", 150, 615, lang='kor')
                pygame.display.update()
                pygame.time.Clock().tick(30)

            display.draw_dialog_area()
            pygame.display.update()
            display.set_text("Jannie는 큰 스트레스를 받았다...", 150, 530, lang='kor', mode='each')
            pygame.time.Clock().tick(1)
            display.set_text("힘내 Jannie!!!!!", 150, 615, lang='kor', mode='each')
            pygame.time.Clock().tick(1)
            pygame.time.Clock().tick(1)
            return 1
        return 0

    def stage_1_already_used(self, display):
        display.draw_dialog_area()
        display.set_text("이미 사용한 기술입니다.", 150, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)


    def stage_1_ending(self, display):
        display.clear()
        display.draw_dialog_area()
        display.set_text("안돼!!!", 150, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("삼성왕국이 무너진다!!!", 150, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)

        #animation
        display.set_image("Resources/samsung.png", 300, 100)
        for i in range(60):
            display.clear()
            x = random.randrange(-20, 21)
            y = random.randrange(-20, 21)
            display.draw_dialog_area()
            display.set_text("안돼!!!", 150, 530, lang='kor')
            display.set_text("삼성왕국이 무너진다!!!", 150, 610, lang='kor')
            display.set_image("Resources/samsung.png", 300+x, 100+y)
            pygame.display.update()
            pygame.time.Clock().tick(60)

        pygame.time.Clock().tick(1)
        display.clear()
        display.draw_dialog_area()
        display.set_image("Resources/samsung_dest.png", 350, 0)
        pygame.display.update()
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("삼성의 잔해에서 선물을 발견하였다!!!", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("(선물을 수령하고 SPACE를 누르시오)", 120, 610, lang='kor', mode='each')






    ############################################################################################################
    # stage 2 functions
    def stage_2_intro(self, display):
        display.clear()
        display.set_text("그렇게 악의 기업 삼성을 물리친 Jannie는", 100, 130, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("독일로 가서 대학원에 진학하기위해", 100, 230, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("독일어 공부를 하게 되는데......", 100, 330, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("Press SPACE", 500, 500, font_size = 50)

    def stage_2_set_UI(self, display):
        display.clear()
        self.music.load_music("Resources/ein-prosit.mp3")
        self.music.play_music()
        display.set_image("Resources/goethe.jpg", 0, 0)
        display.set_image("Resources/tomas.png", 100, 50)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("구텐탁 Jannie, 나는 토마스 밀러", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("당신의 Deutsch 실력 test 할꺼에요", 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("빈칸에 알맞는 Wort를 써봐요", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("대문자 입력은 안되니까 소문자로 해요", 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("7개 이상 맞춰야 통과다", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("그럼 시작!!!!", 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)

    def stage_2_set_problem(self, display):
        display.clear()
        display.set_image("Resources/probleme/answer.png", 300, 500)
        num = random.randrange(0, 15)
        if self.problem[num] == 0:
            path = "Resources/probleme/" + str(num+1) + ".png"
            display.set_image(path, 0, 50)
            self.problem[num] = 1
            self.correct_answer = self.answers[num]
            return 1
        return 0

    def stage_2_result(self, display):
        display.clear()
        display.set_image("Resources/goethe.jpg", 0, 0)
        display.set_image("Resources/tomas.png", 100, 50)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("결과를 발표하겠습니다!", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("맞힌 Nummer : " + str(self.correct), 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)


    def stage_2_pass(self, display):
        display.clear()
        display.set_image("Resources/goethe.jpg", 0, 0)
        display.set_image("Resources/tomas.png", 100, 50)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("Wunderbar! 훌륭합니다!", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("Sie는 독일에 올 자격 haben", 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)

    def stage_2_fail(self, display):
        display.clear()
        display.set_image("Resources/goethe.jpg", 0, 0)
        display.set_image("Resources/tomas_angry.png", 100, 50)
        display.draw_dialog_area()
        pygame.display.update()
        display.set_text("흠...... Nein......", 120, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("다시 복습하고 도전하도록 하세요!", 120, 610, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        for i in range(15):
            self.problem[i] = 0

    def stage_2_ending(self, display):
        display.clear()
        self.music.stop_music()
        display.set_text("그렇게 Thomas muller에게 인정받으며", 100, 130, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("독일어 공부를 마친 Jannie는", 100, 230, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("유창한 독일어 실력을 가지게 되었고", 100, 330, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("독일에 갈 준비를 완료하였다.", 100, 430, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("열심히 한 Jannie에게 선물을 증정한다.", 100, 530, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("(선물을 수령하고 SPACE를 누르시오)", 100, 630, lang='kor', mode='each')


    ##################################################################################################
    #chapter 3

    def stage_3_intro(self, display):
        display.clear()
        display.set_text("Jannie는 독일에 가기전...", 100, 130, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("넓은 독일에서 편안하게 이동하기 위해", 100, 230, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("20살에도 따지 않은 운전면허를 대비해", 100, 330, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("운전 연습을 하게 되는데......", 100, 430, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
        display.set_text("Press SPACE", 500, 550, font_size = 50)

    def stage_3_set_UI(self, display):
        display.clear()
        display.set_text("실사와 같은 좋은 그래픽을 위해", 120, 130, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("새로운 세상으로 당신을 초대합니다.", 120, 230, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("80점 이상시 합격입니다.", 120, 330, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        display.set_text("↑↓←→ : 움직임", 120, 430, lang='kor', mode='each')
        display.set_text("SPACE : 가속", 120, 530, lang='kor', mode='each')
        display.set_text("Z, C : 좌, 우 깜빡이", 120, 630, lang='kor', mode='each')
        pygame.time.Clock().tick(1)
        pygame.time.Clock().tick(1)
